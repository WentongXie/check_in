import requests
import logging
import traceback
from http.cookies import SimpleCookie
from Push import PushMessage

header = {
    "User-Agent": r"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
}

def get_token_payload(account, password):
    return {
        "nickname":"",
        "username": account,
        "password": password,
        "code": "",
        "img_code": "",
        "invitation_code": "",
        "token": "",
        "smsToken": "",
        "luoToken": "",
        "confirmPassword": "",
        "loginType": "",
    }

def parse_cookie(cookie):
    s_cookie = SimpleCookie()
    s_cookie.load(cookie)
    cookies = {k: v.value for k, v in s_cookie.items()}
    return cookies

def yurifans(account, password):
    #cookie = parse_cookie(cookie)
    try:
        with requests.session() as s:
            s.headers.update(header)
            bearer, credit = get_token(s, account, password)
            s.headers.update({"Authorization": "Bearer {}".format(bearer)})
            finish_user_mission(s)
            new_credit = get_userinfo(s)
            assert new_credit > credit
            logging.info("yurifans finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("yurifans check failed.", "yurifans check failed.")

def get_token(session: requests.Session, account, password):
    resp = session.post("https://yuri.website/wp-json/jwt-auth/v1/token", data = get_token_payload(account, password))
    logging.debug(resp.json())
    credit = resp.json()["credit"]
    logging.info(credit)
    return resp.json()["token"], credit

def get_userinfo(session: requests.Session):
    resp = session.post("https://yuri.website/wp-json/b2/v1/getUserInfo", data = {"ref": "null"})
    credit = resp.json()["user_data"]["credit"]
    logging.info(credit)
    return credit

def finish_user_mission(session: requests.Session):
    resp = session.post("https://yuri.website/wp-json/b2/v1/getTaskData")
    logging.info(resp.text)
    resp_json = resp.json()
    if resp_json["task"]["task_mission"]["finish"] != 1:
        resp = session.post("https://yuri.website/wp-json/b2/v1/userMission")
        logging.info(resp.text)

def main():
    logging.basicConfig(level=logging.INFO)
    yurifans("account", "password")
    pass

if __name__ == "__main__":
    main()
