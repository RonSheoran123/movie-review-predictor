import nltk
from nltk.corpus import movie_reviews
import random
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import string
from nltk import pos_tag

documents=[]
for category in movie_reviews.categories():
    for file_id in movie_reviews.fileids(category):
        documents.append((movie_reviews.words(file_id),category))

random.shuffle(documents)
lemmatizer=WordNetLemmatizer()

def get_simple_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

stops=set(stopwords.words('english'))
punctuations=list(string.punctuation)
stops.update(punctuations)

def clean_review(words):
    output_words=[]
    for w in words:
        if w not in stops:
            pos=pos_tag([w])
            clean_word=lemmatizer.lemmatize(w,pos=get_simple_pos(pos[0][1]))
            output_words.append(clean_word.lower())
    return output_words

documents=[(clean_review(document),category) for document,category in documents]
training_documents=documents[0:1500]
testing_documents=documents[1500:]

all_words=[]
for doc in testing_documents:
    all_words+=doc[0]

freq=nltk.FreqDist(all_words)
common=freq.most_common(3000)
features=[i[0] for i in common]

def get_feature_dict(words):
    current_features={}
    words_set=set(words)
    for w in features:
        current_features[w]=w in words_set
    return current_features

training_data=[(get_feature_dict(doc),category) for doc,category in training_documents]
testing_data=[(get_feature_dict(doc),category) for doc,category in testing_documents]
