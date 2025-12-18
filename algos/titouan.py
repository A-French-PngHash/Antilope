import numpy as np
from matplotlib import path
from matplotlib import pyplot as plt

be_raid = [[48.710920, 2.210443]]
def gps_to_xy(cords, res):
    """
    Converts latitude and longitude coordinates to plane (x, y) coordinates.
    
    Requirements : 
        Latitude and longitude should be in degrees.
        - |lat| < 90
        - |long| < 180

    :param cords: Numpy array of shape (N, 2).
    """
    x_be = 4921.2020759 * 50
    y_be = 124516.36854561 * 50
    R = 6378000
    x = np.pi * R * cords[:, 1] / 180 - x_be
    y = R * np.log(np.tan(1/4 * np.pi + np.pi * 1/2 * cords[:, 0] / 180)) - y_be
    return np.column_stack((np.round(x / res, 2), np.round(y / res, 2)))

def point_inpoly(poly, points):
    """ 
    Checks wether (x, y) points are in the given polynom.

    Points should NOT be (latitude, longitude) pairs but instead planar coordinates.

    :param poly: Planar coordinates of the polygon (assumed to be CLOSED)
    :param points: Points to check wether they are in the polygon.
    """

    p = path.Path(list(poly.tolist()))
    return p.contains_points(points)


def get_inside_points(poly, display = True):
    """
    Returns an exhaustive list of point (in planar coordinates) that are located inside the polygon.

    :param poly: Planar coordinates of the polygon (assumed to be CLOSED)
    :param display: Displays the polygon and the 
    """
    maxx, minx = np.int64(np.ceil(poly[:, 0].max())), np.int64(np.floor(poly[:,0].min()))
    maxy, miny = np.int64(np.ceil(poly[:, 1].max())), np.int64(np.floor(poly[:, 1].min()))
    # Checks every point in the square with top left (maxx, maxy) and bottom right (minx, miny)
    x = np.linspace(minx, maxx, num=1 + maxx - minx)
    y = np.linspace(miny, maxy, num=1 + maxy - miny)

    xx, yy = np.meshgrid(x, y) 
    points = np.stack((xx, yy), axis=2)
    m, n = points.shape[0], points.shape[1]
    points = points.reshape((n* m, 2))
    result = point_inpoly(poly, points)
    print(result.shape)
    print(points.shape)

    if display:
        plt.pcolormesh(x, y, result.reshape(m, n), cmap = "Blues")
        
        plt.plot(*poly.transpose(), color="red")
        plt.axis([minx-5, maxx+5, miny-5, maxy+5])
        plt.show()
    return result

def get_points_alongside_route(path : np.array, display):
    """ 
    When a run does not form a closed loop, some segments of it are just straight lines. 
    Alongside those straight lines, the runner should claim surounding tile (in a ~100m = 2 * min_res radius)
    
    We will asume that there is at least a point every ~50m = min_res.
    :param path: List of points in planar coordinates describing the route taken by the user.
    """
    # We need to prevent the same point from appearing multiple times
    upper_left = np.column_stack((np.floor(path[:, 0]), np.ceil(path[:, 1])))
    lower_right = np.column_stack((np.ceil(path[:, 0]), np.floor(path[:, 1])))
    points = np.array([np.ceil(path), np.floor(path), upper_left, lower_right]).reshape((-1,2))
    
    if display:
        window = 5
        xmin, xmax = np.floor(np.min(path[:, 0])) - window, np.ceil(np.max(path[:, 0])) + window
        ymin, ymax = np.floor(np.min(path[:, 1])) - window, np.ceil(np.max(path[:, 1])) + window
        x = np.arange(xmin, xmax+1)
        y = np.arange(ymin, ymax+1)
        xx, yy = np.meshgrid(x, y) 
        grid = np.column_stack((xx.ravel(), yy.ravel())) # better use ravel : makes no copy (flatten makes a copy)

        selected_point = {tuple(p) for p in points}
        result = np.array([1 if tuple(p) in selected_point else 0 for p in grid])
        
        plt.pcolormesh(x, y, result.reshape(y.shape[0],x.shape[0]), cmap = "Blues")#, shading='flat')
        plt.gca().set_aspect('equal')
        plt.plot(*path.transpose(), color="red")
        plt.show()

    return np.unique(points, axis=0)
    



res = 50 # 50 mètres de résolution spatiale.

points = np.array([[48.7, 0]])


#polyx, polyy = gps_to_xy(latcord, longcord)

tour_de_lx = np.array([[48.70983862837168, 2.210642819420365], [48.710920220986154, 2.2203604036855], [48.715709851671406, 2.219681343580225], [48.71770282170553, 2.2051635068467705], [48.71150736152632, 2.201534047663407], [48.709931337221064, 2.2094486102697095]], dtype=float)
trace_vers_piste = np.array([[48.7107286912541, 2.2106586238092576], [48.71081302333026, 2.2112572795094163], [48.711030510663875, 2.211889567552281], [48.71131457433691, 2.2124276850355695], [48.7115542518136, 2.2132819465402904], [48.711745105284066, 2.2140622168910595], [48.712157878918575, 2.2150577342351436], [48.712486320036454, 2.215992713362358], [48.71265941651962, 2.217445630567238], [48.71265053979136, 2.218232627386548], [48.71260615612666, 2.2196115534374754]], dtype=float)

if __name__=="__main__":
	polygon = gps_to_xy(tour_de_lx, res=res)
	get_inside_points(polygon, display=False)


	get_points_alongside_route(gps_to_xy(trace_vers_piste, res= res), display=True)

def doc():
    """
    res est fixé à l'avance.

    Algorithme : 
    Le fichier .gpx est une liste de N points GPS.

    (!) Il serait intéressant d'implémenter ici une vérification de la vitesse sur le parcours, pour être sur que la trace n'est pas
    trafiquée et que c'est effectivement de la course à pied.

    On converti les points GPS en point scalaire sur le plan avec comme origine (0, 0) le BE Raid 24 et comme pas `res`. 
    Ainsi, si res = 50m, un point situé exactement 50m à l'est du BE Raid 24 a pour coordonée (0, 1).

    Ensuite, on applique l'algorithme de détermination des traces fermées et ouverte. On a deux types de segment principaux dans une trace : 
    - Les segments qui ne bouclent jamais. L'utilisateur est allé et venu par le même chemin. 
        On considère alors que le chemin emprunté a été claim sur une largeur de min_res autour de chaque point. 
        Par exemple, le point : (0.25, 0.75) claim les points [(0, 0), (0, 1), (1, 0), (1, 1)]
    - Les segments qui bouclent : ceux ci claim les points dont le centre est dans le polygone.

    L'algorithme de détermination renvoie ainsi une liste de polygone et de segments ouverts contenus dans la trace du .gpx.

    La dernière partie de l'algorithme consiste alors à itérer sur chacun de ces polygones/segments pour déterminer quelles tuiles ont été claim.
    Puis mettre à jour la base de donnée.
    """
    pass


""" 
Note : to update the DB : 

Use an F-expression so the increment happens in the database without loading each object.

If all tiles in the list should be incremented the same way:

from django.db.models import F

Tile.objects.filter(id__in=tile_ids).update(counter=F("counter") + 1)
"""