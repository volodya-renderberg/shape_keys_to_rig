#
#
#
#

bl_info = {
    "name": "Shape Keys To Rig",
    "description": "Add Shape Keys to rig depending on bone position.",
    "author": "Volodya Renderberg",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3d tools panel",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url":"https://github.com/volodya-renderberg/shape_keys_to_rig/blob/master/README.md",
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

