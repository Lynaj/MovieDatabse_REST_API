from uuid import uuid4

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.misc.logger import *

# +++++++++++++++++++++++++++++++++++
logger = logging.getLogger(__name__)
logger.addHandler(handler)
# +++++++++++++++++++++++++++++++++++

class RatingModel(models.Model):
    source = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    value = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

class LanguageModel(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

class ActorModel(models.Model):
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

class MovieModel(models.Model):
    title = models.CharField(
        verbose_name="Umiejętności Oferty",
        max_length=200,
        null=False,
        blank=False,
        unique=True
    )

    year = models.IntegerField(
        blank=True,
        default=0,
        null=True,
        verbose_name='Oczekiwane Zarobki'
    )

    rated = models.CharField(
        verbose_name="Umiejętności Oferty",
        max_length=200,
        null=True,
        blank=True
    )

    released = models.DateTimeField(
        verbose_name='Registered at',
        default=timezone.now
    )

    runtime = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    genre = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    director = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    writer = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    actors = models.ManyToManyField(
        ActorModel,
        blank=True
    )

    plot = models.CharField(
        max_length=2000,
        null=True,
        blank=True
    )

    language = models.ManyToManyField(
        LanguageModel,
        blank=True
    )

    country = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    awards = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    poster = models.URLField()

    ratings = models.ManyToManyField(
        RatingModel,
        blank=True
    )

    metascore = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    imdb_rating = models.DecimalField(
        default=0.0,
        max_digits=3,
        decimal_places=2
    )

    imdb_votes = models.DecimalField(
        default=0.0,
        max_digits=20,
        decimal_places=5
    )

    imbd_id = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    type = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    dvd = models.DateTimeField(
        verbose_name='DVD release date',
        null=True,
        blank=True
    )

    box_office = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    production = models.CharField(
        verbose_name="Umiejętności Oferty",
        max_length=200,
        null=True,
        blank=True
    )

    website = models.URLField()

    response = models.BooleanField(
        default=False
    )
