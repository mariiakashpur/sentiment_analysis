Сreating a polarity lexicon and classifying movie reviews as positive or negative based on this lexicon
Author: Mariia Kashpur
		mariia.kashpur@gmail.com

To create the lexicon, run "polarity.py". Command line arguments to be passed: 
	- path to positive lexicon words (from the positive folder of the gold polarity lexicon)
	- path to negative lexicon words (from the negative folder of the gold polarity lexicon)
	- path to the reviews corpus.
The words "excellent" and "poor" are used to create a lexicon, and the frame is 5 words. 

To see the classification results, run "classify.py". Command line arguments to be passed: 
	- path to polarity lexicon pickle file generated in previous step
	- path to positive reviews dataset
	- path to negative reviews dataset
	- path to positive lexicon words (from the positive folder of the gold polarity lexicon)
	- path to negative lexicon words (from the negative folder of the gold polarity lexicon).
