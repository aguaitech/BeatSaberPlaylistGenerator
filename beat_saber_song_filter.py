import os
import json
import shutil

def find_info_file(song_path):
    for filename in ['info.dat', 'Info.dat']:
        file_path = os.path.join(song_path, filename)
        if os.path.exists(file_path):
            return file_path
    return None

def get_difficulties(info_file):
    with open(info_file, 'r') as f:
        info_data = json.load(f)
    return [diff['_difficulty'] for diff in info_data['_difficultyBeatmapSets'][0]['_difficultyBeatmaps']]

def filter_songs(folder_path, keep_difficulties):
    deleted_count = 0
    kept_count = 0
    
    for song_folder in os.listdir(folder_path):
        song_path = os.path.join(folder_path, song_folder)
        if os.path.isdir(song_path):
            info_file = find_info_file(song_path)
            if info_file:
                difficulties = get_difficulties(info_file)
                if not any(diff in keep_difficulties for diff in difficulties):
                    print(f"Deleting: {song_folder}")
                    shutil.rmtree(song_path)
                    deleted_count += 1
                else:
                    print(f"Keeping: {song_folder}")
                    kept_count += 1
            else:
                print(f"No Info.dat file found in folder: {song_folder}")
    
    return kept_count, deleted_count

def main():
    folder_path = input("Enter the path to the Beat Saber songs folder [.]: ").strip() or "."
    
    keep_difficulties = []
    while True:
        difficulty = input("Enter a difficulty level to keep (or press Enter to finish): ").strip()
        if not difficulty:
            break
        keep_difficulties.append(difficulty)
    
    if not keep_difficulties:
        print("No difficulties specified. No changes will be made.")
        return
    
    print(f"\nKeeping songs with difficulties: {', '.join(keep_difficulties)}")
    confirm = input("This will permanently delete songs without these difficulties. Continue? (y/n): ").lower()
    
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    kept_count, deleted_count = filter_songs(folder_path, keep_difficulties)
    
    print(f"\nOperation complete.")
    print(f"Songs kept: {kept_count}")
    print(f"Songs deleted: {deleted_count}")

if __name__ == "__main__":
    main()