import json

def write_json(matrix):
  with open("result.json", "r") as f:
    result = json.load(f)
  result.append(matrix)
  with open("result.json", "w") as f:
    json.dump(result, f)