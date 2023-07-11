from moviepy.editor import *
import os 
import csv
import soundfile as sf
from moviepy.config import change_settings
from moviepy.video.fx.resize import resize
import pyttsx3
import time

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def generate_video(theme, part_1, part_2, full_text, tts_path):
    # Create a Text-to-Speech engine
    engine = pyttsx3.init()

    # Set the voice speed (rate)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 80)

    # Save the synthesized speech to a file
    engine.save_to_file(full_text, tts_path)
    engine.runAndWait()

    # Get the duration of the text-to-speech audio clip
    audio_info = sf.info(tts_path)
    tts_duration = audio_info.duration

    # Set the speed of the audio clip
    audio_speed = 0.8  # Adjust the speed as needed

    # Prepare video clips
    part_1_clip = TextClip(part_1, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")
    part_2_clip = TextClip(part_2, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")

    # Modify the duration of the video clips based on the speed
    part_1_duration = 3 * tts_duration / audio_speed  # Adjust the duration as needed
    part_2_duration = 4 * tts_duration / audio_speed  # Adjust the duration as needed

    # Set the durations of the video clips
    part_1_clip = part_1_clip.set_duration(part_1_duration)
    part_2_clip = part_2_clip.set_duration(part_2_duration)

    # Prepare base video
    background_images = []
    background_images.append(ImageClip("background_image.jpg").set_duration(tts_duration + 2))
    base = concatenate_videoclips(background_images, method="compose")

    # Set up final video
    final_video_path = "final_videos/" + full_text + ".mp4"
    final_video = CompositeVideoClip([base, part_1_clip, part_2_clip])

    # Start the text-to-speech audio at the beginning
    tts_audio = AudioFileClip(tts_path)

    # Create a silent audio clip for the pause duration
    pause_duration = 1  # Duration of the pause (in seconds)
    pause_audio = AudioFileClip(os.devnull, duration=pause_duration)

    # Insert the pause in the audio clip
    audio_with_pause = concatenate_audioclips([tts_audio.subclip(0, 3), pause_audio, tts_audio.subclip(4)])

    # Set the audio for the final video
    final_video = final_video.set_audio(audio_with_pause)

    # Write the final video file
    final_video.write_videofile(final_video_path, codec="h264_nvenc", fps=24)

    return

# 700x45

def main():
    _csv_file = input("csv file path:")
    if _csv_file:
        with open(_csv_file, 'r') as file: 
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if len(row) >= 3:
                    film_theme = row[0]
                    film_st_part = row[1]
                    film_nd_part = row[2]
                    full_text = f" {film_st_part} {film_nd_part}"
                    tts_path = "tts_voices/" + full_text + ".mp3"
                    generate_video(film_theme, film_st_part, film_nd_part, full_text, tts_path)
    return

if __name__ == "__main__":
    main()
