import socket
import json
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
TUBE_WIDTH = 50
TUBE_GAP = 150
BIRD_X = 50
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
font = pygame.font.SysFont('arial', 20)  # Sử dụng font Arial để hỗ trợ tiếng Việt
clock = pygame.time.Clock()

# Cấu hình socket
HEADER = 64
PORT = 6060
SERVER = "127.0.0.1"  # Sử dụng localhost
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Tải hình ảnh
try:
    
    background_image = pygame.image.load("anhnen.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Điều chỉnh kích thước ảnh nền
   
    bird_image = pygame.image.load("chim.png")
    bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
    
    pipe_image = pygame.image.load("cot.png")
    pipe_image = pygame.transform.scale(pipe_image, (TUBE_WIDTH, HEIGHT))  # Điều chỉnh kích thước cột
    # Tạo phiên bản lật ngược của ảnh cột cho cột phía trên
    pipe_image_top = pygame.transform.flip(pipe_image, False, True)
    
    ground_image = pygame.image.load("matdat.png")
    ground_image = pygame.transform.scale(ground_image, (WIDTH, 50))  # Điều chỉnh kích thước mặt đất
    
except pygame.error as e:
    print(f"[LỖI] Không tải được hình ảnh: {e}")
    pygame.quit()
    exit()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
        print(f"[KẾT NỐI] Đã kết nối tới {SERVER}:{PORT}")
    except ConnectionRefusedError as e:
        print(f"[LỖI] Không kết nối được tới {SERVER}:{PORT}: {e}")
        pygame.quit()
        exit()

        
if __name__ == "__main__":
    main()