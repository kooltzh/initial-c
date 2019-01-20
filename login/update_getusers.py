import requests
import json

URL = "http://localhost:5002/get_users"

data = {
    'target': 'admin2',
    'sender': 'Me',
    'msg': 'Hello good morning',
    'time': 'Today morning',
}

json_txt = json.dumps(data)

r = requests.post(URL, json=json_txt)

print(r.content)
