from django.conf import settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import list_route, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import filters

from apps.comments.models import *
from apps.comments.serializers import *
from apps.misc.logger import *
from django.db.models import Q
import datetime

logger = logging.getLogger(__name__)
logger.addHandler(handler)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (JSONParser,)
    serializer_class = CommentModelExtendedSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = CommentModel.objects.all()
        movieId = self.request.query_params.get('ID', None)

        if movieId is not None:
            queryset = queryset.filter(
                movie__id=movieId
            )

        return queryset


class TopRatedMovies(APIView):
    """
    View to list movies with the biggest amount of
    linked comments
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        '''
            Filtering for movies with at least one comment
        '''


        START_DATE = request.POST.get(
            'START_DATE',
            '01 Jan 1990'
        )

        END_DATE = request.POST.get(
            'END_DATE',
            '01 Jan 2999'
        )

        if(START_DATE != None
            and END_DATE != None):


            # "%d %b %Y"
            # "%m/%d/%Y"
            # YYYY - MM - DD

            START_DATE = datetime.datetime.strptime(
                START_DATE
                ,
                "%d %b %Y"
            )

            END_DATE  = datetime.datetime.strptime(
                END_DATE
                ,
                "%d %b %Y"
            )

        sortedList = []

        # making a simple sorting DO IT WITH YELD !!
        for queriedObject in MovieModel.objects.all():

            if(
                len(
                    sortedList
                ) > 0
            ):

                flag = False
                for idx, val in enumerate(sortedList):

                    if(el.commented_movies.all().count() == queriedObject.commented_movies.all().count()):
                        sortedList.insert(
                            idx,
                            {
                                "movie_id": queriedObject['id'],
                                "total_comments": queriedObject.commented_movies.all().count(),
                                "rank": el['rank']
                            }
                        )
                        break

                    elif(el.commented_movies.all().count() < queriedObject.commented_movies.all().count()):
                        continue
                    else:
                        idx = idx > 0 and idx or 0
                        sortedList.insert(
                            idx,
                            {
                                "movie_id": queriedObject.id,
                                "total_comments": queriedObject.commented_movies.all().count(),
                                "rank": el['rank']
                            }
                        )

            else:

                sortedList.append(
                    {
                        "movie_id": queriedObject.id,
                        "total_comments": queriedObject.commented_movies.all().count(),
                        "rank": 0
                    }
                )





        serializer = MovieModelSerializer(
            MovieModel.objects.all(),
            many=True
        )

        return Response(serializer.data)
