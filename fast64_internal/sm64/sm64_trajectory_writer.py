from collections import defaultdict
from bpy.utils import register_class, unregister_class
import bpy, os, math, re, shutil

from .sm64_constants import *
from .sm64_objects import *
from .sm64_collision import *
from .sm64_geolayout_writer import *
from .sm64_texscroll import *
from .sm64_utility import *

from ..utility import *
from ..panels import SM64_Panel
from ..operators import ObjectDataExporter







class SM64_ExportTrajectory(ObjectDataExporter):
    # set bl_ properties
    bl_idname = "object.sm64_export_trajectory"
    bl_label = "Export Trajectory"
    bl_options = {"REGISTER", "UNDO", "PRESET"}
    
    def execute(self, context):
        romfileOutput = None
        tempROM = None
        try:    
            if context.mode != "OBJECT":
                raise PluginError("Operator can only be used in object mode.")
            allObjs = context.selected_objects
            if len(allObjs) == 0:
                raise PluginError("No objects selected.")
            obj = context.selected_objects[0]
            if obj is None or obj.sm64_obj_type != "Trajectory Point":
                raise PluginError("Is not a trajectory point")
            
            if obj.name != "trajectory.000":
                raise PluginError('the name must "trajectory.000"')
            #obj = context.selected_objects[0]
            #if not isinstance(obj.data, bpy.types.Object.trajectory):
             #   raise PluginError("Object is not a mesh.")
            
        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}
        
        try:
           
       #    self.store_object_data()
            
      #      trajectoryName = context.scene.trajectoryName
     #       trajectoryDir = os.path.join(trajectoryDir, trajectoryName)
    #        trajectoryPath = os.path.join(trajectoryDir, "trajectory.c")
   #         if not os.path.exists(trajectoryDir):
  #              os.mkdir(trajectoryDir)
 #           
#            if not os.path.exists(trajectoryPath):
#                fic = open(trajectoryPath , "w", newline="\n")
#                fic.write("bonjour tout le monde \n")
#                fic.close()                  XDDDDDDDDDDDDDDD
            
            augment = 0
            trajectory_array = [] 
            number_trajectory_point = 0
            trajectory_name = "trajectory.00" + str(number_trajectory_point)
            loop = 0
            while loop == 0:
                if bpy.data.objects.get(trajectory_name) is not None: 
                  #
                    
                
                    obj = bpy.data.objects.get(trajectory_name)
                    
                    posx = obj.location.x
                    posx = int(posx * 100)
                    posy = obj.location.z
                    posy = int(posy * 100)
                    posz = obj.location.y
                    posz = int(posz * -100)
                    
                    posx = str(posx)
                    posx = list(posx)
                    posx = "".join(posx)
                    
                    posy = str(posy)
                    posy = list(posy)
                    posy = "".join(posy)
                        
                    posz = str(posz)
                    posz = list(posz)
                    posz = "".join(posz)
                    
                    
                    
                    trajectory_array.append('    TRAJECTORY_POS( ' + str(number_trajectory_point) + ' , /*pos*/  ' + posx + ', ' + posy + ', ' + posz + '),\n') 
                    
                    bpy.context.active_object.select_set(False)
                    number_trajectory_point += 1
                    trajectory_name = "trajectory.00" + str(number_trajectory_point)
                    
                else:
                    loop = 1
                
                        

            
            

            
                    

            
            
                
                

            trajectory_array.append("    TRAJECTORY_END(), // tank Indigo SM64") 
            trajectory_array = "".join(trajectory_array)
            self.report({"INFO"}, "Success!" + "\nallo lol")           
            self.report({"INFO"}, trajectory_array)

            return {"FINISHED"} 



        
        
        
        except:
            return {"CANCELLED"}
            
   



class SM64_ExportTrajectoryPanel(SM64_Panel):
    bl_idname = "SM64_PT_export_trajectory"
    bl_label = "SM64 Trajectory Exporter"
    goal = "Create Trajectory"
    decomp_only = True
    

    # called every frame
    def draw(self, context):
        col = self.layout.column()
        if context.scene.fast64.sm64.exportType != "C":
            col.label(text="This is for decomp only.")
        col.operator(SM64_ExportTrajectory.bl_idname)
        customExportWarning(col)
            
            

        
        
sm64_trajectory_classes = (SM64_ExportTrajectory,)

sm64_trajectory_panel_classes = (SM64_ExportTrajectoryPanel,)



def sm64_trajectory_panel_register():
    for cls in sm64_trajectory_panel_classes:
        register_class(cls)


def sm64_trajectory_panel_unregister():
    for cls in sm64_trajectory_panel_classes:
        unregister_class(cls)
        

def sm64_trajectory_register():
    for cls in sm64_trajectory_classes:
        register_class(cls)
        
    bpy.types.Scene.trajectoryCustomExport = bpy.props.BoolProperty(name="Custom Export Path")
    bpy.types.Scene.trajectoryName = bpy.props.StringProperty(name="Name", default="Trajectory")
    bpy.types.Scene.trajectoryOption = bpy.props.EnumProperty(name="Trajectory", items=enumTrajectoryName, default="Trajectory")




def sm64_trajectory_unregister():
    for cls in reversed(sm64_trajectory_classes):
        unregister_class(cls)
        
    del bpy.types.Scene.trajectoryCustomExport




