from django.db import models

# Create your models here.

# Set up the database

class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    ban = models.BooleanField()

    def __str__(self):
        return self.surname + self.name
    
class Tile(models.Model):
    user = models.ForeignKey(User)
    nb_passage = models.IntegerField()
    x = models.IntegerField() # Tile location is (n, m) with n and m integers
    y = models.IntegerField()

class Activity(models.Model):
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=40)
    date_added = models.DateTimeField()