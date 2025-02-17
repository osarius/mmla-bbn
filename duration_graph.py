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

ms_body = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-ms_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-ms_bound.csv",-->finished!
    #  "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11-ms_bound.csv",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14-gaze_ms.csv","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11-gaze_ms.csv",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18-gaze_ms.csv","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11-gaze_ms.csv",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14-gaze_ms.csv",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12-gaze_ms.csv",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11-gaze_ms.csv","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12-gaze_ms.csv",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13-gaze_ms.csv","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17-gaze_ms.csv",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11-gaze_ms.csv","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18-gaze_ms.csv",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11-gaze_ms.csv","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP-gaze_ms.csv",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18-gaze_ms.csv","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13-gaze_ms.csv",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13-gaze_ms.csv",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12-gaze_ms.csv",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12-gaze_ms.csv",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17-gaze_ms.csv",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18-gaze_ms.csv","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12-gaze_ms.csv",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12-gaze_ms.csv","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12-gaze_ms.csv",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11-gaze_ms.csv","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18-gaze_ms.csv",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18-gaze_ms.csv","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12-gaze_ms.csv",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11-gaze_ms.csv","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17-gaze_ms.csv",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11-gaze_ms.csv","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12-gaze_ms.csv",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11-gaze_ms.csv","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13-gaze_ms.csv",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12-gaze_ms.csv","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13-gaze_ms.csv",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12-gaze_ms.csv","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13-gaze_ms.csv",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12-gaze_ms.csv","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17-gaze_ms.csv",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11-gaze_ms.csv","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11-gaze_ms.csv",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12-gaze_ms.csv","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11-gaze_ms.csv",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17-gaze_ms.csv","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12-gaze_ms.csv",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18-gaze_ms.csv","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11-gaze_ms.csv",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12-gaze_ms.csv","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12-gaze_ms.csv",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11-gaze_ms.csv","KESK12":"../BBN_test_D_Spikol/KESK12/KESK12-gaze_ms.csv",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17-gaze_ms.csv","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12-gaze_ms.csv",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-gaze_ms.csv","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-gaze_ms.csv",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12-gaze_ms.csv","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15-gaze_ms.csv",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12-gaze_ms.csv","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12-gaze_ms.csv",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11-gaze_ms.csv","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18-gaze_ms.csv",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18-gaze_ms.csv","MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13-gaze_ms.csv",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16-gaze_ms.csv","MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18-gaze_ms.csv",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13-gaze_ms.csv","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17-gaze_ms.csv",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13-gaze_ms.csv","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13-gaze_ms.csv",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16-gaze_ms.csv","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12-gaze_ms.csv",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13-gaze_ms.csv","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12-gaze_ms.csv",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12-gaze_ms.csv","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18-gaze_ms.csv",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12-gaze_ms.csv","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18-gaze_ms.csv",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17-gaze_ms.csv", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14-gaze_ms.csv",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18-gaze_ms.csv","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16-gaze_ms.csv",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13-gaze_ms.csv","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17-gaze_ms.csv",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18-gaze_ms.csv","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13-gaze_ms.csv",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11-gaze_ms.csv","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13-gaze_ms.csv",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17-gaze_ms.csv","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11-gaze_ms.csv",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13-gaze_ms.csv","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17-gaze_ms.csv",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17-gaze_ms.csv","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM-gaze_ms.csv",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18-gaze_ms.csv","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11-gaze_ms.csv",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18-gaze_ms.csv","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12-gaze_ms.csv",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13-gaze_ms.csv","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11-gaze_ms.csv",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17-gaze_ms.csv","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS-gaze_ms.csv",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18-gaze_ms.csv","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13-gaze_ms.csv",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17-gaze_ms.csv","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14-gaze_ms.csv",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13-gaze_ms.csv","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13-gaze_ms.csv",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11-gaze_ms.csv","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18-gaze_ms.csv",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18-gaze_ms.csv","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17-gaze_ms.csv",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17-gaze_ms.csv","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA-gaze_ms.csv",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16-gaze_ms.csv",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17-gaze_ms.csv", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17-gaze_ms.csv","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13-gaze_ms.csv",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13-gaze_ms.csv","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18-gaze_ms.csv",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17-gaze_ms.csv","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18-gaze_ms.csv",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17-gaze_ms.csv","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17-gaze_ms.csv",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13-gaze_ms.csv","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11-gaze_ms.csv",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13-gaze_ms.csv","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18-gaze_ms.csv",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12-gaze_ms.csv"}

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