"""
Source code for COMat: Input file generator for COncrete damaged plasticity Material model in Abaqus

Author: Youngbin LIM
Contact: lyb0684@naver.com
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot(Path, Plot_Graph, E, S_cu, e_cu, e_60, Alpha, S_tu, e_end, Beta, Tension_Recovery, Compression_Recovory, is_meter, Ref_Length):
    E = E * 1000.
    
    # Parabolic hardening part
    if e_cu <= S_cu/E or e_cu >= 2*S_cu/E:
        message = "Ultimate crushing strain should be in the range " + "[" + str(S_cu/E) + "~" + str(2*S_cu/E) + "]"
        raise ValueError(message)
    if e_end <= S_tu/E:
        message = "End strain should be larger than " + "[" + str(S_tu/E) 
        raise ValueError(message)
    
    ##########################################
    ## Compression part SS curve generation ##
    ##########################################

    ## Parabolic hardening
    # Slope constraint at the begining of parabolic hardening
    S_c0 = 2*S_cu - E*e_cu
    e_0 = S_c0/E

    # Generate strain array
    # Linear Elastic part
    e_c_lin = np.linspace(0.0, e_0, num=20, endpoint=False)
    # Parabolic Hardening part
    e_para = np.linspace(e_0, e_cu, num=20, endpoint=False)
    # Gerenate Stress array for Linear elastic part
    S_c_lin = E*e_c_lin
    # Gerenate Stress array for parabolic hardening part
    S_c_para = -((S_cu-S_c0)/(e_cu-e_0)**2)*(e_para-e_0)*(e_para-e_0-2*(e_cu-e_0)) + S_c0

    ## Weibull softening part
    # Calculate end strain
    e_wb_end = e_cu + e_60*np.power(-np.log(0.001/0.99), 1/Alpha)

    # Generate strain array
    e_wb = np.linspace(e_cu, e_wb_end, 50, endpoint=True)
    # Gerenate Stress array
    S_c_wb = S_cu*(0.99*np.exp(-np.power((e_wb-e_cu)/e_60, Alpha)) + 0.01)

    # Combine to 1 array
    e_c_total = np.concatenate((e_c_lin, e_para, e_wb), axis=None)
    S_c_total = np.concatenate((S_c_lin, S_c_para, S_c_wb), axis=None)
    # For txt file out
    Compression_SS_plot=np.stack((e_c_total, S_c_total), axis=1)

    ######################################
    ## Tensile part SS curve generation ##
    ######################################
    e_t0 = S_tu/E

    # Linear Elastic part
    e_t_lin = np.linspace(0.0, e_t0, num=20, endpoint=False)
    # Gerenate Stress array for Linear elastic part
    S_t_lin = E*e_t_lin
    # Power Law Tension stiffning strain
    e_t_power = np.linspace(e_t0, e_end, num=50, endpoint=True)
    # Generate stress array
    S_t_power = S_tu*(np.power(np.abs((e_end-e_t_power)/(e_end-e_t0)), Beta))
    # Combine to 1 array
    e_t_total = np.concatenate((e_t_lin, e_t_power), axis=None)
    S_t_total = np.concatenate((S_t_lin, S_t_power), axis=None)
    # For txt file out
    Tensile_SS_plot=np.stack((e_t_total, S_t_total), axis=1)

    if Plot_Graph==True:
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
        
        axs[0].plot(e_c_total, S_c_total, label='Compression', marker='o', markersize=6, linestyle='-', color='C0')
        axs[0].set_xlabel('Strain')
        axs[0].set_ylabel('Stress (MPa)')
        axs[0].ticklabel_format(axis='x', style='sci', scilimits=(0,0), useMathText=True)
        axs[0].grid(True)
        axs[0].legend()
        
        axs[1].plot(e_t_total, S_t_total, label='Tension', marker='o', markersize=6, linestyle='-', color='C3')
        axs[1].set_xlabel('Strain')
        axs[1].set_ylabel('Stress (MPa)')
        axs[1].ticklabel_format(axis='x', style='sci', scilimits=(0,0), useMathText=True)
        axs[1].grid(True)
        axs[1].legend()
        
        plt.tight_layout()
        plt.show()

def generate(Path, Plot_Graph, E, S_cu, e_cu, e_60, Alpha, S_tu, e_end, Beta, Tension_Recovery, Compression_Recovory, is_meter, Ref_Length):
    E = E * 1000.
    
    # Parabolic hardening part
    if e_cu <= S_cu/E or e_cu >= 2*S_cu/E:
        message = "Ultimate crushing strain should be in the range " + "[" + str(S_cu/E) + "~" + str(2*S_cu/E) + "]"
        raise ValueError(message)
    if e_end <= S_tu/E:
        message = "End strain should be larger than " + "[" + str(S_tu/E) 
        raise ValueError(message)

    ##########################################
    ## Compression part SS curve generation ##
    ##########################################

    ## Parabolic hardening
    # Slope constraint at the begining of parabolic hardening
    S_c0 = 2*S_cu - E*e_cu
    e_0 = S_c0/E

    # Generate strain array
    # Linear Elastic part
    e_c_lin = np.linspace(0.0, e_0, num=20, endpoint=False)
    # Parabolic Hardening part
    e_para = np.linspace(e_0, e_cu, num=20, endpoint=False)
    # Gerenate Stress array for Linear elastic part
    S_c_lin = E*e_c_lin
    # Gerenate Stress array for parabolic hardening part
    S_c_para = -((S_cu-S_c0)/(e_cu-e_0)**2)*(e_para-e_0)*(e_para-e_0-2*(e_cu-e_0)) + S_c0

    ## Weibull softening part
    # Calculate end strain
    e_wb_end = e_cu + e_60*np.power(-np.log(0.001/0.99), 1/Alpha)

    # Generate strain array
    e_wb = np.linspace(e_cu, e_wb_end, 50, endpoint=True)
    # Gerenate Stress array
    S_c_wb = S_cu*(0.99*np.exp(-np.power((e_wb-e_cu)/e_60, Alpha)) + 0.01)

    # Combine to 1 array
    e_c_total = np.concatenate((e_c_lin, e_para, e_wb), axis=None)
    S_c_total = np.concatenate((S_c_lin, S_c_para, S_c_wb), axis=None)
    # For txt file out
    Compression_SS_plot=np.stack((e_c_total, S_c_total), axis=1)

    ######################################
    ## Tensile part SS curve generation ##
    ######################################
    e_t0 = S_tu/E

    # Linear Elastic part
    e_t_lin = np.linspace(0.0, e_t0, num=20, endpoint=False)
    # Gerenate Stress array for Linear elastic part
    S_t_lin = E*e_t_lin
    # Power Law Tension stiffning strain
    e_t_power = np.linspace(e_t0, e_end, num=50, endpoint=True)
    # Generate stress array
    S_t_power = S_tu*(np.power(np.abs((e_end-e_t_power)/(e_end-e_t0)), Beta))
    # Combine to 1 array
    e_t_total = np.concatenate((e_t_lin, e_t_power), axis=None)
    S_t_total = np.concatenate((S_t_lin, S_t_power), axis=None)
    # For txt file out
    Tensile_SS_plot=np.stack((e_t_total, S_t_total), axis=1)

    ######################################
    ## Processing for Abaqus input file ##
    ######################################

    ### Compression part ###
    e_c_pla = np.concatenate((e_para, e_wb), axis=None)
    S_c_pla = np.concatenate((S_c_para, S_c_wb), axis=None)
    # Calculate inelastic strain
    e_c_inelastic = e_c_pla - S_c_pla/E

    # Calculate damage parameter
    # Get index for e_cu
    indices = np.where(e_c_pla <= e_cu)
    e_cu_index = indices[0][-1] if indices[0].size > 0 else None

    # Calculate damage parameter for compression part
    dc = 1.0 - S_c_pla/S_cu
    dc[:e_cu_index] = 0

    # Prepare array for Abaqus input
    Compression_SS = np.stack((S_c_pla, e_c_inelastic), axis=1)
    Compression_D = np.stack((dc, e_c_inelastic), axis=1)

    ### Tensile part ###
    e_t_pla = e_t_power
    S_t_pla = S_t_power
    # Create a boolean mask based on the condition
    mask = S_t_power > 0.01 * S_tu

    # Filter e_t_power and S_t_power using the mask
    e_t_pla = e_t_power[mask]
    S_t_pla = S_t_power[mask]
    
    e_t_cracking = e_t_pla - S_t_pla/E
    u_t_cracking = e_t_cracking*Ref_Length
    # Calculate damage parameter
    dt = 1.0 - S_t_pla/S_tu

    # Prepare array for Abaqus input
    Tensile_SS = np.stack((S_t_pla, u_t_cracking), axis=1)
    Tensile_D = np.stack((dt, u_t_cracking), axis=1)

    ### Write input file CDP marterial model part ###
    Density = 2.4E-9
    Poisson = 0.2

    if is_meter == True:
        Density = Density*1E12
        S_c_pla = S_c_pla*1E6
        S_t_pla = S_t_pla*1E6
        E = E*1E6

    FilePathName = Path + "\CDP_Mat.inp"
    file=open(FilePathName,'w')
    file.write("**************************\n")
    file.write("*** CDP Mat Definition ***\n")
    file.write("**************************\n")
    file.write("**E: "+str(E)+", S_cu: "+str(S_cu)+", e_cu: "+str(e_cu)+", e_63: "+str(e_60)+", Alpha: "+str(Alpha)+", S_tu: "+str(S_tu)+", e_end: "+str(e_end)+", Beta: "+str(Beta)+"**\n")
    file.write("*Material, name=CDP\n")
    file.write("*Density\n")
    file.write(str(Density)+"\n")
    file.write("*Elastic\n")
    file.write(str(E) + ", " + str(Poisson) + "\n")
    file.write("*Concrete Damaged Plasticity, REF LENGTH=" + str(Ref_Length)+"\n")
    file.write("40., 0.1, 1.16, 0.66667, 0.001\n")
    file.write("*Concrete Compression Hardening\n")
    np.savetxt(file,Compression_SS,fmt='%.6e',delimiter=",")
    file.write("*Concrete Tension Stiffening, type=DISPLACEMENT\n")
    np.savetxt(file,Tensile_SS,fmt='%.6e',delimiter=",")
    file.write("*Concrete Compression Damage, tension recovery=" + str(Tension_Recovery) + "\n")
    np.savetxt(file,Compression_D,fmt='%.6e',delimiter=",")
    file.write("*Concrete Tension Damage, type=DISPLACEMENT, compression recovery=" + str(Compression_Recovory) + "\n")
    np.savetxt(file,Tensile_D,fmt='%.6e',delimiter=",")
    file.write("*************************\n")
    file.write("*** End of Definition ***\n")
    file.write("*************************\n")
    file.close()

    ### Write data for SS curve plot in 3rd party ###
    FilePathName = Path + '\Compression_SS.txt'
    file=open(FilePathName,'w')
    file.write("Strain, Stress(MPa)\n")
    np.savetxt(file,Compression_SS_plot,fmt='%.6e',delimiter=",")
    file.close()
    FilePathName = Path + '\Tensile_SS.txt'
    file=open(FilePathName,'w')
    file.write("Strain, Stress(MPa)\n")
    np.savetxt(file,Tensile_SS_plot,fmt='%.6e',delimiter=",")
    file.close()
    
if __name__ == "__main__":
    # Define the parameters
    is_meter = False
    Path = os.path.dirname(os.path.abspath(__file__))
    Plot_Graph = False
    E = 30.0
    S_cu = 50.0
    e_cu = 0.003
    e_60 = 0.005
    Alpha = 2.0
    S_tu = 5.0
    e_end = 0.002
    Beta = 1.2
    Ref_Length = 1.0
    Tension_Recovery = 1.0
    Compression_Recovory = 0.0