import RPi.GPIO as GPIO
import time
import sys

pin = int(sys.argv[1])

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin, GPIO.RISING)

while (True):
  if (GPIO.event_detected(pin)):
    print ('You pressed the button!')
  time.sleep(0.01)
 
