import sys
from game_state import player, npcs, locations, get_current_location, get_npcs_at_location, get_npc_by_name
from npc_dialogue import talk_to_npc

def display_location():
    """Display current location information"""
    location = get_current_location()
    print(f"\n=== {location.get('name', 'Unknown Location')} ===")
    print(location.get('description', 'A mysterious place...'))
    
    # Show NPCs at current location
    local_npcs = get_npcs_at_location(player['location'])
    if local_npcs:
        npc_names = []
        for npc_id in local_npcs:
            if npc_id in npcs:
                npc_names.append(npcs[npc_id]['name'])
        print(f"People here: {', '.join(npc_names)}")
    else:
        print("No one else is here.")
    
    # Show available exits
    exits = location.get('exits', {})
    if exits:
        print(f"Exits: {', '.join(exits.keys())}")
    print()

def display_inventory():
    """Display player inventory"""
    print(f"\n=== Inventory ===")
    if player['inventory']:
        for i, item in enumerate(player['inventory'], 1):
            print(f"{i}. {item.replace('_', ' ').title()}")
    else:
        print("Your inventory is empty.")
    print()

def display_quests():
    """Display active quests"""
    print(f"\n=== Quest Log ===")
    active_quests = [q for q in player['quests'] if q['status'] == 'active']
    if active_quests:
        for quest in active_quests:
            print(f"• {quest['name']}")
            print(f"  {quest['description']}")
            if quest.get('objectives'):
                for obj in quest['objectives']:
                    print(f"  - {obj}")
    else:
        print("No active quests.")
    print()

def display_help():
    """Display available commands"""
    print(f"\n=== Available Commands ===")
    print("talk to [npc name] - Start a conversation with an NPC")
    print("look - Examine your current location")
    print("inventory - Check your inventory")
    print("quests - View your quest log")
    print("move [direction] - Move to another location")
    print("help - Show this help message")
    print("quit - Exit the game")
    print()

def handle_talk_command(command_parts):
    """Handle 'talk to [npc name]' command"""
    if len(command_parts) < 3:
        print("Usage: talk to [npc name]")
        return
    
    # Extract NPC name (everything after "talk to")
    npc_name = " ".join(command_parts[2:])
    
    # Check if NPC exists
    npc = get_npc_by_name(npc_name)
    if not npc:
        print(f"There's no one named '{npc_name}' here.")
        return
    
    # Check if NPC is at current location
    local_npcs = get_npcs_at_location(player['location'])
    npc_id = None
    for npc_id_check, npc_data in npcs.items():
        if npc_data == npc and npc_id_check in local_npcs:
            npc_id = npc_id_check
            break
    
    if not npc_id:
        print(f"{npc['name']} is not here right now.")
        return
    
    # Start conversation
    print(f"\nYou approach {npc['name']}.")
    print(f"{npc['name']}: *{npc.get('dialogue_style', 'looks at you expectantly')}*")
    
    while True:
        try:
            player_message = input(f"\nWhat do you say to {npc['name']}? (or 'exit' to end conversation): ").strip()
            
            if player_message.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print(f"You end your conversation with {npc['name']}.")
                break
            
            if not player_message:
                print("You stand there silently...")
                continue
            
            # Get NPC response
            print("\n" + npc['name'] + " is thinking...")
            response = talk_to_npc(npc, player_message, player)
            print(f"{npc['name']}: {response}")
            
        except KeyboardInterrupt:
            print(f"\nYou abruptly end the conversation with {npc['name']}.")
            break

def handle_move_command(command_parts):
    """Handle movement between locations"""
    if len(command_parts) < 2:
        print("Usage: move [direction]")
        return
    
    direction = command_parts[1].lower()
    current_location = get_current_location()
    exits = current_location.get('exits', {})
    
    if direction not in exits:
        print(f"You can't go {direction} from here.")
        print(f"Available directions: {', '.join(exits.keys())}")
        return
    
    # Move player
    new_location = exits[direction]
    player['location'] = new_location
    print(f"You head {direction}...")
    display_location()

def main_game_loop():
    """Main interactive game loop"""
    print("=" * 50)
    print("    WELCOME TO THE TEXT RPG ADVENTURE!")
    print("=" * 50)
    print(f"Welcome, {player['name']}!")
    print("Type 'help' for available commands.")
    
    # Show initial location
    display_location()
    
    while True:
        try:
            # Get player input
            user_input = input("> ").strip().lower()
            
            if not user_input:
                continue
            
            # Parse command
            command_parts = user_input.split()
            main_command = command_parts[0]
            
            # Handle commands
            if main_command == "quit" or main_command == "exit":
                print("Thanks for playing! Goodbye!")
                break
                
            elif main_command == "help":
                display_help()
                
            elif main_command == "look":
                display_location()
                
            elif main_command == "inventory":
                display_inventory()
                
            elif main_command == "quests":
                display_quests()
                
            elif main_command == "talk":
                handle_talk_command(command_parts)
                
            elif main_command == "move" or main_command == "go":
                handle_move_command(command_parts)
                
            else:
                print(f"Unknown command: {main_command}")
                print("Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Type 'help' for available commands.")

# Additional utility functions for enhanced gameplay
def show_player_status():
    """Display player status information"""
    print(f"\n=== Player Status ===")
    print(f"Name: {player['name']}")
    print(f"Level: {player['level']}")
    print(f"Health: {player['health']}/100")
    print(f"Experience: {player['experience']}")
    print(f"Location: {get_current_location().get('name', 'Unknown')}")
    print()

def save_game_prompt():
    """Prompt player to save game before quitting"""
    try:
        save_choice = input("Would you like to save your game? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            from save_system import save_game
            if save_game():
                print("Game saved successfully!")
            else:
                print("Failed to save game.")
    except:
        pass

if __name__ == "__main__":
    try:
        main_game_loop()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        print("Please report this bug!")
    finally:
        save_game_prompt()