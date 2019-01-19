import requests, time

def calling_func():
    URL = 'http://localhost:5000/mine'
    try:
        r = requests.get(url = URL)
    except:
        print ("failed to connect to {}".format(URL))
        exit()

    resp_json = r.json()

    if resp_json['message'] == "New Block Forged":
        print('{}, index = {}'.format(resp_json['message'], resp_json['index']))

PERIOD = 10

while True:
    try:
        startTime = time.time()
        calling_func()
        sleepTime = PERIOD - (time.time() - startTime)
        # if sleepTime < 0:
        #     print ('The program take longer time to process, exiting..')
        #     break
        # else:
        #     time.sleep(sleepTime)
        if sleepTime > 0:
            time.sleep(sleepTime)
    except:
        break
