from __future__ import division
from collections import defaultdict
import math
import pickle
import re
import sys

def extract_lexicon_words(file_path):
  """ Extract positive/negative words from polarity lexicon file as a list. """ 
  words = []
  with open(file_path) as f:
    for line in f:
      if re.match("[^;]", line) and len(line) > 1:
        words.append(line.strip())
  return words


def get_token_list(corpus_path): 
  """ Return all tokens in corpus as a list. """
  with open(corpus_path) as f:
    tokens = f.read().split()
    return tokens


def count_cooccurence(tokens, lexicon_words, reference_word, window):
  """ Look to the left and to the right of a reference word within a certain window in tokens
      to find how often each of lexicon_words occurs within this window. """
  cooccurence = defaultdict(int)
  indexes = [] 
  for index, token in enumerate(tokens):
    if token == reference_word:
      indexes.append(index)
  for index in indexes:
    for word in lexicon_words:
      if word in tokens[index-window:index] or word in tokens[index:index+window+1]:
        cooccurence[word] += 1
  return cooccurence

def count_polarity(pos_cooccurence, neg_cooccurence, pos_word, neg_word, tokens):
  """ Take a list of tokens and calculate polarity for each.
      This value will be larger than 0 if the word is positive, and smaller than 0 if it is negative. """
  count_pos_word = tokens.count(pos_word)
  count_neg_word = tokens.count(neg_word)
  polarity = defaultdict(float)
  for word in pos_cooccurence:
    neg_cooccur = 0.01
    if word in neg_cooccurence:
      neg_cooccur += neg_cooccurence[word]
    polarity[word] = math.log(((pos_cooccurence[word] + 0.01) * count_neg_word) / (neg_cooccur * count_pos_word))
  for word in neg_cooccurence:
    if word not in polarity:
      pos_cooccur = 0.01
      polarity[word] = math.log((pos_cooccur * count_neg_word) / ((neg_cooccurence[word] + 0.01) * count_pos_word))
  return polarity


def count_accuracy(polarity, pos_words, neg_words):
  """ Count accuracy of predictions for words in polarity lexicon. """
  correct_predictions = 0
  for word in polarity:
    if (polarity[word] > 0 and word in pos_words) or (polarity[word] < 0 and word in neg_words):
      correct_predictions += 1
  return correct_predictions / len(polarity)


def main():
  pos_words = extract_lexicon_words(sys.argv[1])
  neg_words = extract_lexicon_words(sys.argv[2])
  tokens_list = get_token_list(sys.argv[3])

  polarity_lexicon = count_polarity(count_cooccurence(tokens_list, neg_words + pos_words, "excellent", 5),
                            count_cooccurence(tokens_list, neg_words + pos_words, "poor", 5),
                            "excellent", "poor", tokens_list)
    
  # save dictionary as a pickle file
  pickle.dump(polarity_lexicon, open( "lexicon.p", "wb")) 
  print pickle.load(open("lexicon.p", "rb" ))
  print "The polarity was predicted with accuracy " + str(count_accuracy(polarity_lexicon, pos_words, neg_words))


if __name__ == '__main__':
    main()






