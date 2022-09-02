import subprocess
import config as config
import os

os.chdir(config.BASE_DIR)

for play in config.playlists:
    current_dir = os.getcwd()
    togo = os.path.join(current_dir, config.PLAYLIST_NAME, play.name)
    try:
        os.chdir(togo)
    except Exception as e:
        os.makedirs(togo, exist_ok=True)
    os.chdir(togo)
    print(os.getcwd())
    
    subprocess.call([config.YOUTUBE_DL_PATH,
                        play.url,
                        '-f', 'bestaudio/best',
                        '--extract-audio',
                        '--audio-format', 'mp3',
                        #'--postprocessor-args', '"-write_id3v1 1 -id3v2_version 3"',
                        '--embed-thumbnail',
                        '--add-metadata',
                        '--download-archive', 'downloaded.txt',
                        '--no-post-overwrites',
                        '--ignore-errors'])
    
    os.chdir(current_dir)