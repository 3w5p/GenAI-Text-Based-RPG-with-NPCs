player = {
    "name": "Adventurer",
    "location": "village_inn",
    "inventory": ["rusty_sword", "healing_potion", "gold_coins"],
    "quests": [
        {
            "id": "find_missing_cat",
            "name": "Find the Missing Cat",
            "description": "Help the innkeeper find their lost cat, Whiskers",
            "status": "active",
            "objectives": ["Search the forest", "Ask villagers about the cat"]
        }
    ],
    "level": 1,
    "health": 100,
    "experience": 0
}

# NPCs dictionary - contains all non-player characters
npcs = {
    "innkeeper": {
        "name": "Martha",
        "personality": "warm, welcoming, slightly worried about her missing cat",
        "location": "village_inn",
        "knowledge": [
            "local_gossip",
            "village_history", 
            "travelers_tales",
            "missing_cat_quest",
            "inn_services",
            "local_dangers"
        ],
        "dialogue_style": "friendly and motherly, speaks with concern about her cat",
        "backstory": "Has run the village inn for 20 years, knows everyone in town",
        "current_mood": "worried",
        "special_items": ["room_key", "cat_treats"]
    },
    
    "blacksmith": {
        "name": "Gareth",
        "personality": "gruff but helpful, takes pride in his craft",
        "location": "blacksmith_shop",
        "knowledge": [
            "weapon_crafting",
            "armor_repair",
            "metal_working",
            "local_ores",
            "ancient_weapons",
            "combat_techniques"
        ],
        "dialogue_style": "direct and practical, speaks in short sentences",
        "backstory": "Former adventurer turned blacksmith, has seen many battles",
        "current_mood": "busy",
        "special_items": ["masterwork_hammer", "rare_metals"]
    },
    
    "village_elder": {
        "name": "Elder Aldric",
        "personality": "wise, patient, speaks in riddles and metaphors",
        "location": "village_center",
        "knowledge": [
            "ancient_history",
            "magic_lore",
            "prophecies",
            "village_founding",
            "spiritual_guidance",
            "hidden_secrets"
        ],
        "dialogue_style": "speaks slowly and thoughtfully, often in proverbs",
        "backstory": "Has guided the village for over 50 years, keeper of ancient knowledge",
        "current_mood": "contemplative",
        "special_items": ["ancient_tome", "crystal_pendant"]
    }
}

# Game locations dictionary
locations = {
    "village_inn": {
        "name": "The Prancing Pony Inn",
        "description": "A cozy inn with warm firelight and the smell of fresh bread",
        "npcs": ["innkeeper"],
        "exits": {"north": "village_center", "east": "blacksmith_shop"}
    },
    
    "village_center": {
        "name": "Village Square",
        "description": "The heart of the village with a stone fountain and market stalls",
        "npcs": ["village_elder"],
        "exits": {"south": "village_inn", "west": "forest_path", "east": "blacksmith_shop"}
    },
    
    "blacksmith_shop": {
        "name": "Gareth's Forge",
        "description": "A hot, smoky workshop filled with the sound of hammer on anvil",
        "npcs": ["blacksmith"],
        "exits": {"west": "village_center", "south": "village_inn"}
    },
    
    "forest_path": {
        "name": "Forest Trail",
        "description": "A winding path through tall trees with dappled sunlight",
        "npcs": [],
        "exits": {"east": "village_center"}
    }
}

def get_current_location():
    """Returns the player's current location data"""
    return locations.get(player["location"], {})

def get_npcs_at_location(location):
    """Returns list of NPCs at the specified location"""
    location_data = locations.get(location, {})
    return location_data.get("npcs", [])

def get_npc_by_name(npc_name):
    """Returns NPC data by name (case insensitive)"""
    npc_name = npc_name.lower().strip()
    for npc_id, npc_data in npcs.items():
        if npc_data["name"].lower() == npc_name or npc_id == npc_name:
            return npc_data
    return None

# Game state utility functions
def add_to_inventory(item):
    """Add an item to player inventory"""
    player["inventory"].append(item)

def remove_from_inventory(item):
    """Remove an item from player inventory"""
    if item in player["inventory"]:
        player["inventory"].remove(item)
        return True
    return False

def has_item(item):
    """Check if player has a specific item"""
    return item in player["inventory"]

def update_quest_status(quest_id, new_status):
    """Update the status of a quest"""
    for quest in player["quests"]:
        if quest["id"] == quest_id:
            quest["status"] = new_status
            return True
    return False

def add_quest(quest_data):
    """Add a new quest to the player's quest log"""
    player["quests"].append(quest_data)

# Print initial game state for debugging
if __name__ == "__main__":
    print("=== GAME STATE INITIALIZED ===")
    print(f"Player: {player['name']}")
    print(f"Location: {player['location']}")
    print(f"Inventory: {player['inventory']}")
    print(f"Active Quests: {len(player['quests'])}")
    print(f"NPCs Available: {list(npcs.keys())}")
    print("===============================")