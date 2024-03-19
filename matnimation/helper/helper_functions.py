import numpy as np
from typing import Callable

class HelperFunctions:
    def __init__(self):
        return 
    
    def func_ab_to_grid(func: Callable, a: np.ndarray, b: np.ndarray) -> np.ndarray: 
        """
        Takes a mathematical function f(a,b) called func, and two 1D arrays a and b.
        Returns a 2D numpy array called func_grid, where entry [i,j] contains function value func(a[i], b[j]).
        """

        a = a[:, np.newaxis]
        b = b[np.newaxis, :]

        func_grid = func(a,b)

        return func_grid
    
    def xy_grid(x_grid: np.ndarray, y_grid: np.ndarray):
        """
        Given x_grid = [x1, ..., xM] and y_grid = [y1, ..., yN], make an (x,y) coordinate grid of size (M,N):

        # ----------------------------- #
        | (x1,y1)       ...     (xM,y1) |
        |    :                     :    |
        |    :                     :    |
        | (x1,yN)       ...     (xM,yN) |
        # ----------------------------- #
        
        Return the grid as 1D arrays for x and y, which have the form:
        
        x_array = [x1,...,xM, x1,...,xM, ... x1,...,xM]     total of N copies of x1,...,xM
        y_array = [y1,...,y1, y2,...,y2, ... yN,...,yN]     total of N copies of yi,...,yi
        """

        X, Y = np.meshgrid(x_grid, y_grid)
        x_array, y_array = X.flatten(), Y.flatten()

        return x_array, y_array      
    
    def FxFy_to_grid(func_Fx: Callable, func_Fy: Callable, x_array: np.ndarray, y_array: np.ndarray, t_array: np.ndarray) -> np.ndarray:
        """

        Given a 2D vector field vec[F](x,y,t) = F_x(x,y,t) * xhat + F_y(x,y,t) * yhat, the arguments are:

        - The Callable functions func_Fx and func_Fy correspond to the mathematical functions F_x(x,y,t) and F_y(x,y,t), and should have signature (x: float, y: float, t: float). 
        - The 1D arrays x_array = [x1, x2, ... xN] and y_array = [y1, y2, ..., yN] contain the (x,y) coordinates of the N points at which vec[F] should be plotted. 
        - The time array t_array = [t1, t2, ... tM] contains the M chronological timevalues at which the field should be plotted. 

        Warning: x_array and y_array must have the same length!

        Returns:
        Fx_data: 2D numpy array with F_x components at all N plotting points (rows) and timesteps (cols), #nrows = N, #cols = M
        Fy_data: 2D numpy array with F_y components at all N plotting points (rows) and timesteps (cols), #nrows = N, #cols = M

        """

        if x_array.ndim != 1 or y_array.ndim != 1:
            raise ValueError('x_array and/or y_array are not 1D')

        if len(x_array) != len(y_array):
            raise ValueError('Length of x_array and y_array are not identical.')
        
        Nx, Nt = len(x_array), len(t_array)

        Fx_data = np.zeros((Nx, Nt))
        Fy_data = np.zeros((Nx, Nt))

        for coord_index in range(Nx):
            for time_index in range(Nt):

                x, y = x_array[coord_index], y_array[coord_index]
                t = t_array[time_index]

                Fx_data[coord_index, time_index] = func_Fx(x, y, t)
                Fy_data[coord_index, time_index] = func_Fy(x, y, t)

        return Fx_data, Fy_data



        
    
