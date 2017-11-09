# coding=utf-8
from bs4 import BeautifulSoup
from PIL import Image
import requests
import time
import os


User_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
session = requests.session()


def get_xrsf():
    url = "http://www.zhihu.com/"
    html = session.get(url, headers=User_agent,verify=True).content
    soup = BeautifulSoup(html, 'lxml')
    _xrsf = soup.select('input')[0].get('value')
    return _xrsf


def get_captcha():
    url = 'https://www.zhihu.com/captcha.gif?r='+str(int(time.time() * 1000))+'&type=login&lang=en'
    html = session.get(url, headers=User_agent,verify=True).content
    with open('captcha.jpg', 'wb') as f:
        f.write(html)
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except Exception as a:
        print '请到当目录%s手动查看验证码'%os.path.abspath('captcha.jpg')
    captcha = raw_input('请输入验证码')
    return captcha



def start_work():
    username = raw_input('请输入用户名：')
    password = raw_input('请输入登录密码：')
    data = {'_xsrf':get_xrsf(),
            'captcha':get_captcha(),
            'email':username,
            'password':password,
            }
    url = "https://www.zhihu.com/login/email"
    html = session.post(url=url, data=data, headers=User_agent).content
    index_html = session.get(url='http://www.zhihu.com/', headers=User_agent).content
    print html
    print index_html

if __name__ == '__main__':
    start_work()