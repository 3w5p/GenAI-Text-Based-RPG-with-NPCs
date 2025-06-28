import subprocess
import time
from threading import Lock

llama_process = None
process_lock = Lock()

def talk_to_npc(npc, player_input, player_data=None):
    """
    Constructs a detailed prompt for an LLM to generate NPC dialogue
    
    Args:
        npc (dict): NPC data containing personality, location, knowledge etc.
        player_input (str): What the player said to the NPC
        player_data (dict): Optional player data for context
    
    Returns:
        str: The NPC's response (assumes call_llm function exists)
    """
    
    # Build context about the NPC's current situation
    location_context = f"You are currently at {npc.get('location', 'an unknown location')}"
    mood_context = f"You are feeling {npc.get('current_mood', 'neutral')} today"
    
    # Build knowledge context
    knowledge_areas = npc.get('knowledge', [])
    knowledge_context = f"You are knowledgeable about: {', '.join(knowledge_areas)}"
    
    # Add player context if available
    player_context = ""
    if player_data:
        player_context = f"\nThe player you're talking to is named {player_data.get('name', 'Adventurer')} and is currently at {player_data.get('location', 'your location')}."
        if player_data.get('quests'):
            active_quests = [q['name'] for q in player_data['quests'] if q['status'] == 'active']
            if active_quests:
                player_context += f" They have active quests: {', '.join(active_quests)}."
    
    # Construct the comprehensive prompt
    prompt = f"""You are {npc['name']}, a character in a fantasy RPG game.

CHARACTER BACKGROUND:
- Personality: {npc['personality']}
- Dialogue Style: {npc.get('dialogue_style', 'speaks naturally')}
- Backstory: {npc.get('backstory', 'A mysterious figure with an unknown past')}

CURRENT SITUATION:
- {location_context}
- {mood_context}
- {knowledge_context}
{player_context}

ROLEPLAY INSTRUCTIONS:
- Stay completely in character as {npc['name']}
- Respond naturally to what the player says
- Use your personality and dialogue style
- Draw from your knowledge areas when relevant
- Keep responses conversational and engaging (1-3 sentences typically)
- Don't break character or mention that you're an AI
- If the player asks about something outside your knowledge, respond as your character would
- React appropriately to the player's tone and content

The player just said to you: "{player_input}"

Respond as {npc['name']} would:"""

    # Call the LLM with the constructed prompt
    try:
        response = call_llm(prompt)
        return response.strip()
    except Exception as e:
        # Fallback response if LLM call fails
        return f"{npc['name']} looks at you thoughtfully but seems distracted and doesn't respond clearly."
"""
def call_llm(prompt):
    import requests
    import json
    
    # Server settings (adjust if you changed defaults)
    SERVER_URL = "http://localhost:8080/completion"
    
    # Request data
    data = {
        "prompt": prompt,
        "temperature": 0.7,
        "n_predict": 150  # Max tokens to generate
    }
    
    try:
        response = requests.post(
            SERVER_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()["content"].strip()
    except Exception as e:
        print(f"Error calling LLM server: {e}")
        return "The NPC seems distracted and doesn't respond clearly."""



def call_llm(prompt):
    global llama_process
    
    with process_lock:
        if llama_process is None:
            # Start llama-cli in persistent interactive mode
            llama_process = subprocess.Popen(
                [
                    r"REPLACE_WITH_LLAMA_CLI_PATH",  # Path to your llama-cli executable
                    "-m", r"REPLACE_WITH_MODEL_PATH",  # Path to your model file
                    "--temp", "0.7",
                    "--ctx-size", "512",      # Reduced memory usage
                    "--threads", "2",        # Use 2 CPU cores
                    "-n", "20",              # Max 20 tokens per response
                    "--interactive",
                    "--prompt-cache", "cache.bin"  # Cache prompts for speed
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )
        
        # Send prompt and read response
        try:
            llama_process.stdin.write(f"{prompt}\n")
            llama_process.stdin.flush()
            
            # Read until stop condition or timeout
            response = []
            while True:
                line = llama_process.stdout.readline()
                if not line or "User:" in line:
                    break
                response.append(line.strip())
            
            return " ".join(response).strip()
            
        except Exception as e:
            print(f"Error communicating with llama-cli: {e}")
            return "NPC seems distracted and doesn't respond."

# Example usage and testing function
def test_npc_dialogue():
    """Test function to demonstrate the dialogue system"""
    from game_state import npcs, player
    
    print("=== NPC DIALOGUE SYSTEM TEST ===")
    
    # Test with innkeeper
    innkeeper = npcs["innkeeper"]
    test_inputs = [
        "Hello there!",
        "Have you seen anything strange lately?",
        "I'm looking for a missing cat",
        "Can you tell me about the village?"
    ]
    
    print(f"\nTesting dialogue with {innkeeper['name']}:")
    for player_input in test_inputs:
        print(f"\nPlayer: {player_input}")
        response = talk_to_npc(innkeeper, player_input, player)
        print(f"{innkeeper['name']}: {response}")
    
    print("\n================================")

if __name__ == "__main__":
    test_npc_dialogue()