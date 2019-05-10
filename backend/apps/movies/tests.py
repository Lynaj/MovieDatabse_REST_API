import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from apps.movies.models import *
from apps.movies.serializers import *

import json
import os
import codecs

class CompanyViewSetTestCase(APITestCase):
    url_get = reverse("api:movies-get")
    url_list = reverse("api:movies-list")
    url_post = reverse("api:movies-post")

    def setUp(self):
        # Setting up basic variables
        test_rating_model__source = "Rotten Tomatoes"
        test_rating_model__value = "89%"

        test_language_model__name = "English"
        test_second_language_model__name= "Swedish"

        test_actor_model__first_name = "Leonardo"
        test_actor_model__last_name = "DiCaprio"

        # Prepeparing languages, actors & ratings
        created__rating_model = RatingModel.objects.create(
            source=test_rating_model__source,
            value=test_rating_model__value
        )

        created__language_model = LanguageModel.objects.create(
            name=test_language_model__name
        )
        created__second_language_model = LanguageModel.objects.create(
            name=test_second_language_model__name
        )

        created__actor_model = ActorModel.objects.create(
            first_name=test_actor_model__first_name,
            last_name=test_actor_model__last_name
        )