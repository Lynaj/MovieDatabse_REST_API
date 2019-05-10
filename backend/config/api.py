from rest_framework import routers
from apps.users.views import *

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet, base_name="Users Types View")
