import socket
import threading
import json
import os
import time
from random import randint

# Cấu hình socket
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"  # Sử dụng localhost một cách rõ ràng
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Hằng số trong game
WIDTH, HEIGHT = 400, 600
TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
GRAVITY = 0.8

# Trạng thái game
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
        # Cập nhật vị trí chim
        bird_y += bird_drop_velocity
        bird_drop_velocity += GRAVITY

        # Di chuyển ống
        tube1_x -= TUBE_VELOCITY
        tube2_x -= TUBE_VELOCITY
        tube3_x -= TUBE_VELOCITY

        # Reset ống khi đi hết màn hình
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

        # Cập nhật điểm
        if tube1_x + TUBE_WIDTH <= BIRD_X and not tube1_pass:
            score += 1
            tube1_pass = True
        if tube2_x + TUBE_WIDTH <= BIRD_X and not tube2_pass:
            score += 1
            tube2_pass = True
        if tube3_x + TUBE_WIDTH <= BIRD_X and not tube3_pass:
            score += 1
            tube3_pass = True

        # Kiểm tra va chạm
        bird_rect = {'x': BIRD_X, 'y': bird_y, 'width': BIRD_WIDTH, 'height': BIRD_HEIGHT}
        tubes = [
            {'x': tube1_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube1_height},
            {'x': tube2_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube2_height},
            {'x': tube3_x, 'y': 0, 'width': TUBE_WIDTH, 'height': tube3_height},
            {'x': tube1_x, 'y': tube1_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube1_height - TUBE_GAP},
            {'x': tube2_x, 'y': tube2_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube2_height - TUBE_GAP},
            {'x': tube3_x, 'y': tube3_height + TUBE_GAP, 'width': TUBE_WIDTH, 'height': HEIGHT - tube3_height - TUBE_GAP},
            {'x': 0, 'y': 550, 'width': 400, 'height': 50}  # Vùng cát phía dưới
        ]
        for tube in tubes:
            if (bird_rect['x'] < tube['x'] + tube['width'] and
                bird_rect['x'] + bird_rect['width'] > tube['x'] and
                bird_rect['y'] < tube['y'] + tube['height'] and
                bird_rect['y'] + bird_rect['height'] > tube['y']):
                pausing = True
                TUBE_VELOCITY = 0
                bird_drop_velocity = 0

    # Xử lý khi nhấn phím cách (space)
    if space_pressed:
        if pausing:
            # Reset game
            bird_y = 400
            bird_drop_velocity = 0
            tube1_x, tube2_x, tube3_x = 600, 800, 1000
            tube1_height = randint(100, 400)
            tube2_height = randint(100, 400)
            tube3_height = randint(100, 400)
            score = 0
            pausing = False
            TUBE_VELOCITY = 3
        else:
            bird_drop_velocity = -10

    # Chuẩn bị trạng thái game để gửi cho client
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
    print(f"[KẾT NỐI MỚI] {addr} đã kết nối.")
    
    while True:
        try:
            # Nhận độ dài thông điệp
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length.strip())  # Xóa khoảng trắng
            # Nhận dữ liệu thông điệp
            data = conn.recv(msg_length).decode(FORMAT)
            input_data = json.loads(data)
            space_pressed = input_data.get('space_pressed', False)

            # Cập nhật trạng thái game
            game_state = update_game_state(space_pressed)

            # Gửi trạng thái game về client
            msg = json.dumps(game_state).encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(msg)
            
            time.sleep(1.0 / 60)  # Duy trì tốc độ 60 FPS
        except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError, ValueError) as e:
            print(f"[LỖI] {addr} gặp lỗi: {e}")
            break

    conn.close()
    print(f"[NGẮT KẾT NỐI] {addr} đã ngắt kết nối.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
    except OSError as e:
        print(f"[LỖI] Không thể bind tới {ADDR}: {e}")
        return
    server.listen()
    print(f"[ĐANG NGHE] Server đang nghe tại {SERVER}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[SỐ KẾT NỐI HIỆN TẠI] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("[TẮT MÁY] Server đang tắt.")
            break
        except Exception as e:
            print(f"[LỖI] Lỗi server: {e}")
            break

    server.close()

if __name__ == "__main__":
    main()
