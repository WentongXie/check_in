import logging, time, random
from Acfun import AcfunCheck
from Sonkwo import SonkwoCheck
from Yamibo import YamiboCheck
from Gamer import GamerCheck
from ritdon import ritdon
from Push import PushMessageSetConfig

def main():
    time.sleep(random.randint(0, 60))
    PushMessageSetConfig("app_token", ["uid"])
    name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename = "/var/www/html/check/" + name + ".txt",level = logging.INFO, format = LOG_FORMAT)
    SonkwoCheck("account", "password")
    YamiboCheck("account", "password")
    GamerCheck("account", "password")
    ritdon("account", "password")
    pass


if __name__ == "__main__":
    main()
