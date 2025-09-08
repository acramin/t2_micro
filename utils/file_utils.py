"""
File utility functions for handling JSON profiles and backups
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

def ensure_directory_exists(directory_path):
    """Ensure a directory exists, create if it doesn't"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_data_paths():
    """Get paths for data directories"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, '..', 'data')
    characters_path = os.path.join(data_path, 'characters')
    backups_path = os.path.join(data_path, 'backups')
    
    ensure_directory_exists(characters_path)
    ensure_directory_exists(backups_path)
    
    return {
        'characters': characters_path,
        'backups': backups_path
    }

def load_json_file(file_path):
    """Load JSON data from a file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json_file(file_path, data):
    """Save data to a JSON file with backup"""
    paths = get_data_paths()
    
    # Create backup if file exists
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(paths['backups'], f"{timestamp}_{filename}")
        shutil.copy2(file_path, backup_path)
    
    # Save the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_character_files():
    """Get list of all character files"""
    paths = get_data_paths()
    character_files = []
    
    for file in os.listdir(paths['characters']):
        if file.endswith('.json'):
            character_files.append(file)
    
    return character_files

def load_character_profile(character_name):
    """Load a specific character profile"""
    paths = get_data_paths()
    file_path = os.path.join(paths['characters'], f"{character_name}.json")
    return load_json_file(file_path)

def save_character_profile(character_data):
    """Save a character profile"""
    paths = get_data_paths()
    character_name = character_data.get('name', 'unknown').lower().replace(' ', '_')
    file_path = os.path.join(paths['characters'], f"{character_name}.json")
    save_json_file(file_path, character_data)