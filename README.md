# Shape_keys_to_rig
Addon for Blender 3d 2.79 (beta)

- Сreating Shape keys with ready-made drivers.
- In-between Shape keys tool.
- Mirror Shape keys.
- Selected vertices to Basis state tool.

## Сreating Shape keys with ready-made drivers:
The Shape key creation panel is in the left side of 3D viewport toolbar ("T" panel).
![image](https://user-images.githubusercontent.com/22092835/58975072-bb7b2a00-87cc-11e9-86eb-336791d23f20.png) <br/>
A Shape key is created with a driver that counts the distance between the heads of two bones. For this it is convenient to create auxiliary bones.
#### Сreating auxiliary bones:
This purpose is served by two buttons in the "Make Auxiliary Bones" section.<br/>
First you need to determine the parent bone for the future bone.<br/>
To do this, select the future parental bone and click on the button **"Init Parent Bone"**.<br/>
Next, select the bone position of which we want to track and click on the button **"Make Bone"**.<br/>
