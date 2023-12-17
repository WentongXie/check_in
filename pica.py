#https://github.com/czp3009/auto-punch-in-pica
import hashlib
import hmac
import json
import random
import string
import logging
import time
from http import client
import traceback
from Push import PushMessage
import requests

proxies = None
'''
proxies = {
  'http': 'http://127.0.0.1:1080',
  'https': 'http://127.0.0.1:1080',
}
'''
# noinspection SpellCheckingInspection
pica_api_host = "picaapi.picacomic.com"
pica_api_base_url = "https://%s/" % pica_api_host
sign_in_path = "auth/sign-in"
punch_in_path = "users/punch-in"
POST = "POST"

# noinspection SpellCheckingInspection
api_key = "C69BAF41DA5ABD1FFEDC6D2FEA56B"
api_secret = "~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"
# noinspection SpellCheckingInspection
static_headers = {
    "api-key": api_key,
    "accept": "application/vnd.picacomic.com.v1+json",
    "app-channel": "2",
    "app-version": "2.2.1.2.3.3",
    "app-uuid": "defaultUuid",
    "app-platform": "android",
    "app-build-version": "44",
    "User-Agent": "okhttp/3.8.1",
    "image-quality": "original",
}


def send_request(path: string, method: string, body: string = None, token: string = None) -> dict:
    current_time = str(int(time.time()))
    nonce = "".join(random.choices(string.ascii_lowercase + string.digits, k=32))
    raw = path + current_time + nonce + method + api_key
    raw = raw.lower()
    h = hmac.new(api_secret.encode(), digestmod=hashlib.sha256)
    h.update(raw.encode())
    signature = h.hexdigest()
    headers = static_headers.copy()
    headers["time"] = current_time
    headers["nonce"] = nonce
    headers["signature"] = signature
    if body is not None:
        headers["Content-Type"] = "application/json; charset=UTF-8"
    if token is not None:
        headers["authorization"] = token
    rsp = requests.request(method, url="https://{}/{}".format(pica_api_host, path), data=body, headers=headers, proxies=proxies)
    logging.debug(rsp.text)
    json_object = rsp.json()
    if json_object["code"] != 200:
        raise RuntimeError(json_object["message"])
    return json_object


def sign_in(email: string, password: string) -> string:
    body = {
        "email": email,
        "password": password
    }
    return send_request(sign_in_path, POST, json.dumps(body))["data"]["token"]


def punch_in(token: string):
    return send_request(punch_in_path, POST, token=token)

def pica_sign(account, password):
    try:
        current_token = sign_in(account, password)
        punch_in_response = punch_in(current_token)
        result = punch_in_response["data"]["res"]
        if result["status"] == "ok":
            logging.info("Punch-in succeed, last punch-in day: %s" % result["punchInLastDay"])
        else:
            logging.info("Already punch-in")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("pica check failed.", "pica check failed.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    pica_sign("account", "password")
