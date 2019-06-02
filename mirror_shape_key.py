#!BPY
"""
Name: 'MakeMirrorShape'
Blender: 249.2
Group: 'Object'
Tooltip: 'This script mirrors (about x=0) a mesh with shape keys.
	For shape keys with name endings like "_R", ".Left" etc.,
	corresponding mirrored assymetric shape keys will be added.
	For other shape keys, mirror symmetric shape keys will be formed.
	Note that this script is not intended for a full mesh -
	it is supposed to be applied to one half of a mesh.
"""

import math
from math import *
import bpy
from bpy import *
from bpy.Mathutils import *

object=bpy.context.object
shapeIndex=object.active_shape_key_index
me=object.data

#####################################################################################
# Defining a function to right-left flip name string endings

def flipName(inString):
	
	ns=len(inString)
	endingsL=['L','l','Left','left']
	endingsR=['R','r','Right','right']
	indexlist=[1,0];
	endings=[endingsL,endingsR]
	preendings=['.','_','-']
	
	hitIndex=[]
	for i in range(0,2):
		for j in range(len(endings[i])):
			e=endings[i][j]
			if len(e)&lt;=(ns-1):
				if e==inString[ns-len(e):ns]:
					for pe in preendings:
						if inString[ns-len(e)-1]==pe:
							firstPart=inString[0:ns-len(e)-1]
							outString=firstPart+pe+endings[indexlist[i]][j]
							return outString
								
	return inString

######################################################################################
# Defining a function to check if a string is in a list 

def inList(string,stringlist):
	for lstring in stringlist:
		if string==lstring:
			return True
	return False

######################################################################################
# Adds mirrored vertices. Coordinates may be adjusted later

print 'Adding vertices'

epsilon=0.0001 	#The tolerance for considering an index to be at x=0
n=len(me.verts)
mirrorIndexList=[] 
j=n-1	 

basisverts=me.key.blocks[0].getData()[:]
bverts=[]
for i in range(len(basisverts)):
	bverts.append(basisverts[i]*1)	#Really important to multiply by 1, otherwise bverts just links to the key data
						#and these links get broken, giving seemingly random results, as one adds vertices. 

vertseq=[]

for i in range(n):	

	ivert=bverts[i]
	xvec=ivert.x
	yvec=ivert.y
	zvec=ivert.z	

	if -epsilon&lt;xvec&lt;epsilon:
		mirrorIndexList.append(i)  #Makes the original index point to itself
	else:
		j=j+1
		mirrorIndexList.append(j)
		vertseq.append((-xvec,yvec,zvec))

me.verts.extend(vertseq)

######################################################################################
# Create symmetric and asymmetric shape keys

print 'Setting up the shape keys'

km=len(me.key.blocks)

# Making a list of key shape names - to avoid adding shapes with existing names

nameList=[]
for block in me.key.blocks[1:km]:
	nameList.append(block.name)
	
# Here is the main loop
	
for block in me.key.blocks[1:km]:
	
	keyverts=block.getData()
	name=block.name
	newname=flipName(name)
	
	if newname!=name and inList(newname,nameList):
		bpy.Draw.PupMenu("Note:Mirror named shape key already exists - not creating new shape key")
	else:			
		if newname==name:
			#For a symmetric key
			mirrkeyverts=keyverts
		else:
			#For an asymmetric key
			object.insertShapeKey()
			newblock=me.key.blocks[-1]
			newblock.name=newname
			mirrkeyverts=newblock.getData()
			for j in range(n):
				#Comment: If the added ShapeKey was based on 'Basis' - this little loop could be omitted
				mirrkeyverts[j].x=bverts[j].x 
				mirrkeyverts[j].y=bverts[j].y
				mirrkeyverts[j].z=bverts[j].z
		
		for j in range(n):
			mj=mirrorIndexList[j]
			mirrkeyverts[mj].x=-keyverts[j].x 
			mirrkeyverts[mj].y=keyverts[j].y
			mirrkeyverts[mj].z=keyverts[j].z


######################################################################################	
# Create mirrored vertexgroups and vertex weights 

print 'Mirroring vertex groups and vertex weights'

GroupList=me.getVertGroupNames()

for name in GroupList:
	list=me.getVertsFromGroup(name,1)	#The argument 1 is a flag to get weight values as well
	newname=flipName(name)
	
	if inList(newname,GroupList) and newname!=name:
		print 'Mirror named group already exists - not creating new group'
	else:
		if newname!=name:
			me.addVertGroup(newname)
		for vtuplet in list:
			index=vtuplet[0]
			if not (newname==name and mirrorIndexList[index]==index):
				me.assignVertsToGroup(newname,[mirrorIndexList[index]],vtuplet[1],1) 

######################################################################################
# Create mirror edges and crease values

print 'Mirroring edges'

m=len(me.edges)
edgeseq=[]		
mirrEdgeList=[]

for k in range(m):
	iedge=me.edges[k]
	edge=[iedge.v1.index,iedge.v2.index]
	mirredge=[mirrorIndexList[edge[0]], mirrorIndexList[edge[1]]]
	
	if not (mirredge[0]==edge[0] and mirredge[1]==edge[1]):
		mirrEdgeList.append(j)
		edgeseq.append(mirredge)
	else:
		mirrEdgeList.append(k)

me.edges.extend(edgeseq)

for k in range(m):
	if mirrEdgeList[k]!=k:
		me.edges[mirrEdgeList[k]].crease=me.edges[k].crease

######################################################################################a
# Create mirrored faces, material indices, smoothness and normals

print 'Mirroring faces'

m=len(me.faces)
faceseq=[]
faceIndexList=[]	#A pointer list. Position i in the list will contain the index of the face that face number i is mirrored to.

for k in range(m):
	iface=me.faces[k]
	vertlist=iface.verts	
	
	#Setting up a list of the indices for the mirrored face
	mirrorFaceIndexList=[]		#List of lists with indices for the added faces
	centercount=0
	for vert in vertlist:
		vi=vert.index
		mi=mirrorIndexList[vi]
		if mi==vi:
			centercount+=1
		
		mirrorFaceIndexList.append(mi)
	
	if centercount==len(mirrorFaceIndexList):
		faceIndexList.append(k)
	else:
		faceseq.append(mirrorFaceIndexList)
		faceIndexList.append(m+len(faceseq)-1)
		
me.faces.extend(faceseq)

for k in range(m):
	
	ki=faceIndexList[k]
	if not ki==k:
		#Mirroring the material index
		me.faces[ki].mat=me.faces[k].mat
		
		#Mirroring smoothness
		me.faces[ki].smooth=me.faces[k].smooth
		
		#Making a selection for subsequently flipping the normals
		me.faces[k].sel=0
		me.faces[ki].sel=1

me.flipNormals() #Flips normals of selected faces

######################################################################################

object.activeShape=shapeIndex
bpy.Redraw()
print 'Done'
bpy.Draw.PupMenu("Mirrored Shape Keys")

