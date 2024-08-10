from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Type of object for finding the table
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID for finding the record, (This is not work for the tables that their pks not a number)
    object_id = models.PositiveIntegerField()
    # Actual object
    content_object = GenericForeignKey()
