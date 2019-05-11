import bpy

import os
import tempfile
import json

ARMATURE_DATA_FILE_NAME = '.shape_keys_to_rig_armature_data.json' # keys: armature, parent_bone, mesh
MESH_DATA_FILE_NAME = '.shape_keys_to_rig_mesh_data.json' # keys: mesh, 
BONE_PREFIX = 'AUXBS'
SHAPE_KEY_PREFIX = 'aux'

# data_type (str) - in 'Armature', 'Mesh'
def write_data(data, data_type='Armature', clean=False):
    if data_type=='Armature':
        path = os.path.join(tempfile.gettempdir(), ARMATURE_DATA_FILE_NAME)
    elif data_type=='Mesh':
        path = os.path.join(tempfile.gettempdir(), MESH_DATA_FILE_NAME)
    else:
        return
    #
    if not os.path.exists(path) or clean:
        with open(path, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
    else:
        with open(path) as json_file:
            rdata = json.load(json_file)
        for key in data:
            rdata[key] = data[key]
        with open(path, 'w') as outfile:
            json.dump(rdata, outfile, sort_keys=True, indent=4)

# data_type (str) - in 'Armature', 'Mesh'
def read_data(data_type='Armature'):
    if data_type=='Armature':
        path = os.path.join(tempfile.gettempdir(), ARMATURE_DATA_FILE_NAME)
    elif data_type=='Mesh':
        path = os.path.join(tempfile.gettempdir(), MESH_DATA_FILE_NAME)
    else:
        return
    #
    if not os.path.exists(path):
        return({})
    with open(path) as json_file:
        data = json.load(json_file)
    return(data)

def init_parent_bone(context):
    armature = context.object
    if not armature:
        return(False, 'No selected object!')
    if armature.type != 'ARMATURE':
        return(False, 'Selected object is not "ARMATURE"!')
    pose_bones = context.selected_pose_bones
    if not pose_bones:
        return(False, 'Pose bones is not selected!')
    parent_bone = pose_bones[0]
    
    write_data({'armature':armature.name, 'parent_bone': parent_bone.name})
    
    return(True, 'parent bone - %s:%s' % (armature.name, parent_bone.name))

def init_mesh(context):
    ob = context.object
    if not ob:
        return(False, 'No selected object!')
    if ob.type != 'MESH':
        return(False, 'Selected object is not "MESH"!')
    
    write_data({'mesh': ob.name})
    
    return(True, 'mesh - %s' % ob.name)

def init_target(context, target_name):
    armature = context.object
    if not armature:
        return(False, 'No selected object!')
    if armature.type != 'ARMATURE':
        return(False, 'Selected object is not "ARMATURE"!')
    pose_bones = context.selected_pose_bones
    if not pose_bones:
        return(False, 'Pose bones is not selected!')
    bone = pose_bones[0]
    
    write_data({target_name: [armature.name, bone.name]})
    
    return(True, '%s - %s:%s' % (target_name, armature.name, bone.name))

def init_distance(context, distance_name):
    data = read_data()
    
    # get head positions
    heads = []
    for target_name in ['target1','target2']:
        if not target_name in data:
            return(False, '"%s" not defined!' % target_name)
        armature_name = data[target_name][0]
        bone_name = data[target_name][1]
        if not armature_name in bpy.data.objects:
            return(False, 'No object with this name("%s") was found!' % armature_name)
        if not bone_name in bpy.data.objects[armature_name].pose.bones:
            return(False, 'No PoseBone with this name("%s") was found!' % bone_name)
        bone = bpy.data.objects[armature_name].pose.bones[bone_name]
        heads.append(tuple(bone.head))
        
    # calculate distance
    distance = pow((pow((heads[1][0] - heads[0][0]), 2) + pow((heads[1][1] - heads[0][1]), 2) + pow((heads[1][2] - heads[0][2]), 2)), 0.5)
    write_data({distance_name: distance})
    
    return(True, '%s - %s' % (distance_name, str(distance)))

def make_target_bone(context, name, height, layer, from_mirror='.L', to_mirror='.R'):
    pass
    # (1) testing
    if not name:
        return(False, 'Name not specified!')
    if not height:
        return(False, 'Height not specified!')
    if layer>31:
        return(False, 'layer number is greater than the allowed value!')
    
    # (2)
    pose_bones = context.selected_pose_bones
    if not pose_bones:
        return(False, 'Pose bones is not selected!')
    target_bone = pose_bones[0]
    
    # (3) get armature:root
    data = read_data()
    rig = bpy.data.objects[data['armature']]
    
    # (4) make bone
    head_position = tuple(target_bone.head)
    tail_position = (head_position[0], head_position[1], head_position[2]+height)
    layers = [False]*32
    layers[layer]=True
    
    context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    new_name = '%s-%s' % (BONE_PREFIX, name)
    if new_name in rig.data.edit_bones:
        bpy.ops.object.mode_set(mode='POSE')
        return(False, 'This name "%s" is not unique!' % new_name)
    new_bone = rig.data.edit_bones.new(new_name)
    new_bone.head = head_position
    new_bone.tail = tail_position
    new_bone.use_connect = False
    new_bone.parent = rig.data.edit_bones[data['parent_bone']]
    new_bone.use_deform = False
    new_bone.layers = layers
    
    # (5) make R bone
    if name.endswith(from_mirror):
        new_name = '%s-%s' % (BONE_PREFIX, name.replace(from_mirror, to_mirror))
        if new_name in rig.data.edit_bones:
            bpy.ops.object.mode_set(mode='POSE')
            return(False, 'This name "%s" is not unique!' % new_name)
        new_bone = rig.data.edit_bones.new(new_name)
        new_bone.head = (-head_position[0], head_position[1], head_position[2])
        new_bone.tail = (-tail_position[0], tail_position[1], tail_position[2])
        new_bone.use_connect = False
        new_bone.parent = rig.data.edit_bones[data['parent_bone'].replace(from_mirror, to_mirror)]
        new_bone.use_deform = False
        new_bone.layers = layers
        
    bpy.ops.object.mode_set(mode='POSE')
    
    # (6) Clead text
    for key in ['armature', 'parent_bone']:
        del data[key]
    write_data(data, clean=True)
    
    return(True, 'Ok!')

def make_shape_key(context, name, from_mirror='.L', to_mirror='.R'):
    if not name:
        return(False, 'Name not specified!')
        
    new_name = '%s.%s' % (SHAPE_KEY_PREFIX, name)
    data = read_data()
    
    # (1) test mesh
    mesh_name = data.get('mesh')
    if not mesh_name:
        return(False, '"Mesh" not defined')
    if not mesh_name in bpy.data.objects:
        return(False, 'No object with this name("%s") was found!' % mesh_name)
    mesh = bpy.data.objects[mesh_name]
    
    # (2) Basis test
    if not mesh.data.shape_keys:
        mesh.shape_key_add(name='Basis', from_mix=False)
        
    # (3) Shape key
    if new_name in mesh.data.shape_keys.key_blocks:
        return(False, 'Shape Key with the same name("%s") already exists!' % name)
    new_shape_key = mesh.shape_key_add(name=new_name, from_mix=False)
    
    # (4) Drivers
    # (4.1) test Targets
    for key in ['target1', 'target2']:
        target = data.get(key)
        if not target:
            return(False, '%s not defined!' % key)
        if not target[0] in bpy.data.objects:
            return(False, 'Armature with the same name("%s") not found!' % target[0])
        armature = bpy.data.objects[target[0]]
        context.scene.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        if not target[1] in armature.pose.bones:
            return(False, 'Bone with the same name("%s") not found!' % target[1])
    # (4.2) test Distances
    on_distance = data.get('on_distance')
    if on_distance==None:
        return(False, '"Distance to ON" not defined!')
    off_distance = data.get('off_distance')
    if off_distance==None:
        return(False, '"Distance to OFF" not defined!')
    if on_distance == off_distance:
        return(False, '"Distance to ON" and "Distance to OFF" match!')
    
    # (4.3) Driver
    #f_curve = ob.data.shape_keys.key_blocks['jaw_open_C.5'].driver_add('value')
    f_curve = new_shape_key.driver_add('value')
    drv = f_curve.driver
    drv.type = 'SCRIPTED'
    drv.show_debug_info = True
    #
    point = f_curve.keyframe_points.insert(on_distance,1)
    point.interpolation = 'LINEAR'
    point = f_curve.keyframe_points.insert(off_distance,0)
    point.interpolation = 'LINEAR'
    # var
    var = drv.variables.new()
    var.name = 'var'
    var.type = 'LOC_DIFF'
    #
    targ = var.targets[0]
    targ.id = bpy.data.objects[data['target1'][0]]
    targ.bone_target = data['target1'][1]
    targ.transform_space = 'WORLD_SPACE'
    #
    targ = var.targets[1]
    targ.id = bpy.data.objects[data['target2'][0]]
    targ.bone_target = data['target2'][1]
    targ.transform_space = 'WORLD_SPACE'
    #
    # scale
    var = drv.variables.new()
    var.name = 'scale'
    var.type = 'TRANSFORMS'
    #
    targ = var.targets[0]
    targ.id = bpy.data.objects[data['target1'][0]]
    targ.transform_type = 'SCALE_X'
    targ.transform_space = 'WORLD_SPACE'
    #
    drv.expression = 'var/scale'
    #
    fmod = f_curve.modifiers[0]
    f_curve.modifiers.remove(fmod)
    
    # (5) Mirror
    if name.endswith(from_mirror):
        # (5.1) Shape Key
        mirror_name = '%s.%s' % (SHAPE_KEY_PREFIX, name.replace(from_mirror, to_mirror))
        if mirror_name in mesh.data.shape_keys.key_blocks:
            return(False, 'Shape Key with the same name("%s") already exists!' % mirror_name)
        mirror_shape_key = mesh.shape_key_add(name=mirror_name, from_mix=False)
        # (5.2) Drivers
        # (5.2.1) test Targets
        for key in ['target1', 'target2']:
            target = data.get(key)
            armature = bpy.data.objects[target[0]]
            if not target[1].replace(from_mirror, to_mirror) in armature.pose.bones:
                return(False, 'Bone with the same name("%s") not found!' % target[1].replace(from_mirror, to_mirror))
        # (5.3) Driver
        f_curve = mirror_shape_key.driver_add('value')
        drv = f_curve.driver
        drv.type = 'SCRIPTED'
        drv.show_debug_info = True
        #
        point = f_curve.keyframe_points.insert(on_distance,1)
        point.interpolation = 'LINEAR'
        point = f_curve.keyframe_points.insert(off_distance,0)
        point.interpolation = 'LINEAR'
        # var
        var = drv.variables.new()
        var.name = 'var'
        var.type = 'LOC_DIFF'
        #
        targ = var.targets[0]
        targ.id = bpy.data.objects[data['target1'][0]]
        targ.bone_target = data['target1'][1].replace(from_mirror, to_mirror)
        targ.transform_space = 'WORLD_SPACE'
        #
        targ = var.targets[1]
        targ.id = bpy.data.objects[data['target2'][0]]
        targ.bone_target = data['target2'][1].replace(from_mirror, to_mirror)
        targ.transform_space = 'WORLD_SPACE'
        #
        # scale
        var = drv.variables.new()
        var.name = 'scale'
        var.type = 'TRANSFORMS'
        #
        targ = var.targets[0]
        targ.id = bpy.data.objects[data['target1'][0]]
        targ.transform_type = 'SCALE_X'
        targ.transform_space = 'WORLD_SPACE'
        #
        drv.expression = 'var/scale'
        #
        fmod = f_curve.modifiers[0]
        f_curve.modifiers.remove(fmod)
    
    context.scene.objects.active = mesh
    
    # (6) Clead text
    for key in ['target1', 'target2', 'on_distance', 'off_distance']:
        del data[key]
    write_data(data, clean=True)
        
    return(True, 'Shape Key (%s) created' % name)
