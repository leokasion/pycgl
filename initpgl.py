#!/usr/bin/env python3
# pygame + PyOpenGL

import os
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from pygame import mixer

xrot = yrot = zrot = 0.0
# We need to generate actual texture IDs
textures = [0, 0]

def resize(size):
    # Unpack the tuple inside the function instead of the signature
    width, height = size
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glEnable(GL_TEXTURE_2D)
    # Generate the texture IDs properly
    textures[0] = glGenTextures(1) 
    load_textures()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.2, 0.2, 0.2, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def load_textures():
    # Ensure this path is correct relative to your script
    texturefile = os.path.join('data', 'flan.bmp')
    try:
        textureSurface = pygame.image.load(texturefile)
    except pygame.error:
        print(f"Could not load {texturefile}. Check the 'data' folder.")
        return

    # Use "RGBA" to match your glTexImage2D call
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

def draw():
    global xrot, yrot, zrot

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)
    glRotatef(zrot, 0.0, 0.0, 1.0)
    
    glBegin(GL_QUADS)
    # Front Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
    # ... (Rest of your faces are identical)
    # Back Face
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
    # Top Face
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
    # Bottom Face       
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
    # Right face
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
    # Left Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
    glEnd()

    xrot += 0.2
    yrot += 0.2
    zrot += 0.2

def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    # Need to initialize the mixer BEFORE loading music
    mixer.init()
    
    try:
        mixer.music.load("/home/leandro/.wine/drive_c/Games/TalonRO/BGM/60.mp3")
        mixer.music.play()
    except:
        print("Music file not found. Skipping audio.")

    pygame.display.set_mode((640, 480), video_flags)
    resize((640, 480))
    init()

    clock = pygame.time.Clock()
    frames = 0
    ticks = pygame.time.get_ticks()
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Calculate final FPS
                duration = (pygame.time.get_ticks() - ticks) / 1000
                if duration > 0:
                    print(f"fps: {frames / duration:.2f}")
                pygame.quit()
                return
        
        draw()
        pygame.display.flip()
        frames += 1
        clock.tick(60) # Limit to 60 FPS so your CPU doesn't melt

if __name__ == '__main__':
    main()
