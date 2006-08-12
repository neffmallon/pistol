#!/usr/bin/env python

class Octree:
    def __init__(self,nlevels,bbox):
        self.nlevels = nlevels

        self.set_bbox(bbox)
        self.build_levels()
        self.build_neighbors()
        self.build_tree()
        return

    def set_bbox(self,bbox):
        self.bbox = bbox
        self.xmin,self.xmax = self.bbox[0],self.bbox[1]
        self.dx = self.xmax-self.xmin
        self.ymin,self.ymax = self.bbox[2],self.bbox[3]
        self.dy = self.ymax-self.ymin
        self.zmin,self.zmax = self.bbox[4],self.bbox[5]
        self.dz = self.zmax-self.zmin
        return

    def build_levels(self):
        self.levels = []
        for i in range(self.nlevels): self.build_level(i)
        return

    def build_level(self,level):
        if level == 0:
            cell = Cell(self.bbox)
            self.levels.append([cell])
        else:
            ncellx = ncelly = ncellz = pow(2,level)
            dx, dy, dz = self.dx/ncellx, self.dy/ncelly, self.nz/ncellz
            level = []
            self.levels.append(level)
            for i in range(ncellx):
                xmin = self.xmin + i*dx
                xmax = xmin + dx
                for j in range(ncelly):
                    ymin = self.ymin + j*dy
                    ymax = ymin+dy
                    for k in range(ncellz):
                        zmin = self.zmin + k*dz
                        zmax = zmin+dz
                        level.append((xmin,xmax,ymin,ymax,zmin,zmax))
        return
    def build_neighbors(self): return
    def build_tree(self): return
    def add_atoms(self,atoms): return
    def get_cell(self,xyz,level=-1): return

class Cell:
    def __init__(self,bbox):
        self.bbox = bbox
        return

    
