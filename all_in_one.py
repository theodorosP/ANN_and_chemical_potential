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
for id in range(0, 11):
        print ( ' READ ' + str( id ))
        path_6x6x1_c= fix_path( database[str(id+16)+'/16_ML_Pb_on_4x4Ge111_constrained' ][ '6x6x1_path' ] )
        system1 = read( path_6x6x1_c + '/CONTCAR' )
        nPb.append( count_nPb( system1 ) )
        en_c = get_energy(path_6x6x1_c + '/OUTCAR' )
        energy_constrained.append( en_c)


#nc stands for not constrained
for id in range(0 ,11):
        print ( ' READ ' + str( id ))
        path_6x6x1_nc = fix_path( database[str(id + 16)+'/16_ML_Pb_on_4x4Ge111_not_constrained' ][ '6x6x1_path' ] )
        system2 = read( path_6x6x1_nc + '/CONTCAR' )
        en_nc = get_energy(path_6x6x1_nc + '/OUTCAR' )
        energy_not_constrained.append( en_nc )

print(len(nPb))

coverage = []
muy_c	 = []
muy_nc	 = []
gamma1_c = []
gamma1_nc = []
gamma2_c = []
gamma2_nc = []

for id in  range(1, len(nPb)):
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





e = []
for i in range(31, 33):
	path1 = database[ str(i)+'/16_ML_Pb/4x4Ge111_not_constrained' ][ '6x6x1_path' ] 	
	ener = read( path1 + '/OUTCAR' ).get_potential_energy()
	e.append(ener)


diff = (e[1] - e[0])/2 - muy_Pb



y1 = []
y2 = []
c1 = list( np.arange( 0, 1.71, 0.1 ))
for i in range (0, len (c1)):
	y1.append(diff)
	y2.append(0)



c = []
l1 = []
g1 = []
g2 = []
for i in range(0, 5):
	c.append(cov[i])
	l1.append(np.array(dmuy2[i]) -  muy_Pb)
	g1.append(gamma1_nc[i])
	g2.append(gamma2_nc[i])





plt.gcf().number
plt.plot(cov, np.array( dmuy1 ) - muy_Pb, "-o", label = "Pb constrained")
plt.plot(c, l1, "-o", label = "Pb no constrained")
plt.axhline(y=0, color='black', linestyle='--',label =  'Bulk Pb')
plt.axhline(y=diff, color='r', linestyle='-',label =  '2ML coverage')
plt.title("Pb chemical Potential vs Pb coverage")
plt.xlabel("Pb coverage (ML)")
plt.ylabel("$\Delta\mu_{Pb}$ [eV]")
plt.legend(loc = "best", ncol =1 )
plt.savefig("test1_6x6x1.png")
plt.show()


plt.gcf().number
plt.plot(cov, gamma1_c, "-o", label = "Pb constrained")
plt.plot(c, g1, "-o", label = "Pb no constrained")
plt.title("Pb Surface energy vs Pb coverage")
plt.xlabel("Pb coverage (ML)")
plt.ylabel("Surface Energy[J/$m^{2}$]")
plt.legend(loc = "best", ncol =1 )
plt.savefig("test2_6x6x1.png")
plt.show()

plt.gcf().number
plt.plot(cov, gamma2_c, "-o", label = "Pb constrained")
plt.plot(c, g2, "-o", label = "Pb no constrained")
plt.title("Pb Surface energy vs Pb coverage")
plt.xlabel("Pb coverage (ML)")
plt.ylabel("Surface Energy[J/$m^{2}$]")
plt.legend(loc = "best", ncol =1 )
plt.savefig("test3_6x6x1.png")
plt.show()






fig = plt.figure( figsize = ( 3.5, 3.5 ) )
ax = fig.add_subplot( 3, 1, 1 )
#ax.scatter( cov, np.array( dmuy ) - muy_Pb )
ax.plot( cov, np.array( dmuy1 ) - muy_Pb, "-o", label = "Pb constrained" )
ax.plot( c, l1, "-o", label = "Pb not constrained" )
ax.plot(c1, y1,  color='black', linestyle='--',label =  '2ML')
ax.plot(c1, y2,  color='blue', linestyle='-',label =  'Pb Bulk')
ax.legend(loc = 1)
ax.set_xlabel( '' )
ax.set_xticklabels( [] )
ax.set_xticks( np.arange( 1.0, 1.71, 0.1 ) )

ax.set_ylabel(  r'$\Delta \mu_{Pb}$ [eV]', labelpad = 5 )
ax.text( 1.02, 3.2, '$\Delta \mu_{Pb} = \mu_{Pb} - \mu_{Pb(Bulk)}$', va = 'top', ha = 'left' )
ax.hlines( 0, 1, 2, linewidth = 0.5)
ax.set_xlim(1.0, 1.7 )
ax.legend(fontsize=4, loc = 6)
ax = fig.add_subplot( 3, 1, 2 )

ax.plot( cov, np.array( gamma1_c ), '-o', label = "Pb constrained" )
ax.plot( c, g1, '-o', label = "Pb not constrained" )
ax.legend()


ax.set_xlabel( '' )
ax.set_xticklabels( [] )
ax.set_ylabel( r'Surface energy, $\gamma$ [J/m$^2$]', labelpad = 5 )


ax.set_xlim(1.0, 1.7 )
ax.set_xticks( np.arange( 1.0, 1.71, 0.1 ) )
ax.legend(fontsize=6, loc = 1)

ax = fig.add_subplot( 3, 1, 3 )

ax.plot( cov, np.array(gamma2_c ), '-o', label = "Pb constrained" )
ax.plot( c, g2, '-o', label ="Pb not constrained" )
ax.set_xlabel( 'Pb Coverage (ML)' )

ax.legend()
ax.set_xlim(1.0, 1.7 )
ax.legend(fontsize=6, loc = 2)
ax.set_xticks( np.arange( 1.0, 1.71, 0.1 ) )


plt.subplots_adjust(left=0.18, right=0.95, top=0.99, bottom=0.11, wspace=0.01, hspace= 0.01) 
plt.savefig( 'muy_6x6x1.png', dpi = 300 )
plt.show()
