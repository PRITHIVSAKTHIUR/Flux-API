import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
#To submit an image generation task with FLUX 1.1> , create a request:
def submit_request():
    response = requests.post(
        'https://api.bfl.ml/v1/flux-pro-1.1-ultra',
        headers={
            'accept': 'application/json',
            'x-key': os.environ.get("BFL_API_KEY"),
            'Content-Type': 'application/json',
        },
        json={
            'prompt': 'Simple Doodle, A cartoon drawing of a boy with short black hair and a yellow shirt. The boy has a smile on his face. The background is a peach color and there are green leaves on either side of the boy. There are white dots on the peach color background.',
            'width': 1920,
            'height': 1080,
        },
    )
    
    if response.status_code == 200:
        request_data = response.json()
        print("Request Submitted:", request_data)
        return request_data.get("id")
    else:
        print("Error submitting request:", response.text)
        return None

# To retrieve the result, you can poll the get_result endpoint:
def poll_for_result(request_id):
    while True:
        time.sleep(0.5)
        result = requests.get(
            'https://api.bfl.ml/v1/get_result',
            headers={
                'accept': 'application/json',
                'x-key': os.environ.get("BFL_API_KEY"),
            },
            params={'id': request_id},
        ).json()
        
        if result["status"] == "Ready":
            print("Result:", result['result']['sample'])
            break
        else:
            print("Status:", result["status"])

if __name__ == "__main__":
    request_id = submit_request()
    if request_id:
        poll_for_result(request_id)