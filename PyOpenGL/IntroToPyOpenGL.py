# ****************************************************** Imports ******************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy



# ***************************************************** Constants ******************************************************

# Crystals
SC = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
]

BCC = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
    [0.5, 0.5, 0.5]
]

FCC = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
    [0.5, 0.5, 1],
    [0.5, 0.5, 0],
    [0.5, 1, 0.5],
    [0.5, 0, 0.5],
    [1, 0.5, 0.5],
    [0, 0.5, 0.5]
]

SC_TYPE = 0
BCC_TYPE = 1
FCC_TYPE = 2
CRYSTAL_ARRAY = [SC, BCC, FCC]

# Window Const
WIN_HEIGHT = 480
WIN_WIDTH = 640
WIN_X_POS = 200
WIN_Y_POS = 200

# Axis Const
AXIS_LENGTH = 0.2

# Camera Increment Const
THETA_ANGLE_INCREMENT = 0.05
PHI_ANGLE_INCREMENT = 0.05
RHO_INCREMENT = 0.1
NEAR_INCREMENT = 0.1

# Initialization Const
THETA_ANGLE_INITIAL = 0.0
PHI_ANGLE_INITIAL = 0.0
RHO_INITIAL = 10.0
CAM_X_INITIAL = 2.0
CAM_Y_INITIAL = 2.0
CAM_Z_INITIAL = 2.0

# Perspective Const
NEAR_INITIAL = 1.0
FAR_INITIAL = 20.0
FOV_INITIAL = 45.0
ASPECT_INITIAL = float(WIN_WIDTH)/float(WIN_HEIGHT)



# ***************************************************** Variables ******************************************************

# GLUT Variables
window = 0

# Object Position Variables
obj_x_pos = 0.0
obj_y_pos = 0.0
obj_z_pos = 0.0

# Camera Position Variables
theta = THETA_ANGLE_INITIAL
phi = PHI_ANGLE_INITIAL
rho = RHO_INITIAL
cam_x_pos = CAM_X_INITIAL
cam_y_pos = CAM_X_INITIAL
cam_z_pos = CAM_X_INITIAL
cam_x_lookat = 0
cam_y_lookat = 0
cam_z_lookat = 0

# Perspective Variables
perspect_near = NEAR_INITIAL
perspect_far = FAR_INITIAL
perspect_fov = FOV_INITIAL
perspect_aspect = ASPECT_INITIAL



# ***************************************************** Functions ******************************************************

# GLUT Functions
def InitGL(Width, Height):
    # Input: int Width, int Height
    # Output: void, initializes canvas variables

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(perspect_fov, float(Width)/float(Height), perspect_near, perspect_far)
    glMatrixMode(GL_MODELVIEW)
    updateCameraSperhical()

# I/O Functions
def keyPressFunc(key, x, y):
    # Input: arg pointer, key press
    # Output: void, maps key press to functionality
    global rho

    ch = key.decode("utf-8")

    if (ch == chr(43)): # 43 is the char code for "+" and zooms in
        rho -= RHO_INCREMENT
    elif (ch == chr(45)): # 43 is the char code for "-" and zooms out
        rho += RHO_INCREMENT

    updateCameraSperhical()

    glutPostRedisplay();

def specialInputFunc(key, x, y):
    # Input: int keypress, int x, int y
    # Output: void, maps special input key press to functionality
    global phi, theta

    if (key == GLUT_KEY_UP):
        phi += PHI_ANGLE_INCREMENT
    elif (key == GLUT_KEY_DOWN):
        phi -= PHI_ANGLE_INCREMENT
    elif (key == GLUT_KEY_RIGHT):
        theta += THETA_ANGLE_INCREMENT
    elif (key == GLUT_KEY_LEFT):
        theta -= THETA_ANGLE_INCREMENT

    updateCameraSperhical()

    glutPostRedisplay();

# Drawing Functions
def drawGLScene():
    # Input: none
    # Output: void, draws the scene defined by the functions listed in this

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(cam_x_pos, cam_y_pos, cam_z_pos, cam_x_lookat, cam_y_lookat, cam_z_lookat, 0, 1.0, 0.0);
    glTranslatef(0,0,0)

    # Call drawing functions
    drawAxes()
    drawUnitCell(3.0, 3.0, 3.0, 90.0, 90.0, 90.0, FCC_TYPE)

    glutSwapBuffers()

def drawAxes():
    # Input: none
    # Output: void, draws the positive x,y,z axis

    glColor3f(1.0, 1.0, 1.0);
    glRasterPos3f(AXIS_LENGTH, 0, 0);
    glRasterPos3f(0, AXIS_LENGTH, 0);
    glRasterPos3f(0, 0, AXIS_LENGTH);

    glBegin(GL_LINES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(AXIS_LENGTH, 0.0, 0.0);

    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(0.0, AXIS_LENGTH, 0.0);

    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(0.0, 0.0, AXIS_LENGTH);
    glEnd();

def drawCuboid(a, b, c):
    # Input: float a, b, c; where a is x, b is y, c is z
    # Output: void, draws a cuboid given those dimensions

    glPushMatrix()
    glTranslate(-a/2, -b/2, -c/2)
    glBegin(GL_LINE_LOOP)
    glVertex3f(a, b, c)
    glVertex3f(0, b, c)
    glVertex3f(0, 0, c)
    glVertex3f(a, 0, c)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(a, b, 0)
    glVertex3f(0, b, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(a, 0, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(a, b, c)
    glVertex3f(a, b, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0, b, c)
    glVertex3f(0, b, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0, 0, c)
    glVertex3f(0, 0, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(a, 0, c)
    glVertex3f(a, 0, 0)
    glEnd()

    glPopMatrix()

def drawUnitCell(a, b, c, alpha, beta, gamma, type):
    # Input: float a, b, c, alpha, beta, gamma; int type
    # Output: void, draws the unit cell of a crystal

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    drawCuboid(a, b, c)
    glPopMatrix()

    for i in range (0, len(CRYSTAL_ARRAY[type])):
        glPushMatrix()
        glTranslate((a*CRYSTAL_ARRAY[type][i][0] - a/2),
                    (b*CRYSTAL_ARRAY[type][i][1] - b/2),
                    (c*CRYSTAL_ARRAY[type][i][2] - c/2))
        glutWireSphere(0.2, 10, 10)
        glPopMatrix()


def updateCameraSperhical():
    # Input: none
    # Output: void, updates the camera's x,y,z coordinates based on spherical
    global cam_x_pos, cam_y_pos, cam_z_pos, rho, phi, theta

    cam_x_pos = rho * numpy.cos(theta) * numpy.cos(phi)
    cam_y_pos = rho * numpy.sin(phi)
    cam_z_pos = rho * numpy.sin(theta) * numpy.cos(phi)



# *************************************************** Main Function ****************************************************
def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIN_WIDTH, WIN_HEIGHT)
    glutInitWindowPosition(WIN_X_POS, WIN_Y_POS)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(drawGLScene)
    glutIdleFunc(drawGLScene)
    glutKeyboardFunc(keyPressFunc)
    glutSpecialFunc(specialInputFunc);
    InitGL(WIN_WIDTH, WIN_HEIGHT)
    glutMainLoop()



# *************************************************** Calling Main *****************************************************
if __name__ == "__main__":
    main()