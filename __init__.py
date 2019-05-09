#
#
#
#

bl_info = {
    "name": "Shape Keys to Rig",
    "description": "Add Shape Keys to rig depending on bone position.",
    "author": "Volodya Renderberg",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3d tools panel",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Rigging"}

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    from . import ui

import bpy


##### REGISTER #####

def register():
    ui.register()

def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()

