import threading
import time
import pytest
import numpy as np
from threading import Thread, Event
from queue import Queue


from arinc429_voltage_sim import binary_to_voltage
from ARINC429_Client_Server import arinc429_client_server
from FMC_LRU_Simulator import flight_management_computer
from EEC_LRU_Simulator import Full_Authority_Engine_Control, BusError

def main():
    test1()
    test2()

"""
    Test instantiation of ARINC 429 bus on good values
"""
def test1():
    Flight_Management_Computer_1 = flight_management_computer(scheduled_mode=False,speed="High")
    Flight_Management_Computer_2 = flight_management_computer(scheduled_mode=False,speed="Low")
    Flight_Management_Computer_3 = flight_management_computer(scheduled_mode=True,speed="High")
    Flight_Management_Computer_4 = flight_management_computer(scheduled_mode=True,speed="Low")

"""
    Test instantiation of ARINC 429 bus on bas values
"""
def test2():
    with pytest.raises(Exception) as exception:
        Flight_Management_Computer_ = flight_management_computer(scheduled_mode=True,speed="Random")
    with pytest.raises(Exception) as exception:
        Flight_Management_Computer_ = flight_management_computer(scheduled_mode="what",speed="Speed")

"""
    Test ARINC 429 bus to see that it sends correct packets
"""
def test3():
    """
    FMC_LRU = flight_management_computer(scheduled_mode=False,speed="High")
    # Start server for bus channel A
    random_word = FMC_LRU.word_maker.create_random_word(FMC_LRU.word_maker.get_bus_speed())
    FMC_LRU.send_voltage("A",
                         random_word[0],
                         random_word[1])
    print("Sender for Channel A open.")

    FMC_LRU.send_voltage("B",
                         random_word[0],
                         random_word[1])
    print("Sender for Channel B open.")

    voltages = []
    this_word = binary_to_voltage(False)
    def voltage_reporter(voltage):
        voltages.append(voltage)
        print(f"Received voltage: {voltage}")
        ts = np.arange(0,len(voltages),0.5)
        this_word.graph_words((ts,voltages))

    # Start 2 listeners
    # Start client listener for Channel A
    client_channel_A = arinc429_client_server(client_mode = True, server_mode=False,
                                              client_ip = "127.0.0.1",
                                              client_port = 0x429A)
    client_channel_A.client(voltage_reporter)
    print("Listener for Channel A open.")
    # Start client listener for Channel B
    client_channel_B = arinc429_client_server(client_mode = True, server_mode=False,
                                              client_ip = "127.0.0.2",
                                              client_port = 0x429B)
    client_channel_B.client(voltage_reporter)
    print("Listener for Channel B open.")
    """
    pass


"""
    Test of ARINC429_Client_Server utility to see that it can send the correct packets.
"""
def test4():
    bus_shutdown = Event()
    generic_ARINC429_TX = arinc429_client_server(client_mode = False, server_mode = True,
                                                 server_ip = "127.0.0.1",
                                                 server_port = 0x429)
    generic_ARINC429_RX = arinc429_client_server(client_mode = True, server_mode = False,
                                                 client_ip = "127.0.0.1",
                                                 client_port = 0x429)
    hl_speed_is_high = True
    word_voltages = binary_to_voltage(hl_speed_is_high).create_random_word(hl_speed_is_high)

    voltage_RX = []

    def voltage_reporter(voltage):
        print(f"Reported voltage: {voltage}")
        voltage_RX.append(voltage)

    server = Thread(
        target=generic_ARINC429_TX.server,
        args=(word_voltages[0],word_voltages[1],bus_shutdown,)
    )
    client = Thread(
        target=generic_ARINC429_RX.client,
        args=(voltage_reporter,bus_shutdown,)
    )
    #print(bus_shutdown.is_set())
    client.start()
    server.start()

    time.sleep(3)
    bus_shutdown.set()

    server.join()
    client.join()

    print("\n")
    print("RECV'D Voltage: ", voltage_RX)
    print("TX'D Voltage: ", word_voltages[1])

    assert(np.array(voltage_RX) == word_voltages[1])

if __name__ == '__main__':
    main()