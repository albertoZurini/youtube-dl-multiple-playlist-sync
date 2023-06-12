# What is this?

Script that automates downloading of multiple YouTube playlist with youtube-dl (in reality yt-dlp).

# How to use this?

Run `cp config.py.template config.py` and edit `PlayList(name, url)` with your needs as well as the `BASE_DIR`, `PLAYLIST` and `YOUTUBE_DL_PATH` variables.

# Add key and bpm to the songs

`add_key_and_bpm.py` is responsible for adding such data at the end of the filename. The key is being added in both camelot and standard notation.
To use this script you have to install `bpm-tools` ([AUR](https://aur.archlinux.org/packages/bpm-tools)) and `keyfinder-cli` ([AUR](https://aur.archlinux.org/packages/keyfinder-cli-git)). Unfortunately, I wasn't able to find any better library for Python and had to make use of `subprpcess` and `os` to rename the files. Hopefully, the script has enough checks, but you should be careful when using it.