'''
This file is to retrieve tweets information related to Bitcoins then estimate the sentiment score of this tweets.  It includes the following:
(1)	Collect tweet by using the Twitter Public Stream API
(2)	Collect tweets related to Bitcoin by using the Twitter Query API
(3)	Preprocess raw text to clean text using natural language package (nltk) through remove the hyper link and hashtag, split into words, convert to lower case, remove punctuation, filter out stop words.
(4	Use sentiment score package (vader) to analyze the sentiment score of the clean text
(5)	Use sqlite3 to import the tweets information along with its sentiment score into a tweets.db
'''

import os
import re
import time
import json
import string
import tweepy
import logging
import sqlite3
from pprint import pprint
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Logging Setting, For Debugging
logging.basicConfig(level=logging.INFO, format='%(levelname)5s:%(message)s', filename='debug_log.txt')

# Twitter Authentication Setting
auth = tweepy.OAuthHandler(os.environ['TWITTER_APP_KEY'], os.environ['TWITTER_APP_SECRET'])
auth.set_access_token(os.environ['TWITTER_OAUTH_TOKEN'], os.environ['TWITTER_OAUTH_TOKEN_SECRET'])

# Global Variables
counter = 0             # For Debugging, no other usages
api = tweepy.API(auth)
columns = ["id", "created_at", "favorite_count", "quote_count", "retweet_count",
           "pos", "neg", "neu", "compound","text", "clean_text"]
db_name, table_name = 'tweets.db', 'Tweets'

def insert(info):
    '''
        Insert a rew tweet to database.
        If the tweet has been existed in the database, then raise exception
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        statement = "INSERT INTO Tweets VALUES ({}?);".format( '?,' * (len(columns) - 1) )
        cursor.execute( statement, [ info[col] for col in columns ] )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise sqlite3.IntegrityError

    conn.close()

    return

def update(info):
    '''
        If this tweet has existed in database,
        Then update the favorite_count, quote_count, retweet_count
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    statement = '''
    UPDATE Tweets
    SET favorite_count={}, quote_count={}, retweet_count={}
    WHERE id={};
    '''
    cursor.execute(statement.format(info['favorite_count'], info['quote_count'], info['retweet_count'], info['id']))

    conn.commit()
    conn.close()

    return

def save_tweet_db(info):
    '''
        Save tweet to sqlite database
    '''
    try:
        insert(info)
    except sqlite3.IntegrityError:
        # This tweet has been existed 
        update(info)

    return

def save_tweet_csv(info):
    '''
        Save tweet to CSV file
    '''
    dirname  = os.path.join( os.environ['TWITTER'], 'Tweets' )
    fname    = 'tweets.{}.csv'.format( datetime.today().strftime("%Y%m%d") )
    fullname = os.path.join( dirname, fname )

    if not os.path.exists(fullname):
        # Initialize the file if it's not exist
        fp = open(fullname, 'w', encoding='utf-8')  # Write Mode
        fp.write('{}\n'.format(','.join(columns)))
        fp.close()
    else:
        fp = open(fullname, 'a', encoding='utf-8')  # Append Mode
        fp.write('{},{},{},{},{},{},{},{}\n'.format(*[ info.get(col) for col in columns ]))
        fp.close()

    return

def text_preprocess(text):
    '''
        Convert the raw text to clean text
    '''
    # Remove the hyper link and hashtag
    patterns = [re.compile(r'https://(\w+\.*)+/\w+'), re.compile(r'[#|@]\w+')]

    for pattern in patterns:
        text = re.sub(pattern, '', text)

    # Split into words
    words = word_tokenize(text)  
    
    # Convert to lower case
    words = [word.lower() for word in words] 

    # Remove punctuation from each wordord
    table  = str.maketrans('', '', string.punctuation)
    words = [word.translate(table) for word in words]

    # Filter out stop words
    stop_words = stopwords.words('english')
    words = [word for word in words if word not in stop_words]

    clean_text = ' '.join(words)
#    logging.info('Text: {}'.format(clean_text))

    return clean_text

def sentiment_analyze(text):
    analyzer = SentimentIntensityAnalyzer()
    result = analyzer.polarity_scores(text)
    
    return result

def handle_quote(status, category):
    '''
        This will deal with the quote in the tweet
    '''
    info = {}
    if category == 'stream':
        if hasattr(status, "quoted_status"):  # Check if has a quote
            try:
                info['text'] = status.quoted_status.extended_tweet["full_text"]
            except AttributeError:
                info['text'] = status.quoted_status.text

            info['id']             = status.quoted_status.id
            info['created_at']     = status.quoted_status.created_at
            info['favorite_count'] = status.quoted_status.favorite_count
            info['quote_count']    = status.quoted_status.quote_count
            info['retweet_count']  = status.quoted_status.retweet_count
    else: # Category is query
        status = status.get('quoted_status')
        if status:
            info['text']           = status.get('full_text', '')
            info['id']             = status.get('id', -1)
            info['created_at']     = status.get('created_at', '')
            info['favorite_count'] = status.get('favorite_count', -1)
            info['quote_count']    = status.get('quote_count', -1)
            info['retweet_count']  = status.get('retweet_count', -1)
            # Change time format
            info['created_at'] = datetime.strptime(info['created_at'].replace(' +0000 ', ' '), '%c').strftime('%Y-%m-%d %H:%M:%S')

    if info:
        # Append the sentiment to info
        clean_text       = text_preprocess(info['text'])
        sentiment_score  = sentiment_analyze(clean_text)
        info.update(sentiment_score)
        info['clean_text'] = clean_text

        return info
    return

def process_tweet(status, category):
    info = {}
    quote_info = None

    if category == 'stream':
        if hasattr(status, "retweeted_status"):  # Check if is Retweet
            # Handling the retweet
            try:
                info['text'] = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                info['text'] = status.retweeted_status.text

            info['id']             = status.retweeted_status.id
            info['created_at']     = status.retweeted_status.created_at
            info['favorite_count'] = status.retweeted_status.favorite_count
            info['quote_count']    = status.retweeted_status.quote_count
            info['retweet_count']  = status.retweeted_status.retweet_count

            if status.retweeted_status.is_quote_status: # Check if it has a quote
                quote_info = handle_quote(status.retweeted_status, category)
        else:
            # Handling the normal tweet
            try:
                info['text'] = status.extended_tweet["full_text"]
            except AttributeError:
                info['text'] = status.text
            info['id'] = status.id
            info['created_at']     = status.created_at
            info['favorite_count'] = status.favorite_count
            info['quote_count']    = status.quote_count
            info['retweet_count']  = status.retweet_count

            if status.is_quote_status: # Check if it has a quote
                quote_info = handle_quote(status, category)
                logging.info( "{} quote {}".format(info['id'], quote_info['id']) )
    else: # Category is query
        if status.get("retweeted_status"):  # Check if is Retweet
            # Handling the retweet
            status = status.get("retweeted_status")
            info['text']           = status.get('full_text', '')
            info['id']             = status.get('id', -1)
            info['created_at']     = status.get('created_at', '')
            info['favorite_count'] = status.get('favorite_count', -1)
            info['quote_count']    = status.get('quote_count', -1)
            info['retweet_count']  = status.get('retweet_count', -1)

            if status.get('is_quote_status'): # Check if it has a quote
                quote_info = handle_quote(status, category)
        else:
            # Handling the normal tweet

            info['text']           = status.get('full_text', '')
            info['id']             = status.get('id', -1)
            info['created_at']     = status.get('created_at', '')
            info['favorite_count'] = status.get('favorite_count', -1)
            info['quote_count']    = status.get('quote_count', -1)
            info['retweet_count']  = status.get('retweet_count', -1)

            if status.get('is_quote_status'): # Check if it has a quote
                quote_info = handle_quote(status, category)

        # Change time format
        info['created_at'] = datetime.strptime(info['created_at'].replace(' +0000 ', ' '), '%c').strftime('%Y-%m-%d %H:%M:%S')

    # Append the sentiment to info
    clean_text = text_preprocess(info['text'])
    sentiment_score  = sentiment_analyze(clean_text)
    info.update(sentiment_score)
    info['clean_text'] = clean_text

    # Save tweets
    save_tweet_db(info)
    if quote_info is not None:
        save_tweet_db(quote_info)
        logging.info( "{} quote {}".format(info['id'], quote_info['id']) )

    return

class MyStreamListener(tweepy.StreamListener):
    '''
        Public Stream API,
        Use self-defined method to handle the status(a tweet) by overriding StreamListener 
    '''
    def on_status(self, status):
        process_tweet(status, 'stream')
        return
    
def collect_from_stream():
    '''
        Collect tweet by using the Twitter Public Stream API
    '''
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended', lang='en')

    myStream.filter(track=['bitcoin', 'Bitcoin', 'bitcoins', 'Bitcoins'], languages=['en'])

    return

def collect_from_query():
    '''
        Collect tweet by using the Twitter Query API
        until='YYYY-MM-DD', collect the tweepy published before the until
    '''
    max_limit = 1000
    query     = ['bitcoin', 'Bitcoin', 'bitcoins', 'Bitcoins']
    counter = 0

    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', lang='en').items(max_limit):
        counter += 1; print(counter)
        process_tweet(tweet._json, 'query')

    return

if __name__ == '__main__':
    while True:
        try:
            collect_from_stream()
#        collect_from_query()
        except KeyboardInterrupt:
            print('Shutdown Program')
            exit()
        except:
            logging.error('Something happend')
            continue
