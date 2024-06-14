from arinc429_voltage_sim import binary_to_voltage as b2v
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
import numpy as np
from time import time, sleep

class full_authority_engine_control:

    applicable_labels_BCD = {
        0o046: 'Engine Serial No. (LSDs)', # -> BCD
        0o047: 'Engine Serial No. (MSDs)', # -> BCD
    }
    applicable_labels_DISC = {
        0o270: 'Discrete Data #1', # -> DISC
        0o271: 'Discrete Data #2', # -> DISC
        0o272: 'Discrete Data #3', # -> DISC
        0o273: 'Discrete Data #4', # -> DISC
        0o274: 'Discrete Data #5', # -> DISC
        0o275: 'Discrete Data #6', # -> DISC
        0o350: 'Maintenance Data #1', # -> DISC
        0o351: 'Maintenance Data #2', # -> DISC
        0o352: 'Maintenance Data #3', # -> DISC
        0o353: 'Maintenance Data #4', # -> DISC
        0o354: 'Maintenance Data #5', # -> DISC
    }
    applicable_labels_BNR = {
        0o114: 'Selected Ambient Static Pressure', # -> BNR
        0o127: 'Fan Discharge Static Pressure', # -> BNR
        0o130: 'Selected Total Air Temperature', # -> BNR
        0o133: 'Selected Throttle Lever Angle', # -> BNR
        0o134: 'Throttle Lever Angle', # -> BNR
        0o137: 'Selected Thrust Reverser Position', # -> BNR
        0o155: 'Maintenance Data #6', # -> DISC
        0o156: 'Maintenance Data #7', # -> DISC
        0o157: 'Maintenance Data #8', # -> DISC
        0o160: 'Maintenance Data #9', # -> DISC
        0o161: 'Maintenance Data #10', # -> DISC
        0o203: 'Ambient Static Pressure', # -> BNR
        0o205: 'Mach Number', # -> BNR
        0o211: 'Total Fan Inlet Temperature', # -> BNR
        0o244: 'Fuel Mass Flow', # -> BNR
        0o260: 'LP Turbine Discharge Temperature', # -> BNR
        0o261: 'LP Turbine Inlet Pressure', # -> BNR
        0o262: 'HP Compressor Inlet Total Pressure', # -> BNR
        0o263: 'Selected Compressor Inlet Temperature (Total)', # -> BNR
        0o264: 'Selected Compressor Discharge Temperature', # -> BNR
        0o265: 'Selected Compressor Discharge Temperature', # -> BNR
        0o267: 'HP Compressor Inlet Temperature (Total)', # -> BNR
        0o300: 'ECU Internal Temperature', # -> BNR
        0o301: 'Demanded Fuel Metering Valve Position', # -> BNR
        0o302: 'Demanded Variable Stator Vane Position', # -> BNR
        0o303: 'Demanded Variable Bleed Valve Position', # -> BNR
        0o304: 'Demanded HPT Clearance Valve Position', # -> BNR
        0o305: 'Demanded LPT Clearance Valve Position', # -> BNR
        0o316: 'Engine Oil Temperature', # -> BNR
        0o321: 'Exhaust gas Temperature (Total)', # -> BNR
        0o322: 'Total Compressor Discharge Temperature', # -> BNR
        0o323: 'Variable Stator Vane Position', # -> BNR
        0o324: 'Selected Fuel Metering Valve Position', # -> BNR
        0o325: 'Selected Fuel Metering Vane Position', # -> BNR
        0o327: 'Compressor Discharge Static Pressure', # -> BNR
        0o330: 'Fuel Metering Valve Position', # -> BNR
        0o331: 'Selected HPT Clearance Valve Postion', # -> BNR
        0o335: 'Selected Variable Bleed Valve Position', # -> BNR
        0o336: 'Variable Bleed Value Position', # -> BNR
        0o337: 'HPT Clearance Valve Position', # -> BNR
        0o341: 'Command Fan Speed', # -> BNR
        0o342: 'Maximum Allowed Fan Speed', # -> BNR
        0o343: 'Maximum Allowed Fan Speed', # -> BNR
        0o344: 'Selected Actual Core Speed', # -> BNR
        0o345: 'Selected Exhaust Gas Temperature (Total)', # -> BNR
        0o346: 'Selected Actual Fan Speed', # -> BNR
        0o347: 'LPT Clearance Valve Position', # -> BNR
        0o360: 'Throttle Rate of Change', # -> BNR
        0o361: 'Derivative of Thrust vs. N1', # -> BNR
        0o363: 'Corrected Thrust', # -> BNR
        0o372: 'Actual Fan Speed', # -> BNR
        0o373: 'Actual Core Speed', # -> BNR
        0o374: 'Left Thrust Reverser Position', # -> BNR
        0o375: 'Right Thrust Reverser Position' # -> BNR
    }

    def __init__(self, bus_speed, wingCardinality, serial_no = 000000, BUS_CHANNELS = []):
        if(bus_speed.lower() == "high"):
            self.word_generator_obj = b2v(True)
        elif(bus_speed.lower() == "low"):
            self.word_generator_obj = b2v(False)
        else:
            raise ValueError("Speed must be either 'high' or 'low'")

        self.receive_chip = lru_rxr(bus_speed, BUS_CHANNELS)
        # Bus channel a and b:
        self.BUS_CHNNELS = BUS_CHANNELS
        self.usec_start = time()
        self.bus_speed = bus_speed

        # Unique attributes
        self.serial_no = serial_no
        self.wingCardinality = wingCardinality

    def __str__(self):
        engine_str = f"Engine Serial Number: {self.serial_no}"
        engine_str += f"\nOn {self.wingCardinality.lower()} wing"
        for label in self.applicable_labels_BNR:
            # this class replaces data at each label as it is recieved
            engine_str += f"\n{oct(label)} data: " + self.applicable_labels_BNR[label]
        return(engine_str)

    def decode_word(self, word:str):
        label = self.receive_chip.get_label_from_word(int(word,2))
        print(oct(label))

        if(label == 0o046): # Engine Serial No. (LSDs), BCD
            lower_half = self.serial_number_decoder(word)
            # grab the upper half:
            MSBs = int(self.serial_no / 1000) * 1000
            self.serial_no = int(MSBs + lower_half)
            """
            if(self.serial_no < 1_000):
                # First time set
                self.serial_no = lower_half
            else:
                # MSB came across first
                self.serial_no += lower_half
            """
        elif label == 0o047: # Engine Serial No. (MSDs), BCD
            # Get the lower half:
            LSBs = self.serial_no % 1000
            # Decimal shift over by three
            upper_half = self.serial_number_decoder(word) * 1000
            self.serial_no = int(upper_half + LSBs)
            """
            if(self.serial_no < 1_000): # The lower half may have been set.
                self.serial_no += upper_half
            else:
                self.serial_no = upper_half
            """
        elif label >= 0o270 and label <= 0o275: # Discrete Data #1-6, DISC
            """ # save this for later
            # Discrete Data #2, DISC
            elif :
                pass
            # Discrete Data #3, DISC
            elif label == 0o272:
                pass
            # Discrete Data #4, DISC
            elif label == 0o273:
                pass
            # Discrete Data #5, DISC
            elif label == 0o274:
                pass
            # Discrete Data #6, DISC
            elif label == 0o275:
                pass
            """
            # should be 0o270, 0o271, 0o272, 0o273, 0o274, and 0o275
            print(f"ACK recv'd discrete data: {word[8:30]}")
        elif label >= 0o350 and label <= 0o354: # Maintenance Data #1-5, DISC
            # should be 0o350, 0o351, 0o352, 0o353, and 0o354
            print(f"ACK recv'd Maintenance data: {word[8:30]}")
            """ # save for later
            # Maintenance Data #2, DISC
            elif label == 0o351:
                pass
            # Maintenance Data #3, DISC
            elif label == 0o352:
                pass
            # Maintenance Data #4, DISC
            elif label == 0o353:
                pass
            # Maintenance Data #5, DISC
            elif label == 0o354:
                pass
            """
        # Selected Ambient Static Pressure, BNR
        elif label == 0o114:
            pass
        # Fan Discharge Static Pressure, BNR
        elif label == 0o127:
            pass
        # Selected Total Air Temperature, BNR
        elif label == 0o130:
            pass
        # Selected Throttle Lever Angle, BNR
        elif label == 0o133:
            pass
        # Throttle Lever Angle, BNR
        elif label == 0o134:
            pass
        # Selected Thrust Reverser Position, BNR
        elif label == 0o137:
            pass
        # Maintenance Data #6, DISC
        elif label == 0o155:
            pass
        # Maintenance Data #7, DISC
        elif label == 0o156:
            pass
        # Maintenance Data #8, DISC
        elif label == 0o157:
            pass
        # Maintenance Data #9, DISC
        elif label == 0o160:
            pass
        # Maintenance Data #10, DISC
        elif label == 0o161:
            pass
        # Ambient Static Pressure, BNR
        elif label == 0o203:
            pass
        # Mach Number, BNR
        elif label == 0o205:
            pass
        # Total Fan Inlet Temperature, BNR
        elif label == 0o211:
            pass
        # Fuel Mass Flow, BNR
        elif label == 0o244:
            pass
        # LP Turbine Discharge Temperature, BNR
        elif label == 0o260:
            pass
        # LP Turbine Inlet Pressure, BNR
        elif label == 0o261:
            pass
        # HP Compressor Inlet Total Pressure, BNR
        elif label == 0o262:
            pass
        # Selected Compressor Inlet Temperature (Total), BNR
        elif label == 0o263:
            pass
        # Selected Compressor Discharge Temperature, BNR
        elif label == 0o264:
            pass
        # Selected Compressor Discharge Temperature, BNR
        elif label == 0o265:
            pass
        # HP Compressor Inlet Temperature (Total), BNR
        elif label == 0o267:
            pass
        # ECU Internal Temperature, BNR
        elif label == 0o300:
            pass
        # Demanded Fuel Metering Valve Position, BNR
        elif label == 0o301:
            pass
        # Demanded Variable Stator Vane Position, BNR
        elif label == 0o302:
            pass
        # Demanded Variable Bleed Valve Position, BNR
        elif label == 0o303:
            pass
        # Demanded HPT Clearance Valve Position, BNR
        elif label == 0o304:
            pass
        # Demanded LPT Clearance Valve Position, BNR
        elif label == 0o305:
            pass
        # Engine Oil Temperature, BNR
        elif label == 0o316:
            pass
        # Exhaust gas Temperature (Total), BNR
        elif label == 0o321:
            pass
        # Total Compressor Discharge Temperature, BNR
        elif label == 0o322:
            pass
        # Variable Stator Vane Position, BNR
        elif label == 0o323:
            pass
        # Selected Fuel Metering Valve Position, BNR
        elif label == 0o324:
            pass
        # Selected Fuel Metering Vane Position, BNR
        elif label == 0o325:
            pass
        # Compressor Discharge Static Pressure, BNR
        elif label == 0o327:
            pass
        # Fuel Metering Valve Position, BNR
        elif label == 0o330:
            pass
        # Selected HPT Clearance Valve Position, BNR
        elif label == 0o331:
            pass
        # Selected Variable Bleed Valve Position, BNR
        elif label == 0o335:
            pass
        # Variable Bleed Value Position, BNR
        elif label == 0o336:
            pass
        # HPT Clearance Valve Position, BNR
        elif label == 0o337:
            pass
        # Command Fan Speed, BNR
        elif label == 0o341:
            pass
        # Maximum Allowed Fan Speed, BNR
        elif label == 0o342:
            pass
        # Maximum Allowed Fan Speed, BNR
        elif label == 0o343:
            pass
        # Selected Actual Core Speed, BNR
        elif label == 0o344:
            pass
        # Selected Exhaust Gas Temperature (Total), BNR
        elif label == 0o345:
            pass
        # Selected Actual Fan Speed, BNR
        elif label == 0o346:
            pass
        # LPT Clearance Valve Position, BNR
        elif label == 0o347:
            pass
        # Throttle Rate of Change, BNR
        elif label == 0o360:
            pass
        # Derivative of Thrust vs. N1, BNR
        elif label == 0o361:
            pass
        # Corrected Thrust, BNR
        elif label == 0o363:
            pass
        # Actual Fan Speed, BNR
        elif label == 0o372:
            pass
        # Actual Core Speed, BNR
        elif label == 0o373:
            pass
        # Left Thrust Reverser Position, BNR
        elif label == 0o374:
            pass
        # Right Thrust Reverser Position, BNR
        elif label == 0o375:
            pass
        else:
            print('Label not found.')

        if(self.serial_no >= 1_000_000):
            raise ValueError("Serial number too high")

    def serial_number_decoder(self, word:str)->int:
        dig1 = int(word[14:18][::-1],2)
        dig2 = int(word[18:22][::-1],2)
        dig3 = int(word[22:26][::-1],2)
        half_serial_num = int(str(dig3) + str(dig2) + str(dig1))
        return(half_serial_num)

        """
        # Check if words are same
        # Check label of word
        # if the label is in any of the applicable labels:
        #       see which label it is;
        #       do what the label wants (actuation)
        # else; ignore
        if(self.check_if_words_same(self.word_channelA, self.word_channelB)):
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
                self.engine_serial_no(self,"LSD")
            elif(label == 0o047):
                self.engine_serial_no(self,"MSB")
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
                                                                                        self.word_generator_obj.get_speed())

        return(word_as_int)

    def recieve_single_voltage_from_wire(self):
        # Get from program queue

        pass
    """