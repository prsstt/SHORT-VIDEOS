#to jest plik do pisania i testowania uploadu potem zmienie nazwe albo to rozdziele jak cos
from moviepy.editor import *
import os 
import csv
import soundfile as sf
from moviepy.config import change_settings
from moviepy.video.fx.resize import resize
from PIL import Image
import pyttsx3
import soundfile as sf
import textwrap
import json
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
#C:\Users\sh0cky\Desktop\YT AUTOMATIZATION\SHORT-VIDEOS\data.csv
#40 znaków na wiersz
def generate_video(theme, part_1, part_2, full_text, tts_path, config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    #tts_clip_theme = AudioFileClip(tts_path[0])
    tts_clip_part_1 = AudioFileClip(tts_path[1])
    tts_clip_part_2 = AudioFileClip(tts_path[2])  


    file_1 = sf.SoundFile(tts_path[1])
    tts_clip_part_1_duration = int(file_1.frames / file_1.samplerate)
    file_2 = sf.SoundFile(tts_path[2])
    tts_clip_part_2_duration = int(file_2.frames / file_2.samplerate)



    if config.get('background_image'):
        background_clip = ImageClip(f"bg_images/{config['background_image']}")
    elif config.get('background_video'):
        background_clip = VideoFileClip(f"bg_videos/{config['background_video']}")
    else:
        # Jeśli nie ma w configu to ustawia czarne tło defaultowo
        background_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
    
    total_tts_duration = tts_clip_part_1_duration + tts_clip_part_2_duration + 3 


    if background_clip:
        base = concatenate_videoclips([background_clip], method="compose")
    else:
            # Jeśli nie ma w configu to ustawia czarne tło defaultowo
        base = ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(total_tts_duration)
    if background_clip.duration < total_tts_duration:
            # Calculate the number of times to loop the background video
            loop_count = int(total_tts_duration / background_clip.duration) + 1

            # Loop bg_video
            background_clip = background_clip.fx(vfx.loop, duration=background_clip.duration * loop_count)

    background_clip = background_clip.set_duration(total_tts_duration)
    base = concatenate_videoclips([background_clip], method="compose")
       
    #size = 1080, 1920

   #PART1
    width_wrap = int(config['letters_width_wrap'])
    wrapped_part_1 = textwrap.wrap(part_1, width=width_wrap)
    part_1_text = "\n".join(wrapped_part_1)
    part_1_clip = TextClip(part_1_text, font=config['font']['family'], fontsize=config['font']['size'],
                           align="center", color=config['font']['color'], method="label")
    part_1_clip = part_1_clip.set_duration(tts_clip_part_1_duration)
    part_1_clip = part_1_clip.set_position("center")
    color = config.get('text_box_color')

    part_1_clip_bg = ColorClip(size=part_1_clip.size, color=color)
    part_1_clip_bg = part_1_clip_bg.set_duration(tts_clip_part_1_duration)
    part_1_clip_bg = part_1_clip_bg.set_position("center")


    #PART2
    width_wrap = int(config['letters_width_wrap'])
    wrapped_part_2 = textwrap.wrap(part_2, width=width_wrap)
    part_2_text = "\n".join(wrapped_part_2)
    part_2_clip = TextClip(part_2_text, font=config['font']['family'], fontsize=config['font']['size'],
                           align="center", color=config['font']['color'], method="label")
    part_2_clip = part_2_clip.set_start(tts_clip_part_1.duration + 1)
    part_2_clip = part_2_clip.set_duration(tts_clip_part_2.duration)
    part_2_clip = part_2_clip.set_position("center")

    part_2_clip_bg = ColorClip(size=part_2_clip.size, color=color)
    part_2_clip_bg = part_2_clip_bg.set_start(tts_clip_part_1.duration + 1)
    part_2_clip_bg = part_2_clip_bg.set_duration(tts_clip_part_2.duration)
    part_2_clip_bg = part_2_clip_bg.set_position("center")
    tts_clip_part_2.start = tts_clip_part_1_duration + 1 


    final_video_path = config.get("final_video_path") + full_text + ".mp4"
    final_video = CompositeVideoClip([base, part_1_clip_bg, part_1_clip, part_2_clip_bg, part_2_clip])
    final_video.set_duration(tts_clip_part_1_duration + tts_clip_part_2_duration + 2)
    #final_video = final_video.resize(width=1080, height=1920)
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
                    with open(f"configurations/{film_theme}_template.json", 'r') as config_file:
                        config = json.load(config_file)

                    # Set the voice by the value from the config file
                    tts_voice_id = config.get('tts_voice_id')#, voices[4].id)
                    engine.setProperty('voice', voices[tts_voice_id].id)

                    # Set the voice speed by the value from the config file or use a default value
                    tts_voice_speed = config.get('tts_voice_speed')#, rate - 150)
                    engine.setProperty('rate', rate - tts_voice_speed)
                    # Save the synthesized speech to a file

                    #Tworzenie odzielnych ttsow dla parstow
                    for _index, _path in enumerate(tts_path):
                        engine.save_to_file(row[_index], _path)
                        engine.runAndWait()

                    config_file_path = f"configurations/{film_theme}_template.json"

                    generate_video(film_theme, film_st_part, film_nd_part, full_text, tts_path, config_file_path)
    return

if __name__ == "__main__":
    main()


