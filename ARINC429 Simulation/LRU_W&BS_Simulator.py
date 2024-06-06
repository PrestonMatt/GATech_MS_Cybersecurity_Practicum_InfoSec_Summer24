from arinc429_voltage_sim import binary_to_voltage as b2v

class weight_and_balance_system:
    # Responsible for making plane go left and right
    # also manages fuel balancing and center of gravity

    # BTW CG or C/G = center of gravity
    applicable_labels_BCD = {
        0o052: 'BCD', # Longitude Zero Fuel CG
        0o056: 'BCD', # Gross Weight (KG)
        0o052: 'BCD', # Longitude Zero Fuel CG
        0o060: 'BCD', # Tire Loading (Left Body Main)
        0o061: 'BCD', # Tire Loading (Right Body Main)
        0o062: 'BCD', # Tire Loading (Left Wing Main)
        0o063: 'BCD', # Tire Loading (Right Wing Main)
        0o064: 'BCD', # Tire Loading (Nose)
        0o065: 'BCD', # Gross Weight
        0o066: 'BCD', # Longitudinal Center of Gravity
        0o067: 'BCD', # Lateral Center of Gravity
        0o167: 'BCD', # Zero Fuel Weight (lb)
        0o243: 'BCD', # Zero Fuel Weight (kg)
    }

    applicable_labels_DISC = {
        0o270: 'DISC', # Discrete Data #1
        0o357: 'DISC' # ISO Alphabet #5 Message
    }

    applicable_labels_BNR = {
        0o054: 'BNR', # Zero Fuel Weight (KG)
        0o070: 'BNR', # Hard landing Magnitude #1
        0o071: 'BNR', # Hard landing Magnitude #2
        0o074: 'BNR', # Zero Fuel Weight (lb)
        0o075: 'BNR', # Gross Weight
        0o076: 'BNR', # Longitudinal Center of Gravity
        0o077: 'BNR', # Lateral Center of Gravity
        0o100: 'BNR', # Gross Weight (Kilogram)
        0o107: 'BNR', # Longitude Zero Fuel C/G

    }

    def __init__(self):
        pass

    def __str__(self):
        pass

