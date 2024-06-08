# My classes
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
# Python classes
from time import sleep, time


class global_positioning_system():
    # https://www.latlong.net/
    def __init__(self, bus_speed, channel, lat = "N 42 Deg 21.0'", lon = "W 71 Deg 23.0'"):
        if(not isinstance(channel, ARINC429BUS)):
            raise TypeError("Channel must be ARINC429BUS")
        self.channel = channel
        # set gps tx bus speed
        self.bus_speed = bus_speed
        # zero the bus clock.
        self.usec_start = time()
        self.latitude = lat
        self.longitude = lon

    def __str__(self):
        pass

    # returns latitude and longitude based on position
    def determine_position(self):

        return(0.0,0.0)

    def communicate_to_bus(self):
        lat, long = self.determine_position()
        # make word based on that
        word = 0b11111111111111111111111111111111

        communicator_chip = lru_txr(bus_speed = self.bus_speed,
                                    BUS_CHANNELS = [self.channel])

        communicator_chip.transmit_given_word(word, self.usec_start, self.channel)

        communicator_chip.visualize_LRU_transmissions(word, self.channel)
