from arinc429_voltage_sim import binary_to_voltage as b2v
import numpy as np
from time import time, sleep

class full_authority_engine_control:

    applicable_labels_BCD = {
        0o046: 'BCD', # Engine Serial No. (LSDs) -> BCD
        0o047: 'BCD', # Engine Serial No. (MSDs) -> BCD
    }
    applicable_labels_DISC = {
        0o270: 'DISC', # Discrete Data #1 -> DISC
        0o271: 'DISC', # Discrete Data #2 -> DISC
        0o272: 'DISC', # Discrete Data #3 -> DISC
        0o273: 'DISC', # Discrete Data #4 -> DISC
        0o274: 'DISC', # Discrete Data #5 -> DISC
        0o275: 'DISC', # Discrete Data #6 -> DISC
        0o350: 'DISC', # Maintenance Data #1 -> DISC
        0o351: 'DISC', # Maintenance Data #2 -> DISC
        0o352: 'DISC', # Maintenance Data #3 -> DISC
        0o353: 'DISC', # Maintenance Data #4 -> DISC
        0o354: 'DISC', # Maintenance Data #5 -> DISC
    }
    applicable_labels_BNR = {
        0o114: 'BNR', # Selected Ambient Static Pressure -> BNR
        0o127: 'BNR', # Fan Discharge Static Pressure -> BNR
        0o130: 'BNR', # Selected Total Air Temperature -> BNR
        0o133: 'BNR', # Selected Throttle Lever Angle -> BNR
        0o134: 'BNR', # Throttle Lever Angle -> BNR
        0o137: 'BNR', # Selected Thrust Reverser Position -> BNR
        0o155: 'BNR', # Maintenance Data #6 -> DISC
        0o156: 'BNR', # Maintenance Data #7 -> DISC
        0o157: 'BNR', # Maintenance Data #8 -> DISC
        0o160: 'BNR', # Maintenance Data #9 -> DISC
        0o161: 'BNR', # Maintenance Data #10 -> DISC
        0o203: 'BNR', # Ambient Static Pressure -> BNR
        0o205: 'BNR', # Mach Number -> BNR
        0o211: 'BNR', # Total Fan Inlet Temperature -> BNR
        0o244: 'BNR', # Fuel Mass Flow -> BNR
        0o260: 'BNR', # LP Turbine Discharge Temperature -> BNR
        0o261: 'BNR', # LP Turbine Inlet Pressure -> BNR
        0o262: 'BNR', # HP Compressor Inlet Total Pressure -> BNR
        0o263: 'BNR', # Selected Compressor Inlet Temperature (Total) -> BNR
        0o264: 'BNR', # Selected Compressor Discharge Temperature -> BNR
        0o265: 'BNR', # Selected Compressor Discharge Temperature -> BNR
        0o267: 'BNR', # HP Compressor Inlet Temperature (Total) -> BNR
        0o300: 'BNR', # ECU Internal Temperature -> BNR
        0o301: 'BNR', # Demanded Fuel Metering Valve Position -> BNR
        0o302: 'BNR', # Demanded Variable Stator Vane Position -> BNR
        0o303: 'BNR', # Demanded Variable Bleed Valve Position -> BNR
        0o304: 'BNR', # Demanded HPT Clearance Valve Position -> BNR
        0o305: 'BNR', # Demanded LPT Clearance Valve Position -> BNR
        0o316: 'BNR', # Engine Oil Temperature -> BNR
        0o321: 'BNR', # Exhaust gas Temperature (Total -> BNR
        0o322: 'BNR', # Total Compressor Discharge Temperature -> BNR
        0o323: 'BNR', # Variable Stator Vane Position -> BNR
        0o324: 'BNR', # Selected Fuel Metering Valve Position -> BNR
        0o325: 'BNR', # Selected Fuel Metering Vane Position -> BNR
        0o327: 'BNR', # Compressor Discharge Static Pressure -> BNR
        0o330: 'BNR', # Fuel Metering Valve Position -> BNR
        0o331: 'BNR', # Selected HPT Clearance Valve Postion -> BNR
        0o335: 'BNR', # Selected Variable Bleed Valve Position -> BNR
        0o336: 'BNR', # Variable Bleed Value Position -> BNR
        0o337: 'BNR', # HPT Clearance Valve Position -> BNR
        0o341: 'BNR', # Command Fan Speed -> BNR
        0o342: 'BNR', # Maximum Allowed Fan Speed -> BNR
        0o343: 'BNR', # N1 Command vs. TLA -> BNR
        0o344: 'BNR', # Selected Actual Core Speed -> BNR
        0o345: 'BNR', # Selected Exhaust Gas Temperature (Total) -> BNR
        0o346: 'BNR', # Selected Actual Fan Speed -> BNR
        0o347: 'BNR', # LPT Clearance Valve Position -> BNR
        0o360: 'BNR', # Throttle Rate of Change -> BNR
        0o361: 'BNR', # Derivative of Thrust vs. N1 -> BNR
        0o363: 'BNR', # Corrected Thrust -> BNR
        0o372: 'BNR', # Actual Fan Speed -> BNR
        0o373: 'BNR', # Actual Core Speed -> BNR
        0o374: 'BNR', # Left Thrust Reverser Position -> BNR
        0o375: 'BNR' # Right Thrust Reverser Position -> BNR
    }

    def __init__(self, speed, serial_no = 0b11110000):
        self.usec_start = time()
        self.word_channelA = 0b0
        self.word_channelB = 0b0
        if(speed.lower() == "high"):
            self.word_generator_obj = b2v(True)
        elif(speed.lower() == "low"):
            self.word_generator_obj = b2v(False)
        else:
            raise ValueError("Speed must be either 'high' or 'low'")

        self.serial_no = serial_no

    def __str__(self):
        pass

    def decode_words(self):
        # Check if words are same
        # Check label of word
        # if the label is in any of the applicable labels:
        #       see which label it is;
        #       do what the label wants (actuation)
        # else; ignore
        if(check_if_words_same(self.word_channelA, self.word_channelB)):
            # words are the same
            true_word = self.word_channelA
            word_bitstr = bin(true_word)[2:]
            if(len(word_bitstr) < 32):
                word_bitstr = "0" * (32 - len(word_bitstr)) + word_bitstr
            label = word_bitstr[8:0] # see if this actually reverses...
            self.check_labels(label)
        else: # do nothing
            pass

    def check_labels(self,label):
        # BCD
        if(label in self.applicable_labels_BCD):
            if(label == 0o046):
                engine_serial_no(self,"LSD")
            elif(label == 0o047):
                engine_serial_no(self,"MSB")
        # DISC
        elif(label in self.applicable_labels_DISC):
            pass # TODO
        # BNR
        elif(label in self.applicable_labels_BNR):
            pass # TODO
        else:
            pass # ignore word.

    # 0o046: 'BCD', # Engine Serial No. (LSDs) -> BCD
    def engine_serial_no(self,sigdigs):
        if(sigdigs == "MSD"):
            print(f"ENGINE SERIAL NO. MSD DEBUG: {bin(self.serial_no)[0:4]}")
        elif(sigdigs == "LSD"):
            print(f"ENGINE SERIAL NO. LSD DEBUG: {bin(self.serial_no)[5:]}")

    def check_if_words_same(self, word_channelA, word_channelB):
        if(word_channelA == word_channelB):
            return True
        return False

    # TODO: test this.
    def convert_RXd_voltages_to_word(self):
        word_bitStr = ""

        ts = np.array([])
        vs = np.array([])

        while(len(word_bitStr).replace("0b","") < 32):
            current_time_in_usec = time() - self.usec_start
            ts = np.concatenate((ts, current_time_in_usec))
            vs = np.concatenate((vs, self.recieve_single_voltage_from_wire()))

            word_as_int, word_bitStr = self.word_generator_obj.from_voltage_to_bin_word((ts, vs),
                                                                    word_generator_obj.get_speed())

        return(word_as_int)

    def recieve_single_voltage_from_wire(self):
        # Get from program queue

        pass