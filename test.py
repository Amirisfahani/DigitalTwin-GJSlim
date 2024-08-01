import os
import sys
import gmsh

path = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(path, os.pardir, 'bar1.stl'))


with open('bar1.stl', 'rb') as file:
    data = file.read()
    
    print(data)
    
gmsh.is_initialized()
gmsh.initialize()
    
gmsh.clear()
path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge("bar1.stl")
