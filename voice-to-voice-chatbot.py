import os
import whisper from openai
from groq import Groq
from gtts import gTTS
import gradio as gr
import playsound
import tempfile

# Set up the Groq client
client = Groq(
    api_key=os.environ.get("gsk_3U90LE9QszpPzMGIeDUYWGdyb3FYVTj75zH6gcWo7I4Ym28FU8gmY"),
)

# Load the Whisper model for speech-to-text
whisper_model = whisper.load_model("base")

def transcribe_and_generate_response(audio_file):
    # Step 1: Transcribe the audio to text using Whisper
    transcription = whisper_model.transcribe(audio_file)
    user_input = transcription['text']
    print(f"Transcription: {user_input}")

    # Step 2: Get a response from the language model using Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="Llama 3.1 405B",
    )
    llm_response = chat_completion.choices[0].message.content
    print(f"LLM Response: {llm_response}")

    # Step 3: Convert the response text to speech using gTTS
    tts = gTTS(llm_response)
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio_file.name)

    # Play the audio response
    playsound.playsound(temp_audio_file.name)

    # Return transcription and response for display in Gradio
    return user_input, llm_response

# Set up Gradio UI for the chatbot
with gr.Blocks() as app:
    gr.Markdown("# Real-time Voice-to-Voice Chatbot")
    audio_input = gr.Audio(source="microphone", type="filepath", label="Speak here...")
    text_output = gr.Textbox(label="Transcription")
    response_output = gr.Textbox(label="LLM Response")

    audio_input.change(transcribe_and_generate_response, inputs=audio_input, outputs=[text_output, response_output])

# Launch the Gradio app, which will be deployable on Streamlit
app.launch()
