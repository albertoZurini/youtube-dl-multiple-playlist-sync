# Add key and bpm to the mp3s

In order to run this docker container you first have to build it through the `build.sh` script and then it can be run either in normal mode (`run_normal.sh`), which will just run the `add_key_bpm.py` file under a working environment. Otherwise, it's possible to debug its functioning by running `run_debug.sh`, which makes use of `debugpy`. In this folder, the `.vscode` is already configured to make use of this utility for debugging.

## Before using it

Make sure to edit the volume passthrough on the run scripts to match your playlists folder.