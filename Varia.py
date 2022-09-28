import numpy as np
from BasicParameters import *

def printFaultTimes(estFaultType, estFaultIncepTime, estFaultStableTime):
    print("Fault detected!")
    print("estFaultType:", end = ' ')
    print(estFaultType)
    print("estFaultIncepTime:", end = ' ')
    print(estFaultIncepTime)
    print("estFaultStableTime:", end = ' ')
    print(estFaultStableTime)


k_start = 0.01
k = np.arange(k_start,1-k_start+(1/number_of_k),(1/number_of_k))


def checkSettings():
    if USE_IEC61850_DATA == True:
        print("USE_IEC61850_DATA")
    if USE_SIMULATED_DATA == True:
        print("USE_SIMULATED_DATA")

if everyXSamples > 4:
    raise Exception("everyXSamples must be greater or equal to 4 to ensure 1000 Hz update rate")

