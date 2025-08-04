# client.py
import socket
import json
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font

HEADER = 64
FORMAT = 'utf-8'
# <<< QUAN TRỌNG: Hãy đảm bảo IP này khớp với IP của server của bạn
SERVER = '192.168.249.1' 
PORT = 6060
ADDR = (SERVER, PORT)

class Client:
    """Quản lý kết nối và giao tiếp với server."""
    def __init__(self, addr):
        self.addr = addr
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect(self.addr)
        except socket.error as e:
            self.connection = None
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến server tại {self.addr[0]}:{self.addr[1]}. Vui lòng đảm bảo server đang chạy và đúng địa chỉ IP.")
            exit(1)

    def request_from_server(self, data):
        """Gửi yêu cầu và nhận phản hồi từ server theo giao thức đã định."""
        if not self.connection:
            return {"status": "fail", "message": "Mất kết nối đến server."}
        try:
            # Gửi yêu cầu
            message = json.dumps(data, ensure_ascii=False).encode(FORMAT)
            header = f"{len(message):<{HEADER}}".encode(FORMAT)
            self.connection.send(header + message)

            # Nhận phản hồi
            response_header = self.connection.recv(HEADER)
            if not response_header:
                return {"status": "fail", "message": "Không nhận được phản hồi từ server."}
            
            response_length = int(response_header.decode(FORMAT))
            response_data = self.connection.recv(response_length).decode(FORMAT)
            
            return json.loads(response_data)
            
        except (ConnectionResetError, ConnectionAbortedError) as e:
            self.connection = None
            return {"status": "fail", "message": f"Mất kết nối với server.\nLỗi: {e}"}
        except Exception as e:
            return {"status": "fail", "message": f"Đã có lỗi xảy ra: {e}"}

# Khởi tạo client