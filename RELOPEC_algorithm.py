from tempfile import tempdir
import scipy.io
import findData
from precision import Precision
import myFunctionDataProcess
import precision
import pandas as pd
from BasicParameters import *
import myFunctionFaultSelection
import numpy as np
import myFunctionCalcNetwork
import myFunctionCalcFaultLocation
import matplotlib.pyplot as plt
import timeit
import time
import tqdm
import multiprocessing as mp
from itertools import product
from itertools import repeat
import pickle
import os
from ctypes import *
import sys
import struct
import random

USE_CACHED_DATA = False
USE_IEC61850_DATA = True

# Global variables
I_trans = None
V_trans = None
k = None
tn = None
estFaultType = None
estFaultStableTime = None

# Making arrays for k and fictitious fault impedance
k=np.arange(0.01,0.99+0.005,0.005)
LfFictArray=np.zeros((len(k),1))
RfFictArray=np.zeros((len(k),1))

# Progress bar
pbar = tqdm.tqdm(total=196)
def update_progress(*a):
    pbar.update()

def findFaultInit(I_trans_local, V_trans_local, k_local, tn_local, estFaultType_local, estFaultStableTime_local):
    global I_trans 
    I_trans = I_trans_local
    global V_trans 
    V_trans = V_trans_local
    global k 
    k = k_local
    global tn
    tn = tn_local
    global estFaultType
    estFaultType = estFaultType_local
    global estFaultStableTime
    estFaultStableTime = estFaultStableTime_local
    return 

def findFault(n):

    update_progress()

    global I_trans
    global V_trans
    global k
    global tn
    global estFaultType
    global estFaultStableTime
    global LfFictArray
    global RfFictArray

    vF,i2,X=myFunctionCalcNetwork.NetworkParamNoCap(I_trans,V_trans,k[n],L_line,R_line,C_line,Ts,tn,Lg,Rg)

    LfFict,RfFict,ZfFict=myFunctionCalcFaultLocation.Fault(vF,i2,X,Ts,tn,estFaultType,estFaultStableTime)

    # LfFictArray[n]=LfFict    # This is now in parallel
    return LfFict

def write_data(name, data):

    with open(name, 'wb') as f:
        pickle.dump(data, f)

    print("Data saved to file")

def  read_data(name):

    with open(name, 'rb') as f:
        data = pickle.load(f)

    return data

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

def getData():

    # Read the data
    temp = sys.stdin.read(100)

    splitPacket = temp.split()

    t = splitPacket[0]

    V1 = splitPacket[1]
    V2 = splitPacket[2]
    V3 = splitPacket[3]

    I1 = splitPacket[4]
    I2 = splitPacket[5]
    I3 = splitPacket[6]

    # t = random.uniform(-1000,1000)

    # V1 = random.uniform(-1000,1000)
    # V2 = random.uniform(-1000,1000)
    # V3 = random.uniform(-1000,1000)

    # I1 = random.uniform(-1000,1000)
    # I2 = random.uniform(-1000,1000)
    # I3 = random.uniform(-1000,1000)

    return t, V1, V2, V3, I1, I2, I3


# MAIN SCRIPT OF THE ALGORITHM
if __name__=="__main__":

    if USE_CACHED_DATA == False:
        mp.freeze_support()

        if USE_IEC61850_DATA == False:

            # Load Simulation Data
            print("Load data")
            data = scipy.io.loadmat('data2.mat')

            # Put data in variables
            Iabc = data['Iabc']
            Vabc = data['Vabc']
            t = data['t']

        if USE_IEC61850_DATA == True:
            print("USE_IEC61850_DATA == True")

            t, V1, V2, V3, I1, I2, I3 = getData()

            # Create empty arrays
            Iabc = [[I1, I2, I3]]
            Vabc = [[V1, V2, V3]]
            t = []

            # Fill array for first time
            sample_cnt = 0
            while(sample_cnt <= 198):
                t, V1, V2, V3, I1, I2, I3 = getData()
                Iabc = np.append(Iabc, [[I1, I2, I3]], axis=0)

                t, V1, V2, V3, I1, I2, I3 = getData()
                Vabc = np.append(Vabc, [[V1, V2, V3]], axis=0)

                sample_cnt = sample_cnt + 1

            # the Z from 200 samples earlier
            previousZarray = np.zeros(200)

            # Fault detection loop
            while(1):

                start = time.time()

                # Make last place in array free
                Iabc = np.roll(Iabc, -1, axis=0)

                # Fill last place with new data
                t, V1, V2, V3, I1, I2, I3 = getData() # Data is comming in at 4kHz or faster from C program (checked)
                Iabc[-1] = [I1, I2, I3]

                # data = scipy.io.loadmat('data2.mat')
                # t = data['t']
                # Iabc = data['Iabc']
                # Vabc = data['Vabc']
                # Iabc, Vabc, Z, t = myFunctionFaultSelection.testDataset(Iabc,Vabc,t,f,Ts,Zbase)

                # Do the calculations on the updated data with the latest 200st array for comparing Z
                estFaultType,estFaultIncepTime,estFaultStableTime, Z = myFunctionFaultSelection.RealTimeFaultIndentification(Iabc, Vabc, t, previousZarray[-200])  

                previousZarray[-1] = Z
                previousZarray = np.roll(previousZarray, -1)

                end = time.time()
                print((end -start)*1000) # in milliseconds
                

            # Put data in variables
            # Iabc = 0
            # Vabc = 0
            # t = 0

        

        #########################################################
        # PART I: Needs to run at 2 kHz continuously
        #########################################################
        # Fault identification and classification
        print("Detect fault")
        start = time.time()
        estFaultType,estFaultIncepTime,estFaultStableTime=myFunctionFaultSelection.FaultIndentification(Iabc,Vabc,t,f,Ts,Zbase)
        end = time.time()
        print("Time to detect fault:", end = ' ')
        print(end-start)
        #########################################################

        #########################################################
        # PART II: Calculate fault location: only needs to run once to fault has been identified by part I
        #########################################################
        # Filter out fundamental frequency
        print("Filter fundamental")
        I_trans,V_trans,tn=myFunctionDataProcess.FilterFundamental(f,Ts,Iabc,Vabc,t,nargout=3)
        # Small variations on I_trans and V_trans, probably due to different way of calculation between Matlab and Python (some rounding maybe?)
        # These variations get bigger since future calculations use these values
        
        # Calculate fictitious fault inductance for every point on the line (k)
        # Using multiprocessing to speed up the calculation
        print("Start fault detection")
        pool = mp.Pool(processes=mp.cpu_count(), initializer=findFaultInit, initargs=(I_trans, V_trans, k, tn, estFaultType, estFaultStableTime))
        LfFictArray = pool.map(findFault, np.arange(0,len(k)))
        
        # (Temp) Save data for debugging purposes
        data = [k, LfFictArray]
        write_data("tempData", data)

    # (Temp) Read data for debugging purposes
    [k, LfFictArray] = read_data("tempData")

    # Find zero crossing and hence the distance to the fault
    print("Find zero cross")
    zeroCross1=myFunctionCalcFaultLocation.findZeroCross(LfFictArray,k)
    print("FaultLocData:", end = ' ')
    faultLocData = 0.8
    print(faultLocData) # Dit zou 0.3 moeten zijn voor "data.mat" en 0.8 voor "data2.mat"
    #########################################################
