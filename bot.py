import time
import praw
import pickle

#autentica praw, the reddit API
r = praw.Reddit(user_agent='PNWSwag/1.0')
r.login('PNWSwag', pw)


all_tweets = []
combined_stats = []
while True: 
	all_tweeters = {}	
	tweets_per_tweeter = {}
	not_commented =[]
	submissions = r.get_subreddit('nba').get_new(limit=500) #get the newest posts to /r/nba
	for x in submissions:	
		submission = next(submissions)
		if submission.domain == u'twitter.com' or submission.domain == u'mobile.twitter.com': #check if post links to twitter
			idee = submission.id
			if idee not in all_tweets:
				all_tweets.append(idee)
				not_commented.append(idee)
	for i in range(0, len(all_tweets)) :
		submission = r.get_submission(submission_id = all_tweets[i])
		s = submission.url
		split_url = s.split("/", 4)
		tweeter = split_url[3].lower() #pull name of tweeter from twitter url
		if tweeter in all_tweeters:	
			all_tweeters[tweeter] = all_tweeters[tweeter] + submission.score
			tweets_per_tweeter[tweeter] = tweets_per_tweeter[tweeter] + 1
		else:
			all_tweeters[tweeter] = submission.score	
			tweets_per_tweeter[tweeter] = 1
	for ii in range (-1*len(not_commented) + 1, 1) :
		time.sleep(600) #it was a new account, so there was no karma, meaning i could only post every ten minutes
		submission = r.get_submission(submission_id = not_commented[-1*ii])
		s = submission.url
		split_url = s.split("/", 4)
		tweeter = split_url[3].lower()
		num_tweets = tweets_per_tweeter[tweeter]
		num_points = all_tweeters[tweeter]
		
		#posts the amount of tweets linked to date, and the upvotes of those tweets
		s = "{}{}{}\n{}{}\n{}{}".format("Stats for ", tweeter, ", starting from 7/17/2014 - ", "\nNumber of tweets linked: ", num_tweets, "\nPoints from tweets: ", num_points)
		submission.add_comment(s)
	outFile = open('tweet_reps.txt', 'wb')
	pickle.dump(all_tweets, outFile)
	outFile.close()				
