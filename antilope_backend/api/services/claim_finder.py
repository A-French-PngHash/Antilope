import numpy as np
from matplotlib import path
from matplotlib import pyplot as plt

from .gpx_decoder import Trace

class ClaimFinder():
    """
    A utility that implements the algorithm that finds every claimed tile from a Trace object.
    """

    _polygons = [] # List of np.array(N, 2) that holds every closed loop inside the trace
    _segments = [] # List of np.array(M, 2) that holds every segment in the trace.
    

    def __init__(self, trace : Trace):
        self.trace = trace

    
    def _point_inpoly(self, poly, points):
        """ 
        Checks wether (x, y) points are in the given polynom.

        Points should be planar coordinates NOT be (latitude, longitude) pairs.

        :param poly: Planar coordinates of the polygon (assumed to be CLOSED)
        :param points: Points to check wether they are in the polygon. Shape : (N, 2)

        :returns: 
        """

        p = path.Path(list(poly.tolist()))
        return p.contains_points(points)


    def get_inside_points(self, poly, display = False):
        """
        Returns an exhaustive list of point (in planar coordinates) that are located inside the polygon.

        :param poly: Planar coordinates of the polygon (assumed to be CLOSED)
        :param display: Displays the polygon and the inside tile

        :returns:
        """
        maxx, minx = np.int64(np.ceil(poly[:, 0].max())), np.int64(np.floor(poly[:,0].min()))
        maxy, miny = np.int64(np.ceil(poly[:, 1].max())), np.int64(np.floor(poly[:, 1].min()))
        # Checks every point in the square with top left (maxx, maxy) and bottom right (minx, miny)
        x = np.arange(minx, maxx)
        y = np.arange(miny, maxy)

        xx, yy = np.meshgrid(x, y) 
        points = np.stack((xx, yy), axis=2)
        m, n = points.shape[0], points.shape[1]
        points = points.reshape((n* m, 2))
        result = points[self._point_inpoly(poly, points)]

        if display:
            plt.pcolormesh(x, y, result.reshape(m, n), cmap = "Blues")
            
            plt.plot(*poly.transpose(), color="red")
            plt.axis([minx-5, maxx+5, miny-5, maxy+5])
            plt.show()

        return np.unique(result, axis= 0) # Unique here should not be needed as we a priori have no redondency, however just to be sure.


    def get_points_alongside_route(self,path, display=False):
        """ 
        When a run does not form a closed loop, some segments of it are just straight lines. 
        Alongside those straight lines, the runner should claim surounding tile (in a ~100m = 2 * min_res radius)
        
        We will asume that there is at least a point every ~50m = min_res.
        :param path: List of points in planar coordinates describing the route taken by the user.
        :param display: If set to True, will display a map showing the claimed tiles.
        """
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
        
    
    def find_all_tiles_to_claim(self):
        """
        Returns a np.array containing all the tiles to claim in the supplied trace.
        """
        # First apply the algorithm to populate `polygon` and `segments`
        tiles = []
        for poly in self.polygons_:
            tiles.append(self.get_inside_points(poly))
        for segment in self._segments:
            tiles.append(self.get_points_alongside_route(segment))
        
        return np.unique(np.concatenate(tiles))
    
