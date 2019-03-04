#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import httplib, urllib
import os
import sys

# setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# define the GPIO port you will use for the motion detector
BUTTON = 19 
LED = 13
# number of seconds to delay between alarms
DELAY = 1

# set to pull-up (normally closed position for a PIR sensor dry contact)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)
# Pushover API setup
PUSH_TOKEN = "arysgrnmuv4ee9mowykbs6rst1iu4f" # API Token/Key
PUSH_USER = "uqtwg1akbrf3nm4djgubyfg4f6f93f" # Your User Key
PUSH_MSG = "HELLO " # Push Message you want sent

# This function sends the push message using Pushover.
# Pass in the message that you want sent
def sendPush( msg ):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": PUSH_TOKEN,
			"user": PUSH_USER,
			"message": msg,
		}), { "Content-type": "application/x-www-form-urlencoded" })

	conn.getresponse()
	return

try:
	# setup an indefinite loop that looks for the PIR sensor to be triggered
	while True:
		# motion is detected
		GPIO.wait_for_edge(BUTTON, GPIO.RISING)

		GPIO.output(LED, False)

		# print and push message
		print(PUSH_MSG)
		sendPush(PUSH_MSG)
                os.system("sh webcam.sh")
		# do you want a time delay in between alarms?
		time.sleep(DELAY)
		# after delay, turn LED off
		GPIO.output(LED, True)

except KeyboardInterrupt:
	# cleanup GPIOs on keyboard exit
	GPIO.output(LED, False)
	GPIO.cleanup()

# cleanup GPIOs when program exits
GPIO.cleanup()
