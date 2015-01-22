	# train_data = "data/TwitterCorpus_train2"
import sys
import getopt
import Parser
import NaiveTwitter

def main(argv):
	optlist, args = getopt.getopt(argv, 't')
	# assuming file is passed in
	
	# Below are some different sets of training / development data we used

	# train_data = "data/nonpolitical-parsed"
	# train_data = "data/twitter_statuses"
	# test_data = "data/TwitterCorpus_train2"
	# train_data = "data/TwitterCorpus_train"
	# test_data = "data/TwitterCorpus_test2"
	# train_data = "data/TwitterCorpus_train"
	# train_data = "data/alldata/abridged/TwitterCorpus_train2"
	# train_data = "data/collected/2014_12_13_18_54_29"
	# train_data = "data/collected/2014_12_13_20_27_16"
	# train_data = "data/collected/2014_12_13_19_44_03"
	# test_data = "data/collected/2014_12_13_19_44_03"
	# test_data = "data/collected/2014_12_13_18_54_29"
	# test_data = "data/collected/2014_12_13_19_02_42"
	# train_data = "data/collected/2014_12_13_19_02_42"
	# test_data = "data/political-parsed"
	# test_data = "data/alldata/abridged/TwitterCorpus_test2"


	# below are the actual files used

	# train_data = "data/AllCollected570112"
	# test_data = "data/AllCollected570112"

	train_data = "data/train"
	test_data = "data/test"

	# if one wishes to avoid retraining, one can specify count/prob files instead

	count_t_data = ""
	count_wt_data = ""
	prob_wt_data = "" 
	com = "train"
	parser = Parser.Parser(train=train_data, test=test_data, count_t=count_t_data, count_wt=count_wt_data, prob_wt=prob_wt_data, command=com)

	# parser = Parser.Parser(train="no_file", test="data/nonpolitical-parsed", count_t="data/full/tag_counts", count_wt="data/full/wordtag_counts", prob_wt="data/full/wordtag_probs", command="read")

	nt = NaiveTwitter.NaiveTwitter(train_tweets=parser.tweets, count_t=parser.count_t, count_wt=parser.count_wt, prob_wt=parser.prob_wt, command="count")

	nt.train()

	total = 0
	correct = 0

	# print len(parser.test)
	# return

	logfile = open("logfile", "w+")
	for tweet in parser.test:
		tagged = nt.test(tweet[0])

		if accurate(logfile, tweet, tagged):
			correct += 1

		total += 1
		print "Iter.     " + str(total), float(correct) / float(total)
		logfile.write("Iter: " + str(total) + "  Accuracy: " + str(float(correct) / float(total))) + "\n"
		# logfile.write("\n")
		# if total == 400:
		#  	break

	print "accuracy ", float(correct) / float(total)
	logfile.write("accuracy " + str(float(correct) / float(total)))

def accurate(logfile, tweet, tagged):
	for tag in tagged:
		if tag in tweet[1]:
			print "RIGHT     " + str(tweet) + "     " + str(tagged)
			logfile.write( "RIGHT     " + str(tweet) + "     " + str(tagged) + "\n")
			return True
	print "WRONG     " + str(tweet) + "     " + str(tagged)
	logfile.write("WRONG     " + str(tweet) + "     " + str(tagged) + "\n")
	return False

if __name__ == "__main__":
	main(sys.argv[1:])