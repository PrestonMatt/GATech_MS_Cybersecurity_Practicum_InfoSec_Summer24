from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from time import sleep, time
from threading import Thread

"""
Robustness of the IDS: Right now my bus code can transmit at the actual speed of an ARINC429 bus. However, when
receiving words, especially with the IDS, I need to slow it down so that voltages aren’t missed. This is an issue 
with Python threading and dealing with microsecond timing. I will run tests to see how robust my IDS is by testing 
it’s receive function. These tests will be at receive 5 ARINC429 words from a given RX LRU (so FMC, GPS, or ADIRU). 
The speed of the bus will start slow – instead of ½ microsecond between voltage transmissions it will start at ½ second.
Then the intervals will scale up logarithmic up in speed until it gets to ½ microsecond again. From there I will create
a chart: the amount of words it’s able to correctly receive and act upon (based on it’s rules) per speed. Then I will 
repeat this test with various rules, from 1 to 10 rules.
"""

"""
    Given the sampling rate (decreasing logarithmically from 0.5 seconds to 0.5 microseconds)
    Run the IDS. Send it 5 words from:
        GPS
        FMC
        ADIRU
    Check accuracy percentage of RX'd words.
"""

dir = r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\IDS_Rules_test_files\IDS_EVAL1_RULES_FILES"
rules_files = {
    0:r"\ZERO_RULES.txt",
    1:r"\ONE_RULE.txt",
    2:r"\TWO_RULES.txt",
    3:r"\THREE_RULES.txt",
    4:r"\FOUR_RULES.txt",
    5:r"\FIVE_RULES.txt",
    6:r"\SIX_RULES.txt",
    7:r"\SEVEN_RULES.txt",
    8:r"\EIGHT_RULES.txt",
    9:r"\NINE_RULES.txt",
    10:r"\TEN_RULES.txt"
}

def _test_(bus_speed:str, sampling_rate:float, num_rules:int, SDI="ADIRU"):

    Channel1 = ARINC429BUS()
    Channel2 = ARINC429BUS()
    Channel3 = ARINC429BUS()
    bus_channels = [Channel1, Channel2, Channel3]

    filename = dir + rules_files[num_rules]
    IDS_test_numX = IDS(bus_speed, BUS_CHANNELS=bus_channels, rules_file=filename)

    words_to_TX = []

    if(SDI == "ADIRU"):
        transmitting_LRU = ADIRU(bus_speed, BUS_CHANNELS=bus_channels[:-1]) # only gets channel 1 and 2
        # Word 1
        transmitting_LRU.set_value('Present Position - Latitude','N 75 Deg 59.9')
        word1 = transmitting_LRU.encode_word(0o010)
        words_to_TX.append(word1)

        # Word 2
        transmitting_LRU.set_value('Present Position - Latitude','S 40 Deg -40.1')
        word2 = transmitting_LRU.encode_word(0o010)
        words_to_TX.append(word2[:-1]+"0")

        # Word 3
        transmitting_LRU.set_value('Wind Speed',"123 Knots")
        word3 = transmitting_LRU.encode_word(0o015)
        words_to_TX.append(word3)

        transmitting_LRU.set_value('Body Yaw Acceleration',"54.123 Deg/Sec^2")
        word4 = transmitting_LRU.encode_word(0o054)
        words_to_TX.append(word4)

        transmitting_LRU.set_value('Baro Corrected Altitude #2',"35242 feet")
        word5 = transmitting_LRU.encode_word(0o220)
        words_to_TX.append(word5)

        print(f"Words: {words_to_TX}")

        def send_ADIRU_words(transmitting_LRU_ADIRU, words_to_TX):
            for word in words_to_TX:
                print(f"Sending word: 0b{word}")
                # transmit_given_word(self, word:int, bus_usec_start, channel_index=0, slowdown_rate = 5e-7)
                transmitting_LRU_ADIRU.TXcommunicator_chip.transmit_given_word(word=int(word,2), # Words 1 to 5
                                                              bus_usec_start=time(), #start time.
                                                              channel_index=0, # Channel2
                                                              slowdown_rate=sampling_rate) # this is our test
            # Stop the threads?

        # Start the TXr transmission in thread
        transmitter_thread = Thread(target=send_ADIRU_words, args=(transmitting_LRU,words_to_TX,))
        transmitter_thread.start()
        # Start the receiver in a separate thread
        receiver_thread = Thread(target=IDS_test_numX.receive_words, args=(0, sampling_rate,))
        receiver_thread.start()
        # Start the real-time visualization of TX'd voltages in a separate thread
        visualization_threadTX = Thread(target=ARINC429BUS.queue_visual,
                                      args=(Channel1, sampling_rate, "Transmitted Voltages for IDS Eval 1",))
        visualization_threadTX.start()
        # Start the real-time visualization of RX'd voltages in a final thread
        visualization_threadRX = Thread(target=IDS_test_numX.communication_chip.visualize_LRU_receiveds_mother,
                                        args=(Channel1,"Received Voltages for Eval 1",sampling_rate),)
        visualization_threadRX.start()

        # Join threads to main thread keeping simulation running
        transmitter_thread.join()
        receiver_thread.join()
        visualization_threadTX.join()
        visualization_threadRX.join()

    """
    transmitting_LRU = None
    if(SDI == "00"):
        
        #transmitting_LRU = FMC(bus_speed, BUS_CHANNELS=bus_channels)
        #transmitting_LRU.generate_word_to_pitch_plane("up")
        #transmitting_LRU.generate_word_to_pitch_plane("down")
        #transmitting_LRU.generate_word_to_pitch_plane("left") # Transmits 3 words.
    elif(SDI == "01"):
        transmitting_LRU = GPS()
    elif(SDI == "02"):
        transmitting_LRU = ADIRU()
    """

def main():

    bus_speeds = [
        "low",
        "high"
    ]

    SDIs = {
        "00":"FMC",
        "01":"GPS",
        "10":"ADIRU"
    }

    # sampling_rate = 0.5 -> 1/2 second
    # sampling_rate = 0.05 -> 1/20th second
    # sampling_rate = 0.005 -> 5 milliseconds
    # sampling_rate = 0.0005 -> 1/2 millisecond
    # sampling_rate = 0.00005 -> 1/20 millisecond
    # sampling_rate = 0.000005 -> 5 microseconds
    # sampling_rate = 0.0000005 -> 1/2 microsecond
    sampling_rates = []
    for x in range(7):
        sampling_rates.append( 0.05 / (10 ** x) )
    #print(sampling_rate)

    num_rules = [y for y in range(0,11)]
    #print(num_rules)

    # Uncomment this when using EVAL1 for specific sampling rates.
    """
    user_sampling_rate = input("Please enter the sleep time for the slowdown rate:")
    if(user_sampling_rate not in sampling_rates):
        print("Warning, sampling rate arbitrary")
        try:
            sampling_rate = float(user_sampling_rate)
        except ValueError:
            raise ValueError(f"Please enter a valid sampling rate. Needs to be a float. Got: {user_sampling_rate}\nExpected: {sampling_rates}")
    """

    for bus_speed in bus_speeds:
        for sampling_rate in sampling_rates:
            for num_rule in num_rules:
                #for SDI, value in SDIs.items():
                print(f"Performing Evaluation Test on IDS with:\n\t{bus_speed} bus speed,\n\t{sampling_rate} second sampling rate,\n\t{num_rule} rules.\n")
                _test_(bus_speed, sampling_rate, num_rule)
                    #print(f"Performing Evaluation Test on IDS with:\n\t{bus_speed} bus speed,\n\t{sampling_rate} second sampling rate,\n\t{num_rule} rules and on,\n\t{SDIs[SDI]} LRU.\n")
                    #_test_(bus_speed, sampling_rate, num_rule, value)

if __name__ == '__main__':
    main()
