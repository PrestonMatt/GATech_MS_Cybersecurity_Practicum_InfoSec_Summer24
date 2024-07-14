# Import Python modules
import os
from threading import Thread
from time import sleep, time, ctime
from random import choice
import matplotlib.pyplot as plt
# Import MY classes
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_FAEC_Simulator import full_authority_engine_control as FAEC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_WnBS_Simulator import weight_and_balance_system as WnBS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from LRU_RMS_Simulator import radio_management_system as RMS
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from ARINC429_IDS import arinc429_intrusion_detection_system as IDS

global bus_speed

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'

altitudes = []
ground_speeds = []
times_in_UNIX_epoch = []
lats = []
lons = []
rolls = []
interprolated_aoa = []
true_headings = []
wind_speeds = []

word_tx_rate = 0.005

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

def main():

    word_tx_rate = float(input("Please input a word transmission slowdown rate for the bus (default: 0.005):"))
    attack_flag = input("Do you want to simulate an attack here (y for yes)?") == "y"
    ids_flag = input("Do you want to turn on the IDS (y for yes)?") == "y"

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

    # Set up IDS:

    print(f"\n{Colors.RED}Setting up the IDS")
    rules_filename = os.getcwd() + r"\IDS_Rules_test_files\IDS_MAIN_RULES_FILES\MainNT_Rules.txt"
    alert_filename = os.getcwd() + r"\IDS_Rules_test_files\IDS_MAIN_RULES_FILES\Alerts_Logs\Alerts_MAIN.txt"
    log_filename = os.getcwd() + r"\IDS_Rules_test_files\IDS_MAIN_RULES_FILES\Alerts_Logs\Logs_MAIN.txt"
    # Reset the files in between runs:
    with open(alert_filename,"w") as alert_fd:
        alert_fd.write(f"Starting Main demo at {ctime()}\n")
    alert_fd.close()
    with open(log_filename,"w") as log_fd:
        log_fd.write(f"Starting Main demo at {ctime()}\n")
    log_fd.close()
    channels = [OrangeBus,BlueBus,PurpleBus,GreenBus]
    timer_start = time()
    IDS_main = IDS(bus_speed, BUS_CHANNELS=channels, rules_file=rules_filename)
    IDS_main.alert_filepath = alert_filename
    IDS_main.log_filepath = log_filename
    timer_end = time()
    print(f"Set up IDS for main simulation in {round(timer_end-timer_start,5)} seconds.{Colors.RESET}")
    print(f"{Colors.YELLOW}Loading flight data.")
    # Get all the data so we can make words:
    altitudes, ground_speeds, times_in_UNIX_epoch, lats, lons, rolls, interprolated_aoa, true_headings, wind_speeds = get_data()
    print(f"Flight data loaded. Starting word simulation.{Colors.RESET}\n")
    # Define the LRUs that need to be present across multiple buses:
    # Orange bus:
    GPS_LRU = GPS(bus_speed, OrangeBus)
    ADIRU_LRU = ADIRU(bus_speed, [OrangeBus, BlueBus])
    GPS_TX_lat_words = []
    GPS_TX_lon_words = []
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
        GPS_TX_lat_words.append(lat_int)
        GPS_TX_lon_words.append(lon_int)

    FMC_LRU = FMC(bus_speed, "FIFO", BUS_CHANNELS=[BlueBus, PurpleBus, GreenBus])
    # Create all the RX LRUs:
    # RMS
    RMS_LRU = RMS(bus_speed, [PurpleBus, GreenBus])
    # FAECs
    FAEC_1_LRU = FAEC(bus_speed, "left",1,[PurpleBus, GreenBus])
    FAEC_2_LRU = FAEC(bus_speed, "right",2,[PurpleBus, GreenBus])
    # WnBS
    WnBS_LRU = WnBS(bus_speed, [PurpleBus, GreenBus])

    ADIRU_words = []
    # Make the words to send for the ADIRU:
    for alt in altitudes:
        ADIRU_LRU.set_value("Baro Corrected Altitude #1", str(alt) + " knots")
        altitude_word = ADIRU_LRU.encode_word(0o204)
        ADIRU_words.append(altitude_word)
    for gs in ground_speeds:
        ADIRU_LRU.set_value("Ground Speed", str(gs) + " knots")
        ground_speed_word = ADIRU_LRU.encode_word(0o012)
        ADIRU_words.append(ground_speed_word)
    for lat_ in lats:
        ADIRU_LRU.set_value("Present Position - Latitude", str(lat_) + " degrees")
        lat_word = ADIRU_LRU.encode_word(0o310)
        ADIRU_words.append(lat_word)
    for lon_ in lons:
        ADIRU_LRU.set_value("Present Position - Longitude", str(lon_) + " degrees")
        lon_word = ADIRU_LRU.encode_word(0o311)
        ADIRU_words.append(lon_word)
    for roro in rolls:
        ADIRU_LRU.set_value("Roll Angle", str(roro) + " deg")
        roll_word = ADIRU_LRU.encode_word(0o325)
        ADIRU_words.append(roll_word)
    for indicated_angle_of_attack in interprolated_aoa:
        ADIRU_LRU.set_value('Indicated Angle of Attack (Average)', str(indicated_angle_of_attack) + ' deg')
        iaoaWord = ADIRU_LRU.encode_word(0o221)
        ADIRU_words.append(iaoaWord)
    for tHead in true_headings:
        ADIRU_LRU.set_value('True Heading', str(tHead) + ' deg')
        ADIRU_words.append(ADIRU_LRU.encode_word(0o044))
    for wSpeed in wind_speeds:
        ADIRU_LRU.set_value('Wind Speed', str(wSpeed) + ' knots')
        ADIRU_words.append(ADIRU_LRU.encode_word(0o015))
    #print(len(GPS_TX_lon_words), len(GPS_TX_lat_words), len(ADIRU_words), len(FMC_words))
    #print(len(altitudes))
    # total number of words:
    numWords = 107_664 + len(GPS_TX_lon_words) + len(GPS_TX_lat_words) + (2 * len(ADIRU_words))
    if(attack_flag):
        numWords += (100 * 2 * 8) # 8 lat/lon hits across 2 channels, 100 words per attack.
    # Needed ADIRU words twice because they get sent across two buses.
    # 107_664 is the number of words the FMC will generate based off the ADIRU.
    print(f"This flight will generate, send, and receive {numWords} words among four buses.")
    print("Please note that for a real flight, the totals and number of channels would be considerably higher.")
    input("Press enter to send the words.")
    gps_index = 0
    alert_logs_hits_time = []
    als = []
    timer_alert_log_start = time()
    timer_start = time()
    # Iterate over each list evenly:
    for index in range(len(ADIRU_words)):
        if(index % 8 == 0):
            gps_index = int(index / 8)
            #print(gps_index)
            lon_bits = bin(GPS_TX_lon_words[gps_index])[2:]
            GPS_lon_word = "0" * (32 - len(lon_bits)) + lon_bits
            print(f"{Colors.ORANGE}Sending word from GPS to ADIRU:\t\t\t\t\t0b{GPS_lon_word}")
            ADIRU_LRU.decode_GPS_word(GPS_lon_word)
            if(ids_flag):
                # Orange Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(GPS_lon_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            lat_bits = bin(GPS_TX_lat_words[gps_index])[2:]
            GPS_lat_word = "0" * (32 - len(lat_bits)) + lat_bits
            print(f"Sending word from GPS to ADIRU:\t\t\t\t\t0b{GPS_lat_word}")
            ADIRU_LRU.decode_GPS_word(GPS_lat_word)
            if(ids_flag):
                # Orange Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(GPS_lat_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Transmit the altitude word:
            altitude_word = ADIRU_words[index]
            try:
                prev_alt = altitudes[gps_index - 1] if index > 0 else altitudes[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{altitude_word}{Colors.RESET}")
            fmc_word1 = FMC_LRU.decodeADIRUword(altitude_word, prev_alt)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(altitude_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word1}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word1}{Colors.RESET}")
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            RMS_LRU.decode_word(fmc_word1)
            FAEC_1_LRU.decode_word(fmc_word1)
            FAEC_2_LRU.decode_word(fmc_word1)
            WnBS_LRU.decode_word(fmc_word1)
            RMS_LRU.decode_word(fmc_word1)
            FAEC_1_LRU.decode_word(fmc_word1)
            FAEC_2_LRU.decode_word(fmc_word1)
            WnBS_LRU.decode_word(fmc_word1)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word1)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word1)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            if(attack_flag and (lats[gps_index] == 35.741 and lons[gps_index] == 50.578) ):
                # Simulate the attack:
                print(f"{Colors.RED}Executing Attack.{Colors.RESET}")
                # Uncomment this for demo.
                #cont = input("")
                downword = '01101100110000111100000000000000'
                for x in range(100):
                    print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word1}{Colors.RESET}")
                    print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word1}{Colors.RESET}")
                    RMS_LRU.decode_word(downword)
                    FAEC_1_LRU.decode_word(downword)
                    FAEC_2_LRU.decode_word(downword)
                    WnBS_LRU.decode_word(downword)
                    RMS_LRU.decode_word(downword)
                    FAEC_1_LRU.decode_word(downword)
                    FAEC_2_LRU.decode_word(downword)
                    WnBS_LRU.decode_word(downword)
                    if(ids_flag):
                        hit, _alert_log_ = IDS_main.alert_or_log(downword)
                        if(hit):
                            alert_logs_hits_time.append(time())
                            als.append([time(),_alert_log_])
                        IDS_main.n += 1
        elif(index % 8 == 1):
            gsIndex = gps_index
            # Transmit the altitude word:
            ground_speed_word = ADIRU_words[index]
            try:
                prev_gs = ground_speeds[gsIndex - 1] if index > 0 else ground_speeds[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{ground_speed_word}{Colors.RESET}")
            fmc_word2 = FMC_LRU.decodeADIRUword(ground_speed_word, prev_gs)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(ground_speed_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word2}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word2}{Colors.RESET}")
            RMS_LRU.decode_word(fmc_word2)
            FAEC_1_LRU.decode_word(fmc_word2)
            FAEC_2_LRU.decode_word(fmc_word2)
            WnBS_LRU.decode_word(fmc_word2)
            RMS_LRU.decode_word(fmc_word2)
            FAEC_1_LRU.decode_word(fmc_word2)
            FAEC_2_LRU.decode_word(fmc_word2)
            WnBS_LRU.decode_word(fmc_word2)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word2)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word2)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
        elif(index % 8 == 2):
            latIndex = gps_index
            # Transmit the latitude word:
            lat_word = ADIRU_words[index]
            try:
                prev_lat = lats[latIndex - 1] if index > 0 else lats[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{lat_word}{Colors.RESET}")
            fmc_word3 = FMC_LRU.decodeADIRUword(lat_word, prev_lat)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(lat_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word3}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word3}{Colors.RESET}")
            RMS_LRU.decode_word(fmc_word3)
            FAEC_1_LRU.decode_word(fmc_word3)
            FAEC_2_LRU.decode_word(fmc_word3)
            WnBS_LRU.decode_word(fmc_word3)
            RMS_LRU.decode_word(fmc_word3)
            FAEC_1_LRU.decode_word(fmc_word3)
            FAEC_2_LRU.decode_word(fmc_word3)
            WnBS_LRU.decode_word(fmc_word3)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word3)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word3)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
        elif(index % 8 == 3):
            lonIndex = gps_index
            # Transmit the longitude word:
            lon_word = ADIRU_words[index]
            try:
                prev_lon = lons[lonIndex - 1] if index > 0 else lons[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{lon_word}{Colors.RESET}")
            fmc_word4 = FMC_LRU.decodeADIRUword(lon_word, prev_lon)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(lon_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word4}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word4}{Colors.RESET}")
            RMS_LRU.decode_word(fmc_word4)
            FAEC_1_LRU.decode_word(fmc_word4)
            FAEC_2_LRU.decode_word(fmc_word4)
            WnBS_LRU.decode_word(fmc_word4)
            RMS_LRU.decode_word(fmc_word4)
            FAEC_1_LRU.decode_word(fmc_word4)
            FAEC_2_LRU.decode_word(fmc_word4)
            WnBS_LRU.decode_word(fmc_word4)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word4)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word4)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
        elif(index % 8 == 4):
            rollIndex = gps_index
            # Transmit the roll angle word:
            roll_word = ADIRU_words[index]
            try:
                prev_roll = rolls[rollIndex - 1] if index > 0 else rolls[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{roll_word}{Colors.RESET}")
            fmc_word5 = FMC_LRU.decodeADIRUword(roll_word, prev_roll)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(roll_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word5}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word5}{Colors.RESET}")
            RMS_LRU.decode_word(fmc_word5)
            FAEC_1_LRU.decode_word(fmc_word5)
            FAEC_2_LRU.decode_word(fmc_word5)
            WnBS_LRU.decode_word(fmc_word5)
            RMS_LRU.decode_word(fmc_word5)
            FAEC_1_LRU.decode_word(fmc_word5)
            FAEC_2_LRU.decode_word(fmc_word5)
            WnBS_LRU.decode_word(fmc_word5)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word5)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word5)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
        elif(index % 8 == 5):
            aoaIndex = gps_index
            # Transmit the indicated angle of attack word:
            aoa_word = ADIRU_words[index]
            try:
                prev_aoa = interprolated_aoa[aoaIndex - 1] if index > 0 else interprolated_aoa[0]
            except IndexError:
                raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{aoa_word}{Colors.RESET}")
            fmc_word6 = FMC_LRU.decodeADIRUword(aoa_word, prev_aoa)
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(aoa_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            # Receive the FMC word for all the channels:
            # Purple / Green Buses:
            print(f"{Colors.GREEN}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word6}{Colors.RESET}")
            print(f"{Colors.MAGENTA}Sending word from FMC to RMS, FAEC-1, FAEC-2, and W&BS:\t\t\t\t\t0b{fmc_word6}{Colors.RESET}")
            RMS_LRU.decode_word(fmc_word6)
            FAEC_1_LRU.decode_word(fmc_word6)
            FAEC_2_LRU.decode_word(fmc_word6)
            WnBS_LRU.decode_word(fmc_word6)
            RMS_LRU.decode_word(fmc_word6)
            FAEC_1_LRU.decode_word(fmc_word6)
            FAEC_2_LRU.decode_word(fmc_word6)
            WnBS_LRU.decode_word(fmc_word6)
            if(ids_flag):
                # Green Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word6)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
                # Purple Bus IDS:
                hit, _alert_log_ = IDS_main.alert_or_log(fmc_word6)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
        elif(index % 8 == 6):
            #tHeadIndex = gps_index
            # Transmit the true heading word:
            tHead_word = ADIRU_words[index]
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(tHead_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            #try:
            #    prev_tHead = true_headings[tHeadIndex - 1] if index > 0 else true_headings[0]
            #except IndexError:
            #    raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{tHead_word}{Colors.RESET}")
            #fmc_word7 = FMC_LRU.decodeADIRUword(tHead_word, prev_tHead)
        elif(index % 8 == 7):
            #wsIndex = gps_index
            # Transmit the wind speed word:
            ws_word = ADIRU_words[index]
            if(ids_flag):
                # Blue bus IDS
                hit, _alert_log_ = IDS_main.alert_or_log(ws_word)
                if(hit):
                    alert_logs_hits_time.append(time())
                    als.append([time(),_alert_log_])
                IDS_main.n += 1
            #try:
            #    prev_ws = wind_speeds[wsIndex - 1] if index > 0 else wind_speeds[0]
            #except IndexError:
            #    raise ValueError(f"Something wrong with Simulation Altitudes at index {index}!")
            print(f"{Colors.BLUE}Sending word from ADIRU to FMC:\t\t\t\t\t0b{ws_word}{Colors.RESET}")
            #fmc_word8 = FMC_LRU.decodeADIRUword(ws_word, prev_ws)
        sleep(word_tx_rate) # Helps visualize
        print('\n\n')
    timer_end = time()
    print(f"Finished Simulation in {round(timer_end-timer_start,5)} seconds.")
    print(f"Real world flight took: {times_in_UNIX_epoch[-1] - times_in_UNIX_epoch[0]} seconds or 8 hours, 21 minutes and 33 seconds.")
    ratio = (times_in_UNIX_epoch[-1] - times_in_UNIX_epoch[0]) / (timer_end - timer_start)
    print(f"Therefore, this simulation ran at {round(ratio,2)} times as fast.")

    if(ids_flag):
        # Graph the number of alerts & logs
        ts = []
        itms = []
        cnt = 0
        for t in alert_logs_hits_time:
            ts.append(t - timer_alert_log_start)
            itms.append(cnt)
            cnt += 1
        plt.plot(ts, itms,'bo-')
        plt.xlabel("Time (sec) normalized from Eval 3 Start")
        plt.ylabel("Total Words Flagged")
        plt.title("Total Number of Words Flagged over (normalized) Time")
        #plt.xticks(np.arange(min(ts),max(ts)+1,tickrate))
        plt.show()
        plt.grid(True)
        plt.clf()
        # Show the plot as stacked histogram.
        _alerts_ = []
        a_cnt = 0
        _logs_ = []
        l_cnt = 0
        _alertlog_ = []
        al_cnt = 0
        for alelo in als:
            if(alelo[1] == "alert"):
                a_cnt += 1
            elif(alelo[1] == "log"):
                l_cnt += 1
            elif(alelo[1] == "alert/log"):
                al_cnt += 1
            _alerts_.append(a_cnt)
            _logs_.append(l_cnt)
            _alertlog_.append(al_cnt)
        #print(_logs_, _alertlog_)
        #print(_alerts_, _logs_, _alertlog_)
        plt.stackplot(ts, _alerts_, _logs_, _alertlog_, labels=['Alerts', 'Logs', 'Both'])
        plt.title('Stacked Area Chart of Words Flagged Over Time')
        plt.xlabel('Time (sec) Normalized')
        plt.ylabel('Total Words Flagged')
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    main()