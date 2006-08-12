#!/usr/bin/env python
"""\
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
""" 

import sys,math

import pygtk
pygtk.require('2.0')

from gtk.gtkgl.apputils import *

from OpenGL.GLUT import glutSolidSphere

DEBUG = False

class BSArea(GLScene, GLSceneButton, GLSceneButtonMotion):
    """OpenGL drawing area for simple demo."""

    def __init__(self, spheres=[],cyls=[],lines=[]):
        GLScene.__init__(self,
                         gtk.gdkgl.MODE_RGB   |
                         gtk.gdkgl.MODE_DEPTH |
                         gtk.gdkgl.MODE_DOUBLE)

        self.spheres = spheres
        self.cyls = cyls
        self.lines = lines
        self.rotx=20.0
        self.roty=30.0
        self.rotz=0.0
        self.trans_scale = 10
        self.transx = 0.
        self.transy = 0.
        self.depth_scale = 15
        self.depth = 0.

    def init(self, *args):
        self.setup_calllist()
        self.setup_lights()
        self.setup_camera()
        return

    def display(self, *args):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glTranslatef(self.transx,self.transy,self.depth)
        #glMultMatrixf(flatten(self.tb.matrix))
        glRotatef(self.rotx, 1, 0, 0)
        glRotatef(self.roty, 0, 1, 0)
        glRotatef(self.rotz, 0, 0, 1)
    
        glCallList(1)
        glPopMatrix()
        return

    def reshape(self, width, height): glViewport(0, 0, width, height)
    
    def button_press(self, width, height, event):
        if DEBUG: print "Button press"
        self.beginx = event.x
        self.beginy = event.y
    
    def button_release(self, width, height, event):
        if DEBUG: print "Button release"
        pass
    
    def button_motion(self, width, height, event):
        if event.state == gtk.gdk.BUTTON1_MASK:
            self.tb.update(self.beginx,self.beginy,event.x,event.y,
                           width,height)
            self.rotx += ((event.y-self.beginy)/width)*360.0
            self.roty += ((event.x-self.beginx)/height)*360.0
        elif event.state == gtk.gdk.BUTTON2_MASK:
            self.transx += self.trans_scale*(event.x - self.beginx)/width
            self.transy -= self.trans_scale*(event.y - self.beginy)/height
        elif event.state == gtk.gdk.BUTTON3_MASK:
            self.depth += self.depth_scale*(event.y - self.beginy)/height

        self.rotx = self.rotx % 360.
        self.roty = self.roty % 360.
        
        self.beginx = event.x
        self.beginy = event.y
        
        self.queue_draw()
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

    def dump(self,width,height,fname='bs.png'):
        import Image
        pstring = glReadPixels(0,0,width,height,GL_RGBA,GL_UNSIGNED_BYTE)
        snapshot = Image.fromstring("RGBA",(width,height),pstring
                                    ).transpose(Image.FLIP_TOP_BOTTOM)
        snapshot.save(fname)
        return


class BSWindow(gtk.Window):
    """Simple demo application."""

    def __init__(self,spheres=[],cyls=[],lines=[]):
        gtk.Window.__init__(self)

        self.width = 300
        self.height = 300

        self.set_title('Ball and Stick')
        self.set_reallocate_redraws(gtk.TRUE)
        self.connect('delete_event', self.quit)

        # VBox to hold everything.
        vbox = gtk.VBox()
        self.add(vbox)

        # BSArea
        self.bsarea = BSArea(spheres,cyls,lines)
        self.glarea = GLArea(self.bsarea)
        self.glarea.set_size_request(300,300)
        vbox.pack_start(self.glarea)

        # Screen shot button
        ssbutton = gtk.Button('Screen Shot')
        ssbutton.connect('clicked',self.dump)
        vbox.pack_start(ssbutton, expand=gtk.FALSE)

        # A quit button.
        button = gtk.Button('Quit')
        button.connect('clicked', self.quit)
        vbox.pack_start(button, expand=gtk.FALSE)
        return

    def run(self):
        self.show_all()
        gtk.main()

    def dump(self, *args): self.bsarea.dump(self.width,self.height)
    def quit(self, *args): gtk.mainquit()



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
def qnorm(q): return q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3]

def flatten(mat):
    "Flatten a 2d matrix"
    flmat = []
    for vec in mat:
        for vi in vec: flmat.append(vi)
    return flmat

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
    bs = BSWindow(spheres,cyls,lines)
    bs.run()

