import shlex
import subprocess
import os
import config
import multiprocessing
import time

PATH = os.path.join(config.BASE_DIR, config.PLAYLIST_NAME)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def get_key_cmd(mp3_path):
    return f"/usr/bin/keyfinder-cli {mp3_path}"

def get_bpm_cmd(mp3_path):
    return f"/usr/bin/bpm-tag {mp3_path}"

def get_camelot(key):
    mappings = {
        "B": "1B",
        "Abm": "1A",
        "Gb": "2B",
        "Ebm": "2A",
        "Db": "3B",
        "Bbm": "3A",
        "Ab": "4B",
        "Fm": "4A",
        "Eb": "5B",
        "Cm": "5A",
        "Bb": "6B",
        "Gm": "6A",
        "F": "7B",
        "Dm": "7A",
        "C": "8B",
        "Am": "8A",
        "G": "9B",
        "Em": "9A",
        "D": "10B",
        "Bm": "10A",
        "A": "11B",
        "Gbm": "11A",
        "E": "12B",
        "Dbm": "12A",
    }
    return mappings[key]

def get_bpm_and_key(mp3_path):
    bpm_arr = subprocess.Popen(get_bpm_cmd(mp3_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    bpm = ""
    for i in bpm_arr:
        _i = i.decode("utf-8")
        if len(_i) > 4:
            bpm = _i.split(" ")[-2].split(".")[0]
    _key = subprocess.Popen(get_key_cmd(mp3_path), stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8").split("\n")[0]
    key = get_camelot(_key)

    return bpm, key, _key

def increase_progress(state):
    state.processed += 1
    perc = int(state.processed/state.tot_files*100)

    speed = state.processed/(time.time() - state.start)
    
    print(f"{perc}% [{state.processed} of {state.tot_files}] @ {speed} files per second")

SPECIAL_MARKER = "___"
def process_file(path, state, errors):
    increase_progress(state)
    if SPECIAL_MARKER in path:
        return
    info = get_bpm_and_key(path)

    if "mp3" not in path:
        assert Exception("Not an mp3 file")

    if "'" in path:
        quote = "'"
    else:
        quote = ""
        
    new_filename = f"{path[0:len(path)-5]}{SPECIAL_MARKER}{info[0]}_{info[1]}_{info[2]}.mp3{quote}"
    cmd = f"mv {path} {new_filename}"
    status = os.system(cmd)
    if status != 0:
        err_msg = f"== Error processing {path} ```{cmd}```"
        errors.append(err_msg)
        print(err_msg)

def process_chunk(arr, state, errors):
    for f in arr:
        process_file(f, state, errors)

files = []
for (path, dirnames, filenames) in os.walk(PATH):
    for name in filenames:
        if "mp3" not in name:
            continue
        files.append(shlex.quote(f"{path}/{name}"))
        # files.append(os.path.join(path, _name))

cores = multiprocessing.cpu_count()

files_chunks = list(split(files, cores))

processes = []

with multiprocessing.Manager() as manager:
    state = manager.Namespace()
    errors = manager.list([])
    state.start = time.time()
    state.tot_files = len(files)
    state.processed = 0

    for f in files_chunks:
        P = multiprocessing.Process(target=process_chunk, args=(f, state, errors))
        P.start()
        processes.append(P)

    for p in processes:
        p.join()

    if len(errors) > 0:
        print(errors)