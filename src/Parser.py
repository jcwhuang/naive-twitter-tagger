
import sys
from sys import stdin

class Parser(object):
	def __init__(self, train, test, count_t, count_wt, prob_wt, command):
		self.count_t = {}
		self.count_wt = {}
		self.prob_wt = {}

		# probably do something later
		self.test = []
		if command == "train":
			self.tweets = open(train).read().splitlines()
			self.removeTagless()
		elif command == "read":
			self.setVariables(count_t, count_wt, prob_wt)

		self.parseTest(test)

	def parseTest(self, test):
		test_file = open(test).read().splitlines()
		for tweet in test_file:
			split_tweet = tweet.split()
			tags = []
			if len(split_tweet) > 1:
				if "#" in tweet:
					for word in split_tweet:
						if word[0] == '#':
							tags.append(word.lower())
					self.test.append((tweet, tags))

	def setVariables(self, count_t, count_wt, prob_wt):
		self.tweets = []
		self.test = []

		self.tagcounts = open(count_t).read().splitlines()
		self.wordtagcounts = open(count_wt).read().splitlines()
		self.wordtagprobs = open(prob_wt).read().splitlines()
		
		for tagcount in self.tagcounts:
			tc = tagcount.split()
			self.count_t[tc[0]] = float(tc[1])
		
		for wordtag in self.wordtagcounts:
			wt = wordtag.split()
			self.count_wt[wt[0]] = float(wt[1])

		for wordtag in self.wordtagprobs:
			wt = wordtag.split()
			self.prob_wt[wt[0]] = float(wt[1])


		# print self.tweets
		# print "&&&&&&&&&&&&&&&"
		# print self.tweets

	# Eliminates hashtag-less tweets
	def removeTagless(self):
		# numtweets = 0
		updatedtweets = []
		for tweet in self.tweets:
			# numtweets += 1
			# if numtweets % 1000 == 0:
			# 	print numtweets
			if "#" in tweet:
				updatedtweets.append(tweet)
				# self.tweets.remove(tweet)
		self.tweets = updatedtweets
				
		# for i in xrange(len(self.tweets)):
		# 	if "#" not in self.tweets[i]:
		# 		self.tweets.pop(i)
		# 		# print "cool"
