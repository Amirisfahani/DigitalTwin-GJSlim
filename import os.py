import os
import sys
import math
import gmsh

gmsh.initialize()
gmsh.clear()
gmsh.model.add("test1")



# Imports shapes from a STEP file into a Gmsh model.
path = os.path.dirname(os.path.abspath(__file__))
v = gmsh.model.occ.importShapes(os.path.join(path, 'sample1.stp'))

# Get the bounding box of the volume:
xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.occ.getBoundingBox(
    v[0][0], v[0][1])

# We want to slice the model into N slices, and either keep the volume slices
# or just the surfaces obtained by the cutting:
N = 1  # Number of slices
dir = 'Y' # Direction: 'X', 'Y' or 'Z'
surf = False  # Keep only surfaces?

dx = (xmax - xmin)
dy = (ymax - ymin)
dz = (zmax - zmin)
L = dz if (dir == 'X') else dx
H = dz if (dir == 'Y') else dy

# Create the first cutting plane:
s = []
s.append((2, gmsh.model.occ.addRectangle(xmin, ymin, zmin, L, H)))
if dir == 'X':
    gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 0, 1, 0, -math.pi/2)
elif dir == 'Y':
    gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 1, 0, 0, math.pi/2)
tx = dx / N if (dir == 'X') else 0
ty = dy / N if (dir == 'Y') else 0
tz = dz / N if (dir == 'Z') else 0
gmsh.model.occ.translate([s[0]], tx, ty, tz)

# Create the other cutting planes:
for i in range(1, N-1):
    s.extend(gmsh.model.occ.copy([s[0]]))
    gmsh.model.occ.translate([s[-1]], i * tx, i * ty, i * tz)

# Fragment (i.e. intersect) the volume with all the cutting planes:
gmsh.model.occ.fragment(v, s)

# Now remove all the surfaces (and their bounding entities) that are not on the
# boundary of a volume, i.e. the parts of the cutting planes that "stick out" of
# the volume:
gmsh.model.occ.remove(gmsh.model.occ.getEntities(2), True)
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)

gmsh.write("t20.msh")
gmsh.finalize()

