from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip
import numpy as np


def adjusted_audio_volume_db(audio_clip, db_change):
    """
    调整音频剪辑后的音量分贝
    :param audio_clip: AudioFileClip 对象，待调整的音频
    :param db_change: float，音频的分贝变化量
    :return: 返回调整后的音频
    """
    volume_multiplier = 10 ** (db_change / 20.0)
    return audio_clip.volumex(volume_multiplier)


def overlay_audio_loop(video_clip, audio_clip):
    """
    在原视频中覆盖BGM
    :param video_clip: VideoFileClip 对象，原视频
    :param audio_clip: AudioFileClio 对象，加入的BGM
    :return: 加入BGM后的视频
    """
    audio_copies_needed = np.ceil(video_clip.duration / audio_clip.duration)
    audio_clips = [audio_clip] * int(audio_copies_needed)
    looped_audio = concatenate_audioclips(audio_clips)
    # 如果循环音频长度超过视频长度，则截断
    looped_audio = looped_audio.set_duration(video_clip.duration)
    # 混合原视频音频和BGM
    mixed_audio = CompositeAudioClip([video_clip.audio, looped_audio])
    # 将混合音频设置到视频上
    video_clip.audio = mixed_audio.set_duration(video_clip.duration)
    return video_clip


video = VideoFileClip(r"E:\practice_group\generate_novel\work\竖屏\10月10日\10月10日.mp4")
BGM_audio = AudioFileClip(r"E:\practice_group\generate_novel\material\audio\BGM\蝴蝶少女_纯.MP3")
adjusted_BGM_audio = adjusted_audio_volume_db(BGM_audio,-22)
final_video = overlay_audio_loop(video,adjusted_BGM_audio)
final_video.write_videofile(r"E:\practice_group\generate_novel\work\竖屏\10月10日\10月10日_bgm.mp4",codec="libx264",threads=20)