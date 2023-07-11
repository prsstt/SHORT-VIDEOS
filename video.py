from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import csv
import numpy as np
# Load CSV file
csv_file = 'data.csv'

# Set paths
output_audio = 'output_audio.mp3'
output_video = r'C:\Users\sh0cky\Desktop\YT AUTOMATIZATION\output_video.mp4'
background_image = 'background_image.jpg'
font_path = 'font.ttf'
text_position_top = (640, 100)
text_position_center = (640, 360)
font_size_top = 48
font_size_center = 72
text_color = (255, 255, 255)
text_duration = 9  # in seconds
text_pause = 1  # in seconds
width = 720
height = 1280
# Create audio from CSV file
def create_audio_from_csv(csv_file, output_audio):
    quotes = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 3:  # Check if the row has at least 3 columns
                theme = row[0]
                first_part = row[1]
                second_part = row[2]
                quote = f"{theme} {first_part} {second_part}"
                quotes.append(quote)

    if quotes:
        full_text = ' '.join(quotes)
        tts = gTTS(text=full_text, lang='en', tld='com.au', slow=False)
        tts.save(output_audio)
    else:
        print("No quotes found in the CSV file.")

# Create video with text overlay
def create_video_with_text(background_image, output_video, font_path, text_position_top, text_position_center,
                           font_size_top, font_size_center, text_color, text_duration, text_pause):
    width = 720  # Width of the video
    height = 1280  # Height of the video

    # Resize the background image to match the desired aspect ratio
    background = Image.open(background_image)
    background = background.resize((width, height))

    clip = ImageClip(np.array(background))
    clip = clip.set_duration(text_duration * 2 + text_pause)

def text_generator():
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 3:  # Check if the row has at least 3 columns
                theme = row[0]
                first_part = row[1]
                second_part = row[2]

                txt_clip_top = TextClip(theme, fontsize=font_size_top, font=str(font_path), color=text_color) \
                    .set_position(text_position_top) \
                    .set_duration(text_duration)

                txt_clip_center = TextClip(first_part, fontsize=font_size_center, font=str(font_path),
                                           color=text_color) \
                    .set_position(text_position_center) \
                    .set_duration(text_duration)

                pause_clip = TextClip('', duration=text_pause)
                clip = concatenate_videoclips([txt_clip_top, txt_clip_center, pause_clip])
                clip = clip.set_position((0, 0))

                # Resize the clip to match the desired aspect ratio
                clip = clip.resize(width=width, height=height)
                yield clip


    video_clips = list(text_generator())

    final_video = concatenate_videoclips(video_clips)
    final_video = CompositeVideoClip([clip, final_video])
    final_video = final_video.set_duration(duration)
    final_video = final_video.set_audio(audio)

    # Set the video resolution and aspect ratio
    final_video = final_video.resize(height=height)

    # Write the final video file
    final_video.write_videofile(output_video, fps=24)

# Convert CSV to audio
create_audio_from_csv(csv_file, output_audio)

# Read audio and create video
audio = AudioFileClip(output_audio)
duration = audio.duration

# Create video with text overlay
create_video_with_text(background_image, output_video, font_path, text_position_top, text_position_center,
                       font_size_top, font_size_center, text_color, text_duration, text_pause)

# Clean up temporary files (optional)
audio.close()
