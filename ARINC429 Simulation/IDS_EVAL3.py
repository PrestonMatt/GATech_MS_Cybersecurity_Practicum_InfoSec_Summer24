import os
import pytest
import matplotlib.pyplot as plt

from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from LRU_FMC_Simulator import flight_management_computer as FMC
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time, ctime
from datetime import datetime
from random import choice
def main():

    timer_start = time()
    print("Setting up LRUs ADIRU and FMC, and setting up IDS")
    rules_filename = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL3_RULES_FILES\Eval3_Rules.txt"
    flightdata_filenames = os.getcwd() + r"\Flight_data\Attack_Demo_Flight_Data"
    bus_speed = "low"

    Channel1 = ARINC429BUS()
    Channel2 = ARINC429BUS()
    channels = [Channel1, Channel2]

    IDS_test_numX = IDS(bus_speed, BUS_CHANNELS=channels, rules_file=rules_filename)
    transmitting_LRU = ADIRU(bus_speed, BUS_CHANNELS=channels)
    FMC_ = FMC(bus_speed, BUS_CHANNELS=channels)
    transmitting_LRU.set_sdi('00')

    # Check the output files:
    #print(IDS_test_numX.log_filepath)
    #print(IDS_test_numX.alert_filepath)
    alertfilePath = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL3_RULES_FILES\Alerts_Logs\Alerts_EVAL3.txt"
    logfilePath = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL3_RULES_FILES\Alerts_Logs\Logs_EVAL3.txt"
    # Reset the files in between runs:
    with open(alertfilePath,"w") as alert_fd:
        alert_fd.write(f"Starting EVAL3 test at {ctime()}\n")
    alert_fd.close()
    with open(logfilePath,"w") as log_fd:
        log_fd.write(f"Starting EVAL3 test at {ctime()}\n")
    log_fd.close()
    #print(alertfilePath)
    #print(logfilePath)
    # Some error handling:
    if(IDS_test_numX.alert_filepath != alertfilePath):
        IDS_test_numX.set_alertfile(alertfilePath)
    if(IDS_test_numX.log_filepath != logfilePath):
        IDS_test_numX.set_logfile(logfilePath)
    #print(IDS_test_numX.alert_filepath)
    #print(IDS_test_numX.log_filepath)
    #cont = input("")
    timer_end = time()
    print(f"Done setting up LRUs ADIRU, FMC, and IDS in {round(timer_end - timer_start,10)} seconds")

    timer_start = time()
    print("Opening and analyzing flight data...")
    # Grab flight data to plug into ADIRU:
    # Remember to take off \n character in these files.
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
    # Dataset no. 5: Longitude.
    with open(flightdata_filenames+r"\Roll.txt", "r") as roll_fd:
        rolls = roll_fd.readlines()
    roll_fd.close()

    #print(len(altitudes), len(ground_speeds), len(times_in_UNIX_epoch), len(lats_lons), len(rolls))

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
    #print(interprolated_aoa)
    #print(len(interprolated_aoa))

    #print(f"Tables:\n{altitudes}\n{ground_speeds}\n{times_in_UNIX_epoch}\n{lats}\n{lons}\n{rolls}")
    #print(len(altitudes), len(ground_speeds), len(times_in_UNIX_epoch), len(lats), len(lons), len(rolls))

    timer_end = time()
    print(f"Finished opening and analyzing flight data in {round(timer_end-timer_start,3)} seconds.")
    cont = input("Press enter to start the test.")
    # Start Eval 3:
    timer_start = time()
    print("Beginning flight data evaluation 3...")
    prev_altitude = altitudes[0]
    prev_gs = ground_speeds[0]
    prev_lat_ = lats[0]
    prev_lon_ = lons[0]
    prev_roro = rolls[0]
    prev_indicated_angle_of_attack = interprolated_aoa[0]
    alert_logs_hits_time = []
    timer_alert_log_start = time()
    # I have 17944 data points in each array:
    for index in range(17944):
        # Get all the data points:
        altitude = altitudes[index]
        gs = ground_speeds[index]
        t = times_in_UNIX_epoch[index]
        datetime_object = datetime.fromtimestamp(t)
        lat_ = lats[index]
        lon_ = lons[index]
        roro = rolls[index]
        indicated_angle_of_attack = interprolated_aoa[index]
        # Turn those into data points when applicable:
        transmitting_LRU.set_value("Baro Corrected Altitude #1", str(altitude) + " knots")
        transmitting_LRU.set_value("Ground Speed", str(gs) + " knots")
        transmitting_LRU.set_value("Present Position - Latitude", str(lat_) + " degrees")
        transmitting_LRU.set_value("Present Position - Longitude", str(lon_) + " degrees")
        transmitting_LRU.set_value("Roll Angle", str(roro) + " deg")
        transmitting_LRU.set_value('Indicated Angle of Attack (Average)', str(indicated_angle_of_attack) + ' deg')
        # Get the words from those values:
        altWord = transmitting_LRU.encode_word(0o204)
        gsWord = transmitting_LRU.encode_word(0o012)
        latWord = transmitting_LRU.encode_word(0o310)
        lonWord = transmitting_LRU.encode_word(0o311)
        rollWord = transmitting_LRU.encode_word(0o325)
        iaoaWord = transmitting_LRU.encode_word(0o221)
        # Send to FMC & IDS:
        # Handle Altitude Words:
        IDS_test_numX.alert_or_log(altWord)
        IDS_test_numX.n += 1
        fmc_word1 = FMC_.decodeADIRUword(altWord, prev_altitude)
        hit = IDS_test_numX.alert_or_log(fmc_word1)
        if(hit):
            alert_logs_hits_time.append(time())
        # Handle Ground Speed Words:
        IDS_test_numX.alert_or_log(gsWord)
        IDS_test_numX.n += 1
        fmc_word2 = FMC_.decodeADIRUword(gsWord, prev_gs)
        hit = IDS_test_numX.alert_or_log(fmc_word2)
        if(hit):
            alert_logs_hits_time.append(time())
        # Handle Latitude Words:
        IDS_test_numX.alert_or_log(latWord)
        IDS_test_numX.n += 1
        fmc_word3 = FMC_.decodeADIRUword(latWord, prev_lat_)
        hit = IDS_test_numX.alert_or_log(fmc_word3)
        if(hit):
            alert_logs_hits_time.append(time())
        # Handle Longitude Words:
        IDS_test_numX.alert_or_log(lonWord)
        IDS_test_numX.n += 1
        fmc_word4 = FMC_.decodeADIRUword(lonWord, prev_lon_)
        hit = IDS_test_numX.alert_or_log(fmc_word4)
        if(hit):
            alert_logs_hits_time.append(time())
        # Handle Roll Words:
        IDS_test_numX.alert_or_log(rollWord)
        IDS_test_numX.n += 1
        fmc_word5 = FMC_.decodeADIRUword(rollWord, prev_roro)
        hit = IDS_test_numX.alert_or_log(fmc_word5)
        if(hit):
            alert_logs_hits_time.append(time())
        # Handle Indicated Angle of Attack Words:
        IDS_test_numX.alert_or_log(iaoaWord)
        IDS_test_numX.n += 1
        fmc_word6 = FMC_.decodeADIRUword(iaoaWord, prev_indicated_angle_of_attack)
        hit = IDS_test_numX.alert_or_log(fmc_word6)
        if(hit):
            alert_logs_hits_time.append(time())
        # Record the next prev value for the FMC:
        prev_altitude = altitude
        prev_gs = gs
        prev_lat_ = lat_
        prev_lon_ = lon_
        prev_roro = roro
        prev_indicated_angle_of_attack = indicated_angle_of_attack
        # Visualization for the test:
        print('\n\n')
        print(f"Flight data points gathered for step #{index+1}:")
        print(f"Time: {datetime_object},")
        print(f"Altitude: {altitude} ft, corresponding ADIRU word:\t\t\t\t\t0b{altWord}")
        print(f"Ground Speed: {gs} knots,  corresponding ADIRU word:\t\t\t0b{gsWord}")
        print(f"Latitude: {lat_} degrees, corresponding ADIRU word:\t\t\t\t0b{latWord}")
        print(f"Longitude: {lon_} degrees, corresponding ADIRU word:\t\t\t0b{lonWord}")
        print(f"Roll: {roro} degrees, corresponding ADIRU word:\t\t\t\t\t0b{rollWord}")
        print(f"Indicated Angle of Attack: {indicated_angle_of_attack}, corresponding ADIRU word:\t\t0b{iaoaWord}")
        print(f"\nFMC Word 1 (calc. from altitude):\t\t0b{fmc_word1}")
        print(f"FMC Word 2 (calc. from ground speed):\t0b{fmc_word2}")
        print(f"FMC Word 3 (calc. from latitude):\t\t0b{fmc_word3}")
        print(f"FMC Word 4 (calc. from longitude):\t\t0b{fmc_word4}")
        print(f"FMC Word 5 (calc. from roll):\t\t\t0b{fmc_word5}")
        print(f"FMC Word 6 (calc. from roll):\t\t\t0b{fmc_word6}")

        # Attack:
        if(lat_ == 35.741 and lon_ == 50.578):
            print("Executing Attack.")
            downword = '01101100110000111100000000000000'
            for x in range(100):
                hit = IDS_test_numX.alert_or_log(downword)
                if(hit):
                    alert_logs_hits_time.append(time())
                IDS_test_numX.n += 1
            #cont = input("asdf")

    timer_end = time()
    print(f"\n\n\n\n\nThis concludes Eval 3. It took {round(timer_end-timer_start, 3)} seconds.")
    # Graph the number of alerts & logs
    ts = []
    itms = []
    cnt = 0
    for t in alert_logs_hits_time:
        ts.append(t - timer_alert_log_start)
        itms.append(cnt)
        cnt += 1
    fig, ax = plt.plot(ts, itms,'bo')
    fig.set_title("Total Number of Words Flagged over (normalized) Time")
    fig.set_xlabel("Time (sec) normalized from Eval 3 Start")
    fig.set_ylabel("Total Words Flagged")

if __name__ == '__main__':
    main()