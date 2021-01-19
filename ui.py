import webbrowser

import bpy

from . import funcs as fn
from . import settings

def set_mirror_sides():
    bpy.types.Scene.mirror_sides = bpy.props.EnumProperty(items = settings.SIDES, name = 'Mirror', update = None, default=settings.DEFAULT)

class SHAPEKEYSTORIG_create_panel(bpy.types.Panel):
    bl_label = 'Shape Key To Rig - Create:'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'ShKtRig'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        data = fn.read_data()
        
        layout = self.layout
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='')
        row.operator('shapekeystorig.manual', text='', icon='QUESTION')
        
        col = layout.column(align = True)
        col.prop(context.scene, "mirror_sides")
        
        layout.label(text='Make Auxiliary Bones:')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Partent Bone').action = 'init_parent_bone'
        if 'armature' in data:
            row.label(text='%s:%s' % (str(data.get('armature')), str(data.get('parent_bone'))))
        col.operator('shapekeystorig.make_target_bone').height=0.01
        
        layout.label(text='Make Shape Keys:')
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Mesh').action='init_mesh'
        if 'mesh' in data:
            row.label(text=str(data.get('mesh')))
	#
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Root (bone)').action='root_bone'
        if 'root_bone' in data:
            row.label(text='%s:%s' % (str(data.get('root_bone')[0]), str(data.get('root_bone')[1])))
        #
        #col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Target-1 (bone.head)').action='target1'
        if 'target1' in data:
            row.label(text='%s:%s' % (str(data.get('target1')[0]), str(data.get('target1')[1])))
        #
        #col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Target-2 (bone.head)').action='target2'
        if 'target2' in data:
            row.label(text='%s:%s' % (str(data.get('target2')[0]), str(data.get('target2')[1])))
            
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init distance to ON').action='on_distance'
        if 'on_distance' in data:
            row.label(text=str(data.get('on_distance')))
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init distance to OFF').action='off_distance'
        if 'off_distance' in data:
            row.label(text=str(data.get('off_distance')))
            
        col = layout.column(align = True)
        col.operator('shapekeystorig.make_shape_key')
        
        #layout.label(text='Off')
        #col = layout.column(align = True)
        #col.operator('shapekeystorig.unreg')
        
class SHAPEKEYSTORIG_edit_panel(bpy.types.Panel):
    bl_label = 'In-Between Shape Keys:'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    #bl_category = 'ShKTls'
    #bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        if context.object.type == 'MESH':
            return(True)
        return(False)
    
    def draw(self, context):
        data = fn.read_data()
        mesh_name = data.get('mesh')
        mesh = None
        if mesh_name and mesh_name in bpy.data.objects:
            mesh = bpy.data.objects[mesh_name]
        
        layout = self.layout
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='')
        row.operator('shapekeystorig.manual', text='', icon='QUESTION')
        
        col = layout.column(align = True)
        col.prop(context.scene, "mirror_sides")
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.in_between', text='ADD In-between for active')
        #
        #col = layout.column(align = True)
        row.operator('shapekeystorig.remove_in_between', text='REMOVE In-between')
        
        col = layout.column(align = True)
        col.label(text='Copy Shape Key:')
        row = col.row(align = True)
        row.operator('shapekeystorig.init', text='Init Source').action='source_shape_key'
        if 'source_shape_key' in data:
            row.label(text=str(data.get('source_shape_key')))

        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('shapekeystorig.copy_shape_key').action="All"
        row.operator('shapekeystorig.copy_shape_key', text = "To selected vertices").action="selected"
        
        col = layout.column(align = True)
        col.operator('shapekeystorig.vertices_to_basis', text='Vertices to Basis')
        
        col = layout.column(align = True)
        col.label(text='Mirror Shape Key:')
        row = col.row(align=True)
        row.operator('shapekeystorig.mirror_active_shape_key', text='MIRROR active /Step 1')
        row.operator('shapekeystorig.mirror_active_shape_key_step2')
        
        col = layout.column(align = True)
        col.label(text='Import / Export data:')
        row = col.row(align=True)
        row.operator('shapekeystorig.import_export_data', text='Export All Shape Keys').action='export_all'
        row.operator('shapekeystorig.import_export_data', text='Export active Shape Key').action='export_single'
        row = col.row(align=True)
        row.operator('shapekeystorig.import_export_data', text='Import All Shape Keys').action='import_all'
        row.operator('shapekeystorig.import_export_data', text='Import to active Shape Key').action='import_single'

        col = layout.column(align = True)
        col.label(text='Import from Meshes:')
        row = col.row(align=True)
        row.operator('shapekeystorig.insert_sk_from_selected_mesh', text='Import from Selected Objects')

class SHAPEKEYSTORIG_init(bpy.types.Operator):
    bl_idname = "shapekeystorig.init"
    bl_label = "Init"
    
    action: bpy.props.StringProperty()

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
        elif self.action == 'source_shape_key':
            b,r = fn.init_shape_key(context, 'source_shape_key')
        # reports
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}
    
class SHAPEKEYSTORIG_make_target_bone(bpy.types.Operator):
    bl_idname = "shapekeystorig.make_target_bone"
    bl_label = "Make Bone"
    
    name: bpy.props.StringProperty(name='Name:')
    height: bpy.props.FloatProperty(name='Height Bone')
    layer: bpy.props.IntProperty(name='Layer', default=27)
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
    
    name: bpy.props.StringProperty(name='Name:')
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
    
    name: bpy.props.StringProperty(name='Name:')
    #from_mirror = bpy.props.StringProperty(name='From Mirror:', default='.L')
    #to_mirror = bpy.props.StringProperty(name='To Mirror:', default='.R')
    topology: bpy.props.BoolProperty(name='Use Topology', default=False)
    
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
    topology: bpy.props.BoolProperty(name='Use Topology', default=False)
    
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
    
class SHAPEKEYSTORIG_copy_shape_key(bpy.types.Operator):
    bl_idname = "shapekeystorig.copy_shape_key"
    bl_label = "Paste to active"

    action: bpy.props.StringProperty()
    
    def execute(self, context):
        if self.action == "selected":
            b,r = fn.copy_shape_key(context, for_selected_vertices=True)
        else:
            b,r = fn.copy_shape_key(context)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}

class SHAPEKEYSTORIG_insert_sk_from_selected_mesh(bpy.types.Operator):
    bl_idname = "shapekeystorig.insert_sk_from_selected_mesh"
    bl_label = "Insert from selected mesh"
    
    def execute(self, context):
        b,r = fn.insert_sk_from_selected_mesh(context)
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        return{'FINISHED'}

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
        webbrowser.open_new_tab('https://github.com/volodya-renderberg/shape_keys_to_rig/blob/master/README.md')
        #self.report({'INFO'}, 'It is Manual')
        return{'FINISHED'}

class SHAPEKEYSTORIG_unreg(bpy.types.Operator):
    bl_idname = "shapekeystorig.unreg"
    bl_label = "Unregister"

    def execute(self, context):
        unregister()
        return{'FINISHED'}
    
class SHAPEKEYSTORIG_import_export_data(bpy.types.Operator):
    bl_idname = "shapekeystorig.import_export_data"
    bl_label = "Import / Export data"
    
    action: bpy.props.StringProperty()

    def execute(self, context):
        if self.action == 'export_all':
            b,r = fn.export_shape_keys(context, all=True)
        if self.action == 'export_single':
            b,r = fn.export_shape_keys(context, all=False)
        if self.action == 'import_all':
            b,r = fn.import_shape_keys(context, all=True)
        if self.action == 'import_single':
            b,r = fn.import_shape_keys(context, all=False)
        else:
            return{'FINISHED'}
        if b:
            self.report({'INFO'}, r)
        else:
            self.report({'WARNING'}, r)
        
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
    bpy.utils.register_class(SHAPEKEYSTORIG_copy_shape_key)
    bpy.utils.register_class(SHAPEKEYSTORIG_insert_sk_from_selected_mesh)
    bpy.utils.register_class(SHAPEKEYSTORIG_import_export_data)
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
    bpy.utils.unregister_class(SHAPEKEYSTORIG_copy_shape_key)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_insert_sk_from_selected_mesh)
    bpy.utils.unregister_class(SHAPEKEYSTORIG_import_export_data)
    # unreg
    bpy.utils.unregister_class(SHAPEKEYSTORIG_unreg)
