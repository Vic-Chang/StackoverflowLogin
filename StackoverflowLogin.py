import traceback
import requests
import config
import time
from bs4 import BeautifulSoup

# 保持連線，並偽造標頭
rs = requests.Session()
rs.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


# 登入 Stackoverflow
def login_stackoverflow():
    print('登入中...')
    url = 'https://stackoverflow.com/users/login'
    account = config.STACKOVERFLOW_ACCOUNT['account']
    password = config.STACKOVERFLOW_ACCOUNT['password']
    params = {'email': account, 'password': password}
    r = rs.post(url, params)
    check_page_string = ['Are you a human being?', 'The email is not a valid email address.']
    if any(x in r.text for x in check_page_string):
        print('登入需驗證!')
        return False
    else:
        print('成功登入!')
        return True


# 進入第一篇推薦文
def into_first_recommend_article():
    url = 'https://stackoverflow.com'
    r = rs.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    post_url = url + soup.select('#question-mini-list > a')[0]['href']
    rs.get(post_url)


# 傳送錯誤資訊至 Line
def exception_notify(error_msg, detail=''):
    headers = {"Authorization": "Bearer " + config.LINE_NOTIFY_TOKEN}
    params = {"message": 'Stackoverflow 登入程式運行失敗，原因 : ' + error_msg + '\n詳細原因:\n' + detail}
    requests.post(config.LINE_NOTIFY_URL, headers=headers, params=params)


if __name__ == '__main__':
    try:
        success = login_stackoverflow()
        if success:
            into_first_recommend_article()
        else:
            exception_notify('登入需要驗證')
    except Exception as e:
        print('發生錯誤，發送 Line 通知...')
        exception_notify(str(e), traceback.format_exc())
    print('即將關閉程式...')
    time.sleep(5)