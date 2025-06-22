import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = openai.OpenAI()

def generate_image_prompt(context):
    """
    Generate a kid-friendly, educational image prompt based on the AI response context
    """
    try:
        # Use GPT to create a kid-friendly image prompt
        response = client.chat.completions.create(
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

def generate_highlight_word(image_prompt):
    """
    Extract the main keyword from the generated image prompt
    """
    try:
        # Use GPT to extract the keyword
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at extracting the single most important Hindi keyword from a DALL-E image prompt. Return only the word."
                },
                {
                    "role": "user",
                    "content": f"From this prompt: '{image_prompt}', what is the main Hindi word a child is learning? For example, if the prompt is 'A happy yellow (Pīlā) sun smiling', you would return 'Pīlā'. Only return the word."
                }
            ],
            max_tokens=50,
            temperature=0.2
        )

        highlight_word = response.choices[0].message.content.strip()
        return highlight_word

    except Exception as e:
        print(f"Error generating highlight word: {e}")
        return image_prompt.split(" ")[-1]  # Fallback


def generate_image_with_dalle(prompt):
    """
    Generate an image using DALL-E 3 based on the prompt
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="hd",
            style="vivid",
            response_format="url"
        )

        image_url = response.data[0].url
        return image_url

    except Exception as e:
        print(f"Error generating image with DALL-E: {e}")
        return None

def create_enhanced_image_prompt(agent_response: str) -> dict:
    """
    Analyzes the agent's response to create a targeted image prompt
    and provide English/Hindi translations for the key concept.
    """
    try:
        print(f"[DEBUG] 2. Sending to OpenAI for analysis: {agent_response}\n")
        system_prompt = """
You are an AI assistant for a kids' Hindi learning app. Your task is to analyze the AI tutor's response, identify the core learning concept, and create a structured JSON object.

The user is a child learning Hindi. Your output will be used to generate a helpful visual aid.

1.  **Analyze the Response**: Read the tutor's response and identify the main vocabulary word or concept being taught. This is the "pain point" for the child to learn.
2.  **Create Image Prompt**: Generate a very simple, clear, and kid-friendly image prompt for DALL-E. The prompt should visually represent the core concept. Use simple terms. For example, instead of "A majestic elephant majestically traversing the plains", use "A cute, friendly elephant."
3.  **Extract English Word**: Identify the English word for the core concept.
4.  **Extract Hindi Word**: Identify the Hindi word (in Hindi script) for the core concept.

**Output Format**:
Return a single JSON object with three keys:
- "image_prompt": The simple DALL-E prompt.
- "english_word": The key concept in English.
- "hindi_word": The key concept in Hindi script.

**Example**:
Tutor Response: "The Hindi word for elephant is हाथी, pronounced as HAA-THEE."
Your JSON Output:
{
  "image_prompt": "A cute, friendly cartoon elephant smiling.",
  "english_word": "Elephant",
  "hindi_word": "हाथी"
}
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the AI tutor's response: '{agent_response}'"}
            ]
        )

        response_content = response.choices[0].message.content.strip()
        print(f"[DEBUG] 3. Received from OpenAI: {response_content}")

        # Parse the JSON response
        try:
            response_data = json.loads(response_content)
            print(f"[DEBUG] 3. Received from OpenAI: {json.dumps(response_data, indent=2, ensure_ascii=False)}")

            # Validate the response and provide fallbacks for empty fields
            image_prompt = response_data.get('image_prompt', '').strip()
            english_word = response_data.get('english_word', '').strip()
            hindi_word = response_data.get('hindi_word', '').strip()

            # If any field is empty, provide meaningful fallbacks
            if not image_prompt:
                image_prompt = f"A colorful cartoon illustration for kids showing: {agent_response[:100]}"
                print(f"[DEBUG] Using fallback image prompt: {image_prompt}")

            if not english_word:
                english_word = "Learning"
                print(f"[DEBUG] Using fallback English word: {english_word}")

            if not hindi_word:
                hindi_word = "सीखना"
                print(f"[DEBUG] Using fallback Hindi word: {hindi_word}")

            return {
                "image_prompt": image_prompt,
                "english_word": english_word,
                "hindi_word": hindi_word
            }

        except json.JSONDecodeError as e:
            print(f"[DEBUG] Failed to parse OpenAI response as JSON: {e}")
            print(f"[DEBUG] Raw response: {response_content}")
            # Return fallback response
            return {
                "image_prompt": f"A colorful cartoon illustration for kids showing: {agent_response[:100]}",
                "english_word": "Learning",
                "hindi_word": "सीखना"
            }

    except Exception as e:
        print(f"Error creating enhanced image prompt: {e}")
        # Return fallback response
        return {
            "image_prompt": f"A colorful cartoon illustration for kids showing: {agent_response}",
            "english_word": "Learning",
            "hindi_word": "सीखना"
        }

if __name__ == '__main__':
    # Example usage for testing
    sample_response = "The Hindi word for lion is शेर, pronounced as SH-AY-R."
    enhanced_prompt_data = create_enhanced_image_prompt(sample_response)
    print("--- Testing create_enhanced_image_prompt ---")
    print(f"Input: {sample_response}")
    print("Output:")
    # Pretty print the JSON output
    print(json.dumps(enhanced_prompt_data, indent=2, ensure_ascii=False))

    # Test the fallback case from a simple prompt
    sample_context = "A happy yellow (Pīlā) sun smiling"
    prompt = generate_image_prompt(sample_context)
    highlight = generate_highlight_word(prompt)
    print("\n--- Testing original functions ---")
    print(f"Context: {sample_context}")
    print(f"Generated Prompt: {prompt}")
    print(f"Highlight Word: {highlight}")
