import logging, time, random
from Sonkwo import SonkwoCheck
from Yamibo import YamiboCheck
from Gamer import GamerCheck
from ritdon import ritdon
from Push import PushMessageSetConfig
from masiro import MasiroCheck
from pica import pica_sign
from tsdm import tsdm_sign
from right import right_sign
from yurifans import yurifans

def main():
    time.sleep(random.randint(0, 120))
    PushMessageSetConfig("app_token", ["uid"])
    name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename = "/log/" + name + ".txt",level = logging.INFO, format = LOG_FORMAT)
    SonkwoCheck("account", "password")
    YamiboCheck("account", "password")
    GamerCheck("account", "password")
    ritdon("account", "password")
    MasiroCheck("cookie")
    pica_sign("account", "password")
    tsdm_sign("cookie")
    right_sign("cookie")
    yurifans("account", "password")
    pass


if __name__ == "__main__":
    main()
