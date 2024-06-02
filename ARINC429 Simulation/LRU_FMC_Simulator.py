from arinc429_voltage_sim import binary_to_voltage as b2v
from time import sleep, time

class flight_management_computer:

    def __init__(self, speed):
        if(speed.lower() == "high"):
            self.word_voltage_generator = b2v(True)
        elif(speed.lower() == "low"):
            self.word_voltage_generator = b2v(False)
        else:
            raise ValueError("Speed must be either 'HIGH' or 'LOW'")

        self.usec_start = time()

    def __str__(self):
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
            this_word_usec_start = time() - self.usec_start
            print(this_word_usec_start)
            ts, vs = self.word_voltage_generator.from_intWord_to_signal(self.word_voltage_generator.get_speed(),
                                                                         word,
                                                                         this_word_usec_start)
            self.word_voltage_generator.graph_words((ts,vs),tickrate=300)
            for voltage in vs:
                self.transmit_single_voltage_to_wire(voltage)
                sleep(0.5e-6) # sleep 1/2 microsecond

    def validate_word(self, word) -> bool:

        word = bin(word)
        #print(word)

        # First word must be 32 bits:
        if(len(word.replace("0b","")) > 32):
            print("Word too large")
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
        print(voltage)