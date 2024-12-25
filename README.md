# Local-Music-Player

A music player built with Python and `pygame`, featuring playlist management, volume control, shuffle mode, repeat mode, and more.

## Features

- **Play & Pause**: Easily control playback of your tracks.
- **Next/Previous Track**: Switch between tracks in your playlist.
- **Playlist Management**: Add or remove songs in the playlist.
- **Repeat Mode**: Replay the current track.
- **Shuffle Mode**: Play tracks randomly.
- **Volume Control**: Adjust audio levels with a slider.
- **Persistent Settings**: Automatically save and load preferences like volume, repeat, and shuffle.

## Requirements
- **Python**: 3.x
- **Dependencies**: Install via `requirements.txt`

## Installation

1. **Clone the repository** and navigate to the project folder:
    ```bash
    git clone https://github.com/artur3333/Local-Music-Player.git
    cd Local-Music-Player
    ```
    
2. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Directory Tree

```plaintext
Local-Music-Player
├── icons/                   # Folder for UI icons
│   ├── music.ico            # App icon
│   ├── play.png             # Play button
│   ├── pause.png            # Pause button
│   ├── next.png             # Next button
│   ├── prev.png             # Previous button
│   ├── repeat_on.png        # Repeat ON icon
│   ├── repeat_off.png       # Repeat OFF icon
│   ├── remix_on.png         # Shuffle ON icon
│   ├── remix_off.png        # Shuffle OFF icon
│   ├── add_song.png         # Add Song button icon
│   ├── circle.png           # Progress bar circle
│   ├── close.png            # Close playlist icon
│   └── list.png             # Open playlist icon
├── main.py                  # Main script to run the application
├── config.json              # Configuration file for stored data
├── music.txt                # Playlist file (contains track paths)
├── requirements.txt         # List of Python dependencies
└── README.md                # Project readme with usage instructions and details
```

## Usage

Run the Application:
   ```bash
   python main.py
   ```
---

1. **Play and Pause**:
      - Use the play/pause button to start or stop the current track.
        
2. **Track Navigation**:
      - Click the "Next" or "Previous" buttons to switch tracks.
        
3. **Volume Control**:
      - Adjust the volume using the vertical slider on the right.
        
4. **Add Songs**:
      - Click the "Add Song" button to browse and add new tracks to your playlist.
      - Drag and Drop audio files in the Track List to add new tracks to your playlist.
        
6. **Playback Modes**:
      - Use the repeat button to toggle repeat mode for the current track.
      - Use the shuffle button to toggle shuffle mode for random playback.
