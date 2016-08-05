from __future__ import division
from collections import defaultdict
from itertools import chain
from polarity import extract_lexicon_words
import math
import pickle
import os
import re
import sys


def count_score(token_list, polarity_lexicon_dict):
	""" Count classification score for token_list using a polarity_lexicon. 
	    Negative score implies negative opinion, and vice versa. 
	    Return a positive score in case of a tie. """

	total_pos = 0
	total_neg = 0
	for token in token_list:
		if token in polarity_lexicon_dict:
			if polarity_lexicon_dict[token] > 0:
				total_pos += 1
			else:
				total_neg += 1
	total = total_pos - total_neg
	if total != 0:
		return total
	return 1

def count_score_gold(token_list, polarity_lexicon_pos, polarity_lexicon_neg):
	""" Count classification score for token_list using a gold polarity lexicon. 
	Negative score implies negative opinion, and vice versa. 
	Return a positive score in case of a tie. """
	total_pos = 0
	total_neg = 0
	for token in token_list:
		if token in polarity_lexicon_pos:
			total_pos += 1
		if token in polarity_lexicon_neg:
			total_neg += 1
	total = total_pos - total_neg
	if total != 0:
		return total
	return 1


def count_accuracy(pos_path, neg_path, polarity_lexicon): 
	""" Traverse all the files in pos and neg review folders to count the score 
	    and check whether the document lies in corresponding folder.
	    Calculate overall accuracy of predictions. """

	num_files = 0
	predicted_correctly = 0
	for filename in os.listdir(pos_path):
		full_path = os.path.join(pos_path, filename)
  		with open(full_path) as f:
			num_files += 1
	  		tokens = f.read().split()
	  		score = count_score(tokens, polarity_lexicon)
	  		if score > 0:
	  			predicted_correctly += 1
	  		print "My lexicon: predicted score for file %s is %s" % (f, str(score))
	for filename in os.listdir(neg_path):
		full_path = os.path.join(neg_path, filename)
  		with open(full_path) as f:
			num_files += 1
	  		tokens = f.read().split()
	  		score = count_score(tokens, polarity_lexicon)
	  		if score < 0:
	  			predicted_correctly += 1
	  		print "My lexicon: predicted score for file %s is %s" % (f, str(score))
	return predicted_correctly / num_files



def count_accuracy_gold(pos_path, neg_path, polarity_lexicon_pos, polarity_lexicon_neg): 
	""" Traverse all the files in pos and neg review folders to count the score 
	    and check whether the document lies in corresponding folder.
	    Calculate overall accuracy of predictions. """

	num_files = 0
	predicted_correctly = 0
	for filename in os.listdir(pos_path):
		full_path = os.path.join(pos_path, filename)
  		with open(full_path) as f:
			num_files += 1
	  		tokens = f.read().split()
	  		score = count_score_gold(tokens, polarity_lexicon_pos, polarity_lexicon_neg)
	  		if score > 0:
	  			predicted_correctly += 1
	  		print "Gold lexicon: predicted score for file %s is %s" % (f, str(score))
	for filename in os.listdir(neg_path):
		full_path = os.path.join(neg_path, filename)
  		with open(full_path) as f:
			num_files += 1
	  		tokens = f.read().split()
	  		score = count_score_gold(tokens, polarity_lexicon_pos, polarity_lexicon_neg)
	  		if score < 0:
	  			predicted_correctly += 1
	  		print "Gold lexicon: predicted score for file %s is %s" % (f, str(score))
	return predicted_correctly / num_files

def main():
	if len(sys.argv) != 6:
		print "Provide paths to pickle file with polarity lexicon, paths to positive and negative review folders, paths to positive gold lexicon file and negative gold lexicon file!"
	else:
		polarity_lexicon = pickle.load(open(sys.argv[1], "rb" ))
		pos_path = sys.argv[2]
		neg_path = sys.argv[3]
		polarity_lexicon_pos = extract_lexicon_words(sys.argv[4])
		polarity_lexicon_neg = extract_lexicon_words(sys.argv[5])
		score_mine = str(count_accuracy(pos_path, neg_path, polarity_lexicon))
		score_gold = str(count_accuracy_gold(pos_path, neg_path, polarity_lexicon_pos, polarity_lexicon_neg))
		print "With my own polarity lexicon, the documents have been classified with accuracy " + score_mine
		print "With gold polarity lexicon, the documents have been classified with accuracy " + score_gold

if __name__ == '__main__':
    main()




