# BeatSaberPlaylistGenerator
This project contains two Python scripts designed to help Beat Saber players manage their custom songs and create playlists:

1. Beat Saber Playlist Generator
2. Beat Saber Song Difficulty Filter

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the scripts to your local machine.

2. Install the required Python packages:

```
pip install Pillow requests
```

## Important: Song Folder Name Format

For these scripts to work correctly, your Beat Saber custom song folders must follow this naming convention:

```
<song_id> (<song_name> - <artist_name>)
```

For example:
```
1a336 (Green Apple Paradise - Kelvin Chuang)
```

The `<song_id>` at the beginning is crucial for the scripts to fetch the correct song hash from the BeatSaver API.

## Beat Saber Playlist Generator

This script creates a playlist file (.bplist) for Beat Saber, including songs with a specified difficulty level and generating a custom playlist image.

### Usage

1. Run the script:

```
python beat_saber_playlist_generator.py
```

2. Follow the prompts:
   - Enter the path to your Beat Saber songs folder (default is current directory)
   - Enter a title for your playlist
   - Enter the output file name for the playlist (default is `<playlist_title>.bplist`)
   - Enter the difficulty level to include in the playlist (default is "Normal")

3. The script will generate a .bplist file in the specified location, which can be imported into Beat Saber.

### Features

- Generates a custom playlist image with the playlist title
- Supports Unicode characters (including Chinese) in the playlist title
- Automatically adjusts font size to fit the playlist title in the image
- Works on Windows, macOS, and Linux

## Beat Saber Song Difficulty Filter

This script helps you manage your Beat Saber song library by keeping only the songs that have specific difficulty levels.

### Usage

1. Run the script:

```
python beat_saber_song_filter.py
```

2. Follow the prompts:
   - Enter the path to your Beat Saber songs folder (default is current directory)
   - Enter difficulty levels to keep (press Enter after each level, leave blank and press Enter to finish)
   - Confirm that you want to proceed with deleting songs

3. The script will delete song folders that don't contain any of the specified difficulty levels.

### Warning

This script permanently deletes folders. Make sure to backup your Beat Saber songs folder before running this script.

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes.

## License

This project is licensed under the GPLv3 License - see the LICENSE file for details.