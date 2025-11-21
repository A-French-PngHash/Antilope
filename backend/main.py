import numpy as np

latcord = np.array([50, 48, 40, 40, 46])
longcord = np.array([0, 7, 7, -7, 2])
EPSILON = 3
TOL=10
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

def pg_pol(liste,point):
	d1=liste[:]-point
	d2=(d1[:]*d1[:]).sum(1)
	tested = d2<EPSILON*EPSILON
	filtered = np.nonzero(tested)
	return filtered[0]

def dist(a,b):
	d=a-b
	return (d*d).sum(0)
def separe(list_points:np.array):
	"""
	Converts latitude and longitude coordinates to plane (x, y) coordinates.
	Return:
		Array of (bool,array[points])
			bool:true means that array[points] is a cycle, false means it is a paths 
	"""
	if(dist(list_points[0],list_points[-1])<TOL):
		return [(True,list_points)]
	segmented=[]
	last_cut=0
	current_point=0
	while current_point<list_points.shape[0]:
		s = pg_pol(list_points[current_point+1:],list_points[current_point])
		if(s.size!=0):
			print(s)
			segmented.append((False,list_points[last_cut:current_point+1]))
			segmented.append((True,list_points[current_point:(s[-1]+current_point+2)]))
			current_point+=s[-1]+1
			last_cut=current_point
		else:
			current_point+=1
	if(last_cut<list_points.shape[0]):
		segmented.append((False,list_points[last_cut:]))
	return segmented

#print(pg_pol(np.array([[48,7],[40,7],[40,-7],[46,2],[51,1],[61,3],[72,7]]),np.array([50,0])))

print(separe(np.array([[0,0],[50,0],[48,7],[40,7],[40,-7],[46,2],[51,1],[61,3],[72,7],[73,-1],[60,-9],[72,8],[0,10]])))
    