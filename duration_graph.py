import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt
import pandas as pd
import os

def frames_to_mmss(frames, frame_rate=30):
    seconds = frames / frame_rate
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def convert_seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def read_and_validate_csv(filepath):
    try:
        data = pd.read_csv(filepath, header=None)
        data.columns = ['Frame', 'Label', 'x1', 'y1', 'x2', 'y2', 'Stares At']
        print(f"Successfully read {filepath}")
        
        # Ensure that Frame is treated as numeric
        data['Frame'] = pd.to_numeric(data['Frame'], errors='coerce')
        data = data.dropna(subset=['Frame'])
        data['Frame'] = data['Frame'].astype(int)
        
        return data
    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        return None

# Ensure the output directory exists
output_dir = "updated_stares-ms"
os.makedirs(output_dir, exist_ok=True)

ms_body = {}

tracker = {
    'Scenario': [],
    'SW Time': [],
    'MS Time': [],
    'Total Time': []
}

def calculate_durations(stares_df):
    try:
        if stares_df.empty:
            return stares_df
        
        stares_df = stares_df.sort_values(by='Frame').reset_index(drop=True)
        
        stares_df['Start'] = stares_df['Frame'] / 30
        stares_df['Duration'] = 0
        
        starts = []
        durations = []

        i = 0
        while i < len(stares_df):
            start_frame = stares_df.at[i, 'Frame']
            start_time = start_frame / 30
            end_time = start_time + 1/3
            j = i + 1
            duration = 1/3

            while j < len(stares_df) and stares_df.at[j, 'Frame'] == stares_df.at[j-1, 'Frame'] + 10:
                end_time += 1/3
                duration += 1/3
                j += 1
            
            starts.append(start_time)
            durations.append(duration)
            i = j
        
        stares_df['Start'] = pd.Series(starts)
        stares_df['Duration'] = pd.Series(durations)
        stares_df['End'] = stares_df['Start'] + stares_df['Duration']
        
        return stares_df
    except Exception as e:
        print(f"Error calculating durations: {e}")
        print(f"Details: stares_df is: {stares_df}")
        return None

tally_ms = 0.0
total_time_ms = 0.0

tally_sw = 0.0
total_time_sw = 0.0

for person_id, filepath in ms_body.items():
    try:
        # Read the CSV file
        data = read_and_validate_csv(filepath)
        if data is None or data.empty:
            print(f"No valid data for {person_id}")
            continue
        
        # Filter data for the specific "Stares At" conditions
        stares_medical_student_at_widow = data[(data['Label'] == 'Medical Student') & (data['Stares At'] == 'Widow')].copy()
        stares_social_worker_at_widow = data[(data['Label'] == 'Social Worker') & (data['Stares At'] == 'Widow')].copy()
        
        stares_medical_student_at_widow = calculate_durations(stares_medical_student_at_widow)
        stares_social_worker_at_widow = calculate_durations(stares_social_worker_at_widow)

        if stares_medical_student_at_widow is None or stares_social_worker_at_widow is None:
            print(f"Skipping person_id: {person_id} due to duration calculation error.")
            continue

        if 'Duration' not in stares_medical_student_at_widow.columns or 'Duration' not in stares_social_worker_at_widow.columns:
            print(f"Missing 'Duration' in DataFrame for {person_id}")
            continue
        
        # Sum the total staring times
        total_time_medical_student_at_widow = stares_medical_student_at_widow['Duration'].sum()
        total_time_social_worker_at_widow = stares_social_worker_at_widow['Duration'].sum()
        
        # Convert total times to MM:SS format
        time_medical_student_at_widow = convert_seconds_to_mmss(total_time_medical_student_at_widow)
        time_social_worker_at_widow = convert_seconds_to_mmss(total_time_social_worker_at_widow)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for _, row in stares_medical_student_at_widow.iterrows():
            ax.add_patch(plt.Rectangle((row['Start'], 0.5), row['Duration'], 0.5, color='blue'))
        
        for _, row in stares_social_worker_at_widow.iterrows():
            ax.add_patch(plt.Rectangle((row['Start'], -0.5), row['Duration'], 0.5, color='red'))
        
        # Adjust x-axis to reflect time in MM:SS
        frame_rate = 30  # frames per second
        max_frame = max(data['Frame'])
        max_time_seconds = max_frame / frame_rate
        
        # Adding time labels to the x-axis
        num_ticks = 10  # number of ticks on the x-axis
        tick_positions = [i * (max_time_seconds / num_ticks) for i in range(num_ticks + 1)]
        tick_labels = [convert_seconds_to_mmss(pos) for pos in tick_positions]
        
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels)
        
        # Hide the y-axis ticks
        ax.yaxis.set_ticks([])
        
        # Autoscale and set limits
        ax.autoscale()
        ax.set_ylim(-1, 1)

        # Create legends with the time durations
        handles = [
            plt.Line2D([0], [0], color='blue', lw=4, label=f'Medical Student -> Widow: {time_medical_student_at_widow}'),
            plt.Line2D([0], [0], color='red', lw=4, label=f'Social Work Student -> Widow: {time_social_worker_at_widow}')
        ]
        ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.)
        
        # MEDICAL STUDENT TIME TALLYING
        total_minutes_ms = float(time_medical_student_at_widow[:2]) * 60.0
        total_seconds_ms = float(time_medical_student_at_widow[3:])
        float_seconds_ms = total_minutes_ms + total_seconds_ms
        
        if float_seconds_ms != 0.0:
            tally_ms += 1.0
            total_time_ms += float_seconds_ms
            
        # SOCIAL WORKER TIME TALLYING
        total_minutes_sw = float(time_social_worker_at_widow[:2]) * 60.0
        total_seconds_sw = float(time_social_worker_at_widow[3:])
        float_seconds_sw = total_minutes_sw + total_seconds_sw
        
        if float_seconds_sw != 0.0:
            tally_sw += 1.0
            total_time_sw += float_seconds_sw
        
        # Save the plot as a PNG file
        output_filename = os.path.join(output_dir, f"{person_id}_stare_duration_plot.png")
        plt.savefig(output_filename, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved plot for {person_id} as {output_filename}")

    except Exception as e:
        print(f"Error processing {person_id} with file {filepath}: {e}")
    
    tracker['Scenario'].append(person_id)
    tracker['SW Time'].append(total_time_medical_student_at_widow)
    tracker['MS Time'].append(total_time_social_worker_at_widow)
    tracker['Total Time'].append(max_time_seconds)
    
    source_file = ms_body[person_id]

    # Specify the path to the destination directory
    destination_directory = 'raw_duration_files'

    # Create the destination file path
    destination_file = os.path.join(destination_directory, f'{person_id}-gaze_ms.csv')
    
    shutil.copy(source_file, destination_file)
    print(f'File copied to {destination_file}')
    
df = pd.DataFrame(tracker)
file_name = 'data.csv'

df.to_csv(file_name, index=False)
        
        
print(f"Overall Average Staring Duration for Medical Student is {convert_seconds_to_mmss(total_time_ms / tally_ms)}")
print(f"Overall Average Staring Duration for Social Work Student is {convert_seconds_to_mmss(total_time_sw / tally_sw)}")

labels = 'Medical Student', 'Social Work Student'
sizes = [total_time_ms / tally_ms, total_time_sw / tally_sw]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Proportion of Average Times")

# plt.show()
plt.savefig("plotted average for stares", bbox_inches='tight')
plt.close(fig1)