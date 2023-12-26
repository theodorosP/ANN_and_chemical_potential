import json as js
import getpass
from ase.io import read
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
from ase.io import read
import matplotlib as mpl
import matplotlib
from dlePy.vasp.getdata import get_energy
import getpass
import os



Ang2m = 10**(-10)
eV2J  = 1.60218 * 10 **(-19)

username = getpass.getuser()

def fix_path( path ):
    return path.replace( '~', '/home/' + username )

with open( '/home/' + username + '/PROJ_MetalOnSemiconductor/theodoros/database_theo/database.js', 'r' ) as f:
    database = js.load( f )

# List of all entries:
list_entry = database.keys( )

#for key in list_entry:
#    print( key )


def count_nPb( system ):
    x = [ at.index for at in system if at.symbol == 'Pb' ]
    return len( x )


def get_muy_Pb():
        outcar = fix_path( database[ 'Pb_chem_pot' ][ '6x6x1_path' ] )
        #print(get_energy(outcar+'/OUTCAR'))
        return get_energy(outcar+'/OUTCAR')


def get_muy_Ge():
        outcar = fix_path( database[ 'Ge_chem_pot' ][ '6x6x1_path' ] )
       # print(get_energy(outcar+'/OUTCAR')/2.)
        return get_energy(outcar+'/OUTCAR')/2.


def calculate_gamma( system, muy_Pb  ):
    nGe = len( [ at.index for at in system if at.symbol == 'Ge' ] )
    nPb = len( [ at.index for at in system if at.symbol == 'Pb' ] )
    muy_Ge = get_muy_Ge()

    gamma = system.get_potential_energy() - nGe * muy_Ge - nPb * muy_Pb
    #Ignoring vibrational contribution for now
    print ( system.get_volume() / system.cell[ 2, 2 ] )
    gamma = gamma / 2. / ( system.get_volume() / system.cell[ 2, 2 ] )
    gamma *= ( eV2J / Ang2m / Ang2m )
    return gamma

muy_Pb = get_muy_Pb()
muy_Ge = get_muy_Ge()


nPb = []
energy_not_constrained = []
energy_constrained = []

#c stands for constrained
for id in [0, 1, 2, 3, 4, 5, 6, 8, 10 ]:
        print ( ' READ ' + str( id ))
        path_6x6x1_c= fix_path( database[str(id+16)+'/16_ML_Pb_on_4x4Ge111_constrained' ][ '6x6x1_path' ] )
        system1 = read( path_6x6x1_c + '/CONTCAR' )
        nPb.append( count_nPb( system1 ) )
        en_c = get_energy(path_6x6x1_c + '/OUTCAR' )
        energy_constrained.append( en_c)

print(nPb)
#nc stands for not constrained
for id in [0, 1, 2, 3, 4, 5, 6, 8, 10 ]:
        print ( ' READ ' + str( id ))
        path_6x6x1_nc = fix_path( database[str(id + 16)+'/16_ML_Pb_on_4x4Ge111_not_constrained' ][ '6x6x1_path' ] )
        system2 = read( path_6x6x1_nc + '/CONTCAR' )
        en_nc = get_energy(path_6x6x1_nc + '/OUTCAR' )
        energy_not_constrained.append( en_nc )



coverage = []
muy_c	 = []
muy_nc	 = []
gamma1_c = []
gamma1_nc = []
gamma2_c = []
gamma2_nc = []


for id in range (1, len(nPb)):
	print(nPb[id])
	coverage.append( Fraction(nPb[ id ] , nPb[ 0 ]) )
	muy_c.append ( ( energy_constrained[ id ] - energy_constrained[ id -1 ] ) / ( nPb[ id ] - nPb[ id - 1]) )
	muy_nc.append( ( energy_not_constrained[ id ] - energy_not_constrained[ id -1 ] ) / ( nPb[ id ] - nPb[ id - 1]) )

	path_1_c= fix_path( database[str(id+16)+'/16_ML_Pb_on_4x4Ge111_constrained' ][ '6x6x1_path' ] )
	system1_c = read( path_1_c +'/OUTCAR' )
	gamma1_c.append( calculate_gamma( system1_c, muy_c[ -1 ]  ) )
	path_1_nc = fix_path( database[str(id + 16)+'/16_ML_Pb_on_4x4Ge111_not_constrained' ][ '6x6x1_path' ] )
	system1_nc = read( path_1_nc + '/OUTCAR' )
	gamma1_nc.append( calculate_gamma( system1_nc, muy_nc[ -1 ]  ) )
	gamma2_c.append( calculate_gamma( system1_c, muy_Pb ) )
	gamma2_nc.append( calculate_gamma( system1_nc, muy_Pb ) )


print(muy_c)
print(muy_nc)

dmuy1 = muy_c
dmuy2 = muy_nc
cov = coverage

np.array( dmuy1 ) - muy_Pb
np.array( dmuy1 ) - muy_Pb


c = []
l1 = []
g1 = []
g2 = []
for i in range(0, 5):
	c.append(cov[i])
	l1.append(np.array(dmuy2[i]) -  muy_Pb)
	g1.append(gamma1_nc[i])
	g2.append(gamma2_nc[i])

print(g1, g2)
plt.gcf().number
plt.plot(cov, np.array( dmuy1 ) - muy_Pb, "-o", label = "Pb constrained")
plt.plot(c,  l1, "-o", label = "Pb no constrained")
plt.axhline(y=0, color='black', linestyle='--',label =  'Bulk Pb')
plt.title("Pb chemical Potential vs Pb coverage")
plt.xlabel("Pb coverage (ML)")
plt.ylabel("$\Delta\mu_{Pb}$ [eV]")
plt.legend(loc = "best", ncol =1 )
plt.savefig("test1.png")
plt.show()
