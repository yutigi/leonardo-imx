import json
import requests
import time
import validate_image as vi

api_key = "ca8ac37f-8790-4e1b-8ef6-639b93b56b9a"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# set the prompt here
prompt = "A mysterious phantom lurking in the darkness, its eerie grin sending shivers down your spine. As it emerges from the shadows, revealing its ghostly form, you can see translucent wisps of hair framing its spectral face. This chilling image, most likely a haunting painting, captures the essence of fear and intrigue. The details are so vivid, from the ghostly pallor of its skin to the malevolent glint in its eyes, that you can almost feel its icy breath on your neck. This high-quality depiction is sure to captivate and unsettle anyone who dares to gaze upon it. finally, recolor to black and white and present the red eyes and black mouth."

# Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

print("Get a presigned URL for uploading an image: %s" % response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()['uploadInitImage']['fields'])

url = response.json()['uploadInitImage']['url']

# For getting the image later
image_id = response.json()['uploadInitImage']['id']

image_file_path = "image/ref.jpg"
files = {'file': open(image_file_path, 'rb')}

response = requests.post(url, data=fields, files=files)  # Header is not needed

print("Upload image via presigned URL: %s" % response.status_code)


# Generate with Image to Image
url = "https://cloud.leonardo.ai/api/rest/v1/generations"

payload = {
    "public": False,
    "height": 512,
    "width": 512,
    "num_images": 1,
    # "num_inference_steps": 30,
    "presetStyle": "CINEMATIC",
    "modelId": "b820ea11-02bf-4652-97ae-9ac0cc00593d", # Setting model ID to Leonardo Diffusion
    "prompt": prompt,
    "init_image_id": image_id,  # Only allows for one Image
    "init_strength": 0.2,  # Must float between 0.1 and 0.9
}

response = requests.post(url, json=payload, headers=headers)

print("Generation of Images using Image to Image %s" % response.status_code)
print(response.text)

# Get the generation of images
generation_id = response.json()['sdGenerationJob']['generationId']

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(20)

response = requests.get(url, headers=headers)

print("send requests")
print(response.text)

# get image id
image_gen_id = response.json()["generations_by_pk"]["generated_images"][0]["id"]

# Delete the uploaded image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image/%s" % image_id

headers = {
    "accept": "application/json",
    "authorization": authorization
}

response = requests.delete(url, headers=headers)

# print(response.text)


def download():
    print("start download image")
    try:
        exec(open("download_image.py").read())
    except:
        print("download image failed")
        pass

def validate_and_download_image():
    print("check vaildate image")
    if vi.IsValidImage(image_gen_id):
        download()
    else:
        time.sleep(5)
        validate_and_download_image()

validate_and_download_image()