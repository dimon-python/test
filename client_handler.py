import socket
import threading


class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.out = None
        self.in_ = None

    def signIn(self):
        self.in_ = self.client_socket.makefile('r')  # Чтение строк


    def run(self):
        try:

            self.in_ = self.client_socket.makefile('r')  # Чтение строк
            self.out = self.client_socket.makefile('w')  # Запись строк


            from server import add_client
            add_client(self)


            while True:
                message = self.in_.readline()
                if not message:
                    break

                self.broadcast(message.strip())

        except (ConnectionError, OSError) as e:
            print("клиент отключился")
        finally:

            try:
                self.client_socket.close()
            except OSError as e:
                print(f"Ошибка при закрытии сокета: {e}")

            from server import clients
            clients.remove(self)

    def send_message(self, message):

        self.out.write(message + '\n')
        self.out.flush()

    @staticmethod
    def broadcast(message):
        print(message)
        from server import clients
        for client in list(clients):
            try:
                client.send_message(message)
            except Exception as e:
                print("Не удалось отправить сообщение клиенту")