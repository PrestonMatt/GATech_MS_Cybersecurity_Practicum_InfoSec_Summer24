# Import Python modules
from threading import Thread
from time import sleep, time
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
    pass

def START_ORANGE_BUS(GPS_LRU:GPS, ADIRU_LRU:ADIRU):
    pass

def START_channel_a_n_b(FMC_LRU:FMC):
    RMS_LRU = RMS(bus_speed, [PurpleBus, GreenBus])
    FAEC_1_LRU = FAEC(bus_speed, "left",1,[PurpleBus, GreenBus])
    FAEC_2_LRU = FAEC(bus_speed, "right",2,[PurpleBus, GreenBus])
    WnBS_LRU = WnBS(bus_speed, [PurpleBus, GreenBus])

    #START_PURPLE_BUS(FMC_LRU, RMS_LRU, FAEC_1_LRU, FAEC_2_LRU, WnBS_LRU)
    #START_GREEN_BUS(FMC_LRU, RMS_LRU, FAEC_1_LRU, FAEC_2_LRU, WnBS_LRU)

    # Start the FMC_LRU send words
    #sendFMCwords = Thread(FMC_LRU.FIFO_mode())

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

    START_ORANGE_BUS(GPS_LRU, ADIRU_LRU)

    FMC_LRU = FMC(bus_speed, "FIFO", [BlueBus, PurpleBus, GreenBus])

    START_BLUE_BUS(ADIRU_LRU, FMC_LRU)

    START_channel_a_n_b(FMC_LRU)

if __name__ == '__main__':
    main()