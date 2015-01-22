# naive-twitter-tagger

Originally created as a final project for Intro to Machine Learning by Matthew
Hauser and Jade Huang.

### Description
naive-twitter tagger is a Naive Bayes classifier that "auto-generates" relevant Twitter hashtags.
Relevancy is determined based on frequency of a word and hashtag occurring
together as well as frequency of a hashtag.
This could potentially be useful to help generate descriptive tags for users to
increase their visibility and searchability.

Our training data consists of a mix of precollected corpuses of tweets as well
as randomly collected tweets using two libraries of Python scripts and the
Twitter API.

### Precompiled corpuses
- [Sentiment140 Corpus](http://help.sentiment140.com/for-students/)
- [Twitter Political
  Corpus](http://www.usna.edu/Users/cs/nchamber/data/twitter/)

### Scripts used to generate corpuses
- [Python Twitter](https://github.com/bear/python-twitter)
- [twitter-stream-downloader](https://github.com/mdredze/twitter stream downloader)



