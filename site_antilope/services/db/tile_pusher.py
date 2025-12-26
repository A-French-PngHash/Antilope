from datetime import datetime, timezone
from django.db import connection,transaction
from django.db.models import Q, Count, Sum
from itertools import islice

from ...models import *
from ..claim_finder import *
import numpy as np

def claim_tiles(user : User, activity : Activity, tiles : np.array):
    """
    Updates and adds the correct rows in the database to make the `user` claim the supplied `tiles`.
    """
    cursor = connection.cursor()

    def chunked(iterable, size):
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    # Add a tile operation for every modified tile
    query_tileop = """INSERT INTO site_antilope_tileoperation (x, y, activity_id) VALUES {}"""
    query_tileop_list = [(int(tile[0]), int(tile[1]), int(activity.id)) for tile in tiles]
    
    for batch in chunked(query_tileop_list, 1000): # executing by batch because when executing with cursor.executemany it is very slow.
        placeholders = ",".join(["(%s,%s,%s)"] * len(batch))
        flat_values = [v for row in batch for v in row]
        cursor.execute(query_tileop.format(placeholders), flat_values)
    
    # Insert every missing tile with nb_passage = 1 and updates the existing one by adding 1.
    query_tile = """
    INSERT INTO site_antilope_tile (x, y, user_id, last_update, nb_passage)
    VALUES {} 
    ON CONFLICT(x, y, user_id) DO UPDATE SET
     nb_passage = nb_passage + 1, last_update = %s;"""
    query_tile_list = [(int(tile[0]), int(tile[1]), int(user.id), datetime.now(timezone.utc)) for tile in tiles]
    
    for batch in chunked(query_tile_list, 1000):
        placeholders = ",".join(["(%s,%s,%s, %s, 1)"] * len(batch))
        flat_values = [v for row in batch for v in row]
        flat_values.append(datetime.now(tz=timezone.utc))
        cursor.execute(query_tile.format(placeholders), flat_values)

    transaction.commit()
    cursor.close()

    

