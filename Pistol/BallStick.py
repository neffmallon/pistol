#!/usr/bin/env python
"""\
Goal: Create an OpenGL window with two spheres and a trackball
interactor in as simple a way as possible.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys,math

height = 400
width = 400
name = 'BallStick'
beginx = 0
beginy = 0
xcenter = ycenter = zcenter = 0

def init(spheres,cyls):
    glClearColor(0.20,0.25,.20,1.)
    glShadeModel(GL_SMOOTH)
    setup_lights()
    setup_call_list(spheres,cyls)
    setup_callbacks()
    setup_camera()
    return

def setup_lights():
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    return

def setup_call_list(spheres,cyls):
    glNewList(1,GL_COMPILE)
    for (x,y,z,rad,red,green,blue,nslices,nstacks) in spheres:
        addSphere(x,y,z,rad,red,green,blue,nslices,nstacks)
    for (x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue) in cyls:
        addCylinder(x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue)
    glEndList()
    return

def setup_callbacks():
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    return

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    glPushMatrix()
    return

def addSphere(x,y,z,rad,red,green,blue,nslices,nstacks):
    glPushMatrix();
    glTranslatef(x,y,z,)
    color = [red,green,blue,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutSolidSphere(rad,nslices,nstacks)
    glPopMatrix()
    return

def addLine(x1,y1,z1,x2,y2,z2,red,green,blue):
    glDisable(GL_LIGHTING)
    glColor3f(red,green,blue)
    glBegin(GL_LINES)
    glVertex3f(x1,y1,z1)
    glVertex3f(x2,y2,z2)
    glEnd()
    glEnable(GL_LIGHTING)
    return

def addCylinder(x1,y1,z1,x2,y2,z2,rad,nsides,red,green,blue):
    global rotx,roty,rotz
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

def vlength(vect):
    vx,vy,vz = vect
    return math.sqrt(vx*vx+vy*vy+vz*vz)

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(rotx, 1, 0, 0)
    glRotatef(roty, 0, 1, 0)
    glRotatef(rotz, 0, 0, 1)
    glCallList(1)
    glPopMatrix()
    glutSwapBuffers()
    return

def mouse(button,state,x,y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        beginx = x
        beginy = y
    return

def motion(x,y):
    global beginx,beginy,rotx,roty
    print "Motion",x,y,beginx,beginy,rotx,roty
    rotx += 360.0*(y-beginy)/width
    roty += 360.0*(x-beginx)/height
    #rotx = rotx % 360.
    #roty = roty % 360.
    beginx = x
    beginy = y
    glutPostRedisplay()
    return

def keyboard(key,x,y):
    if key == 'x':
        glRotatef(5.,1.,0.,0.)
        glutPostRedisplay()
    elif key == 'y':
        glRotatef(5.,0.,1.,0.)
        glutPostRedisplay()
    elif key == 'i':
        glLoadIdentity()
        gluLookAt(0,0,10,
                  0,0,0,
                  0,1,0)
        glutPostRedisplay()
    elif key == 'q':
        sys.exit()
    return

def main(spheres=[],cyls=[]):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(height,width)
    glutCreateWindow(name)

    init(spheres,cyls)
    
    glutMainLoop()
    return

def test():
    pt1 = (-1.,-1.,0.)
    pt2 = (1.,1.,1.)
    main([(pt1[0],pt1[1],pt1[2],1.,1,0,0,10,10),
          (pt2[0],pt2[1],pt2[2],1.,0,0,1,10,10)],
         [(pt1[0],pt1[1],pt1[2],pt2[0],pt2[1],pt2[2],
           0.2,10,0.5,0.5,0.5)])
    return

if __name__ == '__main__': test()
