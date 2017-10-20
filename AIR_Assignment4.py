import nltk
import string
import math
import numpy as np
import heapq
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *
from nltk.corpus import stopwords
from array import array

stemmer = PorterStemmer()
length = [0] * (1400+1)
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
			length[doc_id] = length[doc_id]+1
		else:
			if(doc_id in index[word][2].keys()):
				index[word][2][doc_id] = index[word][2][doc_id]+1
				index[word][1] = index[word][1]+1
				length[doc_id] = length[doc_id]+1
				# index[word][1][doc_id] = index[word][1][doc_id]+1
			else:
				index[word][0] = index[word][0] + 1
				index[word][1] = index[word][1]+1
				index[word][2][doc_id] = 1
				length[doc_id] = length[doc_id]+1
				# index[word][0] = index[word][0] + 1
				# index[word][1][doc_id] = 1
	return index

def main():
	file_name = 'cran.all.1400'
	# file_name = 'test.all.1'
	
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

	continue_query = '1'
	# print(index)	
	# print(stem('boundary'),index[stem('boundary')])	
	while(continue_query=='1'):
		query = input('Enter the Query:')
		# query = 'in the study of high speed viscous'
		# print(query)
		words_in_query = query.split(' ')
		words_in_query = list(filter(lambda x : x not in stop_words,words_in_query))
		words_in_query = list(map(stem,words_in_query))
		# print(words_in_query)
		term_frequency_query = {}
		for word in words_in_query:
			if(word in term_frequency_query.keys()):
				term_frequency_query[word] = term_frequency_query[word] + 1
			else:
				term_frequency_query[word] = 1
		# print('tf query:',term_frequency_query)

		score = [0.0] * (len(doc)+1)
		# print(length)

		inverse_document_frequency = {}
		tf_idf_query = {}
		for key in term_frequency_query.keys():
			# print(key,term_frequency_query[key],index[key])
			term_frequency_query[key] = 1 + math.log10(term_frequency_query[key])
			inverse_document_frequency[key] = math.log10(len(doc)/index[key][0])
			tf_idf_query[key] = term_frequency_query[key] * inverse_document_frequency[key]

			#tf-idf for documents
			for each_doc in index[key][2].keys():
				# print(each_doc,index[key][2][each_doc])
				term_frequency_doc = 1 + math.log10(index[key][2][each_doc])
				score[each_doc] = score[each_doc]+(term_frequency_doc * inverse_document_frequency[key] * tf_idf_query[key])

		for i in range(1,len(score)):
			if(score[i]!=0 or length[i]!=0):
				score[i] = score[i]/length[i]

		# print('tf',term_frequency_query)
		# print('idf',inverse_document_frequency)
		# print('tf-idf',tf_idf_query)
		# print('score',score)
		# score = np.array(score)
		print(heapq.nlargest(10, range(len(score)), score.__getitem__))
		# print((-score).argsort()[:10])

		continue_query = input('1 to continue 0 to exit:')

main()