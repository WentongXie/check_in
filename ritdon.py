import requests, logging, time, traceback
from Push import PushMessage
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}

def ritdon_login(session, account, password):
    hash_rsp = session.get("https://ritdon.com/")
    hash_bs = BeautifulSoup(hash_rsp.text, "html.parser")
    form_hash = hash_bs.find("input", {"name": "formhash"})
    assert form_hash != None and form_hash.get("value") != None, hash_rsp.text
    formhash = form_hash.get("value")
    url = "https://ritdon.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    payload = "formhash={}&username={}&password={}&quickforward=yes&handlekey=ls".format(formhash, account, password)
    rsp = session.post(url, headers = {"Content-Type":"application/x-www-form-urlencoded"},data = payload)
    logging.debug("login rsp: {}".format(rsp.text))
    assert "window.location.href='https://ritdon.com/" in rsp.text, "login: {}, req header: {}, rsp header: {}".format(rsp.text,  rsp.request.headers, rsp.headers)
    logging.debug("login: {}, req header: {}, rsp header: {}".format(rsp.text,  rsp.request.headers, rsp.headers))
    pass

def ritdon_user_info(session):
    url = "https://ritdon.com/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu"
    rsp = session.get(url)
    body = rsp.text.encode(rsp.encoding).decode(rsp.apparent_encoding)
    assert "金币" in body, "no login: {}".format(body)
    logging.info(body)
    pass

def ritdon_sign(session):
    urls = ["https://ritdon.com/",
        "https://ritdon.com/home.php?mod=spacecp&ac=pm&op=checknewpm&rand="+str(int(time.time())),
        "https://ritdon.com/home.php?mod=misc&ac=sendmail&rand="+str(int(time.time()))
    ]
    for i in urls:
        logging.info(i)
        rsp = session.get(i)
        logging.debug(rsp.text)

def ritdon(account, password):
    try:
        with requests.session() as s:
            s.headers.update(header)
            ritdon_login(s, account, password)
            ritdon_sign(s)
            ritdon_user_info(s)
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("ritdon sign failed.", str(e))
    pass

def main():
    logging.basicConfig(level=logging.INFO)
    #ritdon("account", "password")
    pass

if __name__ == "__main__":
    main()
