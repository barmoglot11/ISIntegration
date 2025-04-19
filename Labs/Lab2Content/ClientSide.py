import socket
import asyncio
import os


async def animate_connecting(dots_event):
    dots = 0
    while not dots_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Ожидание подключения к серверу" + '.' * dots, end='', flush=True)
        dots = (dots + 1) % 4
        await asyncio.sleep(0.5)


async def connect_to_server():
    server_ip = "192.168.200.133"
    server_port = 2727

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)

    dots_event = asyncio.Event()
    animation_task = asyncio.create_task(animate_connecting(dots_event))

    try:
        try:
            await asyncio.wait_for(
                asyncio.get_event_loop().sock_connect(client_socket, (server_ip, server_port)),
                timeout=10.0
            )
        except asyncio.TimeoutError:
            raise TimeoutError("Не удалось подключиться к серверу в течение 10 секунд")

        dots_event.set()
        await animation_task
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nПодключение к серверу {server_ip}:{server_port} успешно!")

        client_socket.sendall(bytes("ready", encoding="UTF-8"))
        server_row_response = await asyncio.get_event_loop().sock_recv(client_socket, 1024)
        server_response = server_row_response.decode("UTF-8")

        print(f"\nОтвет сервера: {server_response}")

    except Exception as e:
        dots_event.set()
        await animation_task
        print(f"\nОшибка: {str(e)}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    asyncio.run(connect_to_server())
