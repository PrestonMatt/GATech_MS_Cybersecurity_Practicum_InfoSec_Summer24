import os
#import PyARINC429.arinc429
import arinc429

"""
    Windows:
    Copy-paste the subfolder arinc429 from https://github.com/aeroneous/PyARINC429/tree/master
    into C:\\Users\\<user name>\\AppData\\Local\\Programs\Python\Python312\Lib

    Otherwise put it in a subdir from this file and have the line:
    import PyARINC429.arinc429
"""

applicable_labels_BCD = {
        0o046: 'BCD', # Engine Serial No. (LSDs) -> BCD
        0o047: 'BCD', # Engine Serial No. (MSDs) -> BCD
    }

applicable_lables_DISC = {

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

applicable_lables_BNR = {
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
        0o363: 'BNR', # Derivative of Thrust vs. N1 -> BNR
        0o372: 'BNR', # Actual Fan Speed -> BNR
        0o373: 'BNR', # Actual Core Speed -> BNR
        0o374: 'BNR', # Left Thrust Reverser Position -> BNR
        0o375: 'BNR' # Right Thrust Reverser Position -> BNR
    }

def recv_ARINC429(data):

    if(data == None):
        return(0)
    
    #eqp_id = label & int("00011100",2)
    # bits 3,4,5 = equip id

    #code_no = label & int("11100000",2)
    
    #if(eqp_id == 0x108):
    #    print("engine recieving wordon channel A.")
    #elif(eqp_id == 0x109):
    #    print("engine recieving word on channel B.")
    #else:
    #    return(0)

def main(word):
    print("Starting RX for EEC")
    print("The equip id for EEC is 0x10A and 0x10B")

    # recv word via pipe
    # label is whatever mode it is
    label = word.label
    data = None
    if(label in applicable_labels_BCD):
        data = arinc429.BCD.decode(word.data, word.ssm, 0.1)
    elif(label in applicable_labels_DISC):
        data = arinc429.Discrete.decode(word.data)
    elif(label in applicable_labels_BNR):
        data = arinc429.BNR.decode(word.get_bit_field(bnr_bit_field.lsb, bnr_bit_field.msb), 17, 0.043945313)
    else:
        continue # next word.
        
    recv_ARINC429(data)

if __name__ == "__main__":
    main()
