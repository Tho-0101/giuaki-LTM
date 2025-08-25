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