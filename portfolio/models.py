
from unicodedata import name
from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name