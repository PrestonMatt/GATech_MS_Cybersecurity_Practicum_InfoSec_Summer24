import socket
import time
from threading import Thread

from arinc429_voltage_sim import binary_to_voltage as b2v

class arinc429_client_server:

    def __init__(self, client_or_server,
                 client_ip = "127.0.0.1",
                 client_port = 42900,
                 server_ip = "127.0.0.1",
                 server_port = 42900):
        self.client_or_server = client_or_server
        self.client_ip = client_ip
        self.client_port = client_port
        self.server_ip = server_ip
        self.server_port = server_port

    def __str__(self):
        if(self.client_or_server):
            print("Is a ARINC429 Receiver")
            print("Running on IP: %s with port %d." % (self.client_ip, self.client_port))
        else:
            print("Is a ARINC429 Transmitter")
            print("Running on IP: %s with port %d." % (self.server_ip, self.server_port))

    def client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 42900))

        try:
            while True:
                data = client_socket.recv(1024)
                if data:
                    print(f"Received voltage: {data.decode('utf-8').strip()}")
        except KeyboardInterrupt:
            client_socket.close()

    def handle_client(client_socket):
        ts, vs = arinc429_voltage_sim.create_random_word(True)

    try:
        while (True):
            try:

                current_voltage = f"{vs[current_index]}\n".encode('utf-8')
                client_socket.send(current_voltage)
                time.sleep(0.0005)
            except socket.error:
                print("BUS CONNECTION ERROR")
                client_socket.close()
                break
    except KeyboardInterrupt:
        print("User bus shutdown")
        client_socket.close()


# Server setup
def server():
    global current_index
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 42900))
    server_socket.listen(5)
    print("Server listening on 127.0.0.1:42900")

    current_index = 0
    while True:
        arinc429_voltage_gen = b2v(True)
        ts, vs = b2v.create_random_word(arinc429_voltage_gen,True)
        print("Recieving data")
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

        # Update voltage index based on timestamps
        for i in range(len(ts)):
            current_index = i
            time.sleep(ts[i] / 1000000.0)  # Convert microseconds to seconds
