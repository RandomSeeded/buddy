'''
    Simple socket server using threads
'''

# TODO: get rid of all of the globals. This is TERRRRRRRRRRRRRIBLE practice.
 
import struct
import socket
import sys
from thread import *
import Tkinter as tk
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import math

batch_size = 64
nb_epoch = 20

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 1337 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
global drivingMode
drivingMode = None
global pressForward
pressForward = 0
global network
global ds

# Train the network til convergence
def train():
    global model
    testSize = int(math.floor(len(ds) / 10))
    np.random.shuffle(ds)
    data, out = zip(*ds)

    # todo: randomly select for training vs test
    trainingData = np.array(data[:-testSize])
    testData = np.array(data[-testSize:])
    trainingOut = np.array(out[:-testSize])
    testOut = np.array(out[-testSize:])
    print(trainingData)
    print(testData)
    print(trainingOut)
    print(testOut)

    # note: need to remove the hardcoded lengths in here. This is w*h
    trainingData.reshape(len(trainingData), 144 * 176)
    testData.reshape(len(testData), 144 * 176)

    # Prints the length
    print(trainingData.shape[0], 'train samples')
    print(testData.shape[0], 'test samples')

    model = Sequential()
    model.add(Dense(64, input_dim = 144*176, init='uniform', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    # model.add(Dense(output_dim = 64, input_dim = 144 * 176))
    # model.add(Activation('relu'))
    # model.add(Dense(output_dim = 1))

    print('Compiling...')
    model.compile(loss='binary_crossentropy', optimizer="rmsprop", class_mode="binary")
    print('Compile succesful')

    print('Fitting...')
    model.fit(trainingData, trainingOut, batch_size=batch_size, nb_epoch = nb_epoch, show_accuracy=True, verbose=2, validation_data = (testData, testOut))
    print('Model has been fitted.')

    score = model.evaluate(testData, testOut, show_accuracy=True, verbose=0)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    # Sanity Checking:
    # testData = np.zeros((1, 144 * 176))
    # predictedOutput = model.predict(testData)
    # print('Sanity check', predictedOutput.tolist())


    # print('Starting training')
    # trainer = BackpropTrainer(network, ds)
    # trainer.trainUntilConvergence()
    # print('Trained until convergence')

# Define action handlers for keypresses
def onKeyPress(event):
    global drivingMode
    if event.char == 'm':
        print('Placing Car in Manual Mode')
        drivingMode = 'Manual'
    elif event.char == 'g':
        print('Placing Car in Automatic Mode')
        train()
        drivingMode = 'Auto'
    elif event.char == 't':
        print('Placing Car in Training Mode')
        drivingMode = 'Training'
    elif event.char == 'w':
        global pressForward
        pressForward = 1
        # GPIO.output(led, GPIO.HIGH)
    elif event.char == 'q':
        root.destroy()
        print("Bye :)")

def onKeyRelease(event):
    if event.char == 'w':
        global pressForward
        pressForward = 0
        pass
    # GPIO.output(led, GPIO.LOW)

#Function for building our network. Can be put in separate thread if network is large
def buildNet(width, height):
    pass
    # print('Initializing neural network...', width * height)
    # network = buildNetwork(width * height, 64, 1)
    # ds = SupervisedDataSet(width*height, 1)
    # print('Neural network initialized')
    # return network, ds

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    print('Client Thread')
    firstFrame = True
    global network
    global ds
    ds = []
    #Sending message to connected client

    # HELPER FUNCTION: reads messages in that fit our protocol
    def recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        byte_width = conn.recv(4)
        byte_height = conn.recv(4)
        width = struct.unpack('>I', byte_width)[0]
        height = struct.unpack('>I', byte_height)[0]
        # print('Frame Received, sanity check width',width)
        # print("Frame Received")

        # This is a string in python2, but strings are just made up of bytes anyway. 
        #We can still reference the byte at a specific index, and call ord to convert it to a number
        pixelStr = recvall(conn, width*height) 
        pixels = bytearray(pixelStr)

        if drivingMode == 'Training': 
            ds.append((pixels, pressForward))
            # ds.addSample(pixels, (0,))
            pass

        elif drivingMode == 'Auto':
            frame = np.array(pixels)
            #trainingData.reshape(len(trainingData), 144 * 176)
            frame = frame.reshape(1, 144*176)

            predictedOutput = model.predict(frame)
            print('predictedOutput', predictedOutput, int(round(predictedOutput)))
            print('temp', predictedOutput[0])
            pass

        if firstFrame:
            # start_new_thread(buildNet, (width, height))
            # network, ds = buildNet(width, height)
            # print('ds', ds)
            firstFrame = False
            pass
        #     net = buildNetwork(2,64,1)
        #     print('reached2')
        # print('width',width,'height',height)
        # print('Next packet length', width*height)

     
    #came out of loop
    conn.close()

def listenForConnections():
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))

start_new_thread(listenForConnections, ())

root = tk.Tk()
# Can be hidden-ish by setting to 0x0
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Arial', 12))
text.insert('end', 'COMMANDS')
text.insert('end', "Press 'm' for manual mode (no training)\n")
text.insert('end', "Press 't' for training mode\n")
text.insert('end', "Press 'w' to drive the car forward\n")
text.insert('end', "Press 'g' to place the car in self-driving mode\n")
text.insert('end', "Press 'q' to quit")
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)
root.mainloop()

s.close()
