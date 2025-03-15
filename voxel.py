import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

CHUNK_SIZE = 16
WORLD_SIZE = 4  # World is WORLD_SIZE * CHUNK_SIZE voxels in each dimension
BLOCK_TYPES = {
    0: None,  # Air
    1: (0.5, 0.5, 0.5),  # Stone (gray)
    2: (0.6, 0.3, 0.1),  # Wood (brown)
    3: (0.0, 0.8, 0.0),  # Leaves (green)
}

def generate_chunk(chunk_x, chunk_y, chunk_z):
    chunk = np.zeros((CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE), dtype=np.uint8)
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                world_x = chunk_x * CHUNK_SIZE + x
                world_y = chunk_y * CHUNK_SIZE + y
                world_z = chunk_z * CHUNK_SIZE + z
                if world_z < 8 and (world_x % 4 != 0 or world_y % 4 != 0):
                    chunk[x, y, z] = 1 #stone
                if world_z == 8 and (world_x%8==0 and world_y%8==0):
                    chunk[x,y,z] = 2; #wood
                if world_z>8 and world_z<12 and (world_x%8==0 and world_y%8==0):
                    chunk[x,y,z]=3 #leaves
    return chunk

def draw_cube(x, y, z, color):
    glColor3fv(color)
    glBegin(GL_QUADS)
    vertices = (
        (x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z),
        (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1),
        (x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1),
        (x, y, z), (x + 1, y, z), (x + 1, y, z + 1), (x, y, z + 1),
        (x, y, z), (x, y + 1, z), (x, y + 1, z + 1), (x, y, z + 1),
        (x + 1, y, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x + 1, y, z + 1),
    )
    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()

def draw_chunk(chunk, chunk_x, chunk_y, chunk_z):
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                block_type = chunk[x, y, z]
                if block_type != 0:
                    color = BLOCK_TYPES[block_type]
                    draw_cube(chunk_x * CHUNK_SIZE + x, chunk_y * CHUNK_SIZE + y, chunk_z * CHUNK_SIZE + z, color)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
    glTranslatef(-WORLD_SIZE * CHUNK_SIZE / 2, -WORLD_SIZE * CHUNK_SIZE / 2, -WORLD_SIZE * CHUNK_SIZE * 1.5)
    glEnable(GL_DEPTH_TEST)

    chunks = {}
    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                chunks[(x, y, z)] = generate_chunk(x, y, z)

    rx, ry = 0, 0
    move_speed = 0.5
    rotate_speed = 0.5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: rx -= rotate_speed
                if event.key == pygame.K_RIGHT: rx += rotate_speed
                if event.key == pygame.K_UP: ry += rotate_speed
                if event.key == pygame.K_DOWN: ry -= rotate_speed
                if event.key == pygame.K_w: glTranslatef(0,0,move_speed)
                if event.key == pygame.K_s: glTranslatef(0,0,-move_speed)
                if event.key == pygame.K_a: glTranslatef(move_speed,0,0)
                if event.key == pygame.K_d: glTranslatef(-move_speed,0,0)
                if event.key == pygame.K_SPACE: glTranslatef(0,move_speed,0)
                if event.key == pygame.K_LCTRL: glTranslatef(0,-move_speed,0)

        glRotatef(ry, 1, 0, 0)
        glRotatef(rx, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for chunk_pos, chunk_data in chunks.items():
            draw_chunk(chunk_data, chunk_pos[0], chunk_pos[1], chunk_pos[2])

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()