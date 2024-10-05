import os
import json
import requests
import re
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import platform

def get_song_hash(song_id):
    try:
        response = requests.get(f"https://api.beatsaver.com/maps/id/{song_id}")
        response.raise_for_status()
        hash = response.json()["versions"][0]["hash"]
        return hash
    except requests.RequestException as e:
        print(f"Error fetching hash for song ID {song_id}: {e}")
        return None

def extract_song_id(folder_name):
    match = re.match(r'^(\w+)', folder_name)
    if match:
        return match.group(1)
    return None
  
def get_system_font():
    system = platform.system()
    if system == "Windows":
        return "C:\\Windows\\Fonts\\msyh.ttc"
    elif system == "Darwin":  # macOS
        if os.path.exists("/System/Library/Fonts/PingFang.ttc"):
            return "/System/Library/Fonts/PingFang.ttc"
        else: # New System Font
            return "/System/Library/Fonts/Hiragino Sans GB.ttc"
    elif system == "Linux":
        return "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
    return None

def generate_playlist_image(title, width=512, height=512):
    background_color = (219, 165, 255)
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    system_font = get_system_font()
    font_size = 100
    use_default_font = False

    if system_font and os.path.exists(system_font):
        try:
            font = ImageFont.truetype(system_font, font_size)
        except IOError:
            print(f"Failed to load system font: {system_font}")
            font = ImageFont.load_default()
            use_default_font = True
    else:
        print("System font not found, using default font")
        font = ImageFont.load_default()
        use_default_font = True

    if not use_default_font:
        # Dynamically adjust font size
        while font.getbbox(title)[2] - font.getbbox(title)[0] > width * 0.9:
            font_size -= 1
            if font_size < 10:
                print("Font size became too small, using default font")
                font = ImageFont.load_default()
                use_default_font = True
                break
            font = ImageFont.truetype(system_font, font_size)
    
    if use_default_font:
        # For default font, we'll use a different approach
        font_size = 1
        while draw.textbbox((0, 0), title, font=font)[2] < width * 0.9:
            font_size += 1
            font = ImageFont.load_default().font_variant(size=font_size)

    text_color = (0, 0, 0)
    text_position = (width // 2, height // 2)
    
    # Draw text with outline for better readability
    for offset in range(-2, 3):
        draw.text((text_position[0] + offset, text_position[1]), title, font=font, fill=background_color, anchor="mm")
        draw.text((text_position[0], text_position[1] + offset), title, font=font, fill=background_color, anchor="mm")
    draw.text(text_position, title, font=font, fill=text_color, anchor="mm")

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"

def find_info_file(song_path):
    for filename in ['info.dat', 'Info.dat']:
        file_path = os.path.join(song_path, filename)
        if os.path.exists(file_path):
            return file_path
    return None

def generate_playlist(folder_path, playlist_title, difficulty):
    playlist = {
        "playlistTitle": playlist_title,
        "playlistAuthor": "JackZAGUAI",
        "playlistDescription": f"All songs with {difficulty} difficulty",
        "image": generate_playlist_image(playlist_title),
        "songs": []
    }

    for song_folder in os.listdir(folder_path):
        song_path = os.path.join(folder_path, song_folder)
        if os.path.isdir(song_path):
            info_file = find_info_file(song_path)
            if info_file:
                with open(info_file, 'r') as f:
                    info_data = json.load(f)
                
                # Check if the song has the specified difficulty
                has_difficulty = any(diff['_difficulty'] == difficulty for diff in info_data['_difficultyBeatmapSets'][0]['_difficultyBeatmaps'])
                
                if has_difficulty:
                    song_id = extract_song_id(song_folder)
                    if song_id:
                        song_hash = get_song_hash(song_id)
                        if song_hash:
                            song_info = {
                                "hash": song_hash,
                                "songName": info_data['_songName']
                            }
                            playlist['songs'].append(song_info)
                            print(f"Added song: {info_data['_songName']}")
                        else:
                            print(f"Couldn't retrieve hash for song: {info_data['_songName']}")
                    else:
                        print(f"Couldn't extract ID from folder name: {song_folder}")
            else:
                print(f"No Info.dat file found in folder: {song_folder}")

    return playlist

def save_playlist(playlist, output_file):
    with open(output_file, 'w') as f:
        json.dump(playlist, f, indent=2)

def get_input_with_default(prompt, default):
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default

if __name__ == "__main__":
    folder_path = get_input_with_default("Enter the path to the Beat Saber songs folder", ".")
    playlist_title = input("Enter the playlist title (required): ").strip()
    while not playlist_title:
        playlist_title = input("Playlist title is required. Please enter a title: ").strip()
    
    output_file = get_input_with_default("Enter the output file name for the playlist", f"{playlist_title}.bplist")
    difficulty = get_input_with_default("Enter the difficulty level", "Normal")

    playlist = generate_playlist(folder_path, playlist_title, difficulty)
    save_playlist(playlist, output_file)
    print(f"Playlist saved to {output_file}")