import os
import time
import tweepy
import numpy as np
import smtplib
import logging
import sys
from email.mime.text import MIMEText
from email.message import EmailMessage

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def import_or_install(package):
    try:
        __import__package
    except:
        os.system("pip install "+ package)


def terminate_if_missing_file(filename):
    '''This function checks if a file is in the working directory and raises exception if needed.'''
    if os.path.exists(filename) == True:
        pass
    else:
        raise FileNotFoundError("The file {} is not in the folder.".format(filename))


def check_if_file_exists(filename):
    '''This function checks if a file is in the working directory.'''
    return(os.path.exists(filename))


def Post_Tweet(Tweets, program_control, Tags, tweet, media, api):
    if '\n' in Tweets[tweet]:
        updated_tweet = Tweets[tweet].replace("\n", " ")
    else:
        updated_tweet = Tweets[tweet]
    if len(updated_tweet) < 280:
        for tag in Tags[np.random.randint(0,int(len(Tags)*0.7)):]:
            if len(updated_tweet + ' ' + tag) < 280:
                updated_tweet += ' ' + tag
        try:
            if media != None:
                if program_control['v2'][0]:
                    api.create_tweet(text = updated_tweet)
                else:
                    api.update_status(updated_tweet, media_ids=[media.media_id])
            else:
                if program_control['v2'][0]:
                    api.create_tweet(text = updated_tweet)
                else:
                    api.update_status(updated_tweet)
            logging.info(f'Succesfully tweeted: {updated_tweet}')
        except tweepy.Forbidden as warning:
            logging.info('Tweet is not successful. Reason: ')
            logging.info(warning)
    else:
        pass


def Media_Uploader(list_of_media, api):
    media = None
    media_file = np.random.choice(list_of_media)
    if check_if_file_exists(media_file):
        media = api.media_upload(media_file)
    return media, api


def Tweet_Manager(api, program_control, list_of_media, Tweets, Tags, Frequencies):
    media, api = Media_Uploader(list_of_media, api)
    tweet = np.random.choice(range(len(Tweets)))
    if tweet in Frequencies:
        np.random.shuffle(Tags)
        Post_Tweet(Tweets, program_control, Tags, tweet, media, api)
        time.sleep(1801)


def Emailer_manager(program_control, letter, alici_list, email_basliklari, hitap, Kanunonerisi, Rapor):
    my_email = program_control.email[0]
    my_password = program_control.password[0]

    while True:
        subject = np.random.choice(list(email_basliklari.Konu))
        counter = 0
        alici_list = alici_list.sample(frac=1).reset_index(drop=True)
        for index, row in alici_list.iterrows():
            try:
                counter += 1
                if str(row['Isim2']) == 'nan':
                    person_name = f"{row['Isim']} {row['Soyisim']}"
                else:
                    person_name = f"{row['Isim']} {row['Isim2']} {row['Soyisim']}"

                new_letter = letter.replace("[NAME]", person_name)
                # mes = f"Subject:{subject}\n\n{new_letter}".encode('utf-8')
                recipient = row['Eposta']

                msg = EmailMessage()
                msg['From'] = my_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.set_content(new_letter)

                with open(Kanunonerisi, 'rb') as content_file:
                    content = content_file.read()
                    msg.add_attachment(content, maintype='application/pdf', subtype='pdf', filename=Kanunonerisi)

                with open(Rapor, 'rb') as content_file:
                    content = content_file.read()
                    msg.add_attachment(content, maintype='application/pdf', subtype='pdf', filename=Rapor)

                mes_w_attachment = msg.as_string().encode('utf-8')


                with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # Starting a connection
                    connection.starttls()  # This is to encrypt email
                    connection.login(user=my_email, password=my_password)
                    connection.sendmail(
                        from_addr=my_email,
                        to_addrs=recipient,
                        msg=mes_w_attachment)
                logging.info(f"Email was sent to {hitap} {person_name} - {recipient}.")
                if counter % 50 == 0:
                    time.sleep(300)
            except:
                logging.info(f'Email could not be sent to {hitap} {person_name} - {recipient}.')
                pass
        time.sleep(3600*24)


def Letter_preprocessor(Mail_icerigi, hitap):
    letter = Mail_icerigi
    return letter.replace("[Vekilim]", hitap)