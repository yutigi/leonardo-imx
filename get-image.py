import requests


api_key = "ca8ac37f-8790-4e1b-8ef6-639b93b56b9a"
authorization = "Bearer %s" % api_key

userid = "bab93ae3-e56c-4426-9051-e2f4582130d5"

url = "https://cloud.leonardo.ai/api/rest/v1/generations/user/%s?offset=0&limit=1" % userid

headers = {
    "accept": "application/json",
    "authorization": authorization
}
# get image url
response = requests.get(url, headers=headers)

print(response.text)

image_url = "%s" % response.json()["generations"][0]["generated_images"][0]["url"]

print("==========================")
print( "image url = " + image_url)
print("downloading image")

# download image
data = requests.get(image_url,headers=headers).content 
  
# Opening a new file named img with extension .jpg 
# This file would store the data of the image file 
f = open('image/img.jpg','wb') 
  
# Storing the image data inside the data variable to the file 
f.write(data) 
f.close() 

print("download successful!")