import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import noise
from OpenGL.GLU import gluPerspective, gluLookAt

# Initialize pygame
pygame.init()

# Window settings
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST)

# Camera setup
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Voxel Grid Settings
GRID_SIZE = 20
VOXEL_SIZE = 0.5
water_level = -2
time_step = 0.0

# Boat Position
boat_x, boat_y = GRID_SIZE // 2, GRID_SIZE // 2

def draw_voxel(x, y, z, color):
    """ Draws a single cube voxel at (x, y, z) """
    glColor3fv(color)
    glBegin(GL_QUADS)

    # Front
    glVertex3f(x, y, z)
    glVertex3f(x + VOXEL_SIZE, y, z)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z)
    glVertex3f(x, y + VOXEL_SIZE, z)

    # Back
    glVertex3f(x, y, z + VOXEL_SIZE)
    glVertex3f(x + VOXEL_SIZE, y, z + VOXEL_SIZE)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z + VOXEL_SIZE)
    glVertex3f(x, y + VOXEL_SIZE, z + VOXEL_SIZE)

    # Left
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + VOXEL_SIZE)
    glVertex3f(x, y + VOXEL_SIZE, z + VOXEL_SIZE)
    glVertex3f(x, y + VOXEL_SIZE, z)

    # Right
    glVertex3f(x + VOXEL_SIZE, y, z)
    glVertex3f(x + VOXEL_SIZE, y, z + VOXEL_SIZE)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z + VOXEL_SIZE)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z)

    # Top
    glVertex3f(x, y + VOXEL_SIZE, z)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z)
    glVertex3f(x + VOXEL_SIZE, y + VOXEL_SIZE, z + VOXEL_SIZE)
    glVertex3f(x, y + VOXEL_SIZE, z + VOXEL_SIZE)

    # Bottom
    glVertex3f(x, y, z)
    glVertex3f(x + VOXEL_SIZE, y, z)
    glVertex3f(x + VOXEL_SIZE, y, z + VOXEL_SIZE)
    glVertex3f(x, y, z + VOXEL_SIZE)

    glEnd()

def generate_water(time_step):
    """ Generates a wavy voxelized water surface using Perlin noise """
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            wave_height = noise.pnoise2(x * 0.2, y * 0.2, octaves=4, repeatx=100, repeaty=100) * 0.5
            draw_voxel(x * VOXEL_SIZE, y * VOXEL_SIZE, water_level + wave_height, (0, 0, 1))  # Blue water

def draw_boat():
    """ Draws a simple boat voxel """
    global boat_x, boat_y
    wave_height = noise.pnoise2(boat_x * 0.2, boat_y * 0.2, octaves=4, repeatx=100, repeaty=100) * 0.5
    boat_z = water_level + wave_height + 0.5
    draw_voxel(boat_x * VOXEL_SIZE, boat_y * VOXEL_SIZE, boat_z, (0.7, 0.3, 0))  # Brown boat

def main():
    global time_step, boat_x, boat_y

    clock = pygame.time.Clock()
    running = True

    while running:
        time_step += 0.1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(5, 5, 5, 5, 5, 0, 0, 0, 1)  # Camera

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    boat_y = min(GRID_SIZE - 1, boat_y + 1)
                elif event.key == K_DOWN:
                    boat_y = max(0, boat_y - 1)
                elif event.key == K_LEFT:
                    boat_x = max(0, boat_x - 1)
                elif event.key == K_RIGHT:
                    boat_x = min(GRID_SIZE - 1, boat_x + 1)

        # Render water and boat
        generate_water(time_step)
        draw_boat()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
