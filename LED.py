import RPi.GPIO as GPIO
import time
import Tkinter as tk

GPIO.setmode(GPIO.BCM)
led = 14
GPIO.setup(led, GPIO.OUT)

def onKeyPress(event):
    text.insert('end', 'You pressed %s\n' % (event.char, ))
    GPIO.output(led, GPIO.HIGH)
    # time.sleep(0.1)

def onKeyRelease(event):
    text.insert('end', 'You released %s\n' % (event.char, ))
    GPIO.output(led, GPIO.LOW)
    # time.sleep(0.1)


# while True:
# 	print 'LED on'
# 	GPIO.output(led, GPIO.HIGH)
# 	time.sleep(1)
# 	print 'LED off'
# 	GPIO.output(led, GPIO.LOW)
# 	time.sleep(1)


root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)
root.mainloop()

GPIO.cleanup()

