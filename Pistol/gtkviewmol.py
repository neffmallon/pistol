#!/usr/bin/env python
"""\
 A molecular viewer in GtkGL. Not working yet.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import gtk
import gtk.gl

def quit(widget,data=None):
    return gtk.mainquit()

def main():
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event",gtk.mainquit)
    glarea = gtk.gl.Area((gtk.gl.RGBA, gtk.gl.DOUBLEBUFFER,
                          gtk.gl.DEPTH_SIZE, 1), None)
    window.show()
    gtk.mainloop()

if __name__ == '__main__': main()
