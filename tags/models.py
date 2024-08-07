from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type of object for finding the table
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID for finding the record, (This is not work for the tables that their pks not a number)
    object_id = models.PositiveIntegerField()
    # Actual object
    content_object = GenericForeignKey()
