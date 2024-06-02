import subprocess

import matplotlib.pyplot as plt
import numpy as np
from arinc429_voltage_sim import binary_to_voltage as b2v
from ARINC429_Client_Server import arinc429_client_server
from threading import Thread, Event
#import arinc429
#from pwn import *

class flight_management_computer:

    words_scheduler = None
    words_FIFO = None

    def __init__(self, scheduled_mode, speed):
        #self.words_FIFO = []
        self.scheduled_mode = scheduled_mode
        self.ADIRUI_RXd_voltages = []
        if(scheduled_mode): # Run in scheduled mode.
            self.words_scheduler = [[]]
        else:
            self.words_FIFO = []
        self.FMCServer_channelA = arinc429_client_server(client_mode=False,server_mode=True,
                                                    server_ip="127.0.0.1",
                                                    server_port=0x429A)
        self.FMCServer_channelB = arinc429_client_server(client_mode=False,server_mode=True,
                                                    server_ip="127.0.0.2",
                                                    server_port=0x429B)
        self.FMCClient_ADIRU = arinc429_client_server(client_mode=True,server_mode=False,
                                                      server_ip="127.0.0.3",
                                                      server_port=0x429C)
        if(speed == "High"):
            self.word_maker = b2v(True)
        elif(speed == "Low"):
            self.word_maker = b2v(False)
        else:
            raise ValueError("Bus speed must be either 'High' or 'Low'")

    def __str__(self):
        pass

    """
        Run a subprocess that is vulnerable
        Takes IP information and generates and sends words based on that connection
    """
    def maintainence_program(self):
        try:
            ts = np.array([0.0])
            vs = np.array([0.0])
            while(True):
                override_word = subprocess.run(["./mx_prog.out"],stdout=subprocess.PIPE)
                usec_start = ts[-1]
                ts, vs = self.word_maker.frombitstring_to_signal(hl_speed=self.word_maker.get_bus_speed(),
                                                                 bits = override_word,
                                                                 usec_start=usec_start)
                self.send_voltage("A",ts,vs)
                self.send_voltage("B",ts,vs)
        except KeyboardInterrupt:
            print("MX PROGRAM USER INTERRUPT")
        except Exception as e:
            print("Error in maintenance_program: %s" % str(e))

    """
        Calculates the words to send based on user input and ADIRU
        Also based on MX program
    """
    def word_generation_calculation(self):
        # Get data from ADIRU
        # Get MX words prepped to send
        # Get pilot input words prepped to send
        # if FIFO mode, just generate words and put them into the FIFO stack
        # if Scheduled mode, assign conditions for the sending of every word and only send when condition is met
        pass

    def get_pilot_input(self):
        pass

    def rx_ADIRU_words(self):

        speed = self.word_maker.get_bus_speed()
        if(speed == True): # HIGH SPEED
            vs_cnt = 8
        else: # LOW SPEED
            vs_cnt = 39

        begin_new_word_flag = False

        def voltage_reporter(voltage):
            self.ADIRUI_RXd_voltages.append(voltage)
            print(f"Received voltage: {voltage}")

            begin_new_word_flag, word = self.word_maker.is_four_nulls_in_a_row(self.ADIRUI_RXd_voltages)
            if(begin_new_word_flag):
                pass

            if(len(self.ADIRUI_RXd_voltages) > vs_cnt):  # Ensure there are enough voltages for HIGH and LOW speeds
                word = (range(len(self.ADIRUI_RXd_voltages)), self.ADIRUI_RXd_voltages)  # Create a tuple of timestamps and voltages
                binary_word = self.word_maker.from_voltage_to_bin_word(word, hl_speed=False)  # Assuming low speed
                self.received_words.append(binary_word)
                self.received_voltages.clear()  # Clear voltages after conversion

        Thread(target=self.FMCClient_ADIRU.client, args=(voltage_reporter,)).start()

    def FIFO_words(self, next_word, stacklength = 8):
        if(len(self.words_FIFO) >= stacklength):
            self.words_FIFO = self.words_FIFO[:-1]
        self.words_FIFO = [next_word] + self.words_FIFO

    def send_voltage(self, channel, ts, vs):
        if(channel == "A"):
            server = self.FMCServer_channelA
        elif(channel == "B"):
            server = self.FMCServer_channelA
        else:
            raise ValueError("Channel must be A or B")

        voltage_event = Event()
        voltageSentThread = Thread(target=server.server, args=(ts, vs, voltage_event,))
        voltageSentThread.start()
        #voltageSentThread.join()

    def scheduler_mode(self):
        pass