import numpy as np
from matplotlib import path
from matplotlib import pyplot as plt

from .gpx_decoder import Trace

class ClaimFinder():
    """
    A utility that implements the algorithm that finds every claimed tile from a Trace object.
    """

    _polygons = [] # List of np.array(N, 2) that holds every closed loop inside the trace
    #_segments = [] # List of np.array(M, 2) that holds every segment in the trace.
    _same_point = 20 # Distance under which points are considered the 'same'.

    def __init__(self, trace : Trace):
        self.trace = trace


    def _pg_pol(self, liste,point, tol):
        """ 
        Return the indices of the points of `liste` which are at a distance < `tol` of `point` 
        """
        d1=liste[:]-point
        d2=(d1[:]*d1[:]).sum(1)
        tested = d2<tol
        filtered = np.nonzero(tested)
        return filtered[0]


    def separe(self, list_points:np.array):
        """
        Converts latitude and longitude coordinates to plane (x, y) coordinates.
        Return:
            Array of (bool,array[points])
                bool:true means that array[points] is a cycle, false means it is a paths 
        """
        def dist(a,b):
            d=a-b
            return (d*d).sum(0)
        TOL=self._same_point / self.trace.res # Distance under which points are considered the same.
        TOL = TOL * TOL # Because we will be comparing squared distances.
        if(dist(list_points[0],list_points[-1])<TOL):
            return [(True,list_points)]
        segmented=[]
        last_cut=0
        current_point=0
        while current_point<list_points.shape[0]:

            # Finding where to stop searching : 
            # We search points from [first point where dist(current_point) > TOL, last point]
            
            left = current_point + 1 # Interval we will be searching is [left:]
            
            while (left < list_points.shape[0] and 
                TOL > np.square((list_points[left]- list_points[current_point]).flatten()).sum()):
                left += 1

            if left == list_points.shape[0]: # Every point in [current_point:] is at distance less than TOL of current_point. Therefore, there is no cycle in this interval.
                break


            s = self._pg_pol(list_points[left:],list_points[current_point], TOL)
            if(s.size!=0):
                segmented.append((False,list_points[last_cut:current_point]))
                segmented.append((True,list_points[current_point:(s[-1]+left+1)]))
                current_point=left + s[-1] + 1
                last_cut=current_point
            else:
                current_point+=1
        if(last_cut<list_points.shape[0]):
            segmented.append((False,list_points[last_cut:]))
        return segmented
    
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


    def get_inside_tiles(self, poly, display = False):
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


    def get_tiles_alongside_route(self,path, display=False):
        """ 
        When a run does not form a closed loop, some segments of it are just straight lines. 
        Alongside those straight lines, the runner should claim surounding tile (in a ~100m = 2 * res radius)
        
        We will asume that there is at least a point every ~50m = res.

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

        return np.unique(points.astype(np.int64), axis=0)
    
    def display_tiles_and_trace(self, tiles):
        """
        Plots the `self.trace` with the supplied `tiles` in a different color in the background.
        
        :param self: Description
        :param tiles: Tiles to display as claimed. np.array of shape (N, 2)
        """
        path = self.trace.points
        window = 5
        xmin, xmax = np.floor(np.min(path[:, 0])) - window, np.ceil(np.max(path[:, 0])) + window
        ymin, ymax = np.floor(np.min(path[:, 1])) - window, np.ceil(np.max(path[:, 1])) + window
        x = np.arange(xmin, xmax+1)
        y = np.arange(ymin, ymax+1)
        xx, yy = np.meshgrid(x, y) 
        grid = np.column_stack((xx.ravel(), yy.ravel())) # better use ravel : makes no copy (flatten makes a copy)

        selected_tiles = {tuple(p) for p in tiles}
        result = np.array([1 if tuple(p) in selected_tiles else 0 for p in grid])
        
        plt.pcolormesh(x, y, result.reshape(y.shape[0],x.shape[0]), cmap = "Blues")#, shading='flat')
        plt.gca().set_aspect('equal')
        plt.plot(*path.transpose(), color="red")
        plt.show()


    
    def _populate_polygons_segments(self):
        """ 
        Populates this class `_polygons` and `_segments` variable.
        """
        output = self.separe(self.trace.points)
        for i in output:
            if i[0]:
                self._polygons.append(i[1])
            #else:
                #self._segments.append(i[1])

    
    def get_all_tiles_to_claim(self):
        """
        Returns a np.array containing all the tiles to claim in the trace obeject supplied at __init__.
        """
        # First apply the algorithm to populate `polygon` and `segments`
        self._populate_polygons_segments()
        tiles = []
        for poly in self._polygons:
            tiles.append(self.get_inside_tiles(poly))
        #for segment in self._segments:
            #tiles.append(self.get_tiles_alongside_route(segment))
        tiles.append(self.get_tiles_alongside_route(self.trace.points))
        return np.unique(np.concatenate(tiles, axis=0), axis=0)
    
