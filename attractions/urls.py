from django.conf.urls import url

from attractions import views

urlpatterns = [
    url(r'^postReview/$',views.postReview, name='postReview'),
    url(r'^getAttractions/$',views.getAttractions, name='getAttractions'),
    url(r'^getReviewDetails/$',views.getReviewDetails,name='getReviewDetails'),
]