import os
import time
import tweepy
import numpy as np
import smtplib


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


def Post_Tweet(Tweets, Tags, tweet, media, api):
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
                api.update_status(updated_tweet, media_ids=[media.media_id])
            else:
                api.update_status(updated_tweet)
            print('\nSuccesfully tweeted:\n%s'%(updated_tweet))
        except tweepy.Forbidden as warning:
            print('\nTweet is not successful. Reason: ')
            print(warning)
    else:
        pass


def Media_Uploader(list_of_media, api):
    media = None
    media_file = np.random.choice(list_of_media)
    if check_if_file_exists(media_file):
        media = api.media_upload(media_file)
    return media, api


def Tweet_Manager(api, list_of_media, Tweets, Tags, Frequencies):
    media, api = Media_Uploader(list_of_media, api)
    tweet = np.random.choice(range(len(Tweets)))
    if tweet in Frequencies:
        np.random.shuffle(Tags)
        Post_Tweet(Tweets, Tags, tweet, media, api)
        time.sleep(np.random.randint(750, 900))


def Emailer_manager(program_control, letter, alici_list, hitap):
    my_email = program_control.email[0]
    my_password = program_control.password[0]

    subject = f"1416 YLSY Bursiyerleri için Sabit Kur Talep Ediyoruz!"

    while True:
        counter = 0
        for index, row in alici_list.iterrows():
            counter += 1
            if str(row['Isim2']) == 'nan':
                person_name = f"{row['Isim']} {row['Soyisim']}"
            else:
                person_name = f"{row['Isim']} {row['Isim2']} {row['Soyisim']}"

            new_letter = letter.replace("[NAME]", person_name)
            mes = f"Subject:{subject}\n\n{new_letter}"
            recipient = row['Eposta']
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # Starting a connection
                connection.starttls()  # This is to encrypt email
                connection.login(user=my_email, password=my_password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=recipient,
                    msg=mes.encode('utf-8'))
            print(f"Email was sent to {hitap} {person_name} - {recipient}")
            if counter % 50 == 0:
                time.sleep(300)
        time.sleep(3600*10)


def Letter_preprocessor(Mail_icerigi, hitap):
    letter = Mail_icerigi
    return letter.replace("[Vekilim]", hitap)