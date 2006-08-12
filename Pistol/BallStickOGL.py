#!/usr/bin/env python
"""\
 BallStickOGL.py - Simple Ball and Stick renderer.
 A very simple OpenGL/Tk renderer for spheres and cylinders. Some
 parts of this code were taken from dek's pyopengl demos.

 This requires Togl

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
#from OpenGL.Tk import *

class Scene:
    def __init__(self,spheres,cyls):
        self.SetupWindow()
        self.make_display_list(spheres,cyls)
        self.ogl.mainloop()
        return

    def make_display_list(self,spheres,cyls):
        self.dlist = glGenLists(1)
        glNewList(self.dlist,GL_COMPILE)
        for (x,y,z,rad,red,green,blue,nslices,nstacks) in spheres:
            self.addSphere(x,y,z,rad,red,green,blue,nslices,nstacks)
        for (x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue) in cyls:
            self.addCylinder(x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue)
        glEndList()
        return

    def SetupWindow(self):
        self.OglFrame = Frame()
        self.OglFrame.pack(side = TOP)
        self.QuitButton = Button(self.OglFrame, text='Quit',command=sys.exit)
        self.QuitButton.pack(side=TOP)
        self.ogl = Opengl(master=self.OglFrame, width = 500,
                          height = 500, double = 1)
        self.ogl.pack(side = TOP, expand = 1, fill = 'both')
        self.ogl.redraw = self.display
        return

    def display(self, event=None):
        glClearColor(0.0, 0.0, 0.0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glCallList(self.dlist)
        glFlush()
        return

    def addSphere(self,x,y,z,rad,red,green,blue,nslices,nstacks):
        glPushMatrix();
        glTranslatef(x,y,z)
        color = [red,green,blue,1.]
        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
        glutSolidSphere(rad,nslices,nstacks)
        glPopMatrix()
        return

    def addLine(self,x1,y1,z1,x2,y2,z2,red,green,blue):
        glDisable(GL_LIGHTING)
        glColor3f(red,green,blue)
        glBegin(GL_LINES)
        glVertex3f(x1,y1,z1)
        glVertex3f(x2,y2,z2)
        glEnd()
        glEnable(GL_LIGHTING)
        return

    def addCylinder(self,x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue):
        l = vlength((x1-x2,y1-y2,z1-z2))
        xd,yd,zd = ((x2-x1)/l,(y2-y1)/l,(z2-z1)/l) #difference vector
        rad2deg = 180./math.pi
        # assume pointing in z and calculate rotation angle and axis
        rotx,roty,rotz = (-yd,xd,0)
        theta = math.acos(zd)*rad2deg

        glPushMatrix()
        glTranslatef(x1,y1,z1)
        glRotatef(theta,rotx,roty,rotz)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (red,green,blue,1))

        obj = gluNewQuadric()
        gluCylinder(obj,rad,rad,l,nsides,nsides)
        glPopMatrix()

        return

# utilities and demos

def vlength(vect):
    vx,vy,vz = vect
    return math.sqrt(vx*vx+vy*vy+vz*vz)

def simple_test():
    pt1 = (-1,-1,0)
    pt2 = (1,1,1)
    Scene([(pt1[0],pt1[1],pt1[2],1.,1,0,0,10,10),
           (pt2[0],pt2[1],pt2[2],1.,0,0,1,10,10)],
          [(pt1[0],pt1[1],pt1[2],pt2[0],pt2[1],pt2[2],
            0.2,10,0.5,0.5,0.5)])
    
if __name__ == '__main__': simple_test()
