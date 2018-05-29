import os,sys,re
from nltk import *
from nltk.collocations import *
from nltk.tokenize import *
from pos_tagger import *
import identify_entities
from feature_reduction import *
from feature_clustering import *
import pickle

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


def get_asins(Product):
    them = os.listdir('Cell_Phones')
    asins = [file.strip('.json') for file in them]
    return asins

def get_review_text(Product,asin):
    data = open(Product+'/'+asin+'.json','r').read()
    data=data.replace('-','.')
    data=data.replace('*','.')
    data=re.sub('\.+','.',data)
    data=re.sub('[^a-zA-Z0-9.\\s]+',' ',data)
    data=re.sub(r'([a-z]{2,})\1+', r'\1', data)
    return data

def convert_review_text_to_nltk_text(review_text):
    tokens = word_tokenize(review_text)
    return tokens

def get_collocations(nltk_text):
    finder = BigramCollocationFinder.from_words(nltk_text)
    finder.apply_freq_filter(3)
    collocations = finder.nbest(bigram_measures.pmi,30)
    return collocations


def analyse_one_product(review_text):
    review_text = re.sub('([.,;!?])\s*(\w)',r'\1 \2',review_text)
    review_text_copy = review_text
    review_text = review_text.lower()
    features = []
    nltk_text = convert_review_text_to_nltk_text(review_text)
    collocations = get_collocations(nltk_text)
    Title = ''
    entities = identify_entities.main(review_text,Title)
    entities = [tuple(word_tokenize(i)) for i in entities]
    reviews = review_text_copy.split('\n')
    reviews = [i for i in reviews if len(i) > 1]
    review_text_tokenized = [sent_tokenize(review) for review in reviews]

    nouns,verbs,adjectives,adverbs,candidate_sentences,collocation_tagged,entities_tagged = pos_tagger(review_text_tokenized,collocations,entities)
    features = feature_reduction(collocation_tagged,candidate_sentences,entities_tagged, review_text_tokenized)
    features = cluster_features(features)
    feature_list = [i for i in features]
    return feature_list,features

def get_features():
    done = os.listdir('Features')
    Product = 'Cell_Phones'
    asins = get_asins(Product)
    asins = ['B079JSZ1Z2']
    for asin in asins:
        if asin+'_features' in done and False:
            print asin + ' Done'
            continue
    review_text = get_review_text(Product,asin)
    feature_list,features = analyse_one_product(review_text)
    f = open('FeatureList/'+asin+'_features','w')
    for i in feature_list:
        f.write(`i`+'\n')
    pickle.dump(features,open('Features/'+asin+'_features','w')) 
    print ' Done'
    f.close()

if __name__ == "__main__":
    get_features()