import socket, json, random, select

PACKET_SIZE = 1024


class Gateway:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))
        print('connected!')
        self.write({'type': 'hello', 'team': 'MOBRIEN'})
        data = self.sock.recv(PACKET_SIZE)
        print(data)
        print(type(data))
        print(json.loads(data))

    def write(self, data):
        formatted_data = json.dumps(data)
        self.sock.send((formatted_data + '\n').encode('utf-8'))

    def read(self):
        data = self.sock.recv(PACKET_SIZE)  # recv is blocking
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
    # gateway.listen()
    order_id = 0
    trade = {'type': 'add',
             'order_id': order_id,
             'symbol': 'AAPL',
             'dir': 'buy',
             'price': "0",
             'size': "0"}
    while True:
        print("client read: " + str(gateway.read()))
        if random.random() < 0.5:
            trade['price'] = str(random.random())
            trade['size'] = str(random.randint(1, 10))
            print("client sending: " + str(trade))
            gateway.write(trade)