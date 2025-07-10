import socket
import threading


class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket  # Сокет подключённого клиента
        self.out = None  # Поток для отправки данных клиенту
        self.in_ = None  # Поток для чтения данных от клиента

    def run(self):
        try:
            # Создаём потоки ввода/вывода
            self.in_ = self.client_socket.makefile('r')  # Чтение строк
            self.out = self.client_socket.makefile('w')  # Запись строк

            # Регистрируем клиента на сервере
            from server import add_client
            add_client(self)

            # Главный цикл обработки сообщений
            while True:
                message = self.in_.readline()  # Читаем строку
                if not message:  # Если соединение разорвано
                    break
                # Рассылаем сообщение всем клиентам
                self.broadcast(message.strip())

        except (ConnectionError, OSError) as e:
            print("клиент отключился")
        finally:
            # Уборка при отключении
            try:
                self.client_socket.close()
            except OSError as e:
                print(f"Ошибка при закрытии сокета: {e}")
            # Удаляем клиента из списка
            from server import clients
            clients.remove(self)

    def send_message(self, message):
        # Отправка сообщения конкретному клиенту
        self.out.write(message + '\n')
        self.out.flush()  # Очищаем буфер

    @staticmethod
    def broadcast(message):
        print(message)  # Логируем на сервере
        from server import clients
        # Рассылаем всем подключённым клиентам
        for client in list(clients):  # Копируем для безопасной итерации
            try:
                client.send_message(message)
            except Exception as e:
                print("Не удалось отправить сообщение клиенту")