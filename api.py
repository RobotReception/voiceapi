import requests

url = 'http://127.0.0.1:8000/send-message/'
payload = {'message': 'Your message here'}
response = requests.post(url, json=payload)

print(response.json())
