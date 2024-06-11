from arinc429_voltage_sim import binary_to_voltage as b2v
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from BusQueue_Simulator import GlobalBus as ARINC429BUS

from time import sleep, time

class weight_and_balance_system:
    # Responsible for making plane go left and right
    # also manages fuel balancing and center of gravity

    # BTW CG or C/G = center of gravity
    applicable_labels_BCD = {
        0o052: 'Longitude Zero Fuel CG', #
        0o056: 'Gross Weight (KG)', #
        0o052: 'Longitude Zero Fuel CG', #
        0o060: 'Tire Loading (Left Body Main)', #
        0o061: 'Tire Loading (Right Body Main)', #
        0o062: 'Tire Loading (Left Wing Main)', #
        0o063: 'Tire Loading (Right Wing Main)', #
        0o064: 'Tire Loading (Nose)', #
        0o065: 'Gross Weight', #
        0o066: 'Longitudinal Center of Gravity', #
        0o067: 'Lateral Center of Gravity', #
        0o167: 'Zero Fuel Weight (lb)', #
        0o243: 'Zero Fuel Weight (kg)', #
    }
    applicable_labels_DISC = {
        0o270: 'Discrete Data #1', #
        0o357: 'ISO Alphabet #5 Message' #
    }
    applicable_labels_BNR = {
        0o054: 'Zero Fuel Weight (KG)', #
        0o070: 'Hard landing Magnitude #1', #
        0o071: 'Hard landing Magnitude #2', #
        0o074: 'Zero Fuel Weight (lb)', #
        0o075: 'Gross Weight', #
        0o076: 'Longitudinal Center of Gravity', #
        0o077: 'Lateral Center of Gravity', #
        0o100: 'Gross Weight (Kilogram)', #
        0o103: 'Left Outboard Flap Position',
        0o104: 'Right Outboard Flap Postion',
        0o107: 'Longitude Zero Fuel C/G' #
    }

    def __init__(self, bus_speed = "low", BUS_CHANNELS = []):
        self.usec_start = time()
        self.word_channelA = 0b0
        self.word_channelB = 0b0
        if(bus_speed.lower() == "high"):
            self.word_generator_obj = b2v(True)
        elif(bus_speed.lower() == "low"):
            self.word_generator_obj = b2v(False)
        else:
            raise ValueError("Speed must be either 'high' or 'low'")

        self.BUS_CHANNELS = BUS_CHANNELS

        self.receive_chip = lru_rxr(bus_speed, BUS_CHANNELS)

    def __str__(self):
        pass

    def decode_word(self, word:str):
        label = self.receive_chip.get_label(word)

        if(label == 0o103):
            print("Adjusting pitch")
        elif(label == 0o104):
            print("Adjusting pitch")
