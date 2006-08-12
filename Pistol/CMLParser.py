#!/usr/bin/env python
"""\
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from xml.sax import ContentHandler,make_parser,ErrorHandler
from xml.sax.handler import feature_namespaces

class handler:
    def __init__(self,attr): self.attr = attr
    def wrap(self, parent): parent.on_child(self,tag)

class DocumentRoot(handler):
    def wrap(self, parent): return self.cml
    def on_child(self,child,tag):
        if tag == 'cml': self.cml = child.cml
        if tag == 'molecule': self.cml = child.molecule #? something like this
        return

class cml(handler):
    tag = "cml"

class list(handler):
    tag = "list"

class molecule(handler):
    tag = "molecule"

class crystal(handler):
    tag = "crystal"
    
class atomArray(handler):
    tag = "atomArray"

class atom(handler):
    tag = "atom"

class coordinate3(handler):
    tag = "coordinate3"

class stringArray(handler):
    tag = "stringArray"
    def on_chars(self, chars): self.val = ' '.join(chars.split())

class string(handler):
    tag = "string"
    def on_chars(self, chars): self.val = chars.strip()

class floatArray(handler):
    tag = "floatArray"
    def on_chars(self,chars): self.val = map(float,chars.split())

class float(handler):
    tag = "float"
    def on_chars(self, characters): self.val = float(chars)

class scalar(handler):
    tag = "scalar"

class CMLParser(ContentHandler):
    handlers = [cml, list, molecule, crystal, atomArray, atom, coordinate3,
                stringArray, string, floatArray, float, scalar]

    def __init__(self):
        ContentHandler.__init__(self)
        self.currentNode = None
        self.nodeStack = []
        self.registerHandlers()
        return

    def process(self,filename):
        root = DocumentRoot()
        self.currentNode = root
        parser = make_parser()
        parser.setFeature(feature_namespaces,0)
        parser.setContentHandler(self)
        parser.parse(filename)
        return root.body()

    def startElement(self, name, attributes):
        self.nodeStack.append(self.currentNode)
        self.currentNode = self.tagHandlers[name](attributes)
        return

    def characters(self, characters):
        import string
        characters = string.strip(characters)
        if characters: self.currentNode.on_chars(chars)
        return

    def endElement(self, name):
        node = self.currentNode
        self.currentNode = self.nodeStack.pop()
        node.wrap(self.currentNode)
        return

    def registerHandlers(self):
        self.tagHandlers = {}
        for handler in self.handlers:
            self.tagHandlers[handler.tag] = handler
        return

if __name__ == '__main__':
    import sys
    parser = CMLParser()
    cml = parser.process(sys.argv[1])
    print cml
