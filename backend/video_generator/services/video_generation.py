import openai
import requests
import os
import moviepy
print(moviepy.__file__)
import tempfile

# Load the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
client = openai



def generate_image(prompt, size="1024x1024"):
    """Generates an image from a prompt using OpenAI's DALL-E API."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size=size
    )
    image_url = response.data[0].url
    return image_url

def download_image(image_url, filename):
    """Downloads an image from a URL."""
    response = requests.get(image_url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def generate_video_with_sora(prompt, output_file="sora_video.mp4", frame_rate=1, num_frames=10):
    """
    Generates a video featuring Sora based on the prompt.

    Args:
    - prompt: The description used to generate frames.
    - output_file: The name of the final video file.
    - frame_rate: Frames per second for the video.
    - num_frames: Number of frames (images) to generate.

    Returns:
    - The filename of the generated video.
    """
    images = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(num_frames):
            # Generate a specific prompt for each frame
            frame_prompt = f"{prompt}, frame {i + 1}, featuring Sora in a dynamic pose"
            print(f"Generating frame {i + 1} with prompt: {frame_prompt}")
            image_url = generate_image(frame_prompt)
            
            # Download the image
            filename = os.path.join(temp_dir, f"frame_{i + 1}.png")
            download_image(image_url, filename)
            images.append(filename)

        # Create the video from the images
        # clip = ImageSequenceClip(images, fps=frame_rate)
        # clip.write_videofile(output_file, codec="libx264")

    return output_file

# Example usage
prompt = "Sora in a fantasy forest with glowing trees and mystical creatures"
video_file = generate_video_with_sora(prompt)
print(f"Video generated: {video_file}")
