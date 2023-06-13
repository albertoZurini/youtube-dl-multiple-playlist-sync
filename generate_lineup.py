import os
import config
import random

PATH = os.path.join(config.BASE_DIR, config.PLAYLIST_NAME)

SPECIAL_MARKER = "___"

def get_bpm_key(path):
    split = path.split("___")[1].split("_")
    return int(split[0]), split[1]

def split_key(key):
    letter = key[-1]
    num = key[0:-1]

    return letter, int(num)

def are_letters_similar(letter_a, letter_b):
    return letter_a == letter_b

def are_numbers_similar(num_a, num_b):
    if num_a == 12 and num_b == 1 or num_a == 12 and num_b == 1:
        return True
    else:
        return abs(num_a - num_b) == 1

def are_keys_similar(key_a, key_b):
    letter_a, num_a = split_key(key_a)
    letter_b, num_b = split_key(key_b)

    if letter_a == letter_b:
        return are_numbers_similar(num_a, num_b)
    elif num_a == num_b:
        return are_letters_similar(letter_a, letter_b)
    else:
        return False

def are_bpm_similar(bpm_a, bpm_b, range):
    return (bpm_a - bpm_b)/bpm_a < range

def are_songs_similar(bpm_a, key_a, bpm_b, key_b):
    global bpm_range
    return are_keys_similar(key_a, key_b) and are_bpm_similar(bpm_a, bpm_b, bpm_range)

num_songs = 10
bpm_range = 0.2 # 10%

lineup = []
files = []
now_bpm = None
now_key = None

for (path, dirnames, filenames) in os.walk(PATH):
    for name in filenames:
        files.append(name)

random.shuffle(files)

for name in files:
    if len(lineup) >= num_songs:
        stop_loop = True
        break

    if "mp3" not in name: 
        continue
    
    bpm, key = get_bpm_key(name)
    if bpm < 100:
        bpm *= 2
    
    if now_bpm is None or are_songs_similar(now_bpm, now_key, bpm, key):
        now_bpm = bpm
        now_key = key
        lineup.append(name)
    

print(lineup)