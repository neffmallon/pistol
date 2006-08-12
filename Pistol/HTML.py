#!/usr/bin/env python
"""\
NAME
        HTML.py - A module for creating HTML web pages.

DESCRIPTION
        An object-oriented module for creating and printing web
        pages.

        A page is created using the HTML() class call. Different
        type of objects (headers with titles, bodies, lists,
        images, etc.).

        The intention is that all of the containers can hold both
        text and other objects. Tables and lists work that way, and
        it is my intention that the other objects function in the
        same way.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

class HTML:
    def __init__(self,title="Web page written by HTML.py"):
        self.header = ["<HTML>\n"]
        self.footer = ["</HTML>\n"]
        self.head = Head(title)
        self.body = Body()
        return

    def add(self,item): self.body.add(item)

    def strarray(self):
        return self.header + self.head.strarray() + self.body.strarray() +\
               self.footer

    def write(self,filename):
        file = open(filename,'w')
        file.writelines(self.strarray())
        file.close()
        return

class Head:
    def __init__(self,title):
        self.header = ["<HEAD>\n"]
        self.footer = ["</HEAD>\n"]
        self.title = Title(title)
        return

    def strarray(self):
        return self.header + self.title.strarray() + self.footer

class Body:
    def __init__(self):
        self.header = ["<BODY>\n"]
        self.footer = ["</BODY>\n"]
        self.items = []
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        val = []
        val += self.header
        for item in self.items: val += item.strarray()
        val += self.footer
        return val

class TagString:
    "Generic object for one-line object delimited by tags"
    def __init__(self,item):
        self.header = ["<%s>\n" % self.tag]
        self.footer = ["</%s>\n" % self.tag]
        self.item = item
        return
    
    def strarray(self):
        val = []
        val += self.header
        if type(self.item) == type(""): # it's a string
            val += ["%s\n" % self.item]
        else: # assume it is something that it's an obj w/strarray
            val += self.item.strarray()
        val += self.footer
        return val

class Title(TagString): tag = "TITLE"
class H1(TagString): tag = "H1"
class H2(TagString): tag = "H2"
class H3(TagString): tag = "H3"
class P(TagString): tag = "P"
class B(TagString): tag = "B"
class I(TagString): tag = "I"
class Sup(TagString): tag = "SUP"
class Sub(TagString): tag = "SUB"

class PLines:
    "Multi-line version of <P>"
    def __init__(self):
        self.header = ["<P>\n"]
        self.footer = ["</P>\n"]
        self.items = []
        return

    def add(self,item): self.items.append(item)

    def addline(self,item):
        self.items.append(item)
        self.items.append(BR())
        return

    def strarray(self):
        val = []
        val += self.header
        for item in self.items:
            if type(item) == type(""): #string
                val += ["%s\n" % item]
            else:
                val += item.strarray()
        val += self.footer
        return val

# Cite and Pre are the same as PLines, except they have different tags
class Cite(PLines):
    def __init__(self):
        PLines.__init__(self)
        self.header = ["<CITE>\n"]
        self.footer = ["</CITE>\n"]

class Pre(PLines):
    def __init__(self):
        PLines.__init__(self)
        self.header = ["<PRE>\n"]
        self.footer = ["</PRE>\n"]

class Table:
    def __init__(self):
        self.header = ["<TABLE>\n"]
        self.footer = ["</TABLE>\n"]
        self.rows = []
        return

    def add(self,rowitems): self.rows.append(TableRow(rowitems))

    def strarray(self):
        val = []
        val += self.header
        for row in self.rows: val += row.strarray()
        val += self.footer
        return val

class TableRow:
    def __init__(self,items):
        self.header = ["<TR VALIGN=\"TOP\">\n"]
        self.footer = ["</TR>\n"]
        self.items = []
        for item in items: self.items.append(TableRowItem(item))
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        val = []
        val += self.header
        for item in self.items: val += item.strarray()
        val += self.footer
        return val

class TableRowItem(TagString): tag = "TD"

class Comment:
    def __init__(self,text):
        self.text = text

    def strarray(self): return ["<!-- %s -->\n" % self.text]        

class BR:
    def strarray(self): return ["<BR>\n"]

class HR:
    def strarray(self): return ["<HR>\n"]

class IMG:
    def __init__(self,link,alt="Image file",height=None,width=None):
        self.link = link
        self.alt = alt
        self.height = height
        self.width = width
        return

    def strarray(self):
        val = ["<img src=\"%s\" alt=\"%s\"" % (self.link,self.alt)]
        if self.height:
            val += ["height=%d" % self.height]
        if self.width:
            val += ["width=%d" % self.width]
        val += [">\n"]
        return [" ".join(val)] # make a one-item strarray

class AbstractList:
    def __init__(self,title=None,items=None):
        self.title = title
        self.items = [] 
        if items: # can pass in a list of strings in items
            for item in items: self.add(item)
        return

    def add(self,text): self.items.append(LI(text))

    def strarray(self):
        val = []
        val += self.header
        if self.title:
            if type(self.title) == type(""):
                val += ["%s\n" % self.title]
            else:
                val += self.title.strarray()
        for item in self.items: val += item.strarray()
        val += self.footer
        return val

class UL(AbstractList):
    def __init__(self,title=None,items=None):
        AbstractList.__init__(self,title,items)
        self.header = ["<UL>\n"]
        self.footer = ["</UL>\n"]

class OL(AbstractList):
    def __init__(self,title=None,items=None):
        AbstractList.__init__(self,title,items)
        self.header = ["<OL>\n"]
        self.footer = ["</OL>\n"]

class LI(TagString): tag = "LI"

class Link:
    def __init__(self,link,text):
        self.link = link
        self.header = ["<a href=\"%s\">\n" % link]
        self.footer = ["</a>\n"]
        self.text = text
        return

    def strarray(self):
        val = []
        val += self.header
        if type(self.text) == type(""): # it's a string
            val += ["%s\n" % self.text]
        else: # assume it is something that it's an obj w/strarray
            val += self.text.strarray()
        val += self.footer
        return val
        
            

if __name__ == '__main__':
    page = HTML("Rick's Test Page")
    page.add(H1("This is Rick's web page"))
    page.add(Comment("This is a simple page to test my HTML module"))
    page.add(Comment("These lines are comments and should not show up"))
    multilines = PLines()
    multilines.add("1")
    multilines.add("This is a multi-line section")
    multilines.add("3")
    page.add(multilines)
    page.add(Comment("Testing to see what a table looks like"))
    table = Table()
    page.add(table)
    table.add(["1","2","3"])
    table.add(["5","6","7","8"])
    page.add(Comment("Another comment - testing OLs"))
    ol = OL(["a","b","c","d"])
    page.add(ol)
    ol.add("e")
    ml = PLines()
    page.add(ml)
    ml.add("Testing normal text\n")
    ml.add(BR())
    ml.add("There should have been a return before this")
    ml.add(B("Testing Bold text"))
    ml.add(I("Testing Italics"))
    ml.add(HR())
    ml.add("Testing ")
    ml.add(Sup("Superscript"))
    ml.add(Sub("Subscripts"))           
    for line in page.strarray(): print line,
    page.write('bs.html')
