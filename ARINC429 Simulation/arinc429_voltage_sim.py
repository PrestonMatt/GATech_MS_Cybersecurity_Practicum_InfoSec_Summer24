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
    #print("Testing HIGH SPEED 1 bit.")
    #graph_words(create_ARINC429_one_highspeed(0),figtitle = "One High speed Bit")
    #print("Testing LOW SPEED 1 bit.")
    #graph_words(create_ARINC429_one_lowspeed(0),figtitle = "One Low speed Bit")
    #print("Testing HIGH SPEED 0 bit.")
    #graph_words(create_ARINC429_zero(0,True),figtitle = "Zero High speed Bit")
    #print("Testing LOW SPEED 0 bit.")
    #graph_words(create_ARINC429_zero(0,False),figtitle = "Zero Low speed Bit")
    print("Creating Random High Speed Word.")
    graph_words(create_random_word(True))
    print("Creating Random Low Speed Word.")
    graph_words(create_random_word(False),tickrate = 50)

def graph_words(word,figtitle = "ARINC 429 Word with Random Bits",tickrate=5):
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
    plt.xticks(np.arange(min(ts),max(ts)+1,tickrate))
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

def create_ARINC429_one_lowspeed(usec_start):
    # Array is in microseconds. This is the LOW SPEED standard
    # 12 kbps = 0.012 bits per microsecond = 83.33 usec per bit -> round to 84
    
    # first [5,15] usec
    v_rise =[]
    rise_usecs = random.randint(5,15)
    # next [40,44] usec
    v_stab = []
    stab_usecs = random.randint(40,44)
    # next [5,15] usec
    v_fall = []
    fall_usecs = random.randint(5,15)
    # final [40,44] usec
    v_null = []
    null_usecs = random.randint(40,44)

    this_bit_usec_total = rise_usecs + stab_usecs + fall_usecs + null_usecs
    #print(rise_usecs, stab_usecs, fall_usecs, null_usecs)

    
    t_usecs = np.arange(usec_start,
                         usec_start + this_bit_usec_total,
                         0.5) # sample every 1/2 microsecond.

    # rise:
    for step1 in range(rise_usecs * 2): 
        rise_voltage = random.uniform(0.0,10.0)
        v_rise.append(rise_voltage)
    v_rise.sort()

    # high:
    for step2 in range(stab_usecs * 2): 
        stable_voltage = random.uniform(9.0,11.0)
        v_stab.append(stable_voltage)

    # fall:
    for step3 in range(fall_usecs * 2): 
        fall_voltage = random.uniform(0.0,10.0)
        v_fall.append(fall_voltage)
    v_fall.sort(reverse=True) # need to reverser order this sort

    # null:
    for step4 in range(null_usecs * 2): 
        null_voltage = random.uniform(-0.5,0.5)
        v_null.append(null_voltage)

    voltages = np.concatenate(
        (v_rise, v_stab, v_fall, v_null)
    )

    return(t_usecs,voltages)

def create_ARINC429_zero(usec_start,lh_speed):
    if(lh_speed):
        ts, vs = create_ARINC429_one_highspeed(usec_start)
    else:
        ts, vs = create_ARINC429_one_lowspeed(usec_start)

    new_vs = []

    for voltage in vs:
        new_voltage = voltage * -1.0
        new_vs.append(new_voltage)

    zero_voltages = np.array(new_vs)

    return(ts,zero_voltages)

def create_random_word(lh_speed):
    voltages = np.array([0.0])
    times = np.array([0.0])

    for x in range(32):
        one_zero_bool = bool(random.getrandbits(1))
        if(one_zero_bool): # 1
            if(lh_speed): # HIGH SPEED
                ts, vs = create_ARINC429_one_highspeed(times[-1] + 0.5)
            else: # LOW SPEED
                ts, vs = create_ARINC429_one_lowspeed(times[-1] + 0.5)
        else: # 0
            ts, vs = create_ARINC429_zero(times[-1] + 0.5,lh_speed)

        voltages = np.concatenate((voltages,vs), axis = 0)
        times = np.concatenate((times, ts), axis = 0)

    return(times,voltages)

if __name__ == "__main__":
    main()
