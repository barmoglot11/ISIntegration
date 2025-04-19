import socket
import asyncio
import os


async def animate_waiting(dots_event):
    dots = 0
    while not dots_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Сервер запущен. Ожидание подключения клиента" + '.' * dots,
              end='', flush=True)
        dots = (dots + 1) % 4
        await asyncio.sleep(0.5)


async def handle_client(client_socket, client_ip):
    try:
        client_row_msg = await asyncio.get_event_loop().sock_recv(client_socket, 1024)
        client_msg = client_row_msg.decode("UTF-8")

        print(f"\nСообщение от клиента {client_ip}: {client_msg}")
        await asyncio.get_event_loop().sock_sendall(client_socket,
                                                    b"received")
        print("Ответ отправлен клиенту.")
    except Exception as e:
        print(f"\nОшибка при работе с клиентом: {e}")
    finally:
        client_socket.close()


async def run_server():
    server_ip = "192.168.200.133"
    server_port = 2727

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)

    dots_event = asyncio.Event()
    animation_task = asyncio.create_task(animate_waiting(dots_event))

    try:
        client_socket, client_ip = await asyncio.get_event_loop().sock_accept(server_socket)
        dots_event.set()
        await animation_task

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nПодключен клиент с IP: {client_ip[0]}")

        await handle_client(client_socket, client_ip[0])
    except asyncio.CancelledError:
        print("\nСервер остановлен")
    except Exception as e:
        dots_event.set()
        await animation_task
        print(f"\nКритическая ошибка сервера: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nСервер завершил работу по команде пользователя")
