import numpy as np
import math
import cmath

# THIS IS THE CONFIGURATION FILE

USE_IEC61850_DATA = False
USE_SIMULATED_DATA = True

# GENERAL PARAMETERS
Ts=0.0001
fs=1 / Ts

# GRID SPECIFIC PARAMETERS
f=50
wb=2*math.pi*f
Vn=15000
Sn=5000000.0
In=Sn / (math.sqrt(3)*Vn)

# PARAMETERS FOR OFFLINE PURPOSES OR FOR CALCULATIONS
faultIncepTime=0.6
Zbase=Vn ** 2 / Sn
a=1*cmath.exp(1j*2*math.pi/3); 
A=np.block([[1,1,1],[1,a ** 2,a],[1,a,a ** 2]])

# TRANSMISSION LINE PARAMETERS
CableLen=10

# Positive- and zero-sequence parameters at 50Hz:
R1=0.11502
R0=0.39461
L1=0.00105 
L0=0.00342   
C1=1.13266e-08  
C0=5.00782e-09

# Total line parameters
R_line=CableLen*R1    
L_line=CableLen*L1
C_line=CableLen*C1
Z_line=R_line + 1j*wb*L_line

# Parameters of the grid impedance 
# X1/R1=5 X0/R0=2  I-3ph SCL=10kA, I-1ph SCL=6kA
remoteR=np.block([1.1784337797630415,0.16984155512168936])
remoteL=np.block([0.8492077756084467,0.8492077756084467])

Rg=remoteR[1]
Lg=remoteL[1] / wb

# How many steps of calculations need to be done
number_of_k = 200

# Length of the buffer on which the calculations are performed
bufferCalculationLength = 200
# Number of extra samples, to ensure all the necessary higher frequency components are captured
numberOfExtraSamplesAfterFault = 100
# Length of the global buffer, used for part II of the algorithm
# This must be bigger than bufferCalculationLength
bufferLength = 900

# Sampling frequency of the incomming data
sampleFreq = 10000 # in Hz

# Move window for real time fault identification over x samples instead of every sample
everyXSamples = 5
