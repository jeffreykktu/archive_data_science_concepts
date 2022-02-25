import os
import re
import json
from dotenv import load_dotenv
import tweepy


def write_to_file(path, content):
    with open(path, "w+") as f:
        for line in content:
            f.write(line)
            f.write("\n")
def prepend_to_file(path, content):
    with open(path, "r+") as f:
        original = f.read()
        f.seek(0)
        for line in content:
            f.write(line)
            f.write("\n")
        f.write(original)

def get_json(path):
    with open(path, "r") as f:
        return json.load(f)

def write_to_json(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, sort_keys=True, indent=4)

def format_text(tweet_text):
    tweet_text = re.sub("@[\w]*", "", tweet_text, flags=re.MULTILINE).replace("\n", "") #remove tagging other users
    tweet_text = re.sub(r'http\S+', '', tweet_text)
    tweet_text = re.sub(r'https\S+', '', tweet_text)
    return tweet_text


if __name__ == "__main__":
    
    load_dotenv()
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")

    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    screen_names = ["jeffreykktu", "lexfridman"]
    tweet_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tweets')
    

    if not os.path.exists(tweet_directory):
        os.mkdir(tweet_directory)
    
    for screen_name in screen_names:
        
        # twitter user id finder : https://tools.codeofaninja.com/find-twitter-id
        # e.g. user_id = 427089628 #@lexfridman
        print('-------------------------------------------------------')
        print('----------- Processing :: [' + screen_name + '] ------')
        print('-------------------------------------------------------')
        
        # retrieve the latest tweet id
        last_updated_id_path = tweet_directory + "/" + screen_name + '.json'
        last_updated_id = {}
        since_id = None
        
        if (os.path.exists(last_updated_id_path)):
            last_updated_id = get_json(last_updated_id_path)
            since_id = last_updated_id.get("last_tweet_id")

        tweet_text_data = []
        user_id = client.get_user(username=screen_name).data.id
        
        if since_id:
            tweets = client.get_users_tweets(id=user_id, max_results=50, since_id=since_id)
        else:
            tweets = client.get_users_tweets(id=user_id, max_results=50)
        
        if tweets.data is None:
            continue

        latest_tweet_id = tweets.data[0].id
        latest_tweet_text = format_text(tweets.data[0].text)
        last_updated_id["last_tweet_id"] = latest_tweet_id
        last_updated_id["last_tweet_text"] = latest_tweet_text

        for tweet in tweets.data:
            tweet_text = tweet.text
            tweet_id = tweet.id
            formatted_tweet = format_text(tweet_text)
            tweet_text_data.append(formatted_tweet)
        
        # store the latest tweet texts to .txt, the latest at the top 
        tweet_data_path = os.path.join(tweet_directory, screen_name + ".txt")

        if not os.path.exists(tweet_data_path):            
            write_to_file(tweet_data_path, tweet_text_data)
        else:
            prepend_to_file(tweet_data_path, tweet_text_data)

        # update the .json with latest tweet_id, we don't care if tweets were removed, we just want the latest tweets
        with open(last_updated_id_path, "w+") as f:
            json.dump(last_updated_id, f, sort_keys=True, indent=4)




        

    
    