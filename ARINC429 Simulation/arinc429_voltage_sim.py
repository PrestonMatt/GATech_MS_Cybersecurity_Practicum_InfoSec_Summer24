import matplotlib.pyplot as plt
import numpy as np
import random

class binary_to_voltage:

    # TX
    # HIGH  (i.e. 1) =>      10.0 V +/- 1.0 V
    # NULL                    0.0 V +/- 0.5 V
    # LOW   (i.e. 0) =>     -10.0 V +/- 1.0 V

    # RX
    # HIGH  (i.e. 1) =>     [+ 6.5V, +13.0V]
    # NULL                  [- 2.5V, + 2.5V]
    # LOW   (i.e. 0) =>     [-13.0V, - 6.5V]

#    def main():
#        print("Test begin")
#        test_all_functions()

    def __init__(self, hl_speed):
        self.hl_speed = hl_speed

    def __str__(self):
        print("Speed: %" % self.hl_speed)

    def get_bus_speed(self):
        return(self.hl_speed)

    def test_all_functions(self):
        print("Testing HIGH SPEED 1 bit.")
        self.graph_words(self.create_ARINC429_one_highspeed(0),figtitle = "One High speed Bit")
        print("Testing LOW SPEED 1 bit.")
        self.graph_words(self.create_ARINC429_one_lowspeed(0),figtitle = "One Low speed Bit")
        print("Testing HIGH SPEED 0 bit.")
        self.graph_words(self.create_ARINC429_zero(0,True),figtitle = "Zero High speed Bit")
        print("Testing LOW SPEED 0 bit.")

        self.graph_words(self.create_ARINC429_zero(0,False),figtitle = "Zero Low speed Bit")
        print("Creating Random High Speed Word.")
        self.graph_words(self.create_random_word(True))
        print("Creating Random Low Speed Word.")
        self.graph_words(self.create_random_word(False),tickrate = 50)

        print("Testing with given LS word of: 0b11111101000000000000001000110000")
        self.graph_words(self.frombitstring_to_signal(False,0b11111101000000000000001000110000,0),figtitle="Set Word Engine Reverse Thrust 70%",tickrate=50)

        print("Testing with null time of 4 bits in between random words, 5 words, HS.")
        self.graph_words(self.generate_n_random_words(True, n = 3),figtitle="Three Random Words")

        print("Trying to RX given HS word of: 0b11111101000000000000001000110000")
        hl_speed = True
        bits = self.from_voltage_to_bin(
            self.frombitstring_to_signal(hl_speed,0b11111101000000000000001000110000,0.0),
            hl_speed,
            True # graph the word.
        )
        print("RX'd %s binary!" % bin(bits))

        print("Trying to RX given LS word of: 0b11111101000000000000001000110000")
        hl_speed = False
        bits = self.from_voltage_to_bin(
            self.frombitstring_to_signal(hl_speed,0b11111101000000000000001000110000,0.0),
            hl_speed,
            True # graph the word.
        )
        print("RX'd %s binary!" % bin(bits))

    def graph_words(self,word,figtitle = "ARINC 429 Word with Random Bits",tickrate=5):
        ts = word[0]
        vs = word[1]

        fig, ax = plt.subplots()
        # want around -10, 0, 10
        ax.axhline(-10.0, linestyle="--")
        ax.axhline(0.0, linestyle="--")
        ax.axhline(10.0, linestyle="--")

        plt.plot(ts, vs, 'go--')
        plt.xlabel("Time in usec")
        plt.ylabel("Voltage")
        plt.title(figtitle)
        plt.xticks(np.arange(min(ts),max(ts)+1,tickrate))
        plt.show()

    def from_voltage_to_bin_word(self, word, hl_speed, show_word=False):
        ts = word[0]
        vs = word[1]

        if(show_word):
            self.graph_words((ts,vs),figtitle = "70% reverse thrust ARINC 429 Word sent.")

        # HIGH SPEED bits can be up/down as short as 4.5 usecs

        # LOW SPEED bits can be up/down as short as 40 usecs

        num_volts = 8 # HIGH SPEED
        if(not hl_speed): # LOW SPEED
            num_volts = 39

        voltages = []

        check_for_null = False

        bits = []

        for voltage in vs:
            if(len(voltages) > num_volts):
                voltages.pop()
            voltages = [voltage] + voltages
            #print(voltages)
            if(check_for_null): # reset between bits
                returned_to_null = self.check_all_voltages_is_ret2null(voltages)
                if(returned_to_null):
                    check_for_null = False
                    voltages = []
            else: # not looking for a reset between bits
                if(self.check_all_voltages_is_1(voltages)):
                    # is a 1
                    bits.append(1)
                    check_for_null = True
                    voltages = []
                elif(self.check_all_voltages_is_0(voltages)):
                    bits.append(0)
                    check_for_null = True
                    voltages = []

        #print(len(bits))

        bin_str = ""
        for bit in bits:
            bin_str += str(bit)

        binary_ = int(bin_str,2)
        #print(bin_str)
        #print(binary_)

        return(binary_)

    def is_four_nulls_in_a_row(self, word, hl_speed):
        ts = word[0]
        vs = word[1]

        num_volts = 8 * 4 # HIGH SPEED
        if(not hl_speed): # LOW SPEED
            num_volts = 39 * 4

        cnt = 0
        copy_vs = vs
        copy_ts = ts
        for voltage in vs:
            cnt += 1
            if(voltage > 2.5 or voltage < -2.5):
                if(cnt < num_volts):
                    return(False, word)
                else:
                    return(True, (copy_ts,copy_vs))
            copy_vs = copy_vs[1:]
            copy_ts = copy_ts[1:] # Leftovers

    def check_all_voltages_is_1(self, vs):
        for voltage in vs:
            if(voltage < 6.5 or voltage > 13.0):
                return(False)
        return(True)

    def check_all_voltages_is_ret2null(self, vs):
        for voltage in vs:
            if(voltage < -2.5 or voltage >2.5):
                return(False)
        return(True)

    def check_all_voltages_is_0(self, vs):
        for voltage in vs:
            if(voltage < -13.0 or voltage > -6.5):
                return(False)
        return(True)

    def create_ARINC429_one_highspeed(self, usec_start):
        # first [0.5,2.0] usec
        v_rise =[]
        rise_usecs = random.randint(2,4) / 2
        # next [4.5,5.5] usec
        v_stab = []
        stab_usecs = random.randint(9,11) / 2
        # next [0.5,2.0] usec
        v_fall = []
        fall_usecs = random.randint(2,4) / 2
        # final [4.5,5.5] usec
        v_null = []
        null_usecs = random.randint(9,11) / 2

        this_bit_usec_total = rise_usecs + stab_usecs + fall_usecs + null_usecs
        #print(rise_usecs, stab_usecs, fall_usecs, null_usecs)

        # Array is in microseconds. This is the HIGH SPEED standard
        t_usecs = np.arange(usec_start,
                             usec_start + this_bit_usec_total,
                             0.5) # sample every 1/2 microsecond.

        # rise:
        for step1 in range(int(rise_usecs * 2)): # maps to -> range(0.0,1.5,0.5):
            rise_voltage = random.uniform(0.0,10.0)
            v_rise.append(rise_voltage)
        v_rise.sort()

        # high:
        for step2 in range(int(stab_usecs * 2)): # maps to -> range(1.5,5,0.5):
            stable_voltage = random.uniform(9.0,11.0)
            v_stab.append(stable_voltage)

        # fall:
        for step3 in range(int(fall_usecs * 2)): # maps to -> range(5,6.5,0.5):
            fall_voltage = random.uniform(0.0,10.0)
            v_fall.append(fall_voltage)
        v_fall.sort(reverse=True) # need to reverser order this sort

        # null:
        for step4 in range(int(null_usecs * 2)): # maps to -> range(6.5,10.0,0.5):
            null_voltage = random.uniform(-0.5,0.5)
            v_null.append(null_voltage)

        voltages = np.concatenate(
            (v_rise, v_stab, v_fall, v_null)
        )

        #print("Time: %s" % t_usecs)
        #print("Voltages: %s", voltages)

        return(t_usecs,voltages)

    def create_ARINC429_one_lowspeed(self, usec_start):
        # Array is in microseconds. This is the LOW SPEED standard
        # 12 kbps = 0.012 bits per microsecond = 83.33 usec per bit -> round to 84

        # first [5,15] usec
        v_rise =[]
        rise_usecs = random.randint(5,15)
        # next [40,44] usec
        v_stab = []
        stab_usecs = random.randint(40,44)
        # next [5,15] usec
        v_fall = []
        fall_usecs = random.randint(5,15)
        # final [40,44] usec
        v_null = []
        null_usecs = random.randint(40,44)

        this_bit_usec_total = rise_usecs + stab_usecs + fall_usecs + null_usecs
        #print(rise_usecs, stab_usecs, fall_usecs, null_usecs)


        t_usecs = np.arange(usec_start,
                             usec_start + this_bit_usec_total,
                             0.5) # sample every 1/2 microsecond.

        # rise:
        for step1 in range(rise_usecs * 2):
            rise_voltage = random.uniform(0.0,10.0)
            v_rise.append(rise_voltage)
        v_rise.sort()

        # high:
        for step2 in range(stab_usecs * 2):
            stable_voltage = random.uniform(9.0,11.0)
            v_stab.append(stable_voltage)

        # fall:
        for step3 in range(fall_usecs * 2):
            fall_voltage = random.uniform(0.0,10.0)
            v_fall.append(fall_voltage)
        v_fall.sort(reverse=True) # need to reverser order this sort

        # null:
        for step4 in range(null_usecs * 2):
            null_voltage = random.uniform(-0.5,0.5)
            v_null.append(null_voltage)

        voltages = np.concatenate(
            (v_rise, v_stab, v_fall, v_null)
        )

        return(t_usecs,voltages)

    def create_ARINC429_zero(self, usec_start, lh_speed):
        if(lh_speed):
            ts, vs = self.create_ARINC429_one_highspeed(usec_start)
        else:
            ts, vs = self.create_ARINC429_one_lowspeed(usec_start)

        new_vs = []

        for voltage in vs:
            new_voltage = voltage * -1.0
            new_vs.append(new_voltage)

        zero_voltages = np.array(new_vs)

        return(ts,zero_voltages)

    def create_null_time_between_words(self, hl_speed, usec_start):
        # "Sequential words are separated by at least 4-bit times of null or zero voltage"
        # zero voltage defined as: [-0.5, +0.5] volts

        # HIGH SPEED BIT TIME -> 10 usec +/- 2.5% -> [7.5, 12.5] usec
        # LOW SPEED BIT TIME -> 84 usec +/- 2.5% [82, 86] usec

        null_time = 0
        for x in range(4):
            if(hl_speed): # HIGH SPEED
                null_time += random.randint(15,25) / 2
            else: # LOW SPEED
                null_time += random.randint(82,86)

        t_usecs = np.arange(usec_start,
                             usec_start + null_time,
                             0.05) # sample every 1/2 microsecond.
        vs = []
        for x in range(len(t_usecs)): # generate voltage samples
            vs.append(random.uniform(-0.5,0.5))

        voltages = np.array(vs)
        return(t_usecs,voltages)

    def create_random_word(self, lh_speed):
        voltages = np.array([0.0])
        times = np.array([0.0])

        for x in range(32):
            one_zero_bool = bool(random.getrandbits(1))
            if(one_zero_bool): # 1
                if(lh_speed): # HIGH SPEED
                    ts, vs = self.create_ARINC429_one_highspeed(times[-1] + 0.5)
                else: # LOW SPEED
                    ts, vs = self.create_ARINC429_one_lowspeed(times[-1] + 0.5)
            else: # 0
                ts, vs = self.create_ARINC429_zero(times[-1] + 0.5,lh_speed)

            voltages = np.concatenate((voltages,vs), axis = 0)
            times = np.concatenate((times, ts), axis = 0)

        return(times,voltages)

    def frombitstring_to_signal(self, hl_speed, bits, usec_start):
        # bits -> int(0b01010101,2)

        voltages = np.array([0.0])
        times = np.array([usec_start])

        o_bits = bin(bits)[2:] # cut out 0b
        for o_bit in o_bits:
            o_bit = int(o_bit,2)

            vs = []
            ts = []
            if(o_bit): # 1
                if(hl_speed): # HIGH SPEED
                    ts, vs = self.create_ARINC429_one_highspeed(times[-1] + 0.5)
                else: # LOW SPEED
                    ts, vs = self.create_ARINC429_one_lowspeed(times[-1] + 0.5)
            else: # 0
                ts, vs = self.create_ARINC429_zero(times[-1] + 0.5,hl_speed)
            voltages =  np.concatenate((voltages,vs), axis = 0)
            times = np.concatenate((times, ts), axis = 0)

        return(times,voltages)

    def generate_n_random_words(self, hl_speed,n=5):
        voltages = np.array([0.0])
        times = np.array([0.0])
        for w in range(n):
            randomword = random.getrandbits(32)

            # Word
            t1s, v1s = self.frombitstring_to_signal(hl_speed, randomword, times[-1] + 0.5)
            voltages =  np.concatenate((voltages,v1s), axis = 0)
            times = np.concatenate((times, t1s), axis = 0)

            t2s, v2s = self.create_null_time_between_words(hl_speed, times[-1] + 0.5)
            voltages =  np.concatenate((voltages,v2s), axis = 0)
            times = np.concatenate((times, t2s), axis = 0)

        return(times,voltages)

#if __name__ == "__main__":
#    main()
