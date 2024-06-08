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

def test_all():
    #test_voltage_sim()
    #test_intWord_to_voltage()
    test_FMC_word_validation1()
    test_FMC_word_validation2()
    test_FMC_word_validation3()
    #test_FMC_pilot_input()
    #test_bus_queue_TX()
    #test_bus_queue_RX()
    #test_FMC_TX()
    #test_GPS_comm()
    #test_RX_Helper1()
    #test_RX_Helper2()
    #test_RX_Helper3()
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
    FMC_test5.pilot_input()

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

def test_FMC_TX():
    Channel_A = ARINC429BUS()
    FMC_test6 = FMC("HIGH", BUS_CHANNELS=[Channel_A])

    # FMC Random Word Thread:
    txer_thread = Thread(target=FMC_test6.transmit_random_voltages, args=(0,) )
    txer_thread.start()

    # FMC build in visualization:
    FMC_test6.visualize_FMC_transmissions(Channel_A)

    txer_thread.join()

def test_GPS_comm():
    GPS_test1 = GPS("HIGH")
    GPS_test1.communicate_to_bus()

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

def test_RX_label_fetch1():
    label_1 = "11111111000000001111111100000000"
    RX_Helper = lru_rxr()
    assert(0b11111111 == RX_Helper.get_label_from_word(int(label_1,2)))

def test_RX_label_fetch2():
    label_1 = "10100101000000001111111100000000"
    RX_Helper = lru_rxr()
    assert(0b10100101 == RX_Helper.get_label_from_word(int(label_1,2)))

def test_RX_label_fetch3():
    label_1 = "00000000111111110000000011111111"
    RX_Helper = lru_rxr()
    assert(0b00000000 == RX_Helper.get_label_from_word(int(label_1,2)))

def test_RX_label_fetch4():
    label_1 = "00110101000000001111111100000000"
    RX_Helper = lru_rxr()
    # 00110101 reversed
    assert(0b10101100 == RX_Helper.get_label_from_word(int(label_1,2)))

def test_RX_label_fetch5():
    label_1 = "00000001000000001111111100000000"
    RX_Helper = lru_rxr()
    # 00110101 reversed
    assert(0b10000000 == RX_Helper.get_label_from_word(int(label_1,2)))

def test_TX_label_reverser1():
    label = 0o066
    # print(bin(label))
    # -> "00110110"
    tx_chip = lru_txr()
    assert("01101100" == tx_chip.make_label_for_word(label)[0])

def test_TX_label_reverser2():
    label = 0o010
    # print(bin(label))
    # -> "00001000"
    tx_chip = lru_txr()
    assert("00001000"[::-1] == tx_chip.make_label_for_word(label)[0])

def test_TX_label_reverser3():
    label = 0o011
    # print(bin(label))
    # -> "00001001"
    tx_chip = lru_txr()
    assert("00001001"[::-1] == tx_chip.make_label_for_word(label)[0])

def test_TX_label_reverser4():
    label = 0o210
    # print(bin(label))
    # -> "10001000"
    tx_chip = lru_txr()
    assert("10001000"[::-1] == tx_chip.make_label_for_word(label)[0])

def test_TX_label_reverser5():
    label = 0o320
    print(bin(label))
    # -> "11010000"
    tx_chip = lru_txr()
    assert("11010000"[::-1] == tx_chip.make_label_for_word(label)[0])

def test_TX_label_reverser_all():
    tx_chip = lru_txr()
    for x in range(0o000, 0o377):
        label = x
        label = bin(label)[2:]
        label = "0"*(8-len(label)) + label
        label = label[::-1]
        #print(label)
        assert(label == tx_chip.make_label_for_word(x)[0])

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

def test_RMS_Test_Static1():
    print("\n")
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    print("Default RMS Bootup Status.")
    assert str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tVOR/ILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
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

def test_RMS_Test_latitudedecode_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o010))
    data = "1001" + "1001" + "1010" + "1010" + "1110" + "0" + "00" + "1"
    print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tVOR/ILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
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

def test_RMS_Test_longitudedecode_BCD():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o011))
    data = "0001" + "1010" + "0100" + "1001" + "0110" + "1" + "11" + "1"
    print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # N 75 Deg 59.9'
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tVOR/ILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
           str({"Flight Number": None,
                "Latitude": "W 169 Deg 25.8'",
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

def test_RMS_flight_number():
    print("\n")
    tx_chip = lru_txr()
    ARINC_Channel = ARINC429BUS()
    RMS_test1 = RMS("low",[ARINC_Channel])
    label, _ = tx_chip.make_label_for_word(int(0o261))
    data = "00" + "000" + "1110" + "1000" + "1000" + "0000" + "00"
    par_bit = tx_chip.calc_parity(label+data)
    data += par_bit
    print(len(data))
    word = label + data
    RMS_test1.decode_word(word)
    # 117
    assert(str(RMS_test1) == f"Commanded Frequencies:\n\tGeneral:0.0\n\tVOR/ILS:0.0\n\tDME:0.0\n\tHF_COMM:0.0" + "\n\nADS-B Message:" + \
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

if __name__ == "__main__":
    test_all()
