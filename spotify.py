#!/usr/bin/env python3

import json
import subprocess
import time
import random

WIDTH = 25
SPACER = "       "
FRAME_DELAY = 0.15
WAVE_CHARS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

levels = [2, 3, 2, 3]
pos = 0
song = ""
last_metadata_check = 0


def get_status():
    try:
        return subprocess.check_output(
            ["playerctl", "-p", "spotify", "status"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return "Error, no process found"


def get_song():
    try:
        return subprocess.check_output(
            [
                "playerctl",
                "-p",
                "spotify",
                "metadata",
                "--format",
                "{{artist}} - {{title}}",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return "No song found"


while True:

    status = get_status()
    if status == "Playing":
        icon = ""

        for i in range(len(levels)):
            change = random.choice([-1, 0, 1])
            levels[i] = max(0, min(7, levels[i] + change))

        wave = "".join(WAVE_CHARS[l] for l in levels)

    elif status == "Paused":
        icon = ""
        wave = "    "
    else:
        print(
            json.dumps(
                {"text": "  Spotify", "tooltip": "Spotify is closed — click to open"}
            ),
            flush=True,
        )
        time.sleep(1)
        continue

    now = time.time()
    if now - last_metadata_check > 1:
        new_song = get_song()
        last_metadata_check = now
        if new_song and new_song != song:
            song = new_song
            pos = 0
    if not song:
        time.sleep(0.5)
        continue

    if len(song) <= WIDTH:
        display = song.ljust(WIDTH)
    else:
        unit = song + SPACER
        loop_text = unit * 3
        display = loop_text[pos : pos + WIDTH]

        pos += 1
        if pos >= len(unit):
            pos = 0

    print(json.dumps({"text": f"{icon} {display} {wave}", "tooltip": song}), flush=True)
    time.sleep(FRAME_DELAY)
