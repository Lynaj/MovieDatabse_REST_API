from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout

from django.conf.urls import include, url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from config.api import api

from apps.comments.views import *
from apps.movies.views import *

app_name = 'api'


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),


    url(r'^top/', TopRatedMovies.as_view(), name='api-top-rated-movies'),
    url(r'^movies/', MovieModelAPIView.as_view(), name="movies"),

    path('api/v1/', include((api.urls, 'api')))
]

# python manage.py test apps


