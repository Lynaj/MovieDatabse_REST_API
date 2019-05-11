from uuid import uuid4

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.misc.logger import *
from apps.movies.models import *

# +++++++++++++++++++++++++++++++++++
logger = logging.getLogger(__name__)
logger.addHandler(handler)
# +++++++++++++++++++++++++++++++++++

class CommentModel(models.Model):
    movie = models.ForeignKey(
        MovieModel,
        on_delete=models.CASCADE,
        null=True,
        related_name="commented_movies"
    )

    content = models.TextField(
        max_length=500,
        default=''
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False
    )
