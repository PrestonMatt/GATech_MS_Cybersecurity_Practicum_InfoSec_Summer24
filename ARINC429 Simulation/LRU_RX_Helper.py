# My classes:
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
# Python classes
import numpy as np
from time import sleep, time
from threading import Thread
from queue import Queue
import matplotlib.pyplot as plt

class arinc429_RX_Helpers():
    def __init__(self, bus_speed = "Low", BUS_CHANNELS = []):
        if(bus_speed.lower() == "high"):
            self.binary_voltage_converter = b2v(True)
        elif(bus_speed.lower() == "low"):
            self.binary_voltage_converter = b2v(False)
        else:
            raise ValueError("Speed must be either 'HIGH' or 'LOW'")

        # Get bus speed
        self.bus_speed = bus_speed
        # pass bus channels here
        self.BUS_CHANNELS = BUS_CHANNELS
        self.usec_start = time()

        self.tx_funcs = lru_txr(self.bus_speed, self.BUS_CHANNELS)

    def __str__(self):
        pass

    def receive_given_word(self, channel_index=0) -> int:
        word_bitStr = ""

        ts = np.array([])
        vs = np.array([])

        while(len(word_bitStr.replace("0b","")) < 32):
            current_time_in_usec = time() - self.usec_start
            ts = np.concatenate((ts, np.array([current_time_in_usec])))
            vs = np.concatenate(
                ( vs,
                 np.array([
                     self.receive_single_voltage_from_wire(self.BUS_CHANNELS[channel_index])
                 ]) )
            )

            word_as_int, word_bitStr = self.binary_voltage_converter.from_voltage_to_bin_word(
                (ts, vs),
                self.binary_voltage_converter.get_speed()
            )
        print(word_bitStr)

        if(self.validate_word(word_as_int) == False):
            print("Word is not valid")
            # Don't raise an error because we don't want to stop the bus from collapsing

        return(word_as_int, word_bitStr)

    """
    # https://stackoverflow.com/questions/24838629/round-off-float-to-nearest-0-5-in-python
    def return_nearest_half_microsecond(self,usec_messy):
        return(round(usec_messy * 2) / 2)
    """

    def validate_word(self, word:int) -> bool:
        return(self.tx_funcs.validate_word(word))

    def receive_single_voltage_from_wire(self, channel) -> float:
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist!")
        #sleep(5e-7)
        voltage = channel.get_voltage()
        #print(voltage)
        return(voltage)

    def visualize_LRU_receiveds(self, channel):
        vs = [0.0 for x in range(100)]
        # interactive plot
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'go--')
        fig.suptitle("Receive Data")

        ax.set_xlim(100)
        ax.set_ylim(-14, 14) # within spec
        while(True):
            vs.append(self.receive_single_voltage_from_wire(channel))

            line.set_xdata(range(100))
            line.set_ydata(vs[-101:-1])

            ax.set_xlim(0, max(100, 1))

            fig.canvas.draw()
            fig.canvas.flush_events()