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
        0o241: "Corrected Angle of Attack",
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

    def __init__(self):
        pass

    def __str__(self):
        pass

    def decode_GPS_word(self):
        pass

    def encode_word(self):
        pass