from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

client = genai.Client(api_key='GEMINI_API_KEY')

def generate_image(prompt):
    """
    Generate an image based on the prompt
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    print("gemini response:")
    print(response)

    return response.text


