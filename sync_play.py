import subprocess
import config as config
import os
import concurrent.futures

# The number of threads you want to run simultaneously
MAX_THREADS = config.MAX_THREADS

def download_playlist(play):
    """
    This function downloads a single playlist. It will be executed by a worker
    thread from the ThreadPoolExecutor.
    """
    # Use the base directory from the config for consistency
    base_dir = config.BASE_DIR
    togo = os.path.join(base_dir, config.PLAYLIST_NAME, play.name)

    try:
        # The 'exist_ok=True' argument prevents an error if the directory already exists.
        os.makedirs(togo, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {togo}: {e}")
        return # Exit the function if the directory can't be created

    print(f"Starting download for '{play.name}' in directory: {togo}")

    # It's safer to run subprocess.call with the full path to the target directory.
    # This avoids issues with os.chdir() in a multithreaded context.
    subprocess.call([config.YOUTUBE_DL_PATH,
                        play.url,
                        '-f', 'bestaudio/best',
                        '--extract-audio',
                        '--audio-format', 'mp3',
                        '--embed-thumbnail',
                        '--add-metadata',
                        # Use an archive file within the playlist's specific directory
                        '--download-archive', os.path.join(togo, 'downloaded.txt'),
                        '--no-post-overwrites',
                        '--ignore-errors',
                        # Change the current working directory for the subprocess only
                        '--paths', togo])
    
    print(f"Finished download for '{play.name}'.")


if __name__ == "__main__":
    # It's better not to change the main process's directory.
    # Let the download_playlist function handle the paths.
    
    # The 'with' statement ensures threads are cleaned up properly
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # 'submit' schedules the function to be executed and returns a Future object.
        # We don't need the future object here, so we just loop.
        for play in config.playlists:
            executor.submit(download_playlist, play)

    # The program will automatically wait here until all threads in the pool are finished
    # because of the 'with' block.
    print("All downloads complete.")