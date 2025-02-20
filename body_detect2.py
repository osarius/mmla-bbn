import torch
import cv2
import numpy as np
import csv
from scipy.spatial.distance import cdist

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

sw_files = {}

ms_files = {}


def safely_delete_keys(dictionary, keys):
    for key in keys:
        if key in dictionary:
            del dictionary[key]

# Function to detect glasses
def detect_glasses(image, bbox):
    x1, y1, x2, y2 = bbox
    face_region = image[y1:y2, x1:x2]
    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)

    glasses = glasses_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(glasses) > 0:
        return "Wearing Glasses"
    return "No Glasses"

# Function to detect skin color
def detect_skin_color(image, bbox):
    x1, y1, x2, y2 = bbox
    face_region = image[y1:y2, x1:x2]
    if face_region.size == 0:
        return "Unknown Skin"
    
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

    skin_colors_ranges = {
        "Fair": [(0, 20, 70), (20, 255, 255)],
        "Light": [(0, 40, 50), (50, 255, 255)],
        "Medium": [(20, 50, 50), (30, 255, 255)],
        "Olive": [(30, 40, 40), (40, 255, 255)],
        "Tan": [(10, 50, 50), (20, 255, 200)],
        "Brown": [(10, 100, 30), (20, 255, 150)],
        "Deep": [(0, 100, 20), (10, 255, 100)]
    }

    color_counts = {}
    for color, (lower, upper) in skin_colors_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        color_counts[color] = cv2.countNonZero(mask)

    if color_counts:
        dominant_color = max(color_counts, key=color_counts.get)
        return dominant_color + " Skin"
    return "Unknown Skin"

# Function to detect hair color
def detect_hair(image, bbox):
    x1, y1, x2, y2 = bbox
    face_region = image[y1:y2, x1:x2]
    if face_region.size == 0:
        return "Unknown Hair"
    
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

    hair_colors_ranges = {
        "Black": [(0, 0, 0), (180, 255, 30)],
        "Blonde": [(20, 40, 100), (40, 255, 255)],
        "Brown": [(10, 100, 20), (20, 255, 200)],
        "Red": [(0, 50, 50), (10, 255, 255)],
        "Gray": [(0, 0, 50), (180, 15, 170)]
    }

    color_counts = {}
    for color, (lower, upper) in hair_colors_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        color_counts[color] = cv2.countNonZero(mask)

    if color_counts:
        dominant_color = max(color_counts, key=color_counts.get)
        return dominant_color + " Hair"
    return "Unknown Hair"

# Function to detect face features
def detect_face(image, bbox):
    try:
        skin_color_description = detect_skin_color(image, bbox)
        hair_description = detect_hair(image, bbox)
        return f'{skin_color_description} & {hair_description}'
    except cv2.error as e:
        print(f"Error processing face: {e}")
        return "Unknown Skin & Unknown Hair"

# Paths (included in a loop)
for idx in ms_files:
    input_video_path = ms_files[idx]
    output_video_path = f'../BBN_test_D_Spikol/{idx}/{idx}-ms_test-revised2.mp4'
    output_csv_path = f'../BBN_test_D_Spikol/{idx}/{idx}-ms_bound-revised2.csv'
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_interval = 10
    frame_index = 0
    person_counter = 1
    distance_threshold = 50.0
    max_persons = 3
    tracked_persons = {}

    with open(output_csv_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Frame', 'Label', 'x1', 'y1', 'x2', 'y2', 'Confidence'])

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % frame_interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model(rgb_frame)
                boxes = results.xyxy[0].cpu().numpy()
                current_positions = []

                for box in boxes:
                    x1, y1, x2, y2, confidence, class_id = box
                    if class_id == 0 and confidence > 0.5:  # Class ID 0 is person
                        # Adjust the lower corner's y-coordinate (y2) to be 30% higher
                        y_diff = y2 - y1
                        y2 = int(y2 - 0.5 * y_diff)
                        y2 = max(y2, y1)  # Ensure y2 is still lower or equal to y1
                        y2 = min(y2, frame_height - 1)  # Ensure y2 is within image boundaries

                        current_positions.append((int(x1), int(y1), int(x2), int(y2), confidence))

                print(f"[DEBUG] Frame {frame_index}: Detected {len(current_positions)} persons")

                current_positions_labels = {}
                keys_to_delete = []

                if tracked_persons:
                    previous_centers = np.array([((x1 + x2) // 2, (y1 + y2) // 2) for (x1, y1, x2, y2, _) in tracked_persons.values()])
                    current_centers = np.array([((x1 + x2) // 2, (y1 + y2) // 2) for (x1, y1, x2, y2, _) in current_positions])

                    if len(previous_centers) > 0 and len(current_centers) > 0:
                        distances = cdist(previous_centers, current_centers)

                        for i, (x1, y1, x2, y2, confidence) in enumerate(current_positions):
                            if len(previous_centers) > 0:
                                min_index = np.argmin(distances[:, i])
                                min_distance = distances[min_index, i]

                                if min_distance < distance_threshold:
                                    assigned_label = list(tracked_persons.values())[min_index][4]
                                    previous_key = list(tracked_persons.keys())[min_index]
                                    keys_to_delete.append(previous_key)
                                else:
                                    if len(tracked_persons) < max_persons:
                                        face_description = detect_face(frame, (x1, y1, x2, y2))
                                        assigned_label = face_description
                                        person_counter += 1
                                    else:
                                        continue
                            else:
                                if len(tracked_persons) < max_persons:
                                    face_description = detect_face(frame, (x1, y1, x2, y2))
                                    assigned_label = face_description
                                    person_counter += 1
                                else:
                                    continue

                            combined_label = assigned_label

                            if combined_label != "Unknown Skin & Unknown Hair":
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, f'{combined_label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                csv_writer.writerow([frame_index, combined_label, x1, y1, x2, y2, f'{confidence:.2f}'])
                                print(f"[DEBUG] Writing to CSV: Frame {frame_index}, BBox: ({x1}, {y1}, {x2}, {y2}), Confidence: {confidence}, Label: {combined_label}")
                                current_positions_labels[i] = (x1, y1, x2, y2, combined_label)

                        safely_delete_keys(tracked_persons, keys_to_delete)

                    tracked_persons.update(current_positions_labels)
                else:
                    for i, (x1, y1, x2, y2, confidence) in enumerate(current_positions):
                        if len(tracked_persons) < max_persons:
                            face_description = detect_face(frame, (x1, y1, x2, y2))
                            assigned_label = face_description
                            combined_label = assigned_label

                            if combined_label != "Unknown Skin & Unknown Hair":
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, f'{combined_label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                csv_writer.writerow([frame_index, combined_label, x1, y1, x2, y2, f'{confidence:.2f}'])
                                print(f"[DEBUG] Writing to CSV: Frame {frame_index}, BBox: ({x1}, {y1}, {x2}, {y2}), Confidence: {confidence}, Label: {combined_label}")
                                current_positions_labels[i] = (x1, y1, x2, y2, combined_label)
                        else:
                            continue

                    tracked_persons.update(current_positions_labels)

            out.write(frame)
            frame_index += 1
            print(f'Processing frame {frame_index}/{frame_count}', end='\r')

        cap.release()
        out.release()

        print("Detection complete. Output video saved to", output_video_path)
        print("Bounding boxes saved to", output_csv_path)