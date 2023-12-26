from ase.io import read, write
import numpy as np
loc = '/home/duy/PROJ_MetalOnSemiconductor/theodoros/Ge111_surface_relaxation/4x4_with_Pb/convergence/test_convergence_Ge_Pb/'
system_10x10 = read( loc + '10x10x1/OUTCAR' )
forces_ref = system_10x10.get_forces()
label = []
df = []
de = []
dfs = {}
for i in range( 1, 11 ):
    sys = str( i ) + 'x' + str( i ) + 'x1'
    system = read( loc + sys + '/OUTCAR' )
    forces = system.get_forces()
    dforces = forces-forces_ref
    #dforces = dforces.flatten()
    print ( sys, np.mean( dforces ), np.std( dforces ), (system.get_potential_energy() - system_10x10.get_potential_energy())/len( system ) )
    label.append( sys )
    df.append( np.std( dforces ) * 1000 )
    de.append( np.abs( system.get_potential_energy() - system_10x10.get_potential_energy())/len( system ) * 1000)
    dfs[ sys ] = dforces
import matplotlib.pyplot as plt
fig = plt.figure( figsize = ( 5, 2.5 ) )

ax1 = fig.add_subplot( 1, 2, 1 )
ax1.plot( range( 1, 11), df, 'o-', label = '$\sigma$$_{force}$' )
ax1.set_yscale( 'log' )
ax1.set_ylabel( 'meV/$\AA$' )
ax1.set_xticks( range( 1, 11 ) )
ax1.set_xticklabels( label, rotation = -45 )
ax1.set_xlabel( 'k-mesh' )
ax1.legend()

ax2 = fig.add_subplot( 1, 2, 2 )
ax2.plot( range( 1, 11), de, 'o-', label = '$\Delta$E' )
ax2.set_yscale( 'log' )
ax2.set_ylabel( 'meV/atom' )
ax2.set_xticks( range( 1, 11 ) )
ax2.set_xticklabels( label, rotation = -45 )
ax1.set_xlabel( 'k-mesh' )
ax2.legend()

plt.subplots_adjust(left=0.15, right=0.98, top=0.98, bottom=0.25, wspace=0.4, hspace= 0.02 )
plt.savefig( 'k-mesh.png', dpi = 300 )


import matplotlib.colors as colors
n, bins, patches = plt.hist( dfs[ '3x3x1' ].flatten(), bins = 100, normed = False, stacked = True )
fracs = n / float( n.max( ) )
norm = colors.Normalize( fracs.min(), fracs.max() )
for thisfrac, thispatch in zip( fracs, patches):
     color = plt.cm.viridis( norm( thisfrac ) )
     thispatch.set_facecolor( color )
