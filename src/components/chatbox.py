import streamlit as st
from typing import Dict, List


def mock_ai_response(user_input: str) -> str:
    """
    Generate a mock AI response by reversing the input string.
    
    Args:
        user_input (str): The user's input message
        
    Returns:
        str: The AI's response
    """
    return f"AI: {user_input[::-1]}"


def chatbox() -> None:
    """
    Display and manage the chat interface.
    Handles message history, user input, and AI responses.
    """
    # Set up the chat interface
    st.title("Chat Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    messages_container = st.container()

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        ai_response = mock_ai_response(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
        
        st.rerun()

    with messages_container:
        for message in st.session_state.messages:
            left, middle, right = st.columns([1, 2, 1])
            
            if message["role"] == "user":
                with right:
                    text_col, icon_col = st.columns([5, 1])
                    with text_col:
                        st.write(message["content"])
                    with icon_col:
                        st.write("👤") # TODO: Create a custom icon
            else:
                with left:
                    icon_col, text_col = st.columns([1, 5])
                    with icon_col:
                        st.write("🤖") # TODO: Create a custom icon
                    with text_col:
                        st.write(message["content"])