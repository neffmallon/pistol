#!/usr/bin/env python

import math
import wx,wx.glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ID_ABOUT=101
ID_EXIT=102

class BSCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent, spheres=[], cyls=[], lines=[]):
        wx.glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_LEFT_DOWN(self, self.OnMouseDown)  # needs fixing...
        wx.EVT_LEFT_UP(self, self.OnMouseUp)
        wx.EVT_MOTION(self, self.OnMouseMotion)

        self.transx = 0
        self.transy = 0
        self.depth = 0
        self.rotx = 20.
        self.roty = 30.
        self.rotz = 0.

        self.spheres = spheres
        self.cyls = cyls
        self.lines = lines

    def OnSize(self, event):
        size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnEraseBackground(self, event): pass #avoid flashing on MSW.

    def OnMouseDown(self, evt):
        self.beginx,self.beginy = evt.GetPosition()
        self.CaptureMouse()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        x,y = evt.GetPosition()
        width,height = self.GetSize()
        if evt.Dragging() and evt.LeftIsDown():
            self.rotx += ((y-self.beginy)/width)*360.0
            self.roty += ((x-self.beginx)/height)*360.0
        self.Refresh(True)

        self.rotx = self.rotx % 360.
        self.roty = self.roty % 360.
        
        self.beginx,self.beginy = x,y
        return

    def InitGL(self):
        # set viewing projection
        self.setup_calllist()
        self.setup_lights()
        self.setup_camera()
        return

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glTranslatef(self.transx,self.transy,self.depth)
        glRotatef(self.rotx, 1, 0, 0)
        glRotatef(self.roty, 0, 1, 0)
        glRotatef(self.rotz, 0, 0, 1)
    
        glCallList(1)
        glPopMatrix()
        self.SwapBuffers()
        return

    def setup_calllist(self):
        glNewList(1, GL_COMPILE)
        for xyz,rad,rgb,nslices,nstacks in self.spheres:
            addSphere(xyz,rad,rgb,nslices,nstacks)
        for xyz1,xyz2,rad,nsides,rgb in self.cyls:
            addCylinder(xyz1,xyz2,rad,nsides,rgb)
        for xyz1,xyz2,rgb in self.lines:
            addLine(xyz1,xyz2,rgb)
        glEndList()
        return

    def setup_lights(self):
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        return

    def setup_camera(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 10.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
        return

class BSFrame(wx.Frame):
    def __init__(self,parent,ID,title,spheres,cyls,lines):
        wx.Frame.__init__(self,parent,ID,title,
                         wx.DefaultPosition, wx.Size(400,400))

        self.CreateStatusBar()

        self.menuBar = wx.MenuBar()
        self.SetMenuBar(self.menuBar)

        self.filemenu = wx.Menu()
        self.menuBar.Append(self.filemenu,'&File')
        self.filemenu.Append(ID_EXIT, 'E&xit','Terminate the program')
        wx.EVT_MENU(self, ID_EXIT, self.TimeToQuit)

        self.helpmenu = wx.Menu()
        self.menuBar.Append(self.helpmenu,'&Help')
        self.helpmenu.Append(ID_ABOUT, '&About',"More info about this program")
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)

        self.glcanvas = BSCanvas(self,spheres,cyls,lines)
        return

    def OnAbout(self,event):
        dlg = wx.MessageDialog(self,
                               "Draw balls and sticks using OpenGL",
                               "About BallStickWX",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    def TimeToQuit(self,event):
        self.Close(true)
        return

class BSApp(wx.App):
    def __init__(self,id,spheres=[],cyls=[],lines=[]):
        self.spheres = spheres
        self.cyls = cyls
        self.lines = lines
        wx.App.__init__(self,id)
        
    def OnInit(self):
        frame = BSFrame(None,-1,'BallStickWX',
                        self.spheres,self.cyls,self.lines)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

def addSphere((x,y,z),rad,(red,green,blue),nslices,nstacks):
    glPushMatrix();
    glTranslatef(x,y,z,)
    color = [red,green,blue,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutSolidSphere(rad,nslices,nstacks)
    glPopMatrix()
    return

def addLine((x1,y1,z1),(x2,y2,z2),(red,green,blue)):
    glDisable(GL_LIGHTING)
    glColor3f(red,green,blue)
    glBegin(GL_LINES)
    glVertex3f(x1,y1,z1)
    glVertex3f(x2,y2,z2)
    glEnd()
    glEnable(GL_LIGHTING)
    return

def addCylinder((x1,y1,z1),(x2,y2,z2),rad,nsides,(red,green,blue)):
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

def vdot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def vlength(v): return math.sqrt(vdot(v,v))


if __name__ == '__main__':
    pt1 = (-1.,-1.,0.)
    pt2 = (1.,1.,1.)

    x1,y1,z1 = pt1
    x2,y2,z2 = pt2

    red = (1,0,0)
    blue = (0,0,1)
    gray = (0.9,0.9,0.9)
    black = (0,0,0)

    spheres = [(pt1,0.3,red,20,20),(pt2,0.3,blue,20,20)]
    cyls = [(pt1,pt2,0.1,20,gray)]
    lines = [
        ((x1,y1,z1),(x1,y1,z2),black),
        ((x1,y1,z2),(x1,y2,z2),black),
        ((x1,y2,z2),(x1,y2,z1),black),
        ((x1,y2,z1),(x1,y1,z1),black),
        ((x2,y1,z1),(x2,y1,z2),black),
        ((x2,y1,z2),(x2,y2,z2),black),
        ((x2,y2,z2),(x2,y2,z1),black),
        ((x2,y2,z1),(x2,y1,z1),black),
        ((x1,y1,z1),(x2,y1,z1),black),
        ((x1,y1,z2),(x2,y1,z2),black),
        ((x1,y2,z2),(x2,y2,z2),black),
        ((x1,y2,z1),(x2,y2,z1),black)]

    app = BSApp(0,spheres,cyls,lines)
    app.MainLoop()
