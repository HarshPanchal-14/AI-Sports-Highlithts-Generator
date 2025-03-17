import ffmpeg
import os
from datetime import timedelta

def extract_highlights(video_path, highlights, output_dir='highlights'):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'highlight.mp4')
    
    # Create FFmpeg filter for highlights
    filters = []
    for i, highlight in enumerate(highlights):
        start = str(timedelta(seconds=highlight['start']))
        end = str(timedelta(seconds=highlight['end']))
        filters.append(f'[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}];')
        filters.append(f'[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];')
    
    filter_str = ''.join(filters)
    filter_str += ''.join(f'[v{i}][a{i}]' for i in range(len(highlights))) + f'concat=n={len(highlights)}:v=1:a=1[outv][outa]'
    
    # Process video with FFmpeg
    (
        ffmpeg
        .input(video_path)
        .filter_('complex_filter', filter_str)
        .output(output_path, map='[outv]')
        .run(overwrite_output=True)
    )
    
    return output_path