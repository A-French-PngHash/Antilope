from titouan import gps_to_xy,res,tour_de_lx,trace_vers_piste
import numpy as np
from matplotlib import pyplot as plt

def get_intersect_squares_from_segment(segment):
    """
    Trouve l'intersection du segment avec les tiles
    """
    def y(x):
        return segment[1][1]*((x-segment[0][0])/(segment[1][0]-segment[0][0]))+segment[0][1]*((x-segment[1][0])/(segment[0][0]-segment[1][0]))
    #On trouve les intersection avec lignes demi-entière en x et on calcul leurs y
    xmin, xmax = np.min(segment[:, 0]), np.max(segment[:, 0])
    intersect_x = np.arange(np.floor(xmin+.5)+.5,np.ceil(xmax-.5)+.5,1)
    intersect_x = np.append(intersect_x,xmax)
    intersect_x = np.insert(intersect_x,0,xmin)
    intersect_x_interval= np.stack((intersect_x[:-1],intersect_x[1:]),axis=1)
    intersect_y_interval=y(intersect_x_interval)
    #Comble un intervalle en y
    def fill (y):
        ymin,ymax=np.floor(np.min(y,0)-.5)+.5,np.floor(np.max(y,0)-.5)+.5
        print(y,ymin,ymax)
        return np.arange(ymin,ymax+1,1)
    #On trouve la case à laquelle correspond le segment de deux x et on combine avec la liste en y
    def pair_with_x(x,y):
        a= [[np.round((x[1]+x[0])*.5),np.ceil(j)] for j in y]
        return a
    #On assemble tout
    a= np.concatenate([ pair_with_x(intersect_x_interval[i],fill(intersect_y_interval[i])) for i in range(intersect_x_interval.shape[0])])
    return a

def get_points_alongside_route(path : np.array, display):
    """ 
    When a run does not form a closed loop, some segments of it are just straight lines. 
    Alongside those straight lines, the runner should claim surounding tile (in a ~100m = 2 * min_res radius)
    
    We will asume that there is at least a point every ~50m = min_res.
    :param path: List of points in planar coordinates describing the route taken by the user.
    """
    
	#On obtient une liste de segments:
    segments= np.stack((path[:-1],path[1:]),axis=1)
    points = np.concatenate([get_intersect_squares_from_segment(i) for i in segments])
    
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
        
        plt.pcolormesh(x, y, result.reshape(y.shape[0],x.shape[0]), cmap = "Blues",linewidth=1,edgecolor='k')#, shading='flat')
        plt.gca().set_aspect('equal')
        plt.plot(*path.transpose(), color="red",marker="+")
        plt.show()

    return np.unique(points, axis=0)

def get_bouding_box(tiles):
    """
    Renvoie la boite englobante la liste des tiles
    """
    return np.array([np.min(tiles,0)-[1,1],np.max(tiles,0)+[1,1]])

if __name__=="__main__":
    #get_points_alongside_route(np.array([[0.4,0.4],[2.4,3.4]]),display=True)
    get_points_alongside_route(gps_to_xy(trace_vers_piste, res= res), display=True)
    get_points_alongside_route(gps_to_xy(tour_de_lx, res= res), display=True)

    #get_intersect_squares_from_segment(np.array([[0.6,0.5],[2.6,3.5]]))