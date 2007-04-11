class MatrixViewer:
    def __init__(self,height=300,width=300,filename='tmp.ps'):
        from Tkinter import Tk, Canvas, Frame, Button
        self.width=width
        self.height=height
        self.root = Tk()
        self.canvas = Canvas(self.root,width=self.width,height=self.height,
                             background='White')
        self.canvas.pack()
        self.toolbar = Frame(self.root)
        self.dumpbutton = Button(self.toolbar,text="Dump",command=self.dump)
        self.dumpbutton.pack(side=LEFT)
        self.quitbutton = Button(self.toolbar,text="Quit",
                                 command=self.root.quit)
        self.quitbutton.pack(side=LEFT)
        self.toolbar.pack()
        self.filename = filename
        return

    def dump(self):
        ps = self.canvas.postscript()
        file = open(self.filename,'w')
        file.write(ps)
        file.close()
        return

    def spy(self,A,cutoff=0.1):
        n,m = A.shape
        if n>self.width or m>self.height: raise "Rectangle too big %d %d %d %d" %\
           (n,m,self.width,self.height)
        for i in range(n):
            xmin = self.width*i/float(n)
            xmax = self.width*(i+1)/float(n)
            for j in range(m):
                ymin = self.height*j/float(m)
                ymax = self.height*(j+1)/float(m)
                if abs(A[i,j]) > cutoff:
                    self.canvas.create_rectangle(xmin,ymin,
                                                 xmax,ymax,fill='Blue',
                                                 outline='')
                else:
                    self.canvas.create_rectangle(xmin,ymin,
                                                 xmax,ymax,fill='White',
                                                 outline='')
        self.root.mainloop()
        return
        
    def pcolor(self,A):
        n,m = A.shape
        mina,maxa = get_extrema(A)
        if n>self.width or m>self.height: raise "Rectangle too big"
        for i in range(n):
            xmin = self.width*i/float(n)
            xmax = self.width*(i+1)/float(n)
            for j in range(m):
                ymin = self.height*j/float(m)
                ymax = self.height*(j+1)/float(m)
                color = get_color(A[i,j],mina,maxa)
                self.canvas.create_rectangle(xmin,ymin,xmax,ymax,fill=color)
        self.root.mainloop()
        return


class MatrixViewerPIL:
    def __init__(self,height=300,width=300,filename='tmp.png'):
        import Image,ImageDraw

        self.height = height
        self.width = width
        
        self.img = Image.new("RGB",(width,height),(255,255,255))
        self.draw = ImageDraw.Draw(self.img)
        self.filename = filename
        
    
    def spy(self,A,cutoff=0.1,fname=None):
        if not fname: fname = self.filename
        n,m = A.shape
        if n>self.width or m>self.height:
            raise "Rectangle too big %d %d %d %d" % (n,m,self.width,self.height)
        for i in range(n):
            xmin = self.width*i/float(n)
            xmax = self.width*(i+1)/float(n)
            for j in range(m):
                ymin = self.height*j/float(m)
                ymax = self.height*(j+1)/float(m)
                if abs(A[i,j]) > cutoff:
                    self.draw.rectangle((xmin,ymin,xmax,ymax),fill=(0,0,255),
                                        outline=(0,0,0))
                #else:
                #    self.draw.rectangle(xmin,ymin,
                #                        xmax,ymax,fill='White',
                #                        outline='')
        self.img.save(fname)
        return
        
    def pcolor(self,A,fname=None):
        if not fname: fname = self.filename
        n,m = A.shape
        mina,maxa = get_extrema(A)
        if n>self.width or m>self.height: raise "Rectangle too big"
        for i in range(n):
            xmin = self.width*i/float(n)
            xmax = self.width*(i+1)/float(n)
            for j in range(m):
                ymin = self.height*j/float(m)
                ymax = self.height*(j+1)/float(m)
                color = get_color(A[i,j],mina,maxa)
                self.draw.rectangle((xmin,ymin,xmax,ymax),fill=color)
        self.img.save(fname)
        return

def spy_matrix_pil(A,fname='tmp.png',cutoff=0.1,do_outline=0,
                   height=300,width=300):
    """\
    Use a matlab-like 'spy' function to display the large elements
    of a matrix using the Python Imaging Library.

    Arguments:
    A          Input Numpy matrix
    fname      Output filename to which to dump the graphics (default 'tmp.png')
    cutoff     Threshold value for printing an element (default 0.1)
    do_outline Whether or not to print an outline around the block (default 0)
    height     The height of the image (default 300)
    width      The width of the image (default 300)

    Example:
    >>> from numpy import identity,Float
    >>> a = identity(10,Float)
    >>> spy_matrix_pil(a)
    
    """
    import Image,ImageDraw
    img = Image.new("RGB",(width,height),(255,255,255))
    d = ImageDraw.Draw(img)

    n,m = A.shape
    if n>width or m>height:
        raise "Rectangle too big %d %d %d %d" % (n,m,width,height)
    fl = (0,0,255)
    ol = fl
    if do_outline: ol = (0,0,0)
    A = abs(A)>cutoff
    scalex = width/float(n)
    scaley = height/float(m)
    for i in range(n):
        xmin = i*scalex
        xmax = (i+1)*scalex
        for j in range(m):
            ymin = j*scaley
            ymax = (j+1)*scaley
            if A[i,j]:
                d.rectangle((xmin,ymin,xmax,ymax),fill=fl,outline=ol)
    img.save(fname)
    return

def pcolor_matrix_pil(A,fname='tmp.png',do_outline=0,
                      height=300,width=300):
    """\
    Use a matlab-like 'pcolor' function to display the large elements
    of a matrix using the Python Imaging Library.

    Arguments:
    A          Input Numpy matrix
    fname      Output filename to which to dump the graphics (default 'tmp.png')
    do_outline Whether or not to print an outline around the block (default 0)
    height     The height of the image (default 300)
    width      The width of the image (default 300)

    Example:
    >>> from numpy import identity,Float
    >>> a = identity(10,Float)
    >>> pcolor_matrix_pil(a)
    
    """
    import Image,ImageDraw
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)

    mina,maxa = get_extrema(A)
    n,m = A.shape
    if n>width or m>height:
        raise "Rectangle too big %d %d %d %d" % (n,m,width,height)
    for i in range(n):
        xmin = width*i/float(n)
        xmax = width*(i+1)/float(n)
        for j in range(m):
            ymin = height*j/float(m)
            ymax = height*(j+1)/float(m)
            color = get_color(A[i,j],mina,maxa)
            if do_outline:
                draw.rectangle((xmin,ymin,xmax,ymax),fill=color,
                               outline=(0,0,0))
            else:
                draw.rectangle((xmin,ymin,xmax,ymax),fill=color)
                    
    img.save(fname)
    return
    

def get_color(a,cmin,cmax):
    # rewritten to use recipe 9.10 from the Python Cookbook
    import math
    try: a = float(a-cmin)/(cmax-cmin)
    except ZeroDivisionError: a=0.5 # cmax == cmin
    blue = min((max((4*(0.75-a),0.)),1.))
    red = min((max((4*(a-0.25),0.)),1.))
    green = min((max((4*math.fabs(a-0.5)-1.,0)),1.))
    return '#%1x%1x%1x' % (int(15*red),int(15*green),int(15*blue))

def get_extrema(A):
    n,m = A.shape
    BIG = 10000.0
    max = -BIG
    min = BIG
    for i in range(n):
        for j in range(m):
            if A[i,j] < min:
                min = A[i,j]
            elif A[i,j] > max:
                max = A[i,j]
    return min,max

def spy(*args,**kwargs): return spy_matrix_pil(*args,**kwargs)
def pcolor(*args,**kwargs): return pcolor_matrix_pil(*args,**kwargs)
