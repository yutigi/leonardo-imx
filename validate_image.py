import sys
import requests

def IsValidImage(generationId):

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

    # print(response.text)

    response_generationId = "%s" % response.json()["generations"][0]["generated_images"][0]["id"]

    bIsValid = str(generationId) == str(response_generationId)
    print("compare ->" + str(generationId) + " and " + str(response_generationId))
    if bIsValid:
        print("found image")
    else:
        print("image not found")

    return bIsValid


if __name__ == '__main__':
    IsValidImage(sys.argv[1:])
    pass