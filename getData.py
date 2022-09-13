import pickle
import scipy.io
import sys
import numpy as np
from time import sleep

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

def getData(dataQueue):

    if USE_SIMULATED_DATA == True:

        global MatlabSimDataSetIndex
        MatlabSimDataSetIndex = MatlabSimDataSetIndex + 1

        t = MatlabSimDataSet['t']
        Iabc = MatlabSimDataSet['Iabc'].transpose()
        Vabc = MatlabSimDataSet['Vabc'].transpose()

        t_resampled = t#[0:len(t):2]
        Iabc_resampled = Iabc#[0:len(t):2]
        Vabc_resampled = Vabc#[0:len(t):2]

        return t_resampled[MatlabSimDataSetIndex,0], Vabc_resampled[MatlabSimDataSetIndex], Iabc_resampled[MatlabSimDataSetIndex]


    if USE_IEC61850_DATA == True:

        data = dataQueue.get()
        print(f"Queue data get {data[0]}, {data[1]}, {data[2]}")

        return data[0], data[1], data[2]


def initDataBuffers(dataQueue):

    # Get the first set of data
    tabc, Vabc, Iabc = getData(dataQueue)

    # Fill array for first time
    sample_cnt = 0
    while(sample_cnt <= bufferArraysLength - 2): # with len of 200, only take 198
        t, V, I = getData(dataQueue)
        Iabc = np.vstack((Iabc, I))
        Vabc = np.vstack((Vabc, V))
        tabc = np.append(tabc, t)
        sample_cnt = sample_cnt + 1

    return tabc, Vabc, Iabc

def updateData(tabc, Vabc, Iabc, dataQueue):

    # Fill last place with new data
    t, V, I = getData(dataQueue) # Data is comming in at 4kHz or faster from C program (checked)

    if len(tabc) <= 900:
        # Append data to full array if not full yet
        Iabc = np.vstack((Iabc, I))
        Vabc = np.vstack((Vabc, V))
        tabc = np.append(tabc, t)
    else:
        Iabc = np.roll(Iabc, -1, axis=0)
        Vabc = np.roll(Vabc, -1, axis=0)
        tabc = np.roll(tabc, -1, axis=0)
        Iabc[-1] = I
        Vabc[-1] = V
        tabc[-1] = t

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

    global MatlabSimDataSetIndex
    global faultDetected

    while(not faultDetectedEvent.is_set()):
        sleep(0.001)

        MatlabSimDataSetIndex = MatlabSimDataSetIndex + 1

        t = MatlabSimDataSet['t']
        Iabc = MatlabSimDataSet['Iabc'].transpose()
        Vabc = MatlabSimDataSet['Vabc'].transpose()

        t_resampled = t#[0:len(t):2]
        Iabc_resampled = Iabc#[0:len(t):2]
        Vabc_resampled = Vabc#[0:len(t):2]

    # temp = sys.stdin.read(100)

    # splitPacket = temp.split()

    # t = splitPacket[0]

    # V1 = splitPacket[1]
    # V2 = splitPacket[2]
    # V3 = splitPacket[3]

    # I1 = splitPacket[4]
    # I2 = splitPacket[5]
    # I3 = splitPacket[6]

    # V = np.array(V1, V2, V3)
    # I = np.array(I1, I2, I3)

        # Buffer the data to transfer to main algorithm
        dataQueue.put(np.array((t_resampled[MatlabSimDataSetIndex,0], Vabc_resampled[MatlabSimDataSetIndex], Iabc_resampled[MatlabSimDataSetIndex])))
        print(f"Update getRealTimeData Thread {t_resampled[MatlabSimDataSetIndex,0]}, {Vabc_resampled[MatlabSimDataSetIndex]}, {Iabc_resampled[MatlabSimDataSetIndex]}")

    # return t, V, I