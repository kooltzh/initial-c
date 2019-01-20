import requests
import json

URL = "http://localhost:5002/msg/send"

data = {
    'target': 'admin3',
    'sender': 'Me',
    'msg': 'Hello! Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
    'time': 'Today morning',
}

r = requests.post(URL, json=data)

print(r.content)
