import numpy as np

class Tides:

    def __init__(self, radius_earth: float, ocean_scaling: float, distance_earth_moon: float):
        # ocean scaling must be larger than 1!!!


        # angles for plotting tidal bulges
        self.N_theta = 100
        self.theta_0 = 0
        self.theta = np.linspace(
            self.theta_0,
            self.theta_0 + 2 * np.pi,
            self.N_theta
        )

        # period/angular frequency earth revolution
        self.T_day = 1 # day
        self.omega_day = 2 * np.pi / self.T_day # per day

        # period/angular frequency lunar/moon orbit
        self.T_moon = 30 # days
        self.omega_moon = 2 * np.pi / self.T_moon # per day

        # delta omaga 
        self.delta_omega = self.omega_day - self.omega_moon

        # time array for one month (= timespan animation)
        self.N_t = 1000
        self.t_0 = 0
        self.t = np.linspace(self.t_0, self.T_moon, self.N_t)

        # array omega * t for the moon, including starting condition
        self.omega_moon_t_0 = 0
        self.omega_moon_t = self.omega_moon * self.t + self.omega_moon_t_0

        # matrix with theta values for tidal bulges (rows) at all times in t (columns)
        # columns represent subsequent times
        self.theta_matrix = np.tile(self.theta, (self.N_t, 1)).transpose()

        # radius earth
        self.radius_earth = radius_earth

        # ocean scaling 
        self.ocean_scaling = ocean_scaling

        # solid (round) earth matrix (at all times t, columns)
        self.x = self.ocean_scaling * self.radius_earth * np.cos(self.theta_matrix)
        self.y = self.ocean_scaling * self.radius_earth * np.sin(self.theta_matrix)

        # motion of moon
        self.distance_earth_moon = distance_earth_moon
        self.x_moon = self.distance_earth_moon * np.cos(self.omega_moon_t)
        self.y_moon = self.distance_earth_moon * np.sin(self.omega_moon_t)

        # scale factor potential
        self.scale_potential = 0.05 / 2

        # schrink factors 
        self.schrink_moon = 0.36
        self.schrink_sun = 0.16
        self.schrink_total = 0.52

        # tidal amplitudes moon and sun
        self.amplitude_moon = 0.36 #m
        self.amplitude_sun = 0.16 #m

        # tidal weight moon over sun
        self.fMS = 2.3876

        # tidal bulges
        self.bulge_moon = None
        self.bulge_sun = None
        self.bulge_total = None

        # minimum radius
        self.radius_min = None

        # observer on equator
        self.x_observer_equator = None
        self.y_observer_equator = None

        return 
    
    def get_time_array(self):
        return self.t
    
    def get_moon_orbit(self):
        return self.x_moon, self.y_moon
    
    def generate_tidal_bulges(self, body = 'total'):
        """
        Generates data for plotting the tidal bulges. 

        Returns:
        bulge_moon  (list, len 2)           list [x_bulge_moon, y_bulge_moon] 
        bulge_sun   (list, len 2)           same as bulge_moon, but for sun
        bulge_total (list, len 2)           same as bulge_moon, but for total = sun + moon
        r_min       (float or None)         mininum radius to center earth at t = 0, defines edge of earth (where ocean begins)
                                            r_min is only float if moon = True and sun = True. 
        
        Format of x_bulge_body and y_bulge_body (body = moon, sun or total) is: 
        x_bulge_body    (2D array)         x-coordinates of bulge at all timesteps, rows: coordinates, columns: timsteps
        y_bulge_body    (2D array)         y-coordinates of bulge at all timesteps, rows: coordinates, columns: timsteps
        """

        # tidal potentials due to moon and sun

        # due to moon, located at angle omega_moon_t with respect to +x axis
        # 'tidal_potential_moon' is a 2D np array 
        # rows: potentials at theta angles  (len: N_theta)
        # cols: potentials at timesteps     (len: N_t)

        tidal_potential_moon = -self.fMS * self.scale_potential * ( 3 * np.cos(self.theta_matrix - self.omega_moon_t) ** 2 - 1 ) 

        # due to moon, located at angle omega_moon_t with respect to +x axis
        # 'tidal_potential_sun' is a 2D np array 
        # rows: potentials at theta angles  (len: N_theta)
        # cols: potentials at timesteps     (len: N_t)

        tidal_potential_sun = -self.scale_potential * ( 3 * np.cos(np.pi - self.theta_matrix) ** 2 - 1 )


        dr_moon = - tidal_potential_moon
        dr_sun = - tidal_potential_sun
        dr_total = - tidal_potential_sun - tidal_potential_moon
        
        dx_moon,    dy_moon   =   dr_moon * np.cos(self.theta_matrix),    dr_moon * np.sin(self.theta_matrix)
        dx_sun,     dy_sun    =   dr_sun * np.cos(self.theta_matrix),     dr_sun * np.sin(self.theta_matrix)
        dx_total,   dy_total  =   dr_total * np.cos(self.theta_matrix),   dr_total * np.sin(self.theta_matrix)

        x_bulge_moon,   y_bulge_moon    = self.x + dx_moon,     self.y + dy_moon
        x_bulge_sun,    y_bulge_sun     = self.x + dx_sun,      self.y + dy_sun
        x_bulge_total,  y_bulge_total   = self.x + dx_total,    self.y + dy_total

        if body == 'total':
            
            # radii corresponding to total bulge
            radii_bulge_total = np.sqrt(x_bulge_total[:,0] ** 2 + y_bulge_total[:,0] ** 2)
            self.radius_total_min = np.amin(radii_bulge_total)

            self.radius_total_min_new = self.ocean_scaling * self.radius_earth - self.schrink_total * (self.ocean_scaling - 1) * self.radius_earth
            self.norm_factor_total = self.radius_total_min_new / self.radius_total_min

            x_bulge_total = self.norm_factor_total * x_bulge_total
            y_bulge_total = self.norm_factor_total * y_bulge_total

            return x_bulge_total, y_bulge_total
        
        if body == 'moon':

            # radii corrsponding to moon bulge
            radii_bulge_moon = np.sqrt(x_bulge_moon[:,0] ** 2 + y_bulge_moon[:,0] ** 2)
            self.radius_moon_min = np.amin(radii_bulge_moon)

            self.radius_moon_min_new = self.ocean_scaling * self.radius_earth - self.schrink_moon * (self.ocean_scaling - 1) * self.radius_earth
            self.norm_factor_moon = self.radius_moon_min_new / self.radius_moon_min

            x_bulge_moon = self.norm_factor_moon * x_bulge_moon
            y_bulge_moon = self.norm_factor_moon * y_bulge_moon

            return x_bulge_moon, y_bulge_moon
        
        if body == 'sun':

            # radii corrsponding to sun bulge
            radii_bulge_sun = np.sqrt(x_bulge_sun[:,0] ** 2 + y_bulge_sun[:,0] ** 2)
            self.radius_sun_min = np.amin(radii_bulge_sun)

            self.radius_sun_min_new = self.ocean_scaling * self.radius_earth - self.schrink_sun * (self.ocean_scaling - 1) * self.radius_earth
            self.norm_factor_sun = self.radius_sun_min_new / self.radius_sun_min

            x_bulge_sun = self.norm_factor_sun * x_bulge_sun
            y_bulge_sun = self.norm_factor_sun * y_bulge_sun

            return x_bulge_sun, y_bulge_sun

    def generate_observer_equator_trajectory(self):
        """Generates the trajectory of a stationary observer on the equator, such that the period of rotation is 1 day."""

        self.x_observer_equator = self.radius_earth * np.cos(self.omega_day * self.t)
        self.y_observer_equator = self.radius_earth * np.sin(self.omega_day * self.t)

        return self.x_observer_equator, self.y_observer_equator

    def tidal_force_total(self, theta_vectors, t, scale = 1):
        """
        Tidal force vectors for total combination sun + moon.
        In this case, theta_vectors are the angles on the earth at which the tidal force vectors should be plotted!
        """

        Fx = scale * (
            self.fMS * (
                -2 * np.cos( theta_vectors ) + 6 * np.cos( theta_vectors - ( self.omega_moon * t + self.omega_moon_t_0 ) ) * np.cos( self.omega_moon * t + self.omega_moon_t_0 )
            )
            + 4 * np.cos( theta_vectors )
        )

        Fy = scale * (
            self.fMS * (
                -2 * np.sin( theta_vectors ) + 6 * np.cos( theta_vectors - ( self.omega_moon * t + self.omega_moon_t_0 ) ) * np.sin( self.omega_moon * t + self.omega_moon_t_0 )
            )
            - 2 * np.sin( theta_vectors )
        )

        return Fx, Fy
    
    def tidal_force_moon(self, theta_vectors, t, scale = 1):
        """Tidal force vectors for moon only.
        In this case, theta_vectors are the angles on the earth at which the tidal force vectors should be plotted!"""

        Fx = scale * self.fMS * ( -2 * np.cos( theta_vectors ) + 6 * np.cos( theta_vectors - ( self.omega_moon * t + self.omega_moon_t_0 ) ) * np.cos( self.omega_moon * t + self.omega_moon_t_0 ) )
        Fy = scale * self.fMS * ( -2 * np.sin( theta_vectors ) + 6 * np.cos( theta_vectors - ( self.omega_moon * t + self.omega_moon_t_0 ) ) * np.sin( self.omega_moon * t + self.omega_moon_t_0 ) )

        return Fx, Fy
    
    def tidal_force_sun(self, theta_vectors, t, scale = 1):
        """Tidal force vectors for sun only.
        In this case, theta_vectors are the angles on the earth at which the tidal force vectors should be plotted!"""

        Fx = scale * ( + 4 * np.cos( theta_vectors ) )
        Fy = scale * ( - 2 * np.sin( theta_vectors ) )

        return Fx, Fy
    
    def tidal_profile_moon(self, t):
        tid_prof = self.amplitude_moon * (1.5*np.cos(self.delta_omega * t)**2-0.5)

        return tid_prof
    
    def tidal_profile_total(self, t):
        tid_prof = self.amplitude_moon * (1.5*np.cos(self.delta_omega * t)**2 - 0.5) + self.amplitude_sun * (1.5*np.cos(np.pi - self.omega_day * t)**2 - 0.5)

        return tid_prof
