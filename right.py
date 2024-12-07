#https://github.com/hedecken/Sign-right.com.cn

import re
import urllib
import requests
import hashlib
import logging
import traceback
from Push import PushMessage
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding':'gzip, deflate, br',
    "Content-Type":"application/x-www-form-urlencoded"
}


# md5加密
def md5_string(in_str):
    md5 = hashlib.md5()
    md5.update(in_str.encode("utf8"))
    result = md5.hexdigest()
    return result


# 登录模块
def login(user, password):
    datas = {'username': user, "password": password}
    r = requests.post(
        "https://www.right.com.cn/forum/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=LgEx5&inajax=1",
        data=datas, headers=headers)
    logging.info(r.text)
    if r.text.find("登录失败") != -1 or r.text.find("密码错误") != -1 or r.text.find("错误") != -1:
        rule = "(?<=\\[CDATA\\[).*(?=<script)"
        return re.findall(rule, r.text)[0]
    else:
        return requests.utils.dict_from_cookiejar(r.cookies)


# 获取现有积分
def get_coin(cookies):
    r = requests.get("https://www.right.com.cn/forum/home.php?mod=spacecp&ac=credit&showcredit=1", headers=headers,cookies=cookies)
    logging.debug(r.text)
    rule = "(?<=showmenu\">).*(?=</a>)"
    return re.findall(rule, r.text)[0]


# 获取随机的一言
def get_one():
    r=requests.get("https://v1.hitokoto.cn/?C=i&encode=text&charset=gbk")
    return r.text


# 获取要留言的帖子（灌水区最新的一条帖子）
def get_tid(cookies):
    r=requests.get("https://www.right.com.cn/forum/forum.php?mod=forumdisplay&fid=48&filter=lastpost&orderby=lastpost",headers=headers,cookies=cookies)
    logging.debug(r.text)
    rule="(?<=href=\"thread-).*(?=-1-1.html)"
    result=re.findall(rule, r.text)
    return result[0]


# 进入帖子后获取formhash，再进行回复操作
def put_reply(cookies,tid):
    r = requests.get("https://www.right.com.cn/forum/thread-"+tid+"-1-1.html",headers=headers, cookies=cookies)
    rule = "(?<=formhash=).*(?=\">)"
    formhash = re.findall(rule, r.text)[0]
    reply=get_one()
    datas="formhash="+formhash+"&message="+urllib.parse.quote(reply.encode('gb2312'))
    r=requests.post("https://www.right.com.cn/forum/forum.php?mod=post&action=reply&fid=48&tid="+tid+"&fromvf=1&extra=page=1&replysubmit=yes&infloat=yes&handlekey=vfastpost&inajax=1",data=datas,headers=headers,cookies=cookies)
    logging.debug(r.request.body)
    if r.text.find("回复发布成功") != -1:
        logging.debug(r.text)
        logging.info("回复帖子tid: "+tid+"成功，回复的内容是:"+reply)
    else:
        logging.error("回复帖子失败，原因是："+r.text)
        PushMessage("right sign failed.", r.text)

def right_sign(cookie):
    try:
        s_cookie = SimpleCookie()
        s_cookie.load(cookie)
        cookies = {k: v.value for k, v in s_cookie.items()}
        coin = get_coin(cookies)
        logging.info("目前" + coin)
        coin = get_coin(cookies)
        logging.info("目前" + coin)
        '''
        # 执行部分
        cookies = login(account, md5_string(password))
        if str(cookies).find("登录失败") != -1 or str(cookies).find("密码错误") != -1 or str(cookies).find("错误") != -1:
            logging.error("用户： " + account + " " + cookies)
            PushMessage("right sign failed.", cookies)
        else:
            coin = get_coin(cookies)
            logging.info("用户: " + account + " 登录成功\n\r目前" + coin)
            #tid=get_tid(cookies)
            #put_reply(cookies,tid)
        '''
        logging.info("right sign finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("right sign failed.", str(e))

def main():
    logging.basicConfig(level=logging.INFO)
    right_sign("cookie")
    pass

if __name__ == "__main__":
    main()
