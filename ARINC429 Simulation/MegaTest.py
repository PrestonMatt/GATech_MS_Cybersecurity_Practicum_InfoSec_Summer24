# Standard Libraries
import time
import random
import pytest
from threading import Thread
import matplotlib.pyplot as plt
# Preston's libraries hehe
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_RMS_Simulator import radio_management_system as RMS
from LRU_FAEC_Simulator import full_authority_engine_control as FAEC
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
def test_all():

    test_FMC_word_validation1()
    test_FMC_word_validation2()
    test_FMC_word_validation3()

    test_RX_label_fetch1()
    test_RX_label_fetch2()
    test_RX_label_fetch3()
    test_RX_label_fetch4()
    test_RX_label_fetch5()
    test_TX_label_reverser1()
    test_TX_label_reverser2()
    test_TX_label_reverser3()
    test_TX_label_reverser4()
    test_TX_label_reverser5()
    test_RMS_Test_Static1()
    test_RMS_Test_latitudedecode_BCD()
    test_RMS_Test_longitudedecode_BCD()
    test_RMS_flight_number()
    test_RMS_ground_speed_BCD()
    test_RMS_track_speed_BCD()
    test_RMS_vert_speed_BCD()
    test_RMS_heading_BCD()
    test_RMS_altitude_BCD()
    test_RMS_ICAO()
    test_RMS_ADF()
    test_RMS_DME1()
    test_RMS_DME2()
    test_RMS_DME3()
    test_RMS_DME4()
    test_RMS_VOR_ILS_freq1()
    test_RMS_VOR_ILS_freq2()
    test_RMS_gen_freq()
    test_RMS_SetHFCOMM_Freq()
    test_RMS_HF_COM_tune()
    test_GPS_setup()
    test_GPS_latlon_update()
    test_GPS_digit_translate_update()
    test_GPS_word_maker()
    test_all_FAECs()
    test_all_ADIRUs()
    test_all_IDS_tests()

def test_all_non_asserts():
    #test_voltage_sim()
    #test_graph_lat_word_HS()
    #test_graph_lat_word_LS()
    #test_graph_3_words()
    #test_intWord_to_voltage()

    #test_FMC_pilot_input()
    #test_bus_queue_TX()
    test_bus_queue_RX()
    #test_FMC_TX()
    #test_FMC_TX()
    #test_GPS_comm()
    #test_RX_Helper1()
    #test_RX_Helper2()
    #test_RX_Helper3()

    pass

# Runs all voltage simulator tests. No assert.
def test_voltage_sim():
    word_voltage_obj = b2v(True)
    print(str(word_voltage_obj))
    word_voltage_obj.test_all_functions()

# Shows graphs for various words. No assert.
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

# Tests voltage set generation for the latitude send. No Assert.
def test_graph_lat_word_HS():
    word_voltage_obj = b2v(True)
    word_1 = 0b00010000000100110011010101011100
    ts, vs = word_voltage_obj.from_intWord_to_signal(word_voltage_obj.get_speed(), word_1,0.0)
    word_voltage_obj.graph_words((ts,vs), tickrate=30,figtitle="Word for N 75 Deg 59.9'")

# Tests voltage set generation for the latitude send. No Assert.
def test_graph_lat_word_LS():
    word_voltage_obj = b2v(False)
    word_1 = 0b00010000000100110011010101011100
    ts, vs = word_voltage_obj.from_intWord_to_signal(word_voltage_obj.get_speed(), word_1,0.0)
    word_voltage_obj.graph_words((ts,vs),tickrate=300, figtitle="Word for N 75 Deg 59.9'")

# Tests voltage set generation for 3 words. No assert.
def test_graph_3_words():
    word_voltage_obj = b2v(True)
    ts, vs = word_voltage_obj.generate_n_random_words(True, n=3)
    word_voltage_obj.graph_words((ts,vs),tickrate=300, figtitle="3 random words.")

# Tests FMC sending rando voltages. No assert.
def test_FMC_send_random_voltages():
    FMC_test1 = FMC("HiGh")
    FMC_test1.transmit_random_voltages()

# Tests word validation function.
def test_FMC_word_validation1():
    FMC_test2 = FMC("HIGh",BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    word_1 = 0b11111111111111111111111111111111
    assert(FMC_test2.validate_word(word_1) == True)

# Tests word validation function.
def test_FMC_word_validation2():
    FMC_test2 = FMC("HIGh", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    word_1 = 0b11111111111111111111111111111110
    assert(FMC_test2.validate_word(word_1) == False)

# Tests word validation function.
def test_FMC_word_validation3():
    FMC_test2 = FMC("HIGh", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    word_1 = 0b11111101000000000000001000110000
    assert(FMC_test2.validate_word(word_1) == True)

# Tests sending a given word from TX FMC. No assert.
def test_FMC_send_given_word1():
    FMC_test3 = FMC("lOW", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    given_word = 0b11111101000000000000001000110000
    FMC_test3.transmit_given_word(given_word)

# Tests sending a given word from TX FMC. No assert.
def test_FMC_send_given_word2():
    FMC_test3 = FMC("lOW", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    given_word = 0b00000000000000000000000000000011
    FMC_test3.transmit_given_word(given_word)

# Tests sending a given word from TX FMC. No assert.
def test_FMC_send_given_word3():
    FMC_test3 = FMC("high", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    given_word = 0b11111111111111111111111111111111
    FMC_test3.transmit_given_word(given_word)

# Tests sending a few given words from TX FMC. No assert.
def test_FMC_send_multiple_given_words():
    FMC_test4 = FMC("high", BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS(),ARINC429BUS(),ARINC429BUS()])
    given_word1 = 0b11111101000000000000001000110000
    given_word2 = 0b00000000000000000000000000000011
    given_word3 = 0b11111111111111111111111111111111

    words = [given_word1, given_word2, given_word3]

    print('\n')
    time.sleep(1) # to show diff between FMC waking up and TX'd voltages.

    for word in words:
        FMC_test4.transmit_given_word(word)

# Tests sending words from Pilot input from TX FMC. No assert.
def test_FMC_pilot_input():
    channel_a = ARINC429BUS()
    FMC_test5 = FMC("HIGH",fifo_len=5,BUS_CHANNELS = [channel_a])

    def pilot_thread(FMC_test5):
        FMC_test5.pilot_input()

    # Start the pilot input thread:
    pilot_thread = Thread(target=pilot_thread, args=(FMC_test5,))
    pilot_thread.start()
    #FMC_test5.visualize_FMC_transmissions(channel_a)

    visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005))
    visualization_thread.start()

    # Join threads to main thread keeping simulation running
    visualization_thread.join()
    pilot_thread.join()

# Tests FMC ability to send data. No assert.
def test_bus_queue_TX():
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
    visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005))
    visualization_thread.start()
    #time.sleep(0.33)

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    visualization_thread.join()

# Tests FMC ability to send and recieve data. No assert.
def test_bus_queue_RX():
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
                time.sleep(0.05)

    def recieve_voltage_data(ARINC_Channel):
        vs = [0.0 for x in range(100)]
        # interactive plot
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'go--')
        fig.suptitle("Receive Data")

        ax.set_xlim(100)
        ax.set_ylim(-14, 14) # within spec
        while(True):
            vs.append(ARINC_Channel.get_all_voltage()[0])

            line.set_xdata(range(100))
            line.set_ydata(vs[-101:-1])

            ax.set_xlim(0, max(100, 1))

            fig.canvas.draw()
            fig.canvas.flush_events()

            #time.sleep(0.000005)

    # Start the TXr transmission in thread
    transmitter_thread = Thread(target=generate_voltage_data, args=(channel_a,))
    transmitter_thread.start()

    # Start the receiver in a separate thread
    receiver_thread = Thread(target=recieve_voltage_data, args=(channel_a,))
    receiver_thread.start()

    # Start the real-time visualization in a separate thread
    visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005,"Transmit Data"))
    visualization_thread.start()

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    receiver_thread.join()
    visualization_thread.join()

# Tests FMC ability to random send data. No assert.
def test_FMC_TX():
    Channel_A = ARINC429BUS()
    FMC_test6 = FMC("HIGH", BUS_CHANNELS=[Channel_A])

    # FMC Random Word Thread:
    txer_thread = Thread(target=FMC_test6.transmit_random_voltages, args=(0,) )
    txer_thread.start()

    # FMC build in visualization:
    FMC_test6.visualize_FMC_transmissions(Channel_A)

    txer_thread.join()

# TODO: Impliment GPS and use this test.
def test_GPS_comm():
    GPS_test1 = GPS("HIGH")
    GPS_test1.communicate_to_bus()

# Tests RX helper class ability to receive Low Speed bus data. No assert.
def test_RX_Helper1():
    print("You need to be using IDLE for this")
    word_voltage_obj = b2v(hl_speed = False)
    channel_a = ARINC429BUS()
    def generate_voltage_data(ARINC_Channel):
        while(True):
            usec_start = time.time()*1_000_000
            word = random.randint(0, 0b11111111111111111111111111111111)
            ts, vs = word_voltage_obj.from_intWord_to_signal(hl_speed = word_voltage_obj.get_speed(),
                                                             word = word,
                                                             usec_start = usec_start)
            for voltage in vs:
                ARINC_Channel.add_voltage(voltage)
                time.sleep(0.05)

    def recieve_voltage_data(ARINC_Channel):
        reciever_chip = lru_rxr(bus_speed = "low", BUS_CHANNELS = [ARINC_Channel])
        reciever_chip.visualize_LRU_receiveds(ARINC_Channel)

    # Start the TXr transmission in thread
    transmitter_thread = Thread(target=generate_voltage_data, args=(channel_a,))
    transmitter_thread.start()

    # Start the receiver in a separate thread
    receiver_thread = Thread(target=recieve_voltage_data, args=(channel_a,))
    receiver_thread.start()

    # Start the real-time visualization in a separate thread
    visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005,"Transmit Data"))
    visualization_thread.start()

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    receiver_thread.join()
    visualization_thread.join()

# Tests RX helper class ability to receive Low Speed bus data and convert it to a word. No assert.
def test_RX_Helper2():
    print("You need to be using IDLE for this")
    word_voltage_obj = b2v(hl_speed = False)
    channel_a = ARINC429BUS()
    def generate_voltage_data(ARINC_Channel):
        while(True):
            usec_start = time.time()*1_000_000
            word = random.randint(0, 0b11111111111111111111111111111111)
            cont = input(f"Transmitting given word:{bin(word)}")
            ts, vs = word_voltage_obj.from_intWord_to_signal(hl_speed = word_voltage_obj.get_speed(),
                                                             word = word,
                                                             usec_start = usec_start)
            for voltage in vs:
                ARINC_Channel.add_voltage(voltage)
                time.sleep(0.005)

    def recieve_voltage_data(ARINC_Channel):
        reciever_chip = lru_rxr(bus_speed = "low", BUS_CHANNELS = [ARINC_Channel])
        #reciever_chip.visualize_LRU_receiveds(ARINC_Channel)
        print(f"RECIEVED WORD AS INT: {reciever_chip.receive_given_word(0)}")

    # Start the TXr transmission in thread
    transmitter_thread = Thread(target=generate_voltage_data, args=(channel_a,))
    transmitter_thread.start()

    # Start the receiver in a separate thread
    receiver_thread = Thread(target=recieve_voltage_data, args=(channel_a,))
    receiver_thread.start()

    # Start the real-time visualization in a separate thread
    #visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005,"Transmit Data"))
    #visualization_thread.start()

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    receiver_thread.join()
    #visualization_thread.join()

# TODO: Use this test to fix the high speed get voltage function and actually RX words.
def test_RX_Helper3():
    print("You need to be using IDLE for this")
    word_voltage_obj = b2v(hl_speed = True)
    channel_a = ARINC429BUS()
    def generate_voltage_data(ARINC_Channel):
        while(True):
            usec_start = time.time()*1_000_000
            word = random.randint(0, 0b11111111111111111111111111111111)
            cont = input(f"Transmitting given word:{bin(word)}")
            ts, vs = word_voltage_obj.from_intWord_to_signal(hl_speed = word_voltage_obj.get_speed(),
                                                             word = word,
                                                             usec_start = usec_start)
            for voltage in vs:
                ARINC_Channel.add_voltage(voltage)
                time.sleep(0.005)

    def recieve_voltage_data(ARINC_Channel):
        reciever_chip = lru_rxr(bus_speed = "high", BUS_CHANNELS = [ARINC_Channel])
        #reciever_chip.visualize_LRU_receiveds(ARINC_Channel)
        print(f"RECIEVED WORD AS INT: {reciever_chip.receive_given_word(0)}")

    # Start the TXr transmission in thread
    transmitter_thread = Thread(target=generate_voltage_data, args=(channel_a,))
    transmitter_thread.start()

    # Start the receiver in a separate thread
    receiver_thread = Thread(target=recieve_voltage_data, args=(channel_a,))
    receiver_thread.start()

    # Start the real-time visualization in a separate thread
    #visualization_thread = Thread(target=ARINC429BUS.queue_visual, args=(channel_a,0.005,"Transmit Data"))
    #visualization_thread.start()

    # Join threads to main thread keeping simulation running
    transmitter_thread.join()
    receiver_thread.join()
    #visualization_thread.join()

# Tests ability for RX helper to parse a label from a word.
def test_RX_label_fetch1():
    label_1 = "11111111000000001111111100000000"
    RX_Helper = lru_rxr()
    assert(0b11111111 == RX_Helper.get_label_from_word(int(label_1,2)))

# Tests ability for RX helper to parse a label from a word.
def test_RX_label_fetch2():
    label_1 = "10100101000000001111111100000000"
    RX_Helper = lru_rxr()
    assert(0b10100101 == RX_Helper.get_label_from_word(int(label_1,2)))

# Tests ability for RX helper to parse a label from a word.
def test_RX_label_fetch3():
    label_1 = "00000000111111110000000011111111"
    RX_Helper = lru_rxr()
    assert(0b00000000 == RX_Helper.get_label_from_word(int(label_1,2)))

# Tests ability for RX helper to parse a label from a word.
def test_RX_label_fetch4():
    label_1 = "00110101000000001111111100000000"
    RX_Helper = lru_rxr()
    # 00110101 reversed
    assert(0b10101100 == RX_Helper.get_label_from_word(int(label_1,2)))

# Tests ability for RX helper to parse a label from a word.
def test_RX_label_fetch5():
    label_1 = "00000001000000001111111100000000"
    RX_Helper = lru_rxr()
    # 00110101 reversed
    assert(0b10000000 == RX_Helper.get_label_from_word(int(label_1,2)))

# Tests ability for TX helper to pack a label into a word.
def test_TX_label_reverser1():
    label = 0o066
    # 00 110 110
    # 1&2 = 00
    # 34&5 = 110
    # 67&8 = 110
    # 00110110 -> 01101100
    # print(bin(label))
    # -> "00110110"
    tx_chip = lru_txr()
    assert("01101100" == tx_chip.make_label_for_word(label)[0])

# Tests ability for TX helper to pack a label into a word.
def test_TX_label_reverser2():
    label = 0o010
    # print(bin(label))
    # -> "00001000"
    tx_chip = lru_txr()
    assert("00001000"[::-1] == tx_chip.make_label_for_word(label)[0])

# Tests ability for TX helper to pack a label into a word.
def test_TX_label_reverser3():
    label = 0o011
    # print(bin(label))
    # -> "00001001"
    tx_chip = lru_txr()
    assert("00001001"[::-1] == tx_chip.make_label_for_word(label)[0])

# Tests ability for TX helper to pack a label into a word.
def test_TX_label_reverser4():
    label = 0o210
    # print(bin(label))
    # -> "10001000"
    tx_chip = lru_txr()
    assert("10001000"[::-1] == tx_chip.make_label_for_word(label)[0])

# Tests ability for TX helper to pack a label into a word.
def test_TX_label_reverser5():
    label = 0o320
    print(bin(label))
    # -> "11010000"
    tx_chip = lru_txr()
    assert("11010000"[::-1] == tx_chip.make_label_for_word(label)[0])

# Tests ability for TX helper to pack all possible labels into a word.
def test_TX_label_reverser_all():
    tx_chip = lru_txr()
    for x in range(0o000, 0o377):
        label = x
        label = bin(label)[2:]
        label = "0"*(8-len(label)) + label
        label = label[::-1]
        #print(label)
        assert(label == tx_chip.make_label_for_word(x)[0])

# Tests ability for RX helper to parse all possible labels from a word.
def test_RX_label_fetchall():
    rx_chip = lru_rxr()
    tx_chip = lru_txr()
    for x in range(0o000, 0o377):
        txd_label = tx_chip.make_label_for_word(x)[0]
        word = txd_label + "0"*24
        word_int = int(word, 2)
        rxd_label = rx_chip.get_label_from_word(word_int)
        #print(label)
        assert(rxd_label == x)

# Tests default RMS stand up.
def test_RMS_Test_Static1():
    print("\n")
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    print("Default RMS Bootup Status.")
    assert str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
        str({"Flight Number": None,
             "Latitude": None,
             "Longitude": None,
             "Altitude": None,
             "Ground Speed": None,
             "Vertical Speed": None,
             "Track Angle": None,
             "Magnetic Heading": None,
             "Emergency Status": "Normal Operations",
             "Ident Switch": False,
             "ICAO Address": None,
             "Aircraft Type": "Civilian"})

# Tests RMS BCD of Lat data for ADS-B.
def test_RMS_Test_latitudedecode_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o010))
    data = "1001" + "1001" + "1010" + "1010" + "1110" + "0" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": "N 75 Deg 59.9'",
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of Lon data for ADS-B.
def test_RMS_Test_longitudedecode_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o011))
    data = "0001" + "1010" + "0100" + "1001" + "0110" + "1" + "11" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": "W 169 Deg 25.8'",
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS flight # for ADS-B.
def test_RMS_flight_number():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o261))
    data = "00" + "000" + "1110" + "1000" + "1000" + "0000" + "00"
    par_bit = tx_chip.calc_parity(label+data)
    data += par_bit
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # 117
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": 117,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of ground speed for ADS-B.
def test_RMS_ground_speed_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o012))
    data = "00" + \
           "0000" + \
            "0000" + "1010" + "0110" + "000" + "00" + "1" #"PPPP" -> middle 0s
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": 650,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BNR of ground speed for ADS-B.
def test_RMS_ground_speed_BNR():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o312))
    data = "00" + "000000010100010100" + "011" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": 650,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of track speed for ADS-B.
def test_RMS_track_speed_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o013))
    data = "00" + "0000" + "1010" + "1010" + "0110" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": 165.5,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of vert speed for ADS-B.
def test_RMS_vert_speed_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o020))
    data = "00" + "0000" + "0000" + "0000" + "0100" + "010" + "11" + "0"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": -2200,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of heading for ADS-B.
def test_RMS_heading_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o023))
    data = "00" + "0000" + "0000" + "1110" + "1110" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": 177,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BCD of altitude for ADS-B.
def test_RMS_altitude_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o025))
    data = "00" + "0000" + "0000" + "0000" + "1000" + "001" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": 41000,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# TODO figure out what this word decodes to?
# Tests RMS BNR of heading for ADS-B.
def test_RMS_heading_BNR():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o101))
    data = "00" + "000000" + "101010101011" + "011" + "0"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": 150,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BNR of altitude label code 1 for ADS-B.
def test_RMS_altitude_BNR1():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o102))
    data = "00" + "00" + "0001010000000101" + "011" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": 41000,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# Tests RMS BNR of altitude label code 2 for ADS-B.
def test_RMS_altitude_BNR2():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o203))
    data = "00" + "0" + "00010011111101010" + "011" + "0"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": 45000,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# TODO figure out what this word decodes to?
# Tests RMS BNR of lat label code 2 for ADS-B.
def test_RMS_lat_BNR():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o310))
    data = "00" + "010101011111001110" + "011" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": "N 81.5 Deg",
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# TODO figure out what this word decodes to?
# Tests RMS BNR of lat label code 2 for ADS-B.
def test_RMS_lon_BNR():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o311))
    data = "00" + "000011011010001110" + "011" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": "W 100.25",
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

# TODO figure out what this word decodes to?
# Tests RMS BNR of lat label code 2 for ADS-B.
def test_RMS_vertspeed_BNR():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o104))
    data = "00" + "00000000" + "0110111011" + "111" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": "W 100.25",
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": -2200,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": None,
                "Aircraft Type": "Civilian"}))

def test_RMS_ICAO():
    print("\n")
    ICAO = bin(0b101011001001011100100110)[2:]
    print(0b101011001001011100100110)
    #print(len(ICAO))
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label1, _ = tx_chip.make_label_for_word(int(0o214))
    data1 = "00" + "0000000" + ICAO[0:12] + "11" + "1"
    #print(len(data))
    word1 = label1 + data1
    label2, _ = tx_chip.make_label_for_word(int(0o216))
    data2 = "00" + "0000000" + ICAO[12:] + "11" + "1"
    #print((label2+data2)[17:29])
    word2 = label2 + data2
    RMS_test1.decode_word(word1)
    RMS_test1.decode_word(word2)
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tADF:0.0\n\tVOR:0.0\n\tILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": None,
                "Longitude": None,
                "Altitude": None,
                "Ground Speed": None,
                "Vertical Speed": None,
                "Track Angle": None,
                "Magnetic Heading": None,
                "Emergency Status": "Normal Operations",
                "Ident Switch": False,
                "ICAO Address": 0b101011001001011100100110,
                "Aircraft Type": "Civilian"}))

def test_RMS_ADF():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o032))
    data = "00" + "0" + "0" + "0" + "1" + "1110" + "1010" + "0000" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.ADF_freq == 1057.5)

# Tests DME function for MLS frequency set.
def test_RMS_DME1():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o035))
    data = "00" + "000" + "0" + "1" + "01" + "1" + "0110" + "1010" + "100" + "00" + "0"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.DME_Frequency == 5046.65)

# Tests DME function for VOR frequency set.
def test_RMS_DME2():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o035))
    data = "00" + "000" + "0" + "0" + "00" + "0" + "0110" + "1010" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.VOR_Frequency == 15.60)

# Tests DME function for ILR frequency set.
def test_RMS_DME3():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o035))
    data = "00" + "000" + "1" + "0" + "10" + "1" + "1110" + "1010" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    #print(word[13:15])
    RMS_test1.decode_word(word)
    assert(RMS_test1.ILS_Frequency == 15.75)

# Check instead that IDENT was turned on.
def test_RMS_DME4():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o035))
    data = "00" + "000" + "0" + "0" + "01" + "1" + "0110" + "1010" + "100" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.ADS_B_Message["Ident Switch"] == True)

# Tests VOR label to set VOR freq.
def test_RMS_VOR_ILS_freq1():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o034))
    data = "00" + "000" + "0" + "0000" + "1100" + "1001" + "000" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.VOR_Frequency == 9.30)

# Tests VOR label to set VOR freq.
def test_RMS_VOR_ILS_freq2():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o034))
    data = "00" + "000" + "1" + "0000" + "1100" + "1001" + "000" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.ILS_Frequency == 9.30)

# Test general freq for RMS.
def test_RMS_gen_freq():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o033))
    data = "00" + "000" + "1" + "0000" + "1100" + "1001" + "000" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.frequency == 9.30)

# Test HFComm freq for RMS.
def test_RMS_SetHFCOMM_Freq():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o037))
    data = "01" + "0" + "1001" + "1110" + "1010" + "1100" + "01" + "00" + "1"
    #print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    assert(RMS_test1.HF_COM_Frequency == 23.579)

# Test HF Comm inc for RMS.
def test_RMS_HF_COM_tune():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])

    label1, _ = tx_chip.make_label_for_word(int(0o037))
    data1 = "01" + "0" + "1001" + "1110" + "1010" + "1100" + "01" + "00" + "1"
    #print(len(data))
    word1 = label1 + data1
    RMS_test1.decode_word(word1)

    label2, _ = tx_chip.make_label_for_word(int(0o205))
    data2 = "00" + "1" + "00000000000000" + "0010" + "00" + "0"
    #print(len(data))
    word2 = label2 + data2
    RMS_test1.decode_word(word2)

    assert(RMS_test1.HF_COM_Frequency == (23.579 + 0.4))

# Tests default GPS Set up
def test_GPS_setup():
    print("\n")
    Orange_Channel = ARINC429BUS()
    GPS_test1 = GPS("low", Orange_Channel, lat='N 75 Deg 59.9\'', lon='W 169 Deg 25.8\'')
    assert(str(GPS_test1) == "Current latitude: N 75 Deg 59.9'\nCurrent longitude: W 169 Deg 25.8'\nBus Channel: ARINC429 Bus Object and Speed: low")

# Tests GPS ability to update position.
def test_GPS_latlon_update():
    print("\n")
    Orange_Channel = ARINC429BUS()
    GPS_test1 = GPS("low", Orange_Channel, lat='N 75 Deg 59.9\'', lon='W 169 Deg 25.8\'')
    GPS_test1.determine_next_position()
    GPS_test1.determine_next_position()
    GPS_test1.determine_next_position()
    assert(str(GPS_test1) == "Current latitude: N 75 Deg 60.2'\nCurrent longitude: W 169 Deg 26.1'\nBus Channel: ARINC429 Bus Object and Speed: low")

# Test GPS ability to translate the digit data into binary for word.
def test_GPS_digit_translate_update():
    print("\n")
    Orange_Channel = ARINC429BUS()
    GPS_test1 = GPS("low", Orange_Channel, lat='N 75 Deg 59.9\'', lon='W 169 Deg 25.8\'')
    latdigi = GPS_test1.from_digits_to_data("75","59.9")
    londigi = GPS_test1.from_digits_to_data("169","25.8")
    assert(latdigi == "100110011010101011100")
    assert(londigi == "000110100100100101101")

# Test GPS ability to make words based on lat and lon data.
def test_GPS_word_maker():
    print("\n")
    Orange_Channel = ARINC429BUS()
    GPS_test1 = GPS("low", Orange_Channel, lat='N 75 Deg 59.9\'', lon='W 169 Deg 25.8\'')

    lat_word, lon_word = GPS_test1.from_lat_lon_to_word()
    lat_word = "0"*(32-len(bin(lat_word)[2:])) + bin(lat_word)[2:]
    lon_word = "0"*(32-len(bin(lon_word)[2:])) + bin(lon_word)[2:]

    RMS_test2 = RMS("low",[Orange_Channel])
    print(f"Latitude word:{lat_word}")
    print(f"Longitude word:{lon_word}")
    RMS_test2.decode_word(lat_word)
    RMS_test2.decode_word(lon_word)

    assert(RMS_test2.ADS_B_Message["Latitude"] == 'N 75 Deg 59.9\'')
    assert(RMS_test2.ADS_B_Message["Longitude"] == 'W 169 Deg 25.8\'')

    #latdigi = GPS_test1.from_digits_to_data("75","59.9")
    #londigi = GPS_test1.from_digits_to_data("169","25.8")
    #assert(latdigi == "100110011010101011100")
    #assert(londigi == "000110100100100101101")

def test_FAEC_default():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()

    FAEC_test1 = FAEC("low","riGHt",BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])
    assert(str(FAEC_test1) == f'Engine Serial Number: 0\nOn right wing\n0o114 data: Selected Ambient Static Pressure\n0o127 data: Fan Discharge Static Pressure\n0o130 data: Selected Total Air Temperature\n0o133 data: Selected Throttle Lever Angle\n0o134 data: Throttle Lever Angle\n0o137 data: Selected Thrust Reverser Position\n0o155 data: Maintenance Data #6\n0o156 data: Maintenance Data #7\n0o157 data: Maintenance Data #8\n0o160 data: Maintenance Data #9\n0o161 data: Maintenance Data #10\n0o203 data: Ambient Static Pressure\n0o205 data: Mach Number\n0o211 data: Total Fan Inlet Temperature\n0o244 data: Fuel Mass Flow\n0o260 data: LP Turbine Discharge Temperature\n0o261 data: LP Turbine Inlet Pressure\n0o262 data: HP Compressor Inlet Total Pressure\n0o263 data: Selected Compressor Inlet Temperature (Total)\n0o264 data: Selected Compressor Discharge Temperature\n0o265 data: Selected Compressor Discharge Temperature\n0o267 data: HP Compressor Inlet Temperature (Total)\n0o300 data: ECU Internal Temperature\n0o301 data: Demanded Fuel Metering Valve Position\n0o302 data: Demanded Variable Stator Vane Position\n0o303 data: Demanded Variable Bleed Valve Position\n0o304 data: Demanded HPT Clearance Valve Position\n0o305 data: Demanded LPT Clearance Valve Position\n0o316 data: Engine Oil Temperature\n0o321 data: Exhaust gas Temperature (Total)\n0o322 data: Total Compressor Discharge Temperature\n0o323 data: Variable Stator Vane Position\n0o324 data: Selected Fuel Metering Valve Position\n0o325 data: Selected Fuel Metering Vane Position\n0o327 data: Compressor Discharge Static Pressure\n0o330 data: Fuel Metering Valve Position\n0o331 data: Selected HPT Clearance Valve Postion\n0o335 data: Selected Variable Bleed Valve Position\n0o336 data: Variable Bleed Value Position\n0o337 data: HPT Clearance Valve Position\n0o341 data: Command Fan Speed\n0o342 data: Maximum Allowed Fan Speed\n0o343 data: Maximum Allowed Fan Speed\n0o344 data: Selected Actual Core Speed\n0o345 data: Selected Exhaust Gas Temperature (Total)\n0o346 data: Selected Actual Fan Speed\n0o347 data: LPT Clearance Valve Position\n0o360 data: Throttle Rate of Change\n0o361 data: Derivative of Thrust vs. N1\n0o363 data: Corrected Thrust\n0o372 data: Actual Fan Speed\n0o373 data: Actual Core Speed\n0o374 data: Left Thrust Reverser Position\n0o375 data: Right Thrust Reverser Position')

def test_FAEC_serial_LSB():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt",BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    label, _ = tx_chip.make_label_for_word(0o046)
    data = "00" + "0000" + "1001" + "0010" + "0110" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word = label + data
    FAEC_lsbtest.decode_word(word)

    assert(FAEC_lsbtest.serial_no == int("000649"))

def test_FAEC_serial_MSB():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt",BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    label, _ = tx_chip.make_label_for_word(0o047)
    data = "00" + "0000" + "0100" + "1100" + "0000" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word = label + data
    FAEC_lsbtest.decode_word(word)

    assert(FAEC_lsbtest.serial_no == int("032000"))

def test_FAEC_full_serial_1():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt",BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    # Send MSB first
    label1, _ = tx_chip.make_label_for_word(0o047)
    data1 = "00" + "0000" + "0100" + "1100" + "0000" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word1 = label1 + data1
    FAEC_lsbtest.decode_word(word1)

    # Send LSB second
    label2, _ = tx_chip.make_label_for_word(0o046)
    data2 = "00" + "0000" + "1001" + "0010" + "0110" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word2 = label2 + data2
    FAEC_lsbtest.decode_word(word2)

    assert(FAEC_lsbtest.serial_no == int("032649"))

def test_FAEC_full_serial_2():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt",BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    # Send LSB first
    label2, _ = tx_chip.make_label_for_word(0o046)
    data2 = "00" + "0000" + "1001" + "0010" + "0110" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word2 = label2 + data2
    FAEC_lsbtest.decode_word(word2)

    # Send MSB second
    label1, _ = tx_chip.make_label_for_word(0o047)
    data1 = "00" + "0000" + "0100" + "1100" + "0000" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word1 = label1 + data1
    FAEC_lsbtest.decode_word(word1)

    assert(FAEC_lsbtest.serial_no == int("032649"))

def test_FAEC_full_serial_3():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt", serial_no=123456, BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    # Send LSB first
    label2, _ = tx_chip.make_label_for_word(0o046)
    data2 = "00" + "0000" + "1001" + "0010" + "0110" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word2 = label2 + data2
    FAEC_lsbtest.decode_word(word2)

    # Send MSB second
    label1, _ = tx_chip.make_label_for_word(0o047)
    data1 = "00" + "0000" + "0100" + "1100" + "0000" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word1 = label1 + data1
    FAEC_lsbtest.decode_word(word1)

    assert(FAEC_lsbtest.serial_no == int("032649"))

def test_FAEC_full_serial_4():
    print("\n")
    Purple_Channel_A = ARINC429BUS()
    Green_Channel_B = ARINC429BUS()
    tx_chip = lru_txr()
    FAEC_lsbtest = FAEC("low","riGHt", serial_no=123456, BUS_CHANNELS=[Purple_Channel_A,Green_Channel_B])

    # Send MSB first
    label1, _ = tx_chip.make_label_for_word(0o047)
    data1 = "00" + "0000" + "0100" + "1100" + "0000" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word1 = label1 + data1
    FAEC_lsbtest.decode_word(word1)

    # Send LSB second
    label2, _ = tx_chip.make_label_for_word(0o046)
    data2 = "00" + "0000" + "1001" + "0010" + "0110" + "000" + "00" + "1"
    #assert(len(data) == 24)
    word2 = label2 + data2
    FAEC_lsbtest.decode_word(word2)

    assert(FAEC_lsbtest.serial_no == int("032649"))

def test_all_FAECs():
    test_FAEC_default()
    test_FAEC_serial_LSB()
    test_FAEC_serial_MSB()
    test_FAEC_full_serial_1()
    test_FAEC_full_serial_2()
    test_FAEC_full_serial_3()
    test_FAEC_full_serial_4()

def test_ADIRU_rx_GPS1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    GPS_test1 = GPS(bus_speed="low", channel=Orange_bus, lat='N 75 Deg 59.9\'', lon='W 169 Deg 25.8\'')
    word1, word2 = GPS_test1.from_lat_lon_to_word()

    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    word1str = bin(word1)[2:]
    word1str = "0" * (32 - len(word1str)) + word1str
    word2str = bin(word2)[2:]
    word2str = "0" * (32 - len(word2str)) + word2str

    #print(word1str)
    #print(word2str)

    ADIRU_test.decode_GPS_word(word1str)
    ADIRU_test.decode_GPS_word(word2str)

    ADIRU_str = str(ADIRU_test)
    lat_ADIRU_str = ADIRU_str.split(":")[1]
    lon_ADIRU_str = ADIRU_str.split(":")[2]

    #print(lat_ADIRU_str)
    #print(lon_ADIRU_str)

    assert(lat_ADIRU_str.__contains__("N 75 Deg 59.9'") == True)
    assert(lon_ADIRU_str.__contains__("W 169 Deg 25.8'") == True)

def test_ADIRU_rx_GPS2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    GPS_test1 = GPS(bus_speed="low", channel=Orange_bus)
    word1, word2 = GPS_test1.from_lat_lon_to_word()

    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    word1str = bin(word1)[2:]
    word1str = "0" * (32 - len(word1str)) + word1str
    word2str = bin(word2)[2:]
    word2str = "0" * (32 - len(word2str)) + word2str

    #print(word1str)
    #print(word2str)

    ADIRU_test.decode_GPS_word(word1str)
    ADIRU_test.decode_GPS_word(word2str)

    ADIRU_str = str(ADIRU_test)
    lat_ADIRU_str = ADIRU_str.split(":")[1]
    lon_ADIRU_str = ADIRU_str.split(":")[2]

    #print(lat_ADIRU_str)
    #print(lon_ADIRU_str)

    assert(lat_ADIRU_str.__contains__("N 42 Deg 21.0'") == True)
    assert(lon_ADIRU_str.__contains__("W 71 Deg 23.0'") == True)

# TODO Make the test values here something
def test_ADIRU_default_values():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    ADIRU_test.bootup_values()

    assert(str(ADIRU_test) == "")

def test_ADIRU_lat():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    # N 75 Deg 59.9'
    ADIRU_test.set_value('Present Position - Latitude',"N 75 Deg 59.9'")
    produced_word = ADIRU_test.encode_word(0o010)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o010))
    data = "1001" + "1001" + "1010" + "1010" + "1110" + "0" + "00" + "0"
    word = label + data

    assert(produced_word == word)

def test_ADIRU_lon():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    # W 169 Deg 25.8'
    ADIRU_test.set_value('Present Position - Longitude',"W 169 Deg 25.8'")
    produced_word = ADIRU_test.encode_word(0o011)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o011))
    data = "0001" + "1010" + "0100" + "1001" + "0110" + "1" + "11" + "0"
    word = label + data

    assert(produced_word == word)

def test_ADIRU_ground_speed():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Ground Speed',"6592 Knots")
    produced_word = ADIRU_test.encode_word(0o012)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001010
    label, _ = tx_chip.make_label_for_word(int(0o012))
    # 06592 Knots
    #               2              9              5               6             0             +
    data = "00" + "0010"[::-1] + "1001"[::-1] + "0101"[::-1] + "0110"[::-1] + "000"[::-1] + "00" + "1"
    word = label + data

    assert(produced_word == word)

def test_ADIRU_ground_speed_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Ground Speed',"10000 Knots")
        produced_word = ADIRU_test.encode_word(0o012)

def test_ADIRU_ground_speed_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Ground Speed',"-399 Knots")
        produced_word = ADIRU_test.encode_word(0o012)

def test_ADIRU_Track_Angle_True():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Track Angle - True',"273.6 Degrees")
    produced_word = ADIRU_test.encode_word(0o013)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o013))
    # 0273.6 Degrees
    #               6              3              7               2             0             +
    data = "00" + "0110"[::-1] + "0011"[::-1] + "0111"[::-1] + "0010"[::-1] + "000"[::-1] + "00" + "1"
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Track_Angle_True_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Track Angle - True',"400.0 Degrees")
        produced_word = ADIRU_test.encode_word(0o013)

def test_ADIRU_Track_Angle_True_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Track Angle - True',"-400.0 Degrees")
        produced_word = ADIRU_test.encode_word(0o013)

def test_ADIRU_Magnetic_Heading():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Magnetic Heading',"273.6 Degrees")
    produced_word = ADIRU_test.encode_word(0o014)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o014))
    # 0273.6 Degrees
    #               6              3              7               2             0             +
    data = "00" + "0110"[::-1] + "0011"[::-1] + "0111"[::-1] + "0010"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Magnetic_Heading_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Magnetic Heading',"400.0 Degrees")
        produced_word = ADIRU_test.encode_word(0o014)

def test_ADIRU_Magnetic_Heading_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Magnetic Heading',"-400.6 Degrees")
        produced_word = ADIRU_test.encode_word(0o014)

def test_ADIRU_Wind_Speed():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Wind Speed',"439 Knots")
    produced_word = ADIRU_test.encode_word(0o015)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o015))
    # 0273.6 Degrees
    #               9              3              4               0             0             +
    data = "00" + "1001"[::-1] + "0011"[::-1] + "0100"[::-1] + "0000"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Wind_Speed_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Speed',"800 Knots")
        produced_word = ADIRU_test.encode_word(0o015)

def test_ADIRU_Wind_Speed_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Speed',"-20.01 Knots")
        produced_word = ADIRU_test.encode_word(0o015)

def test_ADIRU_Wind_Direction_True():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Wind Direction - True',"355 Degrees")
    produced_word = ADIRU_test.encode_word(0o016)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o016))
    # 0273.6 Degrees
    #               5              5              3               0             0             +
    data = "00" + "0101"[::-1] + "0101"[::-1] + "0011"[::-1] + "0000"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Wind_Direction_True_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Direction - True',"1000 Degrees")
        produced_word = ADIRU_test.encode_word(0o016)

def test_ADIRU_Wind_Direction_True_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Direction - True',"-6 Degrees")
        produced_word = ADIRU_test.encode_word(0o016)

def test_ADIRU_True_Heading():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('True Heading',"342.1 Degrees")
    produced_word = ADIRU_test.encode_word(0o044)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o044))
    # 0273.6 Degrees
    #               1               2              4             3              0            -
    data = "00" + "0001"[::-1] + "0010"[::-1] + "0100"[::-1] + "0011"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_True_Heading_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('True Heading',"-80 Degrees")
        produced_word = ADIRU_test.encode_word(0o044)

def test_ADIRU_True_Heading_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('True Heading',"400.0 Degrees")
        produced_word = ADIRU_test.encode_word(0o044)

def test_ADIRU_Total_Air_Temperature():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Total Air Temperature',"-50 Degrees Celsius")
    produced_word = ADIRU_test.encode_word(0o231)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o231))
    # 0273.6 Degrees
    #               0               5              0             0              0            -
    data = "00" + "0000"[::-1] + "0101"[::-1] + "0000"[::-1] + "0000"[::-1] + "000"[::-1] + "11"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Total_Air_Temperature_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Total Air Temperature',"-80 Degrees Celsius")
        produced_word = ADIRU_test.encode_word(0o231)

def test_ADIRU_Total_Air_Temperature_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Total Air Temperature',"100 Degrees Celsius")
        produced_word = ADIRU_test.encode_word(0o231)

def test_ADIRU_Static_Air_Temperature():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Static Air Temperature',"-50 Degrees Celsius")
    produced_word = ADIRU_test.encode_word(0o233)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o233))
    # 0273.6 Degrees
    #               0               5              0             0              0            -
    data = "00" + "0000"[::-1] + "0101"[::-1] + "0000"[::-1] + "0000"[::-1] + "000"[::-1] + "11"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Static_Air_Temperature_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Static Air Temperature',"-80 Degrees Celsius")
        produced_word = ADIRU_test.encode_word(0o233)

def test_ADIRU_Static_Air_Temperature_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Static Air Temperature',"100 Degrees Celsius")
        produced_word = ADIRU_test.encode_word(0o233)

def test_ADIRU_Baro_Correction_mb_1_part1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (mb) #1',"872.8 mb")
    produced_word = ADIRU_test.encode_word(0o234)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o234))
    # 0273.6 Degrees
    #               8               2              7             8              0            +
    data = "00" + "1000"[::-1] + "0010"[::-1] + "0111"[::-1] + "1000"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_mb_1_part2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (mb) #1',"1022.8 mb")
    produced_word = ADIRU_test.encode_word(0o234)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o234))
    # 0273.6 Degrees
    #               8               2              2             0              1            +
    data = "00" + "1000"[::-1] + "0010"[::-1] + "0010"[::-1] + "0000"[::-1] + "001"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_mb_1_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (mb) #1',"80 mb")
        produced_word = ADIRU_test.encode_word(0o234)

def test_ADIRU_Baro_Correction_mb_1_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (mb) #1',"2000 mb")
        produced_word = ADIRU_test.encode_word(0o234)

def test_ADIRU_Baro_Correction_ins_Hg_1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (ins. Hg) #1',"26.431 Ins. Hg")
    produced_word = ADIRU_test.encode_word(0o235)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o235))
    # 0273.6 Degrees
    #               1               3              4             6              2            +
    data = "00" + "0001"[::-1] + "0011"[::-1] + "0100"[::-1] + "0110"[::-1] + "010"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_ins_Hg_1_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (ins. Hg) #1',"50 mb")
        produced_word = ADIRU_test.encode_word(0o235)

def test_ADIRU_Baro_Correction_ins_Hg_1_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (ins. Hg) #1',"3 mb")
        produced_word = ADIRU_test.encode_word(0o235)

def test_ADIRU_Baro_Correction_mb_2_part1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (mb) #2',"872.8 mb")
    produced_word = ADIRU_test.encode_word(0o236)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o236))
    # 0273.6 Degrees
    #               8               2              7             8              0            +
    data = "00" + "1000"[::-1] + "0010"[::-1] + "0111"[::-1] + "1000"[::-1] + "000"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_mb_2_part2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (mb) #2',"1022.8 mb")
    produced_word = ADIRU_test.encode_word(0o236)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o236))
    # 0273.6 Degrees
    #               8               2              2             0              1            +
    data = "00" + "1000"[::-1] + "0010"[::-1] + "0010"[::-1] + "0000"[::-1] + "001"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_mb_2_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (mb) #2',"80 mb")
        produced_word = ADIRU_test.encode_word(0o236)

def test_ADIRU_Baro_Correction_mb_2_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (mb) #2',"2000 mb")
        produced_word = ADIRU_test.encode_word(0o236)

def test_ADIRU_Baro_Correction_ins_Hg_2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Correction (ins. Hg) #2',"26.431 Ins. Hg")
    produced_word = ADIRU_test.encode_word(0o237)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o237))
    # 0273.6 Degrees
    #               1               3              4             6              2            +
    data = "00" + "0001"[::-1] + "0011"[::-1] + "0100"[::-1] + "0110"[::-1] + "010"[::-1] + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Correction_ins_Hg_2_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (ins. Hg) #2',"50 mb")
        produced_word = ADIRU_test.encode_word(0o237)

def test_ADIRU_Baro_Correction_ins_Hg_2_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Baro Correction (ins. Hg) #2',"3 mb")
        produced_word = ADIRU_test.encode_word(0o237)

def test_ADIRU_total_pressure():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Total Pressure',"1000 mb")
    produced_word = ADIRU_test.encode_word(0o242)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o242))
    # 1000 mb
    #     padding   # extra to make it 11 bits long # 1000 to binary
    num = "00000000" + "0"*(11 - len(bin(1000)[2:])) + bin(1000)[2:] # bin(1000) -> "01111101000"
    #            padding/1000  +
    data = "00" + num[::-1] + "00"
    print(len(label+data))
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_total_pressure_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Total Pressure',"2047 mb")
        produced_word = ADIRU_test.encode_word(0o242)

def test_ADIRU_IR_test1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('IR Test',"ON Test Mode")
    produced_word = ADIRU_test.encode_word(0o277)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o277))
    #       SDI      ON    SSM
    data = "00" + "0"*19 + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_IR_test2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('IR Test',"OFF Test Mode")
    produced_word = ADIRU_test.encode_word(0o277)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o277))
    #       SDI      ON    SSM
    data = "00" + "1"*19 + "00"
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_IR_test3():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('IR Test',"WAcKy Test Mode")
        produced_word = ADIRU_test.encode_word(0o277)

def test_ADIRU_Body_Pitch_Acceleration1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Pitch Acceleration',"54.123 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o052)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o052))
    #               padding  54.123 / 2 = 27.0615->bin(27016)
    partial_data = "0000" + "110100110110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Pitch_Acceleration2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Pitch Acceleration',"-37.864 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o052)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o052))
    #               padding  37.864 / 2 = 18.932->bin(18932)
    partial_data = "0000" + "100100111110100"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Pitch_Acceleration_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Pitch Acceleration',"-100.000 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o052)

def test_ADIRU_Body_Pitch_Acceleration_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Pitch Acceleration',"65.534 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o052)

def test_ADIRU_Body_Roll_Acceleration1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Roll Acceleration',"54.123 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o053)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o053))
    #               padding  54.123 / 2 = 27.0615->bin(27016)
    partial_data = "0000" + "110100110110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Roll_Acceleration2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Roll Acceleration',"-37.864 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o053)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o053))
    #               padding  37.864 / 2 = 18.932->bin(18932)
    partial_data = "0000" + "100100111110100"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Roll_Acceleration_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Roll Acceleration',"-100.000 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o053)

def test_ADIRU_Body_Roll_Acceleration_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Roll Acceleration',"65.534 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o053)

def test_ADIRU_Body_Yaw_Acceleration1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Yaw Acceleration',"54.123 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o054)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o054))
    #               padding  54.123 / 2 = 27.0615->bin(27016)
    partial_data = "0000" + "110100110110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Yaw_Acceleration2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Yaw Acceleration',"-37.864 Deg/Sec^2")
    produced_word = ADIRU_test.encode_word(0o054)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o054))
    #               padding  37.864 / 2 = 18.932->bin(18932)
    partial_data = "0000" + "100100111110100"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Yaw_Acceleration_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Yaw Acceleration',"-100.000 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o054)

def test_ADIRU_Body_Yaw_Acceleration_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Yaw Acceleration',"65.534 Deg/Sec^2")
        produced_word = ADIRU_test.encode_word(0o054)

def test_ADIRU_Cabin_Pressure1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Cabin Pressure',"2047.008 mB")
    produced_word = ADIRU_test.encode_word(0o152)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o152))
    #               padding  2048.008 / 8 = 255.876->bin(255876)
    partial_data = "0" + "111110011110000100"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Cabin_Pressure_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as pyE:
        ADIRU_test.set_value('Cabin Pressure',"2059.008 mB")
        produced_word = ADIRU_test.encode_word(0o152)

def test_ADIRU_Cabin_Pressure_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as pyE:
        ADIRU_test.set_value('Cabin Pressure',"-1.008 mB")
        produced_word = ADIRU_test.encode_word(0o152)

def test_ADIRU_Left_Static_Pressure_Uncorrected():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Left Static Pressure Uncorrected, mb',"2047.008 mB")
    produced_word = ADIRU_test.encode_word(0o176)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o176))
    #               padding  2048.008 / 8 = 255.876->bin(255876)
    partial_data = "0" + "111110011110000100"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Right_Static_Pressure_Uncorrected():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Right Static Pressure Uncorrected, mb',"2047.008 mB")
    produced_word = ADIRU_test.encode_word(0o177)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o177))
    #               padding  2048.008 / 8 = 255.876->bin(255876)
    partial_data = "0" + "111110011110000100"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_altitude_1013():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Altitude (1013.25mB)',"35242 feet")
    produced_word = ADIRU_test.encode_word(0o203)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o203))
    #               padding  bin(35242)
    partial_data = "00" + "01000100110101010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_altitude_1013_special_case():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Altitude (1013.25mB)',"131072 feet")
    produced_word = ADIRU_test.encode_word(0o203)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o203))
    #               padding  bin(35242)
    partial_data = "00" + "0"*17
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_altitude_1013_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as pyE:
        ADIRU_test.set_value('Altitude (1013.25mB)',"131073 feet")
        produced_word = ADIRU_test.encode_word(0o203)

def test_ADIRU_Baro_Corrected_Altitude1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Corrected Altitude #1',"35242 feet")
    produced_word = ADIRU_test.encode_word(0o204)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o204))
    #               padding  bin(35242)
    partial_data = "00" + "01000100110101010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_mach1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Mach',"2.986375 Mach")
    produced_word = ADIRU_test.encode_word(0o205)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o205))
    #           padding   2.986375 / 625 = 0.0047782 -> bin(47782)
    partial_data = "000" + "1011101010100110" # 1011101010100110
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_mach2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Mach',"3.1234567 Mach")
    produced_word = ADIRU_test.encode_word(0o205)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o205))
    #           padding   3.1234567 / 625 = 0.0049975 -> bin(47782)
    partial_data = "000" + "1100001100110111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_mach_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as pyE:
        ADIRU_test.set_value('Mach',"50.5050505 Mach")
        produced_word = ADIRU_test.encode_word(0o205)

def test_ADIRU_Max_Allowable_Airspeed():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Max. Allowable Airspeed',"942 Knots")
    produced_word = ADIRU_test.encode_word(0o207)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o207))
    #           padding
    partial_data = "0000000" + "111010111000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Max_Allowable_Airspeed_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as pyE:
        ADIRU_test.set_value('Max. Allowable Airspeed',"2000 Knots")
        produced_word = ADIRU_test.encode_word(0o207)

def test_ADIRU_True_Airspeed_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('True Airspeed',"942 Knots")
    produced_word = ADIRU_test.encode_word(0o210)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o210))
    #           padding
    partial_data = "0000" + "011101011100000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_True_Airspeed_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('True Airspeed',"5000 Knots")
        produced_word = ADIRU_test.encode_word(0o210)

def test_ADIRU_True_Airspeed_BCD():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('True Airspeed',"565 Knots")
    produced_word = ADIRU_test.encode_word(0o230)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o230))
    #             padding   padding    5      6          5
    partial_data = "0000" + "0000" + "101" + "0110" + "0101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Corrected_Angle_of_Attack():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Corrected Angle of Attack',"-72.15 Deg")
    produced_word = ADIRU_test.encode_word(0o241)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o241))
    #               padding     72.15 / 5 = 14.43, bin(1443) = 10110100011
    partial_data = "0000000" + "010110100011"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Corrected_Angle_of_Attack_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Corrected Angle of Attack',"5000 Knots")
        produced_word = ADIRU_test.encode_word(0o241)

def test_ADIRU_Altitude_Rate():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Altitude Rate',"14467 Ft/Min")
    produced_word = ADIRU_test.encode_word(0o212)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o212))
    #               padding     14467 / 16 = 904, bin(904) = 1110001000
    partial_data = "00000000" + "01110001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Altitude_Rate_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Altitude Rate',"50000 Ft/Min")
        produced_word = ADIRU_test.encode_word(0o212)

def test_ADIRU_Static_Air_Temp_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Static Air Temperature',"123 Degrees Celsius")
    produced_word = ADIRU_test.encode_word(0o213)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o213))
    #               padding     123 / 25 = 4.92, bin(492) = 111101100
    partial_data = "00000000" + "00111101100"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Static_Air_Temp_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Static Air Temperature',"600 Degrees Celsius")
        produced_word = ADIRU_test.encode_word(0o213)

def test_ADIRU_Impacted_Pressure_Uncorrected_mb():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Impacted Pressure, Uncorrected, mb',"511 mb")
    produced_word = ADIRU_test.encode_word(0o215)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o215))
    #               padding     511 / 8 = 63.875, bin(63875) = 1111100110000011
    partial_data = "000" + "1111100110000011"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Impacted_Pressure_Uncorrected_mb_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Impacted Pressure, Uncorrected, mb',"513 mb")
        produced_word = ADIRU_test.encode_word(0o215)

def test_ADIRU_Static_Pressure_Average_Corrected_In_Hg():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Static Pressure, Average, Corrected (In. Hg)',"63.999 In. Hg")
    produced_word = ADIRU_test.encode_word(0o217)

    # Make word to assert to
    tx_chip = lru_txr()
    label, _ = tx_chip.make_label_for_word(int(0o217))
    #               padding     bin(63.999)
    partial_data = "000" + "1111100111111111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Static_Pressure_Average_Corrected_In_Hg_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Static Pressure, Average, Corrected (In. Hg)',
                             "65.999 In. Hg")
        produced_word = ADIRU_test.encode_word(0o217)

def test_ADIRU_Baro_Corrected_Altitude2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Corrected Altitude #2',"35242 feet")
    produced_word = ADIRU_test.encode_word(0o220)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o220))
    #               padding  bin(35242)
    partial_data = "00" + "01000100110101010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Indicated_Angle_of_Attack():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Indicated Angle of Attack (Average)',"45.67 Deg")
    produced_word = ADIRU_test.encode_word(0o221)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o221))
    #               padding     45.67 / 5 = 9.134, bin(0913) = 001110010001
    partial_data = "0000000" + "001110010001"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Average_Static_Pressure_mb_Uncorrected():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Average Static Pressure mb, Uncorrected',"2047 mb")
    produced_word = ADIRU_test.encode_word(0o245)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o245))
    #               padding  bin(0.65504)
    partial_data = "000" + "1111111111100000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

def test_ADIRU_Average_Static_Pressure_mb_Corrected():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Average Static Pressure mb, Corrected',"2047 mb")
    produced_word = ADIRU_test.encode_word(0o246)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o246))
    #               padding  bin(0.65504)
    partial_data = "000" + "1111111111100000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Average_Static_Pressure_mb_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Average Static Pressure mb, Corrected',"3047 mb")
        produced_word = ADIRU_test.encode_word(0o246)

def test_ADIRU_Indicated_Side_Slip_Angle():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Indicated Side Slip Angle',"45.67 Deg")
    produced_word = ADIRU_test.encode_word(0o250)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o250))
    #               padding     45.67 / 5 = 9.134, bin(0913) = 001110010001
    partial_data = "0000000" + "001110010001"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Corrected_Altitude3():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Corrected Altitude #3',"35242 feet")
    produced_word = ADIRU_test.encode_word(0o251)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o251))
    #               padding  bin(35242)
    partial_data = "00" + "01000100110101010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Baro_Corrected_Altitude4():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Baro Corrected Altitude #4',"35242 feet")
    produced_word = ADIRU_test.encode_word(0o252)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o252))
    #               padding  bin(35242)
    partial_data = "00" + "01000100110101010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Corrected_Side_Slip_Angle():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Corrected Side Slip Angle',"45.67 Deg")
    produced_word = ADIRU_test.encode_word(0o253)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o253))
    #               padding     45.67 / 5 = 9.134, bin(0913) = 001110010001
    partial_data = "0000000" + "001110010001"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Integrated_Vertical_Acceleration1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Integrated Vertical Acceleration',"243.8523 Ft/Sec")
    produced_word = ADIRU_test.encode_word(0o265)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o265))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(243.8523 / 244, 6)
    partial_data = bin(int(str(x).replace(".","")))[2:] #"11110011111111100010"
    #       SDI
    data = "00" + partial_data[::-1] + "0" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Integrated_Vertical_Acceleration2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Integrated Vertical Acceleration',"-243.8523 Ft/Sec")
    produced_word = ADIRU_test.encode_word(0o265)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o265))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(243.8523 / 244, 6)
    partial_data = bin(int(str(x).replace(".","").replace("-","")))[2:] #"11110011111111100010"
    #       SDI
    data = "00" + partial_data[::-1] + "1" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Integrated_Vertical_Acceleration_exception1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Integrated Vertical Acceleration',"-300.8523 Ft/Sec")
        produced_word = ADIRU_test.encode_word(0o265)

def test_ADIRU_Integrated_Vertical_Acceleration_exception2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Integrated Vertical Acceleration',"-255.9999 Ft/Sec")
        produced_word = ADIRU_test.encode_word(0o265)

def test_ADIRU_Latitude_BNR1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Present Position - Latitude',"145.8672 N")
    produced_word = ADIRU_test.encode_word(0o310)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o310))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(145.8672 / 172, 6)
    partial_data = bin(int(str(x).replace(".","").replace("-","")))[2:] #"11110011111111100010"
    #       SDI
    data = "00" + partial_data[::-1] + "0" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Latitude_BNR2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Present Position - Latitude',"60.1010 S")
    produced_word = ADIRU_test.encode_word(0o310)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o310))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(60.1010 / 172, 6)
    partial_data = bin(int(str(x).replace(".","").replace("-","")))[2:] #"11110011111111100010"
    partial_data = "0" * (20-len(partial_data)) + partial_data
    #       SDI
    data = "00" + partial_data[::-1] + "1" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Latitude_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Present Position - Latitude',"660.1010 S")
        produced_word = ADIRU_test.encode_word(0o310)

def test_ADIRU_Longitude_BNR1():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Present Position - Longitude',"145.8672 W")
    produced_word = ADIRU_test.encode_word(0o311)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o311))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(145.8672 / 172, 6)
    partial_data = bin(int(str(x).replace(".","").replace("-","")))[2:] #"11110011111111100010"
    #       SDI
    data = "00" + partial_data[::-1] + "0" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Longitude_BNR2():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Present Position - Longitude',"60.1010 E")
    produced_word = ADIRU_test.encode_word(0o311)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o311))
    #  no padding     243.8523 / 244 = 0.9993946721311476, bin(999394) = 11110011111111100010
    x = round(60.1010 / 172, 6)
    partial_data = bin(int(str(x).replace(".","").replace("-","")))[2:] #"11110011111111100010"
    partial_data = "0" * (20-len(partial_data)) + partial_data
    #       SDI
    data = "00" + partial_data[::-1] + "1" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Longitude_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Present Position - Longitude',"660.1010 S")
        produced_word = ADIRU_test.encode_word(0o311)

def test_ADIRU_ground_speed_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Ground Speed',"4095 Knots")
    produced_word = ADIRU_test.encode_word(0o312)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o312))
    #              padding    4095 / 125 -> 32.76 -> bin(32760)
    partial_data = "0000" + "111111111111000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_ground_speed_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Ground Speed',"5095 Knots")
        produced_word = ADIRU_test.encode_word(0o312)

def test_ADIRU_Track_Angle_True_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Track Angle - True',"145.067 Degrees")
    produced_word = ADIRU_test.encode_word(0o313)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o313))
    #              padding    145.067 / 55 -> 2.6375818181818182 -> bin(26376)
    partial_data = "0000" + "110011100001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Track_Angle_True_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Track Angle - True',"1145.067 Degrees")
        produced_word = ADIRU_test.encode_word(0o313)

def test_ADIRU_True_Heading_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('True Heading',"145.067 Degrees")
    produced_word = ADIRU_test.encode_word(0o314)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o314))
    #              padding    145.067 / 55 -> 2.6375818181818182 -> bin(26376)
    partial_data = "0000" + "110011100001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Wind_Speed_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Wind Speed',"127 Knots")
    produced_word = ADIRU_test.encode_word(0o315)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o315))
    #              padding   bin(127)
    partial_data = "0"*11 + "01111111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Wind_Speed_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Speed',"300 Knots")
        produced_word = ADIRU_test.encode_word(0o315)

def test_ADIRU_Wind_Angle_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Wind Angle',"-127.3 Degrees")
    produced_word = ADIRU_test.encode_word(0o316)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o316))
    #              padding   -127.3/7 = -18.18 -> bin(182)
    partial_data = "0"*11 + "10110110"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Wind_Angle_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Wind Angle',"-197.3 Degrees")
        produced_word = ADIRU_test.encode_word(0o316)

def test_ADIRU_Track_Angle_Magnetic_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Track Angle - Magnetic',"145.067 Degrees")
    produced_word = ADIRU_test.encode_word(0o317)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o317))
    #              padding    145.067 / 55 -> 2.6375818181818182 -> bin(26376)
    partial_data = "0000" + "110011100001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Magnetic_Heading_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Magnetic Heading',"145.067 Degrees")
    produced_word = ADIRU_test.encode_word(0o320)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o320))
    #              padding    145.067 / 55 -> 2.6375818181818182 -> bin(26376)
    partial_data = "0000" + "110011100001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Drift_Angle_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Drift Angle',"-45.06 Degrees")
    produced_word = ADIRU_test.encode_word(0o321)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o321))
    #              padding    -45.06 / 5 -> 9.012 -> bin(901)
    partial_data = "0000000" + "001110000101"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Flight_Path_Angle_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Flight Path Angle',"-45.06 Degrees")
    produced_word = ADIRU_test.encode_word(0o322)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o322))
    #              padding    -45.06 / 5 -> 9.012 -> bin(901)
    partial_data = "0000000" + "001110000101"
    #       SDI
    data = "00" + partial_data[::-1] + "11" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Flight_Path_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Flight Path Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o323)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o323))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Flight_Path_Acceleration_exception_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Flight Path Acceleration',"4.001 gs")
        produced_word = ADIRU_test.encode_word(0o323)

def test_ADIRU_Pitch_Angle_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Pitch Angle',"35.35 Degrees")
    produced_word = ADIRU_test.encode_word(0o324)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o324))
    #              padding    bin(3535)
    partial_data = "00000" + "00110111001111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Pitch_Angle_BNR_exception():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Pitch Angle',"99935.35 Degrees")
        produced_word = ADIRU_test.encode_word(0o324)

def test_ADIRU_Roll_Angle_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Roll Angle',"35.35 Degrees")
    produced_word = ADIRU_test.encode_word(0o325)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o325))
    #              padding    bin(3535)
    partial_data = "00000" + "00110111001111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Pitch_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Pitch Rate',"35.355 Degrees")
    produced_word = ADIRU_test.encode_word(0o326)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o326))
    #              padding    35.355/15 = 2.357 -> bin(2.357)
    partial_data = "000000" + "0100100110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Pitch_Rate_exception_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Body Pitch Rate',"135.355 Degrees")
        produced_word = ADIRU_test.encode_word(0o326)

def test_ADIRU_Body_Roll_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Roll Rate',"35.355 Degrees")
    produced_word = ADIRU_test.encode_word(0o327)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o327))
    #              padding    35.355/15 = 2.357 -> bin(2.357)
    partial_data = "000000" + "0100100110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Yaw_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Yaw Rate',"35.355 Degrees")
    produced_word = ADIRU_test.encode_word(0o330)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o330))
    #              padding    35.355/15 = 2.357 -> bin(2.357)
    partial_data = "000000" + "0100100110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Longitudinal_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Longitudinal Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o331)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o331))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Lateral_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Lateral Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o332)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o332))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Body_Normal_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Body Normal Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o333)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o333))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Platform_Heading_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Platform Heading',"78.79 Degrees")
    produced_word = ADIRU_test.encode_word(0o334)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o334))
    #              padding   78.79 / 9 = 8.75444 -> bin(0875)
    partial_data = "00000000" + "01101101011"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Platform_Heading_exception_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Platform Heading',"8078.79 Degrees")
        produced_word = ADIRU_test.encode_word(0o334)

def test_ADIRU_Track_Angle_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Track Angle Rate',"28.79 Degrees")
    produced_word = ADIRU_test.encode_word(0o335)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o335))
    #              padding   78.79 / 9 = 8.75444 -> bin(0875)
    partial_data = "00000000" + "11101111111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Track_Angle_Rate_exception_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Track Angle Rate',"33.000 Degrees")
        produced_word = ADIRU_test.encode_word(0o335)

def test_ADIRU_Inertial_Pitch_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Inertial Pitch Rate',"35.355 Degrees")
    produced_word = ADIRU_test.encode_word(0o336)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o336))
    #              padding    35.355/15 = 2.357 -> bin(2.357)
    partial_data = "000000" + "0100100110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Inertial_Roll_Rate_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Inertial Roll Rate',"35.355 Degrees")
    produced_word = ADIRU_test.encode_word(0o337)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o337))
    #              padding    35.355/15 = 2.357 -> bin(2.357)
    partial_data = "000000" + "0100100110101"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Grid_Heading_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Grid Heading',"145.067 Degrees")
    produced_word = ADIRU_test.encode_word(0o341)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o341))
    #              padding    145.067 / 55 -> 2.6375818181818182 -> bin(26376)
    partial_data = "0000" + "110011100001000"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Potential_Vertical_Speed_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Potential Vertical Speed',"11111 Ft/Min")
    produced_word = ADIRU_test.encode_word(0o360)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o360))
    #              padding    bin(11111)
    partial_data = "0000" + "010101101100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Potential_Vertical_Speed_exception_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])
    with pytest.raises(Exception) as ptE:
        ADIRU_test.set_value('Potential Vertical Speed',"111111 Ft/Min")
        produced_word = ADIRU_test.encode_word(0o360)

def test_ADIRU_Along_Track_Horizontal_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Along Track Horizontal Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o362)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o362))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Cross_Track_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Cross Track Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o363)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o363))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_NS_Vel_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('North-South Velocity',"4095.125 Knots")
    produced_word = ADIRU_test.encode_word(0o366)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o366))
    #              padding    4086.125/125.0 =32.761 -> bin(32761)
    partial_data = "0000" + "111111111111001"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_EW_Vel_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('East-West Velocity',"4095.125 Knots")
    produced_word = ADIRU_test.encode_word(0o367)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o367))
    #              padding    4086.125/125.0 =32.761 -> bin(32761)
    partial_data = "0000" + "111111111111001"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Vertical_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Vertical Acceleration',"3.111 gs")
    produced_word = ADIRU_test.encode_word(0o364)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o364))
    #              padding    bin(3111)
    partial_data = "0000000" + "110000100111"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_ADIRU_Along_Heading_Acceleration_BNR():
    print("\n")
    Orange_bus = ARINC429BUS()
    Blue_bus = ARINC429BUS()
    ADIRU_test = ADIRU(bus_speed="low", BUS_CHANNELS=[Orange_bus, Blue_bus])

    ADIRU_test.set_value('Along Heading Acceleration',"3.00153 gs")
    produced_word = ADIRU_test.encode_word(0o375)

    # Make word to assert to
    tx_chip = lru_txr()
    # 0b00001011
    label, _ = tx_chip.make_label_for_word(int(0o375))
    #              padding    bin(3111)
    partial_data = "0" + "101111111001010010"
    #       SDI
    data = "00" + partial_data[::-1] + "00" # <- SSM for - degrees
    # Parity - need label for this
    data += tx_chip.calc_parity(label + data)
    word = label + data

    assert(produced_word == word)

def test_all_ADIRUs():
    test_ADIRU_rx_GPS1()
    test_ADIRU_rx_GPS2()
    #test_ADIRU_default_values()
    test_ADIRU_lat()
    test_ADIRU_lon()
    test_ADIRU_ground_speed()
    test_ADIRU_ground_speed_exception1()
    test_ADIRU_ground_speed_exception2()
    test_ADIRU_Track_Angle_True()
    test_ADIRU_Track_Angle_True_exception1()
    test_ADIRU_Track_Angle_True_exception2()
    test_ADIRU_Magnetic_Heading()
    test_ADIRU_Magnetic_Heading_exception1()
    test_ADIRU_Magnetic_Heading_exception2()
    test_ADIRU_Wind_Speed()
    test_ADIRU_Wind_Speed_exception1()
    test_ADIRU_Wind_Speed_exception2()
    test_ADIRU_Wind_Direction_True()
    test_ADIRU_Wind_Direction_True_exception1()
    test_ADIRU_Wind_Direction_True_exception2()
    test_ADIRU_True_Heading()
    test_ADIRU_True_Heading_exception1()
    test_ADIRU_True_Heading_exception2()
    test_ADIRU_Total_Air_Temperature()
    test_ADIRU_Total_Air_Temperature_exception1()
    test_ADIRU_Total_Air_Temperature_exception2()
    test_ADIRU_Static_Air_Temperature()
    test_ADIRU_Static_Air_Temperature_exception1()
    test_ADIRU_Static_Air_Temperature_exception2()
    test_ADIRU_Baro_Correction_mb_1_part1()
    test_ADIRU_Baro_Correction_mb_1_part2()
    test_ADIRU_Baro_Correction_mb_1_exception2()
    test_ADIRU_Baro_Correction_mb_1_exception1()
    test_ADIRU_Baro_Correction_ins_Hg_1()
    test_ADIRU_Baro_Correction_ins_Hg_1_exception1()
    test_ADIRU_Baro_Correction_ins_Hg_1_exception2()
    test_ADIRU_Baro_Correction_mb_2_part1()
    test_ADIRU_Baro_Correction_mb_2_part2()
    test_ADIRU_Baro_Correction_mb_2_exception1()
    test_ADIRU_Baro_Correction_mb_2_exception2()
    test_ADIRU_Baro_Correction_ins_Hg_2()
    test_ADIRU_Baro_Correction_ins_Hg_2_exception1()
    test_ADIRU_Baro_Correction_ins_Hg_2_exception2()
    test_ADIRU_total_pressure()
    test_ADIRU_total_pressure_exception()
    test_ADIRU_IR_test1()
    test_ADIRU_IR_test2()
    test_ADIRU_IR_test3()
    test_ADIRU_Body_Pitch_Acceleration1()
    test_ADIRU_Body_Pitch_Acceleration2()
    test_ADIRU_Body_Pitch_Acceleration_exception1()
    test_ADIRU_Body_Pitch_Acceleration_exception2()
    test_ADIRU_Body_Roll_Acceleration1()
    test_ADIRU_Body_Roll_Acceleration2()
    test_ADIRU_Body_Roll_Acceleration_exception1()
    test_ADIRU_Body_Roll_Acceleration_exception2()
    test_ADIRU_Body_Yaw_Acceleration1()
    test_ADIRU_Body_Yaw_Acceleration2()
    test_ADIRU_Body_Yaw_Acceleration_exception1()
    test_ADIRU_Body_Yaw_Acceleration_exception2()
    test_ADIRU_Cabin_Pressure1()
    test_ADIRU_Cabin_Pressure_exception1()
    test_ADIRU_Cabin_Pressure_exception2()
    test_ADIRU_Left_Static_Pressure_Uncorrected()
    test_ADIRU_Right_Static_Pressure_Uncorrected()
    test_ADIRU_altitude_1013()
    test_ADIRU_altitude_1013_exception()
    test_ADIRU_altitude_1013_special_case()
    test_ADIRU_Baro_Corrected_Altitude1()
    test_ADIRU_mach1()
    test_ADIRU_mach2()
    test_ADIRU_mach_exception()
    test_ADIRU_Max_Allowable_Airspeed()
    test_ADIRU_Max_Allowable_Airspeed_exception()
    test_ADIRU_True_Airspeed_BNR()
    test_ADIRU_True_Airspeed_BNR_exception()
    test_ADIRU_True_Airspeed_BCD()
    test_ADIRU_Corrected_Angle_of_Attack()
    test_ADIRU_Corrected_Angle_of_Attack_exception()
    test_ADIRU_Altitude_Rate()
    test_ADIRU_Altitude_Rate_exception()
    test_ADIRU_Static_Air_Temp_BNR()
    test_ADIRU_Static_Air_Temp_BNR_exception()
    test_ADIRU_Impacted_Pressure_Uncorrected_mb()
    test_ADIRU_Impacted_Pressure_Uncorrected_mb_exception()
    test_ADIRU_Static_Pressure_Average_Corrected_In_Hg()
    test_ADIRU_Static_Pressure_Average_Corrected_In_Hg_exception()
    test_ADIRU_Baro_Corrected_Altitude2()
    test_ADIRU_Indicated_Angle_of_Attack()
    test_ADIRU_Average_Static_Pressure_mb_Uncorrected()
    test_ADIRU_Average_Static_Pressure_mb_Corrected()
    test_ADIRU_Average_Static_Pressure_mb_exception()
    test_ADIRU_Indicated_Side_Slip_Angle()
    test_ADIRU_Baro_Corrected_Altitude3()
    test_ADIRU_Baro_Corrected_Altitude4()
    test_ADIRU_Corrected_Side_Slip_Angle()
    test_ADIRU_Integrated_Vertical_Acceleration1()
    test_ADIRU_Integrated_Vertical_Acceleration2()
    test_ADIRU_Integrated_Vertical_Acceleration_exception1()
    test_ADIRU_Integrated_Vertical_Acceleration_exception2()
    test_ADIRU_Latitude_BNR1()
    test_ADIRU_Latitude_BNR2()
    test_ADIRU_Latitude_BNR_exception()
    test_ADIRU_Longitude_BNR1()
    test_ADIRU_Longitude_BNR2()
    test_ADIRU_Longitude_BNR_exception()
    test_ADIRU_ground_speed_BNR()
    test_ADIRU_ground_speed_BNR_exception()
    test_ADIRU_Track_Angle_True_BNR()
    test_ADIRU_Track_Angle_True_BNR_exception()
    test_ADIRU_True_Heading_BNR()
    test_ADIRU_Wind_Speed_BNR()
    test_ADIRU_Wind_Speed_BNR_exception()
    test_ADIRU_Wind_Angle_BNR()
    test_ADIRU_Wind_Angle_BNR_exception()
    test_ADIRU_Track_Angle_Magnetic_BNR()
    test_ADIRU_Magnetic_Heading_BNR()
    test_ADIRU_Drift_Angle_BNR()
    test_ADIRU_Flight_Path_Angle_BNR()
    test_ADIRU_Flight_Path_Acceleration_BNR()
    test_ADIRU_Flight_Path_Acceleration_exception_BNR()
    test_ADIRU_Pitch_Angle_BNR()
    test_ADIRU_Pitch_Angle_BNR_exception()
    test_ADIRU_Roll_Angle_BNR()
    test_ADIRU_Body_Pitch_Rate_BNR()
    test_ADIRU_Body_Pitch_Rate_exception_BNR()
    test_ADIRU_Body_Roll_Rate_BNR()
    test_ADIRU_Body_Yaw_Rate_BNR()
    test_ADIRU_Body_Longitudinal_Acceleration_BNR()
    test_ADIRU_Body_Lateral_Acceleration_BNR()
    test_ADIRU_Body_Normal_Acceleration_BNR()
    test_ADIRU_Platform_Heading_BNR()
    test_ADIRU_Platform_Heading_exception_BNR()
    test_ADIRU_Track_Angle_Rate_BNR()
    test_ADIRU_Track_Angle_Rate_exception_BNR()
    test_ADIRU_Inertial_Pitch_Rate_BNR()
    test_ADIRU_Inertial_Roll_Rate_BNR()
    test_ADIRU_Grid_Heading_BNR()
    test_ADIRU_Potential_Vertical_Speed_BNR()
    test_ADIRU_Potential_Vertical_Speed_exception_BNR()
    test_ADIRU_Along_Track_Horizontal_Acceleration_BNR()
    test_ADIRU_Cross_Track_Acceleration_BNR()
    test_ADIRU_Vertical_Acceleration_BNR()
    test_ADIRU_NS_Vel_BNR()
    test_ADIRU_EW_Vel_BNR()
    test_ADIRU_Along_Heading_Acceleration_BNR()

def test_IDS_log_outfile_path():
    try:
        IDS_test_default = IDS()
    except FileNotFoundError:
        IDS_test_default = IDS(rules_file=
                               r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt")
    log_file = IDS_test_default.log_filepath
    assert(log_file == r"C:/ARINC_IDS/Logs/Logs.txt")

def test_IDS_alert_outfile_path():
    try:
        IDS_test_default = IDS()
    except FileNotFoundError:
        IDS_test_default = IDS(rules_file=
                               r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt")
    alert_file = IDS_test_default.alert_filepath
    assert(alert_file == r"C:/ARINC_IDS/Alerts/Alerts.txt")

def test_IDS_Channel_inputs():
    try:
        IDS_test_default = IDS()
    except FileNotFoundError:
        IDS_test_default = IDS(rules_file=
                               r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt")
    channels = IDS_test_default.channels
    #print("\n", channels)
    assert(channels == {
        'Orange': ['GPS -> ADIRU'],
        'Blue': ['ADIRU -> FMC'],
        'Purple': ['FMC -> RMS', 'FMC -> FAEC1', 'FMC -> FAEC2', 'FMC -> WnBS'],
        'Green': ['FMC -> RMS', 'FMC -> FAEC1', 'FMC -> FAEC2', 'FMC -> RWnBS']
    })

def test_IDS_SDI_masks():
    try:
        IDS_test_default = IDS()
    except FileNotFoundError:
        IDS_test_default = IDS(rules_file=
                               r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt")
    sdis = IDS_test_default.sdis
    assert(sdis == {
        "ADIRU_Orange": "11",
        "FMC_Blue": "11",
        "RMS_Purple": "00",
        "FAEC1_Purple": "01",
        "FAEC2_Purple": "10",
        "WnBS_Purple": "11",
        "RMS_Green": "00",
        "FAEC1_Green": "01",
        "FAEC2_Green": "10",
        "WnBS_Green": "11"
    })

def test_rules_default():
    try:
        IDS_test_default = IDS()
    except FileNotFoundError:
        IDS_test_default = IDS(rules_file=
                               r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt")
    rulez = IDS_test_default.rules
    #ADIRU_1 = ADIRU("low",[ARINC429BUS(),ARINC429BUS()])
    #ADIRU_1.set_value('Ground Speed',"6000 Knots")
    #produced_word = ADIRU_1.encode_word(0o012)
    #print(produced_word)
    assert(rulez == [('alert','Blue','0000000000000000000000000000000',None,False,'Blue bus has a word.'),
                     ('alert','Blue','0001000000000000000000000000000',None,False,'Latitude word sent'),
                     ('log', 'Blue', '1001000000000000000000000000000',None,False,''),
                     ('log', 'Blue', '0000000000000000000000000000000',None,False,''),
                    # Label -> 0o012 = 01010000, ADIRS=11, 6000 = 000...1100
                     ('alert','Orange','0101000011000000000000011000000',True,False,"Plane's speed is 6000 Knots"),
                     ('alert','Purple','0000000000111111111111111110000',None,False,'Funny Pattern!'),
                     ('alert','Purple','0100110000000000000000000000000',None,False,'Tire Loading (Left Wing Main) Word!'),
                     ('alert','Purple','0100110000000000000000000000000',None,True,'Tire Loading (Left Wing Main) Word!')])

def test_all_IDS_tests():
    test_IDS_log_outfile_path()
    test_IDS_alert_outfile_path()
    test_IDS_Channel_inputs()
    test_IDS_SDI_masks()


if __name__ == "__main__":
    #test_all()
    test_all_non_asserts()
