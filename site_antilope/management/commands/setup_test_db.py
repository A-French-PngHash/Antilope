from site_antilope.serializer import UserSerializer
from site_antilope.services import *
from django.core.management.base import BaseCommand, CommandError
from site_antilope.services import *
from pathlib import Path
from django.conf import settings
import time
from django.contrib.auth.models import UserManager
class Command(BaseCommand):
    """ 
    This creates a piece of code that can be run with : python manage.py setup_test_db.

    When executing this command, the code inside handle is launched. The benefit of launching code like that is that we have an access to the database.
    """
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        DELETE FROM site_antilope_tile;
        DELETE FROM site_antilope_tileoperation;
        DELETE FROM site_antilope_activity;
        DELETE FROM site_antilope_user;
        """
        try:
            alice = User.objects.get(username='alice.chaise')        
        except User.DoesNotExist:
            print("creating alice")
            alice = User(name="alice", surname="chaise", username="alice.chaise")
            alice.save()
            raid24 = Group(user=alice, group="raid24")
            raid24.save()
        
        try:
            bob = User.objects.get(username='bob.table')        
        except User.DoesNotExist:
            print("creating bob")
            bob = User(name="bob", surname="table", username="bob.table")
            raid23 = Group(user=bob, group = "raid23")
            bob.save()
            raid23.save()
        
        
        files = ["site_antilope/services/test_gpx_file/activity_21016356115.gpx", "site_antilope/services/test_gpx_file/bouclevelo.gpx"]
        users = [bob, alice]
        for i in range(len(files)):

            activity = Activity.objects.get(id=i+3)
            print(activity)
            trace = Trace.from_gpx(files[i])
            claim_finder = ClaimFinder(trace)
            claim_tiles(alice, activity, claim_finder.get_all_tiles_to_claim())
        
        