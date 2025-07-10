import socket
import threading

PORT = 12345
clients = set()  # Множество для хранения всех подключённых клиентов


def add_client(client):
    clients.add(client)  # Добавление нового клиента


def main():
    print("Сервер запущен. Ожидание подключений...")

    # Создаём TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', PORT))  # Привязываем к порту 12345
        server_socket.listen()  # Начинаем слушать подключения

        while True:
            # Принимаем новое подключение
            client_socket, _ = server_socket.accept()
            # Создаём обработчик клиента в отдельном потоке
            client_handler = ClientHandler(client_socket)
            client_handler.start()


if __name__ == "__main__":
    main()