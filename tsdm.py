from Push import PushMessage
import requests
import logging
import traceback
from bs4 import BeautifulSoup


def tsdm_sign(cookie):
    try:
        header = {
            "Cookie": cookie,
            "User-Agent": r"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        }
        url = "https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign"
        hash_rsp = requests.get(url, headers=header)
        hash_bs = BeautifulSoup(hash_rsp.text, "html.parser")
        form_hash = hash_bs.find("input", {"name": "formhash"})
        assert form_hash != None and form_hash.get(
            "value") != None, hash_rsp.text
        formhash = form_hash.get("value")
        logging.info(formhash)
        info = hash_bs.find("div", class_="bm_c add")
        logging.info(info.get_text())
        sign_url = "https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0&mobile=yes"
        header["Content-Type"] = "application/x-www-form-urlencoded"
        sign_data = {
            "formhash": formhash,
            "qdxq": "shuai",
            "qdmode": 3,
            "todaysay": "",
            "fastreply": 1
        }
        sign_rsp = requests.post(sign_url, headers=header, data=sign_data)
        sign_bs = BeautifulSoup(sign_rsp.text, "html.parser")
        result = sign_bs.find(id = "messagetext")
        assert result != None and result.get_text().find("恭喜你签到成功") != -1, sign_rsp.text
        logging.info(result.get_text())
        logging.info("tsdm finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("tsdm check failed.", "tsdm check failed.")


def main():
    cookie = ""
    logging.basicConfig(level=logging.INFO)
    tsdm_sign(cookie)
    pass


if __name__ == "__main__":
    main()
