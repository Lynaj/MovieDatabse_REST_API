import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from apps.comments.models import *
from apps.movies.models import *

import json
import os
import codecs

class CommentViewSetTestCase(APITestCase):
    url_get = reverse("api:comments-get")
    url_post = reverse("api:comments-create")

    def setUp(self):
        # Prepating movie's model data
        self.test_Title = "Guardians of the Galaxy Vol. 2"
        self.test_Year = "2017"
        self.test_Rated = "PG-13"
        self.test_Released = "05 May 2017"
        self.test_Runtime = "136 min"
        self.test_Genre = "Action, Adventure, Comedy, Sci-Fi"
        self.test_Director = "James Gunn"
        self.test_Writer = "James Gunn, Dan Abnett (based on the Marvel comics by), Andy Lanning (based on the Marvel comics by), Steve Englehart (Star-Lord created by), Steve Gan (Star-Lord created by), Jim Starlin (Gamora and Drax created by), Stan Lee (Groot created by), Larry Lieber (Groot created by), Jack Kirby (Groot created by), Bill Mantlo (Rocket Raccoon created by), Keith Giffen (Rocket Raccoon created by), Steve Gerber (Howard the Duck created by), Val Mayerik (Howard the Duck created by)"
        self.test_Plot = "The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father the ambitious celestial being Ego."
        self.test_Country = "USA"
        self.test_Awards = "Nominated for 1 Oscar. Another 12 wins & 42 nominations."
        self.test_Poster = "https://m.media-amazon.com/images/M/MV5BMTg2MzI1MTg3OF5BMl5BanBnXkFtZTgwNTU3NDA2MTI@._V1_SX300.jpg"
        self.test_imdbRating = "7.7"
        self.test_imdbVotes = "471,312"
        self.test_imdbID = "tt3896198"
        self.test_Type = "movie"
        self.test_DVD = "22 Aug 2017"
        self.test_Metascore = "67"
        self.test_BoxOffice = "$389,804,217"
        self.test_Production = "Walt Disney Pictures"
        self.test_Website = "https://marvel.com/guardians"
        self.test_Response = True
        self.number_of_created_comments = 5
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
            plot=self.test_Plot,
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

        self.test_content = "Test Content"

        # Creating comments
        self.list_of_comments = []

        for x in range(self.number_of_created_comments):
            self.list_of_comments.append(
                CommentModel.objects.create(
                    movie=self.created__movie_model,
                    content=self.test_content+str(x)
                )
            )

    def test_CommentViewSet_ID_not_included(self):
        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(
            url_get
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            self.number_of_created_comments
        )

    def test_CommentViewSet_ID_included(self):
        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(url_get, {
                "ID": str(
                    self.list_of_comments[0].id
                )
            }
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            1
        )

        self.assertEqual(
            len(
                self.results
            ),
            1
        )

        # validating data ( movie ID )
        self.assertEqual(
            self.results[0]["movie"]
            ,
            self.list_of_comments[0].id
        )

    def test_CommentViewSet_ID_included_but_not_existing(self):
        # Calling Endpoint containg list of Movies ( potentially )
        resp = self.client.get(url_get, {
                "ID": "5123123123"
            }
        )

        self.assertEqual(
            resp.status_code, status.HTTP_404_NOT_FOUND
        )

class TopRatedtViewSetTestCase(APITestCase):

    url_get = reverse("api-top-rated-movies")

    def setUp(self):
        # Prepating movie's model data
        self.test_Title = "Guardians of the Galaxy Vol. 2"
        self.test_Year = "2017"
        self.test_Rated = "PG-13"
        self.test_Released = "05 May 2017"
        self.test_Runtime = "136 min"
        self.test_Genre = "Action, Adventure, Comedy, Sci-Fi"
        self.test_Director = "James Gunn"
        self.test_Writer = "James Gunn, Dan Abnett (based on the Marvel comics by), Andy Lanning (based on the Marvel comics by), Steve Englehart (Star-Lord created by), Steve Gan (Star-Lord created by), Jim Starlin (Gamora and Drax created by), Stan Lee (Groot created by), Larry Lieber (Groot created by), Jack Kirby (Groot created by), Bill Mantlo (Rocket Raccoon created by), Keith Giffen (Rocket Raccoon created by), Steve Gerber (Howard the Duck created by), Val Mayerik (Howard the Duck created by)"
        self.test_Plot = "The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father the ambitious celestial being Ego."
        self.test_Country = "USA"
        self.test_Awards = "Nominated for 1 Oscar. Another 12 wins & 42 nominations."
        self.test_Poster = "https://m.media-amazon.com/images/M/MV5BMTg2MzI1MTg3OF5BMl5BanBnXkFtZTgwNTU3NDA2MTI@._V1_SX300.jpg"
        self.test_imdbRating = "7.7"
        self.test_imdbVotes = "471,312"
        self.test_imdbID = "tt3896198"
        self.test_Type = "movie"
        self.test_DVD = "22 Aug 2017"
        self.test_Metascore = "67"
        self.test_BoxOffice = "$389,804,217"
        self.test_Production = "Walt Disney Pictures"
        self.test_Website = "https://marvel.com/guardians"
        self.test_Response = True
        self.number_of_created_comments = 5
        second_movie_model_index = 2

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
            plot=self.test_Plot,
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

        self.created__second_movie_model = MovieModel.objects.create(
            title=self.test_Title+ str(second_movie_model_index),
            year=self.test_Year + str(second_movie_model_index),
            rated=self.test_Rated + str(second_movie_model_index),
            released=self.test_Released + str(second_movie_model_index),
            runtime=self.test_Runtime + str(second_movie_model_index),
            genre=self.test_Genre + str(second_movie_model_index),
            director=self.test_Director + str(second_movie_model_index),
            writer=self.test_Writer + str(second_movie_model_index),
            plot=self.test_Plot + str(second_movie_model_index),
            country=self.test_Country + str(second_movie_model_index),
            awards=self.test_Awards + str(second_movie_model_index),
            poster=self.test_Poster + str(second_movie_model_index),
            metascore=self.test_Metascore + str(second_movie_model_index),
            imdb_rating=self.test_imdbRating + str(second_movie_model_index),
            imdb_votes=self.test_imdbVotes + str(second_movie_model_index),
            imbd_id=self.test_imdbID + str(second_movie_model_index),
            type=self.test_Type + str(second_movie_model_index),
            dvd=self.test_DVD + str(second_movie_model_index),
            box_office=self.test_BoxOffice + str(second_movie_model_index),
            production=self.test_Production + str(second_movie_model_index),
            website=self.test_Website + str(second_movie_model_index),
            response=self.test_Response + str(second_movie_model_index)
        )

        self.test_content = "Test Content"

        # Creating comments
        self.list_of_comments = []

        for x in range(self.number_of_created_comments):
            self.list_of_comments.append(
                CommentModel.objects.create(
                    movie=self.created__movie_model,
                    content=self.test_content+str(x)
                )
            )

    def test_lack_of_movies_in_the_database(self):
        CommentModel.objects.all().delete()
        MovieModel.objects.all().delete()

        # Calling Endpoint containg list of most popular movies
        resp = self.client.get(
            url_get
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            0
        )

    def test_two_movies_same_number_of_comments(self):
        number_of_movies = 2
        number_of_comments_linked_to_each_movie = 5
        # Creating MovieModels
        for x in range(number_of_movies):
            created_movie = MovieModel.objects.create(
                title=self.test_Title+str(x)
            )

            for y in range(number_of_comments_linked_to_each_movie):
                CommentModel.objects.create(
                    movie=created_movie,
                    content=self.test_content
                )

        # Calling Endpoint containg list of most popular movies
        resp = self.client.get(
            url_get
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            number_of_movies
        )

        '''
            Validating number of comments
            as well, as value of the rank & movie_id
        '''
        list_of_movie_models_ID = list(map(lambda x: x.id, MovieModel.objects.all()))
        for movie in self.results:
            self.assertEqual(
                str(
                    movie["rank"]
                ),
                "0"
            )

            self.assertTrue(
                movie["movie_id"] in list_of_movie_models_ID ,
            )

            self.assertEqual(
                str(
                    movie["total_comments"]
                ),
                number_of_comments_linked_to_each_movie
            )


    def test_five_movies_each_having_zero_comments(self):
        number_of_movies = 2
        number_of_comments_linked_to_each_movie = 0
        # Creating MovieModels
        for x in range(number_of_movies):
            created_movie = MovieModel.objects.create(
                title=self.test_Title + str(x)
            )

            for y in range(number_of_comments_linked_to_each_movie):
                CommentModel.objects.create(
                    movie=created_movie,
                    content=self.test_content
                )

        # Calling Endpoint containg list of most popular movies
        resp = self.client.get(
            url_get
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            number_of_movies
        )

        '''
            Validating number of comments
            as well, as value of the rank & movie_id
        '''
        list_of_movie_models_ID = list(map(lambda x: x.id, MovieModel.objects.all()))
        for movie in self.results:
            self.assertEqual(
                str(
                    movie["rank"]
                ),
                "0"
            )

            self.assertTrue(
                movie["movie_id"] in list_of_movie_models_ID,
            )

            self.assertEqual(
                str(
                    movie["total_comments"]
                ),
                number_of_comments_linked_to_each_movie
            )

    def test_five_movies_different_number_of_comments(self):
        number_of_movies = 15
        number_of_comments_linked_to_each_movie__array = [x for x in range(15)]
        # Creating MovieModels
        for x in number_of_movies:
            created_movie = MovieModel.objects.create(
                title=self.test_Title + str(x)
            )

            for y in range(number_of_comments_linked_to_each_movie__array[x]):
                CommentModel.objects.create(
                    movie=created_movie,
                    content=self.test_content
                )

        # Calling Endpoint containg list of most popular movies
        resp = self.client.get(
            url_get
        )

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )

        self.assertTrue(
            'results' in resp.data
        )

        self.results = resp.data['results']

        # Validating number of records
        self.assertEqual(
            len(
                self.results
            ),
            number_of_movies
        )

        '''
            Validating number of comments
            as well, as value of the rank & movie_id
        '''
        list_of_movie_models_ID = list(map(lambda x: x.id, MovieModel.objects.all()))
        for (index, movie) in enumerate(self.results):
            self.assertEqual(
                str(
                    movie["rank"]
                ),
                str(index)
            )

            self.assertTrue(
                movie["movie_id"] in list_of_movie_models_ID,
            )

            self.assertEqual(
                str(
                    movie["total_comments"]
                ),
                number_of_comments_linked_to_each_movie__array[index]
            )
