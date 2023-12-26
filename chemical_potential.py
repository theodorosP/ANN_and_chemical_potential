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
eners = []


for id in [0, 1, 2, 3, 4, 5, 6, 8, 10 ]:
    print ( ' READ ' + str( id )) 
    path_6x6x1 = fix_path( database[str(id+16)+'/16_ML_Pb_on_4x4Ge111_constrained' ][ '6x6x1_path' ] )
    system = read( path_6x6x1 + 'CONTCAR' )	
    nPb.append( count_nPb( system ) )
    ener = get_energy(path_6x6x1 + 'OUTCAR' )
    eners.append( ener )



coverage = []
muy	 = []
gamma1    = []
gamma2    = []
for id in range( 1, len( nPb ) ):
    coverage.append( nPb[ id ] / nPb[ 0 ] )
    muy.append ( ( eners[ id ] - eners[ id -1 ] ) / ( nPb[ id ] - nPb[ id - 1]) )
    path_6x6x1 = fix_path( database[str(id+16)+'/16_ML_Pb_on_4x4Ge111_constrained' ][ '6x6x1_path' ] )
    system = read( path_6x6x1 + 'OUTCAR' )
    gamma1.append( calculate_gamma( system, muy[ -1 ]  ) )
    gamma2.append( calculate_gamma( system, muy_Pb  ) )

print(len(coverage), len(muy))


# muy 2 layers

ID = '31/16_ML_Pb/4x4Ge111_not_constrained'
path_6x6x1 = fix_path( database[ ID ][ '6x6x1_path' ] )
system = read( path_6x6x1 + '/CONTCAR' )
n31 =  count_nPb( system ) 
ener31 = get_energy(path_6x6x1 + '/OUTCAR' )

ID = '32/16_ML_Pb/4x4Ge111_not_constrained'
path_6x6x1 = fix_path( database[ ID ][ '6x6x1_path' ] )
system = read( path_6x6x1 + '/CONTCAR' )
n32 =  count_nPb( system ) 
ener32 = get_energy(path_6x6x1 + '/OUTCAR' )

muy_2ML = ( ener32 - ener31 ) / ( n32 - n31 ) - muy_Pb

print ( "%12s %12s" %( 'Coverage', 'DeltaMuy' )  )
for id in range( len( coverage )) :
    print ( "%12.4f %12.6f eV" %( coverage[ id ] , muy[ id ] - muy_Pb )  )

#print(c)
#print(coverage)

cov = coverage
dmuy =muy #muy[0:6] + muy[7:8] + muy[ 9: ]
dgamma1 =gamma1 #gamma[0:6] + gamma[7:8] + gamma[ 9: ]
dgamma2 =gamma2 #gamma[0:6] + gamma[7:8] + gamma[ 9: ]
print ( dmuy )

print(cov)
print( np.array( dmuy ) - muy_Pb)
print(muy_Pb)
