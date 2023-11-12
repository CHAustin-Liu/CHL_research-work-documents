## DESCRIPTION
This repository contains my bachelor thesis (Examination_of_Calendar_Effect_and_Sentiment_Analysis_on_Bitcoin2.pdf) and the py code and some csv files for my thesis.  Please note 
1.	the tweet.db file is too large (more than 1GB) to be uploaded.  
2.	Not all the csv data files used in my bachelor thesis are uploaded. 
3.	Machine learning is not included in my thesis.  They are undergoing.
4.	The overview of the files uploaded are described as follows.

## main.py
This file is to retrieve tweets information related to Bitcoins then estimate the sentiment score of this tweets.  It includes the following:
(1)	Collect tweet by using the Twitter Public Stream API
(2)	Collect tweets related to Bitcoin by using the Twitter Query API
(3)	Preprocess raw text to clean text using natural language package (nltk) through remove the hyper link and hashtag, split into words, convert to lower case, remove punctuation, filter out stop words.
(4)	Use sentiment score package (vader) to analyze the sentiment score of the clean text
(5)	Use sqlite3 to import the tweets information along with its sentiment score into a tweets.db

## Init_db.py
This file is to create a database (tweets.db) to store tweets information.  The database contains the following columns: “id”, “time”, tweets information (“favorite count”, “quote count”, “retweet count”), sentiment score (“pos”, “neg”, “neu”, “compound”), “text”, and “clean text” 

## db_operation_new.py:
This file is to use sqlite3 to calculate the 10-minute average of information in tweets.db and import them into tweet_output.csv file containing “time”, “counts of tweets”, “favorite average”, “quote average”, “retweet average”, “compound sentiment score”, for further analysis of correlation between Bitcoin price change and twitter information. 

## ML_analysis_Poly.py
This file is to conduct machine learning analysis (polynomial regression model) to study the effect of tweets on the price change of Bitcoins. The twitter information (twt_synchronous.csv file) is preprocessed (splitting data, selected features, check for regression assumptions) followed by polynomial analysis, RMSE calculation, and model drawing.  

## ML_analysis_NN.py
This file is to conduct machine learning analysis (neural network model) to study the effect of tweets on the price change of Bitcoins. The twitter information (twt_synchronous.csv file) is preprocessed (splitting data, selected features) followed by neural network analysis, and RMSE calculation.

## Calendareffect_day.py
This file is to use python libraries (pandas, numpy, scipy) to calculate the daily statistical characteristics (mean, stv, skewness, and kurtosis in calendar_day.csv) of Bitcoin price change and trading volume (in total 2241 data in gemini_BTCUSD_day.csv file) for Calendar effect study.
