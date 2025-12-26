from site_antilope.services import *
from django.core.management.base import BaseCommand, CommandError
from site_antilope.services import *
from pathlib import Path
from django.conf import settings
import time

class Command(BaseCommand):
    """ 
    This creates a piece of code that can be run with : python manage.py setup_test_db.

    When executing this command, the code inside handle is launched. The benefit of launching code like that is that we have an access to the database.
    """
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        alice = User(name="Alice", surname = "Eve")
        bob = User(name="Mickael", surname = "Mo")
        raid23 = Group(user=alice, group = "raid23")
        raid24 = Group(user=bob, group="raid24")

        activity = Activity(user = alice, gpx_file="")
        claim_tiles(alice, )
        