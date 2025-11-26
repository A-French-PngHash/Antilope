from api.services import *
from django.core.management.base import BaseCommand, CommandError
from api.services import *
from pathlib import Path
from django.conf import settings
import time

class Command(BaseCommand):
    """ 
    This creates a piece of code that can be run with : python manage.py testing.

    When executing this command, the code inside handle is launched. The benefit of launching code like that is that we have an access to the database.
    """
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        trace = Trace.from_gpx(str(settings.BASE_DIR) + "/api/services/test_gpx_file/bouclevelo.gpx")
        claim_finder = ClaimFinder(trace)
        print("starting", flush=True)
        now = time.time()
        tiles = claim_finder.get_all_tiles_to_claim()
        then = time.time()
        print(then - now)
        #user = User.objects.get(name="Titou")#.filter(surname="Titou")
        
        print(tiles)
        claim_finder.display_tiles_and_trace(tiles)
        