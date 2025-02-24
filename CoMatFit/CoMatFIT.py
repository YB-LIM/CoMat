"""
Source code for CoMatFIT: Perform Regression on target Stress-Strain curve for concrete material

Author: Youngbin LIM
Contact: lyb0684@naver.com
"""

import numpy as np
from scipy import interpolate
from scipy.optimize import minimize
import matplotlib.pyplot as plt

##################################################
## User defined parameters for target data path ##
##################################################

Path_to_Compression_SS_data = "Compression_Ref.txt"
Path_to_Tension_SS_data = "Tension_Ref.txt"

# Elastic modulus of Concrete in GPa
E = 30.0
# Max Compressive Stress in MPa
S_cu = 26.5
# Strain at Max compressive stress
e_cu = 0.0013
# Max Tensile Stress in MPa
S_tu = 2.63

##################################################
##!!!!!!!!!! DO NOT TOUCH LINES BELOW !!!!!!!!!!##
##################################################

# Load Target SS curve

def guess_delimiter_and_load(filename):
    # Read the first line of the file
    with open(filename, 'r') as f:
        first_line = f.readline()
    
    # Guess the delimiter based on the first line
    tab_count = first_line.count('\t')
    comma_count = first_line.count(',')

    if tab_count > comma_count:
        delimiter = '\t'
    else:
        delimiter = ','

    # Use the determined delimiter with genfromtxt
    return np.genfromtxt(filename, delimiter=delimiter)

# TargetData for Compression part
CompTarget = guess_delimiter_and_load(Path_to_Compression_SS_data)

# TargetData for Tension part
TensTarget = guess_delimiter_and_load(Path_to_Tension_SS_data)

######################################
## Regression Starts from this line ##
######################################

#### Compression Part ####

# Interpolate Compression SS curve
e_c_Target, S_c_Target = CompTarget[:,0], CompTarget[:,1]
e_c_Interp = np.linspace(0, max(e_c_Target), num=100, endpoint=True)
Comp_Spline= interpolate.PchipInterpolator(e_c_Target, S_c_Target)

# Parabolic Hardening region is automatically determined by E, S_cu and e_cu
E = 1000*E
S_c0 = 2*S_cu - E*e_cu
e_0 = S_c0/E

# Alpha and e_63 is determined by optimizing the error between target data and prediction

def Error_Comp(Alpha,e_63):
    # Take strain larger than e_cu
    e_wb = e_c_Target[e_c_Target>e_cu]
    
    # Gerenate Stress array for Weibull softening curve
    S_c_wb = S_cu*(0.99*np.exp(-np.power((e_wb-e_cu)/e_63, Alpha)) + 0.01)
    
    # Calculate Error between prediction and Target data
    ErrComp = np.sum(np.power((Comp_Spline(e_wb) - S_c_wb), 2))
    
    return ErrComp

# Generate Random sample for Alpha and e_63
Alpha_min, Alpha_max = 0.5, 8.0
e_63_min, e_63_max = 0.0001, 0.01

Alpha_samples = Alpha_min + (Alpha_max - Alpha_min) * np.random.rand(1000)
e_63_samples = e_63_min + (e_63_max - e_63_min) * np.random.rand(1000)

# Evaluate the error for each sample
errors_comp = [Error_Comp(Alpha, e_63) for Alpha, e_63 in zip(Alpha_samples, e_63_samples)]

# Get the index of the minimum error
best_index = np.argmin(errors_comp)

# Retrieve the corresponding Alpha and e_63 values
best_Alpha = Alpha_samples[best_index]
best_e_63 = e_63_samples[best_index]

# Initial values for optimization
initial_point = [best_Alpha, best_e_63]

# Bounds for Alpha and e_63
bounds = [(Alpha_min, Alpha_max), (e_63_min, e_63_max)]

# Use the best initial values for optimization
result_comp = minimize(lambda params: Error_Comp(*params), initial_point, method='Nelder-Mead', bounds=bounds, 
                  options={'maxiter': 1000000, 'disp': True})

# Extract optimized values
Alpha, e_63 = result_comp.x

# Generae array for whole Compression Stress-Strain curve t
# Generate strain array
# Linear Elastic part
e_c_lin = np.linspace(0.0, e_0, num=5, endpoint=False)
# Parabolic Hardening part
e_para = np.linspace(e_0, e_cu, num=5, endpoint=False)
# Gerenate Stress array for Linear elastic part
S_c_lin = E*e_c_lin
# Gerenate Stress array for parabolic hardening part
S_c_para = -((S_cu-S_c0)/(e_cu-e_0)**2)*(e_para-e_0)*(e_para-e_0-2*(e_cu-e_0)) + S_c0

## Weibull softening part
# Generate strain array
e_wb = np.linspace(e_cu, max(e_c_Target), 20, endpoint=True)
# Gerenate Stress array
S_c_wb = S_cu*(0.99*np.exp(-np.power((e_wb-e_cu)/e_63, Alpha)) + 0.01)

# Combine to 1 array
e_c_total = np.concatenate((e_c_lin, e_para, e_wb), axis=None)
S_c_total = np.concatenate((S_c_lin, S_c_para, S_c_wb), axis=None)
# For txt file out
Compression_SS_plot=np.stack((e_c_total, S_c_total), axis=1)

#### Tension Part ####

e_tu = S_tu/E
# Interpolate Tension SS curve
e_t_Target, S_t_Target = TensTarget[:,0], TensTarget[:,1]
e_t_Interp = np.linspace(0, max(e_t_Target), num=100, endpoint=True)
Tens_Spline= interpolate.PchipInterpolator(e_t_Target, S_t_Target)

# Beta and e_end is determined by optimizing the error between target data and prediction

def Error_Tens(Beta,e_end):
    # Take strain larger than e_tu
    e_t_power = e_t_Target[e_t_Target>e_tu]
    
    # Gerenate Stress array for Power softening curve
    S_t_power = S_tu*(np.power(np.abs((e_end-e_t_power)/(e_end-e_tu)), Beta))
    
    # Calculate Error between prediction and Target data
    ErrTens = np.sum(np.power((Tens_Spline(e_t_power) - S_t_power), 2))
    
    return ErrTens

# Generate Random sample for Beta and e_end
Beta_min, Beta_max = 1.0, 5.0
e_end_min, e_end_max = 0.9*max(e_t_Target), 1.1*max(e_t_Target)

Beta_samples = Beta_min + (Beta_max - Beta_min) * np.random.rand(1000)
e_end_samples = e_end_min + (e_end_max - e_end_min) * np.random.rand(1000)

# Evaluate the error for each sample
errors_tens = [Error_Tens(Beta, e_end) for Beta, e_end in zip(Beta_samples, e_end_samples)]

# Get the index of the minimum error
best_index = np.argmin(errors_tens)

# Retrieve the corresponding Beta and e_end values
best_Beta = Beta_samples[best_index]
best_e_end = e_end_samples[best_index]

# Initial values for optimization
initial_point = [best_Beta, best_e_end]

# Bounds for Beta and e_end
bounds = [(Beta_min, Beta_max), (e_end_min, e_end_max)]

# Use the best initial values for optimization
result_tens = minimize(lambda params: Error_Tens(*params), initial_point, method='Nelder-Mead', bounds=bounds, 
                  options={'maxiter': 1000000, 'disp': True})

# Extract optimized values
Beta, e_end = result_tens.x

# Generae array for whole Tension Stress-Strain curve
# Generate strain array
# Linear Elastic part
e_t_lin = np.linspace(0.0, e_tu, num=5, endpoint=False)
# Gerenate Stress array for Linear elastic part
S_t_lin = E*e_t_lin
# Power Law Tension stiffning strain
e_t_power = np.linspace(e_tu, e_end, num=20, endpoint=True)
# Generate stress array
S_t_power = S_tu*(np.power((e_end-e_t_power)/(e_end-e_tu), Beta))
# Combine to 1 array
e_t_total = np.concatenate((e_t_lin, e_t_power), axis=None)
S_t_total = np.concatenate((S_t_lin, S_t_power), axis=None)
# For txt file out
Tensile_SS_plot=np.stack((e_t_total, S_t_total), axis=1)

#######################################
## Plot Graph and calibration result ##
#######################################

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

axs[0].plot(e_c_Target, S_c_Target, label='Compression-Target', marker='o', linestyle='', markersize=10, color='C0')
axs[0].plot(e_c_total, S_c_total, label='Compression-Fit', linestyle='-', color='C0')
axs[0].set_xlabel('Strain')
axs[0].set_ylabel('Stress (MPa)')
axs[0].ticklabel_format(axis='x', style='sci', scilimits=(0,0), useMathText=True)
axs[0].grid(True)
axs[0].legend(loc='upper left')
axs[0].set_ylim(top=1.4*max(S_c_Target))

axs[1].plot(e_t_Target, S_t_Target, label='Tension-Target', marker='o', linestyle='', markersize=10, color='C3')
axs[1].plot(e_t_total, S_t_total, label='Tension-Fit', linestyle='-', color='C3')
axs[1].set_xlabel('Strain')
axs[1].set_ylabel('Stress (MPa)')
axs[1].ticklabel_format(axis='x', style='sci', scilimits=(0,0), useMathText=True)
axs[1].grid(True)
axs[1].legend(loc='upper left')
axs[1].set_ylim(top=1.4*max(S_t_Target))

# Annotations for Compression side
compression_annotations = [
    ("$E$ (GPa):", E/1000),  # Dividing by 1000 to convert to GPa
    ("$\sigma_{cu}$ (MPa):", S_cu),
    ("$\epsilon_{cu}$:", "{:.1e}".format(e_cu)),
    ("$\epsilon_{0.63}$:", "{:.1e}".format(e_63)),
    ("$\\alpha$:", "{:.3f}".format(Alpha))
]

# Annotations for Tension side
tension_annotations = [
    ("$\sigma_{tu}$ (MPa):", S_tu),
    ("$\epsilon_{tu}$:", "{:.1e}".format(e_tu)),
    ("$\\beta$:", "{:.3f}".format(Beta)),
    ("$\epsilon_{end}$:", "{:.1e}".format(e_end))
]

# Add annotations to Compression plot on the right side
for i, (label, value) in enumerate(compression_annotations):
    axs[0].text(0.95, 0.9 - i*0.1, "{} {}".format(label, value), transform=axs[0].transAxes, ha='right')

# Add annotations to Tension plot on the right side
for i, (label, value) in enumerate(tension_annotations):
    axs[1].text(0.95, 0.9 - i*0.1, "{} {}".format(label, value), transform=axs[1].transAxes, ha='right')

plt.tight_layout()
plt.show()
