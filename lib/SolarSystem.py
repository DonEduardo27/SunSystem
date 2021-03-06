#!/usr/bin/python3

### import guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed
import avango.daemon

### import framework libraries
from lib.SolarObject import SolarObject
import lib.SolarParameters as SolarParameters

### import python libraries
import math


class SolarSystem(avango.script.Script):

    ## input fields
    sf_key0 = avango.SFFloat()
    sf_key1 = avango.SFFloat()
  
    ## output_fields
    sf_time_scale_factor = avango.SFFloat()
    sf_time_scale_factor.value = 1.0


    ### constructor
    def __init__(self):
        self.super(SolarSystem).__init__() # call base-class constructor

        ## init device sensors
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.keyboard_sensor.Station.value = "gua-device-keyboard0"

        self.sf_key0.connect_from(self.keyboard_sensor.Button12)
        self.sf_key1.connect_from(self.keyboard_sensor.Button13)


    def my_constructor(self, PARENT_NODE):

        # init Sun
        self.sun = SolarObject(
            NAME = "sun",
            TEXTURE_PATH = SolarParameters.SUN_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = PARENT_NODE,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.SUN_DIAMETER,
            ORBIT_RADIUS = 0.0,
            ORBIT_INCLINATION = 0.0,
            ORBIT_DURATION = 0.0,
            ROTATION_INCLINATION = 0.0,
            ROTATION_DURATION = 0.0,
            )
                                                                            
        # init lightsource (only for sun)
        self.sun_light = avango.gua.nodes.LightNode(Name = "sun_light", Type = avango.gua.LightType.POINT)
        self.sun_light.Color.value = avango.gua.Color(1.0, 1.0, 1.0)
        self.sun_light.Brightness.value = 25.0
        self.sun_light.Falloff.value = 0.2
        self.sun_light.EnableShadows.value = True
        self.sun_light.ShadowMapSize.value = 2048
        self.sun_light.Transform.value = avango.gua.make_scale_mat(50.0) # light volume defined by scale
        self.sun_light.ShadowNearClippingInSunDirection.value = 0.1 / 50.0

        _node = self.sun.get_orbit_node()
        _node.Children.value.append(self.sun_light)

        ## TODO: init planets and moons below here
        self.mercury = SolarObject(
            NAME = "mercury",
            TEXTURE_PATH = SolarParameters.MERCURY_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.MERCURY_DIAMETER,
            ORBIT_RADIUS = SolarParameters.MERCURY_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.MERCURY_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.MERCURY_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.MERCURY_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.MERCURY_ROTATION_DURATION,
            )
        self.venus = SolarObject(
            NAME = "venus",
            TEXTURE_PATH = SolarParameters.VENUS_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.VENUS_DIAMETER,
            ORBIT_RADIUS = SolarParameters.VENUS_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.VENUS_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.VENUS_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.VENUS_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.VENUS_ROTATION_DURATION,
            )
        self.earth = SolarObject(
            NAME = "earth",
            TEXTURE_PATH = SolarParameters.EARTH_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.EARTH_DIAMETER,
            ORBIT_RADIUS = SolarParameters.EARTH_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.EARTH_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.EARTH_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.EARTH_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.EARTH_ROTATION_DURATION,
            )

        self.earth_moon = SolarObject(
            NAME = "earth_moon",
            TEXTURE_PATH = SolarParameters.EARTH_MOON_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = self.earth.get_orbit_node(),
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.EARTH_MOON_DIAMETER,
            ORBIT_RADIUS = SolarParameters.EARTH_MOON_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.EARTH_MOON_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.EARTH_MOON_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.EARTH_MOON_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.EARTH_MOON_ROTATION_DURATION,
            )

        self.mars = SolarObject(
            NAME = "mars",
            TEXTURE_PATH = SolarParameters.MARS_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.MARS_DIAMETER,
            ORBIT_RADIUS = SolarParameters.MARS_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.MARS_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.MARS_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.MARS_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.MARS_ROTATION_DURATION,
            )

        self.jupiter = SolarObject(
            NAME = "jupiter",
            TEXTURE_PATH = SolarParameters.JUPITER_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.JUPITER_DIAMETER,
            ORBIT_RADIUS = SolarParameters.JUPITER_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.JUPITER_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.JUPITER_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.JUPITER_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.JUPITER_ROTATION_DURATION,
            )
        self.jupiter_moon1 = SolarObject(
            NAME = "jupiter_moon1",
            TEXTURE_PATH = SolarParameters.JUPITER_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = self.jupiter.get_orbit_node(),
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.JUPITER_MOON1_DIAMETER,
            ORBIT_RADIUS = SolarParameters.JUPITER_MOON1_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.JUPITER_MOON1_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.JUPITER_MOON1_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.JUPITER_MOON1_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.JUPITER_MOON1_ROTATION_DURATION,
            )
        self.jupiter_moon2 = SolarObject(
            NAME = "jupiter_moon2",
            TEXTURE_PATH = SolarParameters.JUPITER_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = self.jupiter.get_orbit_node(),
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.JUPITER_MOON2_DIAMETER,
            ORBIT_RADIUS = SolarParameters.JUPITER_MOON2_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.JUPITER_MOON2_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.JUPITER_MOON2_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.JUPITER_MOON2_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.JUPITER_MOON2_ROTATION_DURATION,
            )
        self.jupiter_moon3 = SolarObject(
            NAME = "jupiter_moon3",
            TEXTURE_PATH = SolarParameters.JUPITER_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = self.jupiter.get_orbit_node(),
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.JUPITER_MOON3_DIAMETER,
            ORBIT_RADIUS = SolarParameters.JUPITER_MOON3_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.JUPITER_MOON3_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.JUPITER_MOON3_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.JUPITER_MOON3_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.JUPITER_MOON3_ROTATION_DURATION,
            )

        self.saturn = SolarObject(
            NAME = "saturn",
            TEXTURE_PATH = SolarParameters.SATURN_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.SATURN_DIAMETER,
            ORBIT_RADIUS = SolarParameters.SATURN_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.SATURN_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.SATURN_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.SATURN_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.SATURN_ROTATION_DURATION,
            )
        self.uranus = SolarObject(
            NAME = "uranus",
            TEXTURE_PATH = SolarParameters.URANUS_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.URANUS_DIAMETER,
            ORBIT_RADIUS = SolarParameters.URANUS_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.URANUS_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.URANUS_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.URANUS_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.URANUS_ROTATION_DURATION,
            )
        self.neptune = SolarObject(
            NAME = "neptune",
            TEXTURE_PATH = SolarParameters.NEPTUNE_TEXTURE,
            HIGH_EMISSIVITY = True,
            PARENT_NODE = _node,
            SF_TIME_SCALE = self.sf_time_scale_factor,
            DIAMETER = SolarParameters.NEPTUNE_DIAMETER,
            ORBIT_RADIUS = SolarParameters.NEPTUNE_ORBIT_RADIUS,
            ORBIT_INCLINATION = SolarParameters.NEPTUNE_ORBIT_INCLINATION,
            ORBIT_DURATION = SolarParameters.NEPTUNE_ORBIT_DURATION,  
            ROTATION_INCLINATION = SolarParameters.NEPTUNE_ROTATION_INCLINATION,
            ROTATION_DURATION = SolarParameters.NEPTUNE_ROTATION_DURATION,
            )

    ### callback functions ###
    @field_has_changed(sf_key0)
    def sf_key0_changed(self):
        if self.sf_key0.value == True: # button pressed
            _new_factor = self.sf_time_scale_factor.value * 1.5 # increase factor about 50% 

            self.set_time_scale_factor(_new_factor)
      
    @field_has_changed(sf_key1)
    def sf_key1_changed(self): 
        if self.sf_key1.value == True: # button pressed
            _new_factor = self.sf_time_scale_factor.value * 0.5 # decrease factor about 50% 

            self.set_time_scale_factor(_new_factor)

    ### functions ###
    def set_time_scale_factor(self, FLOAT): 
        self.sf_time_scale_factor.value = min(10000.0, max(1.0, FLOAT)) # clamp value to reasonable intervall