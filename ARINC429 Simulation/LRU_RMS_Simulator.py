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
        0o032: "ADF Frequency",
        0o261: "Flight Number Word",
        0o230: "True Airspeed"
    }
    applicable_labels_DISC = {
        0o033: "Frequency (Hz)",
        0o034: "VOR/ILS Frequency",
        0o035: "DME Frequency",
        0o037: "HF COM Frequency",
        0o205: "HF COM Frequency (alt.)",
        0o150: "UTC",
        0o214: "ICAO Address no. 1",
        0o216: "ICAO Address no. 2"
    }
    applicable_labels_BNR = {
        0o101: "Selected Heading",
        0o102: "Selected Altitude", #
        0o103: "Selected Airspeed", # Deg/180 [-180,180], res: 0.25 deg
        0o142: "UTC",
        0o203: "Altitude", # Feet, [0,131,071], res: ~1 ft
        0o206: "Computed Airspeed", # Knots [0,1024], res ~ 0.25
        0o210: "True Airspeed", # Knots [0,2048], res ~ 0.25
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
        print(label)
        print(word)

        if label == 0o010: # Latitude (Present Position)
            print("HI")
            num1 = word[9:12]
            num2 = word[13:16]
            num3 = word[17:20]
            num4 = word[21:24]
            num5 = word[26:28]
            is_north = (word[29] == 0)
            ssm = word[30:31] # BCD ->
            if(ssm == "00"):
                # Failure Warning
                self.set_ADS_B_Message("Emergency Status","Failure Warning")
        elif label == 0o011:
            pass  # Longitude (Present Position)
        elif label == 0o310:
            pass  # Latitude (Present Position)
        elif label == 0o311:
            pass  # Longitude (Present Position)
        elif label == 0o012:
            pass  # Ground Speed
        elif label == 0o312:
            pass  # Ground Speed
        elif label == 0o013:
            pass  # Track Angle
        elif label == 0o020:
            pass  # Selected Vertical Speed
        elif label == 0o023:
            pass  # Selected Heading
        elif label == 0o025:
            pass  # Selected Altitude
        elif label == 0o032:
            pass  # ADF Frequency
        elif label == 0o261:
            pass  # Flight Number Word
        elif label == 0o230:
            pass  # True Airspeed
        elif label == 0o210:
            pass  # True Airspeed
        elif label == 0o033:
            pass  # Frequency (Hz)
        elif label == 0o034:
            pass  # VOR/ILS Frequency
        elif label == 0o035:
            pass  # DME Frequency
        elif label == 0o037:
            pass  # HF COM Frequency
        elif label == 0o205:
            pass  # HF COM Frequency (alt.)
        elif label == 0o150:
            pass  # UTC
        elif label == 0o214:
            pass  # ICAO Address no. 1
        elif label == 0o216:
            pass  # ICAO Address no. 2
        elif label == 0o101:
            pass  # Selected Heading
        elif label == 0o102:
            pass  # Selected Altitude
        elif label == 0o103:
            pass  # Selected Airspeed
        elif label == 0o142:
            pass  # UTC
        elif label == 0o203:
            pass  # Altitude
        elif label == 0o206:
            pass  # Computed Airspeed
        elif label == 0o313:
            pass  # Track Angle True
        elif label == 0o314:
            pass  # True Heading
        elif label == 0o320:
            pass  # Magnetic Heading
        else:
            pass  # Label not found -> do nothing

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