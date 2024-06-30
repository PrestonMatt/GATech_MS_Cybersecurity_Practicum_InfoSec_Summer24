from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from time import sleep

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

dir = r"/ARINC429 Simulation/IDS_Rules_test_files/IDS_EVAL1_RULES_FILES"
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

def _test_(bus_speed:str, sampling_rate:float, num_rules:int, SDI:str):

    Channel1 = ARINC429BUS()
    Channel2 = ARINC429BUS()
    Channel3 = ARINC429BUS()
    bus_channels = [Channel1, Channel2, Channel3]

    filename = dir + rules_files[num_rules]
    IDS_test_numX = IDS(bus_speed, BUS_CHANNELS=bus_channels, rules_file=filename)

    transmitting_LRU = None
    if(SDI == "00"):
        transmitting_LRU = FMC(bus_speed, BUS_CHANNELS=bus_channels)
        transmitting_LRU.generate_word_to_pitch_plane("up")
        transmitting_LRU.generate_word_to_pitch_plane("down")
        transmitting_LRU.generate_word_to_pitch_plane("left") # Transmits 3 words.
    elif(SDI == "01"):
        transmitting_LRU = GPS()
    elif(SDI == "02"):
        transmitting_LRU = ADIRU()


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
        sampling_rates.append( 0.5 / (10 ** x) )
    #print(sampling_rate)

    num_rules = [y for y in range(0,11)]
    #print(num_rules)

    for bus_speed in bus_speeds:
        for sampling_rate in sampling_rates:
            for num_rule in num_rules:
                for SDI, value in SDIs.items():
                    _test_(bus_speed, sampling_rate, num_rule, value)

if __name__ == '__main__':
    main()