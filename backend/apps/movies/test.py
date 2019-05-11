import json
from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from apps.movies.models import *
from apps.movies.serializers import *

from django.test import Client
from rest_framework import viewsets, status

from apps.misc.logger import *
from django.db.models import Q
import datetime

logger = logging.getLogger(__name__)
logger.addHandler(handler)


import datetime
import json
import os
import codecs

class CompanyViewSetTestCase(APITestCase):
    url_list = reverse("movies")


    def setUp(self):
        # Prepating movie's model data
        self.client = Client()
        self.url = reverse("api:comments-list")
        # Prepating movie's model data
        self.test_Title = "Guardians of the Galaxy Vol. 2"
        self.test_Year = "2017"
        self.test_Rated = "PG-13"
        self.test_Released = datetime.datetime.strptime(
            "05 May 2017"
            ,
            "%d %b %Y"
        )
        self.test_Runtime = "136 min"
        self.test_Genre = "Action, Adventure, Comedy, Sci-Fi"
        self.test_Director = "James Gunn"
        self.test_Writer = "James Gunn, Dan Abnett"
        self.test_Country = "USA"
        self.test_Awards = "Nominated for 1 Oscar. Another 12 wins & 42 nominations."
        self.test_Poster = "https://m.media-amazon.com/images/M/MV5BMTg2MzI1MTg3OF5BMl5BanBnXkFtZTgwNTU3NDA2MTI@._V1_SX300.jpg"
        self.test_imdbRating = "7.7"
        self.test_imdbVotes = "471,312".replace(",", ".")
        self.test_imdbID = "tt3896198"
        self.test_Type = "movie"
        self.test_DVD = datetime.datetime.strptime(
            "22 Aug 2017"
            ,
            "%d %b %Y"
        )
        self.test_Metascore = "67"
        self.test_BoxOffice = "$389,804,217"
        self.test_Production = "Walt Disney Pictures"
        self.test_Website = "https://marvel.com/guardians"
        self.test_Response = True

        # Setting up basic variables
        self.test_rating_model__source = "Rotten Tomatoes"
        self.test_rating_model__value = "89%"

        self.test_language_model__name = "English"
        self.test_second_language_model__name= "Swedish"

        self.test_actor_model__first_name = "Leonardo"
        self.test_actor_model__last_name = "DiCaprio"

        # Prepeparing languages, actors & ratings
        created__rating_model = RatingModel.objects.create(
            source=self.test_rating_model__source,
            value=self.test_rating_model__value
        )

        created__language_model = LanguageModel.objects.create(
            name=self.test_language_model__name
        )
        created__second_language_model = LanguageModel.objects.create(
            name=self.test_second_language_model__name
        )

        created__actor_model = ActorModel.objects.create(
            first_name=self.test_actor_model__first_name,
            last_name=self.test_actor_model__last_name
        )

        # Prepeparing languages, actors & ratings
        self.created__rating_model = RatingModel.objects.create(
            source=self.test_rating_model__source,
            value=self.test_rating_model__value
        )

        self.created__language_model = LanguageModel.objects.create(
            name=self.test_language_model__name
        )

        self.created__second_language_model = LanguageModel.objects.create(
            name=self.test_second_language_model__name
        )

        self.created__actor_model = ActorModel.objects.create(
            first_name=self.test_actor_model__first_name,
            last_name=self.test_actor_model__last_name
        )

        # Creating basic data movie data model
        self.created__movie_model = MovieModel.objects.create(
            title=self.test_Title,
            year=self.test_Year,
            rated=self.test_Rated,
            released=self.test_Released,
            runtime=self.test_Runtime,
            genre=self.test_Genre,
            director=self.test_Director,
            writer=self.test_Writer,
            country=self.test_Country,
            awards=self.test_Awards,
            poster=self.test_Poster,
            metascore=self.test_Metascore,
            imdb_rating=self.test_imdbRating,
            imdb_votes=self.test_imdbVotes,
            imbd_id=self.test_imdbID,
            type=self.test_Type,
            dvd=self.test_DVD,
            box_office=self.test_BoxOffice,
            production=self.test_Production,
            website=self.test_Website,
            response=self.test_Response
        )

    def test_list_all_movies_registered_in_the_database(self):



        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(
            "/movies/"
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )


        # Validating record data
        self.assertEqual(
            resp.data[0]["title"]
            ,
            self.test_Title
        )

        self.assertEqual(
            str(resp.data[0]["year"])
            ,
            str(self.test_Year)
        )

    def test_fetch_movie_information_using_external_api_correct_title(self):
        # Preparing mock data
        test_mockResponse = {"Title":"Titanic","Year":"1997","Rated":"PG-13","Released":"19 Dec 1997","Runtime":"194 min","Genre":"Drama, Romance","Director":"James Cameron","Writer":"James Cameron","Actors":"Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates","Plot":"A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.","Language":"English, Swedish, Italian","Country":"USA","Awards":"Won 11 Oscars. Another 111 wins & 77 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.8/10"},{"Source":"Rotten Tomatoes","Value":"89%"},{"Source":"Metacritic","Value":"75/100"}],"Metascore":"75","imdbRating":"7.8","imdbVotes":"946,032","imdbID":"tt0120338","Type":"movie","DVD":"10 Sep 2012","BoxOffice":"N/A","Production":"Paramount Pictures","Website":"http://www.titanicmovie.com/","Response":"True"}

        self.assertEqual(
            MovieModel.objects.all().count(),
            1
        )
        ''' 
        Invoking the main method responsible for
        fetching the information from external API
        with the usage of POST request
        '''

        test_payload = {
            "title": test_mockResponse["Title"]
        }

        resp = self.client.post(
            "/movies/",
            data=test_payload,
            format='json'
        )

        self.assertTrue(
            resp.data['title'],
            test_mockResponse["Title"]
        )


        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK
        )

        '''
        Validating, whether the entire procedure of
        receiving the data has been realized in
        an expected way or not
        '''

        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(
            "/movies/"
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )


        self.assertTrue(
            resp.data[0]['title'],
            test_mockResponse["Title"]
        )

        self.assertEqual(
            MovieModel.objects.all().count(),
            2
        )



    def test_fetch_movie_information_using_external_api_wrong_title(self):
        # Preparing mock data
        test_mockResponse = {"Title":"Titanic","Year":"1997","Rated":"PG-13","Released":"19 Dec 1997","Runtime":"194 min","Genre":"Drama, Romance","Director":"James Cameron","Writer":"James Cameron","Actors":"Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates","Plot":"A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.","Language":"English, Swedish, Italian","Country":"USA","Awards":"Won 11 Oscars. Another 111 wins & 77 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.8/10"},{"Source":"Rotten Tomatoes","Value":"89%"},{"Source":"Metacritic","Value":"75/100"}],"Metascore":"75","imdbRating":"7.8","imdbVotes":"946,032","imdbID":"tt0120338","Type":"movie","DVD":"10 Sep 2012","BoxOffice":"N/A","Production":"Paramount Pictures","Website":"http://www.titanicmovie.com/","Response":"True"}
        test_wrongTitleData = "TestDataWrong"
        '''
        Invoking the main method responsible for
        fetching the information from external API
        with the usage of POST request
        '''

        test_payload = {
            "title": format(test_wrongTitleData)
        }

        resp = self.client.post(
            "/movies/",
            data=test_payload,
            format='json'
        )

        self.assertEqual(
            resp.status_code,
            status.HTTP_404_NOT_FOUND
        )

        '''
        Validating, whether the entire procedure of
        receiving the data has been realized in
        an expected way or not
        '''

        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(
            "/movies/"
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            MovieModel.objects.all().count(),
            1
        )
