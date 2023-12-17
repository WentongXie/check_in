import requests, json, logging, traceback

appToken = ""
uids = []

def PushMessageSetConfig(app_token, uid):
    global appToken, uids
    appToken = app_token
    uids = uid

def PushMessage(summary, content):
    if len(appToken) == 0:
        return
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": appToken,
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": uids
    }
    payload = json.dumps(payload)
    logging.info("summary: %s, content: %s.", summary, content)
    header = {"content-type": "application/json"}
    try:
        r = requests.post(url, data = payload, headers = header)
        logging.info(r.text)
    except Exception as e:
        logging.error("Exception: %s", traceback.format_exc())
    pass

def main():
    #logging.basicConfig(level=logging.INFO)
    #PushMessage("test summary", "test content")
    pass

if __name__ == "__main__":
    main()
