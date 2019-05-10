from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from apps.movies.tasks import *

class MovieModelAPIView(APIView):
    """
    View to list Movies stored in the DB
    as well as to fetch information about a new one
    """
    authentication_classes = (,)
    permission_classes = (
        permissions.AllowAny,
    )

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