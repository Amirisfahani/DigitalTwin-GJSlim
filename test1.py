import os
import sys
import gmsh


gmsh.initialize()
path = os.path.dirname(os.path.abspath(__file__))
newModel = gmsh.model.occ.importShapes(os.path.join(path, 'sample2.step'))
print(gmsh.model.list())
