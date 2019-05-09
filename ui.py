import bpy

from . import funcs as fn

class SHAPEKEYSTORIG_main_panel(bpy.types.Panel):
    bl_label = 'Shape Keys to Rig:'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'ShKytR'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        data = fn.read_data()
        print(data)
        
        layout = self.layout
        
        layout.label('Make Bones')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init_parent')
        if 'armature' in data:
            row.label('%s:%s' % (str(data.get('armature')), str(data.get('parent_bone'))))
        col.operator('shapekeystorig.make_target_bone').height=0.01
        
        #layout.label('Off')
        #col = layout.column(align = True)
        #col.operator('shapekeystorig.unreg')

class SHAPEKEYSTORIG_init_parent(bpy.types.Operator):
    bl_idname = "shapekeystorig.init_parent"
    bl_label = "Init Parent Bone"

    def execute(self, context):
        b,r = fn.init_parent_bone(context)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
class SHAPEKEYSTORIG_make_target_bone(bpy.types.Operator):
    bl_idname = "shapekeystorig.make_target_bone"
    bl_label = "Make Target Bone"
    
    name = bpy.props.StringProperty(name='Name:')
    height = bpy.props.FloatProperty(name='Height Bone')

    def execute(self, context):
        b,r = fn.make_target_bone(context, self.name, self.height)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SHAPEKEYSTORIG_unreg(bpy.types.Operator):
    bl_idname = "shapekeystorig.unreg"
    bl_label = "Unregister"

    def execute(self, context):
        unregister()
        return{'FINISHED'}

def register():
    bpy.utils.register_class(SHAPEKEYSTORIG_main_panel)
    bpy.utils.register_class(SHAPEKEYSTORIG_init_parent)
    bpy.utils.register_class(SHAPEKEYSTORIG_make_target_bone)
    # unreg
    bpy.utils.register_class(SHAPEKEYSTORIG_unreg)
    
def unregister():
    bpy.utils.unregister_class(SHAPEKEYSTORIG_main_panel)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_init_parent)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_make_target_bone)
    # unreg
    bpy.utils.unregister_class(SHAPEKEYSTORIG_unreg)
