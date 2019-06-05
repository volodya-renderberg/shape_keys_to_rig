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
To do this, select the future parental bone and click on the button **"Init Parent Bone"**, bone name is displayed to the right of the button.<br/>
Next, select the bone position of which we want to track and click on the button **"Make Bone"**, then the dialog will open:<br/>
![image](https://user-images.githubusercontent.com/22092835/58978855-6c85c280-87d5-11e9-9563-8b7a5623fdd0.png)<br/>
In the **Name** field, specify the name of the future bone. At the end of the name you can specify the right or left side. the side designation must match the side designation in the **"Mirror"** field.
