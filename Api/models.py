from django.db import models


class History(models.Model):
    file_name = models.CharField(max_length=255)
    percent = models.FloatField(default=0)
    book_id = models.CharField(max_length=255)
    obid = models.CharField(max_length=255)
    objects = models.Manager()
