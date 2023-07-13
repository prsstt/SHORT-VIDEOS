from moviepy.editor import *
import os 
import csv
import soundfile as sf
from moviepy.config import change_settings
from moviepy.video.fx.resize import resize
import pyttsx3
import soundfile as sf


change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
#C:\Users\sh0cky\Desktop\YT AUTOMATIZATION\SHORT-VIDEOS\data.csv
def generate_video(theme, part_1, part_2, full_text, tts_path):

    #tts_clip_theme = AudioFileClip(tts_path[0])
    tts_clip_part_1 = AudioFileClip(tts_path[1])
    tts_clip_part_2 = AudioFileClip(tts_path[2])  


    #potrzebne bylo do naprawienia bo tam coos nie gralo 
    file_1 = sf.SoundFile(tts_path[1])
    tts_clip_part_1_duration = int(file_1.frames / file_1.samplerate)
    file_2 = sf.SoundFile(tts_path[2])
    tts_clip_part_2_duration = int(file_2.frames / file_2.samplerate)


    background_images = []

    #trzeba tutaj duration ogarnac dobre bo cos mi nie pasuje
    background_images.append(ImageClip("bg_images/background_image.jpg").set_duration(tts_clip_part_1_duration + tts_clip_part_2_duration + 3))

    base = concatenate_videoclips(background_images, method="compose")
    

    #PART1 
    part_1_clip = TextClip(part_1, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")
    part_1_clip = part_1_clip.set_duration(tts_clip_part_1_duration)
    part_1_clip = part_1_clip.set_position("center")

    part_1_clip_bg = ColorClip(size=part_1_clip.size, color=(0, 0, 0))
    part_1_clip_bg = part_1_clip_bg.set_duration(tts_clip_part_1_duration)
    part_1_clip_bg = part_1_clip_bg.set_position("center")


    #PART2
    part_2_clip = TextClip(part_2, font="Arial", fontsize=50, align="center", color="white", kerning=None, method="label")
    part_2_clip = part_2_clip.set_start(tts_clip_part_1.duration + 1 )
    part_2_clip = part_2_clip.set_duration(tts_clip_part_2.duration)
    part_2_clip = part_2_clip.set_position("center")

    part_2_clip_bg = ColorClip(size=part_2_clip.size, color=(0, 0, 0))
    part_2_clip_bg = part_2_clip_bg.set_start(tts_clip_part_1.duration + 1)
    part_2_clip_bg = part_2_clip_bg.set_duration(tts_clip_part_2.duration)
    part_2_clip_bg = part_2_clip_bg.set_position("center")
    tts_clip_part_2.start = tts_clip_part_1_duration + 1 


    final_video_path = "final_videos/" + full_text + ".mp4"
    final_video = CompositeVideoClip([base, part_1_clip_bg, part_1_clip, part_2_clip_bg, part_2_clip])
    final_video.set_duration(tts_clip_part_1_duration + tts_clip_part_2_duration + 2)

    #zostaw to jak jest bo rozpierdoolisz zaufaj mi    
    fixed_tts_clip = CompositeAudioClip([tts_clip_part_1.set_duration(part_1_clip.duration), tts_clip_part_2.set_duration(part_2_clip.duration)])

    final_video.audio = fixed_tts_clip
    final_video.write_videofile(final_video_path,  codec="h264_nvenc", fps=24)

    #Finall message
    print(f"Video was rendered at the path {final_video_path}")

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
                    tts_path = ["tts_voices/" + film_theme + ".mp3", "tts_voices/" + film_st_part + ".mp3", "tts_voices/" + film_nd_part + ".mp3"]
                    # Create a Text-to-Speech engine
                    engine = pyttsx3.init()
                    # Set the voice
                    rate = engine.getProperty('rate')
                    voices = engine.getProperty('voices')
                    engine.setProperty("voice", 'en-us')
                    engine.setProperty('rate', rate-150)# Zmiana prędkości tts, działa mocno średnio, do zmiany!!!
                    # Set the voice by index (change the index as per your system configuration)
                    engine.setProperty('voice', voices[0].id)
                    # Save the synthesized speech to a file

                    #Tworzenie odzielnych ttsow dla parstow
                    for _index, _path in enumerate(tts_path):
                        engine.save_to_file(row[_index], _path)
                        engine.runAndWait()

                    generate_video(film_theme, film_st_part, film_nd_part, full_text, tts_path)
    return

if __name__ == "__main__":
    main()
