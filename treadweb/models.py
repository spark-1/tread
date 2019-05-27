from django.db import models

# Create your models here.
class Keyword(models.Model):
    age = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
