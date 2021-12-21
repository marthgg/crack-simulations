from molecular_builder.core import create_bulk_crystal, write, carve_geometry
from molecular_builder.geometry import NotchGeometry
import ase.cell 

L = [3000, 120, 600]
thickness_crack = 16 #Ångstrøm

quartz_structure = create_bulk_crystal("alpha_quartz", L) 
cell = quartz_structure.get_cell(); cell[0,1] = 0; cell[1,0] = 0; cell[0,2] = 0; cell[2,0] = 0; cell[1,2] = 0; cell[2,1] = 0
quartz_structure.set_cell(cell); quartz_structure.wrap()

#crack = NotchGeometry([L[0]/10,L[1]/2,L[2]/2], [L[0]/4,0,0], [0,0,L[2]/14])
crack = NotchGeometry([0,L[1]/2,L[2]/2], [200*3,0,0], [0,0,thickness_crack/2])

carve_geometry(quartz_structure, crack, side="in")
write(quartz_structure, "alpha_quartz_structure.data", atom_style='atomic')
