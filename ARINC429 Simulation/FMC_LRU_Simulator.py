import matplotlib.pyplot as plt
import numpy as np
import arinc429_voltage_sim
#from pwn import *

class flight_management_computer:

    words_FIFO = []

    def __init__(self, scheduled_mode):
        self.words_FIFO = []
        self.scheduled_mode = scheduled_mode
        pass

    def __str__(self):
        pass

    """
        Run a subprocess that is vulnerable
        Takes IP information and generates and sends words based on that connection
    """
    def maintainence_program(self):
        pass

    """
        Calculates the words to send based on user input and ADIRU
        Also based on MX program
    """
    def word_generation_calculation(self):
        pass

    def get_pilot_input(self):
        pass

    def rx_ADIRU_words(self):
        pass

    def FIFO_words(self, next_word, stacklength = 8):
        if(len(self.words_FIFO) >= stacklength):
            self.words_FIFO = self.words_FIFO[:-1]
        self.words_FIFO = [next_word] + self.words_FIFO

    def generate_voltage_for_word(self, word_binary):
        ts, vs = arinc429_voltage_sim.binary_to_voltage(word_binary)
        return(ts, vs)

    def send_voltage(self, channel):
        pass

    def scheduler_mode(self):
        pass