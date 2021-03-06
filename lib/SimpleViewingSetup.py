#!/usr/bin/python3

### import guacamole libraries
import avango
import avango.gua
import avango.daemon

### import application libraries
from lib.GuaVE import GuaVE


class SimpleViewingSetup:

    ### constructor
    def __init__(self, SCENEGRAPH, STEREO_MODE):

        ### external references ###
        self.SCENEGRAPH = SCENEGRAPH

        ### parameters ###
        self.window_size = avango.gua.Vec2ui(2560, 1440) # in pixels
        self.screen_dimensions = avango.gua.Vec2(0.595, 0.335) # in meter
        self.screen_mat = avango.gua.make_trans_mat(0.0, 0.0, 0.0)

        ### resources ###
        self.shell = GuaVE()

        ## init window
        self.window = avango.gua.nodes.GlfwWindow(Title = "window")
        self.window.Size.value = self.window_size
        self.window.LeftResolution.value = self.window_size
        
        avango.gua.register_window(self.window.Title.value, self.window) 

        ## init viewer
        self.viewer = avango.gua.nodes.Viewer()
        self.viewer.SceneGraphs.value = [self.SCENEGRAPH]
        self.viewer.Windows.value = [self.window]
        self.viewer.DesiredFPS.value = 60.0 # in Hz

        ## init passes & render pipeline description
        self.resolve_pass = avango.gua.nodes.ResolvePassDescription()
        self.resolve_pass.EnableSSAO.value = False
        self.resolve_pass.SSAOIntensity.value = 4.0
        self.resolve_pass.SSAOFalloff.value = 10.0
        self.resolve_pass.SSAORadius.value = 7.0
        self.resolve_pass.EnvironmentLightingColor.value = avango.gua.Color(0.1, 0.1, 0.1)
        self.resolve_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
        self.resolve_pass.Exposure.value = 1.0
     
        self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
        self.resolve_pass.BackgroundTexture.value = "/opt/guacamole/resources/skymaps/stars.jpg"

        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes = [])
        self.pipeline_description.EnableABuffer.value = True        
        self.pipeline_description.Passes.value.append(avango.gua.nodes.TriMeshPassDescription())
        self.pipeline_description.Passes.value.append(avango.gua.nodes.LightVisibilityPassDescription())
        self.pipeline_description.Passes.value.append(self.resolve_pass)
        self.pipeline_description.Passes.value.append(avango.gua.nodes.SSAAPassDescription())

        ## init navigation node
        self.navigation_node = avango.gua.nodes.TransformNode(Name = "navigation_node")
        self.SCENEGRAPH.Root.value.Children.value.append(self.navigation_node)
        
        ## init head node
        self.head_node = avango.gua.nodes.TransformNode(Name = "head_node")
        self.head_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.6)
        self.navigation_node.Children.value.append(self.head_node)


        ## init screen node
        self.screen_node = avango.gua.nodes.ScreenNode(Name = "screen_node")
        self.screen_node.Width.value = self.screen_dimensions.x
        self.screen_node.Height.value = self.screen_dimensions.y
        self.screen_node.Transform.value = self.screen_mat
        self.navigation_node.Children.value.append(self.screen_node)
        

        ## init camera node
        self.camera_node = avango.gua.nodes.CameraNode(Name = "camera_node")
        self.camera_node.SceneGraph.value = self.SCENEGRAPH.Name.value
        self.camera_node.LeftScreenPath.value = self.screen_node.Path.value
        self.camera_node.NearClip.value = 0.1 # in meter
        self.camera_node.FarClip.value = 100.0 # in meter
        self.camera_node.Resolution.value = self.window_size
        self.camera_node.OutputWindowName.value = self.window.Title.value
        self.camera_node.PipelineDescription.value = self.pipeline_description
        self.head_node.Children.value = [self.camera_node]



    ### functions ###
    def run(self, LOCALS, GLOBALS):
        self.shell.start(LOCALS, GLOBALS)
        self.viewer.run()


    def list_variabels(self):
        self.shell.list_variables()


    def connect_navigation_matrix(self, SF_MATRIX):
        self.navigation_node.Transform.connect_from(SF_MATRIX)


    def get_head_position(self): # get relative head position (towards screen)
        return self.head_node.Transform.value.get_translate()