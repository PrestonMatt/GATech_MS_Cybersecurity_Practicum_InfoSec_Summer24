import os
#import PyARINC429.arinc429
#import arinc429
from arinc429_voltage_sim import binary_to_voltage as b2v
from threading import Thread
import ARINC429_Client_Server
#from pwn import *

"""
    Windows:
    Copy-paste the subfolder arinc429 from https://github.com/aeroneous/PyARINC429/tree/master
    into C:\\Users\\<user name>\\AppData\\Local\\Programs\Python\Python312\Lib

    Otherwise put it in a subdir from this file and have the line:
    import PyARINC429.arinc429
"""

class BusError(Exception):
    """Warning Channel A and Channel B not congruent"""
    pass

class Full_Authority_Engine_Control:

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

    # engine: 76,100 pounds of thrust max
    # https://thepointsguy.com/guide/powering-the-dreamliner-how-the-787s-genx-engines-work/
    # 1lb of thrust = 32 feet per second per second acceleration or 9.8m/s^s

    # https://en.wikipedia.org/wiki/Boeing_787_Dreamliner
    # Operating empty weight is 298,700 lb / 135,500 kg

    def __init__(self, channel_a_ip, channel_b_ip, channel_a_port, channel_b_port):
        self.channel_a_ip = channel_a_ip
        self.channel_b_ip = channel_b_ip
        self.channel_b_port = channel_b_port
        self.channel_a_port = channel_a_port
        self.RXd_voltages = []
        pass

    """
        Start listening simultaneously on both channels.
    """
    def listen_on_channels(self):
        # Start listening on channels A and B
        Thread(target=self._listen_channel_a).start()
        Thread(target=self._listen_channel_b).start()

    """
        Listen for words on channel A.
    """
    def _listen_channel_a(self):
        def voltage_reporter(voltage):
            word = self._from_voltage_to_bin_word(voltage)
            if word:
                self.received_word_a = word
                self._check_words()

        client_a = ARINC429_Client_Server(client_or_server=True, client_ip=self.channel_a_ip, client_port=self.channel_a_port)
        client_a.client(voltage_reporter)

    def _listen_channel_b(self):
        """Listen for words on channel B"""
        def voltage_reporter(voltage):
            word = self._from_voltage_to_bin_word(voltage)
            if word:
                self.received_word_b = word
                self._check_words()

        client_b = ARINC429_Client_Server(client_or_server=True, client_ip=self.channel_b_ip, client_port=self.channel_b_port)
        client_b.client(voltage_reporter)

    def _from_voltage_to_bin_word(self, voltage):
        #"""Convert received voltage to binary word"""
        # TODO
        # Implement the logic to convert voltage to binary word
        # Placeholder implementation, replace with actual logic
        return voltage  # This should return the binary word

    """Check if received words from both channels are the same"""
    def _check_words(self):
        if self.received_word_a is not None and self.received_word_b is not None:
            if self.received_word_a == self.received_word_b:
                binary_word = self.received_word_a
                self.received_word_a = None
                self.received_word_b = None
                self._process_word(binary_word)
            else:
                self.received_word_a = None
                self.received_word_b = None
                raise BusError("Channel words are different")

    """
        Process the binary word
    """
    def _process_word(self, binary_word):

        code = binary_word >> 24  # Extract the first 8 bits as the code
        if code in self.code_table:
            data = (binary_word >> 3) & 0x1FFFFF  # Extract bits 11 to 29
            thrust = self._calculate_thrust(data)
            print(f"Thrust: {thrust}")
        else:
            print("Code not in code table")

    def _calculate_thrust(self, data):
        """Calculate thrust based on data"""
        # Placeholder implementation, replace with actual calculation
        return data  # This should return the calculated thrust