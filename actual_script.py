from moviepy.editor import *
import os 
import csv
import soundfile as sf
from moviepy.config import change_settings
from moviepy.video.fx.resize import resize
import pyttsx3
import random
import glob

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
#C:\Users\sh0cky\Desktop\YT AUTOMATIZATION\SHORT-VIDEOS\data.csv
def generate_video(theme, part_1, part_2, full_text, tts_path, background_images):
    tts_clip = AudioFileClip(tts_path)  
    fixed_tts_clip = CompositeAudioClip([tts_clip])
     # Select a random background image from the list
    background_image_path = random.choice(background_images)
    background_image_clip = ImageClip(background_image_path).set_duration(tts_clip.duration + 2)

    base = concatenate_videoclips([background_image_clip], method="compose")

    part_1_clip = TextClip(part_1, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")
    part_1_clip = part_1_clip.set_duration(3)
    part_1_clip = part_1_clip.set_position("center")
    part_1_clip_bg = ColorClip(size=part_1_clip.size, color=(0, 0, 0))
    part_1_clip_bg = part_1_clip_bg.set_duration(3)
    part_1_clip_bg = part_1_clip_bg.set_position("center")

    part_2_clip = TextClip(part_2, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")
    part_2_clip = part_2_clip.set_start(4)
    part_2_clip = part_2_clip.set_duration(4)
    part_2_clip = part_2_clip.set_position("center")

    part_2_clip_bg = ColorClip(size=part_2_clip.size, color=(0, 0, 0))
    part_2_clip_bg = part_2_clip_bg.set_start(4)
    part_2_clip_bg = part_2_clip_bg.set_duration(8)
    part_2_clip_bg = part_2_clip_bg.set_position("center")

    final_video_path = "final_videos/" + full_text + ".mp4"
    final_video = CompositeVideoClip([base, part_1_clip_bg, part_1_clip, part_2_clip_bg, part_2_clip])

    final_video.audio = fixed_tts_clip
    final_video.write_videofile(final_video_path, codec="h264_nvenc", fps=24)

    # Delete the old tts sound file 
    os.remove(tts_path)

    #Finall message
    print(f"Video was rendered at the path {final_video_path}")

    return

# 700x45

def main():
    _csv_file = input("CSV file path: ")
    _image_dir = input("Background image directory: ")
    
    if _csv_file and _image_dir:
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
                    
                    engine = pyttsx3.init()
                    rate = engine.getProperty('rate')
                    voices = engine.getProperty('voices')
                    engine.setProperty("voice", 'en-us')
                    engine.setProperty('rate', rate-80)
                    engine.setProperty('voice', voices[0].id)
                    engine.save_to_file(full_text, tts_path)
                    engine.runAndWait()
                    
                    background_images = glob.glob(os.path.join(_image_dir, '*.jpg'))

                    generate_video(film_theme, film_st_part, film_nd_part, full_text, tts_path, background_images)

    return

if __name__ == "__main__":
    main()
