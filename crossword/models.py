from django.db import models

class Crosswords(models.Model):
    name = models.CharField(max_length=64)
    crossword = models.CharField(max_length=131072)
    describe = models.CharField(max_length=131072)
    link = models.CharField(max_length=64, unique=True)
    creator_id = models.IntegerField()
    status = models.CharField(max_length=1)
    language = models.CharField(max_length=5)
    

class Users(models.Model):
    user_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, null=True)
    sign_up_time = models.CharField(max_length=30)
