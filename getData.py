import pickle
import scipy.io
import sys
import numpy as np
from time import sleep
from numba import njit, jit, prange, objmode, typeof
import struct

from BasicParameters import *


if __name__ == '__main__':
    pass


def checkSettings():
    if USE_IEC61850_DATA == True:
        print("USE_IEC61850_DATA")
    if USE_SIMULATED_DATA == True:
        print("USE_SIMULATED_DATA")


# Global variables
faultDetected = False

# Dataset
MatlabSimDataSet = scipy.io.loadmat('data2.mat')
MatlabSimDataSetIndex = 0

cnt = 0

def getData(dataQueue):

    # if USE_SIMULATED_DATA == True:

    #     global MatlabSimDataSetIndex
    #     MatlabSimDataSetIndex = MatlabSimDataSetIndex + 1

    #     t = MatlabSimDataSet['t']
    #     Iabc = MatlabSimDataSet['Iabc'].transpose()
    #     Vabc = MatlabSimDataSet['Vabc'].transpose()

    #     t_resampled = t#[0:len(t):2]
    #     Iabc_resampled = Iabc#[0:len(t):2]
    #     Vabc_resampled = Vabc#[0:len(t):2]

    #     return t_resampled[MatlabSimDataSetIndex,0], Vabc_resampled[MatlabSimDataSetIndex], Iabc_resampled[MatlabSimDataSetIndex]


    # if USE_IEC61850_DATA == True:

    data = dataQueue.get()
    # print(f"Queue data get {data[0]}, {data[1]}, {data[2]}")
    
    global cnt
    cnt += 1
    if cnt >= 5000:
        cnt = 0
        print(f"Size reduced: {dataQueue.qsize()}")

    return data[0], data[1], data[2]


def initDataBuffers(dataQueue):

    # Get the first set of data
    tabc, Vabc, Iabc = getData(dataQueue)

    # Fill array for first time
    sample_cnt = 0
    while(sample_cnt <= bufferCalculationLength - 2): # with len of 200, only take 198
        t, V, I = getData(dataQueue)
        Iabc = np.vstack((Iabc, I))
        Vabc = np.vstack((Vabc, V))
        tabc = np.append(tabc, t)
        sample_cnt += 1

    return tabc, Vabc, Iabc

def rollFaster(x, newdata):

    x[0:-1] = x[1:]
    x[-1] = newdata
    return x

def updateData(tabc, Vabc, Iabc, dataQueue):

    for x in range(5):
        # Fill last place with new data
        t, V, I = getData(dataQueue) # Data is comming in at 4kHz or faster from C program (checked)

        if len(tabc) <= bufferLength:
            # Append data to full array if not full yet
            Iabc = np.vstack((Iabc, I))
            Vabc = np.vstack((Vabc, V))
            tabc = np.append(tabc, t)
        else:
            # Iabc = np.roll(Iabc, -1, axis=0)
            # Vabc = np.roll(Vabc, -1, axis=0)
            # tabc = np.roll(tabc, -1, axis=0)
            # Iabc[-1] = I
            # Vabc[-1] = V
            # tabc[-1] = t

            Iabc = rollFaster(Iabc, I)
            Vabc = rollFaster(Vabc, V)
            tabc = rollFaster(tabc, t)

    return tabc, Vabc, Iabc

def addData(tabc, Vabc, Iabc, amount, dataQueue):

    for x in range(amount):

        # Fill last place with new data
        t, V, I = getData(dataQueue) # Data is comming in at 4kHz or faster from C program (checked)

        Iabc = np.roll(Iabc, -1, axis=0)
        Vabc = np.roll(Vabc, -1, axis=0)
        tabc = np.roll(tabc, -1, axis=0)
        Iabc[-1] = I
        Vabc[-1] = V
        tabc[-1] = t

        x=x+1

    return tabc, Vabc, Iabc

def write_data(name, data):

    with open(name, 'wb') as f:
        pickle.dump(data, f)

    print("Data saved to file")

def  read_data(name):

    with open(name, 'rb') as f:
        data = pickle.load(f)

    return data


def getRealTimeData(faultDetectedEvent, dataQueue):

    print("Start getRealTimeData")

    cnt = 0

    global MatlabSimDataSetIndex
    global faultDetected

    while(not faultDetectedEvent.is_set()):

        if USE_SIMULATED_DATA == True:
            # sleep(0.00025)

            MatlabSimDataSetIndex = MatlabSimDataSetIndex + 1

            t = MatlabSimDataSet['t']
            Iabc = MatlabSimDataSet['Iabc'].transpose()
            Vabc = MatlabSimDataSet['Vabc'].transpose()

            t_resampled = t#[0:len(t):2]
            Iabc_resampled = Iabc#[0:len(t):2]
            Vabc_resampled = Vabc#[0:len(t):2]

            # Buffer the data to transfer to main algorithm
            dataQueue.put( np.array( (t_resampled[MatlabSimDataSetIndex,0], Vabc_resampled[MatlabSimDataSetIndex], Iabc_resampled[MatlabSimDataSetIndex]), dtype=object ) )
            # print(f"Update getRealTimeData Thread {t_resampled[MatlabSimDataSetIndex,0]}, {Vabc_resampled[MatlabSimDataSetIndex]}, {Iabc_resampled[MatlabSimDataSetIndex]}")

        if USE_IEC61850_DATA == True:

            # Read the data
            temp = sys.stdin.buffer.read(28)
            # print(temp)

            splitPacket = struct.unpack('fffffff', temp)

            # print(splitPacket)

            # splitPacket = temp.split()

            t = splitPacket[0]
            # print(f"t: ---{t}---\n")
            # temp = float(t)
            # print(temp)

            V1 = splitPacket[1]
            V2 = splitPacket[2]
            V3 = splitPacket[3]

            I1 = splitPacket[4]
            I2 = splitPacket[5]
            I3 = splitPacket[6]

            V = np.array( (V1, V2, V3) )
            I = np.array( (I1, I2, I3) )

            dataQueue.put( np.array( (t, V, I), dtype=object ) )

            # if( dataQueue.qsize() > 1000 ):

            # print(f"Size: {dataQueue.qsize()}")
            # print(f"Update getRealTimeData Thread {t}, {V}, {I}\n")
