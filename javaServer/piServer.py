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

s.listen(10)
print 'Socket now listening'

def clientthread(conn):
    print 'Driver connected'

def listenForConnections():
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))

start_new_thread(listenForConnections, ())
s.close()

# GPIO.output(led, GPIO.HIGH)


GPIO.cleanup()
