from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time
from queue import Queue

class arinc429_intrusion_detection_system:

    all_labels = {
        # Format:
        # Label 1 in octal: {Equipment ID 1 in Hex: [BCD/BNR/DISC/SAL, resolution, (range)],
        #                  Equipment ID 2 in Hex: BCD/BNR/DISC/SAL ... },
        #                  ... ]
        # Label 2 in octal : ... etc ...
        # 0o0: [ <NOT USED> ],
        0o001: {0x002: ["BCD", 0.1, (-3999.9, 3999.9)],
                0x056: ["BCD", 0.1, (-3999.9, 3999.9)],
                0x060: ["BCD", 0.1, (-3999.9, 3999.9)]},

        0o002: {0x002: ["BCD", 0.1, (0.0, 399.9)],
                0x056: ["BCD", 0.1, (0.0, 399.9)],
                0x060: ["BCD", 0.1, (0.0, 399.9)],
                0x115: ["BCD", 0.1, (0.0, 399.9)]},

        0o003: {0x002: ["BCD", 0.1, (0.0, 399.9)]},

        0o004: {0x001: ["BCD", 100.0, (0.0, 79900.0)]},

        0o005: {0x0D0: ["DISC", 0.0]},

        0o006: {0x0D0: ["DISC", 0.0]},

        # 0o007: [], SPARE

        0o010: {0x002: ["BCD", 0.1, (-180.0, 180.0)],
                0x004: ["BCD", 0.1, (-180.0, 180.0)],
                0x038: ["BCD", 0.1, (-180.0, 180.0)]},

        0o011: {0x002: ["BCD", 0.1, (-180.0, 180.0)],
                0x004: ["BCD", 0.1, (-180.0, 180.0)],
                0x038: ["BCD", 0.1, (-180.0, 180.0)]},

        0o012: {0x002: ["BCD", 1.0, (0.0, 7000.0)],
                0x004: ["BCD", 1.0, (0.0, 7000.0)],
                0x005: ["BCD", 1.0, (0.0, 79999.0)],
                0x025: ["BCD", 1.0, (0.0, 7000.0)],
                0x038: ["BCD", 1.0, (0.0, 7000.0)],
                0x04d: ["BCD", 1.0, (0.0, 7000.0)],
                0x056: ["BCD", 1.0, (0.0, 7000.0)],
                0x060: ["BCD", 1.0, (0.0, 7000.0)]},

        0o013: {0x002: ["BCD", 0.1, (0.0, 359.9)],
                0x004: ["BCD", 0.1, (0.0, 359.9)],
                0x038: ["BCD", 0.1, (0.0, 79999.0)],
                0x04d: ["BCD", 1.0, (0.0, 359.9)],
                0x0b8: ["DISC", 0.0]},

        0o014: {0x004: ["BCD", 0.1, (0.0, 359.9)],
                0x005: ["BCD", 0.1, (0.0, 359.9)],
                0x038: ["BCD", 0.1, (0.0, 359.9)]},

        0o015: {0x002: ["BCD", 1.0, (0.0, 799.0)],
                0x004: ["BCD", 1.0, (0.0, 799.0)],
                0x005: ["BCD", 1.0, (0.0, 799.0)],
                0x038: ["BCD", 1.0, (0.0, 799.0)]},

        0o016: {0x004: ["BCD", 1.0, (0.0, 359.0)],
                0x038: ["BCD", 1.0, (0.0, 359.0)],
                0x0B8: ["DISC", 0.0, (0.0, 359.0)]},

        0o017: {0x010: ["BCD", 0.1, (0.0, 359.9)],
                0x04d: ["BCD", 1.0, (0.0, 79999.0)],
                0x055: ["BCD", 0.1, (0.0, 359.9)],
                0x0A0: ["BCD", 0.1, (0.0, 359.9)],
                0x0B0: ["BCD", 0.1, (0.0, 359.9)]},

        0o020: {0x020: ["BCD", 1.0, (-6000.0, 6000.0)],
                0x04d: ["BCD", 1.0, (0.0, 79999.0)],
                0x06D: ["DISC", 0.0],
                0x0A1: ["BCD", 1.0, (-6000.0, 6000.0)]},

        0o021: {0x002: ["BCD", 0.001, (0.0, 3.0)],
                0x020: ["BCD", 0.001, (0.0, 3.0)],
                0x06d: ["DISC", 0.0],
                0x0a1: ["BCD", 0.001, (0.0, 3.0)]},

        0o022: {0x020: ["BCD", 0.001, (0.0, 4.0)],
                0x04d: ["BCD", 1.0, (0.0, 79999.0)],
                0x06d: ["DISC", 0.0],
                0x0a1: ["BCD", 0.001, (0.0, 4.0)]},

        0o023: {0x020: ["BCD", 1.0, (0.0, 359.0)],
                0x04d: ["BCD", 1.0, (0.0, 79999.0)],
                0x06d: ["DISC", 0.0],
                0x0a1: ["BCD", 1.0, (0.0, 359.0)]},

        0o024: {0x011: ["BCD", 1.0, (0.0, 359.0)],
                0x020: ["BCD", 1.0, (0.0, 359.0)],
                0x06d: ["DISC", 0.0],
                0x0a1: ["BCD", 1.0, (0.0, 359.0)],
                0x0b1: ["BCD", 1.0, (0.0, 359.0)]},

        0o025: {0x020: ["BCD", 1.0, (0.0, 50000.0)],
                0x04d: ["BNR", 100.0, (0.0, 204700.0), 11],
                0x0a1: ["BCD", 1.0, (0.0, 50000.0)]},

        0o26: {0x003: ["BCD", 1.0, (30.0, 450.0)],
               0x020: ["BNR", 1.0, (30.0, 450.0), 3], # This has a typo in the spec doc. Best guess.
               0x0a1: ["BCD", 1.0, (30.0, 450.0)]},

        0o27: {0x002: ["BCD", 1.0, (0.0, 359.0)],
               0x011: ["BCD", 1.0, (0.0, 359.0)],
               0x020: ["BCD", 1.0, (0.0, 359.0)],
               0x04d: ["BCD", 1.0, (0.0, 359.0)],
               0x056: ["BCD", 1.0, (0.0, 359.0)],
               0x060: ["BCD", 1.0, (0.0, 359.0)],
               0x0a1: ["BCD", 1.0, (0.0, 359.0)],
               0x0b1: ["BCD", 1.0, (0.0, 359.0)]},

        0o30: {0x020: ["BCD", 0.001, (0.0, 79.999)],
               0x024: ["BCD", 0.001, (0.0, 79.999)],
               0x04d: ["BCD", 1.0, (0.0, 79999.0)],
               0x0b6: ["BCD", 0.001, (0.0, 79.999)]},

        0o31: {0x020: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x0b8: ["BCD", 0.01, (0.0, 79.99)]}, # DISC but drop the first digit (base 10)

        0o32: {0x012: ["BCD", 1.0, (0.0, 7999.0)], # DISC but drop the first digit (base 10)
               0x020: ["BCD", 1.0, (0.0, 7999.0)], # DISC but drop the first digit (base 10)
               0x0b2: ["BCD", 1.0, (0.0, 7999.0)]}, # DISC but drop the first digit (base 10)

        0o33: {0x002: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x010: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x020: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x055: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x056: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x060: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x0b0: ["BCD", 0.01, (0.0, 79.99)]}, # DISC but drop the first digit (base 10)

        0o34: {0x002: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x006: ["BCD", 0.1, (745.0, 1050.0)],
               0x011: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x020: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x025: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x056: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x060: ["BCD", 0.01, (0.0, 79.99)], # DISC but drop the first digit (base 10)
               0x0b0: ["BCD", 0.01, (0.0, 79.99)]}, # DISC but drop the first digit (base 10)

        0o35: {0x002: ["BCD", 0.1, (0.0, 39.9)],
               0x006: ["BCD", 0.001, (22.0, 31.0)],
               0x009: ["BCD", 0.1, (0.0, 39.9)],
               0x020: ["BCD", 0.1, (0.0, 39.9)],
               0x025: ["BCD", 0.1, (0.0, 39.9)],
               0x055: ["BCD", 0.05, (108.0, 159.9)],
               0x056: ["BCD", 0.1, (0.0, 39.9)],
               0x060: ["BCD", 0.1, (0.0, 39.9)],
               0x0a9: ["BCD", 0.1, (0.0, 39.9)],},

        # https://en.wikipedia.org/wiki/Microwave_landing_system
        # MLS Freq Range: 5031 to 5090.7 MHz
        0o36: {0x002: ["BCD", 0.1, (5031.0, 5090.7)],
               0x020: ["BCD", 0.1, (5031.0, 5090.7)],
               0x055: ["BCD", 1.0, (500.0, 600.0)],
               0x056: ["BCD", 0.1, (5031.0, 5090.7)],
               0x060: ["BCD", 0.1, (5031.0, 5090.7)],
               0x0c7: ["BCD", 0.1, (5031.0, 5090.7)]},

        0o37: {0x002: ["BCD", 0.1, (0.0, 0.9)], # DISC but drop the first four digits (base 10)
               0x0b9: ["BCD", 0.1, (0.0, 0.9)]}, # DISC but drop the first four digits (base 10)

        # 0o40: {}, SPARE

        0o41: {0x002: ["BCD", 0.1, (-180.0, 180.0)],
               0x004: ["BCD", 0.1, (-180.0, 180.0)],
               0x020: ["BCD", 0.1, (-180.0, 180.0)],
               0x056: ["BCD", 0.1, (-180.0, 180.0)],
               0x060: ["BCD", 0.1, (-180.0, 180.0)],
               0x0a4: ["BCD", 0.1, (-180.0, 180.0)]},

        0o42: {0x002: ["BCD", 0.1, (-180.0, 180.0)],
               0x004: ["BCD", 0.1, (-180.0, 180.0)],
               0x020: ["BCD", 0.1, (-180.0, 180.0)],
               0x056: ["BCD", 0.1, (-180.0, 180.0)],
               0x060: ["BCD", 0.1, (-180.0, 180.0)],
               0x0a4: ["BCD", 0.1, (-180.0, 180.0)]},

        0o43: {0x002: ["BCD", 1.0, (0.0, 359.0)],
               0x004: ["BCD", 1.0, (0.0, 359.0)],
               0x020: ["BCD", 1.0, (0.0, 359.0)],
               0x056: ["BCD", 1.0, (0.0, 359.0)],
               0x060: ["BCD", 1.0, (0.0, 359.0)],
               0x0a4: ["BCD", 1.0, (0.0, 359.0)]},

        0o44: {0x004: ["BCD", 0.1, (0.0, 359.9)],
               0x038: ["BCD", 0.1, (0.0, 359.9)]},

        0o45: {0x003: ["BCD", 0.1, (0.0, 259.9)]}, # This may be a typo, but this is what the spec sheet says.

        0o46: {0x033: ["BCD", 1.0, (0.0, 9999.0)], # Engine serial number half = 0000-9999
               0x10a: ["BCD", 1.0, (0.0, 9999.0)], # Engine serial number half = 0000-9999
               0x10b: ["BCD", 1.0, (0.0, 9999.0)],}, # Engine serial number half = 0000-9999

        0o47: {0x020: ["BCD", 0.001, (0.0, 79.999)],
               0x024: ["BCD", 0.001, (0.0, 79.999)],
               0x033: ["BCD", 1.0, (0.0, 9999.0)], # Engine serial number half = 0000-9999
               0x0b6: ["BCD", 0.001, (0.0, 79.999)],
               0x10a: ["BCD", 1.0, (0.0, 9999.0)], # Engine serial number half = 0000-9999
               0x10b: ["BCD", 1.0, (0.0, 9999.0)]}, # Engine serial number half = 0000-9999

        # 0o50: {}, SPARE

        # 0o51: {}, SPARE

        0o52: {0x004: ["BNR", 0.002, (-64.0, 64.0), 15],
               0x037: ["BCD", 0.01, (0.0, 100.0)],
               0x038: ["BNR", 0.002, (-64.0, 64.0), 15]},

        0o53: {0x004: ["BNR", 0.002, (-64.0, 64.0), 15],
               0x005: ["BCD", 1.0, (0.0, 359.0)],
               0x038: ["BNR", 0.002, (-64.0, 64.0), 15]},

        0o54: {0x004: ["BNR", 0.002, (-64.0, 64.0), 15],
               0x037: ["BNR", 20.0, (0.0, 655360.0)],
               0x038: ["BNR", 0.002, (-64.0, 64.0), 15]},

        # 0o55: {}, SPARE

        0o56: {0x002: ["BCD", 0.1, (0.0, 864000.0)], # 0 - 23:59.9, this is tenths of seconds.
               0x005: ["BCD", 1.0, (0.0, 359.0)],
               0x037: ["BCD", 1.0, (0.0, 19999.0)],
               0x056: ["BCD", 1.0, (0.0, 864000.0)], # 0 - 23:59.9, this is tenths of seconds.
               0x060: ["BCD", 1.0, (0.0, 864000.0)]}, # 0 - 23:59.9, this is tenths of seconds.

        # 0o57: {}, SPARE

        0o60: {0x025: ["BCD", 1.0, (0.0, 9999.0)], # S/G Hardware Part Number
               0x037: ["BCD", 1.0, (0.1, 299.9)],
               0x03c: ["BNR", 1.0, (0.0, 1024.0), 10]},

        # ACMS Information IDK man. It's fucking 1:09 am.
        0o61: {0x002: ["BNR", 1.0, (0.0, 524287.0), 19], # ... there's nothing in the spec ...
               0x00b: ["BNR", 256.0, (-268435456.0, 268435456.0), 20],
               0x025: ["BCD", 1.0, (0.0, 9999.0)], # S/G Hardware Part Number
               0x037: ["BCD", 0.1, (0.0, 299.9)],
               0x03c: ["BNR", 1.0, (0.0, 1024.0), 10],
               0x056: ["BNR", 1.0, (0.0, 524287.0), 19], # ... there's nothing in the spec ...
               0x060: ["BNR", 1.0, (0.0, 524287.0), 19]}, # ... there's nothing in the spec ...

        0o62: {0x002: ["BNR", 1.0, (0.0, 524287.0), 19], # ... there's nothing in the spec ...
               0x00b: ["BNR", 256.0, (0.0, 4096.0), 20],
               0x037: ["BCD", 0.1, (0.0, 299.9)],
               0x03c: ["BNR", 1.0, (0.0, 1024.0), 10],
               0x056: ["BNR", 1.0, (0.0, 524287.0), 19], # ... there's nothing in the spec ...
               0x060: ["BNR", 1.0, (0.0, 524287.0), 19]}, # ... there's nothing in the spec ...

        0o63: {},

        0o64: {},

        0o65: {},

        0o66: {},

        0o67: {},

        0o70: {},

        0o71: {},

        0o72: {},

        0o73: {},

        0o74: {},

        0o75: {},

        0o76: {},

        0o77: {},

        0o100: {},

        0o101: {},

        0o102: {},

        0o103: {},

        0o104: {},

        0o105: {},

        0o106: {},

        0o107: {},

        0o110: {},

        0o111: {},

        0o112: {},

        0o113: {},

        0o114: {},

        0o115: {},

        0o116: {},

        0o117: {},

        0o120: {},

        0o121: {},

        0o122: {},

        0o123: {},

        0o124: {},

        0o125: {},

        0o126: {},

        0o127: {},

        0o130: {},

        0o131: {},

        0o132: {},

        0o133: {},

        0o134: {},

        0o135: {},

        0o136: {},

        0o137: {},

        0o140: {},

        0o141: {},

        0o142: {},

        0o143: {},

        0o144: {},

        0o145: {},

        0o146: {},

        0o147: {},

        0o150: {},

        0o151: {},

        0o152: {},

        0o153: {},

        0o154: {},

        0o155: {},

        0o156: {},

        0o157: {},

        0o160: {},

        0o161: {},

        0o162: {},

        0o163: {},

        0o164: {},

        0o165: {},

        0o166: {},

        0o167: {},

        0o170: {},

        0o171: {},

        0o172: {},

        0o173: {},

        0o174: {},

        0o175: {},

        0o176: {},

        0o177: {},

        0o200: {},

        0o201: {},

        0o202: {},

        0o203: {},

        0o204: {},

        0o205: {},

        0o206: {},

        0o207: {},

        0o210: {},

        0o211: {},

        0o212: {},

        0o213: {},

        0o214: {},

        0o215: {},

        0o216: {},

        0o217: {},

        0o220: {},

        0o221: {},

        0o222: {},

        0o223: {},

        0o224: {},

        0o225: {},

        0o226: {},

        0o227: {},

        0o230: {},

        0o231: {},

        0o232: {},

        0o233: {},

        0o234: {},

        0o235: {},

        0o236: {},

        0o237: {},

        0o240: {},

        0o241: {},

        0o242: {},

        0o243: {},

        0o244: {},

        0o245: {},

        0o246: {},

        0o247: {},

        0o250: {},

        0o251: {},

        0o252: {},

        0o253: {},

        0o254: {},

        0o255: {},

        0o256: {},

        0o257: {},

        0o260: {},

        0o261: {},

        0o262: {},

        0o263: {},

        0o264: {},

        0o265: {},

        0o266: {},

        0o267: {},

        0o270: {},

        0o271: {},

        0o272: {},

        0o273: {},

        0o274: {},

        0o275: {},

        0o276: {},

        0o277: {},

        0o300: {},

        0o301: {},

        0o302: {},

        0o303: {},

        0o304: {},

        0o305: {},

        0o306: {},

        0o307: {},

        0o310: {},

        0o311: {},

        0o312: {},

        0o313: {},

        0o314: {},

        0o315: {},

        0o316: {},

        0o317: {},

        0o320: {},

        0o321: {},

        0o322: {},

        0o323: {},

        0o324: {},

        0o325: {},

        0o326: {},

        0o327: {},

        0o330: {},

        0o331: {},

        0o332: {},

        0o333: {},

        0o334: {},

        0o335: {},

        0o336: {},

        0o337: {},

        0o340: {},

        0o341: {},

        0o342: {},

        0o343: {},

        0o344: {},

        0o345: {},

        0o346: {},

        0o347: {},

        0o350: {},

        0o351: {},

        0o352: {},

        0o353: {},

        0o354: {},

        0o355: {},

        0o356: {},

        0o357: {},

        0o360: {},

        0o361: {},

        0o362: {},

        0o363: {},

        0o364: {},

        0o365: {},

        0o366: {},

        0o367: {},

        0o370: {},

        0o371: {},

        0o372: {},

        0o373: {},

        0o374: {},

        0o375: {},

        0o376: {},

        0o377: {}
    }

    equip_ids = {
        # Format:
        # Equipement ID in hex: "Human Readable Name"
        0x0: "Not Used",
        0x001: "Flight Control Computer",
        0x002: "Flight Management Computer",
        0x003: "Thrust Control Computer ",
        0x004: "Inertial Reference System",
        0x005: "Attitude and Heading Ref. System",
        0x006: "Air Data System",
        0x007: "Radio Altimeter",
        0x008: "Airborne Weather Radar",
        0x009: "Airborne DME",
        0x00A: "FAC",
        0x00B: "Global Positioning System",
        0x00D: " AIDS Data Management System",
        0x010: "Airborne ILS Receiver",
        0x011: "Airborne VOR Receiver ",
        0x012: "Airborne ADF System",
        0x016: "Airborne VHF COM",
        0x017: "DEFDARS-AIDS",
        0x018: "ATC Transponder",
        0x019: "Airborne HF/SSB System",
        0x01A: "Electronic Supervisory Control",
        0x01B: "Digital Slat/Flap Computer",
        0x01D: "A/P & F/D Mode Control Panel ",
        0x01E: "Performance Data Computer",
        0x01F: "Fuel Quantity Totalizer",
        0x020: "DFS System",
        0x023: "Ground Prox. Warning System",
        0x024: "ACARS (724) / CMU Mark 2",
        0x025: "Electronic Flt. Instruments",
        0x026: "Flight Warning Computer",
        0x027: "Microwave Landing System",
        0x029: "ADDCS (729) and EICAS",
        0x02A: "Thrust Management Computer",
        0x02B: "Perf. Nav. Computer System",
        0x02C: "Digital Fuel Gauging System",
        0x02D: "EPR Indicator (Boeing 757)",
        0x02E: "Land Rollout CU/Landing C & LU",
        0x02F: "Full Authority EEC-A 069 030 Airborne Separation Assurance System",
        0x031: "Chronometer",
        0x032: "Pass. Entertainment Tape Reproducer",
        0x033: "Propulsion Multiplexer (PMUX)",
        0x034: "Fault Isolation & Detection System",
        0x035: "TCAS",
        0x036: "Radio Management System",
        0x037: "Weight and Balance System",
        0x038: "ADIRS",
        0x039: "MCDU",
        0x03A: "Propulsion Discrete Interface Unit",
        0x03B: "Autopilot Buffer Unit",
        0x03C: "Tire Pressure Monitoring System",
        0x03D: "Airborne Vibration Monitor",
        0x03E: "Center of Gravity Control Computer",
        0x03F: "Full Authority EEC-B",
        0x040: "Cockpit Printer",
        0x041: "Satellite Data Unit",
        0x04A: "Landing Gear Position Interface Unit",
        0x04B: "Main Electrical System Controller",
        0x04C: "Emergency Electrical System Controller",
        0x04D: "Fuel Qty. Indicating System",
        0x04E: "Fuel Qty. Indicating System",
        0x050: "VDR",
        0x053: "HF Data Unit",
        0x055: "Multi-Mode Receiver (MMR)",
        0x057: "Cockpit Voice Recorder",
        0x05D: "Zone Controller",
        0x05E: "Cargo Heat",
        0x05F: "CIDS",
        0x060: "GNSS Navigation Unit (GNU)",
        0x061: "High-Speed Data Unit",
        0x06A: "AMU (A320)",
        0x06B: "Battery Charge Limiter",
        0x06C: "Flt. Cont. Data Concentrator",
        0x06D: "Landing Gear Prox. Control",
        0x06E: "Brake Steering Unit",
        0x06F: "Bleed Air",
        0x07A: "APU Engine Control Unit",
        0x07B: "Engine Interface Unit)",
        0x07C: "FADEC Channel A",
        0x07D: "FADEC Channel B",
        0x07E: "Centralized Fault Data Interface Unit",
        0x07F: "Fire Detection Unit",
        0x08A: "Window Heat Computer",
        0x08B: "Probes Heat Computer",
        0x08C: "Avionics c-10 Cooling Computer",
        0x08D: "Fuel Flow Indicator",
        0x08E: "Surface Position Digitizer",
        0x08F: "Vacuum System Controller",
        0x0A1: "FCC Controller",
        0x0A2: "FMC Controller",
        0x0A3: "Thrust Rating Controller",
        0x0A4: "IRS Controller",
        0x0A8: "Airborne WXR Controller",
        0x0A9: "Airborne DME Controller",
        0x0AA: "Generator Control Unit",
        0x0AB: "Air Supply Control & Test Unit",
        0x0AC: "Bus Control Unit",
        0x0AD: "ADIRS Air Data Module 0E6",
        0x0AE: "Yaw Damper Module",
        0x0AF: "Stabilizer Trim Module",
        0x0B0: "Airborne ILS Controller",
        0x0B1: "Airborne VOR Controller",
        0x0B2: "Airborne ADF Controller",
        0x0B6: "VHF COM Controller",
        0x0B9: "HF/SSB System Controller",
        0x0B8: "ATC Transponder Controller",
        0x0BA: "Power Supply Module",
        0x0BB: "Flap Control Unit and Flap Slat Electronics Unit",
        0x0BC: "Fuel System Interface Card",
        0x0BD: "Hydraulic Quantity Monitor Unit",
        0x0BE: "Hydraulic Interface Module",
        0x0BF: "Window Heat Control Unit",
        0x0C2: "PVS Control Unit",
        0x0C3: "GPWS Controller",
        0x0C4: "A429W SDU Controller",
        0x0C5: "EFI Controller",
        0x0C7: "MLS Controller",
        0x0CA: "Brake Temperature Monitor Unit",
        0x0CB: "Autostart",
        0x0CC: "Brake System Control Unit",
        0x0CD: "Pack Temperature Controller",
        0x0CE: "EICAS/EFIC Interface Unit",
        0x0CF: "Para Visual Display Computer",
        0x0D0: "Engine Instrument System",
        0x0D3: "Thermal Monitoring Unit (General)",
        0x0D5: "TCAS Control Panel",
        0x0DA: "Prox. Switch Electronics Unit",
        0x0DB: "APU Controller",
        0x0DC: "Zone Temperature Controller",
        0x0DD: "Cabin Pressure Controller",
        0x0DE: "Windshear Computer (Sperry)",
        0x0DF: "Equipment Cooling Card",
        0x0E0: "Crew Rest Temp. Controller",
        0x0EA: "Misc. Environment Control",
        0x0EB: "Fuel Jettison Control Card",
        0x0EC: "Advance Cabin Entertainment Serv. Sys.",
        0x0ED: "Fuel System Controller",
        0x0EE: "Hydraulic System Controller",
        0x0EF: "Environmental System Controller",
        0x0FA: "Misc. System controller",
        0x0FB: "Anti-Skid System",
        0x0FC: "Cabin Pressure Control Sys.",
        0x0FD: "Air Condition Control System",
        0x0FE: "Pneumatic Control System",
        0x0FF: "Manifold Failure Detection System",
        0x108: "Electronic Engine Control (EEC) Channel A",
        0x109: "Elect Eng Control (EEC) Channel B",
        0x10A: "Full Authority Engine Control A",
        0x10B: "Full Authority Engine Control B",
        0x10C: "APU Controller",
        0x10D: "Data Loader",
        0x10E: "Fire Detection Unit",
        0x10F: "Auto Brake Unit",
        0x110: "Multiplexer PES",
        0x112: "TACAN Adapter Unit",
        0x113: "Stall Warning Card",
        0x114: "Fuel Unit Management System",
        0x115: "TACAN",
        0x116: "Eng Interface Vibration Monitoring Unit",
        0x117: "Engine Control Unit Channel A",
        0x118: "Engine Control Unit Channel B",
        0x119: "Centralized Maintenance Computer",
        0x11A: "Multi-Disk Drive Unit",
        0x11E: "Integrated Static Probe",
        0x120: "Multifunction Air Data Probe",
        0x121: "15B Flight Control Unit",
        0x122: "Ground Auxiliary Power Unit",
        0x123: "Ground Power Control Unit",
        0x124: "Fuel Management Computer",
        0x125: "Center of Gravity Fuel Control Comp.",
        0x126: "Circuit breakers Monitoring Unit",
        0x127: "Electrical Contractor Management Unit",
        0x128: "Hydraulic Electrical Generator Control Unit",
        0x129: "Hydraulic System Monitoring Unit",
        0x12A: "Cargo Bay Conditioning Card",
        0x12B: "Predictive Windshear System Sensor",
        0x12C: "Angle of Attack Sensor",
        0x12D: "Logic Drive Control Computer",
        0x12E: "Cargo Control Logic Unit",
        0x12F: "Cargo Electronics Interface Unit",
        0x130: "Load Management Unit (LMU) Airbus",
        0x136: "Audio Management System",
        0x13A: "Full Authority Engine Control (P&W)",
        0x13B: "Audio Entertainment System (AES) Controller",
        0x13C: "Boarding Music Machine",
        0x13D: "Passenger In Flight Info Unit",
        0x13E: "Video Interface Unit",
        0x13F: "Camera Interface Unit",
        0x140: "Supersonic Air Data Computer",
        0x141: "Satellite RF Unit",
        0x142: "ADS-B Link Display c-16 Processor Unit (LPDU)",
        0x143: "Vertical/Horizontal Gyro",
        0x144: "CDTI Display Unit",
        0x14A: "Slide Slip Angle (SSA)",
        0x150: "AIMS Gen. Pur. Bus #1",
        0x151: "AIMS Gen. Pur. Bus #2",
        0x152: "AIMS Digital Comm. Mgmt.",
        0x153: "AIMS Gen. Pur. Bus #3",
        0x154: "Central Maintenance Computer",
        0x155: "AIMS EFIS Control Panel",
        0x156: "AIMS Display Unit",
        0x157: "AIMS Cursor Control Device",
        0x158: "AIMS General Purpose Bus #4",
        0x15A: "Flight Data Interface Unit",
        0x15C: "Flight Control Primary Computer",
        0x15D: "Flight Control Secondary Computer",
        0x15E: "Flight Mgmt Guidance Env Comp",
        0x160: "Special Fuel Quan. Sys.",
        0x167: "Air Traffic Service Unit",
        0x168: "Integ Standby Instr System",
        0x169: "Data Link Control and Display Unit",
        0x16A: "Display Unit",
        0x16B: "Display Management Computer",
        0x16C: "Head-Up Display Computer",
        0x16D: "ECAM Control Panel",
        0x16E: "Clock",
        0x16F: "Cabin Interphone System",
        0x170: "Radio Tuning Panel",
        0x171: "Electronic Flight Bag",
        0x17A: "Cabin Ventilation Controller",
        0x17B: "Smoke Detection Control Unit",
        0x17C: "Proximity Sensor Control Unit",
        0x18A: "Audio Control Panel",
        0x18B: "Cockpit Voice recorder",
        0x18C: "Passenger Entertainment Sys Main MUX",
        0x18D: "Passenger Entertainment Sys Audio Repro.",
        0x18E: "Pre-recorded Announcement Music Repro.",
        0x18F: "Video Control Unit (A330/A340)",
        0x19F: "Cade Environment System",
        0x1E2: "ADS-c-12 B LDPU Controller",
        0x200: "Versatile Integrated Avionics Unit",
        0x201: "Electronic Spoiler Control Unit",
        0x202: "Brake Control Unit",
        0x203: "Pneumatic Overheat Detection Unit",
        0x204: "Proximity Switch Electronics Unit",
        0x205: "APU Electronic Control Unit",
        0x206: "Aircraft Interface Unit",
        0x207: "Fuel Quantity Gauging Unit",
        0x241: "High Power Amplifier",
        0x341: "Satellite ACU c-11"
    }

    def __init__(self, bus_speed="low", BUS_CHANNELS=[], rules_file = r"C:\Users\mspreston\Desktop\Grad School Work\7 - Summer Semester 2024\Cybersecurity Practicum\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt"):
        # Set bus start time
        self.start_time = time()
        # Set bus channels.
        self.BUS_CHANNELS = BUS_CHANNELS
        # set ADIRU T/Rx bus speed
        self.bus_speed = bus_speed

        self.communication_chip = lru_rxr(bus_speed=self.bus_speed,
                                          BUS_CHANNELS=self.BUS_CHANNELS)

        # Output files:
        self.default_filepath = r"C:/ARINC429_IDS/"
        # Input file
        self.rules_file = rules_file
        # Log File location =>
        self.log_filepath = ""
        # Alert File location =>
        self.alert_filepath = ""
        self.get_log_alert_file_path()

        self.channels = {}
        self.get_channel_connections()

        self.sdis = self.get_sdis()

        self.rules = []
        self.get_rules()
        self.n = 1 # number of words.

    def make_default_rules(self):

        #start_time = time()

        #default_filepath = r"C:/ARINC429_IDS/"
        with open("ARINC429_rules_template.txt","r") as template_fd:
            template_lines = template_fd.readlines()
        template_fd.close()
        with open(self.default_filepath + r"ARINC429_rules_defaults.txt","w") as default_rules_fd:
            default_rules_fd.write(template_lines)
        default_rules_fd.close()

        with open(self.default_filepath + r"Alerts/" + f"Alerts_{self.start_time}.txt", "a") as alerts_fd:
            alerts_fd.write(f"Starting New Alert Message Recording at {self.start_time}\n")
        alerts_fd.close()

        default_rules = {}

        return default_rules

        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            logs_fd.write(f"Starting New Alert Message Recording at {self.start_time}\n")
        logs_fd.close()

    def __str__(self):
        return(str(self.rules))

    def get_log_alert_file_path(self) -> str:
        # Log File location =>
        self.alert_filepath = self.default_filepath + r"Alerts/Logs.txt"
        # Alert File location =>
        self.log_filepath = self.default_filepath + r"Logs/Logs.txt"

        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        files_lines = []
        filines = False
        for line in lines:
            if(line.__contains__("!Outfile")):
                filines = True
            if(filines and line.__contains__("alerts")):
                self.alert_filepath = line.split(" ")[2].replace("\n","")
                #print(line.split(" "))
            if(filines and line.__contains__("logs")):
                self.log_filepath = line.split(" ")[2].replace("\n","")
                #print(line.split(" "))
            if(line.__contains__("!Channels")):
                return
        # else keep defaults:
        return

    def get_channel_connections(self):
        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        #files_lines = []
        filines = False
        for line in lines:
            if(line == "\n"):
                continue
            if(line.__contains__("!SDI")):
                break
                #filines = False
                #return
            if(filines): # and not line.__contains__("!Channels") or not line.__contains__("!SDI")):
                channel = line.split(":")[0].replace(":","")
                #print(line.split(":"))
                tx_to_rx = line.split(":")[1][1:].replace("\n","")
                try:
                    self.channels[channel].append(tx_to_rx)
                except KeyError:
                    self.channels[channel] = [tx_to_rx]
            if(line.__contains__("!Channels")):
                filines = True

    def get_sdis(self)->dict:

        sdis = {}

        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        SDI_flag = False
        for line in lines:
            if(line == "\n"):
                continue
            if(line.__contains__("!Rules")):
                break
            if(SDI_flag):
                # remove endline comments
                line = line.split("#")[0]
                # remove full line comments
                if(line == "" or line == "\n"):
                    continue
                try:
                    channel = line.split(" ")[0].replace(":","")
                    sdi_name = line.split(" ")[1]
                    bitmask = line.split(" ")[3].replace("\n","")
                    sdis[sdi_name+"_"+channel] = bitmask
                except IndexError:
                    raise ValueError("SDI Lines formated incorrectly.")
            if(line.__contains__("!SDI")):
                SDI_flag = True

        return(sdis)

    def get_rules(self):
        with open("ARINC429_rules.txt","r") as rules_fd:
            temp_rules = rules_fd.readlines()
        rules_fd.close()

        rules_section = False
        for line in temp_rules:
            if(line[0] == "#" or line == "\n"):
                continue
            if(rules_section):
                line = line.split("#")[0] # remove endline comments
                self.handle_ruleline(line)
            if(line.__contains__("!Rules")):
                rules_section = True

        # Example formats:
        # <alert/log>* <channel>* <label> <SDI> <data> <SSM> <P> <Time> "<message (if alert)>"
        # <log>* <channel>* <label>/<bits>* -> logs the decoded data for this channel & label.
        # <alert/log>* <channel>* <bit[index1:index2) = "01..10"> "<message (if alert)>"
        # <alert/log>* <channel>* <label> <BCD/BNR/DISC> "<message (if alert)>"

    def handle_ruleline(self,line):
        rule = line.split(" ")

        alert_log = ""
        channel = ""
        bitmask = "0"*31
        parity_check = None
        time_notate = False
        message = ""
        try:
            message = line.split('"')[1]
            temp = line.replace('"',"")
            temp = temp.replace(message,"")
            temp = temp.replace("\n","")
            rule = temp.split(" ")
        except IndexError:
            pass # message is already nothing.

        if(not (rule[0].__contains__("alert") or rule.__contains__("log")) ):
            print(f"Problem with rule: {line}")
            raise ValueError("Rule must delineate between Alerting or Logging.")
        else:
            alert_log = rule[0]

        # remove the message from the rule list
        cnt = 0
        for item in rule:
            cnt += 1
            if(item.__contains__('"')):
                # message start
                rule = rule[:cnt]

        if(not rule[1] in self.get_channelnames()):
            print(f"Problem with rule: {line}")
            raise ValueError("Rule must delineate between Channels.")
        else:
            channel = rule[1]

        rulez = Queue()
        [rulez.put(rule[i]) for i in range(2,len(rule))]

        octal_flag = True
        SDI_flag = True
        data_flag = True
        SSM_flag = True
        parity_flag = True
        time_flag = True
        #message_flag = True

        while(rulez.qsize() > 0):
            r = rulez.get().replace("\n","")
            # octal
            if(r.__contains__("0o") and octal_flag):
                octal_flag = False
                label = int(r,8)
                label_chip = lru_txr()
                l, _ = label_chip.make_label_for_word(label)
                bitmask = self.replace_index(0,8,bitmask,l)
            # SDI
            elif(SDI_flag and r+f"_{channel}" in self.sdis):
                SDI_flag = False
                this_sdi = r
                bitmask = self.replace_index(8,10,bitmask,self.sdis[r+f"_{channel}"])
            # Handle data / bits
            elif(data_flag and r.__contains__("bits[") or r.__contains__("data:")):
                data_flag = False
                if(r.__contains__("bits[")):
                    rz = r.split("=")[1].replace('"','')
                    index1 = int(r.split("[")[1].split(":")[0])
                    index2 = int(r.split(":")[1].split(")")[0])
                    if((index2-1)-index1 != len(rz)):
                        print(f"Expected bitmask of length {(index2-1)-index1}, got {len(rz)}")
                        raise ValueError("Bit String to look for does not match length!")
                    cnt = 0
                    # Check if this contradicts the label/sdi
                    for char in bitmask[index1-1:index2]:
                        try:
                            if(char == "1" and rz[cnt] != char):
                                raise ValueError("Bit mask contradicts other flags!!")
                            cnt += 1
                        except IndexError: # reached past the bit mask.
                            break
                    bitmask = self.replace_index(index1-1,index2-2,bitmask,rz)
                    #bitmask += 19 - len(rz)
                elif(r.__contains__("data:")):
                    if(octal_flag != False): #Need the label
                        raise ValueError(f"Label needed in order to properly search word for given data: {r.split(':')[1]}")
                    if(SDI_flag != False): # Need the LRU for the equipment ID
                        raise ValueError(f"Equipment Name needed in order to properly search word for given data: {r.split(':')[1]}")
                    #Figure out if encode to DISC, BNR or BCD

                    for equipID, equipName in self.equip_ids.items():
                        if(equipName.__contains__(this_sdi)):
                            break

                    #equipID = self.equip_ids[this_sdi]
                    encode_type = self.all_labels[label][equipID][0]
                    resolution = self.all_labels[label][equipID][1]
                    try:
                        data = float(r.split(":")[1])
                    except ValueError:
                        raise ValueError("Data given to check is not a number!")
                    if(encode_type == "BCD"):
                        bitmask = self.replace_index(9,
                                                     29,
                                                     bitmask,
                                                     self.BCD_digs(data, resolution))
                    elif(encode_type == "BNR"):
                        bitmask = self.replace_index(9,
                                                     29,
                                                     bitmask,
                                                     self.BNR_encode())
                    elif(encode_type == "DISC"):
                        bitmask = self.replace_index(9,
                                                     29,
                                                     bitmask,
                                                     self.DISC_encode())
                    elif(encode_type == "SAL"):
                        bitmask = self.replace_index(0,
                                                     8,
                                                     bitmask,
                                                     self.SAL_encode(r))
            elif(SSM_flag and len(r) == 2
                 and (r == "00" or r == "01" or r == "10" or r == "11")):
                try:
                    ssmThere = (int(r,2) >= 0 or int(r,2) <= 4)
                    if(ssmThere):
                        if(data < 0.0):
                            print("hello")
                        bitmask = self.replace_index(29,31,bitmask,r)
                        SSM_flag = False
                except ValueError:
                    pass
            elif(parity_flag and (r == "C" or r == "I")):
                parity_check = True if r == "C" else False
                parity_flag = False
            elif(time_flag and (r == "time")):
                time_flag = False
                time_notate = True
            #elif(message_flag and r.__contains__('"')):
            #    mess
            else:
                continue

        if(len(bitmask) != 31):
            raise ValueError(f"Bitmask length error: {len(bitmask)}, for {bitmask}. Error in parsing word!")

        self.rules.append((alert_log, channel, bitmask, parity_check, time_notate, message))

    def replace_index(self,index1:int,index2:int,ogstring:str,replacestr:str)->str:
        # ogstring[index1:index2] = replacestr
        new_str = ogstring[:index1] + replacestr + ogstring[index2:]
        return(new_str)

    def get_channelnames(self)->list:
        channelnames = []
        for chan, value in self.channels.items():
            channelnames.append(chan)
        return(channelnames)

    def alert_or_log(self, word:str):

        #self.rules.add(
        # 0 (alert_log,
        # 1 channel,
        # 2 bitmask,
        # 3 parity_check,
        # 4 time_notate,
        # 5 message)
        # )
        with open(self.log_filepath, "a") as log_fd:
            with open(self.alert_filepath,"a") as alert_fd:
                for tuple in self.rules:
                    parity = tuple[3]
                    time = tuple[4]
                    flag_this_tuple = False
                    # Part 1 Check if you should flag this word.
                    if(tuple[0].__contains__("alert")):
                        #TODO Check channel?
                        p_bitmask = tuple[2] + lru_txr.calc_parity(tuple[2])
                        bitmask = tuple[2] #+ lru_txr.calc_parity(tuple[2])
                        if(bitmask == 31*"0"):
                            flag_this_tuple = True
                        word_check = word[-1:]
                        if(int(bitmask,2) & int(word_check,2) == int(bitmask,2) ):
                            if( (parity == True and word[-1] == p_bitmask)
                            or (parity == False and word[-1] != p_bitmask) ):
                                # alert
                                flag_this_tuple = True
                            elif(parity == None):
                                # alert
                                flag_this_tuple = True
                    # Part 2: If the word is flagged, the log it appropriately.
                    if(flag_this_tuple and time):
                        if(tuple[0].__contains__("alert")):
                            alert_fd.write(f"{time()}: Alert! {tuple[5]}\n")
                        if(tuple.__contains__("log")):
                            log_fd.write(f"{time()}: {word} {tuple[5]}\n")
                    elif(flag_this_tuple and time == False):
                        if(tuple[0].__contains__("alert")):
                            alert_fd.write(f"Alert! {tuple[5]}\n")
                        if(tuple.__contains__("log")):
                            log_fd.write(f"Logged word #{self.n}: {word} {tuple[5]}\n")
            alert_fd.close()
        log_fd.close()

    def log_all_words(self, channel_index):
        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            word = self.communication_chip.receive_given_word(channel_index)
            logs_fd.write(word)
        logs_fd.close()
        #bus_channel = self.BUS_CHANNELS[channel_index]

    def BCD_digs(self, value, res:float)->str:

        # TODO add handling for special cases for BCD

        #SDI = "00"
        #SSM = "00"
        #if(value < 0):
        #    SSM = "11"

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

        partial_data = dig5 + dig4 + dig3 + dig2 + dig1# + SSM
        return(partial_data)

    def BNR_encode(self):
        pass

    def DISC_encode(self):
        pass

    SALs = {
        "CVR": 0o157,
        "FCMC Com A340-500/600": 0o210,
        "FCMC Mon A340-500/600": 0o211,
        "FCMC Int A340-500/600": 0o212,
        "HUD": 0o225,
        "APM-MMR": 0o241,
        "MMR": 0o242,
        "ILS": 0o244,
        "MLS": 0o245,
        "AHRS": 0o246,
        "VDR #1": 0o251,
        "VDR #2": 0o252,
        "VDR #3": 0o253,
        "GPWS": 0o310,
        "GNLU 1": 0o311,
        "GNLU 2": 0o312,
        "GNLU 3": 0o313,
        "GNU 1": 0o314,
        "GNU 2": 0o315,
        "GNU 3": 0o316,
        "AUTOTHROTTLE COMPUTER": 0o321,
        "FCC 1": 0o322,
        "FCC 2": 0o323,
        "FCC 3": 0o324,
        "APU": 0o325,
        "APU CONTROLLER": 0o326,
        "Mode Control Panel (MCP)": 0o327,
        "FMC 3": 0o330,
        "ATC TRANSPONDER": 0o331,
        "DADC": 0o332,
        "Passenger Services System (PSS) 767-300,400": 0o362,
        "Cabin Service System (CSS) 747-400": 0o363,
        "Audio Entertainment System (AES) Boeing": 0o364,
        "Multicast": 0o366,
        "Bridge": 0o367
    }
    def SAL_encode(self, SAL_str):
        sal_label_chip = lru_txr()
        return(sal_label_chip.decode(self.SALs[SAL_str]))