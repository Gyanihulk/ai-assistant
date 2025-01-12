import openai
import os

# Load the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
openai.api_key = openai_api_key

def generate_prompts(topic, num_prompts=3):
    print(f"Generating prompts for topic: {topic}")
    prompts = []

    try:
        for _ in range(num_prompts):
            # Correct method and model name
            response = openai.chat.completions.create(
                model="gpt-4",  # Use "gpt-3.5-turbo" if "gpt-4" is unavailable
                messages=[
                    {"role": "system", "content": "You are a creative assistant."},
                    {"role": "user", "content": f"Generate a creative prompt for: {topic}"}
                ]
            )
            # Extract the generated content
            prompt = response.choices[0].message.content.strip()
            prompts.append(prompt)
            # print(f"Generated Prompt: {prompt}")
   
    except Exception as e:
        print(f"Unexpected Error: {e}")
    return prompts
''





# Example usage
if __name__ == "__main__":
    topic = "Ganga Mata"
    prompts = generate_prompts(topic, num_prompts=3)
    for i, prompt in enumerate(prompts, 1):
        print(f"Prompt {i}: {prompt}")
