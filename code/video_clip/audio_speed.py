from moviepy.editor import AudioFileClip,vfx


def speed_up_audio(input_path, output_path, speed_factor=1.5):
    """
    使用moviepy加速音频文件。
    :param input_path: 源音频文件的路径。
    :param output_path: 加速后音频文件的保存路径。
    :param speed_factor: 加速因子，默认为1.5倍。
    """
    # 加载音频文件
    audio_clip = AudioFileClip(input_path)

    # 加速音频
    sped_up_audio = audio_clip.fx(vfx.speedx, speed_factor)

    # 保存加速后的音频
    sped_up_audio.write_audiofile(output_path)


speed_up_audio(r"E:\practice_group\generate_novel\material\audio\妖精.WAV", r"E:\practice_group\generate_novel\material\audio\妖精_speed.wav")
