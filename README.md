# buddy

Proof of concept code for a self-driving car.

Includes:
- Java Android app for grabbing camera preview frames
- Python TCP server integrated with Keras/Theano neural network for classifying images
- Raspberry Pi code for translating output from neural network into physical movement

## How it works:

The Android application grabs camera preview frames from the Android phone camera at the smallest available resolution. These images are then grayscaled, and streamed to a Python TCP server. This Python TCP server, also responsible for driving the car, additionally deals with both user interaction (manually driving/training the car) and interfacing with the Keras/Theano neural network. 

The car can be placed into multiple modes, the most important of which are training mode and self-driving mode. When in training mode, the car will save tuples of the video frame at the time and the corresponding user input, aka for the given road conditions ahead, how the user is driving the car. When placed into self-driving mode, the neural network will be fit based on the data from the training mode. After the fitting is complete, video frames received are then fed through the neural network, which classifies them according to the network's model of how the user would drive.

Finally, these classifications are fed as driving instructions to the Raspberry Pi, hardwired to the remote of of the car, which causes movement through high/low pulls to the Pi's GPIO.

