#!/usr/bin/env python
"""\
Mathematica-style notebook in python/wxpython.
"""

import wx
import re
import sys
from wx.py import shell,frame
from wx.stc import StyledTextCtrl
from code import InteractiveConsole

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        #output = '\n'.join(self.out)
        output = ''.join(self.out)
        self.reset()
        return output

class ShellWindow(StyledTextCtrl):
    "Holds the Shell in a window"
    def __init__(self,*args,**kwargs):
        StyledTextCtrl.__init__(self,*args,**kwargs)
        self.shell = Shell()
        try:
            self.ps1 = sys.ps1
            self.ps2 = sys.ps2
        except:
            self.ps1 = '>>> '
            self.ps2 = '... '
        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
        self.Write(self.ps1)
        self.prompt_pos_end = self.GetCurrentPos()
        return

    def OnKeyDown(self,event):
        key = event.KeyCode()
        if key == wx.WXK_RETURN:
            self.ProcessLine()
        else:
            event.Skip()
        return

    def ProcessLine(self):
        pos = self.GetCurrentPos()
        line = self.GetTextRange(self.prompt_pos_end,pos)
        more,errors,output = self.shell.push(line)
        self.Write('\n')
        self.Write(errors)
        self.Write(output)
        if more:
            self.Write(self.ps2)
        else:
            self.Write(self.ps1)
        self.prompt_pos_end = self.GetCurrentPos()
        return

    def Write(self,text):
        self.AddText(text)
        return

class Shell(InteractiveConsole):
    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.buffer = []
        self.out_cache = FileCacher()
        self.err_cache = FileCacher()
        InteractiveConsole.__init__(self)
        return

    def get_output(self):
        sys.stdout = self.out_cache
        sys.stderr = self.err_cache
        return
    
    def return_output(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return

    def push(self,line):
        self.get_output()
        more = InteractiveConsole.push(self,line)
        self.return_output()
        output = self.out_cache.flush()
        errors = self.err_cache.flush()
        return more,errors,output
        

class Frame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='Notebook',
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.win = ShellWindow(self)
        self.win.Show()
        return

def test():
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
    return

if __name__ == '__main__': test()
