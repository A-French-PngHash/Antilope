from datetime import datetime, timezone
from django.db import connection,transaction
from django.db.models import Q, Count, Sum
from ...models import *


def get_tile_data_inside(point1 : tuple[int, int],point2 : tuple[int, int], group : str):
    """
    Returns the data inside the rectangle defined by (point1, point2).

    Users are part of groups. The groups of a user can be represented as a set of strings : S = {s1, s2, ...}.
    S is not empty because "{user.name}.{user.surname}" is in S : every user is in the group containing only himself.
    The idea is that the map displayed on the site is two (or more groups) fighting for territory.
    
    :param point1: Top left point.
    :param point2: Bottom right point.
    :param group: Name of the second group.
    """
    tiles = (Tile.objects.filter(
        x__gte=point1[0],
        x__lte=point2[0],
        y__gte=point2[1],
        y__lte=point1[1],
    )

    
    .filter(
        Q(user__group__group=group)
    )
    .values('x', 'y')
    .annotate(total_passage=Sum('nb_passage')))
    # Tiles is now a query set where each result is {'x': 0, 'y': 0, 'total_passage': 7}
    return tiles