import requests
import json

URL = "http://localhost:5002/msg/send"

data = {
    'target': 'User D',
    'sender': 'Me',
    'msg': 'Hello good morning',
    'time': 'Today morning',
}

json_txt = json.dumps(data)

r = requests.post(URL, json=json_txt)

print(r.content)
