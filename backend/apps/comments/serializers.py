from rest_framework import serializers
from django.conf import settings
from apps.movies.serializers import *
from apps.comments.models import *


class CommentModelExtendedSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = [
            'movie',
            'content'
        ]

    def get_movie(self, queriedObject):
        movie_id = queriedObject.movie.id
        return movie_id


