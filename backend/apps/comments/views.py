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
    permission_classes = (permissions.AllowAny,)
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


        START_DATE = datetime.datetime.strptime(
            request.GET.get(
                'START_DATE',
                '01 Jan 1990'
            ),
            "%d %b %Y"
        )

        END_DATE = datetime.datetime.strptime(
            request.GET.get(
                'END_DATE',
                '01 Jan 2999'
            ),
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
                initialSortedList = sortedList.copy()
                flag = False
                for idx, el in enumerate(initialSortedList):


                    if(el["total_comments"] == queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count()):
                        sortedList.insert(
                            idx,
                            {
                                "movie_id": queriedObject.id,
                                "total_comments": queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count(),
                                "rank": el['rank']
                            }
                        )
                        break

                    elif(idx == len(sortedList) - 1):

                        sortedList.append(
                            {
                                "movie_id": queriedObject.id,
                                "total_comments": queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count(),
                                "rank": int(sortedList[idx]['rank']) + 1
                            }
                        )

                    elif(el["total_comments"] > queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count()):
                        idx = idx > 0 and idx or 0
                        rank = el['rank'] > 0 and el['rank'] - 1or 0
                        item = {
                            "movie_id": queriedObject.id,
                            "total_comments": queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count(),
                            "rank": rank
                        }

                        sortedList.insert(
                            idx,
                            item
                        )

            else:

                sortedList.append(
                    {
                        "movie_id": queriedObject.id,
                        "total_comments": queriedObject.commented_movies.filter(created_at__range=[START_DATE, END_DATE]).count(),
                        "rank": 0
                    }
                )


        return Response(sortedList)
