# GenAI Text-Based RPG with NPCs

A text-based role-playing game with AI-powered NPC dialogue, built with Python and Mistral 7B via llama.cpp.

## Features

- Interactive NPC conversations powered by Mistral 7B
- Multiple locations to explore
- Inventory and quest systems
- Save/load game functionality
- Two interface options: terminal or web-based (Streamlit)
- Rich character personalities and knowledge systems

## Requirements

- Python 3.7+
- llama.cpp installed locally
- Mistral 7B model (specifically `mistral-7b-instruct-v0.2.Q3_K_L.gguf`)
- For web interface: `streamlit` (`pip install streamlit`)

## Setup Instructions

### 1. Install llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

2. Download Mistral 7B Model
Download mistral-7b-instruct-v0.2.Q3_K_L.gguf and place it in:
```
llama.cpp/models/mistral/
```
3. Install Python Dependencies
```bash
pip install streamlit requests
```
4. Configure Game Paths
Edit npc_dialogue.py to set correct paths:
```
llama_process = subprocess.Popen(
    [
        "path/to/llama.cpp/build/bin/Release/llama-cli.exe",  # Update this path
        "-m", "path/to/llama.cpp/models/mistral/mistral-7b-instruct-v0.2.Q3_K_L.gguf",  # Update this path
        # ... rest of configuration
    ]
)
```
How to Run
Terminal Version
```bash
python main.py
```
Web Version (Streamlit)
```bash
python main.py --web
```
Run Tests
```bash
python main.py --test
```
The game uses Mistral 7B via llama.cpp to generate dynamic NPC responses. Each NPC has:
-Unique personality traits
-Knowledge areas they can discuss
-Current mood that affects responses
-Backstory and dialogue style

The game saves to savegame.json by default. Features include:
-Multiple save slots
-Save metadata tracking
-Backup system
-Validation checks
