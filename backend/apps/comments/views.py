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

    def get_queryset(self):
        queryset = MovieModel.objects.all()
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
    authentication_classes = ()
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, format=None):
        '''
            Filtering for movies with at least one comment
        '''


        START_DATE = request.POST.get(
            'START_DATE',
            '01/01/1990'
        )

        END_DATE = request.POST.get(
            'END_DATE',
            '01/01/2999'
        )

        if(START_DATE != None
            and END_DATE != None):

            START_DATE = datetime.datetime.strptime(
                START_DATE
                ,
                "%m/%d/%y"
            )

            END_DATE  = datetime.datetime.strptime(
                END_DATE
                ,
                "%m/%d/%y"
            )

        queriedObjects = []
        for obj in MovieModel.objects.all():
            obj['comments'] = obj.commented_movies.all().count()
            queriedObjects.append(
                obj
            )

        sortedList = []

        # making a simple sorting DO IT WITH YELD !!
        for queriedObject in queriedObjects:

            if(
                len(
                    sortedList
                ) > 0
            ):

                flag = False
                for idx, val in enumerate(sortedList):

                    if(el['comments'] == queried['comments']):
                        sortedList.insert(
                            idx,
                            {
                                "movie_id": queried['id'],
                                "total_comments": queried['comments'],
                                "rank": el['rank']
                            }
                        )
                        break

                    elif(el['comments'] < queried['comments']):
                        continue
                    else:
                        idx = idx > 0 and idx or 0
                        sortedList.insert(
                            idx,
                            {
                                "movie_id": queried['id'],
                                "total_comments": queried['comments'],
                                "rank": el['rank']
                            }
                        )

            else:

                sortedList.insert(
                    idx,
                    {
                        "movie_id": queried['id'],
                        "total_comments": queried['comments'],
                        "rank": 0
                    }
                )





        serializer = MovieModelSerializer(
            MovieModel.objects.all(),
            many=True
        )

        return Response(serializer.data)





    def post(self, request, format=None):
        """
        Fetches data connected with
        given movie ( basing on Title )
        """
        try:

            if('title' in request.POST):
                data = processMovieObject(
                    request.POST.get(
                        'title',
                        ''
                    )
                )

            else:
                data = MovieModel.objects.none()

        except Exception as e:
            logger.error(
                "Something unexpected happened when in: MovieModelAPIView-post:"
                + '\n'
                + str(e)
            )

            data = MovieModel.objects.none()

        return Response(
            MovieModelSerializer(
                data,
                many=False
            )
        )
