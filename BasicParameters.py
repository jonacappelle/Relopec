import numpy as np
import math
import cmath

# THIS IS THE CONFIGURATION FILE

USE_IEC61850_DATA = True
USE_SIMULATED_DATA = False


def concat(a, b):
    return np.block(a, b)

def concat(a):
    return np.block(a)

def exp(a):
    return cmath.exp(a)

#GENERAL PARAMETERS
Ts=0.0001
fs=1 / Ts

# TsSim=tOrig(200) - tOrig(199)

# GRID SPECIFIC PARAMETERS
f=50
wb=2*math.pi*f
Vn=15000
Sn=5000000.0
In=Sn / (math.sqrt(3)*Vn)

# PARAMETERS FOR OFFLINE PURPOSES OR FOR CALCULATIONS
faultIncepTime=0.6
Zbase=Vn ** 2 / Sn
a=1*exp(1j*2*math.pi/3); 
A=concat([[1,1,1],[1,a ** 2,a],[1,a,a ** 2]])

# TRANSMISSION LINE PARAMETERS
CableLen=10

#Positive- and zero-sequence parameters at 50Hz:
R1=0.11502
R0=0.39461
L1=0.00105 
L0=0.00342   
C1=1.13266e-08  
C0=5.00782e-09

#total line parameters
R_line=CableLen*R1    
L_line=CableLen*L1
C_line=CableLen*C1
Z_line=R_line + 1j*wb*L_line

# Parameters of the grid impedance 
# X1/R1=5 X0/R0=2  I-3ph SCL=10kA, I-1ph SCL=6kA
remoteR=concat([1.1784337797630415,0.16984155512168936])
remoteL=concat([0.8492077756084467,0.8492077756084467])

# print(remoteR)

Rg=remoteR[1]
Lg=remoteL[1] / wb


number_of_k = 200

k_start = 0.01
k = np.arange(k_start,1-k_start+(1/number_of_k),(1/number_of_k))
# k=np.arange(0.01,0.99+0.001,0.001)

Zarray_number_of_places = 200