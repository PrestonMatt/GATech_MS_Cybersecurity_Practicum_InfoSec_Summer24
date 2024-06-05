from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
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

    def __str__(self):
        pass

    def pilot_input(self):
        # listen for arrow keys to simulate the joystick
        while(True):
            direction = ""
            # UP -> Pitch plane up
            if(keyboard.is_pressed('up')):
                self.generate_word_to_pitch_plane(self, "UP")
            # DOWN -> Pitch plane down
            if(keyboard.is_pressed('down')):
                self.generate_word_to_pitch_plane(self, "DOWN")
            # LEFT -> pitch plane left
            if(keyboard.is_pressed('left')):
                self.generate_word_to_pitch_plane(self, "LEFT")
            # RIGHT -> pitch plane right
            if(keyboard.is_pressed('right')):
                self.generate_word_to_pitch_plane(self, "RIGHT")
            # W -> push plane forward
            if(keyboard.is_pressed('w')):
                self.generate_word_to_pitch_plane(self, "W")
            # S -> slow plane down and go backwards
            if(keyboard.is_pressed('s')):
                self.generate_word_to_pitch_plane(self, "S")

    def generate_word_to_pitch_plane(self, direction):

        # if scheduled mode; send word to scheduler.
        # if FIFO mode; send word to FIFO

        word = 0b0

        if(direction.lower() == "up"):
            # Want to send to W&BS
            # label = 0o066, longitudinal CG
            word_bitStr = bin(0o066)[2:]
            if(len(word_bitStr) < 8):
                word_bitStr = "0"*(8-len(word_bitStr)) + word_bitStr

            # SDI = 11
            word_bitStr += "11"

            # Data = BCD
            # Digit 5 = 11 to 14 (4 bits)
            word_bitStr += "0000"
            # Digit 4 = 15 to 18 (4 bits)
            word_bitStr += "1111"
            # Digit 3 = 19 to 22 (4 bits)
            word_bitStr += "1111"
            # Digit 2 = 26 to 23 (4 bits)
            word_bitStr += "1111"
            # Digit 1 = 27 to 29 (3 bits)
            word_bitStr += "1111" # TODO check all these lols

            # SSM = 00 for normal ops
            word_bitStr += "00"

            # calculate parity
            word_bitStr += self.calc_parity(word_bitStr)

            word = int(word_bitStr,2)
        if(direction.lower() == "down"):
            pass
        if(direction.lower() == "left"):
            pass
        if(direction.lower() == "right"):
            pass
        if(direction.lower() == "w"):
            pass
        if(direction.lower() == "s"):
            pass

        if(self.fifo_mode):
            self.FIFO_mode(word)
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
        self.FIFO.put(next_word)
        if(len(self.FIFO) > self.fifo_len):
            word_to_send = self.FIFO.get() # remove from queue
            self.transmit_given_word(word_to_send)

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

    def transmit_given_word(self, word:int, channel_index=0):
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

    # https://stackoverflow.com/questions/24838629/round-off-float-to-nearest-0-5-in-python
    def return_nearest_half_microsecond(self,usec_messy):
        return(round(usec_messy * 2) / 2)

    def validate_word(self, word) -> bool:

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

    def transmit_single_voltage_to_wire(self, voltage, channel):
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist!")
        channel.add_voltage(voltage)

    def visualize_FMC_transmissions(self, channel):
        if(not channel in self.BUS_CHANNELS):
            raise ValueError("Bus must exist to visualize!")
        # Start the real-time visualization in a separate thread
        visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel,0.005,"Transmit Data"))
        visualization_thread.start()
        #channel.queue_visual(fig_title = f"FMC LRU TX Voltages on Channel {channel}")
        visualization_thread.join()