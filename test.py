import requests
import json

with open('./result.json', 'r') as f:
  a = json.load(f)

url = 'http://13.59.81.160:3000/api/matrix'

for item in a:
  myobj = {'matrix': item, 'type': 'v0'}
  x = requests.post(url, data = myobj)