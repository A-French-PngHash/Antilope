from django.db import connection,transaction
from ..models import *
from .claim_finder import *
import numpy as np

def claim_tiles(user : User, activity : Activity, tiles : np.array):
    """
    Updates and adds the correct rows in the database to make the `user` claim the supplied `tiles`.
    """
    cursor = connection.cursor()

    # Add a tile operation for every modified tile
    query_tileop = """INSERT INTO api_tileoperation (x, y, activity_id) VALUES (%s, %s, %s)"""
    query_tileop_list = [(int(tile[0]), int(tile[1]), int(activity.id)) for tile in tiles]
    cursor.executemany(query_tileop, query_tileop_list)

    # Insert every missing tile with nb_passage = 0
    query_tile = """
    INSERT OR IGNORE INTO api_tile (x, y, user_id, nb_passage)
    VALUES (%s, %s, %s, 0)"""    
    query_tile_list = [(int(tile[0]), int(tile[1]), int(user.id)) for tile in tiles]
    cursor.executemany(query_tile, query_tile_list)

    # Adds one to every tile.
    query_update = """ UPDATE api_tile SET nb_passage = nb_passage + 1 WHERE x = %s AND y = %s;"""
    query_update_list = [(int(tile[0]), int(tile[1])) for tile in tiles]
    cursor.executemany(query_update, query_update_list)

    transaction.commit()
    cursor.close()

