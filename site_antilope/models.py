import os
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# Set up the database

class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    ban = models.BooleanField(default=False)

    def __str__(self):
        return self.surname + self.name
    
    def get_groups(self):
        groups = Group.objects.get(user=self)
        return groups
    
    def add_groups(self, groups:list[str]):
        objs = [Group(user=self, group = g) for g in groups]
        Group.objects.bulk_create(objs)
    
class Tile(models.Model):
    """ 
    An object to store the number of times a tile has been claimed by the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nb_passage = models.IntegerField()
    x = models.IntegerField() # Tile location is (n, m) with n and m integers
    y = models.IntegerField()
    last_update = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["x", "y", "user_id"], name="unique_tile_xyuserid")
        ]

def update_filename(instance, filename):
    path = "upload/gpx_files/"
    print(instance)
    format = instance.user_id + instance.date_added + instance.file_extension
    return os.path.join(path, format)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gpx_file = models.FileField(upload_to="upload/gpx_files/")
    date_added = models.DateTimeField(auto_now_add=True)



class TileOperation(models.Model):
    """
    An object like this is created every time a tile gets a +1
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    x = models.IntegerField() # Tile location is (n, m) with n and m integers
    y = models.IntegerField()

class Group(models.Model):
    """
    Object sorting for every user, every group in which the user is.

    Users are part of groups. The groups of a user can be represented as a set of string : S = {s1, s2, ...}.
    S is not empty because "{user.name}.{user.surname}" is in S : every user is in the group containing only him.
    The idea is that the map displayed on the site is two (or more groups) fighting for territory.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=40)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "group"], name="unique_group_user_combo")
        ]

    
