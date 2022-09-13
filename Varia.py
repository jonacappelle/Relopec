import os
import numpy as np


def printFaultTimes(estFaultType, estFaultIncepTime, estFaultStableTime):
    print("Fault detected!")
    print("estFaultType:", end = ' ')
    print(estFaultType)
    print("estFaultIncepTime:", end = ' ')
    print(estFaultIncepTime)
    print("estFaultStableTime:", end = ' ')
    print(estFaultStableTime)


def tests_matlab_python():
    #########################################
    # Matlab to python test
    array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12])

    print("---------")
    print(array[3:8])
    # First argument: - 1
    # Last argument: keep
    print(array[1:-1-2+1])
    # First argument: - 1
    # Last argument: + 1
    print(array[-1-3:-1-1+1])
    # Keep first argument with end
    # Last argument: + 1
    for i in np.arange(0,5):
        print(i)
    print("---------")
    #########################################
    os.system("pause")


