import RPi.GPIO as GPIO
import Tkinter as tk
import socket

GPIO.setmode(GPIO.BCM)
pin = 14 
GPIO.setup(pin, GPIO.OUT)

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 1338 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

# GPIO.output(led, GPIO.HIGH)


GPIO.cleanup()
