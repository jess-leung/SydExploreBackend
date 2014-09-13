from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from attractions.models import Review
from attractions.models import Attraction
import cPickle as pickle 
from nltk import word_tokenize

stopwords = [] 
labels = ['Fun','Social','Adventurous','Lazy','Hungry','Natural','Cultural','Education','Historical','Luxurious']

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
    print features
    return features

def classifyReview(review_attraction,review_text,review_title,labels,stopwords):
    review_text_tokenized = word_tokenize(review_text)
    review_title_tokenized = word_tokenize(review_title)
    review_attraction_tokenized = word_tokenize(review_attraction)
    print review_text_tokenized
    thisFeatures = getFeatures(review_attraction_tokenized,review_text_tokenized,review_title_tokenized,labels,stopwords)
    classifierFile = open('textClassification/classifier.pkl','rb')
    classifier = pickle.load(classifierFile)
    this_class = classifier.predict(thisFeatures)
    print this_class
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
        print type(review_title)

        # create review 
        r = Review(review_title=review_title, reviewer_name=reviewer_name, review_text=review_text, review_rating=review_rating, attraction=attraction)
        r.save()

        for line in open('textClassification/stopwords'):
            stopwords.append(line.strip()) 

        # onto the machine learning bit 
        review_category = classifyReview(review_attraction,review_text, review_title,labels,stopwords)
        print 'This review is classified as: ',review_category
        # TODO
        # get the category of the attraction that the review is affecting 

        # increment the voted category by 1 

        # if the voted category > current category, change category of the attraction 

        # ENDTODO

    except Exception,e:
        print 'Exception: Could not parse JSON ',str(e)
    
    return HttpResponse('Review Submitted')