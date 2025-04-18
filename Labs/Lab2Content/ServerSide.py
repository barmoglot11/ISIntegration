import socket
import time

server_ip = "192.168.200.133"  # IP-адрес менять для каждого сервера отдельно
server_port = 2727

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Сервер запущен на {server_ip}:{server_port}. Ожидание подключения клиента", end='')

    dots = 0
    while True:
        try:
            client_socket, client_ip = server_socket.accept()
            print("\nПодключен клиент с IP:", client_ip)
            break
        except Exception as e:
            print(f"\nОшибка: {e}")

        dots = (dots + 1) % 4
        print('.' * dots, end='', flush=True)
        time.sleep(0.5)

    with client_socket:
        client_row_msg = client_socket.recv(1024)
        client_msg = str(client_row_msg.decode("UTF-8"))

        print(f"\nСообщение от клиента: {client_msg}")
        client_socket.send(bytes("received", encoding="UTF-8"))
        print("Ответ отправлен клиенту.")
