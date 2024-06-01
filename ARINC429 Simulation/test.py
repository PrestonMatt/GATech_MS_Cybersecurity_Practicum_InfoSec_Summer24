import threading
import time
import pytest

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


if __name__ == '__main__':
    main()