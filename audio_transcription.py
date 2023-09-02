import streamlit as st
import openai
from pytube import YouTube  # You can also use youtube_dl

# Custom state object for Streamlit
class SessionState(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def _get_state():
    return SessionState.get(messages=[])

# Function to download YouTube video audio
def download_audio(youtube_url):
    # ... (same as before)

# Function to transcribe audio using Whisper API
def whisper_transcribe(audio_file_path, api_key):
    # ... (same as before)

# Function to summarize text using ChatGPT API
def gpt_summarize(text, api_key):
    # ... (same as before)

# Function to continue the chat conversation
def continue_chat(api_key, messages):
    # ... (same as before)

# Main function for Streamlit app
def main():
    # Get the state
    state = _get_state()
    
    st.title("YouTube Video Summarizer")

    # Input for OpenAI API Key
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

    # Input for YouTube Video URL
    youtube_url = st.text_input("Enter YouTube Video URL:")

    # Initialize message history if empty
    if not state.messages:
        state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Button to start processing
    if st.button("Summarize"):
        # ... (same as before)

        # Add summary to message history
        state.messages.append({"role": "assistant", "content": f"Summary: {summary}"})

    # Chat Interface
    st.write("## Continue Chatting with GPT")

    # Display previous messages
    for message in state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)

    # User input
    user_input = st.chat_input("Type your message")

    if user_input:
        # Add user message to message history
        state.messages.append({"role": "user", "content": user_input})

        # Get GPT response
        gpt_response = continue_chat(openai_api_key, state.messages)

        # Add GPT message to message history
        state.messages.append({"role": "assistant", "content": gpt_response})

        with st.chat_message("assistant"):
            st.write(gpt_response)

if __name__ == "__main__":
    main()
