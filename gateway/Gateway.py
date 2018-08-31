import socket, json, queue, select


class Gateway:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))
        print('connected!')
        self.write({'type': 'hello', 'team': 'peter'})

    def write(self, data):
        formatted_data = json.dumps(data)
        self.sock.send((formatted_data + '\n').encode('utf-8'))

    def read(self):
        data = self.sock.recv(64)  # recv is blocking
        if data:
            return json.loads(data)

    def listen(self):
        while True:
            sockets = [self.sock]
            ready_to_read, _, _ = select.select(sockets, [], [], 0.1)
            if ready_to_read:
                print("read:" + str(self.read()))


if __name__ == '__main__':
    gateway = Gateway()
    gateway.connect('localhost', 42069)
    gateway.listen()