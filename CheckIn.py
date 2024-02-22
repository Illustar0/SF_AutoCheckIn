import requests
import json, os, time
from datetime import datetime, timedelta, timezone
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
timestamp = bj_dt.timestamp()
readingDate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


headers = {
    'Host': 'api.sfacg.com',
    'accept-charset': 'UTF-8',
    'authorization': 'Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=',
    'accept': 'application/vnd.sfacg.api+json;version=1',
    'user-agent': 'boluobao/4.6.36(android;22)/OPPO',
    'sfsecurity': f'nonce=EE94F4D4-CC0B-43B6-BFF2-6CB72CE8698B&timestamp={int(timestamp)}&devicetoken=F632BBEC-F075-39B5-A2C8-3234F5CBF99D&sign=7778A67648C9D95483E466D9D341FEA1',
    'accept-encoding': 'gzip',
}



# 创建cookie.txt文本
if not os.path.exists("cookie.txt"):
    open("cookie.txt", "a")

def read_cookie():
    with open('cookie.txt') as fb:
        cookie = fb.read() 
        headers['Cookie'] = cookie
    return headers
        
        
def postrequests(api, headers, data):
    read_cookie()
    return requests.post(api, headers=headers, data=data).json()
    
def getrequests(api):
    read_cookie()
    return requests.get(url=api, headers=headers).json()
    
def putrequests(api, put_headers, data):
    read_cookie()
    return requests.put(api, headers=put_headers, data=data).json()
        
    

def task():
    read_cookie()
    print("运行时间:",readingDate)
    ReadTime = {
        "seconds":3605,
        "readingDate":readingDate,
        "entityType":2
    }
    ListenTime = {
        "seconds": 3605,
        "readingDate": readingDate,
        "entityType": 3
    }
    ReadData = json.dumps(ReadTime)
    ListenData = json.dumps(ListenTime)
    put_headers = headers
    put_headers['accept-encoding'] = 'gzip'
    # put_headers['content-length'] = '57'
    # 不再对 content-length 进行硬编码
    put_headers['content-type'] = 'application/json; charset=UTF-8'
    result = putrequests("https://api.sfacg.com/user/newSignInfo",put_headers,ReadData)
    print(result['status']['msg'])
    if result['status']['msg'] == '需要登录才能访问该资源':
        return result['status']['msg']
    if result['status']['msg'] == '签到系统在每日凌晨0~1点之间进行维护,请您选在其他时间签到哦':
        return result['status']['msg']
    if result['status']['msg'] == '您今天已经签过到了,请明天再来':
        return result['status']['msg']

    print("开始执行任务")
    responed = putrequests('https://api.sfacg.com/user/readingtime', put_headers, data=ListenData)
    postrequests('https://api.sfacg.com/user/tasks/4', headers,data=ListenData)
    postrequests('https://api.sfacg.com/user/tasks/5', headers,data=ListenData)
    postrequests('https://api.sfacg.com/user/tasks/17', headers, data=ListenData)
    for _ in range(3):
        r = putrequests('https://api.sfacg.com/user/readingtime', put_headers, ReadData)
        print(r)
        time.sleep(0.5)
        putrequests('https://api.sfacg.com/user/tasks/5', put_headers, data=ListenData)
        putrequests('https://api.sfacg.com/user/tasks/4', put_headers, data=ListenData)
        putrequests('https://api.sfacg.com/user/tasks/17', put_headers, data=ListenData)


def check_cookie():  # 验证cookie信息是否失效
    read_cookie()
    result = requests.get('https://api.sfacg.com/user?', headers=headers).json()
    money = requests.get('https://api.sfacg.com/user/money',headers=headers).json()
    # if '需要登录才能访问该资源' not in result['status']['msg']:
    try:
        nick_Name = result['data']['nickName']
        fireMoneyRemain = money['data']['fireMoneyRemain']
        user_vipLevel = money['data']['vipLevel']
        print("账号名称:", nick_Name, "\t火卷余额:", fireMoneyRemain, "\tVIP:", user_vipLevel)
        print("Cookie 凭证有效！")
    except:
        print('Cookie凭证失效  httpCode:', result['status']['httpCode'])
        session_APP = input("Please input you session_APP:")
        SFCommunity = input("Please input you SFCommunity:")
        cookie = f"session_APP={session_APP};.SFCommunity={SFCommunity}"
        with open("cookie.txt", 'w', encoding='utf-8') as file:
            file.write(cookie)
        print("退出程序")
        quit()



# def checkin():
    # print("运行时间:",readingDate)
    # date_warn = "签到日期: {}年{}月{}日"
    # for data in getrequests('https://api.sfacg.com/user/signInfo', headers)['data']:
        # print(date_warn.format(data['year'], data['month'], data['day']))
    # put_response = requests.put('https://api.sfacg.com/user/signInfo', headers=headers).json()
    # if "您今天已经签过到了,请明天再来" in put_response['status']:
        # print("签到提醒: {}".format(put_response['status']['msg']))
        # print("退出程序");quit()
    # else:
        # print("检测到今天还未签到，已自动签到和完成任务")
        # print(put_response['status']['msg'])
        # task()
        
check_cookie()
# checkin()
task()

