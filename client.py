import socket
import json
import pygame
import math  # Để hỗ trợ animation rotate cho chim
from random import randint

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Các màu sắc cho giao diện
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
<<<<<<< Updated upstream
BLUE_SKY = (135, 206, 235)  # Màu trời xanh nhạt cho background fallback
=======
BLUE_SKY = (135, 206, 235)
SCORE_BOX_BEIGE = (222, 216, 149) # Màu của bảng điểm
BUTTON_ORANGE = (223, 113, 38)     # Màu cam cho chữ

>>>>>>> Stashed changes
TUBE_WIDTH = 50
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
<<<<<<< Updated upstream
font = pygame.font.SysFont('comicsansms', 28)  # Font vui vẻ hơn
small_font = pygame.font.SysFont('comicsansms', 20)
=======

# Sử dụng font chữ dễ nhìn hơn
font = pygame.font.SysFont('Consolas', 30, bold=True)
small_font = pygame.font.SysFont('Consolas', 22, bold=True)
score_font = pygame.font.SysFont('Consolas', 18)

>>>>>>> Stashed changes
clock = pygame.time.Clock()

# Cấu hình socket
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

<<<<<<< Updated upstream
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
=======
# Cấu hình file lưu điểm
SCORE_FILE = "high_scores.json"

# Tải hình ảnh
try:
    background_image = pygame.image.load("images/anhnen.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    bird_image = pygame.image.load("images/chim.png")
    bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
    pipe_image = pygame.image.load("images/cot.png")
    pipe_image = pygame.transform.scale(pipe_image, (TUBE_WIDTH, HEIGHT))
    pipe_image_top = pygame.transform.flip(pipe_image, False, True)
    ground_image = pygame.image.load("images/matdat.png")
    ground_image = pygame.transform.scale(ground_image, (WIDTH * 2, 50))
>>>>>>> Stashed changes
except pygame.error as e:
    print(f"[LỖI] Không tải được hình ảnh: {e}")
    pygame.quit()
    exit()

# Biến cho animation
<<<<<<< Updated upstream
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
=======
bird_rotation = 0
ground_x = 0
ground_speed = 3

# Các đám mây
clouds = []
for i in range(3):
    clouds.append({
        'x': randint(0, WIDTH),
        'y': randint(50, 200),
        'speed': randint(1, 2)
    })

def draw_cloud(x, y):
    pygame.draw.ellipse(screen, WHITE, (x, y, 80, 40))
    pygame.draw.ellipse(screen, WHITE, (x + 20, y - 10, 60, 30))
    pygame.draw.ellipse(screen, WHITE, (x + 40, y, 70, 35))

# Các hàm xử lý điểm cao (giữ nguyên)
def load_scores():
    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_scores(scores):
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
    except IOError as e:
        print(f"[LỖI] Không thể lưu điểm: {e}")

# Hàm vẽ bảng điểm và điểm cao nhất
def draw_score_box(score, best_score):
    """Vẽ bảng điểm trung tâm khi thua."""
    score_box_rect = pygame.Rect(WIDTH/2 - 80, HEIGHT/2 - 100, 160, 100)
    pygame.draw.rect(screen, SCORE_BOX_BEIGE, score_box_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, score_box_rect, 2, border_radius=10)

    # Hiển thị chữ "SCORE" và "BEST"
    score_label = score_font.render("SCORE", True, BUTTON_ORANGE)
    best_label = score_font.render("BEST", True, BUTTON_ORANGE)
    screen.blit(score_label, (score_box_rect.centerx - 60, score_box_rect.y + 15))
    screen.blit(best_label, (score_box_rect.centerx + 20, score_box_rect.y + 15))

    # Hiển thị điểm số
    score_text = font.render(str(score), True, BLACK)
    best_text = font.render(str(best_score), True, BLACK)
    screen.blit(score_text, (score_box_rect.centerx - 60, score_box_rect.y + 45))
    screen.blit(best_text, (score_box_rect.centerx + 20, score_box_rect.y + 45))

# Màn hình nhập tên (giữ nguyên)
def get_username_input():
    input_box = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 20, 250, 50)
    color = pygame.Color('dodgerblue2')
    username = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username: return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15: username += event.unicode
        screen.blit(background_image, (0, 0))
        title_surface = font.render("Enter Your Name", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 180))
        txt_surface = font.render(username, True, BLACK)
        input_box.w = max(250, txt_surface.get_width() + 20)
        input_box.x = WIDTH // 2 - input_box.w // 2
        pygame.draw.rect(screen, WHITE, input_box, border_radius=5)
        pygame.draw.rect(screen, color, input_box, 2, border_radius=5)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        instr_text = small_font.render("Press Enter to start", True, BLACK)
        screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        clock.tick(60)

# Màn hình menu (giữ nguyên)
def show_menu():
    button_rect = pygame.Rect(130, 280, 140, 60)
    hover = False
    bird_menu_y = HEIGHT // 2
    bird_menu_vel = -2
    menu_timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos): return
            if event.type == pygame.MOUSEMOTION:
                hover = button_rect.collidepoint(event.pos)
        menu_timer += 1
        bird_menu_y += bird_menu_vel
        if bird_menu_y < 100 or bird_menu_y > 300:
            bird_menu_vel = -bird_menu_vel
        screen.blit(background_image, (0, 0))
        for cloud in clouds:
            draw_cloud(cloud['x'], cloud['y'])
            cloud['x'] -= cloud['speed'] * 0.5
            if cloud['x'] < -100:
                cloud['x'] = WIDTH
                cloud['y'] = randint(50, 200)
        title_surface = font.render("Flappy Bird", True, BLACK)
        wave_offset = math.sin(menu_timer / 10) * 5
        screen.blit(title_surface, (80, 100 + wave_offset))
        btn_width, btn_height = (160, 70) if hover else (140, 60)
        btn_rect = pygame.Rect(WIDTH/2 - btn_width/2, 275, btn_width, btn_height)
        pygame.draw.rect(screen, BUTTON_ORANGE, btn_rect, border_radius=10)
        play_text = font.render("Play", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=btn_rect.center))
        pygame.display.flip()
        clock.tick(60)

# Game chính
def main():
    username = get_username_input()
    show_menu()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
        print(f"[KẾT NỐI] Đã kết nối tới {SERVER}:{PORT}")
        msg = json.dumps({"username": username}).encode(FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(msg)
    except ConnectionRefusedError:
        print(f"[LỖI] Không kết nối được tới server.")
        return

    best_score = 0
    running = True
    game_over_processed = False
    global bird_rotation, ground_x

    # ---- SỬA LỖI: Di chuyển game_state ra ngoài vòng lặp ----
    game_state = {} 

    while running:
        clock.tick(60)
        screen.fill(BLUE_SKY)
        screen.blit(background_image, (0, 0))
        
        space_pressed = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    # Hiệu ứng xoay chim chỉ hoạt động khi game đang chạy
                    if 'pausing' in game_state and not game_state['pausing']:
                         bird_rotation = -20

        try:
            input_data = {'space_pressed': space_pressed}
            msg = json.dumps(input_data).encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client_socket.send(send_length)
            client_socket.send(msg)
            
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if not msg_length: break
            msg_length = int(msg_length.strip())
            data = client_socket.recv(msg_length).decode(FORMAT)
            game_state = json.loads(data)
        except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError):
            print("[LỖI] Mất kết nối tới server.")
            break

        bird_y = game_state.get('bird_y', HEIGHT/2)
        score = game_state.get('score', 0)
        pausing = game_state.get('pausing', False)
        current_username = game_state.get('username', username) # Lấy tên từ server nếu có
        
        bird_rotation = min(bird_rotation + 1, 90)

        # Vẽ các thành phần game (ống, mây, đất, chim)
        for cloud in clouds:
            draw_cloud(cloud['x'], cloud['y'])
            if not pausing: cloud['x'] -= cloud['speed']
            if cloud['x'] < -100:
                cloud['x'] = WIDTH
                cloud['y'] = randint(50, 200)
        
        for i in range(1, 4):
            tube_x = game_state.get(f'tube{i}_x', WIDTH + i*200)
            tube_height = game_state.get(f'tube{i}_height', HEIGHT/2)
            screen.blit(pipe_image_top, (tube_x, tube_height - HEIGHT))
            screen.blit(pipe_image, (tube_x, tube_height + TUBE_GAP))
        
        if not pausing:
            ground_x -= ground_speed
            if ground_x <= -WIDTH: ground_x = 0
        screen.blit(ground_image, (ground_x, 550))
        screen.blit(ground_image, (ground_x + WIDTH, 550))
        
        rotated_bird = pygame.transform.rotate(bird_image, bird_rotation)
        bird_rect = rotated_bird.get_rect(center=(BIRD_X + BIRD_WIDTH / 2, bird_y + BIRD_HEIGHT / 2))
        screen.blit(rotated_bird, bird_rect.topleft)
        
        score_txt = font.render(f"{current_username} - Score: {score}", True, BLACK)
        screen.blit(score_txt, (5, 5))

        # Logic màn hình Game Over
        if pausing:
            if not game_over_processed:
                scores = load_scores()
                player_found = False
                for record in scores:
                    if record['username'] == current_username:
                        player_found = True
                        if score > record['score']:
                            record['score'] = score
                        break
                if not player_found:
                    scores.append({"username": current_username, "score": score})
                
                sorted_scores = sorted(scores, key=lambda s: s['score'], reverse=True)
                top_scores = sorted_scores[:5]
                save_scores(top_scores)
                
                best_score = top_scores[0]['score'] if top_scores else score
                game_over_processed = True

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            draw_score_box(score, best_score)
            
            press_space_txt = small_font.render("Press Space to Restart", True, WHITE)
            text_rect = press_space_txt.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
            screen.blit(press_space_txt, text_rect)
            
            if space_pressed:
                break 
        else:
            game_over_processed = False

        pygame.display.flip()

    print("[NGẮT KẾT NỐI] Đã đóng kết nối tới server.")
    client_socket.close()

if __name__ == "__main__":
    while True:
        main()
>>>>>>> Stashed changes
