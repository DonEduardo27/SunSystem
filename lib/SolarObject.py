#!/usr/bin/python3

### import guacamole libraries
import avango
import avango.gua

## import framework libraries
from lib.OrbitVisualization import OrbitVisualization

class SolarObject:

    ### constructor ###
    def __init__(self,
        NAME = "",
        TEXTURE_PATH = "",
        HIGH_EMISSIVITY = False,
        PARENT_NODE = None,
        SF_TIME_SCALE = None,
        DIAMETER = 1.0,
        ORBIT_RADIUS = 1.0,
        ORBIT_INCLINATION = 0.0, # in degrees
        ORBIT_DURATION = 0.0,
        ROTATION_INCLINATION = 0.0, # in degrees
        ROTATION_DURATION = 0.0
        ):

        if PARENT_NODE is None: # guard
            print("ERROR: missing parameters")            
            return


        ### parameters ###
        self.sf_time_scale_factor = SF_TIME_SCALE        

        self.diameter = DIAMETER * 0.000001
        self.orbit_radius = ORBIT_RADIUS * 0.000000002

        if ORBIT_DURATION > 0.0:
          self.orbit_velocity = 1.0 / ORBIT_DURATION
        else:
          self.orbit_velocity = 0.0

        if ROTATION_DURATION > 0.0:
            self.rotation_velocity = 1.0 / ROTATION_DURATION # get velocity
        else:
            self.rotation_velocity = 0.0

        self.rotation_inclination = ROTATION_INCLINATION


        ### resources ###
        # init geometries of solar object
        loader = avango.gua.nodes.TriMeshLoader() # init trimesh loader to load external meshes

        self.object_geometry = loader.create_geometry_from_file(NAME + "_geometry", "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.object_geometry.Transform.value = avango.gua.make_scale_mat(self.diameter)
        self.object_geometry.Material.value.set_uniform("ColorMap", TEXTURE_PATH)
        self.object_geometry.Material.value.set_uniform("Roughness", 0.2)
        self.object_geometry.Material.value.EnableBackfaceCulling.value = False

        if HIGH_EMISSIVITY:
            self.object_geometry.Material.value.set_uniform("Emissivity", 1.0)
            

        self.axis1_geometry = loader.create_geometry_from_file("axis1", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.axis1_geometry.Transform.value = avango.gua.make_scale_mat(0.001,self.diameter*2.5,0.001)
        self.axis1_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0, 0.0, 0.0, 1.0))
        self.axis1_geometry.Material.value.set_uniform("Emissivity", 1.0) # no shading --> render color
        self.axis1_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF # geometry does not cast shadows

        self.axis2_geometry = loader.create_geometry_from_file("axis2", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.axis2_geometry.Transform.value = avango.gua.make_scale_mat(0.001,self.diameter*2.5,0.001)
        self.axis2_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(0.0, 1.0, 0.0, 1.0))
        self.axis2_geometry.Material.value.set_uniform("Emissivity", 1.0) # no shading --> render color
        self.axis2_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF # geometry does not cast shadows

           
        # init transformation nodes for specific solar object aspects
        ## TODO: create further scenegraph nodes below here
        self.orbit_radius_node = avango.gua.nodes.TransformNode(Name = NAME + "_orbit_radius_node")
        self.orbit_radius_node.Children.value = [self.object_geometry, self.axis1_geometry, self.axis2_geometry]
        self.orbit_radius_node.Transform.value = avango.gua.make_trans_mat(self.orbit_radius, 0.0, 0.0)
        PARENT_NODE.Children.value.append(self.orbit_radius_node)


        ## TODO: create orbit visualization below here
        OrbitVisualization(PARENT_NODE, self.orbit_radius)



        # Triggers framewise evaluation of respective callback method
        self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)


    ### functions ###
    def get_orbit_node(self):
        return self.orbit_radius_node


    def update_orbit(self):
        self.orbit_radius_node.Transform.value = \
            avango.gua.make_rot_mat(self.orbit_velocity * self.sf_time_scale_factor.value, 0.0, 1.0, 0.0) * \
            self.orbit_radius_node.Transform.value


    def update_rotation(self):
        pass
        ## TODO: fill this function with code


    ### callback functions ###
    def frame_callback(self): # evaluated once per frame
        self.update_orbit()
        self.update_rotation()
