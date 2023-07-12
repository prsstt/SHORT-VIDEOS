import glob
import os 

final_videos_files = glob.glob("final_videos/*.mp4")
tts_voices_files = glob.glob("tts_voices/*.mp3")
temp_files = glob.glob(".mp3")

all_files = []
all_files.insert(final_videos_files, tts_voices_files, temp_files)

for file in all_files:
    os.remove(file)