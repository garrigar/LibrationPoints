import math
from collections import namedtuple
import tkinter
from tkinter import ttk

Constants = namedtuple('Constants', [
    'G',

    'MASS_MIN',
    'MASS_DEF',
    'MASS_MAX',

    'DENSITY_MIN',
    'DENSITY_DEF',
    'DENSITY_MAX',

    'RADIUS_MIN',
    'RADIUS_MAX',

    'DISTANCE_MIN',
    'DISTANCE_DEF',
    'DISTANCE_MAX',

    'SPEED_MIN',
    'SPEED_MAX'
])
constants = Constants(
    1,

    0.0,
    100.0,
    1000.0,

    1.0,
    10.0,
    20.0,

    0.0,
    5.0,

    10.0,
    15.0,
    100.0,

    0.0,
    5.0
)


class BinarySystem:
    class __Body:

        class __BodyConfig:

            def __init__(self, mass_, density_, radius_):
                self.__mass = mass_
                self.__density = density_
                self.__radius = radius_

            @property
            def mass(self):
                return self.__mass

            @property
            def density(self):
                return self.__density

            @property
            def radius(self):
                return self.__radius

        def __init__(self):
            self.__density = constants.DENSITY_DEF
            self.mass = constants.MASS_DEF

        @property
        def mass(self):
            return self.__mass

        @mass.setter
        def mass(self, value):
            self.__mass = min(max(constants.MASS_MIN, value), constants.MASS_MAX)

            new_radius = ((0.75 * self.__mass) / (math.pi * self.__density)) ** (1 / 3)
            if new_radius < constants.RADIUS_MIN or new_radius > constants.RADIUS_MAX:
                self.radius = new_radius
            else:
                self.__radius = new_radius

        @property
        def density(self):
            return self.__density

        @density.setter
        def density(self, value):
            self.__density = min(max(constants.DENSITY_MIN, value), constants.DENSITY_MAX)

            new_mass = (4 / 3) * math.pi * self.__density * (self.__radius ** 3)
            if new_mass < constants.MASS_MIN or new_mass > constants.MASS_MAX:
                self.mass = new_mass
            else:
                self.__mass = new_mass

        @property
        def radius(self):
            return self.__radius

        @radius.setter
        def radius(self, value):
            self.__radius = min(max(constants.RADIUS_MIN, value), constants.RADIUS_MAX)

            new_mass = (4 / 3) * math.pi * self.__density * (self.__radius ** 3)
            if new_mass < constants.MASS_MIN or new_mass > constants.MASS_MAX:
                self.mass = new_mass
            else:
                self.__mass = new_mass

        @property
        def config(self):
            return self.__BodyConfig(self.__mass, self.__density, self.__radius)

        @config.setter
        def config(self, config: __BodyConfig):  # USE WITH PREVIOUSLY GOTTEN CONFIGS ONLY
            self.__mass = config.mass
            self.__density = config.density
            self.__radius = config.radius

    def __init__(self):
        self.__body1 = self.__Body()
        self.__body2 = self.__Body()
        self.distance = constants.DISTANCE_DEF

    @property
    def mass1(self):
        return self.__body1.mass

    @mass1.setter
    def mass1(self, value):
        config = self.__body1.config

        self.__body1.mass = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body1.config = config
        else:
            self.__speed = new_speed

    @property
    def density1(self):
        return self.__body1.density

    @density1.setter
    def density1(self, value):
        config = self.__body1.config

        self.__body1.density = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body1.config = config
        else:
            self.__speed = new_speed

    @property
    def radius1(self):
        return self.__body1.radius

    @radius1.setter
    def radius1(self, value):
        config = self.__body1.config

        self.__body1.radius = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body1.config = config
        else:
            self.__speed = new_speed

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def mass2(self):
        return self.__body2.mass

    @mass2.setter
    def mass2(self, value):
        config = self.__body2.config

        self.__body2.mass = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body2.config = config
        else:
            self.__speed = new_speed

    @property
    def density2(self):
        return self.__body2.density

    @density2.setter
    def density2(self, value):
        config = self.__body2.config

        self.__body2.density = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body2.config = config
        else:
            self.__speed = new_speed

    @property
    def radius2(self):
        return self.__body2.radius

    @radius2.setter
    def radius2(self, value):
        config = self.__body2.config

        self.__body2.radius = value

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.__body2.config = config
        else:
            self.__speed = new_speed

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = min(max(constants.DISTANCE_MIN, value), constants.DISTANCE_MAX)

        new_speed = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__distance ** 3)) ** 0.5
        if new_speed < constants.SPEED_MIN or new_speed > constants.SPEED_MAX:
            self.speed = new_speed
        else:
            self.__speed = new_speed

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = min(max(constants.SPEED_MIN, value), constants.SPEED_MAX)

        new_distance = ((constants.G * (self.__body1.mass + self.__body2.mass)) / (self.__speed ** 2)) ** (1 / 3)
        if new_distance < constants.DISTANCE_MIN or new_distance > constants.DISTANCE_MAX:
            self.distance = new_distance
        else:
            self.__distance = new_distance


class BinarySystemRenderer:

    class Point:
        def __init__(self, x: float = 0, y: float = 0):
            self.x = x
            self.y = y

    def __init__(self, binary_system: BinarySystem, canvas_frame: ttk.LabelFrame,
                 canvas_width: int, canvas_height: int):

        self.__binary_system = binary_system

        self.__CANVAS_WIDTH = canvas_width
        self.__CANVAS_HEIGHT = canvas_height

        self.__canvas = tkinter.Canvas(canvas_frame, width=self.__CANVAS_WIDTH, height=self.__CANVAS_HEIGHT)
        self.__canvas.pack(expand=1)

        self.__canvas.config(bg='white')

        self.update()

    def update(self):
        bs = self.__binary_system

        alpha = bs.mass1 / (bs.mass1 + bs.mass2)

        middle = self.Point(self.__CANVAS_WIDTH / 2, self.__CANVAS_HEIGHT / 2)
        self.__canvas.create_line(0, 0, middle.x, middle.y)

        self.__canvas.create_line(0, 0, bs.mass1, bs.mass2)


class MainWindow(tkinter.Tk):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title('Binary System Simulator')
        self.geometry('+5+5')
        self.minsize(1520, 768)

        controls_frame = ttk.LabelFrame(self, text='System parameters')
        controls_frame.pack(expand=1, padx=7, pady=5, side=tkinter.LEFT)

        canvas_frame = ttk.LabelFrame(self, text='Simulation')
        canvas_frame.pack(expand=1, padx=7, pady=5, side=tkinter.RIGHT)

        bin_sys = BinarySystem()

        bin_sys_renderer = BinarySystemRenderer(bin_sys, canvas_frame, canvas_width=1150, canvas_height=733)

        self.__init_controls(controls_frame, bin_sys, bin_sys_renderer)

    @staticmethod
    def __init_controls(controls_frame: ttk.LabelFrame, bin_sys: BinarySystem, bin_sys_renderer: BinarySystemRenderer):

        slider_length = 300
        # ----------------------------------BODY 1--------------------------------------------

        body1_frame = ttk.LabelFrame(controls_frame, text='Body 1')
        body1_frame.grid(row=0, column=0, padx=10, pady=5)

        body1_mass_scale = tkinter.Scale(body1_frame, label='Mass',
                                         from_=constants.MASS_MIN, to=constants.MASS_MAX,
                                         tickinterval=constants.MASS_MAX, resolution=0.001,
                                         length=slider_length, orient=tkinter.HORIZONTAL)
        # body1_mass_scale.config(command=lambda val: update_scale(body1_mass_scale, float(val)))
        body1_mass_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body1_mass_scale))
        body1_mass_scale.grid(row=0)

        body1_density_scale = tkinter.Scale(body1_frame, label='Density',
                                            from_=constants.DENSITY_MIN, to=constants.DENSITY_MAX,
                                            tickinterval=constants.DENSITY_MAX, resolution=0.001,
                                            length=slider_length, orient=tkinter.HORIZONTAL)
        # body1_density_scale.config(command=lambda val: update_scale(body1_density_scale, float(val)))
        body1_density_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body1_density_scale))
        body1_density_scale.grid(row=1)

        body1_radius_scale = tkinter.Scale(body1_frame, label='Radius',
                                           from_=constants.RADIUS_MIN, to=constants.RADIUS_MAX,
                                           tickinterval=constants.RADIUS_MAX, resolution=0.001,
                                           length=slider_length, orient=tkinter.HORIZONTAL)
        # body1_radius_scale.config(command=lambda val: update_scale(body1_radius_scale, float(val)))
        body1_radius_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body1_radius_scale))
        body1_radius_scale.grid(row=2)

        # ----------------------------------BODY 2--------------------------------------------

        body2_frame = ttk.LabelFrame(controls_frame, text='Body 2')
        body2_frame.grid(row=1, column=0, padx=10, pady=5)

        body2_mass_scale = tkinter.Scale(body2_frame, label='Mass',
                                         from_=constants.MASS_MIN, to=constants.MASS_MAX,
                                         tickinterval=constants.MASS_MAX, resolution=0.001,
                                         length=slider_length, orient=tkinter.HORIZONTAL)
        # body2_mass_scale.config(command=lambda val: update_scale(body2_mass_scale, float(val)))
        body2_mass_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body2_mass_scale))
        body2_mass_scale.grid(row=0)

        body2_density_scale = tkinter.Scale(body2_frame, label='Density',
                                            from_=constants.DENSITY_MIN, to=constants.DENSITY_MAX,
                                            tickinterval=constants.DENSITY_MAX, resolution=0.001,
                                            length=slider_length, orient=tkinter.HORIZONTAL)
        # body2_density_scale.config(command=lambda val: update_scale(body2_density_scale, float(val)))
        body2_density_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body2_density_scale))
        body2_density_scale.grid(row=1)

        body2_radius_scale = tkinter.Scale(body2_frame, label='Radius',
                                           from_=constants.RADIUS_MIN, to=constants.RADIUS_MAX,
                                           tickinterval=constants.RADIUS_MAX, resolution=0.001,
                                           length=slider_length, orient=tkinter.HORIZONTAL)
        # body2_radius_scale.config(command=lambda val: update_scale(body2_radius_scale, float(val)))
        body2_radius_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(body2_radius_scale))
        body2_radius_scale.grid(row=2)

        # ------------------------------------------------------------------------------------

        distance_scale = tkinter.Scale(controls_frame, label='Distance between bodies',
                                       from_=constants.DISTANCE_MIN, to=constants.DISTANCE_MAX,
                                       tickinterval=constants.DISTANCE_MAX, resolution=0.001,
                                       length=slider_length, orient=tkinter.HORIZONTAL)
        # distance_scale.config(command=lambda val: update_scale(distance_scale, float(val)))
        distance_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(distance_scale))
        distance_scale.grid(row=2, column=0, padx=10, pady=5)

        speed_scale = tkinter.Scale(controls_frame, label='Angle speed',
                                    from_=constants.SPEED_MIN, to=constants.SPEED_MAX,
                                    tickinterval=constants.SPEED_MAX, resolution=0.001,
                                    length=slider_length, orient=tkinter.HORIZONTAL)
        # speed_scale.config(command=lambda val: update_scale(speed_scale, float(val)))
        speed_scale.bind("<ButtonRelease-1>", lambda event: on_scale_release(speed_scale))
        speed_scale.grid(row=3, column=0, padx=10, pady=5)

        rotation_switch_button = ttk.Button(controls_frame, text='Enable rotation', width=15)
        rotation_switch_button.grid(row=4, column=0, padx=10, pady=5)

        # ------------------------------------------------------------------------------------

        def on_scale_release(scale: tkinter.Scale):
            update_scale(scale, scale.get())

        def update_scale(scale: tkinter.Scale, value: float):
            if scale == body1_mass_scale:
                bin_sys.mass1 = value
            elif scale == body1_density_scale:
                bin_sys.density1 = value
            elif scale == body1_radius_scale:
                bin_sys.radius1 = value
            elif scale == body2_mass_scale:
                bin_sys.mass2 = value
            elif scale == body2_density_scale:
                bin_sys.density2 = value
            elif scale == body2_radius_scale:
                bin_sys.radius2 = value
            elif scale == distance_scale:
                bin_sys.distance = value
            elif scale == speed_scale:
                bin_sys.speed = value
            else:
                raise AttributeError()  # unexpected scale reference
            refresh_all_scales()
            bin_sys_renderer.update()

        def refresh_all_scales():
            body1_mass_scale.set(bin_sys.mass1)
            body1_density_scale.set(bin_sys.density1)
            body1_radius_scale.set(bin_sys.radius1)
            body2_mass_scale.set(bin_sys.mass2)
            body2_density_scale.set(bin_sys.density2)
            body2_radius_scale.set(bin_sys.radius2)
            distance_scale.set(bin_sys.distance)
            speed_scale.set(bin_sys.speed)

        # ------------------------------------------------------------------------------------

        refresh_all_scales()


if __name__ == "__main__":
    MainWindow().mainloop()
