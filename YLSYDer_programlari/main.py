import utils

utils.import_or_install('tweepy')
utils.import_or_install('openpyxl')
utils.import_or_install('ray')

from Tweet import Tweet_Poster
from Email import Emailer
import ray
import os
from pathlib import Path

# How to get gmail app password:
# https://myaccount.google.com/apppasswords

Program_control_path = 'ProgramControl.xlsx'
Tweets_tags_path = 'TweetlerveHesaplar.xlsx'
MV_listesi_path = 'MV_Listesi.xlsx'
Bakan_listesi_path = 'Bakan_Listesi.xlsx'
Mail_icerigi_path = "mail.txt"
list_of_media = ["sabitkurgrafigi.png", "TBB_image1.jpeg","TBB_image2.jpeg","TBB_image3.jpeg",
                "TBB_image4.jpeg", "TBB_image5.jpeg"]
list_of_media = [Path(os.getcwd()) / 'grafikler' / i for i in list_of_media]

ray.init()
@ray.remote
def Bakan_Email():
    try:
        Emailer(Program_control_path, Mail_icerigi_path, Bakan_listesi_path, 'Bakanım')
    except:
        print('Something is wrong with Bakan Emailer. Consider rerunning')

@ray.remote
def Vekil_Email():
    try:
        Emailer(Program_control_path, Mail_icerigi_path, MV_listesi_path, 'Vekilim')
    except:
        print('Something is wrong with Vekil Emailer. Consider rerunning')

@ray.remote
def Twitter():
    try:
        Tweet_Poster(Program_control_path, Tweets_tags_path, list_of_media)
    except:
        print('Something is wrong with Twitter. Consider rerunning')

ray.get([Twitter.remote(), Bakan_Email.remote(), Vekil_Email.remote()])