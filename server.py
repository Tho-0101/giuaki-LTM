import socket
import threading
import json
import os
import time
from random import randint


HEADER = 64
PORT = 6060
SERVER = "127.0.0.1" 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


WIDTH, HEIGHT = 400, 600
TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
GRAVITY = 0.8


bird_y = 400
bird_drop_velocity = 0
tube1_x = 600
tube2_x = 800
tube3_x = 1000
tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)
score = 0
tube1_pass = False
tube2_pass = False
tube3_pass = False
pausing = False

def update_game_state(space_pressed):
    global bird_y, bird_drop_velocity, tube1_x, tube2_x, tube3_x
    global tube1_height, tube2_height, tube3_height, score
    global tube1_pass, tube2_pass, tube3_pass, pausing, TUBE_VELOCITY

    if not pausing:
        # Update bird position
        bird_y += bird_drop_velocity
        bird_drop_velocity += GRAVITY

        # Move tubes
        tube1_x -= TUBE_VELOCITY
        tube2_x -= TUBE_VELOCITY
        tube3_x -= TUBE_VELOCITY

        # Reset tubes
        if tube1_x < -TUBE_WIDTH:
            tube1_x = 550
            tube1_height = randint(100, 400)
            tube1_pass = False
        if tube2_x < -TUBE_WIDTH:
            tube2_x = 550
            tube2_height = randint(100, 400)
            tube2_pass = False
        if tube3_x < -TUBE_WIDTH:
            tube3_x = 550
            tube3_height = randint(100, 400)
            tube3_pass = False

        # Update score
        if tube1_x + TUBE_WIDTH <= BIRD_X and not tube1_pass:
            score += 1
            tube1_pass = True
        if tube2_x + TUBE_WIDTH <= BIRD_X and not tube2_pass:
            score += 1
            tube2_pass = True
        if tube3_x + TUBE_WIDTH <= BIRD_X and not tube3_pass:
            score += 1
            tube3_pass = True