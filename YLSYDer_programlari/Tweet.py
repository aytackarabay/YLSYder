import tweepy
import numpy as np
import pandas as pd
import utils
import requests

def Tweet_Poster(Program_control_path, Tweets_tags_path, list_of_media):
    utils.terminate_if_missing_file(Program_control_path)
            
    program_control = pd.read_excel(Program_control_path)
    tweets_tags = pd.read_excel(Tweets_tags_path)

    if program_control['v2'][0]:
        api = tweepy.Client(
                        consumer_key=program_control['api_key'][0], 
                        consumer_secret=program_control['api_key_secret'][0], 
                        access_token=program_control['access_token'][0], 
                        access_token_secret=program_control['access_token_secret'][0], 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)
    else:
        auth = tweepy.OAuthHandler(program_control['api_key'][0], program_control['api_key_secret'][0])
        auth.set_access_token(program_control['access_token'][0], program_control['access_token_secret'][0])
        api = tweepy.API(auth, wait_on_rate_limit=True)

    Tweets = list(tweets_tags[tweets_tags['Tweet Icerik'].notnull()]['Tweet Icerik'])
    Iktidar_tags = list(tweets_tags[tweets_tags['Iktidar Tagleri'].notnull()]['Iktidar Tagleri'])
    Focus_tags = list(tweets_tags[tweets_tags['Focus Taglar'].notnull()]['Focus Taglar'])
    Muhalefet_tags = list(tweets_tags[tweets_tags['Muhalefet Tagleri'].notnull()]['Muhalefet Tagleri'])
    Gazeteci_tags = list(tweets_tags[tweets_tags['Gazeteci Taglari'].notnull()]['Gazeteci Taglari'])
    Diger_tags = list(tweets_tags[tweets_tags['Diger Taglar'].notnull()]['Diger Taglar'])

    muhalefet_freq_threshold  = 0.1
    Muhalefet_frequencies = list(np.random.randint(0,len(Tweets),
                                int(len(Tweets)*muhalefet_freq_threshold)))

    gazeteci_freq_threshold  = 0.05
    Gazeteci_frequencies = list(np.random.randint(0,len(Tweets),
                                int(len(Tweets)*gazeteci_freq_threshold)))

    diger_freq_threshold  = 0.02
    Diger_frequencies = list(np.random.randint(0,len(Tweets),
                                int(len(Tweets)*diger_freq_threshold)))

    np.random.shuffle(Tweets) #Shuffle tweets

    while True:
        ###Tweet for focus tags###
        utils.Tweet_Manager(api, program_control, list_of_media, Tweets, Focus_tags, range(len(Tweets)))
        
        ###Tweet for iktidar tags###
        utils.Tweet_Manager(api, program_control, list_of_media, Tweets, Iktidar_tags, range(len(Tweets)))
        
        ###Tweet for muhalefet tags###
        utils.Tweet_Manager(api, program_control, list_of_media, Tweets, Muhalefet_tags, Muhalefet_frequencies)

        ###Tweet for gazeteci tags###
        utils.Tweet_Manager(api, program_control, list_of_media, Tweets, Gazeteci_tags, Gazeteci_frequencies)

        ###Tweet for diger tags###
        utils.Tweet_Manager(api, program_control, list_of_media, Tweets, Diger_tags, Diger_frequencies)