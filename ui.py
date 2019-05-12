import bpy

from . import funcs as fn

class SHAPEKEYSTORIG_create_panel(bpy.types.Panel):
    bl_label = 'Shape Keys Tools / Create:'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'ShKTls'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        data = fn.read_data()
        
        layout = self.layout
        
        layout.label('Make Auxiliary Bones:')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', 'Init Partent Bone').action = 'init_parent_bone'
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
    bl_label = 'Shape Keys Tools / Edit:'
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'ShKTls'
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
    from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')

    def execute(self, context):
        b,r = fn.make_target_bone(context, self.name, self.height, self.layer, from_mirror=self.from_mirror, to_mirror=self.to_mirror)
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
    from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    
    def execute(self, context):
        b,r = fn.make_shape_key(context, self.name, from_mirror=self.from_mirror, to_mirror=self.to_mirror)
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
    from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    topology = bpy.props.BoolProperty(name='Use Topology', default=False)
    
    def execute(self, context):
        b,r = fn.mirror_shape_key(context, self.name, self.topology, from_mirror=self.from_mirror, to_mirror=self.to_mirror)
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
    bpy.utils.register_class(SHAPEKEYSTORIG_create_panel)
    bpy.utils.register_class(SHAPEKEYSTORIG_edit_panel)
    bpy.utils.register_class(SHAPEKEYSTORIG_init)
    bpy.utils.register_class(SHAPEKEYSTORIG_make_target_bone)
    bpy.utils.register_class(SHAPEKEYSTORIG_make_shape_key)
    bpy.utils.register_class(SHAPEKEYSTORIG_mirror_shape_key)
    # unreg
    bpy.utils.register_class(SHAPEKEYSTORIG_unreg)
    
def unregister():
    bpy.utils.unregister_class(SHAPEKEYSTORIG_create_panel)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_edit_panel)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_init)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_make_target_bone)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_make_shape_key)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_mirror_shape_key)
    # unreg
    bpy.utils.unregister_class(SHAPEKEYSTORIG_unreg)
