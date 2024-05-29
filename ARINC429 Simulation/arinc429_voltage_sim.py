import matplotlib as plt
import numpy as np
import random

# TX
# HIGH  (i.e. 1) =>      10.0 V +/- 1.0 V
# NULL                    0.0 V +/- 0.5 V
# LOW   (i.e. 0) =>     -10.0 V +/- 1.0 V

# RX
# HIGH  (i.e. 1) =>     [+ 6.5V, +13.0V]
# NULL                  [- 2.5V, + 2.5V]
# LOW   (i.e. 0) =>     [-13.0V, - 6.5V]

def main():
    print("test")

def create_ARINC429_one_highspeed(usec_start):
    # first [0.5,2.0] usec
    v_rise =[]
    rise_usecs = random.randint(2,4) / 2
    # next [4.5,5.5] usec
    v_stab = []
    stab_usecs = random.randint(9,11) / 2
    # next [0.5,2.0] usec
    v_fall = []
    fall_usecs = random.randint(2,4) / 2
    # final [4.5,5.5] usec
    v_null = []
    null_usecs = random.randint(9,11) / 2

if __name__ == "__main__":
    main()
