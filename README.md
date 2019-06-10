# Shape_keys_to_rig
Addon for Blender 3d 2.79 (alpha)

- Сreating Shape keys with ready-made drivers.
- In-between Shape keys tool.
- Mirror Shape keys.
- Selected vertices to Basis state tool.

## Сreating Shape keys with ready-made drivers:
The Shape key creation panel is in the left side of 3D viewport toolbar ("T" panel).
![image](https://user-images.githubusercontent.com/22092835/58975072-bb7b2a00-87cc-11e9-86eb-336791d23f20.png) <br/>
A Shape key is created with a driver that counts the distance between the heads of two bones. For this it is convenient to create auxiliary bones.
#### Сreating auxiliary bones:
- This purpose is served by two buttons in the section "Make Auxiliary Bones".<br/>
- First you need to determine the parent bone for the future bone.<br/>
- To do this, select the future parental bone and click on the button **"Init Parent Bone"**, bone name is displayed to the right of the button.<br/>
- Next, select the bone position of which we want to track and click on the button **"Make Bone"**, then the dialog will open:<br/>
![image](https://user-images.githubusercontent.com/22092835/58979196-254c0180-87d6-11e9-8011-d1401e199235.png)<br/>
  - In the **Name** field, specify the name of the future bone. At the end of the name you can specify the right or left side.
    - The side designation must match the side designation in the **"Mirror"** field (use "from mirror" side). If you do not specify a side, only one bone will be created, and if you specify, two mirror-symmetric bones will be created.<br/>
  - The **"Height Bone"** field for the height of the bone to be created in units of the scene.<br/>
  - The **"Layer"** field for the bone layer to be created.<br/>
- The head of the newly created auxiliary bone will coincide with the head of the selected bone.
![image](https://user-images.githubusercontent.com/22092835/59151560-ec15ca80-8a3d-11e9-93ac-d527f710272c.png)
#### Сreating Shape Keys:
- Everything you need to create Shape Keys is in the section "Make Shape Keys".
- The very first we define the mesh for which the Shape Key will be created:
  - You need to select the mesh and click on the button **"Init Mesh"**.
- Further it is required to determine the root bone of the character, whose scale will affect the size of the character:
  - You need to select the root bone and click on the button **"Init Root (Bone)"**.
- Then you need to specify two bones, the distance between the heads of which will be taken into account by the driver:
  - select the first bone and click on the button **"Init Target-1 (bone-head)"**.
  - select the second bone and click on the button **"Init Target-2 (bone-head)"**.
  - no matter which bone is first and which is second.
![image](https://user-images.githubusercontent.com/22092835/59177121-bec33c80-8b63-11e9-9804-ed7d0520c7e8.png)
- Then you should determine the distance to enable (ON distance) and disable (OFF distance) the created Shape Key:
  - put the rig in the position at which the Shape Key should be included (it is best if the distance between the bones(Target-1 and Target-2) is as close as possible to zero).
  ![image](https://user-images.githubusercontent.com/22092835/59181156-58441b80-8b6f-11e9-9800-321ffeb1a9ab.png)
  - click on the **"Init distance to ON"**.
  - put the rig in the position where the created Shape Key should be disabled.
  ![image](https://user-images.githubusercontent.com/22092835/59181219-86296000-8b6f-11e9-8d33-444b7753e7dd.png)
  - click on the **"Init distance to OFF"**.
- Clicking the **"Make Shape Key"** button will open a dialog box where you will need to specify the name of the Shape Key to be created. At the end of the name you can specify the right or left side.
  - The side designation must match the side designation in the **"Mirror"** field (use "from mirror" side). If you do not specify a side, only one Shape Key will be created, and if you specify, two mirror-symmetric Shape Keys will be created.
- The created Shape Key will have a driver that will take into account the distance between the bones (Target-1 and Target-2).
  - while reducing the distance (to **"ON distance"**) - Shape Key will be enabled.
  - with increasing distance (to **"OFF distance"**) - Shape Key will be disabled.
