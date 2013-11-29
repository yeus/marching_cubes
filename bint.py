#blender interface for marching cube algorithm

import mathutils
import bpy
vec=mathutils.Vector

import marchingcube_np

def genobject(objname,verts=[],faces=[],edges=[]):
    me = bpy.data.meshes.new(objname)  # create a new mesh
    me.from_pydata(verts,edges,faces)
    me.update()      # update the mesh with the new data
    ob = bpy.data.objects.new(objname,me) # create a new object
    ob.data = me          # link the mesh data to the object
    scene = bpy.context.scene           # get the current scene
    scene.objects.link(ob)                      # link the object into the scene
    return ob

def creategeometry(verts):
    faces=[]
    faceoffset=0
    for ver in verts:
        if len(ver)==4: 
            faces.append((faceoffset+0,faceoffset+1,faceoffset+2,faceoffset+3))
            faceoffset+=4
        elif len(ver)==3:
            faces.append((faceoffset+0,faceoffset+1,faceoffset+2)) 
            faceoffset+=3
    return list(chain.from_iterable(verts)),faces

def genobjandremovedoubles(verts,name="test"):
    verts,faces=creategeometry(verts)
    obj=genobject(name,verts,faces)
    selectobj(obj)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.1)#TODO: threshold distance in relation to gridsize
    bpy.ops.object.editmode_toggle()
    return obj

def selectobj(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select=True
    bpy.context.scene.objects.active=obj
