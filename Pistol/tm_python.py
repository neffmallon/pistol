#!/usr/bin/env python
#
# Ero Carrera (c) 2004
# ero@dkbza.org
#
# Distributed under GPL.

import os
import traceback
import keyword
import re
import string

__version__='0.8.1'
__author__='Ero Carrera'

DATA_ESCAPE = chr(27)
DATA_COMMAND = chr(16)

class Capture:
	"""Capture python output.
	
	Class in charge of recording the output of the
	statements/expressions entered in the TeXmacs
	session and executed in Python.
	"""
	def __init__(self):
		self.text = ''
	def write(self, str):
		self.text += str
	def getOutput(self):
		return self.text
	def flush(self):
		self.text = ''

def data_begin():
	"""Signal the beginning of data to TeXmacs."""
	os.sys.stdout.write(chr(2))

def data_end():
	"""Signal the end of data to TeXmacs."""
	os.sys.stdout.write(chr(5))
	os.sys.stdout.flush()

def texmacs_out(out_str):
	"""Feed data back to TeXmacs.
	
	Output results back to TeXmacs, with the DATA_BEGIN,
	DATA_END control characters."""
	data_begin()
	os.sys.stdout.write(out_str)
	data_end()

def ps_out(ps_file):
	"""Outputs Postscript within TeXmacs.

	According the the type of the argument the following
	scenarios can take place:	

	If the argument is a string and has more than one line, it
	will be processed as raw Postscript data.
	
	If the argument is a string, it's supposed to contain the
	filename of a Postscript file which will be  read ( if the
	file  has no extension, the defaults .ps and .eps will be
	tried.)
	
	If the argument is a file  or other object which provides a
	'read'  method, data will be obtained by calling such
	method.
	
	
	Implemented from suggestion by Alvaro Tejero Cantero.
	Implementation partially based on information provided
	by Mark Arrasmith.
	"""
	
	if 'read' in dir(ps_file):
		data = ps_file.read()
		return chr(2)+'ps:'+data+chr(5)
		
	if ps_file.find('\n')>0:
		return chr(2)+'ps:'+ps_file+chr(5)
	
	ext_list = ['', '.eps', '.ps']
	if isinstance(ps_file, str):
		for ext in ext_list:
			if os.path.exists(ps_file+ext):
				ps_fd = file(ps_file+ext, 'r')
				data = ps_fd.read()
				ps_fd.close()
				break
		else:
			raise IOError('File \''+ps_file+'+'+str(ext_list)+'\' not found.')

	return chr(2)+'ps:'+data+chr(5)

def compose_output(data):
	"""Do some parsing on the output according to its type."""
	if isinstance(data, str):
		return 'verbatim:'+data.strip()
	if isinstance(data, int):
		return 'verbatim: %d' % data
	if isinstance(data, float):
		return 'verbatim: %f' % data
	
	if isinstance(data, unicode):
		data2=r''
		for c in data:
			if c not in string.printable:
				data2+='\\x%x' % ord(c)
			else:
				data2+=c
		data=data2

	return 'verbatim: %s' % str(data)

def do_module_hierarchy(mod, attr):
	"""Explore an object's hierarchy.
	
	Go through the objects hierarchy looking for
	attributes/methods to provide as autocompletion
	options.
	"""
	dot = attr.find('.')
 	if dot>0:
		if hasattr(mod, attr[:dot]):
			next = getattr(mod, attr[:dot])
			return do_module_hierarchy(next, attr[dot+1:])
	if isinstance(mod, dict):
		return dir(mod)
	else:
		return dir(mod)

def find_completion_candidates(cmpl_str, my_globals):
	"""Harvest candidates to provide as autocompletion options."""
	
	haystack = my_globals.keys()+dir(my_globals['__builtins__'])+keyword.kwlist
	dot = cmpl_str.rfind('.')
	offset = None
	if dot>0:
		offset = len(cmpl_str[dot+1:])
		first_dot = cmpl_str[:dot].find('.')
		if first_dot<0:
			mod_name = cmpl_str[:dot]
			r_str = cmpl_str[dot+1:]
		else:
			mod_name = cmpl_str[:first_dot]
			r_str = cmpl_str[first_dot+1:]
		if mod_name in keyword.kwlist:
			return None, []
		if os.sys.modules.has_key(mod_name):
			haystack = do_module_hierarchy(os.sys.modules[mod_name], r_str)
		elif mod_name in my_globals.keys():
			haystack = do_module_hierarchy(my_globals[mod_name], r_str)
		else:
			haystack = do_module_hierarchy(type(mod_name), r_str)
			
	return offset, filter(lambda x:x.find(cmpl_str[dot+1:])  ==  0, haystack)

def name_char(c):
	"""Check whether a character is a valid symbol."""
	if c in '+-*/%<>&|^~ = !,:()[]{}':
		return ' '
	else:
		return c

def complete(cmd, my_globals):
	"""Parse autocomplete command.
	 
	Parse the command and return a suitable answer to
	give back to TeXmacs.
	"""

	# Parse Texmacs command and extract string to
	# complete and offset to complete from.
	cmd = cmd.strip()[:-1]
	cmd_re = re.compile(r'"(.*)"\s+(\d+)')
	res = cmd_re.match(cmd)
	
	# if we don't match anything we return
	# no completion possibilities.
	if res is None:
		return 'scheme:(tuple "" "")'
		
	cmpl_str = res.group(1)
	pos_str = int(res.group(2))
	
	cmpl_str = cmpl_str[:pos_str]
	if len(cmpl_str)  ==  0:
		return 'scheme:(tuple "" "")'
	
	# We get the string after the last space character.
	# no completion is done for strings with spaces
	# within
	cmpl_str = str().join(map(name_char, cmpl_str))
	cmpl_str = cmpl_str.split()[-1]
	pos = len(cmpl_str)
	
	# no string after last space? return empty
	# completion
	if len(cmpl_str)  ==  0:
		return 'scheme:(tuple "" "")'
		
	# Find completion candidates and form a suitable
	# answer to Texmacs
	offset, cand = find_completion_candidates(cmpl_str, my_globals)
	if len(cand) == 0:
		res = '""'
	else:
		res = ''
	for c in cand:
		if offset is not None:
			pos = offset
		res += '"%s" ' % c[pos:]
	return 'scheme:(tuple "'+cmpl_str+'" '+res+')'
		
# Beginning of user defined functions

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

    draw.rectangle((0,0,height-1,width-1),outline=(0,0,0))

    img.save(fname)
    return ps_out(fname)

def plot(*ys,**options):
    """\
    Usage: biggles_render(*ys,**options)
    
    Use biggles to plot different data curves.

    Options:
    xcol        If true, use the first ys column as x values
    filename    Use the value as the filename
    title       Use the value as the title
    xlabel      Use the value as the xlabel
    ylabel      Use the value as the ylabel
    style       'lines' (default) or 'points'
    png_output  Use the value as the name of the png output file
    """
    import biggles

    colors = ['blue','green','red','orange','black','purple']

    biggles.configure('postscript','width','4in')
    biggles.configure('postscript','height','4in')
    p = biggles.FramedPlot()

    fname = options.get("filename","bs.ps")

    title = options.get("title",None)
    if title: p.title(title)

    xlabel = options.get("xlabel",None)
    if xlabel: p.xlabel(xlabel)

    ylabel = options.get("ylabel",None)
    if ylabel: p.ylabel(ylabel)

    style = options.get("style",'lines')

    png_output = options.get("png_output",None)

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
	if style == 'points':
		p.add(biggles.Points(x,y,color=colors[i%len(colors)]))
	else:
		p.add(biggles.Curve(x,y,color=colors[i%len(colors)]))
    p.write_eps(fname)
    if png_output: p.write_img(400,400,png_output)
    return ps_out(fname)

def pixels(data,**options):
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
    return ps_out(fname)

def lines(data,**options):
    "Take a set of lines (list of ((x0,y0),(x1,y1)) coords in data) and render"
    import Image, ImageDraw
    height = options.get("height",200)
    width = options.get("width",200)
    fname = options.get("filename","bs.ps")
    
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)
    for line in data: draw.line(line,(0,0,0))
    img.save(fname,"EPS")
    return ps_out(fname)

# End of user defined functions

texmacs_out("""verbatim:Welcome to Python
TeXmacs Python interface version """+__version__+""". """+__author__+""" (c) 2004
http://dkbza.org/tmPython.html""")

my_globals = {}
# We insert into the session's namespace the 'ps_out' method.
my_globals['ps_out'] = ps_out

# Insert user-defined functions
my_globals['plot'] = plot
my_globals['pixels'] = pixels
my_globals['spy'] = spy
my_globals['lines'] = lines

# As well as some documentation.
my_globals['__doc__'] = """TeXmacs Python plugin.

	TeXmacs Python interface v0.8.1. Ero Carrera (c) 2004
	
	The plugin homepage:
		http://dkbza.org/tmPython.html

	The version distributed with TeXmacs is always the latest.
	
	This plugin has been programed and tested under Python 2.3.3,
	the degree of compatibility with older version is unknown.
	
	For bugs/suggestions/requests I can be reached at ero@dkbza.org.
	
	Enjoy it!
	"""

capt = Capture()
stdout_saved, os.sys.stdout  =  os.sys.stdout, capt
co = compile('import __builtin__ as __builtins__', 'tm_python', 'exec')
eval(co, my_globals)
os.sys.stdout = stdout_saved

# Main session loop.
while 1:
	line = os.sys.stdin.readline()
	if not line:
		texmacs_out('')
	else:
		if line[0]  ==  DATA_COMMAND:
			if line[1:].find('(complete ')  ==  0:
				texmacs_out(complete(line[11:], my_globals))
			continue
		capt = Capture()
		result = None
		# We guess where the lines will break.
		line = re.sub(r' {2}(\s*)', r'\n \1', line)
		try:
			out = eval(line, my_globals)
			result = out
		except:
			try:
				stdout_saved, os.sys.stdout  =  os.sys.stdout, capt
				co = compile(line, 'tm_python', 'exec')
				eval(co, my_globals)
				os.sys.stdout = stdout_saved
				result = capt.getOutput()
			except Exception:
				traceback.print_exc(file = os.sys.stdout, limit = 0)
				os.sys.stdout = stdout_saved
				result = capt.getOutput()
		del capt
		
		out = compose_output(result)
		texmacs_out(out.strip())
