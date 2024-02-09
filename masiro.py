import logging, requests
import traceback
from bs4 import BeautifulSoup
from Push import PushMessage
import http.cookies

header = {
    "User-Agent": r"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Accept-Language": r"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

def MasiroLogin(session, account, password):
    login_info_rsp = session.get("https://masiro.me/admin/auth/login")
    login_info_bs = BeautifulSoup(login_info_rsp.text, "html.parser")
    token = login_info_bs.find("input", {"name":"_token"})
    assert token != None and token.get("value") != None, login_info_rsp.text
    token = token.get("value")
    logging.info(token)
    payload = {
        "username": account,
        "password": password,
        "activationcode":"",
        "remember": 1,
        "_token": token
    }
    login_rsp = session.post("https://masiro.me/admin/auth/login", data=payload)
    login_rsp.encoding = "utf-8"
    logging.info(login_rsp.json())

def MasiroLogUserInfo(session):
    admin_rsp = session.get("https://masiro.me/admin")
    admin_bs = BeautifulSoup(admin_rsp.text, "html.parser")
    info = admin_bs.find("li", class_="user-header")
    logging.info(info.get_text())

'''
def MasiroCheck(account, password):
    try:
        with requests.Session() as s:
            s.headers.update(header)
            MasiroLogin(s, account, password)
            MasiroLogUserInfo(s)
            MasiroSignIn(s)
            MasiroLogUserInfo(s)
            MasiroLogout(s)
            logging.info("MasiroCheck finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("masiro check failed.", "masiro check failed.")
'''

def MasiroCheck(cookie):
    try:
        with requests.Session() as s:
            s.headers.update(header)
            cookie = http.cookies.SimpleCookie(cookie)
            cookie_jar = requests.cookies.RequestsCookieJar()
            cookie_jar.update(cookie)
            s.cookies.update(cookie_jar)
            MasiroLogUserInfo(s)
            MasiroSignIn(s)
            MasiroLogUserInfo(s)
            logging.info("MasiroCheck finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("masiro check failed.", "masiro check failed.")
    

def MasiroLogout(session):
    logout_rsp = session.get("https://masiro.me/admin/auth/logout")
    logging.debug(logout_rsp.text)
    logout_rsp.encoding = "utf-8"
    assert logout_rsp.text.find("登录") != -1, logout_rsp.text
    logging.debug(logout_rsp.text)

def MasiroSignIn(session):
    sign_rsp = session.get("https://masiro.me/admin/dailySignIn")
    #sign_rsp.encoding = "utf-8"
    result = sign_rsp.json()["msg"]
    assert result.find("打卡成功") != -1 or result.find("已打卡") != -1, sign_rsp.text
    logging.info(result)

def main():
    logging.basicConfig(level=logging.INFO)
    #MasiroCheck("account", "password")
    MasiroCheck("cookie")
    print("import masiro")

if __name__ == "__main__":
    main()
