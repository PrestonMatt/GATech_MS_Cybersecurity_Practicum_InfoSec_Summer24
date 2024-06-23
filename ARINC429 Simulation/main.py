# Import Python modules
from threading import Thread
from time import sleep, time
import random
# Import MY classes
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_FAEC_Simulator import full_authority_engine_control as FAEC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_WnBS_Simulator import weight_and_balance_system as WnBS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from LRU_RMS_Simulator import radio_management_system as RMS
from BusQueue_Simulator import GlobalBus as ARINC429BUS

global bus_speed

def START_BLUE_BUS(ADIRU_LRU:ADIRU, FMC_LRU:FMC):
    while(True):
        data = ADIRU_LRU.data
        for datum in data:
            ADIRU_LRU.TXcommunicator_chip.transmit_given_word(ADIRU_LRU.encode_word(datum))
            FMC_LRU.RXcomm_chip.receive_given_word(0) # Channel index = 0 as this is the blue bus.

def START_ORANGE_BUS(GPS_LRU:GPS, ADIRU_LRU:ADIRU):
    while(True):
        GPS_LRU.communicate_to_bus()
        GPS_LRU.determine_next_position()
        ADIRU_LRU.RXcommunicator_chip.receive_given_word(channel_index=0)

def START_channel_a_n_b(FMC_LRU:FMC):
    RMS_LRU = RMS(bus_speed, [PurpleBus, GreenBus])
    FAEC_1_LRU = FAEC(bus_speed, "left",1,[PurpleBus, GreenBus])
    FAEC_2_LRU = FAEC(bus_speed, "right",2,[PurpleBus, GreenBus])
    WnBS_LRU = WnBS(bus_speed, [PurpleBus, GreenBus])

    #START_PURPLE_BUS(FMC_LRU, RMS_LRU, FAEC_1_LRU, FAEC_2_LRU, WnBS_LRU)
    #START_GREEN_BUS(FMC_LRU, RMS_LRU, FAEC_1_LRU, FAEC_2_LRU, WnBS_LRU)

    # Start the FMC_LRU send words
    #sendFMCwords = Thread(FMC_LRU.FIFO_mode())
    while(True):
        word = FMC_LRU.generate_word_to_pitch_plane(random.choice(["up","down","left","right","w","s"]))
        FMC_LRU.communication_chip.transmit_given_word(word,FMC_LRU.usec_start,channel_index=0)
        FMC_LRU.communication_chip.transmit_given_word(word,FMC_LRU.usec_start,channel_index=1)

        RMS_LRU.communication_chip.receive_given_word(channel_index=0)
        RMS_LRU.communication_chip.receive_given_word(channel_index=1)

        FAEC_1_LRU.communication_chip.receive_given_word(channel_index=0)
        FAEC_1_LRU.communication_chip.receive_given_word(channel_index=1)

        FAEC_2_LRU.communication_chip.receive_given_word(channel_index=0)
        FAEC_2_LRU.communication_chip.receive_given_word(channel_index=1)

        WnBS_LRU.communication_chip.receive_given_word(channel_index=0)
        WnBS_LRU.communication_chip.receive_given_word(channel_index=1)

def main():
    global bus_speed
    bus_speed = "low"
    # Define all the bus objects:
    global OrangeBus # = ARINC429BUS()
    OrangeBus = ARINC429BUS()

    global BlueBus # = ARINC429BUS()
    BlueBus = ARINC429BUS()

    global PurpleBus # = ARINC429BUS()
    PurpleBus = ARINC429BUS()

    global GreenBus # = ARINC429BUS()
    GreenBus = ARINC429BUS()

    # Define the LRUs that need to be present across multiple buses:
    GPS_LRU = GPS(bus_speed, OrangeBus)
    ADIRU_LRU = ADIRU(bus_speed, [OrangeBus, BlueBus])

    orange_thread = Thread(target=START_ORANGE_BUS, args=(GPS_LRU, ADIRU_LRU,))
    FMC_LRU = FMC(bus_speed, "FIFO", [BlueBus, PurpleBus, GreenBus])

    blue_thread = Thread(target=START_BLUE_BUS, args=(ADIRU_LRU, FMC_LRU,))

    purple_green_thread = Thread(target=START_channel_a_n_b, args=(FMC_LRU,))

    orange_thread.start()
    blue_thread.start()
    purple_green_thread.start()

    orange_thread.join()
    blue_thread.join()
    purple_green_thread.join()

if __name__ == '__main__':
    main()