import requests
import time
import random
import click

from sense_hat import SenseHat

sense = SenseHat()

def get_direction():
    d_long = 0
    d_la = 0
    send_vel = False
    while True:
        for event in sense.stick.get_events():
            lastevent = event.action
            while lastevent != "released":
                if event.direction == "left":
                    send_vel = True
                    d_long = -1
                    d_la = 0
                elif event.direction == "right":
                    send_vel = True
                    d_long = 1
                    d_la = 0
                elif event.direction == "up": 
                    send_vel = True
                    d_long = 0
                    d_la = 1
                elif event.direction == "down":
                    send_vel = True
                    d_long = 0
                    d_la = -1
                elif event.direction == "middle":
                    d_long = 0
                    d_la = 0
                    click.echo('Invalid input :(')
                    send_vel = False
                print(event.direction)
                return d_long, d_la, send_vel


if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"
    while True:
        d_long, d_la, send_vel = get_direction()
        if send_vel:
            with requests.Session() as session:
                current_location = {'longitude': d_long,
                                    'latitude': d_la
                                    }
                resp = session.post(SERVER_URL, json=current_location)
