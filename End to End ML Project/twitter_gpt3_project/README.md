# Twitter Scrapper and GPT-3 Tweet Generator

### Objective: 
- To utilize OpenAI GPT-3 to generate tweet that similar to others tweets

### Description:
This project uses Python Tweepy package to access Twitter API. A dummy twitter account was created to collect tweets.


### Output:
- The get-tweets.py will fetch each twitter users' latest 50 tweets in /tweets/<username>.txt. (in this case @jeffreykktu and @lexfridman)
- The gpt3_openai.py is used to create tweet:
  - The tweet is set to start with the phrase: "I wish";
  - The prompt is "Generate tweets similar to the followings: <paste lines of extracted tweets from the .txt files>
  - It will print out a new tweet.

  
### Notes:
- Replace CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, and BEARER_TOKEN with your own.
- Packages required are listed in requirements.txt
- You can also use OpenAI gpt3 playground to do the same process by gpt3_openai.py


