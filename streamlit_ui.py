import streamlit as st
import json
from datetime import datetime

# Import game modules
try:
    from game_state import player, npcs, locations, get_current_location, get_npcs_at_location, get_npc_by_name
    from npc_dialogue import talk_to_npc
    from save_system import save_game, load_game, apply_save_data
except ImportError:
    st.error("Could not import game modules. Make sure all game files are in the same directory.")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="Text RPG Adventure",
    page_icon="🗡️",
    layout="wide"
)

# Initialize session state
if 'dialogue_history' not in st.session_state:
    st.session_state.dialogue_history = []
if 'current_npc' not in st.session_state:
    st.session_state.current_npc = 'innkeeper'
if 'game_initialized' not in st.session_state:
    st.session_state.game_initialized = True

def display_game_header():
    """Display the main game header"""
    st.title("🗡️ Text RPG Adventure")
    st.markdown("---")
    
    # Player status in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Player", player['name'])
    
    with col2:
        st.metric("Level", player['level'])
    
    with col3:
        st.metric("Health", f"{player['health']}/100")
    
    with col4:
        current_location = get_current_location()
        st.metric("Location", current_location.get('name', 'Unknown'))

def display_current_location():
    """Display current location info"""
    location = get_current_location()
    
    st.subheader(f"📍 {location.get('name', 'Unknown Location')}")
    st.write(location.get('description', 'A mysterious place...'))
    
    # Show NPCs at location
    local_npcs = get_npcs_at_location(player['location'])
    if local_npcs:
        st.write("**People here:**")
        npc_names = []
        for npc_id in local_npcs:
            if npc_id in npcs:
                npc_names.append(npcs[npc_id]['name'])
        st.write(", ".join(npc_names))

def npc_dialogue_interface():
    """Main NPC dialogue interface"""
    st.subheader("💬 Talk to NPCs")
    
    # NPC selection
    available_npcs = get_npcs_at_location(player['location'])
    if not available_npcs:
        st.warning("No NPCs are at your current location.")
        return
    
    # Create NPC options for selectbox
    npc_options = {}
    for npc_id in available_npcs:
        if npc_id in npcs:
            npc_options[npcs[npc_id]['name']] = npc_id
    
    selected_npc_name = st.selectbox(
        "Choose an NPC to talk to:",
        options=list(npc_options.keys()),
        key="npc_selector"
    )
    
    if selected_npc_name:
        selected_npc_id = npc_options[selected_npc_name]
        selected_npc = npcs[selected_npc_id]
        
        # Display NPC info
        with st.expander(f"About {selected_npc['name']}", expanded=False):
            st.write(f"**Personality:** {selected_npc['personality']}")
            st.write(f"**Current Mood:** {selected_npc.get('current_mood', 'neutral')}")
            st.write(f"**Knows About:** {', '.join(selected_npc['knowledge'])}")
        
        # Dialogue input
        st.markdown("---")
        
        # Chat input
        player_message = st.text_input(
            f"What do you want to say to {selected_npc['name']}?",
            placeholder="Type your message here...",
            key="player_input"
        )
        
        # Submit button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💬 Send", type="primary"):
                if player_message.strip():
                    # Get NPC response
                    with st.spinner(f"{selected_npc['name']} is thinking..."):
                        npc_response = talk_to_npc(selected_npc, player_message, player)
                    
                    # Add to dialogue history
                    st.session_state.dialogue_history.append({
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'player': player_message,
                        'npc_name': selected_npc['name'],
                        'npc_response': npc_response
                    })
                    
                    # Clear input by rerunning
                    st.rerun()
                else:
                    st.warning("Please enter a message!")
        
        with col2:
            if st.button("🗑️ Clear History"):
                st.session_state.dialogue_history = []
                st.rerun()
        
        # Display dialogue history
        if st.session_state.dialogue_history:
            st.markdown("---")
            st.subheader("📜 Conversation History")
            
            # Display in reverse order (most recent first)
            for dialogue in reversed(st.session_state.dialogue_history[-10:]):  # Show last 10 exchanges
                with st.container():
                    st.markdown(f"**[{dialogue['timestamp']}] You:** {dialogue['player']}")
                    st.markdown(f"**{dialogue['npc_name']}:** {dialogue['npc_response']}")
                    st.markdown("---")

def inventory_sidebar():
    """Display inventory in sidebar"""
    with st.sidebar:
        st.subheader("🎒 Inventory")
        if player['inventory']:
            for item in player['inventory']:
                st.write(f"• {item.replace('_', ' ').title()}")
        else:
            st.write("*Empty*")
        
        st.markdown("---")
        
        # Quest log
        st.subheader("📋 Quest Log")
        active_quests = [q for q in player['quests'] if q['status'] == 'active']
        if active_quests:
            for quest in active_quests:
                with st.expander(quest['name']):
                    st.write(quest['description'])
                    if quest.get('objectives'):
                        st.write("**Objectives:**")
                        for obj in quest['objectives']:
                            st.write(f"• {obj}")
        else:
            st.write("*No active quests*")

def game_controls_sidebar():
    """Game controls in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎮 Game Controls")
        
        # Save game
        if st.button("💾 Save Game"):
            if save_game("streamlit_save.json"):
                st.success("Game saved!")
            else:
                st.error("Failed to save game!")
        
        # Load game
        if st.button("📁 Load Game"):
            success, save_data = load_game("streamlit_save.json")
            if success and save_data:
                if apply_save_data(save_data):
                    st.success("Game loaded!")
                    st.rerun()
                else:
                    st.error("Failed to apply save data!")
            else:
                st.error("No save file found!")
        
        # Reset dialogue
        if st.button("🔄 Reset Dialogue"):
            st.session_state.dialogue_history = []
            st.rerun()

def game_stats_sidebar():
    """Display game statistics"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("📊 Statistics")
        
        total_items = len(player['inventory'])
        total_quests = len(player['quests'])
        active_quests = len([q for q in player['quests'] if q['status'] == 'active'])
        dialogue_count = len(st.session_state.dialogue_history)
        
        st.metric("Items Carried", total_items)
        st.metric("Total Quests", total_quests)
        st.metric("Active Quests", active_quests)
        st.metric("Conversations", dialogue_count)

def debug_panel():
    """Debug panel for development"""
    if st.checkbox("🔧 Show Debug Info"):
        st.subheader("Debug Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Player Data:**")
            st.json(player)
        
        with col2:
            st.write("**Session State:**")
            debug_state = {
                'dialogue_history_count': len(st.session_state.dialogue_history),
                'current_npc': st.session_state.current_npc,
                'game_initialized': st.session_state.game_initialized
            }
            st.json(debug_state)
        
        st.write("**Available NPCs:**")
        st.json(list(npcs.keys()))

def main():
    """Main Streamlit application"""
    try:
        # Header
        display_game_header()
        
        # Main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Current location
            display_current_location()
            
            st.markdown("---")
            
            # Main dialogue interface
            npc_dialogue_interface()
        
        with col2:
            # Sidebar content in the right column for better mobile experience
            st.subheader("🎒 Inventory")
            if player['inventory']:
                for item in player['inventory']:
                    st.write(f"• {item.replace('_', ' ').title()}")
            else:
                st.write("*Empty*")
            
            st.subheader("📋 Active Quests")
            active_quests = [q for q in player['quests'] if q['status'] == 'active']
            if active_quests:
                for quest in active_quests:
                    with st.expander(quest['name'], expanded=False):
                        st.write(quest['description'])
            else:
                st.write("*No active quests*")
        
        # Sidebar
        inventory_sidebar()
        game_controls_sidebar()
        game_stats_sidebar()
        
        # Debug panel
        st.markdown("---")
        debug_panel()
        
        # Footer
        st.markdown("---")
        st.markdown("*Built with Streamlit • Text RPG Adventure Game*")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please check that all game modules are properly imported.")

if __name__ == "__main__":
    main()