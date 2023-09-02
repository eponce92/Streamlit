import streamlit as st
import openai
from pytube import YouTube  # You can also use youtube_dl

# Function to download YouTube video audio
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = f"{yt.title}.webm"
    stream.download(filename=audio_file_path)
    return audio_file_path

# Function to transcribe audio using Whisper API
def whisper_transcribe(audio_file_path, api_key):
    openai.api_key = api_key
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

# Function to summarize text using ChatGPT API
def gpt_summarize(text, api_key):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please summarize the following text: {text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Function to continue the chat conversation
def continue_chat(api_key, messages, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Main function for Streamlit app
def main():
    st.title("YouTube Video Summarizer")

    # Dropdown for GPT model selection
    gpt_model = st.selectbox(
        "Select GPT model:",
        ("gpt-4-32k", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k")
    )

    # Input for OpenAI API Key
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    youtube_url = st.text_input("Enter YouTube Video URL:")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]

    if st.button("Summarize"):
        if not openai_api_key or not youtube_url:
            st.warning("Please fill in all fields.")
        else:
            audio_file_path = download_audio(youtube_url)
            transcription = whisper_transcribe(audio_file_path, openai_api_key)

            with st.expander("Show Transcription"):
                st.write(transcription)

            summary = gpt_summarize(transcription, openai_api_key)

            with st.expander("Show Summary"):
                st.write(summary)
            
            st.session_state['messages'].append({"role": "assistant", "content": f"Summary: {summary}"})

    st.write("## Continue Chatting with GPT")

    for message in st.session_state['messages']:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)

    user_input = st.chat_input("Type your message")

    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        gpt_response = continue_chat(openai_api_key, st.session_state['messages'], gpt_model)
        st.session_state['messages'].append({"role": "assistant", "content": gpt_response})
        
        with st.chat_message("assistant"):
            st.write(gpt_response)

if __name__ == "__main__":
    main()
