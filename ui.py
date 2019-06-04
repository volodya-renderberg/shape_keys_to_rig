import bpy

from . import funcs as fn
from . import settings

def set_mirror_sides():
	bpy.types.Scene.mirror_sides = bpy.props.EnumProperty(items = settings.SIDES, name = 'Mirror', update = None, default=settings.DEFAULT)

class SHAPEKEYSTORIG_create_panel(bpy.types.Panel):
    bl_label = 'Shape Key To Rig - Create:'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'ShKtRig'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        data = fn.read_data()
        
        layout = self.layout
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.label('')
        row.operator('shapekeystorig.manual', text='', icon='QUESTION')
        
        col = layout.column(align = True)
        col.prop(context.scene, "mirror_sides")
        
        layout.label('Make Auxiliary Bones:')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Partent Bone').action = 'init_parent_bone'
        if 'armature' in data:
            row.label('%s:%s' % (str(data.get('armature')), str(data.get('parent_bone'))))
        col.operator('shapekeystorig.make_target_bone').height=0.01
        
        layout.label('Make Shape Keys:')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Mesh').action='init_mesh'
        if 'mesh' in data:
            row.label(str(data.get('mesh')))
	#
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Root (bone)').action='root_bone'
        if 'root_bone' in data:
            row.label('%s:%s' % (str(data.get('root_bone')[0]), str(data.get('root_bone')[1])))
        #
        #col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Target-1 (bone.head)').action='target1'
        if 'target1' in data:
            row.label('%s:%s' % (str(data.get('target1')[0]), str(data.get('target1')[1])))
        #
        #col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Target-2 (bone.head)').action='target2'
        if 'target2' in data:
            row.label('%s:%s' % (str(data.get('target2')[0]), str(data.get('target2')[1])))
            
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init distance to ON').action='on_distance'
        if 'on_distance' in data:
            row.label(str(data.get('on_distance')))
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init distance to OFF').action='off_distance'
        if 'off_distance' in data:
            row.label(str(data.get('off_distance')))
            
        col = layout.column(align = True)
        col.operator('shapekeystorig.make_shape_key')
        
        #layout.label('Off')
        #col = layout.column(align = True)
        #col.operator('shapekeystorig.unreg')
        
class SHAPEKEYSTORIG_edit_panel(bpy.types.Panel):
    bl_label = 'In-Between Shape Keys:'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    #bl_category = 'ShKTls'
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        data = fn.read_data()
        mesh_name = data.get('mesh')
        mesh = None
        if mesh_name and mesh_name in bpy.data.objects:
            mesh = bpy.data.objects[mesh_name]
        
        layout = self.layout
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.label('')
        row.operator('shapekeystorig.manual', text='', icon='QUESTION')
        
        col = layout.column(align = True)
        col.prop(context.scene, "mirror_sides")
        
        '''
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Mesh').action='init_mesh'
        if 'mesh' in data:
            row.label(str(data.get('mesh')))
        
        col = layout.column(align = True)
        if mesh and mesh.data.shape_keys:
            for key in mesh.data.shape_keys.key_blocks.keys():
                if not key.startswith(fn.SHAPE_KEY_PREFIX):
                    continue
                row=col.row(align = True)
                row.label(key)
                row.operator('shapekeystorig.mirror_shape_key', text='mirror').name=key
        '''
        
        col = layout.column(align = True)
        col.operator('shapekeystorig.in_between', text='ADD In-between for active')
        
        col = layout.column(align = True)
        col.operator('shapekeystorig.remove_in_between', text='REMOVE In-between')
        
        col = layout.column(align = True)
        col.operator('shapekeystorig.vertices_to_basis', text='Vertices to Basis')
        
        col = layout.column(align = True)
        row = col.row(align=True)
        row.operator('shapekeystorig.mirror_active_shape_key', text='MIRROR active /Step 1')
        row.operator('shapekeystorig.mirror_active_shape_key_step2')

class SHAPEKEYSTORIG_init(bpy.types.Operator):
    bl_idname = "shapekeystorig.init"
    bl_label = "Init"
    
    action = bpy.props.StringProperty()

    def execute(self, context):
        b=False
        r='Nothing!'
        if self.action == 'init_parent_bone':
            b,r = fn.init_parent_bone(context)
        elif self.action == 'init_mesh':
            b,r = fn.init_mesh(context)
        elif self.action == 'root_bone':
            b,r = fn.init_target(context, 'root_bone')
        elif self.action == 'target1':
            b,r = fn.init_target(context, 'target1')
        elif self.action == 'target2':
            b,r = fn.init_target(context, 'target2')
        elif self.action == 'on_distance':
            b,r = fn.init_distance(context, 'on_distance')
        elif self.action == 'off_distance':
            b,r = fn.init_distance(context, 'off_distance')
        # reports
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
class SHAPEKEYSTORIG_make_target_bone(bpy.types.Operator):
    bl_idname = "shapekeystorig.make_target_bone"
    bl_label = "Make Bone"
    
    name = bpy.props.StringProperty(name='Name:')
    height = bpy.props.FloatProperty(name='Height Bone')
    layer = bpy.props.IntProperty(name='Layer', default=27)
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')

    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
                        
        b,r = fn.make_target_bone(context, self.name, self.height, self.layer, from_mirror=from_mirror, to_mirror=to_mirror)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_make_shape_key(bpy.types.Operator):
    bl_idname = "shapekeystorig.make_shape_key"
    bl_label = "Make Shape Key"
    
    name = bpy.props.StringProperty(name='Name:')
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    
    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
        b,r = fn.make_shape_key(context, self.name, from_mirror=from_mirror, to_mirror=to_mirror)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_mirror_shape_key(bpy.types.Operator):
    bl_idname = "shapekeystorig.mirror_shape_key"
    bl_label = "Mirror Shape Key"
    
    name = bpy.props.StringProperty(name='Name:')
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    topology = bpy.props.BoolProperty(name='Use Topology', default=False)
    
    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
        b,r = fn.mirror_shape_key(context, self.name, self.topology, from_mirror=from_mirror, to_mirror=to_mirror)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_mirror_active_shape_key(bpy.types.Operator):
    bl_idname = "shapekeystorig.mirror_active_shape_key"
    bl_label = "Mirror Shape Key"
    
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    topology = bpy.props.BoolProperty(name='Use Topology', default=False)
    
    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
        sh_key = bpy.context.object.active_shape_key
        if not sh_key:
            self.report({'WARNING'}, 'No active Shape Key!')
            return{'FINISHED'}
        b,r = fn.mirror_shape_key(context, sh_key.name, self.topology, from_mirror=from_mirror, to_mirror=to_mirror, active=True)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_mirror_active_shape_key_step2(bpy.types.Operator):
    bl_idname = "shapekeystorig.mirror_active_shape_key_step2"
    bl_label = "Step 2"
    
    def execute(self, context):
        b,r = fn.mirror_step_2(context)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
class SHAPEKEYSTORIG_in_between(bpy.types.Operator):
    bl_idname = "shapekeystorig.in_between"
    #bl_label = "In-between"
    bl_label = "Are you sure?"
    
    #method = bpy.props.BoolProperty(name='between adjacent', default = True)
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    
    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
        b,r = fn.in_between(context, from_mirror=from_mirror, to_mirror=to_mirror)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
# shapekeystorig.remove_in_between
class SHAPEKEYSTORIG_remove_in_between(bpy.types.Operator):
    bl_idname = "shapekeystorig.remove_in_between"
    bl_label = "Are you sure?"
    
    def execute(self, context):
        from_mirror, to_mirror = settings.DATA[context.scene.mirror_sides]
        b,r = fn.remove_in_between(context, from_mirror, to_mirror)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_vertices_to_basis(bpy.types.Operator):
    bl_idname = "shapekeystorig.vertices_to_basis"
    bl_label = "Are you sure?"
    
    def execute(self, context):
        b,r = fn.selected_vertices_to_basis_shape_key(context)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class SHAPEKEYSTORIG_manual(bpy.types.Operator):
    bl_idname = "shapekeystorig.manual"
    bl_label = "Help"
    
    def execute(self, context):
        self.report({'INFO'}, 'It is Manual')
        return{'FINISHED'}

class SHAPEKEYSTORIG_unreg(bpy.types.Operator):
    bl_idname = "shapekeystorig.unreg"
    bl_label = "Unregister"

    def execute(self, context):
        unregister()
        return{'FINISHED'}

def register():
    bpy.utils.register_class(SHAPEKEYSTORIG_create_panel)
    bpy.utils.register_class(SHAPEKEYSTORIG_edit_panel)
    bpy.utils.register_class(SHAPEKEYSTORIG_init)
    bpy.utils.register_class(SHAPEKEYSTORIG_make_target_bone)
    bpy.utils.register_class(SHAPEKEYSTORIG_make_shape_key)
    bpy.utils.register_class(SHAPEKEYSTORIG_mirror_shape_key)
    bpy.utils.register_class(SHAPEKEYSTORIG_in_between)
    bpy.utils.register_class(SHAPEKEYSTORIG_remove_in_between)
    bpy.utils.register_class(SHAPEKEYSTORIG_mirror_active_shape_key)
    bpy.utils.register_class(SHAPEKEYSTORIG_mirror_active_shape_key_step2)
    bpy.utils.register_class(SHAPEKEYSTORIG_vertices_to_basis)
    bpy.utils.register_class(SHAPEKEYSTORIG_manual)
    # unreg
    bpy.utils.register_class(SHAPEKEYSTORIG_unreg)
    set_mirror_sides()
    
def unregister():
    bpy.utils.unregister_class(SHAPEKEYSTORIG_create_panel)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_edit_panel)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_init)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_make_target_bone)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_make_shape_key)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_mirror_shape_key)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_in_between)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_remove_in_between)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_mirror_active_shape_key)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_mirror_active_shape_key_step2)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_vertices_to_basis)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_manual)
    # unreg
    bpy.utils.unregister_class(SHAPEKEYSTORIG_unreg)
