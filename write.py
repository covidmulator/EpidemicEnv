import json

def write_json(matrix):
  with open("result.json", "w") as f:
    json.dump(matrix, f)