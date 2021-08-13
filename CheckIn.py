import requests
import json
from datetime import datetime, timedelta, timezone
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
timestamp=bj_dt.timestamp()
readingDate=datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
print(readingDate)
headers = {
        'Host': 'api.sfacg.com',
        'accept-charset': 'UTF-8',
        'authorization': '',
        'accept': 'application/vnd.sfacg.api+json;version=1',
        'user-agent': '',
        'sfsecurity': 'nonce=xxxx&timestamp=' + str(int(timestamp)) + '&devicetoken=xxxx&sign=xxxx',
        'accept-encoding': 'gzip',
        'cookie': '',
    }
def checkin():
    response = requests.get('https://api.sfacg.com/user/signInfo', headers=headers)
    print(response.text)
    response = requests.put('https://api.sfacg.com/user/signInfo', headers=headers)
    print(response.text)



def read():
    read_headers = {
        'Host': 'api.sfacg.com',
        'accept-charset': 'UTF-8',
        'authorization': '',
        'accept': 'application/vnd.sfacg.api+json;version=1',
        'user-agent': '',
        'sfsecurity': 'nonce=xxxx&timestamp=xxxx' + str(int(timestamp)) + '&devicetoken=xxxx&sign=xxxx',
        'content-type': 'application/json; charset=UTF-8',
        'content-length': '57',
        'accept-encoding': 'gzip',
        'cookie': '',
    }

    data = '{"seconds":9000,"entityType":2,"readingDate":"' + readingDate + '"}'
    response = requests.put('https://api.sfacg.com/user/readingtime', headers=read_headers, data=data)
    print(response.text)


def task():
    response = requests.get('https://api.sfacg.com/user/tasks?taskCategory=1&page=0&size=20', headers=headers)
    print(response.text)
    task = json.loads(response.text)
    n=0
    while n+1<=len(task["data"]):
        if "阅读" in task["data"][n]["name"]:
            requests.post('https://api.sfacg.com/user/tasks/'+str(task["data"][n]["taskId"]), headers=headers)
            print(response.text)
            read()
            read()
            requests.put('https://api.sfacg.com/user/tasks/' + str(task["data"][n]["taskId"]), headers=headers)
            print(response.text)
checkin()
task()
