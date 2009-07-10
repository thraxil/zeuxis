#!/usr/bin/env python

import pygame
import sys
import random
import time
import Image, ImageOps, ImageDraw

from pygame.locals import *
pygame.init()
window = pygame.display.set_mode(pygame.display.list_modes()[0])
pygame.display.toggle_fullscreen()
screen = pygame.display.get_surface()

seconds = int(sys.argv[1])
images = sys.argv[2:]

SWITCH  = 10
TICK    = 11
counter = 0

current_image = None
posterized = False
posterize_bits = 4
grayscale = False

gridlines = 0

def display():
    global counter
    global current_image, posterized
    im = Image.open(images[random.randint(0, len(images) - 1)])
    mode = im.mode
    im.thumbnail(screen.get_size(),Image.ANTIALIAS)
    assert mode in "RGB", "RGBA"
    current_image = im
    render(im)
    counter = 0

def render(im):
    if grayscale:
        im = ImageOps.grayscale(im)        
        im = ImageOps.colorize(im,"black","white")    
    if posterized:
        im = ImageOps.autocontrast(im)                
        im = ImageOps.posterize(im,posterize_bits)
        im = ImageOps.autocontrast(im)
    if gridlines > 0:
        im = draw_grid(im,gridlines)

    data = im.tostring()
    surface = pygame.image.fromstring(data, im.size, im.mode)
    screen.blit(surface,(0,0))
    pygame.display.flip()

def make_grayscale():
    global grayscale
    if not grayscale:
        grayscale = True
    else:
        grayscale = False
    render(current_image)

def posterize():
    global posterized, posterize_bits
    if not posterized:
        posterized = True
        posterize_bits = 4
    else:
        posterize_bits -= 1
        if posterize_bits < 1:
            posterized = False
    render(current_image)

def grid():
    global gridlines
    gridlines += 1
    if gridlines > 8:
        gridlines = 1
    render(current_image)

def draw_grid(image,lines):
    if lines == 1: return image
    try:
        (width,height) = image.size
        draw = ImageDraw.Draw(image)
        for x in segment(height,lines):
            draw.line([(0,x),(width,x)],fill="red")
        for x in segment(width,lines):
            draw.line([(x,0),(x,height)],fill="red")
#        for c in range(lines):
#            draw.line([(0,int(height/2)),(width,int(height/2))],fill="red")
#            draw.line([(int(width/2),0),(int(width/2),height)],fill="red")
        return image
    except Exception, e:
        print "exception: " + str(e)

def segment(t,n):
    for i in range(1,n):
        yield int((t/n) * i)


def skip():
    # clear the timer
    pygame.time.set_timer(SWITCH,0)
    # display a different image
    display()
    # start the timer over fresh
    pygame.time.set_timer(SWITCH,1000 * seconds)

red    = (255,0,0)
black  = (0,0,0)
white  = (255,255,255)
orange = (255,128,0)
yellow = (255,255,0)

def tick():
    global counter
    background = pygame.Surface((100,50))
    background = background.convert()
    color = white

    if (seconds - counter) < 10:
        color = yellow
    if (seconds - counter) < 7:
        color = orange
    if (seconds - counter) < 3:
        color = red
    background.fill(color)
    font = pygame.font.Font(None, 36)
    text = font.render(str(seconds - counter), 1, (10, 10, 10))

    screen.blit(background, (1500,1150))
    screen.blit(text, (1510,1160))
    pygame.display.flip()
    counter += 1

def input(events):
    for event in events: 
        if event.type == QUIT: 
            sys.exit(0) 
        else:
            if event.type == KEYDOWN and event.key == ord('q'):
                sys.exit(0)
            if event.type == KEYDOWN and event.key == ord('s'):
                skip()
            if event.type == KEYDOWN and event.key == ord('p'):
                posterize()
            if event.type == KEYDOWN and event.key == ord('g'):
                make_grayscale()
            if event.type == KEYDOWN and event.key == ord('l'):
                grid()                                
            if event.type == SWITCH:
                display()
            if event.type == TICK:
                tick()

display()
clock = pygame.time.Clock()
pygame.time.set_timer(SWITCH,1000 * seconds)
pygame.time.set_timer(TICK,1000)

while True:
    clock.tick(60)
    input(pygame.event.get())
    pygame.time.wait(100)
