#!/usr/bin/env python
"""\
 yaml_utils.py

 Simple utilities written to extend syck functions
 
"""

import sys
import syck

from xml.sax import ContentHandler,make_parser,parse,parseString

spaces_per_level=4

from types import ListType, DictType

class YAMLPrintHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.level = 0          # Current indentation level
        self.indent_spaces = 4  # Number of spaces to indent each level
        self.data = []
        return

    def spaces(self): return self.level*self.indent_spaces*' '
    
    def startElement(self,name,attributes):
        self.data.append("%s- %s:" % (self.spaces(),name.strip()) )
        self.level += 1
        for key in attributes.keys():
            self.data.append("%s- %s : %s" % (self.spaces(),key,
                                                     attributes[key]))
        return 

    def characters(self,chars):
        chars = chars.strip()
        if chars: self.data.append("%s%s" % (self.spaces(),chars))
        return

    def endElement(self,name): self.level -= 1

    def getdata(self): return '\n'.join(self.data)

class XMLNodeHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.root = XMLNode('root')
        self.currentnode = self.root
        self.nodestack = []
        return
    
    def startElement(self,name,attributes):
        self.nodestack.append(self.currentnode)
        parent = self.currentnode
        self.currentnode = XMLNode(name,parent,attributes)
        return 

    def characters(self,chars):
        chars = chars.strip()
        if chars: self.currentnode.add_chars(chars)
        return

    def endElement(self,name): self.currentnode = self.nodestack.pop()

    # Don't know which is better, returning the root and then
    #  not printing the container node, or returning the first child
    #def getroot(self): return self.root
    def getroot(self): return self.root.children[0]

class XMLNode:
    def __init__(self,name,parent=None,attributes={}):
        self.name = name
        self.parent = parent
        if parent: parent.add_child(self)
        self.attributes = attributes
        self.children = []
        self.chars = []
        return

    def add_child(self,child): self.children.append(child)
    def add_chars(self,chars): self.chars.append(chars)
    def add_attr(self,key,value): self.attributes[key] = value

def PrintVisitor(node):
    print node.name
    for key in node.attributes.keys():
        print str(key), ' : ', str(node.attributes[key])
    for child in node.children:
        PrintVisitor(child)
    return

def YAMLPrintVisitor(node,level=0):
    # This captures the bulk of the features from the old YAML handler.
    print "%s- %s:" % (spaces(level),node.name)
    level += 1
    for key in node.attributes.keys():
        print "%s- %s : %s" % (spaces(level),key,node.attributes[key])
    for child in node.children:
        YAMLPrintVisitor(child,level)
    return

def PythonObjectVisitor(node):
    attr = []
    for key in node.attributes.keys():
        attr.append({key:node.attributes[key]})
    for child in node.children:
        attr.append(PythonObjectVisitor(child))
    return {node.name:attr}
    
def xml2yaml(fname):
    handler = XMLNodeHandler()
    parseString(caffeine_cml,handler)
    PrintVisitor(handler.getroot())
    #YAMLPrintVisitor(handler.getroot())
    #print PythonObjectVisitor(handler.getroot())
    return

def render(item,level=0):
    if type(item) == ListType:
        list_render(item,level)
    elif type(item) == DictType:
        dict_render(item,level)
    else:
        default_render(item,level)
    return

def list_render(list,level):
    for item in list: render(item,level)
    return

def dict_render(dict,level):
    for key in dict:
        print "%s<%s>" % (spaces(level),key)
        render(dict[key],level+1)
        print "%s</%s>" % (spaces(level),key)
    return

def default_render(item,level):
    print spaces(level),item
    return

def spaces(level): return level*spaces_per_level*' '

def yaml2xml(fname):
    data = syck.load(open(fname).read())
    render(data)
    return


# Some test files:
caffeine_cml = '''\
<?xml version="1.0" ?>
<cml title="caffeine">
<molecule id="caffeine">
 <atomArray>
  <atom id="H0" elementType="H" x3="-3.380413" y3="-1.127237" z3="0.573304"/>
  <atom id="N1" elementType="N" x3="0.966830" y3="-1.073743" z3="-0.819823"/>
  <atom id="C2" elementType="C" x3="0.056729" y3="0.852719" z3="0.392316"/>
  <atom id="N3" elementType="N" x3="-1.375174" y3="-1.021224" z3="-0.057055"/>
  <atom id="C4" elementType="C" x3="-1.261502" y3="0.259071" z3="0.523413"/>
  <atom id="C5" elementType="C" x3="-0.306834" y3="-1.683633" z3="-0.716934"/>
  <atom id="C6" elementType="C" x3="1.139423" y3="0.187412" z3="-0.270090"/>
  <atom id="N7" elementType="N" x3="0.560263" y3="2.083909" z3="0.825159"/>
  <atom id="O8" elementType="O" x3="-0.492680" y3="-2.818055" z3="-1.209473"/>
  <atom id="C9" elementType="C" x3="-2.632807" y3="-1.730396" z3="-0.006095"/>
  <atom id="O10" elementType="O" x3="-2.230134" y3="0.798862" z3="1.089973"/>
  <atom id="H11" elementType="H" x3="2.549699" y3="2.973498" z3="0.622959"/>
  <atom id="C12" elementType="C" x3="2.052743" y3="-1.736089" z3="-1.493128"/>
  <atom id="H13" elementType="H" x3="-2.480771" y3="-2.726953" z3="0.488263"/>
  <atom id="H14" elementType="H" x3="-3.008904" y3="-1.902525" z3="-1.049802"/>
  <atom id="H15" elementType="H" x3="2.917610" y3="-1.848152" z3="-0.785787"/>
  <atom id="H16" elementType="H" x3="2.378786" y3="-1.121192" z3="-2.374366"/>
  <atom id="H17" elementType="H" x3="1.718988" y3="-2.748992" z3="-1.843921"/>
  <atom id="C18" elementType="C" x3="-0.151845" y3="3.097005" z3="1.534835"/>
  <atom id="C19" elementType="C" x3="1.893410" y3="2.118124" z3="0.419319"/>
  <atom id="N20" elementType="N" x3="2.286125" y3="0.996844" z3="-0.244030"/>
  <atom id="H21" elementType="H" x3="-0.168703" y3="4.043655" z3="0.930109"/>
  <atom id="H22" elementType="H" x3="0.353532" y3="3.297906" z3="2.517775"/>
  <atom id="H23" elementType="H" x3="-1.207450" y3="2.753759" z3="1.720305"/>
 </atomArray>
</molecule>
</cml>
'''


if __name__ == '__main__':
    xml2yaml('/home/rmuller/Library/Preferences/com.apple.mail.plist')
    

