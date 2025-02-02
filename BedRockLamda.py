import json
import boto3
import os
import random
# Initialize the Bedrock client
bedrock = boto3.client('bedrock-runtime',region_name='ap-south-1')

color_palettes = {#Sophisticated and Elegant
    "Executive": "Navy Blue, Gold, White",
    "Prestige": "Deep Purple, Silver, Black",
    "Classic": "Burgundy, Cream, Gold", 
    # Modern and Tech-Focused
    "Metro": "Steel Grey, Electric Blue, White",
    "Innovation": "Teal, Silver, Black",
    "DigitalZen": "Cobalt Blue, Electric Purple, Silver",
    # Nature-Inspired
    "Serenity": "Sky Blue, Sage Green, White",
    "EarthTone": "Brown, Olive Green, Beige",
    "Oceanic": "Teal, Navy Blue, Sand",
    # Energetic and Dynamic
    "Fiery": "Red, Orange, Yellow",
    "Pulse": "Magenta, Lime Green, Black",
    "Velocity": "Electric Blue, Orange, Grey"
}

def generate_prompt(event):
    body = json.loads(event['body'])
    event_name = body.get('event_name')
    event_description = body.get('event_description', "a general theme")  # Default if not provided
    color_palette_type = body.get('colour_palette', "Executive")  # Default if not provided
    color_palette = color_palettes.get(color_palette_type)  # Default to "Executive" colors if key not found

    # Construct the prompt based on the number of parameters provided
    if event_description and color_palette:
        # Case with all three parameters
        prompt = (f"Design a captivating poster for {event_name}, blending {event_description}. "
                  f"Utilize a bold, sans-serif font for the event title and clean, modern typography for details. "
                  f"Employ a {color_palette} color scheme. Deliver a high-resolution poster suitable for both digital and print media.")
    elif event_description:
        # Case with two parameters (event_name and event_description)
        prompt = (f"Design a captivating poster for {event_name}, blending {event_description}. "
                  f"Utilize a bold, sans-serif font for the event title and clean, modern typography for details. "
                  f"Employ a {color_palette} color scheme. Deliver a high-resolution poster suitable for both digital and print media.")
    elif color_palette:
        # Case with two parameters (event_name and color_palette)
        prompt = (f"Design a poster for the event titled '{event_name}' using a blend of {event_description}. "
                  f"Use a bold, sans-serif font for the event title and clean typography for the details. "
                  f"Apply a color palette of {color_palette}. Deliver a high-res poster, suitable for both digital and print formats.")
    else:
        # Fallback if no valid two-parameter combination (event_name and default values)
        prompt = (f"Design a captivating poster for {event_name}, blending {event_description}. "
                  f"Utilize a bold, sans-serif font for the event title and clean, modern typography for details. "
                  f"Employ a {color_palette} color scheme. Deliver a high-resolution poster suitable for both digital and print media.")

    return prompt
    
    
def lambda_handler(event, context):
    # Retrieve the prompt from the incoming event
    prompt = generate_prompt(event)
    num_images = 1
    seed = random.randint(0, 2147483647)
    native_request = {
        "taskType": "TEXT_IMAGE",  # Specifies the task type as text-to-image generation
        "textToImageParams": {
            "text": prompt  # The text prompt used for image generation
        },
        "imageGenerationConfig": {
            "numberOfImages": num_images,  
            "quality": "standard",  # Image quality level
            "cfgScale": 8.0,  # Configuration scale parameter for the model
            "height": 512,  # Image height in pixels
            "width": 512,  # Image width in pixels
            "seed": seed  # Seed value for randomization (ensures reproducibility)
        }
    }
    request = json.dumps(native_request)

    try:
        # Call Amazon Bedrock to generate an image using the Titan Image Generator G1 model
        response = bedrock.invoke_model(modelId='amazon.titan-image-generator-v1',body=request)
        model_response = json.loads(response["body"].read().decode('utf-8'))
        generated_image=model_response.get('images')
        images = model_response.get('images', [])
        print('sucess function')
        # response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(images),# JSON array of Base64 strings
            'isBase64Encoded': False  
        }
        
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error generating image: {str(e)}")
        }
