# save_system.py - Game Save/Load System

import json
import os
from datetime import datetime
from game_state import player, npcs

def save_game(filename="savegame.json"):
    """
    Save the current game state to a JSON file
    
    Args:
        filename (str): Name of the save file (default: "savegame.json")
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        # Create save data structure
        save_data = {
            "player": player.copy(),
            "npcs": npcs.copy(),
            "save_timestamp": datetime.now().isoformat(),
            "game_version": "1.0",
            "save_location": player.get("location", "unknown")
        }
        
        # Add metadata
        save_data["metadata"] = {
            "save_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player_name": player.get("name", "Unknown"),
            "player_level": player.get("level", 1),
            "current_location": player.get("location", "unknown"),
            "inventory_count": len(player.get("inventory", [])),
            "active_quests": len([q for q in player.get("quests", []) if q.get("status") == "active"])
        }
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as save_file:
            json.dump(save_data, save_file, indent=2, ensure_ascii=False)
        
        print(f"Game saved to {filename}")
        print(f"Save created at: {save_data['metadata']['save_date']}")
        return True
        
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(filename="savegame.json"):
    """
    Load game state from a JSON file
    
    Args:
        filename (str): Name of the save file (default: "savegame.json")
    
    Returns:
        tuple: (success: bool, save_data: dict or None)
    """
    try:
        if not os.path.exists(filename):
            print(f"Save file {filename} not found.")
            return False, None
        
        with open(filename, 'r', encoding='utf-8') as save_file:
            save_data = json.load(save_file)
        
        # Validate save data structure
        if not validate_save_data(save_data):
            print("Save file appears to be corrupted or invalid.")
            return False, None
        
        return True, save_data
        
    except json.JSONDecodeError:
        print("Save file is corrupted (invalid JSON).")
        return False, None
    except Exception as e:
        print(f"Error loading game: {e}")
        return False, None

def validate_save_data(save_data):
    """
    Validate that save data has required structure
    
    Args:
        save_data (dict): The loaded save data
    
    Returns:
        bool: True if valid, False otherwise
    """
    required_keys = ["player", "npcs", "save_timestamp"]
    
    # Check for required top-level keys
    for key in required_keys:
        if key not in save_data:
            print(f"Missing required save data key: {key}")
            return False
    
    # Check player data structure
    player_data = save_data["player"]
    required_player_keys = ["name", "location", "inventory", "quests"]
    
    for key in required_player_keys:
        if key not in player_data:
            print(f"Missing required player data key: {key}")
            return False
    
    # Validate inventory is a list
    if not isinstance(player_data["inventory"], list):
        print("Player inventory must be a list")
        return False
    
    # Validate quests is a list
    if not isinstance(player_data["quests"], list):
        print("Player quests must be a list")
        return False
    
    return True

def apply_save_data(save_data):
    """
    Apply loaded save data to current game state
    
    Args:
        save_data (dict): The validated save data
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        global player, npcs
        from game_state import player, npcs
        
        # Update player data
        for key, value in save_data["player"].items():
            player[key] = value
        
        # Update NPC data (in case NPCs have state changes)
        if "npcs" in save_data:
            for npc_id, npc_data in save_data["npcs"].items():
                if npc_id in npcs:
                    npcs[npc_id].update(npc_data)
        
        print("Game loaded successfully!")
        if "metadata" in save_data:
            metadata = save_data["metadata"]
            print(f"Save from: {metadata.get('save_date', 'Unknown date')}")
            print(f"Player: {metadata.get('player_name', 'Unknown')} (Level {metadata.get('player_level', 1)})")
        
        return True
        
    except Exception as e:
        print(f"Error applying save data: {e}")
        return False

def list_save_files():
    """
    List all available save files in the current directory
    
    Returns:
        list: List of save file names
    """
    save_files = []
    for filename in os.listdir('.'):
        if filename.endswith('.json') and ('save' in filename.lower() or 'game' in filename.lower()):
            save_files.append(filename)
    return save_files

def get_save_info(filename):
    """
    Get information about a save file without loading it
    
    Args:
        filename (str): Name of the save file
    
    Returns:
        dict: Save file information or None if error
    """
    try:
        with open(filename, 'r', encoding='utf-8') as save_file:
            save_data = json.load(save_file)
        
        if "metadata" in save_data:
            return save_data["metadata"]
        else:
            # Create basic info from player data
            player_data = save_data.get("player", {})
            return {
                "player_name": player_data.get("name", "Unknown"),
                "player_level": player_data.get("level", 1),
                "current_location": player_data.get("location", "unknown"),
                "save_date": save_data.get("save_timestamp", "Unknown")
            }
    except:
        return None

def backup_save(filename="savegame.json"):
    """
    Create a backup of the current save file
    
    Args:
        filename (str): Name of the save file to backup
    
    Returns:
        bool: True if backup was successful
    """
    try:
        if not os.path.exists(filename):
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.backup_{timestamp}"
        
        with open(filename, 'r') as original:
            with open(backup_name, 'w') as backup:
                backup.write(original.read())
        
        print(f"Backup created: {backup_name}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

# Interactive save/load functions
def interactive_save():
    """Interactive save function with user prompts"""
    print("\n=== Save Game ===")
    
    # Show current save files
    save_files = list_save_files()
    if save_files:
        print("Existing save files:")
        for i, filename in enumerate(save_files, 1):
            info = get_save_info(filename)
            if info:
                print(f"{i}. {filename} - {info.get('player_name', 'Unknown')} (Level {info.get('player_level', 1)})")
    
    # Get filename from user
    filename = input("Enter save filename (or press Enter for 'savegame.json'): ").strip()
    if not filename:
        filename = "savegame.json"
    
    # Add .json extension if not present
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Check if file exists and confirm overwrite
    if os.path.exists(filename):
        confirm = input(f"File {filename} already exists. Overwrite? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Save cancelled.")
            return False
        
        # Create backup
        backup_save(filename)
    
    # Save the game
    return save_game(filename)

def interactive_load():
    """Interactive load function with user prompts"""
    print("\n=== Load Game ===")
    
    save_files = list_save_files()
    if not save_files:
        print("No save files found.")
        return False
    
    print("Available save files:")
    for i, filename in enumerate(save_files, 1):
        info = get_save_info(filename)
        if info:
            print(f"{i}. {filename}")
            print(f"   Player: {info.get('player_name', 'Unknown')} (Level {info.get('player_level', 1)})")
            print(f"   Location: {info.get('current_location', 'Unknown')}")
            print(f"   Saved: {info.get('save_date', 'Unknown')}")
        else:
            print(f"{i}. {filename} - (Unable to read save info)")
    
    try:
        choice = input("Enter save file number (or filename): ").strip()
        
        # Check if it's a number
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(save_files):
                filename = save_files[choice_num - 1]
            else:
                print("Invalid choice.")
                return False
        else:
            filename = choice
            if not filename.endswith('.json'):
                filename += '.json'
        
        # Load the game
        success, save_data = load_game(filename)
        if success:
            return apply_save_data(save_data)
        else:
            return False
            
    except ValueError:
        print("Invalid input.")
        return False
    except KeyboardInterrupt:
        print("\nLoad cancelled.")
        return False

# Testing and utility functions
def test_save_system():
    """Test the save/load system"""
    print("=== TESTING SAVE SYSTEM ===")
    
    # Test saving
    print("Testing save...")
    if save_game("test_save.json"):
        print("✓ Save test passed")
    else:
        print("✗ Save test failed")
        return
    
    # Test loading
    print("Testing load...")
    success, save_data = load_game("test_save.json")
    if success and save_data:
        print("✓ Load test passed")
    else:
        print("✗ Load test failed")
        return
    
    # Test validation
    print("Testing validation...")
    if validate_save_data(save_data):
        print("✓ Validation test passed")
    else:
        print("✗ Validation test failed")
    
    # Cleanup
    try:
        os.remove("test_save.json")
        print("✓ Cleanup completed")
    except:
        print("! Could not clean up test file")
    
    print("=== SAVE SYSTEM TESTS COMPLETE ===")

if __name__ == "__main__":
    test_save_system()