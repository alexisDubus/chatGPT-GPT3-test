import openai
import logging
import requests
import json
import datetime
import os
import sys
from dotenv import load_dotenv

load_dotenv()


# 3. Rename the `environ` to env object for more concise code
from os import environ as env

logging.basicConfig(level=logging.DEBUG)

try:  
  api_key = os.environ['API_KEY']
except KeyError: 
  print('[error]: `API_KEY` environment variable required')
  sys.exit(1)

prompt = "generate me a prompt about a beautiful sunset"
#prompt = "generate a worflow diagram for a simple web application based upon the MVC model."
#prompt = "Generate me a prompt about 'Devoteam' a consulting tech agency web page. The page must look young, fresh, appeal to the new generation."
#prompt = "generate me a prompt on how to be rich and successfull."
#prompt = "Generate me a prompt about a web agency marketing page. The page must look young, fresh, appeal to the new generation."
#prompt = "Generate me a prompt for a photo of a happy corgi puppy sitting and facing forward, studio light, longshot"
#prompt = "I am the head of this great place, and I just want so much more space !"
model_engine = "text-davinci-003"

def get_chat_gpt_prompt_response(prompt):
    try: 
            
        openai.api_key = api_key

        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens= 1024, 
            n=1, 
            stop=None, 
            temperature=0.9
        )
        contents = []
        for response in completion.choices:
            print(response.text)
            return response.text
            contents.add(response.text)

        return contents

    except Exception as e: 
        logging.debug('error {e}')

def open_ai_image_generation(prompt, enhanced_prompt):
    print(prompt + " "+ enhanced_prompt)
    
    try: 
        # Make a request to the OpenAI API to generate an image
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": "image-alpha-001",
                "prompt": enhanced_prompt
            })
        )
        print(response.json())
        # Check if the request was successful
        if response.status_code == 200:
            # Get the generated image from the response
            image_url = response.json()["data"][0]["url"]
                
            # Get the current date and time
            now = datetime.datetime.now()
            date_time = now.strftime("%Y-%m-%d-%H-%M-%S")

            # Download the image and save it with the date and time suffix
            response = requests.get(image_url)
            open(f"image_{date_time}.jpg", "wb").write(response.content)
            print(f"Image saved as image_{date_time}.jpg")
        else:
            print(f"Failed to generate image: {response.text}")
        
    except Exception as e: 
        logging.debug('error {e}')



another_prompt = get_chat_gpt_prompt_response(prompt)
open_ai_image_generation(prompt, another_prompt)