import numpy as np
import matplotlib.pyplot as plt
from scipy.special import kv


###################################################################################################################
# code units (in cgs)
UNIT_L                         = 4.58351745817846e+24 
UNIT_M                         = 2.57725326366036e+44 
UNIT_T                         = 4.58351745817846e+17 
UNIT_V                         = 1.00000000000000e+07 
UNIT_D                         = 2.67645797518917e-30 
h0 = 0.6732117
# length units
Const_cm     = 1.0;
Const_pc     = 3.08567758149e18;
Const_kpc    = 1.0e3*Const_pc;
Const_Mpc_h0 = 1.0e6*Const_pc/h0;

# mass units
Const_g    = 1.0;
Const_kg   = 1.0e3*Const_g;
Const_Msun = 1.9885e33;
# density units
Const_Msun_pc3 = 6.77e-23
###################################################################################################################


###################################################################################################################
# density profile
def Halo_fitting_analytical_dens(r, rho_0, r_0, alpha, beta, gamma):
    x = r / r_0
    return rho_0 * ( x**(-gamma) ) * ( ( 1.0+(x**alpha) )**( (gamma-beta)/alpha ) )

def Soliton_rho_c_from_r_c(m22, r_c):
    return 1.945e7/( m22**2 * (r_c*UNIT_L/Const_kpc)**4 )*(Const_Msun/Const_kpc**3)/UNIT_D

def Soliton_fitting_analytical_dens(r, m22, r_c):
    rho_c = Soliton_rho_c_from_r_c(m22, r_c)
    x = r / r_c
    return rho_c*( 1.0+9.06e-2*(x**2) )**(-8)

def K_0(r, r_0, Amp):
    x = r / r_0
    return Amp*kv(0,x+0j).real

def Plummer_dens(r, b, M):
    return (3*M/(4*np.pi*(b**3)))*pow((1+(r/b)**2),-2.5)

def Logistic_dens(r, r0, k, Amp):
    return Amp/(1+np.exp(k*(r-r0)))
###################################################################################################################


###################################################################################################################
# parameters for the particles
exp_scale_r_0         =       4.000 *(Const_kpc)/UNIT_L                # in code_length
halo_fitting_alpha    =       4.800
halo_fitting_beta     =       3.098
halo_fitting_gamma    =       0.000
Density_Amp           =       2.0e-5 *(Const_Msun_pc3)/UNIT_D
Plummer_scale_length  =       2.8e-2 *(Const_kpc)/UNIT_L
Mass_parameter        =       1.0e3  *(Const_Msun)/UNIT_M
Logistic_decay_rate   =       5.0e3
###################################################################################################################


###################################################################################################################
# output the information
print( 'Information'                                                                 )
print( 'UNIT_L                 = {: >16.8e} cm'.format(      UNIT_L                ) )
print( 'UNIT_D                 = {: >16.8e} g/cm**3'.format( UNIT_D                ) )
print( 'exp_scale_r_0          = {: >16.8e} UNIT_L'.format(  exp_scale_r_0         ) )
print( 'Plummer_scale_length   = {: >16.8e} UNIT_L'.format(  Plummer_scale_length  ) )
print( 'Total_mass             = {: >16.8e} UNIT_M'.format(  Mass_parameter        ) )
print( 'Logistic_decay_rate    = {: >16.8e} '.format(    Logistic_decay_rate       ) )
###################################################################################################################


###################################################################################################################
# create the density profile
particle_densprof_radius  = np.logspace( -3.5, -0.5, num=1000 ) * Const_kpc/UNIT_L
#particle_densprof_density = K_0( particle_densprof_radius, exp_scale_r_0, Density_Amp)
particle_densprof_density = Plummer_dens(particle_densprof_radius, Plummer_scale_length, Mass_parameter)
# particle_densprof_density = Logistic_dens(particle_densprof_radius, exp_scale_r_0, Logistic_decay_rate, Density_Amp)
###################################################################################################################


###################################################################################################################
# save to file
np.savetxt( 'ParticleDensityProfile_Plummer_r_scale_28pc_M_1e3',
            np.column_stack( (particle_densprof_radius, particle_densprof_density) ),
            fmt='          %9.8e',
            header='                     r                  density' )
###################################################################################################################

###################################################################################################################
"""
fig = plt.figure()
ax  = fig.add_subplot(111)

# plot some important values for reference
ax.plot( [exp_scale_r_0                       , exp_scale_r_0                       ], [0.3*np.min(particle_densprof_density), 3.0*np.max(particle_densprof_density)],    '--',  color='grey',  label=r'$r_{\rm c}$'     )
ax.plot( [0.3*np.min(particle_densprof_radius), 3.0*np.max(particle_densprof_radius)], [exp_scale_r_0                        , exp_scale_r_0                        ],    '--',  color='grey',  label=r'$\rho_{\rm c}$'  )

# plot the density profile
ax.plot( particle_densprof_radius * UNIT_L/Const_kpc,                                     particle_densprof_density*1e9*UNIT_D/(Const_Msun_pc3) ,                                                          '-',   color='r',     label=r'$\rho(r)$' )

# annotate the information
ax.annotate( r'$r_{\rm c}$ = %.8e'%(exp_scale_r_0)+'\n',
            xy=(0.5,0.5), xycoords='axes fraction')

# setting for the figure
ax.set_xscale('log')
ax.set_yscale('log')
#ax.set_xlim(    0.5*np.min(particle_densprof_radius),  2.0*np.max(particle_densprof_radius)  )
#ax.set_ylim( 0.0001*np.max(particle_densprof_density), 3.0*np.max(particle_densprof_density) )
# ax.set_xlim(  0.05,         20)
# ax.set_ylim(   0.1,        1e5)
#ax.set_xlim( 0, 0.1*np.max(particle_densprof_radius)  )
#ax.set_ylim( 0, 1.5*np.max(particle_densprof_density) )

# set the labels
ax.set_xlabel( r'$r$'+' (kpc)'     )
ax.set_ylabel( r'$\rho$'+' Msun_kpc3' )
fig.suptitle(   'Density Profile of Particles'  )
ax.legend( loc='upper right' )

# save the figure
fig.subplots_adjust( top=0.93, bottom=0.1, left=0.1, right=0.97 )
fig.savefig( 'fig_ParticleDensityProfile_Plummer.png' )
plt.close()
"""