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

    def get_label_from_word(self, word:int) -> int:
        # remember label is transmitted BACKWARDS for some ******** reason
        # get the top 8 bits from a 32bit word:
        top8_bits = word >> 24
        # Convert the integer to a binary string without the '0b' prefix
        label_bin_str = bin(top8_bits)[2:]
        if(len(label_bin_str) < 8):
            # Need to append zeros.
            label_bin_str = "0"*(8-len(label_bin_str)) + label_bin_str
        # Reverse the binary string
        reversed_label_str = label_bin_str[::-1]
        # Convert the reversed binary string back to an integer
        # This has to be digit by digit.
        dig1 = reversed_label_str[0:2] # bits 1 and 2
        dig2 = reversed_label_str[2:5] # bits 3, 4, and 5
        dig3 = reversed_label_str[5:] # bits 6, 7, 8

        digit1 = int(dig1,2) # this should be in octal
        digit2 = int(dig2,2) # this should be in octal
        digit3 = int(dig3,2) # this should be in octal

        full_octal_code = str(digit1) + str(digit2) + str(digit3)

        true_label = int(full_octal_code, 8)

        return(true_label)

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