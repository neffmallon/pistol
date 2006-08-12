#!/usr/bin/env python
"""\
NAME
      PIL.py - Interface to Python Imaging Libraries

DESCRIPTION
      This is a slightly simplified interface to the functions in
      the Python Imaging Libraries, that somewhat mimicks the
      interface I have used in SVG, HTML, VRML, etc., of writing
      a file an image or a page at a time.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""
import os
display_prog = 'display' # Command to execute to display images.
      
class Scene:
    def __init__(self,name="pil",height=400,width=400):
        try:
            import Image,ImageDraw
        except:
            raise "You must install the Python Imaging Library"

        self.name = name
        self.height = height
        self.width = width
        self.img = Image.new("RGB",(width,height),(255,255,255))
        self.draw = ImageDraw.Draw(self.img)
        return

    def write(self,filename=None):
        if filename:
            self.outname = filename
        else:
            self.outname = self.name + ".png"
        self.img.save(self.outname,"PNG")
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.outname))
        return

    def add_line(self,start,end,fill=(0,0,0)):
        self.draw.line((start[0],start[1],end[0],end[1]),fill=fill)
        return

    def add_circle(self,center,radius,color):
        self.draw.ellipse((center[0]-radius,center[1]-radius,
                           center[0]+radius,center[1]+radius),
                          fill=color,outline=(0,0,0))
        return

if __name__ == '__main__':
    scene = Scene('test')
    scene.add_line((200,200),(200,300))
    scene.add_line((200,200),(300,200))
    scene.add_line((200,200),(100,200))
    scene.add_line((200,200),(200,100))
    scene.add_circle((200,200),30,(0,0,255))
    scene.add_circle((200,300),30,(0,255,0))
    scene.add_circle((300,200),30,(255,0,0))
    scene.add_circle((100,200),30,(255,255,0))
    scene.add_circle((200,100),30,(255,0,255))
    scene.write()
    scene.display()



