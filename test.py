import requests
import json
import tqdm

with open('./result.json', 'r') as f:
  a = json.load(f)

url = 'http://13.59.81.160:3000/api/matrix'

for item in tqdm(a):
  myobj = {'matrix': item, 'type': 'v1'}
  x = requests.post(url, data = myobj)
