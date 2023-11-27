#!/usr/bin/env python3

import time
import board
import digitalio
from flask import Flask, render_template, request

aliases = [ board.D13, board.D11, board.D35, board.D33 ]

relays = []

pins = {
    0 : { 'name' : 'CH0', 'state' : False },
    1 : { 'name' : 'CH1', 'state' : False },
    2 : { 'name' : 'CH2', 'state' : False },
    3 : { 'name' : 'CH3', 'state' : False }
    }

def refresh_relays():
    n = 0
    for relay in relays:
        pins[n]['state'] = relay.value
        n = n + 1

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
        relays[changePin].value = False
        message = 'Turned ' + deviceName + 'on.'
    elif action == 'off':
        relays[changePin].value = True
        message = 'Turned ' + deviceName + 'off.'

    refresh_relays()

    templateData = {
            'pins' : pins
            }

    return render_template('main.html', **templateData)

if __name__ == '__main__':
    for aliase in aliases:
        relay = digitalio.DigitalInOut(aliase)
        relay.direction = digitalio.Direction.OUTPUT
        relays.append(relay)

    app.run(host = '0.0.0.0', port = '8080', debug = True, use_reloader = False)
