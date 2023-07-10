from fuzzywuzzy import fuzz
import requests

url = "https://shazam.p.rapidapi.com/search"

querystring = {"term":"kiss the rain","locale":"en-US","offset":"0","limit":"5"}

headers = {
	"X-RapidAPI-Key": "b194ff0091msh3c479f5135dfbccp129c58jsnd23e44fc997a",
	"X-RapidAPI-Host": "shazam.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())



def search(text, data):
    result = []
    for item in data:
        similarity = fuzz.ratio(text.lower(), item.lower())
        result.append(similarity)
    return result
