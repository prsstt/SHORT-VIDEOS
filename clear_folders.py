import glob
import os 

final_videos_files = glob.glob("final_videos/*.mp4")
tts_voices_files = glob.glob("tts_voices/*.mp3")
temp_files = glob.glob(".mp3")

all_files = [final_videos_files, tts_voices_files, temp_files ]

for files in all_files:
    for file in files:
        print(f"Removing {file}")
        os.remove(file)


print("Cleaning complete :)")