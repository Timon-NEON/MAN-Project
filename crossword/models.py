from django.db import models

class Crosswords(models.Model):
    name = models.CharField(max_length=64)
    crossword = models.CharField(max_length=131072)
    describe = models.CharField(max_length=131072)
    link = models.CharField(max_length=64, unique=True)
    creator_id = models.IntegerField()
    posting_time = models.IntegerField(default=0)
    status = models.CharField(max_length=1)
    language = models.CharField(max_length=25)
    

class Users(models.Model):
    user_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    crosswords_id = models.CharField(max_length=10000)
    sign_up_time = models.CharField(max_length=30)
