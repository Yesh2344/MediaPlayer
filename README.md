# Sonic Wave Music Player

Sonic Wave is a modern, feature-rich music player built with Python using customtkinter and pygame. It offers a sleek, dark-themed interface with advanced playback controls and music visualization. It should be someones dream to work on these projects.

## Features

- Modern dark-themed user interface
- Music library management
- Playlist support
- Real-time music visualization
- Advanced playback controls (play, pause, next, previous)
- Shuffle and repeat modes
- Volume control
- Progress bar with seeking capability
- Search functionality
- MP3 metadata support
- File system navigation
- Favorites system
- Custom playlist creation

## Requirements

- Python 3.x
- tkinter
- customtkinter
- pygame
- mutagen
- numpy
- matplotlib

## Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
```bash
pip install customtkinter pygame mutagen numpy matplotlib
```

## Usage

1. Run the application:
```bash
python music_player.py
```

2. Click on "Library" to select a folder containing your music files
3. Double-click any song to start playing
4. Use the control buttons to:
   - Play/Pause (⏯)
   - Skip to next track (⏭)
   - Return to previous track (⏮)
   - Toggle shuffle mode (🔀)
   - Toggle repeat mode (🔁)

## Features in Detail

## Keyboard Shortcuts

- Space: Play/Pause
- Left Arrow: Previous track
- Right Arrow: Next track
- Up Arrow: Volume up
- Down Arrow: Volume down
- Ctrl+F: Focus search bar
- Ctrl+L: Open library
- Ctrl+P: Create new playlist

### Music Library
- Browse and select music folders
- Automatic metadata extraction from MP3 files
- Search functionality for quick access to songs

### Playback Controls
- Basic controls (play, pause, next, previous)
- Progress bar with seeking capability
- Volume control slider
- Shuffle and repeat modes (none, one, all)

### User Interface
- Dark theme for comfortable viewing
- Real-time music visualization
- Song information display (title, artist)
- Clean and intuitive layout

### Organization
- Create and manage playlists
- Add songs to favorites
- Search through your music library

## File Management

The application saves user data (playlists, favorites, last directory) in a JSON file named `music_player_data.json` in the application directory.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements you'd like to add.

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Complete implementation of playlist management
- Enhanced visualization options
- Equalizer functionality
- Audio effects
- Extended file format support
- Remote control capabilities
- Cross-platform testing and optimization

## Contact Information

Email: yeswanthsoma83@gmail.com
