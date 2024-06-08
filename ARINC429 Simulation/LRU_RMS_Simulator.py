# My Classes
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
#from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
# Python Classes
from time import sleep, time
from threading import Thread
from queue import Queue

class radio_management_system:

    applicable_labels_BCD = {
        0o010: "Latitude (Present Position)", # Deg: Min [180N - 180S] POS SENSE: N, Res: 0.1
        0o011: "Longitude (Present Position)", # Deg: Min [180E - 180W] POS SENSE: E, Res: 0.1
        0o012: "Ground Speed",
        0o013: "Track Angle",
        0o020: "Selected Vertical Speed",
        0o023: "Selected Heading",
        0o025: "Selected Altitude",
        #0o026: "Selected Airspeed",
        0o032: "ADF Frequency",
        #0o125: "UTC",
        0o261: "Flight Number Word",
        #0o230: "True Airspeed"
    }
    applicable_labels_DISC = {
        0o033: "Frequency (Hz)",
        0o034: "VOR/ILS Frequency",
        0o035: "DME Frequency",
        0o037: "HF COM Frequency",
        0o205: "HF COM Frequency (alt.)",
        #0o150: "UTC",
        0o214: "ICAO Address no. 1",
        0o216: "ICAO Address no. 2"
    }
    applicable_labels_BNR = {
        0o101: "Selected Heading",
        0o102: "Selected Altitude", #
        #0o103: "Selected Airspeed", # Deg/180 [-180,180], res: 0.25 deg
        #0o142: "UTC",
        0o203: "Altitude", # Feet, [0,131,071], res: ~1 ft
        #0o206: "Computed Airspeed", # Knots [0,1024], res ~ 0.25
        #0o210: "True Airspeed", # Knots [0,2048], res ~ 0.25
        0o310: "Latitude (Present Position)",
        0o311: "Longitude (Present Position)",
        0o312: "Ground Speed",
        0o313: "Track Angle True", # Deg/180 [-180,180], res: 0.05 deg
        0o314: "True Heading", # Deg/180 [-180,180], res: 0.05 deg
        0o320: "Magnetic Heading" # Deg/180 [-180,180], res: 0.05 deg
    }

    def __init__(self, bus_speed = "low", BUS_CHANNELS = []):
        if(bus_speed.lower() == "high"):
            self.binary_voltage_converter = b2v(True)
        elif(bus_speed.lower() == "low"):
            self.binary_voltage_converter = b2v(False)
        else:
            raise ValueError("Speed must be either 'HIGH' or 'LOW'")

        self.equip_ID = 0x036

        # Get bus speed
        self.bus_speed = bus_speed
        # pass bus channels here ->
        # channel a = index 0
        # channel b - index 1
        self.BUS_CHANNELS = BUS_CHANNELS
        # zero out our bus time
        self.usec_start = time()
        # create receive chip object
        self.receive_chip = lru_rxr(bus_speed, BUS_CHANNELS)

        self.frequency = 0.0
        self.VOR_ILS_Frequency = 0.0
        self.DME_Frequency = 0.0
        self.HF_COM_Frequency = 0.0

        self.ADS_B_Message = {
            "Flight Number": None,
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
            "Aircraft Type": "Civilian"
        }

    def __str__(self):
        message_1 = f"Commanded Frequencies:\n\tGeneral:{self.frequency}\n\tVOR/ILS:{self.VOR_ILS_Frequency}\n\tDME:{self.DME_Frequency}\n\tHF_COMM:{self.HF_COM_Frequency}"
        message_2a = "\n\nADS-B Message:"
        message_2b = str(self.ADS_B_Message)
        print(message_1 + message_2a + message_2b)
        return(message_1 + message_2a + message_2b)

    # ADS-B Broadcasts the following information from a plane
    # Flight Number - BCD
    # Latitude - BCD, BNR
    # Longitude - BCD, BNR
    # Altitude - BCD, BNR
    # Ground Speed - BCD, BNR
    # Vertical Speed - BCD
    # Track Angle - BCD
    # Magnetic Heading - BCD
    # Emergency Status -> special.
    # Ident Switch
    #       -> A signal that the pilot can activate to highlight the aircraft on air traffic control screens.
    # ICAO Address - DISC
    # Aircraft Type - NOT OVER BUS
    def decode_word(self,word:str):
        label = self.receive_chip.get_label_from_word(int(word,2))
        #print(oct(label))
        #print(word)

        if label == 0o010: # Latitude (Present Position)
            #print("HI")
            num1 = word[8:12]
            dig_1 = int(num1[::-1],2)
            num2 = word[12:16]
            dig_2 = int(num2[::-1],2)
            num3 = word[16:20]
            dig_3 = int(num3[::-1],2)
            num4 = word[20:24]
            dig_4 = int(num4[::-1],2)
            num5 = word[24:28]
            dig_5 = int(num5[::-1],2)
            num6 = word[28]
            dig_6 = int(num6[::-1],2)
            str6 = ""
            if(dig_6 == 1):
                str6 = "1"
            ssm = word[29:31]
            #print(ssm)
            if(ssm == "00"):
                is_north = "N "
            else:
                is_north = "S "

            #print(f"Number 1: {num1}\nNumber 2: {num2}\nNumber 3: {num3}\nNumber 4: {num4}\nNumber 5: {num5}")
            #print(f"Digit 1: {dig_1}\nDigit 2: {dig_2}\nDigit 3: {dig_3}\nDigit 4: {dig_4}\nDigit 5: {dig_5}")

            self.set_ADS_B_Message("Latitude",
                                   is_north + str6+str(dig_5)+str(dig_4) + " Deg " + str(dig_3)+str(dig_2) + "." + str(dig_1) + "'"
                                   )
        elif label == 0o011: # Longitude (Present Position)
            num1 = word[8:12]
            dig_1 = int(num1[::-1],2)
            num2 = word[12:16]
            dig_2 = int(num2[::-1],2)
            num3 = word[16:20]
            dig_3 = int(num3[::-1],2)
            num4 = word[20:24]
            dig_4 = int(num4[::-1],2)
            num5 = word[24:28]
            dig_5 = int(num5[::-1],2)
            num6 = word[28]
            dig_6 = int(num6[::-1],2)
            str6 = ""
            if(dig_6 == 1):
                str6 = "1"
            ssm = word[29:31]
            #print(ssm)
            if(ssm == "00"):
                is_north = "E "
            else:
                is_north = "W "
            self.set_ADS_B_Message("Latitude",
                                   is_north + str6+str(dig_5)+str(dig_4) + " Deg " + str(dig_3)+str(dig_2) + "." + str(dig_1) + "'"
                                   )
        elif label == 0o310: # Latitude (Present Position)
            SDI = word[8:10]
            data = word[10:28][::-1]
            dir = word[28:31]
            print(int(data,2))
            if(dir == "011"):
                is_north = "N "
            else:
                is_north = "S "
            # TODO: figure this shit out.
            self.set_ADS_B_Message("Latitude",
                                   is_north + "TODO" + "." + "TODO" + " Deg "
                                   )
        elif label == 0o311: # Longitude (Present Position)
            pass
        elif label == 0o012: # Ground Speed
            SDI = word[8:10]
            parity = word[10:14] # Do nothing with these two values

            digits = self.get_digits_BCD(word)

            x1s = digits[1]
            x10s = digits[2]
            x100s = digits[3]
            x1000s = digits[4]

            #print(f"{x1000s}{x100s}{x10s}{x1s}")
            self.set_ADS_B_Message("Ground Speed",int(f"{x1000s}{x100s}{x10s}{x1s}"))
        elif label == 0o312: # Ground Speed
            #SDI = word[8:10]
            data = word[10:27]
            speed = int(data,2)
            #dir = word[28:31]
            #print(speed)
            self.set_ADS_B_Message("Ground Speed",speed)
        elif label == 0o013: # Track Angle
            #SDI = word[8:10]
            #parity = word[10:14] # Do nothing with these two values

            digits = self.get_digits_BCD(word)

            xpoint1s = digits[1]
            x1s = digits[2]
            x10s = digits[3]
            x100s = digits[4]

            angle = float(f"{x100s}{x10s}{x1s}.{xpoint1s}")

            self.set_ADS_B_Message("Track Angle",angle)
        elif label == 0o313: # Track Angle True
            pass
        elif label == 0o020: # Selected Vertical Speed
            digits = self.get_digits_BCD(word)

            x1s = digits[1]
            x10s = digits[2]
            x100s = digits[3]
            x1000s = digits[4]

            #print(f"{x1000s}{x100s}{x10s}{x1s}")

            if(word[29:31] == "11"):
                sign = -1
            else:
                sign = 1

            self.set_ADS_B_Message("Vertical Speed",sign*int(f"{x1000s}{x100s}{x10s}{x1s}"))
        elif label == 0o023: # Selected Heading
            digits = self.get_digits_BCD(word)

            x1s = digits[2]
            x10s = digits[3]
            x100s = digits[4]

            #print(f"{x100s}{x10s}{x1s}")

            if(word[29:31] == "11"):
                sign = -1
            else:
                sign = 1

            self.set_ADS_B_Message("Magnetic Heading",sign*int(f"{x100s}{x10s}{x1s}"))
        elif label == 0o101: # Selected Heading
            pass
        elif label == 0o314: # True Heading
            pass
        elif label == 0o320: # Magnetic Heading
            pass
        elif label == 0o025: # Selected Altitude
            digits = self.get_digits_BCD(word)

            x1s = digits[0]
            x10s = digits[1]
            x100s = digits[2]
            x1000s = digits[3]
            x10000s = digits[4]

            #print(f"{x1000s}{x100s}{x10s}{x1s}")

            self.set_ADS_B_Message("Altitude",int(f"{x10000s}{x1000s}{x100s}{x10s}{x1s}"))
        elif label == 0o102: # Selected Altitude
            pass
        elif label == 0o203: # Altitude
            pass
        elif label == 0o214:
            pass  # ICAO Address no. 1
        elif label == 0o216:
            pass  # ICAO Address no. 2
        elif label == 0o032: # ADF Frequency
            pass
        elif label == 0o033: # Frequency (Hz)
            pass
        elif label == 0o034: # VOR/ILS Frequency
            pass
        elif label == 0o035: # DME Frequency
            pass
        elif label == 0o037: # HF COM Frequency
            pass
        elif label == 0o205: # HF COM Frequency (alt.)
            pass
        elif label == 0o261: # Flight Number Word
            ones_place = word[13:17]
            flt_dig_1 = int(ones_place[::-1],2)
            tens_place = word[17:21]
            flt_dig_2 = int(tens_place[::-1],2)
            hunds_place = word[21:25]
            flt_dig_3 = int(hunds_place[::-1],2)
            thous_place = word[25:29]
            flt_dig_4 = int(thous_place[::-1],2)
            #print(f"x1: {ones_place}\nx10: {tens_place}\nx100: {hunds_place}\nx1000: {thous_place}")
            #print(f"{flt_dig_4}{flt_dig_3}{flt_dig_2}{flt_dig_1}")
            self.set_ADS_B_Message("Flight Number",
                                   int(f"{flt_dig_4}{flt_dig_3}{flt_dig_2}{flt_dig_1}")
                                   )
        else:
            pass  # Label not found -> do nothing

        """
        elif label == 0o026: # True Airspeed
            digits = self.get_digits_BCD(word)
    
            x1s = digits[2]
            x10s = digits[3]
            x100s = digits[4]
    
            #print(f"{x1000s}{x100s}{x10s}{x1s}")
    
            self.set_ADS_B_Message("Altitude",int(f"{x100s}{x10s}{x1s}"))
        elif label == 0o230: # True Airspeed
            pass
        elif label == 0o210: # True Airspeed
            pass
        elif label == 0o103: # Selected Airspeed
            pass
        elif label == 0o206: # Computed Airspeed
            pass
        elif label == 0o125: # UTC
            pass
        elif label == 0o150: # UTC
            pass
        elif label == 0o142: # UTC
            pass
        """

    def get_digits_BCD(self,word:str) -> (int,int,int,int,int):

        optionals_place = word[10:14]
        xOps = int(optionals_place[::-1],2)
        ones_place = word[14:18]
        x1s = int(ones_place[::-1],2)
        tens_place = word[18:22]
        x10s = int(tens_place[::-1],2)
        hunds_place = word[22:26]
        x100s = int(hunds_place[::-1],2)
        thousand_place = word[26:29]
        x1000s = int(thousand_place[::-1],2)

        return(xOps,x1s,x10s,x100s,x1000s)

    def set_DME_frequency(self,frequency:float):
        self.DME_Frequency = frequency

    def set_HF_COM_frequency(self,frequency:float):
        self.HF_COM_Frequency = frequency

    def set_VOR_ILS_frequency(self,frequency:float):
        self.VOR_ILS_Frequency = frequency

    def set_general_frequency(self,frequency:float):
        self.frequency = frequency

    def set_ADS_B_Message(self,ads_b_param:str,ads_b_message):
        try:
            self.ADS_B_Message[ads_b_param] = ads_b_message
        except KeyError:
            print("Error. Data not needed for ADS-B")

    def set_ICAO_Address(self,icao_address:int):
        # 24 bit address
        if(icao_address > 0b111111111111111111111111):
            print("Error. ICAO Address not valid")
        else:
            self.set_ADS_B_Message("ICAO Address", icao_address)