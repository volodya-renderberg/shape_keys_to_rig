# Shape_keys_to_rig
Addon for Blender 3d v2.79 (betta)

- [Install](#install)
- [Сreating Shape keys with ready-made drivers](#сreating-shape-keys-with-ready-made-drivers).
- [In-between Shape keys tool](#in-between-shape-keys-tool).
- [Selected vertices to Basis state tool](#selected-vertices-to-basis-state-tool).
- [Copy Shape Key Data](#copy-shape-key-data).
- [Mirror Shape keys](#mirror-shape-keys).
- [Import/Export Shape Keys](#importexport-shape-keys).
- [Troubleshooting](#troubleshooting).

## Install

#### way 1

Place addon folder in blender addons directory.

#### way 2
Running the following commands in a linux terminal:
```
cd ~/.config/blender/2.79/scripts/addons
git clone https://github.com/volodya-renderberg/shape_keys_to_rig.git
```
and to update the addon to the latest version execute these commands:
```
cd ~/.config/blender/2.79/scripts/addons/shape_keys_to_rig
git fetch
git pull
```

## Сreating Shape keys with ready-made drivers.

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
![image](https://user-images.githubusercontent.com/22092835/59181543-444ce980-8b70-11e9-8368-131c3f8f9e72.png)
  - The side designation must match the side designation in the **"Mirror"** field (use "from mirror" side). If you do not specify a side, only one Shape Key will be created, and if you specify, two mirror-symmetric Shape Keys will be created.
- The created Shape Key will have a driver that will take into account the distance between the bones (Target-1 and Target-2).
  - while reducing the distance (to **"ON distance"**) - Shape Key will be enabled.
  - with increasing distance (to **"OFF distance"**) - Shape Key will be disabled.

## In-between Shape keys tool.

One Shape Key may not be enough.<br/>
One Shape Key may be well suited for the final form, but poorly suited for intermediate positions.

To solve this problem, as well as for other cases when it is necessary to create non-linear deformations (e.g. sliding), in-between forms are used.

The panel for this purpose is located in the **Property editor**.

#### Creating an in-between Shape key:

- To create an in-between Shape Key, you need to set the rig to the position for which the in-between form is required.
  - In our example, we will be bend about 90 degrees in the elbow.

- Then it is necessary to select the Shape key for which the in-between form is created.
  - **It matters** the Shape Key for which side to choose, **left** or **right**.
  - The designation of the side must match the designation of the side in the field **"Mirror"** and you must choose the side _"from mirror"_.
  - Only in this case in-between Shape keys will be created for both the right and left sides.

- Then click on the button **"ADD In-between for active"**.
![image](https://user-images.githubusercontent.com/22092835/61184496-153a0400-a657-11e9-8fa1-4a0c10fc650b.png)

#### Overview of the created in-between Shape key:

- This creation method is suitable for any Shape Keys that is controlled by the **driver** and **the key frame points**.
- The name of the created Shape Keys differs from the base name by adding a number, which is the relative distance between **ON** and **OFF** distances.
- A new Shape Key will be created from the current state of the Shape Keys.
- The created Shape Keys has the same driver, but receives new key frame points, with a value of **1** at the point of the corresponding relative position when creating this Shape Keys, and with values of **0** - at the points corresponding to the values equal to **1** of the nearest Shape Keyss (see picture).
![image](https://user-images.githubusercontent.com/22092835/61184617-8d54f980-a658-11e9-99b2-65cc94d4642b.png)
- the number of in-between Shape Keys can be any.
![image](https://user-images.githubusercontent.com/22092835/61184750-01dc6800-a65a-11e9-8c2e-40c49364ba62.png)

#### in-between Shape keys removal:

- Select the Shape Key to be deleted and click on the **REMOVE in-between** button.
  - The choice of the side does not matter, both will be deleted.
  - Key frame points of the remaining Shape Kes will be recalculated for adequate work.
  > In version 2.79, the animation curves themselves are not deleted, they are underlined in red and must be removed manually. In version 2.8, there is no such problem anymore.
  ![image](https://user-images.githubusercontent.com/22092835/61184796-65ff2c00-a65a-11e9-8b99-de716eb788b3.png)
  
## Selected vertices to Basis state tool.

Often it is required to return a part of the vertices of the active Shape Key to its original state.
- To do this, in the editing mode, select the desired vertices and click on the button - **Vertices to Basis**.
![image](https://user-images.githubusercontent.com/22092835/61184817-99da5180-a65a-11e9-9d76-cf75d4ee037f.png)
- The selected vertices will return to their original state.
  
## Copy Shape Key Data.

Sometimes you want to copy a form from one Shape Key to another.
For this:
- Select the Shape Key to be copied and click on the **Init Source** button, the name of this shape key will be displayed next to the button.
![image](https://user-images.githubusercontent.com/22092835/61184847-e6be2800-a65a-11e9-966d-dbe9960808df.png)
- Select the Shape Key into which we copy and click on the **Copy to active** button.
![image](https://user-images.githubusercontent.com/22092835/61184860-081f1400-a65b-11e9-84f1-8fa0a6cccd8a.png)
- this shape key will be fully consistent with the source.

## Mirror Shape keys.

> In connection with some unresolved problems, it takes two steps.
- Select the Shape Key that must be mirrored.
  - side must match **from mirror**.
- Click on the **Mirror active/Step 1** button.
![image](https://user-images.githubusercontent.com/22092835/61184876-2e44b400-a65b-11e9-92bd-1397c0eaf31d.png)
- auxiliary geometry will be created, with the only Shape Key that will be active without performing extra actions - perform **Mirror Shape Key** or **Mirror Shape Key (Topology)**.
![image](https://user-images.githubusercontent.com/22092835/61184912-8f6c8780-a65b-11e9-8946-4bd7b1ae6eb3.png)
- Click on **Step 2**.
![image](https://user-images.githubusercontent.com/22092835/61184919-a7dca200-a65b-11e9-9af9-e575ec94d5db.png)

## Import/Export Shape Keys.

> Export / Import procedures transfer information through an external text file. Therefore, Import and Export can be done between different scenes of the Blender. In case of use [Lineyka](https://github.com/volodya-renderberg/lineyka) - text file storage location is linked to an asset.
- Export import all forms:
 ![image](https://user-images.githubusercontent.com/22092835/61184987-541e8880-a65c-11e9-936b-6b86ef9a9458.png)
 - The **Export All Shape Keys** button will save all Shape Keys of the active object to a text file.
 - The **Import All Shape Keys** button will load those Shape Keys that will be present in the active object.
- Export import of one form:
 ![image](https://user-images.githubusercontent.com/22092835/61184976-40732200-a65c-11e9-8ad1-1267279212da.png)
 - The **Export active Shape Key** button will save only the active Shape Key to a text file.
 - The **Import active Shape Key** button will load the Shape Key into the active one if the Shape Key with the same name was previously written to the file.
 
## Troubleshooting.
- creation of auxiliary bones.
  -
- the creation of in-between Shape Keys.
  - 
