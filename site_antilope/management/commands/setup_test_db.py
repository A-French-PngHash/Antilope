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
        try:
            alice = User.objects.get(username='alice.chaise')        
        except User.DoesNotExist:
            alice = User(name="alice", surname="chaise", username="alice.chaise")
            alice.save()
            raid24 = Group(user=bob, group="raid24")
            raid24.save()
        
        try:
            bob = User.objects.get(username='bob.table')        
        except User.DoesNotExist:
            bob = User(name="bob", surname="table", username="bob.table")
            raid23 = Group(user=alice, group = "raid23")
            raid23.save()
            bob.save()

        print("opening file")

        with open("site_antilope/services/test_gpx_file/bouclevelo.gpx") as f:
            activity = Activity.objects.get(id=1)
            print(activity)
            trace = Trace.from_gpx("site_antilope/services/test_gpx_file/bouclevelo.gpx")
            claim_finder = ClaimFinder(trace)
            print("claiming")
            claim_tiles(alice, activity, claim_finder.get_all_tiles_to_claim())
        