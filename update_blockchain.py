import requests

ipAddress = '25.57.238.186'

URL = 'http://' + ipAddress + ':5000/msg/new'

JSON = {
    'sender': 'a',
    'recipient': 'b',
    'original_msg': 'hello',
    'modified_msg': 'bello',
    'similarity': '10'
}

try:
    r = requests.post(url=URL, json=JSON)
except:
    print("failed to connect to {}".format(URL))
    exit()

print(r.content)

# next

JSON = {
    'sender': 'c',
    'recipient': 'd',
    'original_msg': 'how are you',
    'modified_msg': 'how are you too?',
    'similarity': '10'
}

try:
    r = requests.post(url=URL, json=JSON)
except:
    print("failed to connect to {}".format(URL))
    exit()

print(r.content)

# next

JSON = {
    'sender': 'b',
    'recipient': 'c',
    'original_msg': 'bello',
    'modified_msg': 'bello2',
    'similarity': '10'
}

try:
    r = requests.post(url=URL, json=JSON)
except:
    print("failed to connect to {}".format(URL))
    exit()

print(r.content)

# next

URL = 'http://' + ipAddress + ':5000/mine'
try:
    r = requests.get(url=URL)
except:
    print("failed to connect to {}".format(URL))
    exit()

print(r.content)

# next

URL = 'http://' + ipAddress + ':5000/msg/trace'

JSON = {
    'sender': 'b',
    'recipient': 'c',
    'msg': 'bello2'
}

try:
    r = requests.post(url=URL, json=JSON)
except:
    print("failed to connect to {}".format(URL))
    exit()

print(r.content)
