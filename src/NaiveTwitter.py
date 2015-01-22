import math
import sys
import getopt
from sys import stdin

class NaiveTwitter(object):
	def __init__(self, train_tweets, count_t, count_wt, prob_wt, command):
		self.train_tweets = train_tweets

		if command == "set":
			# count tags
			self.count_t = count_t
			# count (words, tags)
			self.count_wt = count_wt
			self.prob_wt = prob_wt
		elif command == "count":
			self.count_t = {}
			self.count_wt = {}
			self.prob_wt = {}
			self.train()

		self.Z = 0.0
		self.calculateZ()

	def calculateZ(self):
		for tag in self.count_t:
			self.Z += self.count_t[tag]

	def train(self):
		self.buildProbabilities()

	def buildProbabilities(self):
		tags_for_tweet = []

		for line in self.train_tweets:
			tokens = set(line.split()) # split at whitespace

			if len(tokens) > 0:
				tags_for_tweet = [] # refresh tags per line
				for t in tokens:
					# search for tag
					if t[0] == '#' and len(t) > 1:
						# increment tag count
						tag = t.lower()
						if self.count_t.get(tag, 0) == 0:
							self.count_t[tag] = 1.0
						else:
							self.count_t[tag] += 1.0
						if tag not in tags_for_tweet:
							tags_for_tweet.append(tag)

				# increment word, tag counts
				for w in tokens:
					if not (w[0] == "#") and not (w[0] == "@"):
						for t in tags_for_tweet:
							if self.count_wt.get(self.makeKey(w, t), 0) == 0:
								self.count_wt[self.makeKey(w, t)] = 1.0
							else:
								self.count_wt[self.makeKey(w, t)] += 1.0


		dirname = "data/full/"
		wt_count_file = open(dirname + "wordtag_counts", "w+")
		wt_probs_file = open(dirname + "wordtag_probs", "w+")
		wt_log_probs_file = open(dirname + "wordtag_logprobs", "w+")

		for wt in self.count_wt:
			wt_count_file.write(wt + " " + str(self.count_wt[wt]) + "\n");
			wt_probs_file.write(wt + " " + str(float(self.count_wt[wt]) / float(self.count_t[self.splitOnFunkySymbol(wt)])) + "\n")
			prob = float(self.count_wt[wt]) / float(self.count_t[self.splitOnFunkySymbol(wt)])
			wt_log_probs_file.write(wt + " " + str(math.log(prob)) + "\n")

		wt_count_file.close()
		wt_probs_file.close()
		wt_log_probs_file.close()

		t_count_file = open(dirname + "tag_counts", "w+")
		for t in self.count_t:
			t_count_file.write(t + " " + str(self.count_t[t]) + "\n")

		t_count_file.close()

		t_count_sorted_file = open(dirname + "tag_counts_sorted", "w+")
		for t in sorted(self.count_t, key=self.count_t.get):
			t_count_sorted_file.write(t + " " + str(self.count_t[t]) + "\n")

		t_count_sorted_file.close()

		# for wt in self.count_wt:
		# 	print wt, ": ", float(self.count_wt[wt]) / float(self.count_t[self.splitOnFunkySymbol(wt)])

	def splitOnFunkySymbol(self, funkytag):
		return funkytag.split("<|>")[1]



	def test(self, tweet):
		# add-lambda smoothing

		# vocab size
		V = len(self.count_wt)

		# total_prob = 1.0
		# highest_prob = -float("inf")

		highest_weight = -float("inf")

		likely_tags = []
		actual_tags = []
		# for line in self.train_tweets:

		tokens = set(tweet.split()) # split at whitespace

		# consider each tag
		
		# highest_prob = -float("inf")
		for tag in self.count_t:
			# reset for every tag

			total_weight = math.log(self.count_t[tag] / self.Z)
			for word in tokens:
				# ignore hashtags
				if "#" not in word: 
					if self.count_wt.get(self.makeKey(word, tag), 0) == 0:
						# add-1 smoothing
						prob = 1.0 / (self.count_t[tag] + V)
					else:
						prob = (self.count_wt[self.makeKey(word, tag)]) / (self.count_t[tag])
					
					total_weight += math.log(prob)

					# stop if the probability is already less than the highest probability stored
					if total_weight < highest_weight:
						break;
				else:
					# save actual tag
					actual_tags.append(word)

			# store highest probability and best tag so far
			if total_weight > highest_weight:
				# print total_weight, highest_weight
				highest_weight = total_weight

				# scrap existing likely tags and begin new list
				likely_tags = [tag]

			elif total_weight == highest_weight:
				likely_tags.append(tag)

		return likely_tags
		# print "Guessed Tag: ", tweet, ": " + str(likely_tags)



	def makeKey(self, str1, str2):
		return str1 + "<|>" + str2