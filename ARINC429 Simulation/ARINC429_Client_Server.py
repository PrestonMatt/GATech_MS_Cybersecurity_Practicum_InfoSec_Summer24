import socket
import time
from threading import Thread, Event

from arinc429_voltage_sim import binary_to_voltage as b2v

class arinc429_client_server:

    def __init__(self, client_mode, server_mode,
                 client_ip = "127.0.0.1",
                 client_port = 42900,
                 server_ip = "127.0.0.1",
                 server_port = 42900):

        if(client_mode == server_mode):
            raise ValueError("Server and Client must be opposite boolean values.")

        self.client_mode = client_mode
        self.server_mode = server_mode
        if(client_mode):
            self.client_ip = client_ip
            self.client_port = client_port
            self.server_ip = None
            self.server_port = None
        elif(server_mode):
            self.client_ip = None
            self.client_port = None
            self.server_ip = server_ip
            self.server_port = server_port

    def __str__(self):
        if(self.client_mode):
            print("Is a ARINC429 Receiver")
            print("Running on IP: %s with port %d." % (self.client_ip, self.client_port))
        else:
            print("Is a ARINC429 Transmitter")
            print("Running on IP: %s with port %d." % (self.server_ip, self.server_port))

    def client(self, voltage_reporter, bus_shutdown):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind((self.client_ip, self.client_port))

        try:
            while(not bus_shutdown.is_set()):
                try:
                    client_socket.settimeout(3)
                    data, addr = client_socket.recvfrom(1024)
                    print(f"Received data from {addr}")
                    if(data):
                        voltage = float(data.decode('utf-8').strip())
                        voltage_reporter(voltage)
                        print(f"Received voltage: {voltage}", flush=True)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            client_socket.close()
        finally:
            client_socket.close()

    # Server setup
    def server(self, ts, vs, bus_shutdown):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.server_ip, self.server_port))
        print("\nARINC429 TX on %s:%d" % (self.server_ip, self.server_port), flush=True)

        try:
            for i in range(len(vs)):
                if(bus_shutdown.is_set()):
                    break
                current_voltage = f"{vs[i]}\n".encode('utf-8')
                #print(f"Sending voltage: {vs[i]} at time: {ts[i]}", flush=True)
                server_socket.sendto(current_voltage, (self.server_ip, self.server_port))
                if i < len(ts) - 1:
                    sleep_time = (ts[i + 1] - ts[i]) / 1_000_000.0 # 0.000 000 5 is a half microsecond
                    #print(sleep_time)
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("Server commanded shutdown")
            server_socket.close()
        finally:
            server_socket.close()