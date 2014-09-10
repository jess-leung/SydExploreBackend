from django.conf.urls import url

from attractions import views

urlpatterns = [
    url(r'^postReview/$',views.postReview, name='postReview'),
]