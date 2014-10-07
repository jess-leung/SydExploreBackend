from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from attractions.models import Review
from attractions.models import Attraction
import cPickle as pickle 
import nltk
from nltk import word_tokenize
from collections import defaultdict 
import string
from porter2 import stem
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
import random 

stopwords = [] 
labels = ['Fun','Social','Adventurous','Lazy','Hungry','Natural','Cultural','Education','Historical','Luxurious']
labels_mapping = { 'Fun': 'FUN', 'Social': 'SOC', 'Adventurous': 'ADV','Lazy':'LAZ','Hungry':'HUN','Natural':'NAT','Cultural':'CUL','Education':'EDU','Historical':'HIS','Luxurious':'LUX' }
nltk.data.path.append('textClassification/nltk_data/')

def getFeatures(attraction,title,bodyText,labels,stopwords): 
    features = defaultdict() 
    for word in attraction: 
        features[('attraction_word',word)]=1
    titleCount=0
    for word in title: 
        if word.lower() not in stopwords: 
            features[('title_word',word.lower())]=1
            if word.lower() in labels:
                features[('title_label',word.lower())]=1
            if titleCount==0:
                features[('first_word',word)]=1
        titleCount+=1
    counter = 0
    previousWord = ''
    for word in bodyText: 
        if word.lower() not in stopwords and word not in string.punctuation: 
            features[('body_word',word)]=1
            features[('body_word_stemmed',stem(word).lower())]=1
            # if postags[counter][1]=='JJ':
            #   features[('body_jj',word)]=1
            # if postags[counter][1]=='NN':
            #   features[('body_nn',word)]=1
            if word.lower() in labels:
                features[('body_label',word.lower())]=1
            # if counter != 0:
            #   features[('bigram',previousWord.lower()+word.lower())]=1
            previousWord=word
            # for key,value in gazeteer.iteritems():
            #   if word.lower() in value: 
            #       features[(key+'gazeteer',word.lower())]=1

        counter+=1
    features[('length_review',len(bodyText))]=1
    return features

def classifyReview(review_attraction,review_text,review_title,labels,stopwords):
    # tokenize stuff for this review 
    review_text_tokenized = word_tokenize(review_text)
    review_title_tokenized = word_tokenize(review_title)
    review_attraction_tokenized = word_tokenize(review_attraction)
    # get features 
    thisFeatures = getFeatures(review_attraction_tokenized,review_text_tokenized,review_title_tokenized,labels,stopwords)
    ''' Load pickle objects ''' 
    classifierFile = open('textClassification/classifier.pkl','rb')
    selectorFile = open('textClassification/selector.pkl','rb')
    vecFile = open('textClassification/dictvect.pkl','rb')
    vec = pickle.load(vecFile)
    selector = pickle.load(selectorFile)
    classifier = pickle.load(classifierFile)
    # transform the features for this review 
    thisFeatures = vec.transform(thisFeatures)
    thisFeatures = selector.transform(thisFeatures)
    # classify review 
    this_class = classifier.predict(thisFeatures)
    return this_class

@csrf_exempt    
def postReview(request):
    print 'Post from Android'
    try:
        # parse JSON 
        # print request.body
        data = json.loads(request.body)
        review_title=data['reviewTitle']
        review_text=data['reviewText']
        reviewer_name=data['reviewer']
        review_rating=data['rating']
        review_attraction=data['attraction']
        # search what the attraction id is 
        attraction = Attraction.objects.get(name=review_attraction)
        # attraction_id = attraction.id 

        for line in open('textClassification/stopwords'):
            stopwords.append(line.strip()) 

        # onto the machine learning bit 
        review_category = classifyReview(review_attraction,review_text, review_title,labels,stopwords)[0]
        print 'This review is classified as: ',review_category

        # create review 
        r = Review(review_title=review_title, reviewer_name=reviewer_name, review_text=review_text, review_rating=review_rating, attraction=attraction,review_category=review_category)
        r.save()

        # get the category of the attraction that the review is affecting 
        # and increment the voted category by 1 
        affected_vote_count=0
        new_category=''
        if review_category == 'Cultural': 
            affected_vote_count = attraction.vote_cultural
            attraction.vote_cultural = affected_vote_count+1
            new_category = 'CUL'
        elif review_category == 'Education':
            affected_vote_count = attraction.vote_education
            attraction.vote_education = affected_vote_count+1
            new_category = 'EDU'
        elif review_category == 'Social':
            affected_vote_count = attraction.vote_social
            attraction.vote_social = affected_vote_count+1
            new_category = 'SOC'
        elif review_category == 'Adventurous':
            affected_vote_count = attraction.vote_adventurous
            attraction.vote_adventurous = affected_vote_count+1
            new_category = 'ADV'
        elif review_category == 'Fun':
            affected_vote_count = attraction.vote_fun
            attraction.vote_fun = affected_vote_count+1
            new_category = 'FUN'
        elif review_category == 'Lazy':
            affected_vote_count = attraction.vote_lazy
            attraction.vote_lazy = affected_vote_count+1
            new_category = 'LAZ'
        elif review_category == 'Hungry':
            affected_vote_count = attraction.vote_hungry
            attraction.vote_hungry = affected_vote_count+1
            new_category = 'HUN'
        elif review_category == 'Natural':
            affected_vote_count = attraction.vote_natural
            attraction.vote_natural = affected_vote_count+1
            new_category = 'NAT'
        elif review_category == 'Historical': 
            affected_vote_count = attraction.vote_historical
            attraction.vote_historical = affected_vote_count+1
            new_category = 'HIS'
        else: #luxurious 
            affected_vote_count = attraction.vote_luxurious
            attraction.vote_luxurious = affected_vote_count+1
            new_category = 'LUX'

        # get current category count 
        current_category_count = attraction.vote_category 
        affected_vote_count+=1
        print current_category_count
        print new_category
        print affected_vote_count
        # if the voted category > current category, change category of the attraction 
        if affected_vote_count > current_category_count: 
            attraction.category = new_category 
            attraction.vote_category = affected_vote_count
        elif affected_vote_count == current_category_count:
            tiebreaker = random.randint(0,1)
            # if tiebreaker = 0 then change to the new category and update the count for that to be affected_vote_count
            if tiebreaker == 0: 
                attraction.category = new_category

        attraction.save()

    except Exception,e:
        print 'Exception: Could not parse JSON ',str(e)
    
    return HttpResponse('Review Submitted')

@csrf_exempt    
def getAttractions(request):
    print 'Getting attractions'
    attractions=''
    try: 
        data = json.loads(request.body)
        attractions=[]
        if data['category_name']=="All":
            attractions=Attraction.objects.values('name','location','latitude','longitude','thumbnail','opening_hours','description','url','image')
        else: 
            category_key = labels_mapping[data['category_name']]
            attractions = Attraction.objects.filter(category=category_key).values('name','location','latitude','longitude','thumbnail','opening_hours','description','url','image')
    except Exception,e:
        print 'Exception: Could not parse JSON ',str(e)

    return HttpResponse(json.dumps(list(attractions)), content_type="application/json")

@csrf_exempt
def getReviewDetails(request):
    reviewDetails=''
    try:
        data=json.loads(request.body)
        attraction_name = data['attraction_name'] 
        reviewDetails = Review.objects.filter(attraction__name=attraction_name).values('review_text','reviewer_name','review_title','review_rating')
        print reviewDetails
                
    except Exception,e:
        print 'Exception: Could not parse JSON'

    return HttpResponse(json.dumps(list(reviewDetails)), content_type="application/json")

