import socket
import json
import pygame
import math  # Để hỗ trợ animation rotate cho chim
from random import randint

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_SKY = (135, 206, 235)  # Màu trời xanh nhạt cho background fallback
TUBE_WIDTH = 50
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
font = pygame.font.SysFont('comicsansms', 28)  # Font vui vẻ hơn
small_font = pygame.font.SysFont('comicsansms', 20)
clock = pygame.time.Clock()

# Cấu hình socket
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Tải hình ảnh (giữ nguyên, nhưng thêm fallback nếu không load được)
try:
    background_image = pygame.image.load("anhnen.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  
    bird_image = pygame.image.load("chim.png")
    bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
    pipe_image = pygame.image.load("cot.png")
    pipe_image = pygame.transform.scale(pipe_image, (TUBE_WIDTH, HEIGHT))  
    pipe_image_top = pygame.transform.flip(pipe_image, False, True)
    ground_image = pygame.image.load("matdat.png")
    ground_image = pygame.transform.scale(ground_image, (WIDTH * 2, 50))  # Làm dài hơn để scroll
except pygame.error as e:
    print(f"[LỖI] Không tải được hình ảnh: {e}")
    pygame.quit()
    exit()

# Biến cho animation
bird_rotation = 0  # Góc xoay của chim
bird_flap_timer = 0  # Timer cho animation vỗ cánh (giả sử chỉ rotate)
ground_x = 0  # Vị trí scroll cho mặt đất
ground_speed = 3  # Tốc độ scroll mặt đất

# Thêm cloud cho background sáng tạo (lấy cảm hứng từ Mario)
clouds = []  # List các đám mây
for i in range(3):
    clouds.append({
        'x': randint(0, WIDTH),
        'y': randint(50, 200),
        'speed': randint(1, 2)
    })

def draw_cloud(x, y):
    # Vẽ đám mây đơn giản bằng ellipse
    pygame.draw.ellipse(screen, WHITE, (x, y, 80, 40))
    pygame.draw.ellipse(screen, WHITE, (x + 20, y - 10, 60, 30))
    pygame.draw.ellipse(screen, WHITE, (x + 40, y, 70, 35))

# ---------------- Màn hình menu ----------------
def show_menu():
    button_rect = pygame.Rect(130, 280, 140, 60)  # Nút lớn hơn
    hover = False
    bird_menu_y = HEIGHT // 2  # Chim bay trong menu
    bird_menu_vel = -2  # Tốc độ bay lên xuống
    menu_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # bấm Play thì vào game
            if event.type == pygame.MOUSEMOTION:
                hover = button_rect.collidepoint(event.pos)

        # Animation menu
        menu_timer += 1
        bird_menu_y += bird_menu_vel
        if bird_menu_y < 100 or bird_menu_y > 300:
            bird_menu_vel = -bird_menu_vel

        # Nền
        screen.blit(background_image, (0, 0))  # Sử dụng background game cho menu

        # Đám mây di chuyển trong menu
        for cloud in clouds:
            draw_cloud(cloud['x'], cloud['y'])
            cloud['x'] -= cloud['speed'] * 0.5  # Chậm hơn trong menu
            if cloud['x'] < -100:
                cloud['x'] = WIDTH
                cloud['y'] = randint(50, 200)

        # Tiêu đề với hiệu ứng wave
        title_surface = font.render("Flappy Bird", True, BLACK)
        wave_offset = math.sin(menu_timer / 10) * 5  # Wave effect
        screen.blit(title_surface, (80, 100 + wave_offset))

        # Nút Play với hover effect (phóng to khi hover)
        btn_width = 140 + 20 if hover else 140
        btn_height = 60 + 10 if hover else 60
        btn_rect = pygame.Rect(130 - 10 if hover else 130, 280 - 5 if hover else 280, btn_width, btn_height)
        pygame.draw.rect(screen, (0, 255, 0) if hover else GREEN, btn_rect, border_radius=10)
        play_text = font.render("Play", True, BLACK)
        screen.blit(play_text, (btn_rect.x + (btn_width - play_text.get_width()) // 2, btn_rect.y + (btn_height - play_text.get_height()) // 2))

        # Hướng dẫn
        instr_text = small_font.render("Press Space to flap!", True, BLACK)
        screen.blit(instr_text, (90, 380))

        # Chim bay trong menu
        screen.blit(bird_image, (BIRD_X, bird_menu_y))

        pygame.display.flip()
        clock.tick(60)

# ---------------- Game chính ----------------
def main():
    username = "player"  #  Tên mặc định
    show_menu()              # Màn hình menu trước khi vào game

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
        print(f"[KẾT NỐI] Đã kết nối tới {SERVER}:{PORT}")
        # Gửi tên đăng nhập ngay khi kết nối
        msg = json.dumps({"username": username}).encode(FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(msg)
    except ConnectionRefusedError as e:
        print(f"[LỖI] Không kết nối được tới {SERVER}:{PORT}: {e}")
        pygame.quit()
        exit()

    running = True
    global bird_rotation, bird_flap_timer, ground_x
    while running:
        clock.tick(60)
        
        # Background fallback nếu không có image
        screen.fill(BLUE_SKY)
        screen.blit(background_image, (0, 0))
        
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    bird_rotation = -20  # Xoay lên khi flap

        # Gửi dữ liệu đầu vào cho server
        input_data = {'space_pressed': space_pressed}
        msg = json.dumps(input_data).encode(FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        try:
            client_socket.send(send_length)
            client_socket.send(msg)
        except (ConnectionResetError, BrokenPipeError):
            break

        # Nhận trạng thái trò chơi từ server
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length.strip())
            data = client_socket.recv(msg_length).decode(FORMAT)
            game_state = json.loads(data)
        except:
            break

        # Lấy state
        bird_y = game_state['bird_y']
        tube1_x, tube1_height = game_state['tube1_x'], game_state['tube1_height']
        tube2_x, tube2_height = game_state['tube2_x'], game_state['tube2_height']
        tube3_x, tube3_height = game_state['tube3_x'], game_state['tube3_height']
        score = game_state['score']
        pausing = game_state['pausing']
        username = game_state['username']

        # Animation chim: rotate dần về xuống
        bird_rotation = min(bird_rotation + 1, 90)  # Giới hạn rotate

        # Vẽ đám mây di chuyển (sáng tạo, lấy từ Mario-like)
        for cloud in clouds:
            draw_cloud(cloud['x'], cloud['y'])
            if not pausing:
                cloud['x'] -= cloud['speed']
            if cloud['x'] < -100:
                cloud['x'] = WIDTH
                cloud['y'] = randint(50, 200)

        # Vẽ ống
        screen.blit(pipe_image_top, (tube1_x, tube1_height - HEIGHT))
        screen.blit(pipe_image, (tube1_x, tube1_height + TUBE_GAP))
        screen.blit(pipe_image_top, (tube2_x, tube2_height - HEIGHT))
        screen.blit(pipe_image, (tube2_x, tube2_height + TUBE_GAP))
        screen.blit(pipe_image_top, (tube3_x, tube3_height - HEIGHT))
        screen.blit(pipe_image, (tube3_x, tube3_height + TUBE_GAP))

        # Scroll mặt đất
        if not pausing:
            ground_x -= ground_speed
            if ground_x <= -WIDTH:
                ground_x = 0
        screen.blit(ground_image, (ground_x, 550))
        screen.blit(ground_image, (ground_x + WIDTH, 550))

        # Vẽ chim với rotate
        rotated_bird = pygame.transform.rotate(bird_image, bird_rotation)
        bird_rect = rotated_bird.get_rect(center=(BIRD_X + BIRD_WIDTH // 2, bird_y + BIRD_HEIGHT // 2))
        screen.blit(rotated_bird, bird_rect.topleft)

        # Điểm số
        score_txt = font.render(f"{username} - Score: {score}", True, BLACK)
        screen.blit(score_txt, (5, 5))

        if pausing:
            # Game over với overlay mờ
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)  # Độ mờ
            screen.blit(overlay, (0, 0))
            
            game_over_txt = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_txt, (100, 200))
            final_score_txt = small_font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score_txt, (130, 250))
            press_space_txt = small_font.render("Press Space to Restart", True, WHITE)
            screen.blit(press_space_txt, (80, 300))

        pygame.display.flip()

    client_socket.close()
    pygame.quit()

if __name__ == "__main__":
    main()