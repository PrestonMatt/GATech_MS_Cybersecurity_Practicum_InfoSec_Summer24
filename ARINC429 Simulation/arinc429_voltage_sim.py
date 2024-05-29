import matplotlib.pyplot as plt
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
    print("Test being")
    test_all_functions()

def test_all_functions():
    print("Testing HIGH SPEED 1 bit.")
    graph_words(create_ARINC429_one_highspeed(0),figtitle = "One High speed Bit")

def graph_words(word,figtitle = "ARINC 429 Word with Random Bits"):
    ts = word[0]
    vs = word[1]

    fig, ax = plt.subplots()
    # want around -10, 0, 10
    ax.axhline(-10.0, linestyle="--")
    ax.axhline(0.0, linestyle="--")
    ax.axhline(10.0, linestyle="--")

    plt.plot(ts, vs, 'go--')
    plt.xlabel("Time in usec")
    plt.ylabel("Voltage")
    plt.title(figtitle)
    #plt.xticks(np.arange(min(ts),max(ts)+1,5))
    plt.show()

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

    this_bit_usec_total = rise_usecs + stab_usecs + fall_usecs + null_usecs
    #print(rise_usecs, stab_usecs, fall_usecs, null_usecs)

    # Array is in microseconds. This is the HIGH SPEED standard
    t_usecs = np.arange(usec_start,
                         usec_start + this_bit_usec_total,
                         0.5) # sample every 1/2 microsecond.

    # rise:
    for step1 in range(int(rise_usecs * 2)): # maps to -> range(0.0,1.5,0.5):
        rise_voltage = random.uniform(0.0,10.0)
        v_rise.append(rise_voltage)
    v_rise.sort()

    # high:
    for step2 in range(int(stab_usecs * 2)): # maps to -> range(1.5,5,0.5):
        stable_voltage = random.uniform(9.0,11.0)
        v_stab.append(stable_voltage)

    # fall:
    for step3 in range(int(fall_usecs * 2)): # maps to -> range(5,6.5,0.5):
        fall_voltage = random.uniform(0.0,10.0)
        v_fall.append(fall_voltage)
    v_fall.sort(reverse=True) # need to reverser order this sort

    # null:
    for step4 in range(int(null_usecs * 2)): # maps to -> range(6.5,10.0,0.5):
        null_voltage = random.uniform(-0.5,0.5)
        v_null.append(null_voltage)

    voltages = np.concatenate(
        (v_rise, v_stab, v_fall, v_null)
    )

    #print("Time: %s" % t_usecs)
    #print("Voltages: %s", voltages)

    return(t_usecs,voltages)

if __name__ == "__main__":
    main()
