import requests

with open("input.json") as fl:
    data = json.load(fl)

x = requests.post("http://localhost:8000", json=data)
print(x.json())