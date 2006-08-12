#!/usr/bin/env python
"Helper applications for using TeXmacs"

def spy(A,**options):
    import Image,ImageDraw
    fname = options.get("filename","bs.ps")
    width = options.get("width",200)
    height = options.get("height",200)
    outline = options.get("outline",0)
    cutoff = options.get("cutoff",0.1)

    n,m = A.shape

    width = max(m,width)
    height = max(n,height)

    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)

    for i in range(n):
        xmin = width*i/float(n)
        xmax = width*(i+1)/float(n)
        for j in range(m):
            ymin = height*j/float(m)
            ymax = height*(j+1)/float(m)
            if abs(A[i,j]) > cutoff:
                if outline:
                    draw.rectangle((xmin,ymin,xmax,ymax),fill=(0,0,255),
                                        outline=(0,0,0))
                else:
                    draw.rectangle((xmin,ymin,xmax,ymax),fill=(0,0,255))
    img.save(fname)
    return

def plot(*ys,**options):
    """\
    Usage: biggles_render(*ys,**options)
    
    Use biggles to plot different data curves.

    Options:
    xcol        If true, use the first ys column as x values
    filename    Use the value as the filename
    """
    import biggles

    p = biggles.FramedPlot()

    fname = options.get("filename","bs.ps")

    title = options.get("title",None)
    if title: p.title(title)

    xlabel = options.get("xlabel",None)
    if xlabel: p.xlabel(xlabel)

    ylabel = options.get("ylabel",None)
    if ylabel: p.ylabel(ylabel)

    ncol = len(ys)
    xcol = options.get("xcol",0)
    if xcol:
        xcol = ys[0]
        start = 1
    else:
        start = 0
    
    for i in range(start,ncol):
        y = ys[i]
        if xcol: x = xcol
        else: x = range(len(y))
        p.add(biggles.Curve(x,y,color=colors[i%ncol]))
    p.write_eps(fname)
    return

def pil_pixels(data,**options):
    "Take a set of pixels (list of x,y coords in data) and render"
    import Image, ImageDraw
    height = options.get("height",200)
    width = options.get("width",200)
    fname = options.get("filename","bs.ps")
    
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        for x in range(width):
            if data[y][x]: draw.point((x,y),(0,0,0))
    img.save(fname,"EPS")
    return
