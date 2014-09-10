from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import nltk 
from django.utils import timezone
from attractions.models import Review
from attractions.models import Attraction

@csrf_exempt    
def postReview(request):
    print 'Post from Android'
    try:
    	# parse JSON 
        data=json.loads(request.body)
        print data
        review_title=data['reviewTitle']
        review_text=data['reviewText']
        reviewer_name=data['reviewer']
        review_rating=data['rating']
        review_attraction=data['attraction']
        print review_title
        print review_text
        print reviewer_name
        print review_rating
        print review_attraction
        # search what the attraction id is 
        #attraction = Attraction.objects.get(name=review_attraction)
        #attraction_id = attraction.id 

        # create review 
        r = Review(review_title=review_title, reviewer_name=reviewer_name, review_text=review_text, review_rating=review_rating, attraction=review_attraction)
        r.save()

        # onto the machine learning bit 
        review_category = classifyReview(review_text, review_title)
        print review_category
        # TODO
 		# get the category of the attraction that the review is affecting 

 		# increment the voted category by 1 

 		# if the voted category > current category, change category of the attraction 

    except:
        print 'Exception: Could not parse JSON'
    
    return HttpResponse('Review Submitted')

def classifyReview(review_text,review_title):
	return 1
