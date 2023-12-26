from ase.cluster.icosahedron import *
from ase.io import *
from ase import *
from numpy import *

vac = 15
for i in range( 2, 9 ):
    system = Icosahedron( 'Pb', i, latticeconstant = 4.9 ) 
    system.center( )
    c=system.cell[ 0, : ]
    c[ : ] = 0.5 * (system.cell[ 0, : ] + system.cell[ 1, : ] + system.cell[ 2, :])
    system.rotate( 'x', 30, center = c )
    system.cell[ :, : ] = 0
    for j in range( 3 ):
        d = max( system.positions[ :, j] ) - min( system.positions[ :, j ] )
        system.cell[ j, j ] = d + vac
    
    system.center()
    write( 'POSCAR.icosahedron.' + str(i), system, format = 'vasp', direct=True)

vac = 15
for i in range(2,7):
    system=Octahedron('Pb',i,latticeconstant=4.9)
    system.cell[ :, : ] = 0.
    for j in range(3):
        d = max( system.positions[ :, j ] ) - min( system.positions[ :, j] )
        system.cell[ j, j ] = d + vac
    
    system.center()
    write('POSCAR.Octahedron.'+str(i)+'.vasp',system,format='vasp',direct=True)
