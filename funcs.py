import bpy

import os
import tempfile
import json

DATA_FILE_NAME = '.shape_keys_to_rig_data.json'
BONE_PREFIX = 'AUXBS'

def write_data(data, clean=False):
    path = os.path.join(tempfile.gettempdir(), DATA_FILE_NAME)
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
        
def read_data():
    path = os.path.join(tempfile.gettempdir(), DATA_FILE_NAME)
    if not os.path.exists(path):
        return({})
    with open(path) as json_file:
        data = json.load(json_file)
    return(data)

def init_parent_bone(context):
    armature = context.object
    if armature.type != 'ARMATURE':
        return(False, 'Selected object is not ARMATURE!')
    pose_bones = context.selected_pose_bones
    if not pose_bones:
        return(False, 'Pose bones is not selected!')
    parent_bone = pose_bones[0]
    
    write_data({'armature':armature.name, 'parent_bone': parent_bone.name})
    
    return(True, 'Ok!')

def make_target_bone(context, name, height):
    pose_bones = context.selected_pose_bones
    if not pose_bones:
        return(False, 'Pose bones is not selected!')
    target_bone = pose_bones[0]
    
    # get armature:root
    data = read_data()
    rig = bpy.data.objects[data['armature']]
    
    # make bone
    head_position = tuple(target_bone.head)
    tail_position = (head_position[0], head_position[1], head_position[2]+height)
    
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
    
    if name.endswith('.L'):
        new_name = '%s-%s' % (BONE_PREFIX, name.replace('.L', '.R'))
        if new_name in rig.data.edit_bones:
            bpy.ops.object.mode_set(mode='POSE')
            return(False, 'This name "%s" is not unique!' % new_name)
        new_bone = rig.data.edit_bones.new(new_name)
        new_bone.head = (-head_position[0], head_position[1], head_position[2])
        new_bone.tail = (-tail_position[0], tail_position[1], tail_position[2])
        new_bone.use_connect = False
        new_bone.parent = rig.data.edit_bones[data['parent_bone'].replace('.L', '.R')]
        new_bone.use_deform = False
        
    bpy.ops.object.mode_set(mode='POSE')
    
    return(True, 'Ok!')
