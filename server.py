import socket
import threading
import json
import time
from random import randint

# Socket configuration
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"  
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Game constants
WIDTH, HEIGHT = 400, 600
TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 180   # 👈 chỉnh khoảng trống giữa cột
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
GRAVITY = 0.8

# Giới hạn chiều cao cột
MIN_TUBE_HEIGHT = 120
MAX_TUBE_HEIGHT = 300

# Game state
bird_y = HEIGHT // 2
bird_drop_velocity = 0
tube1_x = 600
tube2_x = 800
tube3_x = 1000
tube1_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
tube2_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
tube3_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
score = 0
tube1_pass = False
tube2_pass = False
tube3_pass = False
pausing = False
game_started = False   # 👈 Thêm trạng thái chờ bắt đầu

def update_game_state(space_pressed):
    global bird_y, bird_drop_velocity, tube1_x, tube2_x, tube3_x
    global tube1_height, tube2_height, tube3_height, score
    global tube1_pass, tube2_pass, tube3_pass, pausing, TUBE_VELOCITY
    global game_started

    # Trạng thái chờ bắt đầu
    if not game_started:
        bird_y = HEIGHT // 2
        if space_pressed:
            game_started = True
            bird_drop_velocity = -10
        game_state = {
            'bird_y': bird_y,
            'tube1_x': tube1_x, 'tube1_height': tube1_height,
            'tube2_x': tube2_x, 'tube2_height': tube2_height,
            'tube3_x': tube3_x, 'tube3_height': tube3_height,
            'score': score,
            'pausing': False
        }
        return game_state

    # Game đang chạy
    if not pausing:
        bird_y += bird_drop_velocity
        bird_drop_velocity += GRAVITY

        tube1_x -= TUBE_VELOCITY
        tube2_x -= TUBE_VELOCITY
        tube3_x -= TUBE_VELOCITY

        if tube1_x < -TUBE_WIDTH:
            tube1_x = 550
            tube1_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            tube1_pass = False
        if tube2_x < -TUBE_WIDTH:
            tube2_x = 550
            tube2_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            tube2_pass = False
        if tube3_x < -TUBE_WIDTH:
            tube3_x = 550
            tube3_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            tube3_pass = False

        if tube1_x + TUBE_WIDTH <= BIRD_X and not tube1_pass:
            score += 1
            tube1_pass = True
        if tube2_x + TUBE_WIDTH <= BIRD_X and not tube2_pass:
            score += 1
            tube2_pass = True
        if tube3_x + TUBE_WIDTH <= BIRD_X and not tube3_pass:
            score += 1
            tube3_pass = True

        bird_rect = {'x': BIRD_X, 'y': bird_y, 'width': BIRD_WIDTH, 'height': BIRD_HEIGHT}
        tubes = [
            {'x': tube1_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube1_height},
            {'x': tube2_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube2_height},
            {'x': tube3_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube3_height},
            {'x': tube1_x, 'y': tube1_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube1_height - TUBE_GAP},
            {'x': tube2_x, 'y': tube2_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube2_height - TUBE_GAP},
            {'x': tube3_x, 'y': tube3_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube3_height - TUBE_GAP},
            {'x': 0, 'y': 550, 'width': 400, 'height': 50}  # đất
        ]
        for tube in tubes:
            if (bird_rect['x'] < tube['x'] + tube['width'] and
                bird_rect['x'] + bird_rect['width'] > tube['x'] and
                bird_rect['y'] < tube['y'] + tube['height'] and
                bird_rect['y'] + bird_rect['height'] > tube['y']):
                pausing = True
                TUBE_VELOCITY = 0
                bird_drop_velocity = 0

        # Check chạm trần trời
        if bird_y <= 0:
            pausing = True
            TUBE_VELOCITY = 0
            bird_drop_velocity = 0

    if space_pressed:
        if pausing:
            # Reset game
            bird_y = HEIGHT // 2
            bird_drop_velocity = 0
            tube1_x, tube2_x, tube3_x = 600, 800, 1000
            tube1_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            tube2_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            tube3_height = randint(MIN_TUBE_HEIGHT, MAX_TUBE_HEIGHT)
            score = 0
            pausing = False
            TUBE_VELOCITY = 3
            game_started = False  # 👈 quay lại trạng thái chờ
        else:
            bird_drop_velocity = -10

    game_state = {
        'bird_y': bird_y,
        'tube1_x': tube1_x, 'tube1_height': tube1_height,
        'tube2_x': tube2_x, 'tube2_height': tube2_height,
        'tube3_x': tube3_x, 'tube3_height': tube3_height,
        'score': score,
        'pausing': pausing
    }
    return game_state

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if not msg_length:
            conn.close()
            return
        msg_length = int(msg_length.strip())
        data = conn.recv(msg_length).decode(FORMAT)
        init_data = json.loads(data)
        username = init_data.get("username", "Người chơi")
        print(f"[LOGIN] {addr} => {username}")
    except Exception as e:
        print(f"[ERROR] Không nhận được username: {e}")
        conn.close()
        return

    while True:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length.strip())
            data = conn.recv(msg_length).decode(FORMAT)
            input_data = json.loads(data)
            space_pressed = input_data.get('space_pressed', False)

            game_state = update_game_state(space_pressed)
            game_state['username'] = username

            msg = json.dumps(game_state).encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(msg)

            time.sleep(1.0 / 60)
        except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR] {addr} encountered error: {e}")
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} ({username}) disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
    except OSError as e:
        print(f"[ERROR] Failed to bind to {ADDR}: {e}")
        return
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("[SHUTDOWN] Server is shutting down.")
            break
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
            break

    server.close()

if __name__ == "__main__":
    main()
