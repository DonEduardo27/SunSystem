#!/usr/bin/python3

### import guacamole libraries
import avango
import avango.gua

### import application libraries
from lib.SimpleViewingSetup import *
from lib.SolarSystem import SolarSystem
from lib.Device import *
from lib.Navigation import SteeringNavigation


### global variables ###
NAVIGATION_MODE = "Spacemouse"
#NAVIGATION_MODE = "Keyboard"


def start():

    ## init scenegraph
    scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
    
    ## init solar system
    solar_system = SolarSystem()
    solar_system.my_constructor(scenegraph.Root.value)

    ## init navigation technique
    steering_navigation = SteeringNavigation()
    steering_navigation.set_start_transformation(avango.gua.make_trans_mat(0.0,0.1,0.3)) # move camera to initial position
        
    if NAVIGATION_MODE == "Spacemouse":
        device_input = NewSpacemouseInput()
        device_input.my_constructor("gua-device-spacemouse")
            
        steering_navigation.my_constructor(device_input.mf_dof, 0.1, 1.0) # connect navigation with spacemouse input

    elif NAVIGATION_MODE == "Keyboard":
        device_input = KeyboardInput()
        device_input.my_constructor("gua-device-keyboard0")

        steering_navigation.my_constructor(device_input.mf_dof) # connect navigation with keyboard input

    else:    
        print("Error: NAVIGATION_MODE " + NAVIGATION_MODE + " is not known.")
        return


    ## init viewing setup
    viewing_setup = SimpleViewingSetup(scenegraph, "mono")
    viewing_setup.connect_navigation_matrix(steering_navigation.sf_nav_mat)
    steering_navigation.set_rotation_center_offset(viewing_setup.get_head_position())

    viewing_setup.run(locals(), globals())



### helper functions ###

## print the subgraph under a given node to the console
def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])


## print all fields of a field container to the console
def print_fields(node, print_values = False):
  for i in range(node.get_num_fields()):
    field = node.get_field(i)
    print("→ {0} <{1}>".format(field._get_name(), field.__class__.__name__))
    if print_values:
      print("  with value '{0}'".format(field.value))


if __name__ == '__main__':
    start()