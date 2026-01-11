bl_info = {
    "name": "Procedural Eyeball Generator",
    "blender": (4, 2, 0),
    "category": "Add Mesh",
    "version": (0, 0, 1),
    "author": "Preston Chavez",
    "description": "Ready-to-Go Eyeball customizer ready for finalization",
    "location": "Add > Mesh > Prefab Meshes",
}

import bpy
from bpy.types import Operator, Menu
from bpy.props import StringProperty
from . mesh_library import create_prefab_instance


PREFABS = {
    "human_eye": {
        "blend_file": "human_eye",
        "collection": "Human_Eye"
    },
    "human_eye_stylized": {
        "blend_file": "human_eye_stylized",
        "collection": "Human_Eye_Stylized"
    },
    "aquatic_vertabrate_eye": {
        "blend_file": "aquatic_vertabrate_eye",
        "collection": "Aquatic_Vertabrate_Eye"
    },
    "reptile_eye": {
        "blend_file": "reptile_eye",
        "collection": "Reptile_Eye"
    },
}


class MESH_OT_add_prefab(Operator):
    """Add a prefabricated eyeball mesh"""
    bl_idname = "mesh.add_prefab"
    bl_label = "Add Prefab Eyeball"
    bl_options = {'REGISTER', 'UNDO'}
    
    prefab_type: StringProperty(
        name="Prefab Type",
        description="Type of prefab eyeball to add",
        default="human_eye"
    )
    
    def execute(self, context):
        try:
            if self.prefab_type not in PREFABS:
                raise ValueError(f"Unknown prefab type: {self.prefab_type}")
            
            prefab_info = PREFABS[self.prefab_type]
            create_prefab_instance(
                prefab_info["blend_file"],
                prefab_info["collection"],
                context
            )
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load prefab: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class MESH_MT_add_prefab(Menu):
    """Menu for prefab eyeballs"""
    bl_idname = "MESH_MT_add_prefab"
    bl_label = "Prefab Eyeballs"
    
    def draw(self, context):
        layout = self.layout
        
        # Dynamically create menu items from PREFABS dictionary
        for prefab_id, prefab_info in PREFABS.items():
            # Format the display name (e.g., "human_eye" becomes "Human Eye")
            display_name = prefab_id.replace("_", " ").title()
            layout.operator("mesh.add_prefab", text=display_name).prefab_type = prefab_id


def menu_func_add(self, context):
    self.layout.menu("MESH_MT_add_prefab", icon='PLUGIN')


def register():
    bpy.utils.register_class(MESH_OT_add_prefab)
    bpy.utils.register_class(MESH_MT_add_prefab)
    #bpy.types.VIEW3D_MT_mesh_add.append(menu_func_add)

try:
        mesh_add_menu.remove(menu_func_add)
    except: 
        pass
    
    # Add the menu (it will appear at the end by default)
    mesh_add_menu.append(menu_func_add)


def unregister():
    bpy. utils.unregister_class(MESH_OT_add_prefab)
    bpy.utils.unregister_class(MESH_MT_add_prefab)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_add)


if __name__ == "__main__": 
    register()

#def unregister():
   # bpy.utils.unregister_class(MESH_OT_add_prefab)
   # bpy.utils.unregister_class(MESH_MT_add_prefab)
   # bpy.types.VIEW3D_MT_mesh_add. remove(menu_func_add)


#if __name__ == "__main__":
  #  register()