# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 08:03:06 2012

@author: leonard
"""
import matplotlib

def cmap_xmap(function,cmap):
    """ Applies function, on the indices of colormap cmap. Beware, function
        should map the [0, 1] segment to itself, or you are in for surprises.
        See also cmap_xmap.
    """
    cdict = cmap._segmentdata
    function_to_map = lambda x : (function(x[0]), x[1], x[2])
    for key in ('red','green','blue'):         
        cdict[key] = map(function_to_map, cdict[key])
        cdict[key].sort()
        assert (cdict[key][0]<0 or cdict[key][-1]>1), "Resulting indices extend out of the [0, 1] segment."
    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)
    
def cmap_discretize(cmap, N):
    """ Return a discrete colormap from the continuous colormap cmap.
            cmap: colormap instance, eg. cm.jet. 
            N: Number of colors.
   Example
       x = resize(arange(100), (5,100))
       djet = cmap_discretize(cm.jet, 5)
       imshow(x, cmap=djet) 
   """
    
    dict = cmap._segmentdata.copy()
    # N colors
    colors_i = linspace(0,1.,N)
    # N+1 indices
    indices = linspace(0,1.,N+1)
    for key in ('red','green','blue'):
        # Find the N colors
        D = array(cdict[key])
        I = interpolate.interp1d(D[:,0], D[:,1])
        colors = I(colors_i)
        # Place these colors at the correct indices.
        A = zeros((N+1,3), float)
        A[:,0] = indices
        A[1:,1] = colors
        A[:-1,2] = colors
        # Create a tuple for the dictionary.
        L = []
        for l in A:
            L.append(tuple(l))
        cdict[key] = tuple(L)
        # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)
  
cmap_discretize(cm.jet,6)