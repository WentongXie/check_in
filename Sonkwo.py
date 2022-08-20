from Push import PushMessage
import urllib.request, re, json, urllib.parse, time, logging, traceback, requests, uuid

def SonkwoCheck(account, password):
    token_url = r"https://auth.sonkwo.cn/api/access_token.json?locale=js"
    check_url = r"https://auth.sonkwo.cn/api/me/clock_in.json?locale=js"#r"https://www.sonkwo.com/api/clock_in.json?locale=js" 20190417 check_in.json -> clock_in.json
    me_url = r"https://auth.sonkwo.cn/api/me.json?locale=js&sonkwo_version=1&sonkwo_client=web&q%5Bintroduction%5D=true&q%5Bbirthday%5D=true&q%5Bshow_steam_review%5D=true&q%5Blast_sign_in_at_timestamp%5D=true&q%5Blast_sign_in_ip%5D=true&q%5Bset_password%5D=true&q%5Bgender%5D=true&q%5Bemail_asterisks%5D=true&q%5Bphone_number_asterisks%5D=true&q%5Bcredential_num_asterisks%5D=true&q%5Bunmute_at_timestamp%5D=true&q%5Bsign_in_count%5D=true&q%5Bpoint%5D%5Bxp%5D=true&q%5Bpoint%5D%5Bscore%5D=true&q%5Bpoint%5D%5Btasks%5D=true&q%5Bpoint%5D%5Bhistory_score%5D=true&q%5Bplatforms%5D%5Bshow_id%5D=true&q%5Bplatforms%5D%5Bkind%5D=true&q%5Bwallet%5D%5Bbalance%5D=true&q%5Bwallet%5D%5Bstatus%5D=true&q%5Bregion%5D=true&q%5Bconfigs%5B%5D%5Bid%5D%5D=true&q%5Bconfigs%5B%5D%5Bkind%5D%5D=true&q%5Bconfigs%5B%5D%5Bkey%5D%5D=true&q%5Bconfigs%5B%5D%5Bvalue%5D%5D=true&q%5Bsafrv%5D=true&_=" + str(int(time.time()))
    
    me_headers = {
        "Accept": r"application/vnd.sonkwo.v1+json",
        #"Authorization": "Bearer " + token["access_token"],
        "Origin": r"https://www.sonkwo.com",
        "Referer": r"https://www.sonkwo.com/",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    token_header = {
        "Accept": "application/vnd.sonkwo.v1+json",
        "Origin": "https://www.sonkwo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://www.sonkwo.com/sign_in?return_addr=%2F",
        "Accept-Encoding": "gzip",
    }
    check_headers = {
        "Accept": r"application/vnd.sonkwo.v1+json",
        #"Authorization": "Bearer " + token["access_token"],
        "Content-Type": r"application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": r"https://www.sonkwo.com",
        "Referer": r"https://www.sonkwo.com/",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    logout_headers = {
        "Accept": "application/vnd.sonkwo.v1+json",
        "Accept-Encoding": "gzip",
        #"Authorization": "Bearer " + token["access_token"],
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.sonkwo.com",
        "Referer": "https://www.sonkwo.com/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    try:
        check_data = {"sonkwo_version": "1", "sonkwo_client": "web"}
        check_data = urllib.parse.urlencode(check_data)
        token_data = "sonkwo_version=1&sonkwo_client=web&account[remember_me]=true&account[email_or_phone_number_eq]={}&account[password]={}&a[uuid]={}&a[client]=mall_native_pc".format(account, password, str(uuid.uuid4()))
        
        token_rsp = requests.post(token_url, data = token_data.encode(), headers = token_header)
        token = token_rsp.json()
        logging.debug(token)
        async_url = '''https://www.sonkwo.cn/fa/async_tokens?nickname={}&avatar={}&account_region=cn&access_token={}&access_token_expires_in={}&refresh_token={}&token_type=bearer&id={}&sync_language={{"value":"chinese","id":""}}'''.format(token["nickname"], token["avatar"], token["access_token"], (int(token["created_at"]) + int(token["expires_in"])) * 1000, token["refresh_token"], token["id"])
        logging.debug(async_url)
        async_rsp = requests.get(token_url, data = token_data.encode(), headers = token_header)
        logging.debug(async_rsp.text)
        
        me_headers["Authorization"] = "Bearer " + token["access_token"]
        me_request = urllib.request.Request(me_url, headers = me_headers)
        logging.info(urllib.request.urlopen(me_request).read())

        check_headers["Authorization"] = "Bearer " + token["access_token"]
        check_request = urllib.request.Request(check_url,data = check_data.encode(), headers = check_headers)
        logging.info(urllib.request.urlopen(check_request).read())

        logout_headers["Authorization"] = "Bearer " + token["access_token"]
        logout_request = urllib.request.Request(token_url,data = check_data.encode(), headers = logout_headers)
        logout_request.get_method = lambda: 'DELETE'
        urllib.request.urlopen(logout_request)
        logging.info("SonkwoCheck finish.")
        
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
        PushMessage("sonkwo check failed.", "sonkwo check failed.")

def main():
    logging.basicConfig(level=logging.INFO)
    #SonkwoCheck("account", "password")
    print("import sonkwo")

if __name__ == "__main__":
    main()
