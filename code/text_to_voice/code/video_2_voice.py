from moviepy.editor import VideoFileClip

def convert_mp4_to_wav(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

# 使用示例
convert_mp4_to_wav(r"E:\practice_group\generate_novel\text_to_voice\data\sweet_girl.mp4", r"E:\practice_group\generate_novel\text_to_voice\data\sweet_girl.wav")
