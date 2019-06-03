import bpy

import os
import tempfile
import json
import sys

ARMATURE_DATA_FILE_NAME = '.shape_keys_to_rig_armature_data.json' # keys: armature, parent_bone, mesh
MESH_DATA_FILE_NAME = '.shape_keys_to_rig_mesh_data.json' # keys: mesh,
TO_STEP_DATA_FILE_NAME = '.shape_keys_to_to_step_data' # для пошагового миррора.
BONE_PREFIX = 'AUXBS'
SHAPE_KEY_PREFIX = 'aux'

def set_float(self, value):
    self["zero"] = value

# data_type (str) - in 'Armature', 'Mesh', 'Steps'
def write_data(data, data_type='Armature', clean=False):
    if data_type=='Armature':
        path = os.path.join(tempfile.gettempdir(), ARMATURE_DATA_FILE_NAME)
    elif data_type=='Mesh':
        path = os.path.join(tempfile.gettempdir(), MESH_DATA_FILE_NAME)
    elif data_type=='Steps':
        path = os.path.join(tempfile.gettempdir(), TO_STEP_DATA_FILE_NAME)
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
    elif data_type=='Steps':
        path = os.path.join(tempfile.gettempdir(), TO_STEP_DATA_FILE_NAME)
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
    targ.id = bpy.data.objects[data['root_bone'][0]]
    targ.bone_target = data['root_bone'][1]
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
        targ.id = bpy.data.objects[data['root_bone'][0]]
        targ.bone_target = data['root_bone'][1]
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

def mirror_shape_key(context, name, topology, from_mirror='.L', to_mirror='.R', active=False):
    pass
    # (1) name
    if name.endswith(to_mirror):
        return(False, 'Сan not be mirrored ("%s" to "%s")' % (to_mirror, to_mirror))
    if not from_mirror:
        return(False, 'Сan not be mirrored!' )
    #
    if not active:
        data = read_data()
        # (2)
        mesh_name = data.get('mesh')
        if not mesh_name:
            return(False, '"Mesh" not defined')
        if not mesh_name in bpy.data.objects:
            return(False, 'No object with this name("%s") was found!' % mesh_name)
        ob = bpy.data.objects[mesh_name]
    else:
        ob = context.object
    
    # mirror_name
    mirror_name = name.replace(from_mirror, to_mirror)
    if not mirror_name in ob.data.shape_keys.key_blocks:
        return(False, 'Shape Key named %s not found!' % mirror_name)
    for i,key in enumerate(ob.data.shape_keys.key_blocks.keys()):
        if key == mirror_name:
            ob.active_shape_key_index = i
            break
    
    # mirror
    new_ob = ob.copy()
    new_ob.data = ob.data.copy()
    new_ob.data.animation_data_clear()

    bpy.context.scene.objects.link(new_ob)

    new_ob.parent = None

    for mod in new_ob.modifiers:
        new_ob.modifiers.remove(mod)
        
    for grp in new_ob.vertex_groups:
        new_ob.vertex_groups.remove(grp)
    
    # remove осталных shape key
    for shkey in new_ob.data.shape_keys.key_blocks:
        if shkey.name in ['Basis', name]:
            continue
        new_ob.shape_key_remove(shkey)
    
    ob.select=False
    context.scene.objects.active = None
    context.scene.objects.active = new_ob
    #bpy.ops.object.mode_set(mode = 'EDIT')
    #bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # выставление в 1
    for i,key in enumerate(new_ob.data.shape_keys.key_blocks.keys()):
        if key == name:
            new_ob.active_shape_key_index = i
            new_ob.active_shape_key.value = 1
            break
    # to steps
    wr_data = {
    'new_ob_name':new_ob.name,
    'ob_name': ob.name,
    'name': name,
    'mirror_name': mirror_name,
    'from_mirror': from_mirror,
    'to_mirror': to_mirror,
    'topology': topology,
    }
    write_data(wr_data, data_type='Steps', clean=True)
    return(True, 'Step1 fin, mirror "Shape key" and click "Step2"')

    #new_ob.active_shape_key_index = i
    #context.scene.update()
    #bpy.ops.object.paths_update()
    bpy.ops.object.shape_key_mirror(use_topology=topology)
    
    source_shkey = new_ob.data.shape_keys.key_blocks[name]
    target_shkey = ob.data.shape_keys.key_blocks[mirror_name]
    
    # relative key
    rel_name = source_shkey.relative_key.name
    mirror_rel_name = rel_name.replace(from_mirror, to_mirror)
    if mirror_rel_name in ob.data.shape_keys.key_blocks:
        target_shkey.relative_key = ob.data.shape_keys.key_blocks[mirror_rel_name]
    
    # vertices
    for vtx in new_ob.data.vertices:
        target_shkey.data[vtx.index].co = source_shkey.data[vtx.index].co[:]
    
    # remove new ob
    #bpy.data.objects.remove(new_ob, do_unlink=True)
    
    return(True, 'Mirrored from "%s" to "%s"' % (source_shkey.name, target_shkey.name))

def mirror_step_2(context):
    pass
    data = read_data(data_type='Steps')
    print(data)
    
    #
    new_ob = bpy.data.objects[data['new_ob_name']]
    ob = bpy.data.objects[data['ob_name']]
    name = data['name']
    mirror_name = data['mirror_name']
    from_mirror = data['from_mirror']
    to_mirror = data['to_mirror']
    topology = data['topology']
    

    source_shkey = new_ob.data.shape_keys.key_blocks[name]
    target_shkey = ob.data.shape_keys.key_blocks[mirror_name]
    
    # relative key
    rel_name = source_shkey.relative_key.name
    mirror_rel_name = rel_name.replace(from_mirror, to_mirror)
    if mirror_rel_name in ob.data.shape_keys.key_blocks:
        target_shkey.relative_key = ob.data.shape_keys.key_blocks[mirror_rel_name]
    
    # vertices
    for vtx in new_ob.data.vertices:
        target_shkey.data[vtx.index].co = source_shkey.data[vtx.index].co[:]
    
    # remove new ob
    bpy.data.objects.remove(new_ob, do_unlink=True)
    
    return(True, 'Mirrored from "%s" to "%s"' % (source_shkey.name, target_shkey.name))

def in_between(context, from_mirror='.L', to_mirror='.R'):
    pass
    # 1 - получение сетки - возможно нужно просто context.object
    # 2 - получение чистого имени бленда (base_name). имя состоит из 4 частей префикс.имя.вес-инбитвина.сторона - сторна может отсутствовать.
    # 3 - миррорить или нет / base_shape_key_name
    # 4 - определение текущего веса.
    # 5 - запись значения для нуля базового бленда - до создания первого инбитвина.
    # 6 - создание shape_key метод 1 (между нулём и блендом).
    # 7 - создание shape_key метод 2 (между двумя блендами).
    
    # (1)
    ob = bpy.context.object
    #
    shape_key = ob.active_shape_key
    if shape_key.name.endswith(to_mirror):
        return(False, 'Сan not be mirrored ("%s" to "%s")' % (to_mirror, to_mirror))
    
    # (2) name
    separate_name = shape_key.name.split('.')
    if len(separate_name) < 2:
        return(False, 'Shape Key name is wrong! Must be: prefix.name.weight.side ("weight" and "side" not required)')
    base_name = '%s.%s' % (separate_name[0], separate_name[1])
    
    # (3)
    if shape_key.name.endswith(from_mirror):
        mirror = True
    else:
        mirror = False
    
    # -- (3.1) base shape key name
    if mirror:
        base_shape_key_name = '%s%s' % (base_name, from_mirror)
    else:
        base_shape_key_name = base_name
    
    # (4) value
    weights = {}
    num_shape_keys = 0
    for sh_key in ob.data.shape_keys.key_blocks:
        if sh_key.name.startswith(base_name):
            if sh_key.name.endswith(to_mirror):
                continue
            elif sh_key.name.endswith(from_mirror) and not shape_key.name.endswith(from_mirror):
                continue
            elif shape_key.name.endswith(from_mirror) and not sh_key.name.endswith(from_mirror):
                continue
            #
            num_shape_keys+=1
            #
            c_value = round(sh_key.value, 3)
            if c_value==0 or c_value==1:
                continue
            #
            if len(sh_key.name.split('.')) > 2:
                try:
                    weight = int(sh_key.name.split('.')[2]) # int - чтобы проверить число это или нет
                except:
                    weight = 1000
            
            weights[str(weight)] = c_value
    
    print(weights)
    
    if not weights:
        return(False, 'Сannot be created in this position!')
    
    # (5) add FloatProperty for zero value
    if num_shape_keys==1:
        attr_name = base_shape_key_name.replace('.', '_')
        exec('bpy.types.Mesh.%s =  bpy.props.FloatProperty(name = \"%s\", default=0.0)' % (attr_name, attr_name))
        base_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % base_shape_key_name)
        for point in base_fc.keyframe_points:
            if point.co[1]==0:
                setattr(ob.data, attr_name, point.co[0])
        if base_shape_key_name.endswith(from_mirror):
            mr_attr_name = base_shape_key_name.replace(from_mirror, to_mirror).replace('.', '_')
            exec('bpy.types.Mesh.%s =  bpy.props.FloatProperty(name = \"%s\", default=0.0)' % (mr_attr_name, mr_attr_name))
            setattr(ob.data, mr_attr_name, point.co[0])

    # (6) method 1 (между нулём и блендом)
    if len(weights)==1:
        pass
        # 6.1 - get shape_key_name/weight/value
        # 6.2 - new_name
        # 6.3 - create shape_key
    
        # (6.1)
        # -- get after_shape_key name
        key = list(weights.keys())[0]
        weight = weights[list(weights.keys())[0]]
        
        # -- get abs weight
        if key=='1000': 
            abs_weight = weight
        else:
            abs_weight = weight*(int(key)/1000)
        
        #
        if mirror:
            if key=='1000':
                after_shape_key_name = '%s%s' % (base_name, from_mirror)
            else:
                after_shape_key_name = '%s.%s%s' % (base_name, int(key), from_mirror)
        else:
            if key=='1000':
                after_shape_key_name = base_name
            else:
                after_shape_key_name = '%s.%s' % (base_name, int(key))
        
        after_shape_key = ob.data.shape_keys.key_blocks.get(after_shape_key_name)
        if not after_shape_key:
            return(False, 'Shape Key "%s" not found' % after_shape_key_name)
        
        #
        value = get_value(ob, after_shape_key_name, base_shape_key_name, weight)
        
        print('method 1, value: %s' % str(value))
        
        # (6.2)
        # -- new name
        if mirror:
            new_name = '%s.%s%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1], from_mirror)
        else:
            new_name = '%s.%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1])
        
        # (6.3)
        # -- test exists shape key
        if new_name in ob.data.shape_keys.key_blocks:
            return(False, 'Key with that name "%s" already exists' % new_name)
        
        # create shape key
        new_shape_key = ob.shape_key_add(name=new_name, from_mix=True)
        # vertex position
        before, after = 0, int(key)/1000
        __make_in_between(ob, new_shape_key, after_shape_key, after, before, value, abs_weight, base_shape_key_name)
        #
        
        #
        if mirror:
            if key=='1000':
                mirror_after_name = '%s%s' % (base_name, to_mirror)
            else:
                mirror_after_name = '%s.%s%s' % (base_name, int(key), to_mirror)
            #
            mirror_new_name = '%s.%s%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1], to_mirror)
            # get mirror shape key
            if mirror_after_name in ob.data.shape_keys.key_blocks:
                mirror_after_shkey = ob.data.shape_keys.key_blocks[mirror_after_name]
            else:
                return(False, '#9 Shape Key not found by "%s" name' % mirror_after_name)
            
            # new shape key
            # -- test exists shape key
            if mirror_new_name in ob.data.shape_keys.key_blocks:
                return(False, 'Shape Key with that name "%s" already exists' % mirror_new_name)
            # -- create shape key
            new_shape_key = ob.shape_key_add(name=mirror_new_name, from_mix=True)
            #
            
            # -- -- vertex position
            __make_in_between(ob, new_shape_key, mirror_after_shkey, after, before, value, abs_weight, base_shape_key_name)
    # (7) (между двумя блендами)
    elif len(weights)==2:
        pass
        # 7.1 - get before_shape_key / after_shape_key
        # 7.2 - get value/weight
        # 7.3 - create new_shape_key
        
        # (7.1)
        weights_keys = sorted([int(item) for item in weights.keys()])
        if mirror:
            before_shape_key_name = '%s.%s%s' % (base_name, weights_keys[0], from_mirror)
            if weights_keys[1]==1000:
                after_shape_key_name = '%s%s' % (base_name, from_mirror)
            else:
                after_shape_key_name = '%s.%s%s' % (base_name, weights_keys[1], from_mirror)
        else:
            before_shape_key_name = '%s.%s' % (base_name, weights_keys[0])
            if weights_keys[1]==1000:
                after_shape_key_name = '%s' % (base_name)
            else:
                after_shape_key_name = '%s.%s' % (base_name, weights_keys[1])
        #
        
        #
        if before_shape_key_name in ob.data.shape_keys.key_blocks:
            before_shape_key = ob.data.shape_keys.key_blocks[before_shape_key_name]
        else:
            return(False, '#8 Shape Key not found by "%s" name' % before_shape_key_name)
        #
        if after_shape_key_name in ob.data.shape_keys.key_blocks:
            after_shape_key = ob.data.shape_keys.key_blocks[after_shape_key_name]
        else:
            return(False, '#7 Shape Key not found by "%s" name' % after_shape_key_name)
        
        # (7.2)
        key0 = list(weights.keys())[0]
        key1 = list(weights.keys())[1]
        y = weights[key1]
        before = x1 = int(key0)/1000
        after = x2 = int(key1)/1000
        
        # -- get abs weight
        abs_weight = (y-1)*(x2-x1)+x2
        
        # get value
        value = get_value(ob, after_shape_key_name, base_shape_key_name, y)
        
        # -- new name
        if mirror:
            new_name = '%s.%s%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1], from_mirror)
        else:
            new_name = '%s.%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1])
        #
        print('after_name: %s\nbefor_name: %s\nabs_weight: %s\nvalue: %s\nnew_name: %s' % (after_shape_key_name, before_shape_key_name, abs_weight, value, new_name))
        # make shape_key
        if not new_name in ob.data.shape_keys.key_blocks:
            new_shape_key = ob.shape_key_add(name=new_name, from_mix=True)
        else:
            return(False, 'Shape Key with that name "%s" already exists' % new_name)
        
        # make in_between
        __make_in_between(ob, new_shape_key, after_shape_key, after, before, value, abs_weight, base_shape_key_name, before_shape_key=before_shape_key)
        
        #
        if mirror:
            mirror_new_name = '%s.%s%s' % (base_name, str(format(round(abs_weight,3), '.3f')).split('.')[1], to_mirror)
            mirror_before_name = '%s.%s%s' % (base_name, weights_keys[0], to_mirror)
            if weights_keys[1]==1000:
                mirror_after_name = '%s%s' % (base_name, to_mirror)
            else:
                mirror_after_name = '%s.%s%s' % (base_name, weights_keys[1], to_mirror)
                
            # get mirror shape keys
            # -- after
            if mirror_after_name in ob.data.shape_keys.key_blocks:
                mirror_after_shkey = ob.data.shape_keys.key_blocks[mirror_after_name]
            else:
                return(False, '#4 Shape Key not found by "%s" name' % mirror_after_name)
            # -- before
            if mirror_before_name in ob.data.shape_keys.key_blocks:
                mirror_before_shkey = ob.data.shape_keys.key_blocks[mirror_before_name]
            else:
                return(False, '#5 Shape Key not found by "%s" name' % mirror_before_name)
                
            # new shape key
            # -- test exists shape key
            if mirror_new_name in ob.data.shape_keys.key_blocks:
                return(False, 'Shape Key with that name "%s" already exists' % mirror_new_name)
            # -- create shape key
            mirror_new_shkey = ob.shape_key_add(name=mirror_new_name, from_mix=True)
            
            # make in_between
            __make_in_between(ob, mirror_new_shkey, mirror_after_shkey, after, before, value, abs_weight, base_shape_key_name, before_shape_key=mirror_before_shkey)

    return(True, 'Ok!')

def remove_in_between(context, from_mirror, to_mirror):
    pass
    # 1 - парсинг имени, если это не инбитвин то отказ.
    # 2 - поиск after и before.
    # 3 - перезапись поинтов.
    # 4 - удаление.

    ob = context.object
    shape_key = ob.active_shape_key
    
    # (1)
    # -- parsing of name
    separate_name = shape_key.name.split('.')
    if len(separate_name) < 2:
        return(False, 'Shape Key name is wrong! Must be: prefix.name.weight.side ("weight" and "side" not required)')
    base_name = '%s.%s' % (separate_name[0], separate_name[1])
    
    # -- get mirror
    fr_mr = from_mirror
    to_mr = to_mirror
    if shape_key.name.endswith(from_mirror):
        mirror = True
    elif shape_key.name.endswith(to_mirror):
        mirror = True
        fr_mr = to_mirror
        to_mr = from_mirror
    else:
        mirror = False
    
    # -- get base shape key
    if mirror:
        base_shape_key = ob.data.shape_keys.key_blocks['%s%s' % (base_name, fr_mr)]
    else:
        base_shape_key = ob.data.shape_keys.key_blocks[base_name]
        
    #  --
    if mirror and shape_key.name == base_shape_key.name:
        return(False, 'base Shape_key cannot be removed!')
    
    # (2)
    try:
        num = int(shape_key.name.split('.')[2])
    except Exception as e:
        print(e)
        return(False, 'wrong number "%s"!' % shape_key.name.split('.')[2])
    #
    before_num = 0
    after_num = 1000
    before_shape_key = None
    after_shape_key = base_shape_key
    #
    for sh_key in ob.data.shape_keys.key_blocks:
        pass
        name = sh_key.name
        if mirror and name.endswith(to_mr):
            continue
        elif not mirror and (name.endswith(to_mr) or name.endswith(fr_mr)):
            continue
        try:
            c_num = int(name.split('.')[2]) # сразу исключаем базовый шейп, так как after_num уже = 1000
            if c_num == num:
                continue
        except:
            continue
        
        if before_num < c_num < num:
            before_num = c_num
            before_shape_key = sh_key
        elif num < c_num < after_num:
            after_num = c_num
            after_shape_key = sh_key
    
    # (3)
    af_p0, af_p1, zero = get_two_points(ob, after_shape_key.name, base_shape_key.name)
    if before_shape_key:
        bf_p0, bf_p1, zero = get_two_points(ob, before_shape_key.name, base_shape_key.name, more=True)
        after_new_point = (tuple(bf_p1.co)[0], 0)
        before_new_point = (tuple(af_p1.co)[0], 0)
    else:
        after_new_point = (zero, 0)
    # -- after
    after_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % after_shape_key.name)
    after_fc.keyframe_points.remove(af_p0)
    after_fc.keyframe_points.insert(after_new_point[0], after_new_point[1])
    # -- before
    if before_shape_key:
        before_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % before_shape_key.name)
        before_fc.keyframe_points.remove(bf_p0)
        before_fc.keyframe_points.insert(before_new_point[0], before_new_point[1])
        
    # -- remove
    fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % shape_key.name)
    #ob.data.animation_data.action.fcurves.remove(fc)
    bpy.ops.object.shape_key_remove(all=False)
    
    if mirror:
        pass
        #
        name = shape_key.name.replace(fr_mr, to_mr)
        if name in ob.data.shape_keys.key_blocks:
            shape_key = ob.data.shape_keys.key_blocks[name]
        else:
            return(False, '#6 Shape Key not found by "%s" name' % name)
        #
        base_name = base_shape_key.name.replace(fr_mr, to_mr)
        if base_name in ob.data.shape_keys.key_blocks:
            base_shape_key = ob.data.shape_keys.key_blocks[base_name]
        else:
            return(False, '#3 Shape Key not found by "%s" name' % base_name)
        #
        if before_shape_key:
            before_name = before_shape_key.name.replace(fr_mr, to_mr)
            if before_name in ob.data.shape_keys.key_blocks:
                before_shape_key = ob.data.shape_keys.key_blocks[before_name]
            else:
                return(False, '#2 Shape Key not found by "%s" name' % before_name)
        #
        after_name = after_shape_key.name.replace(fr_mr, to_mr)
        if after_name in ob.data.shape_keys.key_blocks:
            after_shape_key = ob.data.shape_keys.key_blocks[after_name]
        else:
            return(False, '#1 Shape Key not found by "%s" name' % after_name)
        #
        # (3 mirror)
        af_p0, af_p1, zero = get_two_points(ob, after_shape_key.name, base_shape_key.name)
        if before_shape_key:
            bf_p0, bf_p1, zero = get_two_points(ob, before_shape_key.name, base_shape_key.name, more=True)
            after_new_point = (tuple(bf_p1.co)[0], 0)
            before_new_point = (tuple(af_p1.co)[0], 0)
        else:
            after_new_point = (zero, 0)
        # -- after
        after_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % after_shape_key.name)
        after_fc.keyframe_points.remove(af_p0)
        after_fc.keyframe_points.insert(after_new_point[0], after_new_point[1])
        # -- before
        if before_shape_key:
            before_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % before_shape_key.name)
            before_fc.keyframe_points.remove(bf_p0)
            before_fc.keyframe_points.insert(before_new_point[0], before_new_point[1])
            
        # -- remove
        for i,key in enumerate(ob.data.shape_keys.key_blocks.keys()):
            if key == name:
                ob.active_shape_key_index = i
                break
        fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % shape_key.name)
        #ob.data.animation_data.action.fcurves.remove(fc)
        bpy.ops.object.shape_key_remove(all=False)
    
    return(True, 'Remove: %s' % shape_key.name)

def selected_vertices_to_basis_shape_key(context):
    pass
    
    ob = context.object
    shape_key = ob.active_shape_key
    base_shape_key = shape_key.relative_key
    
    if not shape_key or not base_shape_key:
        return(False, 'Not found Shape_key or Basis Shape key!')

    print('Basis name: "%s"' % base_shape_key.name)

    bpy.ops.object.mode_set(mode='OBJECT')


    for v in ob.data.vertices:
        if v.select:
            p = base_shape_key.data[v.index].co[:]
            print(p)
            shape_key.data[v.index].co[0] = p[0]
            shape_key.data[v.index].co[1] = p[1]
            shape_key.data[v.index].co[2] = p[2]
            
    bpy.ops.object.mode_set(mode='EDIT')
    
    return(True, '"Vertices to Basis" is done!')

# ========================== Utilits ==============================

def copy_target(src, tgt):
    tgt.data_path = src.data_path
    tgt.id = src.id
    tgt.bone_target = src.bone_target
    tgt.transform_space = src.transform_space
    tgt.transform_type = src.transform_type
    
def copy_variable(src, tgt):
    v2 = tgt.variables.new()
    v2.type = src.type
    v2.name = src.name
    for i, target in enumerate(v2.targets):
        try:
            copy_target(src.targets[i], v2.targets[i])
        except:
            print("dang, %s %s"%(src.targets[0].id, sys.exc_info()[0]) )

# src - f-curve
# tgt - shape_key
def copy_driver(src, tgt, mirror=False):
    d2 = tgt.driver_add('value')

    d2.driver.expression = src.driver.expression
    for v1 in src.driver.variables:
        copy_variable(v1, d2.driver)

def __make_in_between(ob, new_shape_key, after_shape_key, after, before, value, weight, base_shape_key_name, before_shape_key=False):
    after_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % after_shape_key.name)
    if before_shape_key:
        before_fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % before_shape_key.name)
        
    #
    print('__make_in_between', after, before, weight)
    # vertex position
    for v in ob.data.vertices:
        if before_shape_key:
            before_v = before_shape_key.data[v.index].co[:]
        else:
            before_v = after_shape_key.relative_key.data[v.index].co[:]
        after_v = after_shape_key.data[v.index].co[:]
        #
        new_shape_key.data[v.index].co[0] = before_v[0] + (after_v[0] - before_v[0])*((weight - before)/(after - before))
        new_shape_key.data[v.index].co[1] = before_v[1] + (after_v[1] - before_v[1])*((weight - before)/(after - before))
        new_shape_key.data[v.index].co[2] = before_v[2] + (after_v[2] - before_v[2])*((weight - before)/(after - before))
    
    # copy driver.variables
    copy_driver(after_fc, new_shape_key)
    
    # after
    # -- get points
    zero_point, p1, z = get_two_points(ob, after_shape_key.name, base_shape_key_name)
    after_value=tuple(p1.co[:])[0]
    # -- edit points
    after_zero_value = tuple(zero_point.co[:])[0]
    after_fc.keyframe_points.remove(zero_point)
    #
    for p in after_fc.keyframe_points:
        p.co[0] = p.co[0]*1000
    #
    after_fc.keyframe_points.insert(value*1000, 0)
    #
    for p in after_fc.keyframe_points:
        p.co[0] = p.co[0]/1000
    #
    
    # -- before
    if before_shape_key:
        zero_point, bf_p1, z = get_two_points(ob, before_shape_key.name, base_shape_key_name, more=True)
        befo_point = tuple(bf_p1.co[:])
        #print('&'*3, tuple(zero_point.co), befo_point)
        before_fc.keyframe_points.remove(zero_point)
        #
        for p in before_fc.keyframe_points:
            p.co[0] = p.co[0]*1000
        #
        before_fc.keyframe_points.insert(value*1000, 0)
        #
        for p in before_fc.keyframe_points:
            p.co[0] = p.co[0]/1000
        #
        
    # -- new
    new_f_curve = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % new_shape_key.name)
    #
    if before_shape_key:
        points = [(befo_point[0], 0), (value, 1), (after_value,0)]
        print('points with before:', points)
    else:
        points = [(z , 0), (value, 1), (after_value,0)]
        print('points*:', points)
    for p in points:
        point = new_f_curve.keyframe_points.insert(p[0]*1000, p[1])
        point.interpolation = 'LINEAR'
    for p in new_f_curve.keyframe_points:
        p.co[0] = p.co[0]/1000
    # -- remove modifier
    fmod = new_f_curve.modifiers[0]
    new_f_curve.modifiers.remove(fmod)
    
def get_value(ob, after_shape_key_name, base_shape_key_name, weight):
    p1, p2, z = get_two_points(ob, after_shape_key_name, base_shape_key_name)
    #
    value=(weight - p2.co[1])*((p2.co[0] - p1.co[0])/(p2.co[1] - p1.co[1])) + p2.co[0]
    return(value)

def get_two_points(ob, shape_key_name, base_shape_key_name, more=False):
    fc = ob.data.animation_data.drivers.find('shape_keys.key_blocks["%s"].value' % shape_key_name)
    # get zero
    attr_name = base_shape_key_name.replace('.', '_')
    if not attr_name in dir(ob.data):
        exec('bpy.types.Mesh.%s =  bpy.props.FloatProperty(name = \"%s\", default=0.0)' % (attr_name, attr_name))
    zero = getattr(ob.data, attr_name)
    print('zero: %s' % str(zero))
    # get points
    p1, p2 = None, None
    for point in fc.keyframe_points:
        if point.co[1]==1:
            p2=point
        elif point.co[1]==0:
            if p1 is None:
                p1=point
            else:
                if more:
                    if abs(point.co[0] - zero) > abs(p1.co[0] - zero):
                        p1=point
                else:
                    if abs(point.co[0] - zero) < abs(p1.co[0] - zero):
                        p1=point
                    
    return(p1, p2, zero)
