# -*- coding: UTF-8 -*-
import requests
import re
import os
import time

session = requests.Session()


def login():
    xrsf = get_xrsf()
    while True:
        captcha = get_captcha()
        if post(xrsf, captcha):
            if is_login():
                return True
    return session


def get_xrsf():
    url = 'http://www.zhihu.com/#signin'
    res = session.get(url)
    xrsf = re.search('input type="hidden" name="_xsrf" value="(.*?)"', res.content).group(1)
    return xrsf


def get_captcha():
    url = 'http://www.zhihu.com/captcha.gif'
    res = session.get(url)
    format = re.search('.*?/(.*)', res.headers['Content-Type']).group(1)
    with open('pic.' + format, 'w')as f:
        f.write(res.content)
    os.system('open pic.' + format)
    captcha = raw_input()
    return captcha


def post(xrsf, captcha):
    print 'input your email'
    email = raw_input()
    print 'input your password'
    password = raw_input()
    data = {'_xsrf': xrsf, 'password': password, 'remember_me': 'true', 'email': email,
            'captcha': captcha}
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/46.0.2490.86 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
    time.sleep(1)
    url = 'http://www.zhihu.com/login/email'
    res = session.post(url, data=data, headers=headers)
    info = res.json()
    if info['r'] == 0:
        return True
    else:
        return False


def is_login():
    url = "http://www.zhihu.com/settings/profile"
    r = requests.get(url, allow_redirects=False)
    status_code = int(r.status_code)
    if status_code == 301 or status_code == 302:
        return False
    elif status_code == 200:
        return True

if __name__ == '__main__':
    session = login()