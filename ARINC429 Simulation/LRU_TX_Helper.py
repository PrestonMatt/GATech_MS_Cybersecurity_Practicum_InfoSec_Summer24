# My classes:
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
# Python classes
from time import sleep, time
from threading import Thread
from queue import Queue

class arinc429_TX_Helpers():
    def __init__(self, bus_speed = "Low", BUS_CHANNELS = []):
        if(bus_speed.lower() == "high"):
            self.word_voltage_generator = b2v(True)
        elif(bus_speed.lower() == "low"):
            self.word_voltage_generator = b2v(False)
        else:
            raise ValueError("Speed must be either 'HIGH' or 'LOW'")

        # Get bus speed
        self.bus_speed = bus_speed
        # pass bus channels here
        self.BUS_CHANNELS = BUS_CHANNELS

    def __str__(self):
        pass

    def transmit_random_voltages(self, channel_index = 0, visualize = False):
        while(True):
            try:
                random_word = self.word_voltage_generator.generate_n_random_words(self.word_voltage_generator.get_speed(), n = 1)
                if(visualize):
                    self.word_voltage_generator.graph_words(random_word)
                voltages = random_word[1]
                for voltage in voltages:
                    # send this voltage to the wire
                    self.transmit_single_voltage_to_wire(voltage, self.BUS_CHANNELS[channel_index])
                    # sleep 1/2 microsecond
                    sleep(0.5e-6)
            except KeyboardInterrupt:
                break

    def transmit_given_word(self, word:int, bus_usec_start, channel_index=0, slowdown_rate = 5e-7):
        if(self.validate_word(word) == False): # word is invalid:
            raise ValueError("Word is not valid")
        else:
            this_word_usec_start = (time() - bus_usec_start) # this is given in seconds.
            this_word_usec_start *= 1_000_000 # now given in microseconds since FMC fired up.
            # Just round to nearest half microseconds:
            this_word_usec_start = self.return_nearest_half_microsecond(this_word_usec_start)
            print(this_word_usec_start)
            ts, vs = self.word_voltage_generator.from_intWord_to_signal(self.word_voltage_generator.get_speed(),
                                                                        word,
                                                                        this_word_usec_start)
            self.word_voltage_generator.graph_words((ts,vs),tickrate=300)
            #print(ts)
            for voltage in vs:
                self.transmit_single_voltage_to_wire(voltage, self.BUS_CHANNELS[channel_index])
                sleep(slowdown_rate) # sleep 1/2 microsecond is default

    # https://stackoverflow.com/questions/24838629/round-off-float-to-nearest-0-5-in-python
    def return_nearest_half_microsecond(self,usec_messy):
        return(round(usec_messy * 2) / 2)

    def validate_word(self, word:int) -> bool:

        word = bin(word)

        # First word must be 32 bits:
        if(len(word.replace("0b","")) > 32):
            #print("Word too large")
            return(False)

        # Count the number of '1's in the bit string (excluding the parity bit)
        num_of_ones = word[:-1].count('1')

        # Get the parity bit (last bit)
        parity_bit = word[-1]

        # Check the parity condition
        if(num_of_ones % 2 == 0): # even
            return(parity_bit == '0')
        else: # odd
            return(parity_bit == '1')

    def transmit_single_voltage_to_wire(self, voltage, channel):
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist!")
        channel.add_voltage(voltage)

    def visualize_LRU_transmissions(self, channel):
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist to visualize!")
        # Start the real-time visualization in a separate thread
        visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel,0.005,"Transmit Data"))
        visualization_thread.start()
        #channel.queue_visual(fig_title = f"FMC LRU TX Voltages on Channel {channel}")
        visualization_thread.join()

    def make_label_for_word(self, label:int) -> (str,int):
        # Convert the integer to a binary string without the '0b' prefix
        label_bin_str = bin(label)[2:]
        if(len(label_bin_str) < 8):
            # Need to append zeros.
            label_bin_str = "0"*(8-len(label_bin_str)) + label_bin_str
        # Reverse the binary string
        reversed_label_str = label_bin_str[::-1]
        # Convert the reversed binary string back to an integer
        true_label = int(reversed_label_str, 2)
        return(reversed_label_str,true_label)

    def calc_parity(self, word_bitStr):
        if(len(word_bitStr) != 31):
            raise ValueError("Checking parity must be for 31 bit imcomplete words")
        # Count the number of '1's in the bit string (excluding the parity bit)
        num_of_ones = word_bitStr[:-1].count('1')

        # Check the parity condition
        if(num_of_ones % 2 == 0): # even
            return('0')
        else: # odd
            return('1')