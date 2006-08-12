#!/usr/bin/env python
"Sierpinski curves in Python."

from math import sin,cos,pi
deg2rad = pi/180.

class Drawer:
    """\
    Class to encapsulate drawing-related functions.
    """
    def __init__(self,**opts):
        import Image, ImageDraw
        self.width = opts.get('width',256)
        self.height = opts.get('height',256)
        self.fname = opts.get('fname','curve.png')
        self.stride = opts.get('stride',4)
        
        self.img = Image.new("RGB",(self.width,self.height),(255,255,255))
        self.imgdraw = ImageDraw.Draw(self.img)
        #self.x = self.width/2
        #self.y = self.height/2
        self.x = self.width# + self.stride
        self.y = 0
        self.orient = 0
        return

    def save(self): self.img.save(self.fname,'PNG')
    def left(self): self.orient = (self.orient+90)%360
    def right(self): self.orient = (self.orient-90)%360

    def advance(self):
        xnew = self.x + int(self.stride*cos(self.orient*deg2rad))
        ynew = self.y + int(self.stride*sin(self.orient*deg2rad))
        self.imgdraw.line((self.x,self.y,xnew,ynew),(0,0,0))
        self.x,self.y = xnew,ynew
        return

    def zig(self,n):
        if n == 1:
            self.left()
            self.advance()
            self.left()
            self.advance()
        else:
            self.zig(n/2)
            self.zag(n/2)
            self.zig(n/2)
            self.zag(n/2)
        return

    def zag(self,n):
        if n == 1:
            self.right()
            self.advance()
            self.right()
            self.advance()
            self.left()
            self.advance()
        else:
            self.zag(n/2)
            self.zag(n/2)
            self.zig(n/2)
            self.zag(n/2)
        return

def main(**opts):
    import os
    n = opts.get('n',64)
    draw = Drawer(stride=2)
    draw.zig(n)
    draw.zig(n)
    draw.save()
    os.system('open curve.png')
    return

if __name__ == '__main__': main()

