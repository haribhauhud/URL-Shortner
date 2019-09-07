
from django.urls import path
from django.conf.urls import url
from . import views
from . import services

app_name = 'urlmgmt'
urlpatterns = [
    # for our home/index page
    url(r'^index/', views.index, name='index'),

    # when short URL is requested it redirects to original URL
    # path(r'^(?P&lt;short_id&gt;\w{6})$', views.redirect_original, name='redirectoriginal'),
    # this will create a URL's short id and return the short URL
    url(r'^makeshort/', views.shorten_url, name='makeshort'),
    
    # APIs
    url(r'^api/v1/urls/', services.ShortUrlAPIView.as_view(), name='classview'),

    # url(r'^(?P<short_url>w{6})$', views.redirect_url, name='redirect'),
    url(r'^(?P<url>.+)/$', views.redirect_url, name='redirect'),
]


