from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys,math

name = 'ball_glut'

def vlength(vect):
    vx,vy,vz = vect
    return math.sqrt(vx*vx+vy*vy+vz*vz)

def addSphere(x,y,z,rad,red,green,blue,nslices,nstacks):
    glPushMatrix();
    glTranslatef(x,y,z)
    color = [red,green,blue,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glMaterialfv(GL_FRONT, GL_SHININESS, [25.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0,1.0,1.0,1.0])
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
    l = vlength((x1-x2,y1-y2,z1-z2))
    xd,yd,zd = ((x2-x1)/l,(y2-y1)/l,(z2-z1)/l) #difference vector
    rad2deg = 180./math.pi
    # assume pointing in z and calculate rotation angle and axis
    rotx,roty,rotz = (-yd,xd,0)
    theta = math.acos(zd)*rad2deg
    
    glPushMatrix()
    glTranslatef(x1,y1,z1)
    glRotatef(theta,rotx,roty,rotz)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (red,green,blue,1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, [25.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0,1.0,1.0,1.0])
    obj = gluNewQuadric()
    gluCylinder(obj,rad,rad,l,nsides,nsides)
    glPopMatrix()
    
    return

    return

def main(r,g,b):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400,400)
    glutCreateWindow(name)

    glClearColor(r,g,b,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glDepthFunc(GL_LEQUAL)
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_ALPHA_TEST)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT,GL_DONT_CARE)
    glHint(GL_POLYGON_SMOOTH_HINT,GL_DONT_CARE)

    glutDisplayFunc(display)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,100.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,5,
              0,0,0,
              0,1,0)
    glPushMatrix()
    setup_calllist()
    glutMainLoop()
    return

def setup_calllist():
    dlist = glGenLists(1)
    glNewList(dlist,GL_COMPILE)
    cyl_rad = 0.1
    ax,ay,az = -1.0,-1.0,0.0
    bx,by,bz = 1.0,1.0,1.0
    addSphere(ax,ay,az,  0.3,  1.0,0.0,1.0,  50,50)
    addSphere(bx,by,bz,    0.3,  1.0,0.0,1.0,  50,50)
    addCylinder(-1,-1,0,  1,1,1, cyl_rad,  10, 0.5,0.5,0.5)
    glEndList()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glCallList(1)
    glPopMatrix()
    glutSwapBuffers()
    return

if __name__ == '__main__':
    main(1.,1.,1.) # white
    #main(0.,0.,0.) # black
