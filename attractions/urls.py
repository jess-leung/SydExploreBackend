from django.conf.urls import url

from attractions import views

urlpatterns = [
    url(r'^$', views.index, name='postReview'),
]