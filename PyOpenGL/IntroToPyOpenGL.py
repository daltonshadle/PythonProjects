# ****************************************************** Imports *******************************************************
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL._bytes import as_8_bit
import time

# ***************************************************** Constants ******************************************************
ESCAPE = '\033'
AXIS_LENGTH = 0.2

window = 0

# ***************************************************** Variables ******************************************************
# Rotation Variables
x_pos = 0.0
y_pos = 0.0
z_pos = 0.0

DIRECTION = 1

# ***************************************************** Functions ******************************************************

# GLUT Functions
def InitGL(Width, Height):

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# I/O Functions
def keyPressed(*args):
    if args[0] == ESCAPE:
            sys.exit()


# Drawing Functions
def drawAxes():
    glColor3f(1.0, 1.0, 1.0);
    glRasterPos3f(AXIS_LENGTH, 0, 0);
    glRasterPos3f(0, AXIS_LENGTH, 0);
    glRasterPos3f(0, 0, AXIS_LENGTH);

    glBegin(GL_LINES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(-AXIS_LENGTH, 0.0, 0.0);
    glVertex3f(AXIS_LENGTH, 0.0, 0.0);

    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0.0, -AXIS_LENGTH, 0.0);
    glVertex3f(0.0, AXIS_LENGTH, 0.0);

    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(0.0, 0.0, -AXIS_LENGTH);
    glVertex3f(0.0, 0.0, AXIS_LENGTH);
    glEnd();

def DrawGLScene():
    global x_pos,y_pos,z_pos
    global DIRECTION


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0,0.0,-6.0)
    drawAxes()

    glRotatef(x_pos,1.0,0.0,0.0)
    glRotatef(y_pos,0.0,1.0,0.0)
    glRotatef(z_pos,0.0,0.0,1.0)

    glColor3f(1.0, 1.0, 1.0);
    glutWireCube(1.0);

    #x_pos = x_pos - 0.30
    #z_pos = z_pos - 0.30

    glutSwapBuffers()

    time.sleep(0.03)
    gluLookAt(5, 10, 5, 0, 0, 0, 0, 1.0, 0.0);

# *************************************************** Main Function ****************************************************
def main():

    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(200,200)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

# *************************************************** Calling Main *****************************************************
if __name__ == "__main__":
    main()