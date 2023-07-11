from moviepy.editor import *
import os 
from gtts import gTTS
import csv
import soundfile as sf
from moviepy.config import change_settings
from moviepy.video.fx.resize import resize
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def generate_video(theme, part_1, part_2, full_text, tts_path):
    tts_clip = AudioFileClip(tts_path)  
    fixed_tts_clip = CompositeAudioClip([tts_clip])

    background_images = []
    background_images.append(ImageClip("background_image.jpg").set_duration(tts_clip.duration + 2))

    base = concatenate_videoclips(background_images, method="compose")
    
    _size = 1080, 1920

    #text_clip = TextClip(full_text, font="Arial", fontsize=50, color="white")
    #text_clip = text_clip.set_position("center").set_duration(tts_clip.duration)

    theme_clip = TextClip(theme, font="Arial-Bold", fontsize=80, color="white", stroke_width=2, stroke_color="black")
    theme_clip = theme_clip.set_position(("center", 80))
    theme_clip = theme_clip.set_duration(tts_clip.duration + 2)

    part_1_clip = TextClip(part_1, font="Arial", fontsize=100, align="west", color="white", kerning=5, method="caption")
    part_1_clip = part_1_clip.set_duration(3)
    part_1_clip = part_1_clip.set_position("center")
    part_1_clip_bg = ColorClip(size=part_1_clip.size, color=(0, 0, 0))
    part_1_clip_bg = part_1_clip_bg.set_duration(3)
    part_1_clip_bg = part_1_clip_bg.set_position("center")

    part_2_clip = TextClip(part_2, font="Arial", fontsize=100, align="west", color="white", kerning=5, method="caption")
    part_2_clip = part_2_clip.set_start(4)
    part_2_clip = part_2_clip.set_duration(4)
    part_2_clip = part_2_clip.set_position("center")

    part_2_clip_bg = ColorClip(size=part_2_clip.size, color=(0, 0, 0))
    part_2_clip_bg = part_2_clip_bg.set_start(4)
    part_2_clip_bg = part_2_clip_bg.set_duration(4)
    part_2_clip_bg = part_2_clip_bg.set_position("center")

    final_video_path = "final_videos/" + full_text + ".mp4"
    final_video = CompositeVideoClip([base, theme_clip, part_1_clip_bg, part_1_clip, part_2_clip_bg, part_2_clip])
    final_video.audio = fixed_tts_clip
    final_video.write_videofile(final_video_path, codec="h264_nvenc", fps=24)
    return()

# 700x45

def main():
    _csv_file = input("csv file path:")
    if(_csv_file):
        with open(_csv_file, 'r') as file: 
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if(len(row) >= 3):
                    film_theme = row[0]
                    film_st_part = row[1]
                    film_nd_part = row[2]
                    full_text =  f"{film_theme} {film_st_part} {film_nd_part}"
                    tts = gTTS(text=full_text, lang="en", tld="com.au", slow=False)
                    tts_path = "tts_voices/" + full_text + ".mp3"
                    tts.save(tts_path)
                    generate_video(film_theme, film_st_part, film_nd_part, full_text, tts_path)
    return




if __name__ == "__main__": 
    main()