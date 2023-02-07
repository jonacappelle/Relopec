import numpy as np
import math

# THIS IS THE CONFIGURATION FILE
USE_IEC61850_DATA = True
USE_SIMULATED_DATA = False
USE_FIXED_STABLE_TIME = True

# GENERAL PARAMETERS
# Sampling frequency of the incoming data
sampleFreq = 4000 # in Hz
Ts=1/sampleFreq # in seconds
CT_ratio = 10000
VT_ratio = 1000
ID_ratio = 10000

fixed_stable_time = 120/sampleFreq # 1.5 periods

# GRID SPECIFIC PARAMETERS
gridFreq=50 # in Hz
wb=2*math.pi*gridFreq # in rad/s
Vn=15000 # in Volts
Sn=5000000.0 # in VA
In=Sn / (math.sqrt(3)*Vn)

# PARAMETERS FOR OFFLINE PURPOSES OR FOR CALCULATIONS
Zbase=Vn ** 2 / Sn # in Ohm

# TRANSMISSION LINE PARAMETERS
CableLen=10 # in kilometers

# Positive- and zero-sequence parameters at 50Hz:
R1=0.11502 # in Ohm/km
R0=0.39461 # in Ohm/km
L1=0.00105 # in H/km
L0=0.00342 # in H/km
C1=1.13266e-08 # in F/km
C0=5.00782e-09 # in F/km

# Total line parameters
R_line=CableLen*R1 # in Ohm
L_line=CableLen*L1 # in Henry
C_line=CableLen*C1 # in Farad, but not used
Z_line=R_line + 1j*wb*L_line # not used

# Parameters of the grid impedance 
# X1/R1=5 X0/R0=2  I-3ph SCL=10kA, I-1ph SCL=6kA
remoteR=np.block([1.1784337797630415,0.16984155512168936])
remoteL=np.block([0.8492077756084467,0.8492077756084467])

Rg=remoteR[1] # in Ohm
Lg=remoteL[1] / wb # in Henry

# How many steps of calculations need to be done
number_of_k = 200

# Length of the buffer on which the calculations are performed
bufferCalculationLength = 200 # in number of samples
# Number of extra samples, to ensure all the necessary higher frequency components are captured
numberOfExtraSamplesAfterFault = 100 # in numer of samples
# Length of the global buffer, used for part II of the algorithm
# This must be bigger than bufferCalculationLength
bufferLength = 900 # in number of samples

# Move window for real time fault identification over x samples instead of every sample
everyXSamples = 4 # minimal value 4 -> 1000 Hz
