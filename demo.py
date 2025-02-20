import argparse
import pathlib
import cv2
import time
import torch
import csv
import os
from l2cs import select_device, Pipeline, render


# PIPELINE NOTICE: I have mistakenly processed the frames at a rate of 10 FPS with videos ending in "_gaze_data-sw"(all completed before PMAR13), "-sw_bb"(all completed), and "-ms_bb"(all completed before HKHR12)
# To make it 3 fps, you must process these videos by intervals of 10 frames as they are a total of 8550 frames. --> refer to csv files of "_gaze_raw" and "_bound" respectively


CWD = pathlib.Path.cwd()
sw_files = {}

ms_files = {}

def parse_args():
    parser = argparse.ArgumentParser(description='Gaze evaluation using model pretrained with L2CS-Net on Gaze360.')
    parser.add_argument('--device', help='Device to run model: cpu or gpu:0', default='cpu', type=str)
    parser.add_argument('--snapshot', help='Path of model snapshot.', default='output/L2CSNet_gaze360.pkl', type=str)
    parser.add_argument('--output_dir', help='Directory to save csv files.', default='output_csv', type=str)
    parser.add_argument('--arch', help='Network architecture, can be: ResNet18, ResNet34, ResNet50, ResNet101, ResNet152', default='ResNet50', type=str)
    
    args = parser.parse_args()
    return args

def draw_headbox(frame, bbox, color=(0, 255, 0), thickness=2):
    x, y, w, h = map(int, bbox)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

def render(frame, gaze_results_container):
    try:
        for i, bbox in enumerate(gaze_results_container.bboxes):
            print(f"Rendered bbox: {bbox}")

            score = gaze_results_container.scores[i]
            pitch = gaze_results_container.pitch[i]
            yaw = gaze_results_container.yaw[i]

            draw_headbox(frame, bbox)

            text = f'Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Score: {score:.2f}'
            cv2.putText(frame, text, (int(bbox[0]), int(bbox[1]) - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0), 1)
    except Exception as e:
        print(f"Error in rendering the frame: {e}")
    return frame

def process_video(video_path, output_csv_path, output_video_path, gaze_pipeline):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")

    frame_numbers_to_process = range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 10)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 3, (width, height))

    with open(output_csv_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Frame', 'x', 'y', 'width', 'height', 'Pitch', 'Yaw', 'Score'])

        with torch.no_grad():
            frame_count = 0
            
            while True:
                success, frame = cap.read()
                if not success:
                    print("Failed to obtain frame or end of video.")
                    break
                
                if frame_count not in frame_numbers_to_process:
                    frame_count += 1
                    continue

                start_fps = time.time()
                results = gaze_pipeline.step(frame)
                frame = render(frame, results)

                for i, bbox in enumerate(results.bboxes):
                    score = results.scores[i]
                    pitch = results.pitch[i]
                    yaw = results.yaw[i]
                    x, y, w, h = map(int, bbox)
                    csv_writer.writerow([frame_count, x, y, w, h, pitch, yaw, score])

                frame_count += 1

                myFPS = 1.0 / (time.time() - start_fps)
                cv2.putText(frame, f'FPS: {myFPS:.1f}', (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1, cv2.LINE_AA)

                out.write(frame)

    cap.release()
    out.release()

if __name__ == '__main__':
    args = parse_args()
    torch.backends.cudnn.enabled = True
    arch = args.arch

    gaze_pipeline = Pipeline(
        weights=CWD / args.snapshot,
        arch=args.arch,
        device=select_device(args.device, batch_size=1)
    )

    # for name, video_path in sw_files.items():
    #     print(f"Processing {name}...")
    #     video_dir = os.path.dirname(video_path)  # Get the directory of the video
    #     output_csv_path = os.path.join(video_dir, f'{name}_gaze_raw-sw.csv') # Save CSV in the same directory
    #     output_video_path = os.path.join(args.output_dir, f'{name}_output.avi')
    #     process_video(video_path, output_csv_path, output_video_path, gaze_pipeline)
    #     print(f"Finished processing {name}. CSV saved to {output_csv_path}, video saved to {output_video_path}")
        
    for name, video_path in ms_files.items():
        print(f"Processing {name}...")
        video_dir = os.path.dirname(video_path)  # Get the directory of the video
        output_csv_path = os.path.join(video_dir, f'{name}_gaze_raw-ms.csv') # Save CSV in the same directory
        output_video_path = os.path.join(args.output_dir, f'{name}_output.avi')
        process_video(video_path, output_csv_path, output_video_path, gaze_pipeline)
        print(f"Finished processing {name}. CSV saved to {output_csv_path}, video saved to {output_video_path}")