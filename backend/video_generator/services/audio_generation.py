import openai
import os
from pathlib import Path
import requests

# Load the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
client = openai

def generate_audio(text, model="tts-1", voice="alloy",filename="test_audio.mp3"):
    """
    Generate an audio file from text using OpenAI's TTS model.

    Parameters:
        text (str): The text to convert to speech.
        model (str): The TTS model to use (default is "tts-1").
        voice (str): The voice for TTS (default is "alloy").

    Returns:
        audio_url (str): The URL of the generated audio.
    """
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    print(f"Response: {response}")
   
     

    # Define the output directory
    output_dir = Path("data/audios")
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    output_path = output_dir / filename

    # Save the binary response to a file
    with open(output_path, "wb") as audio_file:
        audio_file.write(response.read())  # Save binary data

    print(f"Audio file saved successfully at: {output_path}")
    return str(output_path)


def download_audio(audio_url, filename):
    """
    Download the generated audio from the URL and save it to a file.

    Parameters:
        audio_url (str): The URL of the audio file.
        filename (str): The local filename to save the audio.

    Returns:
        str: Path to the saved audio file.
    """
    response = requests.get(audio_url)
    output_path = Path("data/audios") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    with open(output_path, 'wb') as file:
        file.write(response.content)
    
    return str(output_path)

# # Example usage
# if __name__ == "__main__":

