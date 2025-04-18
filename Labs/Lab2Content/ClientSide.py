import socket
import time
import sys

server_ip = "192.168.200.133"  # IP-адрес менять для каждого сервера отдельно
server_port = 2727

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    dots = 0
    while True:
        try:
            client_socket.connect((server_ip, server_port))
            print(f"\nПодключение к серверу {server_ip}:{server_port} успешно!")
            break
        except ConnectionRefusedError:
            print("Сервер недоступен. Повторная попытка подключения", end='')
            dots = (dots + 1) % 4
            print('.' * dots, end='', flush=True)
            time.sleep(0.5)

    client_socket.send(bytes("ready", encoding="UTF-8"))
    server_row_response = client_socket.recv(1024)
    server_response = str(server_row_response.decode("UTF-8"))

    print(f"\nОтвет сервера: {server_response}")
