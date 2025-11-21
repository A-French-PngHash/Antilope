from django.db import connection,transaction
from ..models import *
from .claim_finder import *
import numpy as np

def insert_tiles(user : User, activity : Activity, tiles : np.array):
    cursor = connection.cursor()
    query = """INSERT INTO Tile (x, y, activity_id) VALUES (%s, %s, %s)"""
    query_list = [tuple(tile[0], tile[1], activity.id) for tile in tiles]

    cursor.executemany(query, query_list)
    transaction.commit()
    cursor.close()

