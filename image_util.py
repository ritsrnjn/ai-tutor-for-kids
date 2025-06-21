import openai_integration


def generate_image(prompt):
    # call gemini to generate an image
    image_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    
    return image_url



def generate_relevant_image(input_transcript):
    # make prompt for this transcript
    prompt = openai_integration.generate_image_prompt(input_transcript)

    return generate_image(prompt)