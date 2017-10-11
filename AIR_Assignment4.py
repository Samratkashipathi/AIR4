import nltk
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *
from nltk.corpus import stopwords

stemmer = PorterStemmer()

stop = set(stopwords.words('english'))
# print(stop)

def preprocesing(word):
	if word not in stop:
		word = word.lower()
		return word

def buildInvertedIndex(doc_id , content):
	content_array = content.split(' ')
	# print(content_array)
	for i in range(len(content_array)):
		word = preprocesing(content_array[i])
		# print(word)


# file_name = 'cran.all.1400'
file_name = 'test.all.10'
with open(file_name) as f:
    data = f.read()
# print(data)
doc = data.split('.I')
del(doc[0])
# print(doc[1])
for i in range(len(doc)):
	doc_id = doc[i].split('.T')[0]
	print(doc_id)
	content = doc[i].split('.W')[1]
	# print(content)
	buildInvertedIndex(doc_id,content)

# print(inverted_index)