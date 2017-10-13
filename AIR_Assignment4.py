import nltk
import string
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *
from nltk.corpus import stopwords

stemmer = PorterStemmer()

stop_words = set(stopwords.words('english'))

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
	for word in tokens:
		if(word not in index):
			# index[word] = [1,{doc_id:1}]

			#df,tf,{doc_id:frequency}
			index[word] = [1,1,{doc_id:1}]
		else:
			if(doc_id in index[word][2].keys()):
				index[word][2][doc_id] = index[word][2][doc_id]+1
				index[word][1] = index[word][1]+1

				# index[word][1][doc_id] = index[word][1][doc_id]+1
			else:
				index[word][0] = index[word][0] + 1
				index[word][1] = index[word][1]+1
				index[word][2][doc_id] = 1

				# index[word][0] = index[word][0] + 1
				# index[word][1][doc_id] = 1
	return index

def main():
	# file_name = 'cran.all.1400'
	file_name = 'test.all.1'

	with open(file_name) as f:
	    data = f.read()

	doc = data.split('.I')
	del(doc[0])
	print('Total Documents:',len(doc))
	index = {}
	for i in range(len(doc)):
		doc_id = doc[i].split('.T')[0]
		content = doc[i].split('.W')[1]
		tokens = preProcessing(content)
		index = buildIndex(index, int(doc_id), tokens)
	
	# print(index)	
	# print(stem('boundary'),index[stem('boundary')])	
	query = input('Enter the Query:')
	# print(query)

main()