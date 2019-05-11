from rest_framework import serializers
from django.conf import settings
from apps.movies.models import *


class LanguageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageModel
        fields = [
            'name'
        ]

class ActorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActorModel
        fields = [
            'first_name',
            'last_name'
        ]


class RatingModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingModel
        fields = [
            'source',
            'value'
        ]


class MovieModelSerializer(serializers.ModelSerializer):
    actors = ActorModelSerializer(
        read_only=False,
        many=True
    )
    language = LanguageModelSerializer(
        read_only=False,
        many=True
    )
    ratings = RatingModelSerializer(
        read_only=False,
        many=True
    )

    class Meta:
        model = MovieModel
        fields = [
            'title',
            'year',
            'rated',
            'released',
            'runtime',
            'genre',
            'director',
            'writer',
            'actors',
            'plot',
            'language',
            'country',
            'awards',
            'poster',
            'ratings',
            'metascore',
            'imdb_rating',
            'imdb_votes',
            'imbd_id',
            'type',
            'dvd',
            'box_office',
            'production',
            'website'
        ]
