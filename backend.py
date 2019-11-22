from flask import Flask, request, json
from flask import render_template
from flask_cors import CORS, cross_origin
import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer	
from textblob import TextBlob
import re

app = Flask(__name__)
cors = CORS(app)

@app.route('/Analysis', methods=['POST'])
def Analysis():
	import tweepy
	from textblob import TextBlob
	query = request.form['Query'];
	consumer_key = 'XXX'
	consumer_secret = 'XXX'
	access_token = 'XXX-XXX'
	access_token_secret = 'XXX'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_token_secret) 
	api = tweepy.API(auth)

	searchTerm = query
	noOfSearchItem = 100

	tweets = api.search(q=searchTerm, count = noOfSearchItem)

	polarity = 0
	positive = 0
	negative = 0
	neutral = 0
	posTweets = []

	for tweet in tweets:
	  val = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet.text).split())
	  analysis = TextBlob(val)
	  #print(analysis.sentiment.polarity)
	  polarity += analysis.sentiment.polarity
	  if (analysis.sentiment.polarity == 0):
	      neutral += 1
	  elif (analysis.sentiment.polarity > 0):
	      positive += 1
	      posTweets += 
	  elif (analysis.sentiment.polarity < 0):
	      negative += 1
	  
	print(positive,negative,neutral,noOfSearchItem)


	polarity = polarity/noOfSearchItem

	if (polarity == 0):
	    value = "Neutral"
	elif (polarity > 0):
	    value = "Positive"
	elif (polarity < 0):
	    value ="Negative"

	return json.dumps({'status':'OK','value':value});


 
@app.route("/")
def hello():
    return "Welcome to Python Flask!"
 
if __name__ == "__main__":
    app.run()	