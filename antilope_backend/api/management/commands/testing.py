from api.services import *
from django.core.management.base import BaseCommand, CommandError
from api.services import *
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        trace = Trace.from_gpx(str(settings.BASE_DIR) + "/api/services/test_file/activity_20978283261.gpx")
        claim_finder = ClaimFinder(trace)
        tiles = claim_finder.get_inside_points(claim_finder.trace.points)
        user = User.objects.get(name="Titou")#.filter(surname="Titou")
        print(user)
        print(tiles)
        