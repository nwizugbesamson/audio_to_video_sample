# from collections import deque
import time
from controllers.audio_split import segment_audiofile, AudioSplit
from controllers.transcriber import transcribe
from controllers.img_composer import make_video
from controllers.pool_video import pool
from uuid import uuid4
from moviepy.editor import VideoFileClip, AudioFileClip
from sys import argv
# @click.group()
# def cli():
#     pass


# @click.command()
# @click.argument('-M', '--metadata_json', description='path to metadata json format')
# @click.argument('-A', '--audio_path', description='path to audio file')
# @click.argument('-O', '--output_path', description='path to video output')
# def animate(metadata_json: str, audio_path: str, output_path: str) -> None:
def animate(audio_path: str, time_stamp_path :str) -> None:
    """_summary_

    Args:
        metadata_json (str): _description_
        audio_path (str): _description_
        output_path (str): _description_
    """
    output_path = f'data/Result/{str(uuid4())}.mp4'
    audio_segments = segment_audiofile(audio_path, time_stamp_path)
    for segment in audio_segments:
        segment.transcription = transcribe(segment.stream)
        segment.video = make_video(segment.speaker, segment.duration)
    
   
    
    sorted(audio_segments, key=lambda segment: segment.index)
    
    video_paths = [segment.video for segment in audio_segments]
    compiled_video_path = pool(video_paths, f'data/compiled_final/{str(uuid4())}.mp4')
    
    videoclip = VideoFileClip(compiled_video_path)
    audioclip = AudioFileClip('data/Audio/Recording.m4a')
    video = videoclip.set_audio(audioclip)
    video.write_videofile(output_path)
    print(f'YOUR VIDEO HAS BEEN SAVED TO: [{output_path}]')

        
    
    
    



# registering the commands
if __name__=='__main__':
    # cli.add_command(animate)
    # cli()
    start = time.time()
    audio_path = str(argv[1])
    map_path = str(argv[2])
    print(audio_path, map_path)
    animate(audio_path, map_path)
    # animate("data/Audio/Recording.m4a", 'timestamp.json')
    print(f'RUNTIME: [{time.time() - start}]')
    