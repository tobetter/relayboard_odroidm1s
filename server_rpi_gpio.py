#!/usr/bin/env python3

import RPi.GPIO as GPIO
from flask import Flask, render_template, request

pins = {
    27 : { 'name' : 'CH0', 'state' : GPIO.LOW },
    17 : { 'name' : 'CH1', 'state' : GPIO.LOW },
    19 : { 'name' : 'CH2', 'state' : GPIO.LOW },
    13 : { 'name' : 'CH3', 'state' : GPIO.LOW }
    }

def refresh_relays():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

app = Flask(__name__)

@app.route("/")
def main():
    refresh_relays()

    templateData = {
            'pins' : pins
            }
    return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']

    if action == 'on':
        GPIO.output(changePin, GPIO.LOW)
        message = 'Turned ' + deviceName + 'on.'
    elif action == 'off':
        GPIO.output(changePin, GPIO.HIGH)
        message = 'Turned ' + deviceName + 'off.'

    refresh_relays()

    templateData = {
            'pins' : pins
            }

    return render_template('main.html', **templateData)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    app.run(host = '0.0.0.0', port = '8080', debug = True)
