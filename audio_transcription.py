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


# Main function for Streamlit app
def main():
    st.title("YouTube Video Summarizer")

    # Input for OpenAI API Key
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

    # Input for YouTube Video URL
    youtube_url = st.text_input("Enter YouTube Video URL:")

    # Button to start processing
    if st.button("Summarize"):
        if not openai_api_key or not youtube_url:
            st.warning("Please fill in all fields.")
        else:
            # Download the video and extract audio
            audio_file_path = download_audio(youtube_url)
            
            # Transcribe the video using Whisper API
            transcription = whisper_transcribe(audio_file_path, openai_api_key)

            st.write("## Transcription")
            st.write(transcription)

            # Summarize the transcription using OpenAI GPT API
            summary = gpt_summarize(transcription, openai_api_key)

            st.write("## Summary")
            st.write(summary)

if __name__ == "__main__":
    main()
