import nltk
import string
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *
from nltk.corpus import stopwords

stemmer = PorterStemmer()

stop_words = set(stopwords.words('english'))
# print(stop)
def stem(word):
	return stemmer.stem(word)

def preProcessing(content):
	tokens = nltk.wordpunct_tokenize(content)
	tokens = list(map(lambda x : x.lower(), tokens))
	tokens = list(filter(lambda x : x not in stop_words,tokens))
	tokens = list(filter(lambda x : len(x)>1,tokens))
	tokens = list(map(stem,tokens))
	return tokens

def buildIndex(index, doc_id, tokens):
	print(tokens)
	for word in tokens:
		print(word)
		if(word not in index):
			index[word] = [{doc_id:1}]
		else:
			list = index[word]
			for i in range(len(list)):
				if(doc_id in list[i]):
					# print(list[i])
					
	print(len(index))
	return index

def main():
	# file_name = 'cran.all.1400'
	file_name = 'test.all.1'

	with open(file_name) as f:
	    data = f.read()

	doc = data.split('.I')
	del(doc[0])
	index = {}
	for i in range(len(doc)):
		doc_id = doc[i].split('.T')[0]
		print(doc_id)
		content = doc[i].split('.W')[1]
		tokens = preProcessing(content)
		index = buildIndex(index, doc_id, tokens)
	
	print(index['samrat'])		


main()