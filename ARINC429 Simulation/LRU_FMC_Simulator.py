from arinc429_voltage_sim import binary_to_voltage as b2v
from time import sleep, time
import keyboard

class flight_management_computer:

    def __init__(self, speed, mode = "FIFO"): # Default is FIFO mode
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

    def __str__(self):
        pass

    def FIFO_words(self):
        pass

    def pilot_input(self):
        # listen for arrow keys to simulate the joystick
        while(True):
            direction = ""
            # UP -> Pitch plane up
            if(keyboard.is_pressed('up')):
                generate_word_to_pitch_plane(self, "UP")
            # DOWN -> Pitch plane down
            if(keyboard.is_pressed('down')):
                generate_word_to_pitch_plane(self, "DOWN")
            # LEFT -> pitch plane left
            if(keyboard.is_pressed('left')):
                generate_word_to_pitch_plane(self, "LEFT")
            # RIGHT -> pitch plane right
            if(keyboard.is_pressed('right')):
                generate_word_to_pitch_plane(self, "RIGHT")
            # W -> push plane forward
            if(keyboard.is_pressed('w')):
                generate_word_to_pitch_plane(self, "W")
            # S -> slow plane down and go backwards
            if(keyboard.is_pressed('s')):
                generate_word_to_pitch_plane(self, "S")

    def generate_word_to_pitch_plane(self, direction):
        if(direction.lower() == "up"):
            # word goes to FAEC
            word
        if(direction.lower() == "down"):
            pass


    def transmit_random_voltages(self):
        while(True):
            try:
                random_word = self.word_voltage_generator.generate_n_random_words(self.word_voltage_generator.get_speed(), n = 1)
                self.word_voltage_generator.graph_words(random_word)

                cnt = 0
                voltages = random_word[1]
                times = random_word[0]

                for voltage in voltages:
                    # send this voltage to the wire
                    self.transmit_single_voltage_to_wire(voltage)
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

    def transmit_given_word(self, word:int):
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
                self.transmit_single_voltage_to_wire(voltage)
                sleep(0.5e-6) # sleep 1/2 microsecond

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

    # TODO: Send them over some bus-like, simulation medium.
    def transmit_single_voltage_to_wire(self, voltage):
        #print(voltage)
        pass