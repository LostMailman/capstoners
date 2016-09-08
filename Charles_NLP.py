# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 23:50:38 2016

@author: Charles
"""

#%%

#########################
#Read dataset reviews##
#######################
import os
import pandas as pd

os.chdir('C:\\Users\\Charles\\OneDrive\\capstoners')
########################
# original files code ##
########################
#rev = pd.read_csv('yelp_academic_dataset_review.csv')
#bsn = pd.read_csv('yelp_academic_dataset_business.csv')
#print rev.head(10)

##################
# Queryied code ##
##################
data = pd.read_csv('AZ_business_join_review.csv')

#%%
###########################
# Preprocess Review text ##
###########################
import re
import nltk

#porter = nltk.PorterStemmer()
lemma = nltk.wordnet.WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')
# Unicode conversion, Lowercase, Strip Numbers, Strip Punctuation and Tokenize
rev = [nltk.regexp_tokenize(re.sub(r'\d+', '', w.decode('utf-8').lower()), r'\w+') for w in data['text'] if isinstance(w, basestring)]
#Lemmatize
words = [[lemma.lemmatize(w) for w in lis if w not in stopwords] for lis in rev]

#%%
'''
#Save the words list because lemmatization takes forever
import pickle
pickle.dump(words, open("AZ_lemma.p", "wb"))
'''
#%%
'''
#load words if starting a new instance
import pickle #if code is starting from the load to save time
words = pickle.load(open("AZ_lemma.p", "wb"))
'''
#%%
################################
# Create Document Term Matrix ##
################################

from gensim import corpora

reviews = corpora.Dictionary(words)
#reviews.save('reviews.dict')

# create corpus
revCorp = [reviews.doc2bow(w) for w in words]
'''
# save corpus in Blei's lda-c format because creating corpus takes forever
# corpora.BleiCorpus.serialize('revCorp.lda-c', revCorp)
'''
#%%
#load corpora if starting a new instance
'''
from gensim import corpora #if code is starting from the load to save time
revCorp = corpora.BleiCorpus.load('revCorp.lda-c')
'''
#%%
#################################
# LDA algorithm with 10 topics ##
#################################
from gensim import models

revLDA = models.LdaModel(revCorp, num_topics = 10, id2word = reviews, passes = 100)
#%%
#Save the model, because it takes forever
import pickle
pickle.dump(revLDA, open('revLDA.model', 'wb'))

#%%
import pickle
revLDA = pickle.load(open('revLDA.model'))
#%%
#Show what the 10 topics are, and the words that comprise them
#print(revLDA.print_topics(num_topics=10, num_words=10))

'''
topic 1: (0, u'0.141*pizza + 0.037*wing + 0.024*crust + 0.019*sauce + 0.016*topping + 0.015*cheese + 0.014*pie + 0.011*delivery + 0.010*free + 0.010*slice')

topic 2: (1, u'0.036*chicken + 0.025*roll + 0.020*sushi + 0.019*rice + 0.016*dish + 0.015*spicy + 0.015*thai + 0.013*noodle + 0.012*soup + 0.011*fried')

topic 3: (2, u'0.026*place + 0.023*like + 0.021*good + 0.016*food + 0.012*really + 0.011*get + 0.011*would + 0.010*one + 0.009*go + 0.009*better')

topic 4: (3, u'0.072*taco + 0.030*burrito + 0.025*salsa + 0.024*mexican + 0.022*chip + 0.018*bean + 0.018*fish + 0.014*good + 0.013*chicken + 0.012*carne')

topic 5: (4, u'0.032*bar + 0.027*beer + 0.016*drink + 0.011*night + 0.011*patio + 0.011*hour + 0.010*happy + 0.009*music + 0.008*table + 0.008*wine')

topic 6: (5, u'0.019*food + 0.016*time + 0.016*u + 0.015*order + 0.012*service + 0.011*back + 0.011*minute + 0.010*table + 0.010*came + 0.010*get')

topic 7: (6, u'0.037*burger + 0.034*sandwich + 0.030*fry + 0.024*breakfast + 0.017*coffee + 0.013*cheese + 0.013*egg + 0.012*dog + 0.012*good + 0.010*bacon')

topic 8: (7, u'0.098*salad + 0.032*chicken + 0.021*fresh + 0.014*bread + 0.013*tomato + 0.013*dressing + 0.012*pasta + 0.011*healthy + 0.010*lunch + 0.010*option')

topic 9: (8, u'0.013*ordered + 0.011*sauce + 0.010*good + 0.008*great + 0.008*flavor + 0.008*back + 0.008*delicious + 0.008*came + 0.007*pork + 0.007*cheese')

topic 10: (9, u'0.048*great + 0.043*food + 0.037*place + 0.025*service + 0.023*good + 0.017*friendly + 0.016*time + 0.015*back + 0.014*love + 0.014*staff')

topic 1 = pizza and wings. with free delivery. almost a dominos ad

topic 2 = fried chicken, asian food

topic 3 = words associated with good/better/like

topic 4 = mexican food

topic 5 = bar / alcohol

topic 6 = service related items

topic 7 = burger stuff

topic 8 = healthiness stuff

topic 9 = barbeque maybe? sauce and pork stuff + postiive words

topic 10 = good food and service words

'''


#%%
#Reverse transform the LDA model back onto the reviews
#Get probabilities for the ten topics
revTopics = [revLDA[reviews.doc2bow(w)] for w in words]

#%%
#Move into dataframe
topicsTab = pd.DataFrame(columns = (0,1,2,3,4,5,6,7,8,9))

for row in range(len(revTopics)):
    topicsTab.loc[row] = [dict(revTopics[row]).get(i,0) for i in range(10)]
