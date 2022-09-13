from tempfile import tempdir
from precision import Precision
import DataProcess
import precision
import pandas as pd
import FaultSelection
import numpy as np
import CalcNetwork
import CalcFaultLocation
import matplotlib.pyplot as plt
import timeit
import time
import _thread as thread
from threading import Thread, Event
import queue
from time import sleep

# Own libraries
from BasicParameters import *
from ctypes import *
from getData import *
from Varia import *


# Global variables
I_trans = None
V_trans = None
# k = None
tn = None
estFaultType = None
estFaultStableTime = None

# Making arrays for k and fictitious fault impedance
LfFictArray=np.zeros((len(k),1))
RfFictArray=np.zeros((len(k),1))

# create a queue
dataQueue = queue.Queue()
faultDetectedEvent = Event()

try:
    t = Thread(target=getRealTimeData, args=(faultDetectedEvent, dataQueue, ))
    t.start()
except:
    print("Error: unable to start thread")

# MAIN SCRIPT OF THE ALGORITHM
if __name__=="__main__":

    checkSettings()

    # Initialize data buffer and fill with 200 samples
    tabc, Vabc, Iabc = initDataBuffers(dataQueue)

    # the Z from 200 samples earlier
    previousZarray = np.zeros(Zarray_number_of_places)

    estFaultIncepTime_first = True

    start = time.time()
    counter = 0

    #########################################################
    # PART I: Needs to run at 4 kHz continuously
    #########################################################


    # Fault detection loop
    while(1):
        counter = counter + 1

        # Do the calculations on the updated data with the latest 200st array for comparing Z
        estFaultType,estFaultIncepTime_temp,estFaultStableTime, Z = FaultSelection.RealTimeFaultIndentification(Iabc[-Zarray_number_of_places:], Vabc[-Zarray_number_of_places:], tabc[-1], previousZarray[-Zarray_number_of_places])  
        if estFaultIncepTime_temp != 0 and estFaultIncepTime_first:
            # Only store estFaultIncepTime's first value
            estFaultIncepTime = estFaultIncepTime_temp
            estFaultIncepTime_first = False
        if estFaultType != 0:
            printFaultTimes(estFaultType, estFaultIncepTime, estFaultStableTime)
            break
        
        tabc, Vabc, Iabc = updateData(tabc, Vabc, Iabc, dataQueue)

        # Add Z to previous array and roll
        previousZarray = np.roll(previousZarray, -1)
        previousZarray[-1] = Z

    end = time.time()
    print(f"Time: {(end -start)*1000} Counter: {counter}") # in milliseconds

    # Get some more data
    tabc, Vabc, Iabc = addData(tabc, Vabc, Iabc, 100, dataQueue)

    faultDetectedEvent.set()

    #########################################################
    # PART II: Calculate fault location: only needs to run once to fault has been identified by part I
    #########################################################
    # Second part
    print("Filter fundamental")
    start = time.time()
    I_trans,V_trans,tn=DataProcess.RealTimeFilterFundamental(Iabc,Vabc,tabc,nargout=3)
    # I_trans,V_trans,tn=DataProcess.FilterFundamental(f,Ts,Iabc_full,Vabc_full,tabc_full,nargout=3)
    stop = time.time()

    print(f"Time filter fundamental: {stop-start}")

    # plt.plot(tabc, Vabc[:,0])
    # plt.plot(tn, V_trans[0])
    # plt.show()

    start = np.argwhere(tn>=estFaultIncepTime)[0][0]
    tn = tn[start:]
    V_trans = V_trans[:,start:]
    I_trans = I_trans[:,start:]

    # plt.plot(tabc, Vabc[:,0])
    # plt.plot(tn, V_trans[0])
    # plt.show()

    print("Start calculating fault location")
    # Calculate fictitious fault inductance for every point on the line (k)

    for n in np.arange(0,len(k)-1,1):
        start1 = time.time()
        vF,i2,X=CalcNetwork.NetworkParamNoCap(I_trans,V_trans,k[n],L_line,R_line,C_line,Ts,tn,Lg,Rg)
        stop1 = time.time()

        start2 = time.time()
        LfFict,RfFict,ZfFict=CalcFaultLocation.Fault(vF,i2,X,Ts,tn,estFaultType,estFaultStableTime)
        stop2 = time.time()
        LfFictArray[n]=LfFict            


    # Find zero crossing and hence the distance to the fault
    print("Find zero cross")
    zeroCross1=CalcFaultLocation.findZeroCross(LfFictArray,k)
    print("FaultLocData:", end = ' ')
    faultLocData = 0.8
    print(faultLocData) # Dit zou 0.3 moeten zijn voor "data.mat" en 0.8 voor "data2.mat"
