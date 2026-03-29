from moviepy import TextClip, ImageClip, CompositeVideoClip, AudioFileClip

def create_video(script_text):
    audio = AudioFileClip("assets/voice.mp3")

    duration = audio.duration  # 🔥 match video to audio

    txt_clip = TextClip(
        text=script_text,
        font_size=28,
        color='white',
        size=(800, 600),
        method='caption'
    ).with_duration(duration)

    bg_clip = ImageClip("assets/bg.jpg").with_duration(duration)

    video = CompositeVideoClip([
        bg_clip,
        txt_clip.with_position('center')
    ])

    video = video.with_audio(audio)

    video.write_videofile("output.mp4", fps=24)

    return "output.mp4"