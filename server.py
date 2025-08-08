import socket
import threading
import json
import os
import time
from random import randint

# Cấu hình Socket
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"  # Chỉ định rõ sử dụng localhost
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Các hằng số của trò chơi
WIDTH, HEIGHT = 400, 600
TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
GRAVITY = 0.8

# Trạng thái trò chơi
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


if __name__ == "__main__":
    main()