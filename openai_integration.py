import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_image_prompt(context):
    """
    Generate a kid-friendly, educational image prompt based on the AI response context
    """
    try:
        # Use GPT to create a kid-friendly image prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating kid-friendly, educational image prompts for a Hindi learning app."
                },
                {
                    "role": "user",
                    "content": f"Based on this AI tutor response about learning Hindi: '{context}', create a simple image prompt that would help a child visualize and remember the key concept. The prompt should be suitable for DALL-E image generation. Focus on the main subject(animal, bird, colour emotion, etc.)"
                }
            ],
            max_tokens=3000,
            temperature=0.7
        )

        prompt = response.choices[0].message.content.strip()
        return prompt

    except Exception as e:
        print(f"Error generating image prompt: {e}")
        # Fallback to a simple prompt
        return f"Colorful cartoon illustration for children showing: {context}. Bright, fun, and educational style."

def generate_highlight_word(prompt):
    """
    Generate a highlight word based on the prompt
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating highlight words for a Hindi learning app. ONLY return the word, no other text."
                },
                {
                    "role": "user",
                    "content": f"Based on this image prompt: '{prompt}', create a highlight word that would help a child visualize and remember the key concept. Name on the main subject(animal, bird, colour, emotion, etc.) in both English and Hindi"
                }
            ],
            max_tokens=3000,
            temperature=0.7
        )

        word = response.choices[0].message.content.strip()
        return word

    except Exception as e:
        print(f"Error generating highlight word: {e}")
        return None


def generate_image_with_dalle(prompt):
    """
    Generate an image using DALL-E based on the prompt
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )

        image_url = response['data'][0]['url']
        return image_url

    except Exception as e:
        print(f"Error generating image with DALL-E: {e}")
        return None
