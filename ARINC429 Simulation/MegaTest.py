# Standard Libraries
import time
import random
import pytest
from threading import Thread
# Preston's libraries hehe
from arinc429_voltage_sim import binary_to_voltage as b2v
from LRU_FMC_Simulator import flight_management_computer as FMC
from BusQueue_Simulator import GlobalBus as ARINC429BUS

def main():
    #test_voltage_sim()
    #test_intWord_to_voltage()
    #test_FMC_word_validation1()
    #test_FMC_word_validation2()
    #test_FMC_word_validation3()
    #test_FMC_pilot_input()
    test_bus_queue()

def test_voltage_sim():
    word_voltage_obj = b2v(True)
    print(str(word_voltage_obj))
    word_voltage_obj.test_all_functions()

def test_intWord_to_voltage():
    word_voltage_obj1 = b2v(True)
    print(str(word_voltage_obj1))

    word_1 = 0b11111111111111111111111111111111
    ts, vs = word_voltage_obj1.from_intWord_to_signal(word_voltage_obj1.get_speed(), word_1,0.0)
    word_voltage_obj1.graph_words((ts,vs))

    word_2 = 0b00000000000000000000000000000011
    ts, vs = word_voltage_obj1.from_intWord_to_signal(word_voltage_obj1.get_speed(), word_2,0.0)
    word_voltage_obj1.graph_words((ts,vs))

    word_3 = 0b00000100001001000011000110100011
    ts, vs = word_voltage_obj1.from_intWord_to_signal(word_voltage_obj1.get_speed(), word_3,0.0)
    word_voltage_obj1.graph_words((ts,vs))

    word_voltage_obj2 = b2v(False)
    print(str(word_voltage_obj2))

    ts, vs = word_voltage_obj2.from_intWord_to_signal(word_voltage_obj2.get_speed(), word_1,0.0)
    word_voltage_obj2.graph_words((ts,vs))

    ts, vs = word_voltage_obj2.from_intWord_to_signal(word_voltage_obj2.get_speed(), word_2,0.0)
    word_voltage_obj2.graph_words((ts,vs))

    ts, vs = word_voltage_obj2.from_intWord_to_signal(word_voltage_obj2.get_speed(), word_3,0.0)
    word_voltage_obj2.graph_words((ts,vs))

def test_FMC_send_random_voltages():
    FMC_test1 = FMC("HiGh")
    FMC_test1.transmit_random_voltages()

def test_FMC_word_validation1():
    FMC_test2 = FMC("HIGh")
    word_1 = 0b11111111111111111111111111111111
    assert(FMC_test2.validate_word(word_1) == True)

def test_FMC_word_validation2():
    FMC_test2 = FMC("HIGh")
    word_1 = 0b11111111111111111111111111111110
    assert(FMC_test2.validate_word(word_1) == False)

def test_FMC_word_validation3():
    FMC_test2 = FMC("HIGh")
    word_1 = 0b11111101000000000000001000110000
    assert(FMC_test2.validate_word(word_1) == True)

def test_FMC_send_given_word1():
    FMC_test3 = FMC("lOW")
    given_word = 0b11111101000000000000001000110000
    FMC_test3.transmit_given_word(given_word)

def test_FMC_send_given_word2():
    FMC_test3 = FMC("lOW")
    given_word = 0b00000000000000000000000000000011
    FMC_test3.transmit_given_word(given_word)

def test_FMC_send_given_word3():
    FMC_test3 = FMC("high")
    given_word = 0b11111111111111111111111111111111
    FMC_test3.transmit_given_word(given_word)

def test_FMC_send_multiple_given_words():
    FMC_test4 = FMC("high")
    given_word1 = 0b11111101000000000000001000110000
    given_word2 = 0b00000000000000000000000000000011
    given_word3 = 0b11111111111111111111111111111111

    words = [given_word1, given_word2, given_word3]

    print('\n')
    time.sleep(1) # to show diff between FMC waking up and TX'd voltages.

    for word in words:
        FMC_test4.transmit_given_word(word)

def test_FMC_pilot_input():
    FMC_test5 = FMC("HIGH")
    FMC_test5.transmit_pilot_input()

def test_bus_queue():
    print("You need to be using IDLE for this")
    word_voltage_obj = b2v(hl_speed = True)
    channel_a = ARINC429BUS()

    # TX random voltages thread -> probably will be good as template for TXrs
    def generate_voltage_data(ARINC_Channel):
        while(True):
            usec_start = time.time()*1_000_000
            word = random.randint(0, 0b11111111111111111111111111111111)
            ts, vs = word_voltage_obj.from_intWord_to_signal(hl_speed = word_voltage_obj.get_speed(),
                                                             word = word,
                                                             usec_start = usec_start)
            for voltage in vs:
                ARINC_Channel.add_voltage(voltage)
                time.sleep(5e-7)

    # Start the TXr transmission in thread
    transmitter_thread = Thread(target=generate_voltage_data, args=(channel_a,))
    transmitter_thread.start()
    # Start the real-time visualization in a separate thread
    visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,))
    visualization_thread.start()
    #time.sleep(0.33)

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    visualization_thread.join()

#channel_a.queue_visual()

if __name__ == "__main__":
    main()
