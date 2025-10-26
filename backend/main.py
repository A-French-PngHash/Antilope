import numpy as np

latcord = np.array([50, 48, 40, 40, 46])
longcord = np.array([0, 7, 7, -7, 2])
# 43 -2
# 

R = 6378000
def gps_to_xy(lat, long):
    """
    Converts latitude and longitude coordinates to plane (x, y) coordinates.
    
    Requirements : 
        Latitude and longitude should be in degrees.
        - |lat| < 90
        - |long| < 180
    """

    x = np.pi * R * long / 180
    y = np.log(np.tan(1/4 * np.pi + np.pi * 1/2 * lat / 180))
    print(x, y)

gps_to_xy(latcord, longcord)

def point_inpoly(latcord, longcord):
    pass