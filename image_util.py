import openai_integration
import requests
import base64
from io import BytesIO
from PIL import Image
import os


def generate_image(prompt):
    """
    Generate an image using DALL-E based on the prompt
    """
    try:
        # Use OpenAI DALL-E to generate the image
        image_url = openai_integration.generate_image_with_dalle(prompt)

        if image_url:
            return image_url
        else:
            # Fallback to a placeholder if DALL-E fails
            return generate_placeholder_image()

    except Exception as e:
        print(f"Error in generate_image: {e}")
        return generate_placeholder_image()


def generate_placeholder_image():
    """
    Generate a colorful placeholder image for when DALL-E is not available
    """
    # Return a fun educational placeholder - you could replace this with a local image
    placeholder_urls = [
        "https://via.placeholder.com/512x512/FFE135/FF6B6B?text=🎨+Learning+Fun!",
        "https://via.placeholder.com/512x512/4ECDC4/FFFFFF?text=🌟+Keep+Learning!",
        "https://via.placeholder.com/512x512/45B7D1/FFFFFF?text=📚+Hindi+Time!",
        "https://via.placeholder.com/512x512/FA709A/FFFFFF?text=🎯+Great+Job!",
        "https://via.placeholder.com/512x512/FEE140/333333?text=🚀+Amazing!"
    ]

    import random
    return random.choice(placeholder_urls)


def generate_relevant_image_and_highlight_word(input_transcript):
    """
    Generate a relevant image based on the AI response transcript
    """
    try:
        # Step 1: Generate an optimized prompt for the image
        prompt = openai_integration.generate_image_prompt(input_transcript)
        print(f"Generated image prompt: {prompt}")

        highlight_word = openai_integration.generate_highlight_word(prompt)
        print(f"Generated highlight word: {highlight_word}")

        # Step 2: Generate the actual image
        image_url = generate_image(prompt)
        print(f"Generated image URL: {image_url}")

        return image_url, highlight_word

    except Exception as e:
        print(f"Error generating relevant image: {e}")
        return generate_placeholder_image()
