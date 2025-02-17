from collections import OrderedDict
import csv
import pandas as pd
import cv2
import os

sw_body = {}

sw_faces = {}

# input medical student csv files from body_detection.py
ms_body = {}

# input medical student csv files from demo.py
ms_faces = {}

ms_videos = {}


           
def is_gaze_in_bbox(gaze_x, gaze_y, bbox):
    x1, y1, x2, y2 = bbox
    return x1 <= gaze_x <= x2 and y1 <= gaze_y <= y2
                
def process_files(idx):
    file_path_bound = f'../BBN_test_D_Spikol/{idx}/{idx}-sw_bound-revised2.csv'
    file_path_gaze = f'../BBN_test_D_Spikol/{idx}/{idx}_gaze_raw-sw.csv'
    output_path = f'../BBN_test_D_Spikol/{idx}/{idx}-gaze.csv'

    try:
        df_bound = pd.read_csv(file_path_bound, on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path_bound}: {e}")
        return

    try:
        df_gaze = pd.read_csv(file_path_gaze)
    except Exception as e:
        print(f"Error reading {file_path_gaze}: {e}")
        return

    df_bound['Frame'] = df_bound['Frame'].astype(int)
    df_gaze['Frame'] = df_gaze['Frame'].astype(int)

    ordered_dict = OrderedDict()

    # append the subjects
    for _, row in df_bound.iterrows():
        key = row['Frame']
        values = row[1:].tolist()

        # if the frame scene is already in there
        if key in ordered_dict:
            ordered_dict[key].append(values)
        else:
            #otherwise, we're already in a new scene frame.
            ordered_dict[key] = [values]

    with open(output_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Frame', 'Label', 'x1', 'y1', 'x2', 'y2', 'Stares At'])
        
        # each row of the csv gaze file
        for _, row in df_gaze.iterrows():
            frame = row['Frame']
            gaze_x = row['x']
            gaze_y = row['y']

            stares_at = "N/A"
            
            # only assess frames that have bb data in them
            if frame in ordered_dict:
                 for bbox in ordered_dict[frame]:
                     label = bbox[0]
                     bbox_coords = bbox[1:5]
                     if is_gaze_in_bbox(gaze_x, gaze_y, bbox_coords):
                         stares_at = label
                         break

                 for bbox in ordered_dict[frame]:
                     csv_writer.writerow([
                         frame, bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], stares_at
                     ])
    print("done with " + idx + "\n")

for idx in sw_body:
    process_files(idx)
    
    
    
    
#TASK:

#create 100 frames in random sample, have 1-2 humans to rate who is looking at who
#create a binary list --> the target of who's looking at who. (eg. 3rd class being looking at nowhere)

#make 100 frames w/o arrows --> so that they don't assume by arrows.
#don't run by script, try to find a command that does it.
#ensure frame 65, make sure it strikes that frame from the original video.
