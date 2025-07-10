import requests

url = 'http://127.0.0.1:5000/simplify'
data = {
    'text': 'The cat is sitting on the mat.'
}

response = requests.post(url, json=data)
print(response.json())
