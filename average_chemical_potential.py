theodoros@artemis [14:30:32]$ cat new_average.py 
import matplotlib.pyplot as plt
import numpy as np
import json as js
from fractions import Fraction
from ase.io import read
import matplotlib as mpl
import matplotlib
from dlePy.vasp.getdata import get_energy
import getpass
import os
Ang2m = 10**(-10)
eV2J  = 1.60218 * 10 **(-19)
username=getpass.getuser()

def fix_path( path ):
    return path.replace( '~', '/home/' + username )

with open( '/home/' + username + '/PROJ_MetalOnSemiconductor/theodoros/database_theo/database.js', 'r' ) as f:
    database = js.load( f )

# List of all entries:
list_entry = database.keys( )

def get_muy_Pb(  ):
    outcar = '/home/' + username + '/PROJ_MetalOnSemiconductor/theodoros/Ge_bulk/DOS/SCF/OUTCAR'
    outcar = '/home/' + username + '/PROJ_MetalOnSemiconductor/theodoros/Pb/Pb_chemical_potential/OUTCAR'
    return get_energy( outcar )

def get_muy_Ge(  ):
    outcar = '/home/' + username + '/PROJ_MetalOnSemiconductor/theodoros/Ge_bulk/DOS/SCF/OUTCAR'
    return get_energy( outcar ) / 2.


def calculate_gamma( system, muy_Pb  ):
    nGe = len( [ at.index for at in system if at.symbol == 'Ge' ] ) 
    nPb = len( [ at.index for at in system if at.symbol == 'Pb' ] ) 
    muy_Ge = get_muy_Ge( )

    gamma = system.get_potential_energy() - nGe * muy_Ge - nPb * muy_Pb
    #Ignoring vibrational contribution for now
    print ( system.get_volume() / system.cell[ 2, 2 ] )
    gamma = gamma / 2. / ( system.get_volume() / system.cell[ 2, 2 ] )
    gamma *= ( eV2J / Ang2m / Ang2m )
    return gamma

def get_subdir( folder ):                                                              
     dirs = [ int( x ) for x in os.listdir( folder ) if os.path.isdir( folder + '/' + x 
 ) ]                                                                                    
     if len( dirs ) > 0:                                                                
         subdir = str( sorted( dirs )[ -1 ] )                                           
     else:                                                   
         subdir = '/'                                                                   
     return subdir        


def count_nPb( system ):
    x = [ at.index for at in system if at.symbol == 'Pb' ]
    return len( x )


muy_Pb = get_muy_Pb(  )
muy_Ge = get_muy_Ge(  )

loc1 = "/home/"+ username +"/PROJ_MetalOnSemiconductor/theodoros/6x6/5_system_each_no_constrained/no_constrained_"
loc2 = "/home/"+ username +"/PROJ_MetalOnSemiconductor/theodoros/6x6/5_system_each_constrained/constrained_new_systems_"
loc3 = "/home/"+ username +"/PROJ_MetalOnSemiconductor/theodoros/6x6/2ML/3x3x1/system_"




nPb = [ 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98,100, 102,104, 106, 108, 110,112, 114, 116, 118, 120, 122]
eners = []


for id in range(1, 13):
	a = 0
	for j in range(1, 6):
		print ( ' READ ' + str( id ) )
		folder = loc1 + str(id) + "/3x3x1/system_" + str(j)
		ener = get_energy( folder + '/OUTCAR' )
		a = a + ener		
	eners.append( a )


print(eners)

l = []
#for id in range( 0, 11 ):
for id in [13, 14, 15, 16, 17, 18, 19,20, 21, 22, 23 , 24, 25]:
#for id in [13, 14, 15, 16, 17, 18, 19, 20, 21]:
	a = 0
	for j in range(1, 6):
		print ( ' READ ' + str( id ) )
		folder = loc2 + str(id) + "/3x3x1/system_" + str(j)
		ener = get_energy( folder + '/OUTCAR' )
		a = a + ener
		l.append(ener)
	eners.append( a )

print(eners)

for i in range(0, len(eners)):
	eners[i] = eners[i] / 5
print("*"*30)
print("energy= ", eners)

print("elements of eners : ", len(eners))

energy_not_constrained = []
energy_constrained = []

coverage = []
muy      = []
gamma1    = []
gamma2    = []
for id in range(1, len(nPb)):
    coverage.append( Fraction(nPb[ id ] , nPb[ 0 ]) )
    muy.append ( ( eners[ id ] - eners[ id -1 ] ) / ( nPb[ id ] - nPb[ id - 1]) )	
    print((nPb[ id ] - nPb[ id - 1]))
print ( "%12s %12s" %( 'Coverage', 'DeltaMuy' )  )
for id in range( len( coverage )) :
    print ( "%12.4f %12.6f eV" %( coverage[ id ] , muy[ id ] - muy_Pb )  )

cov = coverage 
dmuy =muy 

dgamma1 =gamma1 
dgamma2 =gamma2 
print ( dmuy )
print(np.array( dmuy ) - muy_Pb)
print( muy_Pb )

print("elements of dmuy: ", len(dmuy))
print("elements of coverage: ", len(cov))

l_2ml = []
for i in range(1, 6):
	folder = loc3 + str(i) 
	ener = get_energy( folder + '/OUTCAR' )
	l_2ml.append(ener)
b = sum(l_2ml) / len(l_2ml)
print(b)

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

fig = plt.figure( figsize = ( 3.5, 3.5 ) )
ax = fig.add_subplot( 1, 1, 1 )

plt.gcf().number
dmuy = np.array( dmuy ) - muy_Pb
n = 20
ax.plot(cov[0:n], dmuy[ 0:n], "-o")

ax.set_xlabel( '' )
ax.set_xticklabels( [] )
ax.set_xticks( np.arange( 1.0, 1.71, 0.1 ) )
#ax.set_ylabel(  r'$\Delta \mu_{Pb} = \mu_{Pb} - \mu_{Pb(Bulk)}$ [eV]', labelpad = 5 )
ax.set_ylabel(  r'$\Delta \mu_{Pb}$ (eV)', labelpad = 2 )
ax.text( 1.02, 3.2, '$\Delta \mu_{Pb} = \mu_{Pb} - \mu_{Pb(Bulk)}$', va = 'top', ha = 'left' )
ax.hlines( 0, 1, 2, linewidth = 0.5)
ax.text( 1.4, -0.01, 'Pb Cluster', va = 'top', ha = 'left' )
ax.hlines( muy_2ML, 1, 2, linewidth = 0.5, color = "C3" )
ax.text( 1.4, muy_2ML + 0.01, '2ML Pb', va = 'bottom', ha = 'left', color = "C3" )
#ax.text( 1.3, 2, '1 Layer of Pb', va = 'bottom', ha = 'center', color = "C0", rotation = 50, fontsize = 12 )

ax.set_xlim(1.0, 1.55 )


ax.set_xlabel( 'Pb Coverage (ML)' )
ax.set_xticks( np.arange( 1.0, 1.71, 0.1 ) )
ax.set_xticklabels( [ round( x, 1 ) for x in np.arange( 1.0, 1.8, 0.1 )])

plt.subplots_adjust(left=0.15, right=0.95, top=0.99, bottom=0.15, wspace=0.01, hspace= 0.01)
plt.savefig("new_avg.png")
