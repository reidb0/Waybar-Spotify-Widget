## Features

A Python script for Waybar that displays:

- Play/Pause state  
- Current song (artist - title)  
- Faux equalizer bars 
- Scrolling text for longer titles

## Requirements

- Python 3  
- playerctl  
- Spotify (MPRIS support)  
- Waybar  

## Usage

Add this to your Waybar config (inside "modules-center", "modules-right", etc.):

```json
"custom/spotify": {
  "exec": "python3 -u ~/.config/waybar/scripts/spotify.py",
  "return-type": "json"
}
```
