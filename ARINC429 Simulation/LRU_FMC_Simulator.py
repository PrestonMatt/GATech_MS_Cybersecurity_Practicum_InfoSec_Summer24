# My Classes
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
# Python Classes
from time import sleep, time
import keyboard
from threading import Thread
from queue import Queue

class flight_management_computer:

    def __init__(self, speed, mode = "FIFO", fifo_len = 8, BUS_CHANNELS = []): # Default is FIFO mode
        if(speed.lower() == "high"):
            self.word_voltage_generator = b2v(True)
        elif(speed.lower() == "low"):
            self.word_voltage_generator = b2v(False)
        else:
            raise ValueError("Speed must be either 'HIGH' or 'LOW'")

        # zero the bus clock.
        self.usec_start = time()
        if(mode.lower() == "fifo"):
            self.fifo_mode = True
            self.scheduler_mode = False
        if(mode.lower() == "scheduler"):
            self.scheduler_mode = True
            self.fifo_mode = False

        self.fifo_len = fifo_len

        self.FIFO = Queue() # inherently FIFO
        self.scheduler = {}
        # pass bus channels here
        self.BUS_CHANNELS = BUS_CHANNELS

        self.communication_chip = lru_txr(bus_speed = speed.lower(), BUS_CHANNELS = [self.BUS_CHANNELS[1:]])

        self.RXcomm_chip = lru_rxr(bus_speed = speed.lower(), BUS_CHANNELS = [self.BUS_CHANNELS[0]])

    def __str__(self):
        pass

    def pilot_input(self):
        # listen for arrow keys to simulate the joystick
        while(True):
            direction = ""
            # UP -> Pitch plane up
            if(keyboard.is_pressed('up')):
                self.generate_word_to_pitch_plane("UP")
            # DOWN -> Pitch plane down
            if(keyboard.is_pressed('down')):
                self.generate_word_to_pitch_plane("DOWN")
            # LEFT -> pitch plane left
            if(keyboard.is_pressed('left')):
                self.generate_word_to_pitch_plane("LEFT")
            # RIGHT -> pitch plane right
            if(keyboard.is_pressed('right')):
                self.generate_word_to_pitch_plane("RIGHT")
            # W -> push plane forward
            if(keyboard.is_pressed('w')):
                self.generate_word_to_pitch_plane("W")
            # S -> slow plane down and go backwards
            if(keyboard.is_pressed('s')):
                self.generate_word_to_pitch_plane("S")

    def generate_word_to_pitch_plane(self, direction):

        # if scheduled mode; send word to scheduler.
        # if FIFO mode; send word to FIFO

        word = 0b0

        if(direction.lower() == "up"):
            # Want to send to W&BS
            # label = 0o066, longitudinal CG
            """
            word_bitStr = bin(0o066)[2:]
            if(len(word_bitStr) < 8):
                word_bitStr = "0"*(8-len(word_bitStr)) + word_bitStr
            """
            word_bitStr, _ = self.communication_chip.make_label_for_word(0o066)

            # SDI = 11
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "1111" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "0000" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "0000" # LEFT = 0000
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "0000" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)

            word = int(word_bitStr,2)
        if(direction.lower() == "down"):
            word_bitStr, _ = self.communication_chip.make_label_for_word(0o066)

            # SDI = 11 for W&BS
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "0000" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "1111" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "0000" # LEFT = 0000
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "0000" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)
        if(direction.lower() == "left"):
            word_bitStr, _ = self.communication_chip.make_label_for_word(0o067)

            # SDI = 11 for W&BS
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "0000" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "0000" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "1111" # LEFT = 0000
            # Digit 2 = 23 to 26 (4 bits)
            word_bitStr += "0000" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)
            # Close flap on the right:
            second_word = self.communication_chip.make_label_for_word(0o104) + "11" # SDI = W&BS
            second_word += "0000" # UP = 0000
            second_word += "0000" # DOWN = 0000
            second_word += "0000" # LEFT = 0000
            second_word += "0101" # RIGHT = 0000
            second_word += "000" # FORWARD = 000, BACKWARD = 111
            # SSM = 00 for normal ops
            second_word += "00"
            second_word += self.calc_parity(second_word)
            # Open flap on left:
            third_word = self.communication_chip.make_label_for_word(0o103) + "11" # SDI = W&BS
            third_word += "0000" # UP = 0000
            third_word += "0000" # DOWN = 0000
            third_word += "1010" # LEFT = 0000
            third_word += "0000" # RIGHT = 0000
            third_word += "000" # FORWARD = 000, BACKWARD = 111
            # SSM = 00 for normal ops
            third_word += "00"
            third_word += self.calc_parity(third_word)

            if(self.fifo_mode):
                # TODO fix FIFO Full feature
                #self.FIFO_mode(word)
                self.transmit_given_word(second_word)
                self.transmit_given_word(third_word)
            else:
                self.scheduler_mode(second_word, 20_000_000) # send 20 sec later
                self.scheduler_mode(third_word, 20_000_000) # send 20 sec later
        if(direction.lower() == "right"):
            word_bitStr, _ = self.communication_chip.make_label_for_word(0o067)

            # SDI = 11
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "0000" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "0000" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "0000" # LEFT = 0000
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "1111" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)

            # Close flap on the left:
            second_word = self.communication_chip.make_label_for_word(0o104) + "11" # SDI = W&BS
            second_word += "0000" # UP = 0000
            second_word += "0000" # DOWN = 0000
            second_word += "0101" # LEFT = 0000
            second_word += "0000" # RIGHT = 0000
            second_word += "000" # FORWARD = 000, BACKWARD = 111
            # SSM = 00 for normal ops
            second_word += "00"
            second_word += self.calc_parity(second_word)
            # Open flap on left:
            third_word = self.communication_chip.make_label_for_word(0o103) + "11" # SDI = W&BS
            third_word += "0000" # UP = 0000
            third_word += "0000" # DOWN = 0000
            third_word += "0000" # LEFT = 0000
            third_word += "1010" # RIGHT = 0000
            third_word += "000" # FORWARD = 000, BACKWARD = 111
            # SSM = 00 for normal ops
            third_word += "00"
            third_word += self.calc_parity(third_word)

            if(self.fifo_mode):
                # TODO fix FIFO Full feature
                #self.FIFO_mode(word)
                self.transmit_given_word(second_word)
                self.transmit_given_word(third_word)
            else:
                self.scheduler_mode(second_word, 20_000_000) # send 20 sec later
                self.scheduler_mode(third_word, 20_000_000) # send 20 sec later
        if(direction.lower() == "w"):
            # SDI = 11
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "0000" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "0000" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "0000" # LEFT = 0000
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "0000" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)
        if(direction.lower() == "s"):
            # SDI = 11
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "1111" # UP = 1111
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "0000" # DOWN = 0000
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "0000" # LEFT = 0000
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "0000" # RIGHT = 0000
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "000" # FORWARD = 000, BACKWARD = 111

            # SSM = 00 for normal ops
            word_bitStr += "00"
            #print(word_bitStr)

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)
        print(word)

        if(self.fifo_mode):
            # TODO fix FIFO Full feature
            #self.FIFO_mode(word)
            self.transmit_given_word(word)
        else:
            self.scheduler_mode(word, 20_000_000) # send 20 sec later

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

    def FIFO_mode(self, next_word):
        print(str(self.FIFO))
        if(self.FIFO.full()):
            print("FIFO is full")
            word_to_send = self.FIFO.get() # remove from queue
            self.transmit_given_word(word_to_send)
        self.FIFO.put(next_word)
        #if(len(self.FIFO) > self.fifo_len):

    def scheduler_mode(self, next_word, condition):
        # add to scheduler dict:
        self.scheduler[next_word] = condition
        for word in self.scheduler: # check to see if any contition is set
            this_cond = self.scheduler[word]
            if(self.check_condition_met(this_cond)):
                self.transmit_given_word(word)
                # remove from scheduler
                self.scheduler.pop(word)

    def check_condition_met(self, condition):
        if(isinstance(condition, int)): # this is usecs
            usec_now = (time() - self.usec_start) # this is given in seconds.
            usec_now *= 1_000_000 # now given in microseconds since FMC fired up.
            # Just round to nearest half microseconds:
            usec_now = self.return_nearest_half_microsecond(usec_now)
            if(usec_now >= condition):
                return(True)
            else:
                return(False)
        elif(isinstance(condition, str)):
            # TODO set more example conditions
            pass
        else:
            # mis-made word. Never send then
            return(False)

    def transmit_random_voltages(self, channel_index = 0):
        self.communication_chip.transmit_random_voltages(channel_index)
        """
        while(True):
            try:
                random_word = self.word_voltage_generator.generate_n_random_words(self.word_voltage_generator.get_speed(), n = 1)
                #self.word_voltage_generator.graph_words(random_word)

                cnt = 0
                voltages = random_word[1]
                times = random_word[0]

                for voltage in voltages:
                    # send this voltage to the wire
                    self.transmit_single_voltage_to_wire(voltage, self.BUS_CHANNELS[channel_index])
                    # sleep for the appropriate amount of time.
                    # will always be 0.5 microseconds so the math is redundant.
                    #if(cnt < len(times)):
                    #    time_to_sleep = times[cnt + 1] - times[cnt]
                    #    cnt += 1
                    #    sleep(time_to_sleep)
                    #else:
                    sleep(0.5e-6) # sleep 1/2 microsecond
            except KeyboardInterrupt:
                break
        """

    def transmit_given_word(self, word:int, channel_index=0):
        #print(f"TX word:{word}")
        self.communication_chip.transmit_given_word(word, channel_index)
        """
        if(self.validate_word(word) == False): # word is invalid:
            raise ValueError("Word is not valid")
        else:
            this_word_usec_start = (time() - self.usec_start) # this is given in seconds.
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
                sleep(0.5e-7) # sleep 1/2 microsecond
        """

    # https://stackoverflow.com/questions/24838629/round-off-float-to-nearest-0-5-in-python
    def return_nearest_half_microsecond(self,usec_messy):
        return(round(usec_messy * 2) / 2)

    def validate_word(self, word) -> bool:
        """
        word = bin(word)
        #print(word)

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
        """
        return(self.communication_chip.validate_word(word))

    def transmit_single_voltage_to_wire(self, voltage, channel):
        """
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist!")
        channel.add_voltage(voltage)
        """
        self.communication_chip.transmit_single_voltage_to_wire(voltage, channel)

    def visualize_FMC_transmissions(self, channel):
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist to visualize!")
        # Start the real-time visualization in a separate thread
        visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel,0.005,"Transmit Data"))
        visualization_thread.start()
        #channel.queue_visual(fig_title = f"FMC LRU TX Voltages on Channel {channel}")
        visualization_thread.join()

    # Takes a word from the ADIRU and MX_program and does stuff to plane.
    def decodeADIRUword(self, adiruWord:str, prevVal)->str:
        new_word = "0"*32
        label = self.RXcomm_chip.get_label_from_word(int(adiruWord,2))
        #print(oct(label))
        if(label == 0o204):
            # Altitude: This is BNR.

            data = self.decode_BNR(adiruWord,1.0, (0.0,131072),0)

            if(data - prevVal > 0.0): # getting bigger:
                # Shift plane upwards:
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "1111" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                # calculate parity
                new_word += self.calc_parity(new_word)
            elif(data - prevVal < 0.0): # getting smaller
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "1111" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                # calculate parity
                new_word += self.calc_parity(new_word)
            else: # same
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0110" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                # calculate parity
                new_word += self.calc_parity(new_word)
        elif(label == 0o012):
            # Ground Speed: This is BNR
            ones_place = adiruWord[10:14]
            x1s = int(ones_place[::-1],2)
            tens_place = adiruWord[14:18]
            x10s = int(tens_place[::-1],2)
            hunds_place = adiruWord[18:22]
            x100s = int(hunds_place[::-1],2)
            thousand_place = adiruWord[22:26]
            x1000s = int(thousand_place[::-1],2)
            tenthousand_place = adiruWord[26:29]
            x10000s = int(tenthousand_place[::-1],2)

            data = (x10000s * 10000) + (x1000s * 1000) + (x100s * 100) + (x10s * 10) + x1s

            # Ground speed is increasing meaning increase thrust:
            if(data - prevVal > 0.0):
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                #print(word_bitStr)
                # calculate parity
                new_word += self.calc_parity(new_word)
            # Ground speed is decreasing meaning decrease thrust:
            elif(data - prevVal < 0.0):
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "111" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                #print(word_bitStr)
                # calculate parity
                new_word += self.calc_parity(new_word)
            # Ground speed is staying the same.
            else:
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "010" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                #print(word_bitStr)
                # calculate parity
                new_word += self.calc_parity(new_word)
            #print(f"RX Word, gs is {data} kts")
        elif(label == 0o310):
            # Latitude: This is BNR
            data = self.decode_BNR(adiruWord,0.000172, (-180.0, 180.0), 3)
            # Send to MX program
        elif(label == 0o311):
            # Longitude: This is BNR
            data = self.decode_BNR(adiruWord,0.000172, (7.0, 79.0),3)
            # Send to MX program
        elif(label == 0o325):
            # Roll Angle: This is BNR
            data = self.decode_BNR(adiruWord,0.1, (-4.0, 4.0),1)
            if(data < 0.0):
                # Turn left
                new_word, _ = self.communication_chip.make_label_for_word(0o067)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "1111" # LEFT = 0000
                # Digit 2 = 23 to 26 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                new_word += self.calc_parity(new_word)
            elif(data > 0.0):
                # Turn right
                new_word, _ = self.communication_chip.make_label_for_word(0o067)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 23 to 26 (4 bits)
                new_word += "1111" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                new_word += self.calc_parity(new_word)
            else: # Keep as is
                # Turn left
                new_word, _ = self.communication_chip.make_label_for_word(0o067)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0110" # LEFT = 0000
                # Digit 2 = 23 to 26 (4 bits)
                new_word += "0110" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                new_word += self.calc_parity(new_word)
        elif(label == 0o221):
            # Indicated Angle of Attack: This is BNR
            data = self.decode_BNR(adiruWord,0.000172, (-10.0, 10.0),3)
            if(data < 0.0): #AoA means go down
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11 for W&BS
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "0000" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "1111" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                # calculate parity
                new_word += self.calc_parity(new_word)
            elif(data > 0.0): #AoA means go up
                # Shift plane upwards:
                new_word, _ = self.communication_chip.make_label_for_word(0o066)
                # SDI = 11
                new_word += "11"
                # Data = BCD
                # Digit 5 = 11 to 14 (4 bits)
                new_word += "1111" # UP = 1111
                # Digit 4 = 15 to 18 (4 bits)
                new_word += "0000" # DOWN = 0000
                # Digit 3 = 19 to 22 (4 bits)
                new_word += "0000" # LEFT = 0000
                # Digit 2 = 26 to 23 (4 bits)
                new_word += "0000" # RIGHT = 0000
                # Digit 1 = 27 to 29 (3 bits)
                new_word += "000" # FORWARD = 000, BACKWARD = 111
                # SSM = 00 for normal ops
                new_word += "00"
                # calculate parity
                new_word += self.calc_parity(new_word)
            # else do nothing.
        # See if you need to grab MX word instead.
        #word =
        #cont = input("")
        return(new_word)

    def decode_BNR(self, word:str, res:float, encrange:tuple, round_digs:int) -> float:
        data = word[10:29][::-1]

        data = int(data, 2)

        if(res < 1.0):
            float_str = str(res).replace('.','')
            result = int(float_str)
            """
            decimal_pos = float_str.find('.')
            non_zero_pos = next((i for i, ch in enumerate(float_str[decimal_pos + 1:], start=decimal_pos + 1) if ch != '0'), None)
            if non_zero_pos:
                multiplier = 10 ** (non_zero_pos - decimal_pos)
            else:
                multiplier = 1  # fallback, though it shouldn't happen for a valid float input

            # Multiply and convert to integer
            result = int(res * multiplier)
            """
            data *= result
            # Find the decimal place.
            while(not (data < encrange[1] and data > encrange[0])):
                data /= 10.0
            data = round(data, round_digs)

        SSM = word[29:31]
        if(SSM.__contains__("1")):
            data *= -1.0

        return(data)