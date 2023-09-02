
import streamlit as st
import openai
from pytube import YouTube  # You can also use youtube_dl
import re

# Function to download YouTube video audio
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    sanitized_title = re.sub(r'[^\w\s]', '', yt.title)
    sanitized_title = re.sub(r'\s+', '_', sanitized_title)
    audio_file_path = f"{sanitized_title}.webm"
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=audio_file_path)
    return audio_file_path

# Function to transcribe audio using Whisper API
def whisper_transcribe(audio_file_path, api_key):
    openai.api_key = api_key
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

# Function to continue the chat conversation
def continue_chat(api_key, messages, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("YouTube Video Transcriber 📹")

    # Dropdown for GPT model selection
    gpt_model = st.selectbox(
        "Select GPT model:",
        ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k")  # Add your accessible models here
    )


    # Input for OpenAI API Key
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    youtube_url = st.text_input("Enter YouTube Video URL:")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "system", "content": "Use this audio transcription as context to chat with the user. The user might ask you to summarize or questions about the content of the transcription and you should answer based on this information."}]

    # Button to start transcription
    if st.button("Transcribe"):
        if not openai_api_key or not youtube_url:
            st.warning("Please fill in all fields.")
        else:
            try:
                # Download the video and extract audio
                audio_file_path = download_audio(youtube_url)
                
                # Transcribe the video using Whisper API
                transcription = whisper_transcribe(audio_file_path, openai_api_key)

                with st.expander("Show Transcription"):
                    st.write(transcription)

                # Add transcription to message history
                st.session_state['messages'].append({"role": "assistant", "content": f"Transcription: {transcription}"})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Chat Interface
    if 'messages' in st.session_state and len(st.session_state['messages']) > 1:  # Check if transcription is done
        st.write("## Continue Chatting with GPT")

        # Display previous messages
        for message in st.session_state['messages']:
            role = message["role"]
            content = message["content"]
            with st.chat_message(role):
                st.write(content)

        # User input
        user_input = st.chat_input("Type your message")

        if user_input:
            try:
                # Add user message to message history
                st.session_state['messages'].append({"role": "user", "content": user_input})

                # Get GPT response
                gpt_response = continue_chat(openai_api_key, st.session_state['messages'], gpt_model)

                # Add GPT message to message history
                st.session_state['messages'].append({"role": "assistant", "content": gpt_response})
                
                with st.chat_message("assistant"):
                    st.write(gpt_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()