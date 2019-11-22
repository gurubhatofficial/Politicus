from flask import Flask, request, json
from flask import render_template
from flask_cors import CORS, cross_origin
import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer	
from textblob import TextBlob
import re

analyzer = SentimentIntensityAnalyzer()
app = Flask(__name__)
cors = CORS(app)

ans = ""
stats = {}
positive = 0
negative = 0
neutral = 0

@app.route('/Summary', methods=['GET'])
def Summary():
	global positive
	global negative
	global neutral
	return json.dumps({'status':'OK','pos':positive, 'neu':neutral, 'neg':negative});

@app.route('/Analysis', methods=['POST'])
def Analysis():
	global ans
	global positive
	global negative
	global neutral

	import tweepy
	query = request.form['Query'];
	consumer_key = '2iIKQ2OGISWaC7bCN4sRV1R5f'
	consumer_secret = 'dhucIfcl4x9Ga32BXl4JxG86t1EuoSm0o5ihPbIx3jcK5CbQIP'
	access_token = '1196118763415846912-pWeWqLmb16UvfJSQmh9aWDEIKmAfXI'
	access_token_secret = 'PA2KOuuv6gDJUb5geOmf6WeowjpWoUoIaoSY8beh4Ue9L'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_token_secret) 
	api = tweepy.API(auth)

	searchTerm = query
	noOfSearchItem = 100

	tweets = api.search(q=searchTerm, count = noOfSearchItem)

	for tweet in tweets:
	  val = tweet.text
	  score = analyzer.polarity_scores(str(val))
	  #print(score["compound"])
	  if(score["compound"] > 0.0):
	    positive += 1
	  if(score["compound"] == 0.0):
	    neutral += 1
	  if(score["compound"] < 0.0):
	    #print(val)
	    negative += 1
	import operator
	#print(positive, neutral, negative)
	stats = {'pos':positive, 'neutral':neutral, 'neg': negative}
	ans = max(stats.items(), key=operator.itemgetter(1))[0]
	return json.dumps({'status':'OK','value':ans});


 
@app.route("/")
def hello():
    return "Welcome to Python Flask!"
 
if __name__ == "__main__":
    app.run()	