from Push import PushMessage
import urllib.request, urllib.parse, re, requests, logging, traceback, hashlib
from bs4 import BeautifulSoup

def YamiboGetLoginUrl(login_hash):
    return r"https://bbs.yamibo.com/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=" + login_hash + r"&inajax=1"

def YamiboGetLoginData(account, password, form_hash):
    post_data = {
        "formhash": form_hash,
        "referer": r"https://bbs.yamibo.com/home.php?mod=spacecp&ac=credit&op=base",
        "loginfield": "username",
        "username": account,
        "password": hashlib.md5(password.encode('utf-8')).hexdigest(),
        "questionid": "0",
        "answer": ""
    }
    return post_data

def YamiboGetCheckUrl(check_hash):
    return r"https://bbs.yamibo.com/plugin.php?id=study_daily_attendance:daily_attendance&fhash=" + check_hash

def YamiboCheck(account, password):
    login_info_url = r"https://bbs.yamibo.com/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login"
    home_url = r"https://bbs.yamibo.com/home.php?mod=spacecp&ac=credit&op=base"
    header = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": r"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Accept-Encoding": "gzip",
        "Origin": r"https://bbs.yamibo.com",
        "Referer": r"https://bbs.yamibo.com/home.php?mod=spacecp&ac=credit&op=base"
    }
    try:
        with requests.Session() as s:
            login_info_rsp = s.get(login_info_url, headers = header)
            s.cookies.update({r"EeqY_2132_nofavfid": "1", r"EeqY_2132_sendmail": "1"})
            login_hash = re.search(r'''loginhash=(.*?)"''', login_info_rsp.text)
            assert login_hash != None, login_info_rsp.text
            login_hash = login_hash.group(1)
            form_hash  = re.search(r'''name="formhash" value="(.*?)"''', login_info_rsp.text)
            assert form_hash != None, login_info_rsp.text
            form_hash = form_hash.group(1)
            logging.info("login_hash: {}, form_hash:{}".format(login_hash, form_hash))
            home_rsp = s.post(YamiboGetLoginUrl(login_hash), headers = header, data = YamiboGetLoginData(account, password, form_hash))
            home_rsp = s.get(home_url, headers = header)
            assert -1 == home_rsp.text.find("您需要先登录才能继续本操作"),home_rsp.text
            body = BeautifulSoup(home_rsp.text, 'html.parser')
            li_list = body.find_all("li", class_ = "xi1 cl")
            for i in li_list:
                logging.info(i.get_text())
            check_hash = re.search(r'''fhash=(.*?)"''', home_rsp.text)
            assert None != check_hash, home_rsp.text
            check_hash = check_hash.group(1)
            logging.info("check_hash:{}".format(check_hash))
            check_rsp = s.get(YamiboGetCheckUrl(check_hash), headers = header)
            home_rsp = s.get(home_url, headers = header)
            assert -1 == home_rsp.text.find("您需要先登录才能继续本操作"),home_rsp.text
            body = BeautifulSoup(home_rsp.text, 'html.parser')
            li_list = body.find_all("li", class_ = "xi1 cl")
            for i in li_list:
                logging.info(i.get_text())
            logging.info("YamiboCheck finish.")
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("yamibo check failed.", "yamibo check failed.")



def main():
    #logging.basicConfig(level=logging.INFO)
    pass

if __name__ == "__main__":
    main()

    
