#!/usr/bin/python3

### import guacamole libraries
import avango
import avango.gua

### import python libraries
import math

class OrbitVisualization:

    ### constructor
    def __init__(self, PARENT_NODE = None , ORBIT_RADIUS = 1.0):

        if PARENT_NODE is None: # guard
            print("ERROR: missing parameters")            
            return

        ### parameters ###
        self.number_of_segments = 100
        self.thickness = 0.001  
        self.color = avango.gua.Color(1.0,1.0,1.0)
        
        ## init geometry
        loader = avango.gua.nodes.TriMeshLoader() # init trimesh loader

        for i in range(self.number_of_segments):
            segment_angle  = 360.0 / self.number_of_segments
            segment_length = (math.pi * 2.0 * ORBIT_RADIUS) / self.number_of_segments
     
            geometry = loader.create_geometry_from_file("orbit_segment_{0}".format(str(i)), "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
            geometry.Transform.value = \
                avango.gua.make_rot_mat(i * segment_angle, 0.0, 1.0, 0.0) * \
                avango.gua.make_trans_mat(ORBIT_RADIUS, 0.0, 0.0) * \
                avango.gua.make_scale_mat(self.thickness, self.thickness, segment_length)
            geometry.Material.value.set_uniform("Color", avango.gua.Vec4(self.color.r, self.color.g, self.color.b, 1.0))
            geometry.Material.value.set_uniform("Emissivity", 0.5)
            geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
    
            PARENT_NODE.Children.value.append(geometry)