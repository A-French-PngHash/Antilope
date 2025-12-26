import gpxpy
import numpy as np
import gpxpy.gpx
from matplotlib import path
from matplotlib import pyplot as plt

class Trace:
    """
    Holds a trace in planar coordinate. 
    WARNING : The coordinates are stored at dimension min_res which means (1, 1) is actually (min_res, min_res)
    """
    
    points : np.array
    res = 50 # Resolution to use for the tiles

    def __init__(self, points : np.array):
        """ 
        Builds a trace object from a list of points (in planar coordinates).
        """
        self.points = points

    @staticmethod
    def from_gpx(file_path):
        """
        Reads a .gpx file and returns a Trace object with the points that are in the GPX.
        
        :param file_path: Path to access the file.

        :returns: np.array of dim (N, 2)
        """
        gpx_file = open(file_path, 'r')
        gpx = gpxpy.parse(gpx_file)

        path_points = []

        for track in gpx.tracks:
            for segment in track.segments:
                print(segment)
                for point in segment.points:
                    path_points.append((point.latitude, point.longitude))

        path_points = np.array(path_points, dtype=float)
        path_xy = Trace.gps_to_xy(path_points, Trace.res)
        return Trace(path_xy)

    @classmethod
    def gps_to_xy(cls, cords, res):
        """
        Converts latitude and longitude coordinates to plane (x, y) coordinates.
        
        Requirements : 
            Latitude and longitude should be in degrees.
            - |lat| < 90
            - |long| < 180

        :param cords: Numpy array of shape (N, 2).
        """
        x_be = 246060.103795
        y_be = 6225818.4272805
        R = 6378000
        x = np.pi * R * cords[:, 1] / 180 - x_be
        y = R * np.log(np.tan(1/4 * np.pi + np.pi * 1/2 * cords[:, 0] / 180)) - y_be
        return np.column_stack((np.round(x / res, 2), np.round(y / res, 2)))
    
    def __repr__(self):
        return "object Trace(points=" + str(self.points) + ")"

print(__name__)
if __name__ == "__main__":
    print(Trace.gps_to_xy(np.array([[48.787917,1.980520]]), 50))