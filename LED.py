import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 14
GPIO.setup(led, GPIO.OUT)
while True:
	print 'LED on'
	GPIO.output(led, GPIO.HIGH)
	time.sleep(1)
	print 'LED off'
	GPIO.output(led, GPIO.LOW)
	time.sleep(1)
GPIO.cleanup()
