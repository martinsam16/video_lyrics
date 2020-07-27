import os

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip, TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.config import change_settings
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.resize import resize
from mutagen.mp3 import MP3

current_directory = os.path.dirname(os.path.realpath(__file__))
path_mp3 = os.path.join(current_directory, 'audio.mp3')
path_video_saved = os.path.join(current_directory, 'video.mp4')
IMAGE_MAGICK = os.path.join(current_directory, 'IMAGE_MAGICK', 'magick.exe')
change_settings({"IMAGEMAGICK_BINARY": IMAGE_MAGICK})

## configuration

# audio
duration_audio = MP3(path_mp3).info.length

# video
background_video = (0, 0, 0)
size_video = (1280, 720)
fps_video = 25
duration_video = duration_audio

# text
style_text: dict = {
    'font': 'Amiri-regular',
    'color': 'white',
    'fontsize': 50
}

struct_text = [
    {
        'text': 'Si quieren parar lo que ahora voy a hacer',
        'duration': 3
    },
    {
        'text': 'denle al pausa y dejen de jod*',
        'duration': 3
    },
    {
        'text': 'dsps negro ..',
        'duration': 3
    }
]

struct_images = [
    {
        'img': './img1.jpg',
        'duration': 3,
        'size': size_video
    },
    {
        'img': './img2.jpg',
        'duration': 3,
        'size': size_video
    },
    {
        'img': './img1.jpg',
        'duration': 3,
        'size': size_video
    },
]

## processing

# clip of video with the audio
clip_video = ColorClip(size=size_video, color=background_video, duration=duration_video)
clip_audio = CompositeAudioClip([AudioFileClip(path_mp3)])
clip_video.audio = clip_audio

# create a list of textclip

clips_txt = [TextClip(txt=element.get('text'),
                      color=style_text.get('color'),
                      font=style_text.get('font'),
                      size=size_video,
                      fontsize=style_text.get('fontsize')
                      ).set_duration(element.get('duration'))
             for element in struct_text]
clips_img = [resize(ImageClip(img=element.get('img'), duration=element.get('duration')), element.get('size'))
             for element in struct_images]

clips_text = concatenate_videoclips(clips_txt)
clips_img = concatenate_videoclips(clips_img)

processed_video = CompositeVideoClip([clip_video, clips_img, clips_text])

# save
# processed_video.write_videofile(filename=path_video_saved, fps=fps_video)
processed_video.subclip(t_start=0, t_end=9).write_videofile(filename=path_video_saved, fps=fps_video)
