import requests

url = "http://localhost:5000/simplify"
data = {"text": "The attendees endeavored to commence the event expeditiously."}

response = requests.post(url, json=data)
print(response.json())