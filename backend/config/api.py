from rest_framework import routers

from apps.movies.views import *
from apps.comments.views import *

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'movies', MovieViewSet, base_name="movies")
api.register(r'comments', CommentViewSet, base_name="comments")
