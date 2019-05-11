from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from apps.movies.tasks import *
from apps.movies.serializers import *
from apps.movies.models import *
from rest_framework import viewsets, status


class MovieModelAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of all Movies.
        """

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
            if ('title' in request.POST):
                data = processMovieObject(
                    request.POST.get(
                        'title',
                        ''
                    )
                )
                return Response(
                    MovieModelSerializer(
                        data,
                        many=False
                    ).data
                )

        except Exception as e:
            logger.error(
                "Something unexpected happened when in: MovieModelAPIView-post:"
                + '\n'
                + str(e)
            )

        return Response(status=status.HTTP_404_NOT_FOUND)
