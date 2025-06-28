# main.py - Main Game Runner

"""
Text RPG Adventure Game
=======================

This is the main entry point for the Text RPG game. It provides options to run
the game in different modes: terminal-based or web-based using Streamlit.

Usage:
    python main.py           # Run terminal version
    python main.py --web     # Run Streamlit web version
    python main.py --test    # Run tests
"""

import sys
import argparse

def run_terminal_game():
    """Run the terminal-based version of the game"""
    try:
        from game_loop import main_game_loop
        main_game_loop()
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure all game files are in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running terminal game: {e}")
        sys.exit(1)

def run_web_game():
    """Run the Streamlit web version of the game"""
    try:
        import subprocess
        import os
        
        # Check if streamlit is installed
        try:
            import streamlit
        except ImportError:
            print("Streamlit is not installed.")
            print("Install it with: pip install streamlit")
            sys.exit(1)
        
        # Run streamlit
        print("Starting Streamlit web interface...")
        print("The game will open in your default web browser.")
        print("Press Ctrl+C to stop the server.")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_ui.py"
        ])
        
    except KeyboardInterrupt:
        print("\nWeb server stopped.")
    except Exception as e:
        print(f"Error running web game: {e}")
        sys.exit(1)

def run_tests():
    """Run all game tests"""
    print("Running Text RPG Tests...")
    print("=" * 40)
    
    try:
        # Test game state
        print("Testing game state...")
        from game_state import player, npcs, locations
        print(f"✓ Player initialized: {player['name']}")
        print(f"✓ {len(npcs)} NPCs loaded")
        print(f"✓ {len(locations)} locations loaded")
        
        # Test NPC dialogue
        print("\nTesting NPC dialogue system...")
        from npc_dialogue import test_npc_dialogue
        test_npc_dialogue()
        
        # Test save system
        print("\nTesting save system...")
        from save_system import test_save_system
        test_save_system()
        
        print("\n" + "=" * 40)
        print("All tests completed!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

def show_help():
    """Show help information"""
    help_text = """
Text RPG Adventure Game
=======================

A Python-based text RPG with NPC dialogue powered by LLM integration.

GAME MODES:
-----------
Terminal Mode: Classic text-based interface in your terminal
Web Mode: Modern web interface using Streamlit

FEATURES:
---------
• Interactive NPC dialogue with AI-powered responses
• Inventory and quest management
• Save/load game functionality
• Multiple locations to explore
• Rich character personalities and knowledge systems

COMMANDS (Terminal Mode):
------------------------
talk to [npc name] - Start conversation with an NPC
look               - Examine current location
inventory          - Check your inventory
quests            - View active quests
move [direction]  - Move to another location
help              - Show available commands
quit              - Exit the game

REQUIREMENTS:
-------------
• Python 3.7+
• streamlit (for web mode): pip install streamlit

FILES:
------
game_state.py     - Core game state and data structures
npc_dialogue.py   - NPC dialogue system with LLM integration
game_loop.py      - Terminal-based game loop
save_system.py    - Save/load functionality
streamlit_ui.py   - Web-based interface
main.py          - This file (main runner)

EXAMPLES:
---------
python main.py              # Start terminal game
python main.py --web        # Start web interface
python main.py --test       # Run tests
python main.py --help       # Show this help

Have fun adventuring!
"""
    print(help_text)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Text RPG Adventure Game",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Run the web-based Streamlit interface'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run all game tests'
    )
    
    parser.add_argument(
        '--help-full',
        action='store_true',
        help='Show detailed help information'
    )
    
    args = parser.parse_args()
    
    # Handle arguments
    if args.help_full:
        show_help()
    elif args.test:
        run_tests()
    elif args.web:
        run_web_game()
    else:
        # Default to terminal game
        print("Starting Text RPG Adventure...")
        print("Use --web for the web interface or --help for more options.")
        print()
        run_terminal_game()

if __name__ == "__main__":
    main()