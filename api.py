import random

import requests
from lxml import etree
from requests import Session

from config import *
from loguru import logger

log = logger.bind(user="m站辅助工具")
s: Session = requests.Session()


def 登录(账号, 密码):
    s = requests.Session()
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/login.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J17C Build/RKQ1.200826.002)"
    }
    data = {
        "username": 账号,
        "password": 密码,
        "ticket": "",
        "randstr": ""
    }
    r = s.post(url, headers=headers, data=data)
    log.info(f'返回信息:{r.json()}')
    if 'set-cookie' in r.headers:
        cookie = r.headers['set-cookie']
    else:
        cookie = r.headers['cookie']
    log.success(f'登录成功!  cookie: {cookie}')
    return cookie


def 获取用户信息():
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/stencil/mywallet.php'
    r = s.get(url)
    html = etree.HTML(r.text)
    uid = html.xpath('//a/@href')[0]
    uid = uid[uid.rfind("/") + 1:]
    try:
        用户名 = html.xpath("//div[@class='name']/a/text()")[0]
    except Exception:
        用户名 = html.xpath("//div[@class='name']/a/font/text()")[0]
    喵币 = html.xpath('//i/text()')[0]
    经验 = 获取经验()
    log.success(f'登录成功!  当前用户名: {用户名}  uid: {uid}  喵币: {喵币}   经验: {经验}')
    return 用户名, uid, 喵币, 经验


def 获取经验():
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/mobile/module/stencil/mine-page.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J17C Build/RKQ1.200826.002)"
    }
    r = s.get(url, headers=headers)
    html = etree.HTML(r.text)
    # 用户名 = html.xpath('//p[@class="name"]/font/text()')[0]
    # uid = html.xpath("//p[@class='id']/text()")[0].split("：")[1]
    经验 = html.xpath("//span[@class='progress-text']/text()")[0]
    return 经验


def 签到():
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/sign.php'
    data = {
        'sign': 1,
        'ticket': '',
        'randstr': ''
    }
    r = s.post(url, data=data)
    if r.text == 'null':
        raise Exception
    log.info(f'返回信息:{r.json()}')


def 领取签到奖励(num):
    # num: 从0开始 对应天数: 7/10/15/20/28

    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/sign-treasure.php'
    data = {
        'number': num
    }
    r = s.post(url, data=data)
    log.info(f'返回信息:{r.json()}')


def 点赞回复(tid, i):
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/comment-up.php'
    data = {
        'comment_id': tid,
        'type': 2
    }

    r = s.post(url, data=data)
    log.info(f'当前为第{i}次任务   id: {id}   返回信息:{r.json()}')


def 喜欢帖子(tid, i):
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/like-post.php'
    #      0=访问失败 1=喜欢成功 2=已经取消喜欢
    data = {
        'post_id': tid
    }
    r = s.post(url, data=data)
    log.info(f'当前为第{i}次任务   id: {id}   返回信息:{r.json()}')
    return r.json()['code']


#
# def 回复帖子(内容, i):
#     url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/comment-bbs.php'
#     data = {
#         'content': 内容,
#         'comment_id': comment_id,
#         'post_id': post_id,
#         'bbs_id': 15,
#         'type': 2,
#         'ticket': '',
#         'randstr': ''
#     }
#     r = s.post(url, data=data)
#     log.info(f'当前为第{i}次任务   回复内容: {内容}   返回信息:{r.json()}')
#     return r.json()['id']
#
#
# def 删除帖子(tid):
#     url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/delete/comment.php'
#     data = {
#         'comment_id': tid,
#         'type': 'bbs-post-floor',
#         'bbs_id': 15
#     }
#     r = s.post(url, data=data)
#     log.info(f' id: {tid}   返回信息:{r.json()}')


def 打赏帖子(tid, i):
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/reward.php'
    data = {
        'number': 1000,
        'post_id': tid,
        'type': 'post'
    }
    r = s.post(url, data=data)
    log.info(f'当前为第{i}次任务   tid: {tid}   返回信息:{r.json()}')
    return r.json()


def 领取打赏任务奖励():
    url = 'https://www.mfuns1.cn/wp-content/themes/LightSNS/module/action/task.php'
    data = {
        'task_id': 'rw6',
        'type': 'day'
    }
    r = s.post(url, data=data)
    log.info(f'返回信息:{r.json()}')
    return r.json()


def get_id(start=1):
    return str(random.randint(start, 178125))


# def 取随机评论内容():
#     内容 = ['20回复...', '评论任务 [s-6] ', "评论任务", '氵点经验', ' [s-1] ', ' [s-2] ', ' [s-6] ', ' [s-7] ',
#             ' [s-6]  [s-6]  [s-6] ']
#     return 内容[random.randint(0, len(内容) - 1)]


def Server酱推送(msg):
    url = f"https://sctapi.ftqq.com/{Server酱_key}.send"
    data = {"title": f"【m站辅助工具】", "desp": msg}
    r = s.post(url, data=data)
    log.info(f'返回信息:{r.json()}')


def pushplus推送(msg):
    url = "http://www.pushplus.plus/send"
    data = {"token": pushplus_key, "title": f"【m站辅助工具】", "content": msg}
    r = s.post(url, data=data)
    log.info(f'返回信息:{r.json()}')
