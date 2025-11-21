from django.db import models

# Create your models here.

# Set up the database

class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    ban = models.BooleanField(default=False)

    def __str__(self):
        return self.surname + self.name
    
class Tile(models.Model):
    """ 
    An object to store the number of times a tile has been claimed by the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nb_passage = models.IntegerField()
    x = models.IntegerField() # Tile location is (n, m) with n and m integers
    y = models.IntegerField()

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=40)
    date_added = models.DateTimeField()


class TileOperation(models.Model):
    """
    An object like this is created every time a tile gets a +1
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    x = models.IntegerField() # Tile location is (n, m) with n and m integers
    y = models.IntegerField()

