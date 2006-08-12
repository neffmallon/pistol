#!/usr/bin/env vtkpython
"""
NAME
     VTK.py - Interface to the VTK python libraries

DESCRIPTION

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from vtk import *
from math import sqrt

class Scene:
    def __init__(self):
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.0,1.0,1.0)
        self.window = vtkRenderWindow()
        self.window.AddRenderer(self.renderer)
        self.window.SetSize(500,500)
        self.interactor = vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)
        # I think that these are necessary to keep references
        #  pointing to the objects so they aren't deleted.
        self.items = []
        self.mappers = []
        self.actors = []
        return

    def add_sphere(self,radius,(x,y,z),(r,g,b)):
        sphere = vtkSphereSource()
        self.items.append(sphere)
        sphere.SetRadius(radius)
        sphere.SetThetaResolution(15)
        sphere.SetPhiResolution(15)
        mapper = vtkPolyDataMapper()
        self.mappers.append(mapper)
        mapper.SetInput(sphere.GetOutput())
        actor = vtkActor()
        self.actors.append(actor)
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(r,g,b)
        actor.SetPosition(x,y,z)
        self.renderer.AddActor(actor)
        return

    def add_cylinder(self,(x1,y1,z1),(x2,y2,z2),(r,g,b),radius=0.08):
        l,ux,uy,uz = unit_vector((x1,y1,z1),(x2,y2,z2))
        cx,cy,cz = midpoint((x1,y1,z1),(x2,y2,z2))
        theta,rx,ry,rz = rotation_angle(ux,uy,uz)
        cyl = vtkCylinderSource()
        self.items.append(cyl)
        cyl.SetRadius(radius)
        cyl.SetHeight(l)
        mapper = vtkPolyDataMapper()
        self.mappers.append(mapper)
        mapper.SetInput(cyl.GetOutput())
        actor = vtkActor()
        self.actors.append(actor)
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(r,g,b)
        actor.RotateWXYZ(theta,rx,ry,rz)
        actor.SetPosition(cx,cy,cz)
        self.renderer.AddActor(actor)
        return

    def add_grid_data(self,(ox,oy,oz),(nx,ny,nz),(dx,dy,dz),array):
        self.grid = vtkStructuredPoints()
        self.grid.SetDimensions(nx,ny,nz)
        self.grid.SetOrigin(ox,oy,oz)
        self.grid.SetSpacing(dx,dy,dz)
        self.grid.GetPointData().SetScalars(array)
        return

    def add_contour(self,value,(r,g,b),opacity):
        if not self.grid: raise "Need grid to add contour"
        contour = vtkContourFilter()
        self.items.append(contour)
        contour.SetInput(self.grid)
        contour.SetValue(0,value)
        normals = vtkPolyDataNormals() #add normals for smoothing
        self.items.append(normals)
        normals.SetInput(contour.GetOutput())
        mapper = vtkPolyDataMapper()
        self.mappers.append(mapper)
        mapper.SetInput(normals.GetOutput())
        mapper.ScalarVisibilityOff()
        actor = vtkActor()
        self.actors.append(actor)
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(r,g,b)
        actor.GetProperty().SetOpacity(opacity)
        self.renderer.AddActor(actor)
        return

    def display(self):
        self.interactor.Initialize()
        self.interactor.Start()
        return

# Utility functions, which should be in something like TupleMath
def midpoint((xi,yi,zi),(xj,yj,zj)):
    cx = 0.5*(xi+xj)
    cy = 0.5*(yi+yj)
    cz = 0.5*(zi+zj)
    return (cx,cy,cz)

def unit_vector((xi,yi,zi),(xj,yj,zj)):
    ax = xj-xi       #bond axis
    ay = yj-yi
    az = zj-zi
    al = sqrt(ax*ax + ay*ay + az*az)
    ax = ax/al
    ay = ay/al
    az = az/al
    return (al,ax,ay,az)    

def rotation_angle(ax,ay,az):
    from math import acos,pi
    rad2deg = 180./pi
    # Compute the rotational axis (y cross a)
    rx = az
    ry = 0
    rz = -ax
    # Compute the rotational angle (y dot a)
    theta = rad2deg*acos(ay)
    return (theta,rx,ry,rz)

def vtk_grid_data3((nx,ny,nz),data):
    "Make a vtk grid object from a 3d array"
    vtkdata = vtkFloatArray()
    for i in range(nx):
        for j in range(ny):
            joffset = j*nx
            for k in range(nz):
                koffset = k*nx*ny
                offset = i+joffset+koffset
                vtkdata.InsertValue(offset,data[i,j,k])
    return vtkdata

    
if __name__ == '__main__':
    scene = Scene()
    scene.add_sphere(0.2,(0,0,0),(1.,0,0))
    scene.add_sphere(0.15,(1,0,0),(0.9,0.9,0.9))
    scene.add_sphere(0.15,(0,1,0),(0.9,0.9,0.9))
    scene.add_cylinder((0,0,0),(1,0,0),(0.25,0.25,0.25))
    scene.add_cylinder((0,0,0),(0,1,0),(0.25,0.25,0.25))

    # make a fake mesh:
    nx=ny=nz=10
    data = vtkFloatArray()
    for i in range(nx):
        x = (i-4.5)
        for j in range(ny):
            y = j-4.5
            joffset = j*nx
            for k in range(nz):
                koffset = k*nx*ny
                z = k-4.5
                offset = i+joffset+koffset
                val = sqrt(x*x+y*y+z*z)
                data.InsertValue(offset,val)
    scene.add_grid_data((-4.5,-4.5,-4.5),(nx,ny,nz),(1,1,1),data)
    scene.add_contour(1.5,(0,0,1),0.5)
    scene.display()

