
from site_antilope.services import *
from django.core.management.base import BaseCommand, CommandError
from site_antilope.services import *
from pathlib import Path
from django.conf import settings
from datetime import datetime, timezone
from site_antilope.services.db import *

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
        user = User.objects.get(name="Titou")#.filter(surname="Titou")
        get_tile_data_inside((-10, 10), (10, -10), "raid24", "raid23")

        #activity = Activity(user=user, filename="testing", date_added = datetime.now(timezone.utc))

        #create_user_db("tyméo", "thomas", groups=["famille"])

        #activity.save()
        #tiles = claim_finder.get_all_tiles_to_claim()
        #print(tiles)
        #claim_finder.display_tiles_and_trace(tiles)
        