from apps.movies.models import *
from apps.misc.logger import *

from django.conf import settings

import datetime
import requests
import json

# +++++++++++++++++++++++++++++++++++
logger = logging.getLogger(__name__)
logger.addHandler(handler)


# +++++++++++++++++++++++++++++++++++


def processRequest(requestURL):
    GET_request_obtained_data = []
    try:
        GET_request_processed = requests.get(
            url=requestURL
        )
    except requests.exceptions.Timeout:
        logger.error(
            "***[EXCEPTION]*** [processRequest] Request Timeout"
        )
    except requests.exceptions.TooManyRedirects:
        logger.error(
            "***[EXCEPTION]*** [processRequest] Request TooManyRedirects"
        )
    except requests.exceptions.RequestException as e:
        logger.error(
            "***[EXCEPTION]*** [processRequest] Request RequestException"
            + '\nError: '
            + str(e)
        )
    except Exception as e:
        logger.error("***[EXCEPTION]*** [processRequest] Request Exception"
                     + '\nError: '
                     + str(e)
                     )
    else:
        GET_request_obtained_data = GET_request_processed.text
    finally:
        return GET_request_obtained_data


def processMovieObject(title):
    request_URL = "http://www.omdbapi.com/?t={0}&apikey={1}".format(
        title,
        settings.OMDBAPI_KEY
    )

    try:
        request_response = json.loads(
            processRequest(
                request_URL
            )
        )


    except Exception as e:
        logger.error("***[EXCEPTION]*** [processMovieObject] Error Happened when unpacking JSON array"
                 + '\nError: '
                 + str(e)
                 )

    '''
    Determining, whether queried Title is a correct one
    and exists in the external's API database
    '''
    if (
        len(
            request_response
        ) > 0
        and
        "Title" in request_response
        and
        request_response["Title"] == title
    ):
        '''
        Checking the existence of particular Title
        on the Application's local database
        '''



        queried__movie = MovieModel.objects.filter(
            title=title
        )

        if (
            queried__movie.count() > 0
        ):
            # Updating existing movie object
            queried__movie.update(
                title=request_response["Title"],
                year=request_response["Year"],
                rated=request_response["Rated"],
                released=datetime.datetime.strptime(
                    request_response["Released"]
                    ,
                    "%d %b %Y"
                ),
                runtime=request_response["Runtime"],
                genre=request_response["Genre"],
                director=request_response["Director"],
                writer=request_response["Writer"],
                plot=request_response["Plot"],
                country=request_response["Country"],
                awards=request_response["Awards"],
                poster=request_response["Poster"],
                metascore=request_response["Metascore"],
                imdb_rating=request_response["imdbRating"],
                imdb_votes=request_response["imdbVotes"].replace(",", "."),
                imbd_id=request_response["imdbID"],
                type=request_response["Type"],
                dvd=datetime.datetime.strptime(
                    request_response["DVD"]
                    ,
                    "%d %b %Y"
                ),
                box_office=request_response["BoxOffice"],
                production=request_response["Production"],
                website=request_response["Website"]
            )

            '''
            REMEMBER TO CHECK WHETHER
            PARTICULAR LANGUAGE / ACTOR ETC EXISTS OR NOT
            '''

            # Filtering unecessary actors / languages / reviews
            filtered_languages = filter(
                lambda x: x not in list(
                    map(
                        lambda y: y.name
                        ,
                        queried__movie.language
                    )
                )
                ,
                request_response["Language"].split(", ")
            )

            request_response["Language"] = filtered_languages

            filtered_actors = filter(
                lambda x: x not in list(
                    map(
                        lambda y: (y.first_name + " " + y.last_name)
                        ,
                        queried__movie.actors
                    )
                )
                ,
                request_response["Actors"].split(", ")
            )

            request_response["Language"] = filtered_actors

            filtered_ratings = filter(
                lambda x: x["Source"] not in list(
                    map(
                        lambda y: y.source
                        ,
                        queried__movie.ratings
                    )
                )
                ,
                request_response["Ratings"]
            )

            request_response["Language"] = filtered_ratings

        else:
            # Creating a completely new Movie object
            queried__movie = MovieModel.objects.create(
                title=request_response["Title"],
                year=request_response["Year"],
                rated=request_response["Rated"],
                released=datetime.datetime.strptime(
                    request_response["Released"]
                    ,
                    "%d %b %Y"
                ),
                runtime=request_response["Runtime"],
                genre=request_response["Genre"],
                director=request_response["Director"],
                writer=request_response["Writer"],
                plot=request_response["Plot"],
                country=request_response["Country"],
                awards=request_response["Awards"],
                poster=request_response["Poster"],
                metascore=request_response["Metascore"],
                imdb_rating=request_response["imdbRating"],
                imdb_votes=request_response["imdbVotes"].replace(",", "."),
                imbd_id=request_response["imdbID"],
                type=request_response["Type"],
                dvd=datetime.datetime.strptime(
                    request_response["DVD"]
                    ,
                    "%d %b %Y"
                ),
                box_office=request_response["BoxOffice"],
                production=request_response["Production"],
                website=request_response["Website"]
            )

        # Adding Languages
        for language in request_response["Language"].split(", "):
            queried__movie.language.add(
                LanguageModel.objects.create(
                    name="language"
                )
            )

        # Adding Actors
        for actor_name in request_response["Actors"].split(", "):
            first_name, last_name = actor_name.split(" ")
            queried__movie.actors.add(
                ActorModel.objects.create(
                    first_name=first_name,
                    last_name=last_name
                )
            )

        # Adding Ratings
        for rating in request_response["Ratings"]:
            queried__movie.ratings.add(
                RatingModel.objects.create(
                    source=rating["Source"],
                    value=rating["Value"]
                )
            )

        return queried__movie

    return MovieModel.objects.none()
