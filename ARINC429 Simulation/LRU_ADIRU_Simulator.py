# My Classes
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
# Python Classes
from time import sleep, time
from threading import Thread
from queue import Queue

class air_data_inertial_reference_unit:

    # Hex Equipment Code: 0x038, ADIRS
    # Hex Equipment Code: 0x0AD, ADIRS Air Data Module

    applicable_labels_BCD = {
        0o010: "Present Position - Latitude",
        0o011: "Present Position - Longitude",
        0o012: "Ground Speed",
        0o013: "Track Angle - True",
        0o014: "Magnetic Heading",
        0o015: "Wind Speed",
        0o016: "Wind Direction - True",
        0o044: "True Heading",
        0o231: "Total Air Temperature",
        0o233: "Static Air Temperature",
        0o234: "Baro Correction (mb) #1",
        0o235: "Baro Correction (ins. Hg) #1",
        0o236: "Baro Correction (mb) #2",
        0o237: "Baro Correction (ins. Hg) #2"
    }
    applicable_labels_DISC = {
        0o242: "Total Pressure",
        0o270: "Discrete Data #1", # Also 0x0AD
        0o271: "Discrete Data #2", # Also 0x0AD
        0o272: "Discrete Data #3", # Also 0x0AD
        0o275: "IR Discrete Word #2",
        0o277: "IR Test",
        0o350: "IRS Maintenance Word #1",
        0o351: "IRS Maintenance Word #2",
        0o353: "IRS Maintenance Word #3",
        0o355: "IRS Maintenance Word #4",

    }
    applicable_labels_BNR = {
        0o052: "Body Pitch Acceleration",
        0o053: "Body Roll Acceleration",
        0o054: "Body Yaw Acceleration",
        0o152: "Cabin Pressure", # Also 0x0AD
        0o176: "Left Static Pressure Uncorrected, mb", # 0x0AD -> Static Pressure Left, Uncorrected, mb
        0o177: "Right Static Pressure Uncorrected, mb", # 0x0AD -> Static Pressure Right, Uncorrected, mb
        0o203: "Altitude (1013.25mB)",
        0o204: "Baro Corrected Altitude #1",
        0o205: "Mach",
        0o207: "Max. Allowable Airspeed",
        0o210: "True Airspeed",
        0o211: "Total Air Temperature", # 0x0AD -> Total Air Temperature Indicated
        0o212: "Altitude Rate",
        0o213: "Static Air Temperature",
        0o215: "Impacted Pressure, Uncorrected, mb", # Also 0x0AD
        0o217: "Static Pressure, Average, Corrected (In. Hg)",
        0o220: "Baro Corrected Altitude #2",
        0o221: "Indicated Angle of Attack (Average)", # Also 0x0AD
        0o230: "True Airspeed",
        0o241: "Corrected Angle of Attack",
        0o242: "Total Pressure", # 0x0AD -> Total Pressure, Uncorrected, mb
        0o245: "Average Static Pressure mb, Uncorrected", # 0x0AD -> Average Static Pressure mb, Uncorrected
        0o246: "Average Static Pressure mb, Corrected",
        0o250: "Indicated Side Slip Angle", # 0x0AD -> Indicated Side Slip Angle or AOS
        0o251: "Baro Corrected Altitude #3",
        0o252: "Baro Corrected Altitude #4",
        0o253: "Corrected Side Slip Angle",
        0o265: "Integrated Vertical Acceleration",
        0o310: "Present Position - Latitude",
        0o311: "Present Position - Longitude",
        0o312: "Ground Speed",
        0o313: "Track Angle - True",
        0o314: "True Heading",
        0o315: "Wind Speed",
        0o316: "Wind Angle",
        0o317: "Track Angle - Magnetic",
        0o320: "Magnetic Heading",
        0o321: "Drift Angle",
        0o322: "Flight Path Angle",
        0o323: "Flight Path Acceleration",
        0o324: "Pitch Angle",
        0o325: "Roll Angle",
        0o326: "Body Pitch Rate",
        0o327: "Body Roll Rate",
        0o330: "Body Yaw Rate",
        0o331: "Body Longitudinal Acceleration",
        0o332: "Body Lateral Acceleration",
        0o333: "Body Normal Acceleration",
        0o334: "Platform Heading",
        0o335: "Track Angle Rate",
        0o336: "Inertial Pitch Rate",
        0o337: "Inertial Roll Rate",
        0o341: "Grid Heading",
        0o360: "Potential Vertical Speed",
        0o361: "Altitude (Inertial)",
        0o362: "Along Track Horizontal Acceleration",
        0o363: "Cross Track Acceleration",
        0o364: "Vertical Acceleration",
        0o365: "Inertial Vertical Velocity (EFI)",
        0o366: "North-South Velocity",
        0o367: "East-West Velocity",
        0o375: "Along Heading Acceleration",
        0o276: "Cross Heading Acceleration"
    }

    def __init__(self, bus_speed="low", BUS_CHANNELS=[]):
        # Set bus start time
        #self.bus_start = time()
        # Set bus channels.
        self.BUS_CHANNELS = BUS_CHANNELS
        # set ADIRU T/Rx bus speed
        self.bus_speed = bus_speed
        # zero the bus clock.
        self.usec_start = time()

        self.TXcommunicator_chip = lru_txr(bus_speed = self.bus_speed,
                                         BUS_CHANNELS = [self.BUS_CHANNELS[0]])
        self.RXcommunicator_chip = lru_rxr(bus_speed = self.bus_speed,
                                         BUS_CHANNELS = [self.BUS_CHANNELS[1]])

        self.data = {
            'Present Position - Latitude': '',
            'Present Position - Longitude': '',
            'Ground Speed': '',
            'Track Angle - True': '',
            'Magnetic Heading': '',
            'Wind Speed': '',
            'Wind Direction - True': '',
            'True Heading': '',
            'Total Air Temperature': '',
            'Static Air Temperature': '',
            'Baro Correction (mb) #1': '',
            'Baro Correction (ins. Hg) #1': '',
            'Baro Correction (mb) #2': '',
            'Baro Correction (ins. Hg) #2': '',
            'Corrected Angle of Attack': '',
            'Total Pressure': '',
            'Discrete Data #1': '',
            'Discrete Data #2': '',
            'Discrete Data #3': '',
            'IR Discrete Word #2': '',
            'IR Test': '',
            'IRS Maintenance Word #1': '',
            'IRS Maintenance Word #2': '',
            'IRS Maintenance Word #3': '',
            'IRS Maintenance Word #4': '',
            'Body Pitch Acceleration': '',
            'Body Roll Acceleration': '',
            'Body Yaw Acceleration': '',
            'Cabin Pressure': '',
            'Left Static Pressure Uncorrected, mb': '',
            'Right Static Pressure Uncorrected, mb': '',
            'Altitude (1013.25mB)': '',
            'Baro Corrected Altitude #1': '',
            'Mach': '',
            'Max. Allowable Airspeed': '',
            'True Airspeed': '',
            'Altitude Rate': '',
            'Impacted Pressure, Uncorrected, mb': '',
            'Static Pressure, Average, Corrected (In. Hg)': '',
            'Baro Corrected Altitude #2': '',
            'Indicated Angle of Attack (Average)': '',
            'Average Static Pressure mb, Uncorrected': '',
            'Average Static Pressure mb, Corrected': '',
            'Indicated Side Slip Angle': '',
            'Baro Corrected Altitude #3': '',
            'Baro Corrected Altitude #4': '',
            'Corrected Side Slip Angle': '',
            'Integrated Vertical Acceleration': '',
            'Wind Angle': '',
            'Track Angle - Magnetic': '',
            'Drift Angle': '',
            'Flight Path Angle': '',
            'Flight Path Acceleration': '',
            'Pitch Angle': '',
            'Roll Angle': '',
            'Body Pitch Rate': '',
            'Body Roll Rate': '',
            'Body Yaw Rate': '',
            'Body Longitudinal Acceleration': '',
            'Body Lateral Acceleration': '',
            'Body Normal Acceleration': '',
            'Platform Heading': '',
            'Track Angle Rate': '',
            'Inertial Pitch Rate': '',
            'Inertial Roll Rate': '',
            'Grid Heading': '',
            'Potential Vertical Speed': '',
            'Altitude (Inertial)': '',
            'Along Track Horizontal Acceleration': '',
            'Cross Track Acceleration': '',
            'Vertical Acceleration': '',
            'Inertial Vertical Velocity (EFI)': '',
            'North-South Velocity': '',
            'East-West Velocity': '',
            'Along Heading Acceleration': '',
            'Cross Heading Acceleration': ''
        }

    def __str__(self):
        return str(self.data)

    def bootup_values(self):
        self.data = {
            'Present Position - Latitude': "N 42 Deg 21.0'",
            'Present Position - Longitude': "W 71 Deg 23.0'",
            'Ground Speed': '',
            'Track Angle - True': '',
            'Magnetic Heading': '',
            'Wind Speed': '',
            'Wind Direction - True': '',
            'True Heading': '',
            'Total Air Temperature': '',
            'Static Air Temperature': '',
            'Baro Correction (mb) #1': '',
            'Baro Correction (ins. Hg) #1': '',
            'Baro Correction (mb) #2': '',
            'Baro Correction (ins. Hg) #2': '',
            'Corrected Angle of Attack': '',
            'Total Pressure': '',
            'Discrete Data #1': '',
            'Discrete Data #2': '',
            'Discrete Data #3': '',
            'IR Discrete Word #2': '',
            'IR Test': '',
            'IRS Maintenance Word #1': '',
            'IRS Maintenance Word #2': '',
            'IRS Maintenance Word #3': '',
            'IRS Maintenance Word #4': '',
            'Body Pitch Acceleration': '',
            'Body Roll Acceleration': '',
            'Body Yaw Acceleration': '',
            'Cabin Pressure': '',
            'Left Static Pressure Uncorrected, mb': '',
            'Right Static Pressure Uncorrected, mb': '',
            'Altitude (1013.25mB)': '',
            'Baro Corrected Altitude #1': '',
            'Mach': '',
            'Max. Allowable Airspeed': '',
            'True Airspeed': '',
            'Altitude Rate': '',
            'Impacted Pressure, Uncorrected, mb': '',
            'Static Pressure, Average, Corrected (In. Hg)': '',
            'Baro Corrected Altitude #2': '',
            'Indicated Angle of Attack (Average)': '',
            'Average Static Pressure mb, Uncorrected': '',
            'Average Static Pressure mb, Corrected': '',
            'Indicated Side Slip Angle': '',
            'Baro Corrected Altitude #3': '',
            'Baro Corrected Altitude #4': '',
            'Corrected Side Slip Angle': '',
            'Integrated Vertical Acceleration': '',
            'Wind Angle': '',
            'Track Angle - Magnetic': '',
            'Drift Angle': '',
            'Flight Path Angle': '',
            'Flight Path Acceleration': '',
            'Pitch Angle': '',
            'Roll Angle': '',
            'Body Pitch Rate': '',
            'Body Roll Rate': '',
            'Body Yaw Rate': '',
            'Body Longitudinal Acceleration': '',
            'Body Lateral Acceleration': '',
            'Body Normal Acceleration': '',
            'Platform Heading': '',
            'Track Angle Rate': '',
            'Inertial Pitch Rate': '',
            'Inertial Roll Rate': '',
            'Grid Heading': '',
            'Potential Vertical Speed': '',
            'Altitude (Inertial)': '',
            'Along Track Horizontal Acceleration': '',
            'Cross Track Acceleration': '',
            'Vertical Acceleration': '',
            'Inertial Vertical Velocity (EFI)': '',
            'North-South Velocity': '',
            'East-West Velocity': '',
            'Along Heading Acceleration': '',
            'Cross Heading Acceleration': ''
        }

    def decode_GPS_word(self, word:str):
        label = self.RXcommunicator_chip.get_label_from_word(int(word,2))
        if(label == 0o010):
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

            self.set_data("Present Position - Latitude",
                                   is_north + str6+str(dig_5)+str(dig_4) + " Deg " + str(dig_3)+str(dig_2) + "." + str(dig_1) + "'"
                                   )
        elif(label == 0o011):
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
            self.set_data("Present Position - Longitude",
                                   is_north + str6+str(dig_5)+str(dig_4) + " Deg " + str(dig_3)+str(dig_2) + "." + str(dig_1) + "'"
                                   )

    def encode_word(self, key:int) -> str:
        # some label like 0o101
        word_label = key
        # converted that label to a string like "00101101"
        word_label_str, _ = self.TXcommunicator_chip.make_label_for_word(word_label)

        data_key = ''
        word_data = ''

        # Getting the actual human representable interpritation of that label.
        # I.E. Ground Speed or Track Angle
        if(word_label in self.applicable_labels_BCD):
            data_key = self.applicable_labels_BCD[word_label]
        elif(word_label in self.applicable_labels_DISC):
            data_key = self.applicable_labels_DISC[word_label]
        elif(word_label in self.applicable_labels_BNR):
            data_key = self.applicable_labels_BNR[word_label]

        # Getting the human represented value for that word
        # i.e. for latitude something like N 75 Deg 59.9'
        word_data = self.data[data_key]

        # Handle error if that hasn't been set yet
        if(word_data == ""):
            return("")

        word_data_str = ""
        # Translating that human redable value to the actual value in the word
        # like "010...101" etc.
        # BCD
        if data_key == 'Present Position - Latitude':
            lat_num = word_data.split(" ")[1]
            lat_deg = word_data.split(" ")[-1].replace("'","")
            lat_NS = word_data.split(" ")[0]
            if(lat_NS == "N"):
                SSM = "00"
            else:
                SSM = "11"
            #lat_data = self.from_digits_to_data(lat_num,lat_deg)

            degree = lat_deg.replace(".","")
            degree = degree[::-1]
            number = lat_num[::-1]

            digit1 = int(degree[0])
            dig1 = bin(digit1)[2:]
            dig1 = "0"*(4-len(dig1)) + dig1
            dig1 = dig1[::-1]

            digit2 = int(degree[1])
            dig2 = bin(digit2)[2:]
            dig2 = "0"*(4-len(dig2)) + dig2
            dig2 = dig2[::-1]

            digit3 = int(degree[2])
            dig3 = bin(digit3)[2:]
            dig3 = "0"*(4-len(dig3)) + dig3
            dig3 = dig3[::-1]

            digit4 = int(number[0])
            dig4 = bin(digit4)[2:]
            dig4 = "0"*(4-len(dig4)) + dig4
            dig4 = dig4[::-1]

            digit5 = int(number[1])
            dig5 = bin(digit5)[2:]
            dig5 = "0"*(4-len(dig5)) + dig5
            dig5 = dig5[::-1]

            dig6 = "0"
            if(len(lat_num)==3):
                dig6 = "1"

            lat_data = dig1 + dig2 + dig3 + dig4 + dig5 + dig6

            word_data_str = lat_data + SSM
        elif data_key == 'Present Position - Longitude':
            lon_num = word_data.split(" ")[1]
            lon_deg = word_data.split(" ")[-1].replace("'","")
            lon_EW = word_data.split(" ")[0]
            if(lon_EW == "W"):
                SSM = "11"
            else:
                SSM = "00"

            degree = lon_deg.replace(".","")
            degree = degree[::-1]
            number = lon_num[::-1]

            digit1 = int(degree[0])
            dig1 = bin(digit1)[2:]
            dig1 = "0"*(4-len(dig1)) + dig1
            dig1 = dig1[::-1]

            digit2 = int(degree[1])
            dig2 = bin(digit2)[2:]
            dig2 = "0"*(4-len(dig2)) + dig2
            dig2 = dig2[::-1]

            digit3 = int(degree[2])
            dig3 = bin(digit3)[2:]
            dig3 = "0"*(4-len(dig3)) + dig3
            dig3 = dig3[::-1]

            digit4 = int(number[0])
            dig4 = bin(digit4)[2:]
            dig4 = "0"*(4-len(dig4)) + dig4
            dig4 = dig4[::-1]

            digit5 = int(number[1])
            dig5 = bin(digit5)[2:]
            dig5 = "0"*(4-len(dig5)) + dig5
            dig5 = dig5[::-1]

            dig6 = "0"
            if(len(lon_num)==3):
                dig6 = "1"

            lat_data = dig1 + dig2 + dig3 + dig4 + dig5 + dig6

            word_data_str = lat_data + SSM
        elif data_key == 'Ground Speed':
            # Remove Knots from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 0 - 7000 Knots
            if(float(word_data) < 0 or float(word_data) > 7000):
                raise Exception("Ground Speed Error")
            # 4 sig bits
            # Resolution: 1 knot
            word_data_str = self.BCD_digs(float(word_data),1.0)
        elif data_key == 'Track Angle - True':
            # Remove Degrees from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 000.0 to 359.9 Degrees
            if(float(word_data) < 0.0 or float(word_data) > 359.9):
                raise Exception("Track Angle Error")
            # 4 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),0.1)
        elif data_key == 'Magnetic Heading':
            # Remove Degrees from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 000.0 to 359.9 Degrees
            if(float(word_data) < 0.0 or float(word_data) > 359.9):
                raise Exception("Magnetic Heading Error")
            # 4 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),0.1)
        elif data_key == 'Wind Speed':
            # Remove Knots from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 0 to 799 Degrees
            if(float(word_data) < 0.0 or float(word_data) > 799):
                raise Exception("Wind Speed Error")
            # 4 sig bits
            # Resolution: 1 knot
            word_data_str = self.BCD_digs(float(word_data),1.0)
        elif data_key == 'Wind Direction - True':
            # Remove Degrees from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 000.0 to 359.9 Degrees
            if(float(word_data) < 0.0 or float(word_data) > 359.0):
                raise Exception("Wind Direction Error")
            # 4 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),1.0)
        elif data_key == 'True Heading':
            # Remove Degrees from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 000.0 to 359.9 Degrees
            if(float(word_data) < 0.0 or float(word_data) > 359.9):
                raise Exception("True Heading Error")
            # 4 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),0.1)
        elif data_key == 'Total Air Temperature':
            # Remove Degrees Celsius from the data point:
            word_data = word_data.split(" ")[0]
            # Range: -060 to 099 Degrees
            if(float(word_data) < -60.0 or float(word_data) > 99.0):
                raise Exception("Total Air Temperature Error")
            # 3 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),1.0)
        elif data_key == 'Static Air Temperature':
            # Remove Degrees Celsius from the data point:
            word_data = word_data.split(" ")[0]
            # Range: -060 to 099 Degrees
            if(float(word_data) < -60.0 or float(word_data) > 99.0):
                raise Exception("Static Air Temperature Error")
            # 3 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),1.0)
        elif data_key == 'Baro Correction (mb) #1':
            # Remove mb from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 745 to 1050 mb
            if(float(word_data) < 745.0 or float(word_data) > 1050.0):
                raise Exception("Baro Correction (mb) #1 Error")
            # 5 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),0.1)
        elif data_key == 'Baro Correction (ins. Hg) #1':
            # Remove ins Hg from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 22.000 to 31.000 ins Hg
            if(float(word_data) < 22.0 or float(word_data) > 31.0):
                raise Exception("Baro Correction (ins. Hg) #1 Error")
            # 5 sig bits
            # Resolution: 0.001 degree
            word_data_str = self.BCD_digs(float(word_data),0.001)
        elif data_key == 'Baro Correction (mb) #2':
            # Remove mb from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 745 to 1050 mb
            if(float(word_data) < 745.0 or float(word_data) > 1050.0):
                raise Exception("Baro Correction (mb) #2 Error")
            # 5 sig bits
            # Resolution: 0.1 degree
            word_data_str = self.BCD_digs(float(word_data),0.1)
        elif data_key == 'Baro Correction (ins. Hg) #2':
            # Remove ins Hg from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 22.000 to 31.000 ins Hg
            if(float(word_data) < 22.0 or float(word_data) > 31.0):
                raise Exception("Baro Correction (ins. Hg) #2 Error")
            # 5 sig bits
            # Resolution: 0.001 degree
            word_data_str = self.BCD_digs(float(word_data),0.001)
        # DISC
        elif data_key == 'Total Pressure':
            # Remove mb from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 0 to 2045 mb
            # This is "00000000000" to "11111111101"
            if(float(word_data) < 0.0 or float(word_data) > 2045.0):
                raise Exception("Total Pressure Error")
            # 11 sig bits
            data = bin(int(word_data))[2:]
            # Add extra bits if less than 11 bits
            data = "0" * (11 - len(data)) + data
            padding = "00000000"
            data = padding + data
            data = data[::-1]

            SSM = "00" # Always positive
            SDI = "00" # Always towards 1 LRU
            # Resolution: 1.0 degree
            word_data_str = SDI + data + SSM
        elif data_key == 'Discrete Data #1':
            pass # This isn't detailed in the spec.
        elif data_key == 'Discrete Data #2':
            pass # This isn't detailed in the spec.
        elif data_key == 'Discrete Data #3':
            pass # This isn't detailed in the spec.
        elif data_key == 'IR Discrete Word #2':
            pass
        elif data_key == 'IR Test':
            mode = word_data.split(" ")[0] # get rid of extraneous words
            SDI = "00"
            SSM = "00"
            if(mode == "ON"):
                data = "0"* (19)
            elif(mode == "OFF"):
                data = "1"* (19)
            else:
                raise Exception("IR Discrete Word Error")
            word_data_str += SDI + data + SSM
        elif data_key == 'IRS Maintenance Word #1':
            pass # This isn't detailed in the spec.
        elif data_key == 'IRS Maintenance Word #2':
            pass # This isn't detailed in the spec.
        elif data_key == 'IRS Maintenance Word #3':
            pass # This isn't detailed in the spec.
        elif data_key == 'IRS Maintenance Word #4':
            pass # This isn't detailed in the spec.
        # BNR
        elif data_key == 'Body Pitch Acceleration' or data_key == 'Body Roll Acceleration' or data_key == 'Body Yaw Acceleration':
            # Remove Deg/Sec^2 from the data point:
            word_data = word_data.split(" ")[0]
            # Range: -64 to 64 Deg/Sec^2
            if(float(word_data) < -64.0 or float(word_data) > 64.0):
                raise Exception("Body Pitch Acceleration Error")
            # 15 sig bits
            # Resolution: 0.002 Deg/Sec^2 -> this means that what's encoded
            # is actually [-32000, +32000]
            value = float(word_data)/2.0
            if(len(str(value).replace(".","").replace("-","")) > 5): #54.123 -> 27.061_5 <- don't want this
                value = str(value)[:-1] # cut off the 0.5
                value = float(value)
            word_data_str = self.BNR_bits(value,0.002,15)
            """
            elif data_key == 'Body Roll Acceleration':
                # Remove Deg/Sec^2 from the data point:
                word_data = word_data.split(" ")[0]
                # Range: -64 to 64 Deg/Sec^2
                if(float(word_data) < -64.0 or float(word_data) > 64.0):
                    raise Exception("Body Roll Acceleration Error")
                # 15 sig bits
                # Resolution: 0.002 Deg/Sec^2 -> this means that what's encoded
                # is actually [-32000, +32000]
                value = float(word_data)/2.0
                if(len(str(value).replace(".","").replace("-","")) > 5): #54.123 -> 27.061_5 <- don't want this
                    value = str(value)[:-1] # cut off the 0.5
                    value = float(value)
                word_data_str = self.BNR_bits(value,0.002,15)
            elif data_key == 'Body Yaw Acceleration':
                pass
            """
        elif data_key == 'Cabin Pressure':
            # Remove mB from the data point:
            word_data = word_data.split(" ")[0]
            # Range: 0 to 2048 mB
            if(float(word_data) < 0.0 or float(word_data) > 2048.0):
                raise Exception("Cabin Pressure Error")
            # 16 sig bits
            # Resolution: 0.008 mB -> this means that what's encoded
            # is actually [-32000, +32000]
            value = float(word_data)/8.0
            if(len(str(value).replace(".","").replace("-","")) > 6):
                value = str(value)[0:8] # grab first six digits -> including . e.g. 123.321
                value = float(value)
            word_data_str = self.BNR_bits(value,0.008,18)
        elif data_key == 'Left Static Pressure Uncorrected, mb':
            pass
        elif data_key == 'Right Static Pressure Uncorrected, mb':
            pass
        elif data_key == 'Altitude (1013.25mB)':
            pass
        elif data_key == 'Baro Corrected Altitude #1':
            pass
        elif data_key == 'Mach':
            pass
        elif data_key == 'Max. Allowable Airspeed':
            pass
        elif data_key == 'True Airspeed':
            pass
        elif data_key == 'Corrected Angle of Attack':
            pass
        elif data_key == 'Altitude Rate':
            pass
        elif data_key == 'Impacted Pressure, Uncorrected, mb':
            pass
        elif data_key == 'Static Pressure, Average, Corrected (In. Hg)':
            pass
        elif data_key == 'Baro Corrected Altitude #2':
            pass
        elif data_key == 'Indicated Angle of Attack (Average)':
            pass
        elif data_key == 'Average Static Pressure mb, Uncorrected':
            pass
        elif data_key == 'Average Static Pressure mb, Corrected':
            pass
        elif data_key == 'Indicated Side Slip Angle':
            pass
        elif data_key == 'Baro Corrected Altitude #3':
            pass
        elif data_key == 'Baro Corrected Altitude #4':
            pass
        elif data_key == 'Corrected Side Slip Angle':
            pass
        elif data_key == 'Integrated Vertical Acceleration':
            pass
        elif data_key == 'Wind Angle':
            pass
        elif data_key == 'Track Angle - Magnetic':
            pass
        elif data_key == 'Drift Angle':
            pass
        elif data_key == 'Flight Path Angle':
            pass
        elif data_key == 'Flight Path Acceleration':
            pass
        elif data_key == 'Pitch Angle':
            pass
        elif data_key == 'Roll Angle':
            pass
        elif data_key == 'Body Pitch Rate':
            pass
        elif data_key == 'Body Roll Rate':
            pass
        elif data_key == 'Body Yaw Rate':
            pass
        elif data_key == 'Body Longitudinal Acceleration':
            pass
        elif data_key == 'Body Lateral Acceleration':
            pass
        elif data_key == 'Body Normal Acceleration':
            pass
        elif data_key == 'Platform Heading':
            pass
        elif data_key == 'Track Angle Rate':
            pass
        elif data_key == 'Inertial Pitch Rate':
            pass
        elif data_key == 'Inertial Roll Rate':
            pass
        elif data_key == 'Grid Heading':
            pass
        elif data_key == 'Potential Vertical Speed':
            pass
        elif data_key == 'Altitude (Inertial)':
            pass
        elif data_key == 'Along Track Horizontal Acceleration':
            pass
        elif data_key == 'Cross Track Acceleration':
            pass
        elif data_key == 'Vertical Acceleration':
            pass
        elif data_key == 'Inertial Vertical Velocity (EFI)':
            pass
        elif data_key == 'North-South Velocity':
            pass
        elif data_key == 'East-West Velocity':
            pass
        elif data_key == 'Along Heading Acceleration':
            pass
        elif data_key == 'Cross Heading Acceleration':
            pass
        else:
            raise ValueError("Label is wrong!")

        word = word_label_str + word_data_str + self.TXcommunicator_chip.calc_parity(word_label_str + word_data_str)

        if(len(word) != 32):
            raise ValueError("Word has been calculated incorrectly!!")

        return(word)

    # Meant for testing purposes only.
    def set_value(self,key_str:str, value:str):
        self.data[key_str] = value

    def BCD_digs(self, value:float, res:float):
        SDI = "00"
        SSM = "00"
        if(value < 0):
            SSM = "11"

        digits = str(value).strip("-")
        if(res >= 1.0): # remove the stuff after 0.000000
            digits = digits.split(".")[0]
        digits = digits.replace(".","")
        digits = "0" * (5 - len(digits)) + digits
        digits = digits[::-1]

        # e.g. 06572 knots
        # 11 - 14 -> 2
        # 15 - 18 -> 7
        # 19 - 22 -> 5
        # 23 - 26 -> 6
        # 27 - 29 -> 0

        digit5 = int(digits[0])
        dig5 = bin(digit5)[2:]
        dig5 = "0"*(4-len(dig5)) + dig5
        dig5 = dig5[::-1]

        digit4 = int(digits[1])
        dig4 = bin(digit4)[2:]
        dig4 = "0"*(4-len(dig4)) + dig4
        dig4 = dig4[::-1]

        digit3 = int(digits[2])
        dig3 = bin(digit3)[2:]
        dig3 = "0"*(4-len(dig3)) + dig3
        dig3 = dig3[::-1]

        digit2 = int(digits[3])
        dig2 = bin(digit2)[2:]
        dig2 = "0"*(4-len(dig2)) + dig2
        dig2 = dig2[::-1]

        digit1 = int(digits[4])
        dig1 = bin(digit1)[2:]
        dig1 = "0"*(3-len(dig1)) + dig1
        dig1 = dig1[::-1]

        partial_data = SDI + dig5 + dig4 + dig3 + dig2 + dig1 + SSM
        return(partial_data)

    def BNR_bits(self, value:float, res:float, sig_digs:int)->str:
        # get leading padding zeros
        padding = "0" * (19-sig_digs)
        # set SDI
        SDI = "00"
        # Set the sign to +/-
        SSM = "00"
        if(value < 0):
            SSM = "11"
        # get right of sign, we have saved that value
        val = str(value).strip("-")
        # get right of a X.0 if the resolution is 1+
        if(res >= 1.0):
            val = val.split(".")[0]
        # get rid of any decimal
        val = val.replace(".","")
        # get the bitstring from that value now
        val = bin(int(val))[2:]
        # add leading zeros as necessary
        val = "0" * (sig_digs - len(val)) + val
        # get the full data field
        data = padding + val
        # reverse it because everything is fucking reverse order
        data = data[::-1]
        return(SDI+data+SSM)

    def set_data(self, key, value):
        self.data[key] = value
        #word = self.BUS_CHANNELS[0].encode_word(key)
        #word = self.encode_word(key)
        #self.TXcommunicator_chip.transmit_given_word(int(word), bus_usec_start=time(), channel_index=0)