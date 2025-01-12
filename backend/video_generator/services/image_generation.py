import openai
import requests
import os

# Load the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
client = openai

def generate_image(prompt):
    response = client.images.generate(
        model = "dall-e-2",
        prompt = prompt,
        n = 1,
        size="256x256"
        )
    print(f"{response}")
    image_url = response.data[0].url
    return image_url


def download_image(image_url, filename):
    response = requests.get(image_url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename
