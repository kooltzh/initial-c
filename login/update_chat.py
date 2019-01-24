import requests
import json

URL = "http://localhost:5002/msg/send"

data = {
    'target': 'User C',
    'sender': 'Me',
    'msg': 'Hey! You are running Vue in development mode. Make sure to turn on production mode when deploying for production.',
    'time': 'Today morning',
}

r = requests.post(URL, json=data)

print(r.content)
