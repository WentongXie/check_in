from Push import PushMessage
import re
import requests
import logging
import traceback
from bs4 import BeautifulSoup
from urllib import parse
import cloudscraper
import http.cookies

header = {
    "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": r"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

def YamiboLogin(session, account, password):
    login_info_url = r"https://bbs.yamibo.com/member.php?mod=logging&action=login&mobile=2"
    login_info_rsp = session.get(login_info_url, headers=header)
    login_info_bs = BeautifulSoup(login_info_rsp.text, "html.parser")
    form_hash = login_info_bs.find("input", id="formhash")
    assert form_hash != None and form_hash.get("value") != None, login_info_rsp.text
    form_hash = form_hash.get("value")
    login_url = login_info_bs.find("form", id="loginform")
    assert login_url != None and login_url.get("action") != None, login_info_rsp.text
    login_url = login_url.get("action")
    login_url = parse.urljoin("https://bbs.yamibo.com/", login_url)
    logging.info("login_hash: {}, form_hash:{}".format(login_url, form_hash))
    login = session.post(login_url, headers=header,
                         data=YamiboGetLoginData(account, password, form_hash))
    uid = re.search(r'''uid=(\d+)&''', login.text)
    assert uid != None, login.text
    uid = uid.group(1)
    logging.info("uid: {}".format(uid))
    return uid


def YamiboGetLoginData(account, password, form_hash):
    post_data = {
        "formhash": form_hash,
        "referer": r"https://bbs.yamibo.com/",
        "fastloginfield": "username",
        "cookietime": 2592000,
        "username": account,
        "password": password,
        "questionid": "0",
        "answer": ""
    }
    return post_data


def YamiboLogout(session, uid):
    rsp = session.get(
        "https://bbs.yamibo.com/home.php?mod=space&uid={}&do=profile&mycenter=1&mobile=2".format(uid), headers=header)
    home_bs = BeautifulSoup(rsp.text, "html.parser")
    logout_url = home_bs.find("a", class_="pn")
    assert logout_url != None and logout_url.get("href") != None, rsp.text
    logout_url = logout_url.get("href")
    logout_url = parse.urljoin("https://bbs.yamibo.com/", logout_url)
    logout_rsp = session.get(logout_url, headers=header)
    assert logout_rsp.text.find("您已退出站点") != -1, logout_rsp.text


def YamiboSign(session):
    rsp = session.get("https://bbs.yamibo.com/plugin.php?id=zqlj_sign&mobile=2")
    sign_bs = BeautifulSoup(rsp.text, "html.parser")
    sign_url = sign_bs.find("a", class_="btna")
    assert sign_url != None and sign_url.get("href") != None, rsp.text
    sign_url = sign_url.get("href")
    sign_url = parse.urljoin("https://bbs.yamibo.com/", sign_url)
    sign_rsp = session.get(sign_url, headers=header)
    assert sign_rsp.text.find("打卡成功") != -1, sign_rsp.text
    logging.debug(sign_rsp.text)


def YamiboCheck(cookie):
    try:
        with requests.Session() as s:
            s.headers.update(header)
            cookie = http.cookies.SimpleCookie(cookie)
            cookie_jar = requests.cookies.RequestsCookieJar()
            cookie_jar.update(cookie)
            s.cookies.update(cookie_jar)
            #uid = YamiboLogin(s, account, password)
            YamiboLogUserInfo(s)
            YamiboSign(s)
            YamiboLogUserInfo(s)
            #YamiboLogout(s, uid)
            logging.info("YamiboCheck finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("yamibo check failed.", "yamibo check failed.")


def YamiboLogUserInfo(session):
    rsp = session.get("https://bbs.yamibo.com/home.php?mod=spacecp&ac=credit")
    home_bs = BeautifulSoup(rsp.text, "html.parser")
    logging.debug(rsp.text)
    info = home_bs.find("ul", class_="creditl mtm bbda cl")
    assert info is not None, rsp.text
    logging.info(info.get_text())


def main():
    logging.basicConfig(level=logging.INFO)
    YamiboCheck("cookie")
    pass


if __name__ == "__main__":
    main()
