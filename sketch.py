#!/usr/bin/env python

import pygame
import sys
import random
import time
import Image, ImageOps, ImageDraw

#from pygame.locals import *


RED    = (255,0,0)
BLACK  = (0,0,0)
WHITE  = (255,255,255)
ORANGE = (255,128,0)
YELLOW = (255,255,0)

SWITCH  = 10
TICK    = 11

def clear():
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)
    screen.blit(background, (0,0))
    pygame.display.flip()


class App:
    def __init__(self,seconds,images=None):
        self.counter = 0

        self.current_image = None
        self.posterized = False
        self.posterize_bits = 4
        self.grayscale = False

        self.gridlines = 1
        self.seconds = seconds
        if images is None:
            self.images = []
        else:
            self.images = images

    def display(self):
        clear()
        im = Image.open(self.images[random.randint(0, len(self.images) - 1)])
        mode = im.mode
        im.thumbnail(screen.get_size(),Image.ANTIALIAS)
        assert mode in "RGB", "RGBA"
        self.current_image = im
        self.render(im)
        self.counter = 0

    def skip(self):
        # clear the timer
        pygame.time.set_timer(SWITCH,0)
        # display a different image
        self.display()
        # start the timer over fresh
        pygame.time.set_timer(SWITCH,1000 * self.seconds)

    def input(self,events):
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0) 
            else:
                if event.type == KEYDOWN and event.key == ord('q'):
                    sys.exit(0)
                if event.type == KEYDOWN and event.key == ord('s'):
                    self.skip()
                if event.type == KEYDOWN and event.key == ord('p'):
                    self.posterize()
                if event.type == KEYDOWN and event.key == ord('g'):
                    self.make_grayscale()
                if event.type == KEYDOWN and event.key == ord('l'):
                    self.grid()                                
                if event.type == SWITCH:
                    self.display()
                if event.type == TICK:
                    self.tick()

    def tick(self):
        background = pygame.Surface((100,50))
        background = background.convert()
        color = WHITE

        if (self.seconds - self.counter) < 10:
            color = YELLOW
        if (self.seconds - self.counter) < 7:
            color = ORANGE
        if (self.seconds - self.counter) < 3:
            color = RED
        background.fill(color)
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.seconds - self.counter), 1, (10, 10, 10))

        (sw,sh) = screen.get_size()
        screen.blit(background, (sw - 100,sh - 50))
        screen.blit(text, (sw - 90,sh - 40))
        pygame.display.flip()
        self.counter += 1

    def make_grayscale(self):
        if not self.grayscale:
            self.grayscale = True
        else:
            self.grayscale = False
        self.render(self.current_image)

    def posterize(self):
        if not self.posterized:
            self.posterized = True
            self.posterize_bits = 4
        else:
            self.posterize_bits -= 1
            if self.posterize_bits < 1:
                self.posterized = False
        self.render(self.current_image)

    def grid(self):
        self.gridlines += 1
        if self.gridlines > 8:
            self.gridlines = 1
        self.render(self.current_image)

    def render(self,im):
        im2 = im.copy()
        if self.grayscale:
            im2 = ImageOps.grayscale(im2)        
            im2 = ImageOps.colorize(im2,"black","white")    
        if self.posterized:
            im2 = ImageOps.autocontrast(im2)                
            im2 = ImageOps.posterize(im2,self.posterize_bits)
            im2 = ImageOps.autocontrast(im2)
        if self.gridlines > 0:
            im2 = draw_grid(im2,self.gridlines)

        data = im2.tostring()
        surface = pygame.image.fromstring(data, im2.size, im2.mode)
        screen.blit(surface,(0,0))
        pygame.display.flip()


def draw_grid(image,lines):
    if lines == 1: return image
    try:
        (width,height) = image.size
        draw = ImageDraw.Draw(image)
        for x in segment(height,lines):
            draw.line([(0,x),(width,x)],fill="red")
        for x in segment(width,lines):
            draw.line([(x,0),(x,height)],fill="red")
        return image
    except Exception, e:
        print "exception: " + str(e)

def segment(t,n):
    for i in range(1,n):
        yield int((t/n) * i)


if __name__ ==  "__main__":
    pygame.init()
    window = pygame.display.set_mode(pygame.display.list_modes()[0])
    pygame.display.toggle_fullscreen()
    screen = pygame.display.get_surface()
    pygame.mouse.set_visible(False)

    seconds = int(sys.argv[1])
    
    clock = pygame.time.Clock()
    pygame.time.set_timer(SWITCH,1000 * seconds)
    pygame.time.set_timer(TICK,1000)

    app = App(seconds,images=sys.argv[2:])
    app.display()

    while True:
        clock.tick(60)
        app.input(pygame.event.get())
        pygame.time.wait(100)
