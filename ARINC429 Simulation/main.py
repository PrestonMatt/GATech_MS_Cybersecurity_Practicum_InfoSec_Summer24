# Import Python modules
import os
from threading import Thread
from time import sleep, time
from random import choice
# Import MY classes
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_FAEC_Simulator import full_authority_engine_control as FAEC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_WnBS_Simulator import weight_and_balance_system as WnBS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from LRU_RMS_Simulator import radio_management_system as RMS
from BusQueue_Simulator import GlobalBus as ARINC429BUS

global bus_speed

altitudes = []
ground_speeds = []
times_in_UNIX_epoch = []
lats = []
lons = []
rolls = []
interprolated_aoa = []
true_headings = []
wind_speeds = []

sampling_rate = 0.05

def get_data():
    flightdata_filenames = os.getcwd() + r"\Flight_data\Attack_Demo_Flight_Data"
    # Dataset no. 1: Altitude.
    with open(flightdata_filenames+r"\Baro_Altitude.txt", "r") as altitude_fd:
        altitudes = altitude_fd.readlines()
    altitude_fd.close()
    # Dataset no. 2: Ground Speed.
    with open(flightdata_filenames+r"\Ground_Speed.txt", "r") as ground_speeds_fd:
        ground_speeds = ground_speeds_fd.readlines()
    ground_speeds_fd.close()
    # Dataset no. 3: Time as UTC Epoch.
    with open(flightdata_filenames+r"\Pos_Epoch.txt", "r") as times_fd:
        times_in_UNIX_epoch = times_fd.readlines()
    times_fd.close()
    # Dataset no. 4: Latitude and Longitudes.
    with open(flightdata_filenames+r"\Pos.txt", "r") as latlon_fd:
        lats_lons = latlon_fd.readlines()
    latlon_fd.close()
    # Dataset no. 5: Roll.
    with open(flightdata_filenames+r"\Roll.txt", "r") as roll_fd:
        rolls = roll_fd.readlines()
    roll_fd.close()
    # Dataset no. 6: Heading.
    with open(flightdata_filenames+r"\True_Heading.txt", "r") as true_heading_fd:
        true_headings = true_heading_fd.readlines()
    true_heading_fd.close()
    # Dataset no. 7: Wind Speed.
    with open(flightdata_filenames+r"\Wind_Speed.txt", "r") as wind_speed_fd:
        wind_speeds = wind_speed_fd.readlines()
    wind_speed_fd.close()
    # Data Handling:
    # Altitudes:
    prev_alt = 250.0 # There are some points where it cuts off, so I'll interpolate:
    for altIndex in range(len(altitudes)):
        if(altitudes[altIndex] == 'n/a\n'):
            altitudes[altIndex] = prev_alt
        else:
            alt = altitudes[altIndex].replace(' ft','').replace('\n','')
            try:
                alt = int(alt)
            except ValueError:
                #print(alt)
                alt = int(alt.split(' ')[1])
            altitudes[altIndex] = alt
        prev_alt = altitudes[altIndex]
    # Ground Speeds:
    # There are some points where it cuts off, so I'll interpolate:
    prev_gs = 181.0
    for gsIndex in range(len(ground_speeds)):
        if(ground_speeds[gsIndex] == 'n/a\n'):
            ground_speeds[gsIndex] = prev_gs
        else:
            ground_speeds[gsIndex] = float(ground_speeds[gsIndex].split(' ')[0])
        prev_gs = ground_speeds[gsIndex]
    # Time:
    for timeIndex in range(len(times_in_UNIX_epoch)):
        times_in_UNIX_epoch[timeIndex] = int(times_in_UNIX_epoch[timeIndex].replace('\n',''))
    lats = []
    lons = []
    for posIndex in range(len(lats_lons)):
        line = lats_lons[posIndex].encode('utf-8').replace(b'\n',b'').replace(b'\xc3\x82\xc2\xb0',b'').replace(b',',b'')
        line = line.decode('utf-8').split(' ')
        lat = float(line[0])
        lon = float(line[1])
        lats.append(lat)
        lons.append(lon)
    for rollIndex in range(len(rolls)):
        if(rolls[rollIndex] == 'n/a\n' or rolls[rollIndex] == 'n/a'):
            rolls[rollIndex] = 0.0 # in a runway so no roll obvs.
        else:
            rolls[rollIndex] = float(rolls[rollIndex].replace('\n',''))
    # Interprolate Indicated AoA
    with open(os.getcwd() + r"\Flight_data\Tail_687_1"+r"\INDICATED ANGLE OF ATTACK_Tail_687_1_data.txt", "r") as indicated_aoa_fd:
        long_indicated_aoas = indicated_aoa_fd.readlines()
    indicated_aoa_fd.close()
    # Real world data set opened.
    # Starting interpolation.
    interprolated_aoa = []
    # Climbing:
    for aoaIndex1 in range(5981):
        iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        while(iaoa < 0.0 or iaoa >= 3.0):
            iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        interprolated_aoa.append(iaoa)
    interprolated_aoa = sorted(interprolated_aoa)
    # Stable:
    for aoaIndex2 in range(5981):
        iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        while(iaoa < -2.0 or iaoa > 2.0):
            iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        interprolated_aoa.append(iaoa)
    # Descending:
    desc_iaoa = []
    for aoaIndex2 in range(5982):
        iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        while(iaoa < 0.0 or iaoa >= 3.0):
            iaoa = round(float(choice(long_indicated_aoas).replace('\n','')),3)
        desc_iaoa.append(iaoa)
    desc_iaoa = reversed(sorted(desc_iaoa))
    for desc_iaoa_ in desc_iaoa:
        interprolated_aoa.append(desc_iaoa_)
    # True Headings:
    prev_heading = 180.0 # There are some points where it cuts off, so I'll interpolate:
    for tHeadingIndex in range(len(true_headings)):
        tHead = true_headings[tHeadingIndex]
        if(tHead == 'n/a\n'):
            true_headings[tHeadingIndex] = prev_heading
        else:
            tHead = float(tHead[:-3]) # Take off the degrees and the newline
            true_headings[tHeadingIndex] = tHead
            prev_heading = tHead
    # Wind Speeds:
    prev_wind_speed = 15 # There are some points where it cuts off, so I'll interpolate:
    for windSpeedIndex in range(len(wind_speeds)):
        ws = wind_speeds[windSpeedIndex]
        if(ws == 'n/a\n'):
            wind_speeds[windSpeedIndex] = prev_wind_speed
        else:
            ws = int(ws.split(" ")[0])
            wind_speeds[windSpeedIndex] = ws
            prev_wind_speed = ws
    """
    print(altitudes)
    input("Next")
    print(ground_speeds)
    input("Next")
    print(times_in_UNIX_epoch)
    input("Next")
    print(lats)
    input("Next")
    print(lons)
    input("Next")
    print(rolls)
    input("Next")
    print(interprolated_aoa)
    input("Next")
    print(true_headings)
    input("Next")
    print(wind_speeds)
    input("Next")
    """
    return( (altitudes, ground_speeds, times_in_UNIX_epoch, lats, lons, rolls, interprolated_aoa, true_headings, wind_speeds) )

def send_GPS_words(transmitting_LRU_GPS, words_to_TX):
    for word in words_to_TX:
        print(f"Sending word from GPS: 0b{bin(word)[2:]}")
        # transmit_given_word(self, word:int, bus_usec_start, channel_index=0, slowdown_rate = 5e-7)
        transmitting_LRU_GPS.communicator_chip.transmit_given_word(word=word,
                                                                   bus_usec_start=time(), #start time.
                                                                   channel_index=0,
                                                                   slowdown_rate=sampling_rate)

def send_ADIRU_words(transmitting_LRU_ADIRU, words_to_TX):
    for word in words_to_TX:
        print(f"Sending word from ADIRU: 0b{word}")
        # transmit_given_word(self, word:int, bus_usec_start, channel_index=0, slowdown_rate = 5e-7)
        transmitting_LRU_ADIRU.TXcommunicator_chip.transmit_given_word(word=int(word,2),
                                                                       bus_usec_start=time(), #start time.
                                                                       channel_index=0, # Channel for the Blue Bus
                                                                       slowdown_rate=sampling_rate)

def send_FMC_words(transmitting_LRU_FMC, words_to_TX):
    for word in words_to_TX:
        print(f"Sending word from FMC: 0b{word}")
        # transmit_given_word(self, word:int, bus_usec_start, channel_index=0, slowdown_rate = 5e-7)
        transmitting_LRU_FMC.communication_chip.transmit_given_word(word=int(word,2),
                                                                   bus_usec_start=time(), #start time.
                                                                   channel_index=0, # Green Bus
                                                                   slowdown_rate=sampling_rate)
        transmitting_LRU_FMC.communication_chip.transmit_given_word(word=int(word,2),
                                                                   bus_usec_start=time(), #start time.
                                                                   channel_index=1, # Purple Bus
                                                                   slowdown_rate=sampling_rate)

def receive_ADIRU_words(ADIRU_LRU, channel_index:int, sample_rate=sampling_rate):
    while(True):
        word_int, word_str = ADIRU_LRU.RXcommunicator_chip.receive_given_word(channel_index=channel_index,
                                                                             slowdown_rate=sample_rate)
        print(f"ADIRU Recv'd word: {word_str}")
        ADIRU_LRU.decode_GPS_word(word_str)

def receive_FMC_words(FMC_LRU, channel_index:int, sample_rate=sampling_rate):
    while(True):
        word_int, word_str = FMC_LRU.RXcomm_chip.receive_given_word(channel_index=channel_index, # Blue
                                                                    slowdown_rate=sample_rate)
        print(f"FMC Recv'd word: {word_str}")

def receive_RMS_words(RMS_LRU, sample_rate=sampling_rate):
    while(True):
        word_int_green, word_str_green = RMS_LRU.receive_chip.receive_given_word(channel_index=0, # Green
                                                                                slowdown_rate=sample_rate)
        word_int_purple, word_str_purple = RMS_LRU.receive_chip.receive_given_word(channel_index=1, # Purple
                                                                                  slowdown_rate=sample_rate)
        print(f"RMS Recv'd word for Green Channel: 0b{word_str_green}")
        print(f"RMS Recv'd word for Green Channel: 0b{word_str_purple}")
        RMS_LRU.decode_word(word_str_green)
        # "send" radio message:
        print("ADS-B Chirp (Green Info):")
        print(RMS_LRU.ADS_B_Message)
        RMS_LRU.decode_word(word_str_purple)
        # "send" radio message:
        print("ADS-B Chirp (Purple Info):")
        print(RMS_LRU.ADS_B_Message)

def receive_FAEC_words(FAEC_LRU, sample_rate=sampling_rate):
    while(True):
        word_int_green, word_str_green = FAEC_LRU.receive_chip.receive_given_word(channel_index=0, # Green
                                                                                 slowdown_rate=sample_rate)
        word_int_purple, word_str_purple = FAEC_LRU.receive_chip.receive_given_word(channel_index=1, # Purple
                                                                                   slowdown_rate=sample_rate)
        print(f"{FAEC_LRU.wingCardinality} FAEC Recv'd word for Green Channel: 0b{word_str_green}")
        print(f"{FAEC_LRU.wingCardinality} FAEC Recv'd word for Purple Channel: 0b{word_str_purple}")
        FAEC_LRU.decode_word(word_str_green)
        FAEC_LRU.decode_word(word_str_purple)

def receive_WnBS_words(WnBS_LRU, sample_rate=sampling_rate):
    while(True):
        word_int_green, word_str_green = WnBS_LRU.receive_chip.receive_given_word(channel_index=0, # Green
                                                                                  slowdown_rate=sample_rate)
        word_int_purple, word_str_purple = WnBS_LRU.receive_chip.receive_given_word(channel_index=1, # Purple
                                                                                    slowdown_rate=sample_rate)
        print(f"W&BS Recv'd word for Green Channel: 0b{word_str_green}")
        print(f"W&BS Recv'd word for Purple Channel: 0b{word_str_purple}")
        WnBS_LRU.decode_word(word_str_green)
        WnBS_LRU.decode_word(word_str_purple)

def main():
    global bus_speed
    bus_speed = "low"
    # Define all the bus objects:
    global OrangeBus # = ARINC429BUS()
    OrangeBus = ARINC429BUS()

    global BlueBus # = ARINC429BUS()
    BlueBus = ARINC429BUS()

    global PurpleBus # = ARINC429BUS()
    PurpleBus = ARINC429BUS()

    global GreenBus # = ARINC429BUS()
    GreenBus = ARINC429BUS()

    # Get all the data so we can make words:
    altitudes, ground_speeds, times_in_UNIX_epoch, lats, lons, rolls, interprolated_aoa, true_headings, wind_speeds = get_data()

    # Define the LRUs that need to be present across multiple buses:
    GPS_LRU = GPS(bus_speed, OrangeBus)
    GPS_words_to_TX = []
    for l_index in range(len(lats)):
        latitude = lats[l_index]
        degrees = int(abs(latitude))
        if(len(f"{degrees}") < 2):
            degrees = "0" + str(degrees)
        minutes = round((abs(latitude) - int(degrees)) * 60, 1)
        if(minutes < 10.0):
            minutes = "0" + str(minutes)
        latitude = f"N {degrees} Deg {minutes}"

        longitude = lons[l_index]
        degrees = int(abs(longitude))
        if(len(f"{degrees}") < 2):
            degrees = "0" + str(degrees)
        minutes = round((abs(longitude) - int(degrees)) * 60, 1)
        if(minutes < 10.0):
            minutes = "0" + str(minutes)
        longitude = f"E {degrees} Deg {minutes}"
        #print(f"Lat: {latitude}, Lon: {longitude}")
        GPS_LRU.set_position(latitude, longitude)

        lat_int, lon_int = GPS_LRU.from_lat_lon_to_word()
        GPS_words_to_TX.append(lat_int)
        GPS_words_to_TX.append(lon_int)

    # Start the TXr transmission in thread
    GPS_transmitter_thread = Thread(target=send_GPS_words, args=(GPS_LRU, GPS_words_to_TX,))

    ADIRU_LRU = ADIRU(bus_speed, [OrangeBus, BlueBus])
    FMC_LRU = FMC(bus_speed, "FIFO", BUS_CHANNELS=[BlueBus, PurpleBus, GreenBus])
    ADIRU_receiver_thread = Thread(target=receive_ADIRU_words, args=(ADIRU_LRU, 0, sampling_rate,))
    FMC_receiver_thread = Thread(target=receive_FMC_words, args=(FMC_LRU, 0, sampling_rate,))
    # Make the words to send for the ADIRU:
    ADIRU_words = []
    FMC_words = []
    prev_alt = altitudes[0]
    for alt in altitudes:
        ADIRU_LRU.set_value("Baro Corrected Altitude #1", str(alt) + " knots")
        altitude_word = ADIRU_LRU.encode_word(0o204)
        ADIRU_words.append(altitude_word)
        fmc_word1 = FMC_LRU.decodeADIRUword(altitude_word, prev_alt)
        FMC_words.append(fmc_word1)
        prev_alt = alt
    prev_gs = ground_speeds[0]
    for gs in ground_speeds:
        ADIRU_LRU.set_value("Ground Speed", str(gs) + " knots")
        ground_speed_word = ADIRU_LRU.encode_word(0o012)
        ADIRU_words.append(ground_speed_word)
        fmc_word2 = FMC_LRU.decodeADIRUword(ground_speed_word, prev_gs)
        FMC_words.append(fmc_word2)
        prev_gs = gs
    prev_lat = lats[0]
    for lat_ in lats:
        ADIRU_LRU.set_value("Present Position - Latitude", str(lat_) + " degrees")
        lat_word = ADIRU_LRU.encode_word(0o310)
        ADIRU_words.append(lat_word)
        fmc_word3 = FMC_LRU.decodeADIRUword(lat_word, prev_lat)
        FMC_words.append(fmc_word3)
        prev_lat = lat_
    prev_lon = lons[0]
    for lon_ in lons:
        ADIRU_LRU.set_value("Present Position - Longitude", str(lon_) + " degrees")
        lon_word = ADIRU_LRU.encode_word(0o311)
        ADIRU_words.append(lon_word)
        fmc_word4 = FMC_LRU.decodeADIRUword(lon_word, prev_lon)
        FMC_words.append(fmc_word4)
        prev_lon = lon_
    prev_roll = rolls[0]
    for roro in rolls:
        ADIRU_LRU.set_value("Roll Angle", str(roro) + " deg")
        roll_word = ADIRU_LRU.encode_word(0o325)
        ADIRU_words.append(roll_word)
        fmc_word5 = FMC_LRU.decodeADIRUword(roll_word, prev_roll)
        FMC_words.append(fmc_word5)
        prev_roll = roro
    prev_aoa = interprolated_aoa[0]
    for indicated_angle_of_attack in interprolated_aoa:
        ADIRU_LRU.set_value('Indicated Angle of Attack (Average)', str(indicated_angle_of_attack) + ' deg')
        iaoaWord = ADIRU_LRU.encode_word(0o221)
        ADIRU_words.append(iaoaWord)
        fmc_word6 = FMC_LRU.decodeADIRUword(iaoaWord, prev_aoa)
        FMC_words.append(fmc_word6)
        prev_aoa = indicated_angle_of_attack
    for tHead in true_headings:
        ADIRU_LRU.set_value('True Heading', str(tHead) + ' deg')
        ADIRU_words.append(ADIRU_LRU.encode_word(0o044))
    for wSpeed in wind_speeds:
        ADIRU_LRU.set_value('Wind Speed', str(wSpeed) + ' knots')
        ADIRU_words.append(ADIRU_LRU.encode_word(0o015))

    ADIRU_transmitter_thread = Thread(target=send_ADIRU_words, args=(ADIRU_LRU, ADIRU_words,))
    FMC_transmitter_thread = Thread(target=send_FMC_words, args=(FMC_LRU, FMC_words,))

    # Create all the RX LRUs:
    # RMS
    RMS_LRU = RMS(bus_speed, [PurpleBus, GreenBus])
    RMS_receiver_thread = Thread(target=receive_RMS_words, args=(RMS_LRU, sampling_rate,))
    # FAECs
    FAEC_1_LRU = FAEC(bus_speed, "left",1,[PurpleBus, GreenBus])
    FAEC_2_LRU = FAEC(bus_speed, "right",2,[PurpleBus, GreenBus])
    leftWing_receiver_thread = Thread(target=receive_FAEC_words, args=(FAEC_1_LRU, sampling_rate,))
    rightWing_receiver_thread = Thread(target=receive_FAEC_words, args=(FAEC_2_LRU, sampling_rate,))
    # WnBS
    WnBS_LRU = WnBS(bus_speed, [PurpleBus, GreenBus])
    WnBS_LRU_receiver_thread = Thread(target=receive_WnBS_words, args=(WnBS_LRU, sampling_rate,))

    # Start all the Threads:
    print("Starting all Threads for buses!")
    GPS_transmitter_thread.start()
    ADIRU_receiver_thread.start()
    ADIRU_transmitter_thread.start()
    FMC_receiver_thread.start()
    FMC_transmitter_thread.start()
    RMS_receiver_thread.start()
    leftWing_receiver_thread.start()
    rightWing_receiver_thread.start()
    WnBS_LRU_receiver_thread.start()
    # Join all the threads:
    GPS_transmitter_thread.join()
    ADIRU_receiver_thread.join()
    ADIRU_transmitter_thread.join()
    FMC_receiver_thread.join()
    FMC_transmitter_thread.join()
    RMS_receiver_thread.join()
    leftWing_receiver_thread.join()
    rightWing_receiver_thread.join()
    WnBS_LRU_receiver_thread.join()

if __name__ == '__main__':
    main()