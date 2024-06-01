import threading
import time

from FMC_LRU_Simulator import flight_management_computer
from EEC_LRU_Simulator import Full_Authority_Engine_Control, BusError

def main():
    # Create an instance of the Flight Management Computer (FMC)
    Flight_Management_Computer = flight_management_computer(scheduled_mode=False)
    # This should now be sending data on channel A and B
    # This should now be recieveing data from the ADIRU

    # Create instances of the Full Authority Engine Controllers for Left and Right engines.
    FAEC_LRU_Lefty_Engine = Full_Authority_Engine_Control()
    # This should be listening on channel A and B
    FAEC_LRU_Right_Engine = Full_Authority_Engine_Control()
    # This should be listening on channel A and B

if __name__ == '__main__':
    main()