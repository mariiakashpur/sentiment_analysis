from __future__ import division
from collections import defaultdict
from itertools import chain
import math
import pickle
import os
import re


def count_score(token_list, polarity_lexicon):
	""" Count classification score for token_list using a polarity_lexicon. 
	    Negative score implies negative opinion, and vice versa. 
	    Return a positive score in case of a tie. """

	total_pos = 0
	total_neg = 0
	for token in token_list:
		if token in polarity_lexicon:
			if polarity_lexicon[token] > 0:
				total_pos += 1
			else:
				total_neg += 1
	total = total_pos - total_neg
	if total != 0:
		return total
	return 1


def count_accuracy(paths, polarity_lexicon): 
	""" Take tuple of folder paths and traverse all the files in folders to count the score 
	    and check whether the document lies in corresponding folder.
	    Calculate overall accuracy of predictions. """

	num_files = 0
	predicted_correctly = 0
	for path, dirs, files in chain.from_iterable(os.walk(path) for path in paths):
		for f in files:
			full_path = os.path.join(path, f)
			with open(full_path) as f:
				num_files += 1
		  		tokens = f.read().split()
		  		score = count_score(tokens, polarity_lexicon)
		  		if (path == 'pos' and score > 0) or (path == 'neg' and score < 0):
		  			predicted_correctly += 1
		  		print "Predicted score for file %s is %s" % (full_path, str(score))
	return predicted_correctly / num_files


def main():
	polarity_lexicon = pickle.load(open("lexicon.p", "rb" ))
	print "The documents have been classified with accuracy "+ str(count_accuracy(('pos', 'neg'), polarity_lexicon))

if __name__ == '__main__':
    main()
