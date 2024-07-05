import os

from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
from LRU_FMC_Simulator import flight_management_computer as FMC
from LRU_GPS_Simulator import global_positioning_system as GPS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from time import sleep, time
from threading import Thread
def main():

    rules_filename = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL2_RULES_FILES\Eval2_Rules.txt"
    flightdata_filenames = os.getcwd() + r"\Flight_data\Tail_687_1"
    bus_speed = "low"

    Channel1 = ARINC429BUS()
    Channel2 = ARINC429BUS()
    channels = [Channel1, Channel2]

    IDS_test_numX = IDS(bus_speed, BUS_CHANNELS=channels, rules_file=rules_filename)
    transmitting_LRU = ADIRU(bus_speed, BUS_CHANNELS=channels)

    timer_start = time()
    print("Opening and analyzing flight data...")
    # Grab flight data to plug into ADIRU:
    # Remember to take off \n character in these files.
    # Dataset no. 1: Airspeed.
    with open(flightdata_filenames+r"\COMPUTED AIRSPEED LSP_Tail_687_1_data.txt", "r") as airspeed_fd:
        airspeeds = airspeed_fd.readlines()
        #print(airspeeds)
    airspeed_fd.close()
    # Dataset no. 2: Corrected Angle of Attack.
    with open(flightdata_filenames+r"\CORRECTED ANGLE OF ATTACK_Tail_687_1_data.txt", "r") as corrected_aoa_fd:
        corrected_aoas = corrected_aoa_fd.readlines()
        #print(corrected_aoas)
    corrected_aoa_fd.close()
    # Dataset no. 3: Indicated Angle of Attack.
    with open(flightdata_filenames+r"\INDICATED ANGLE OF ATTACK_Tail_687_1_data.txt", "r") as indicated_aoa_fd:
        indicated_aoas = indicated_aoa_fd.readlines()
    indicated_aoa_fd.close()
    # Dataset no. 4: Latitude.
    with open(flightdata_filenames+r"\LATITUDE POSITION LSP_Tail_687_1_data.txt", "r") as latitude_fd:
        lats = latitude_fd.readlines()
    latitude_fd.close()
    # Dataset no. 5: Longitude.
    with open(flightdata_filenames+r"\LATITUDE POSITION LSP_Tail_687_1_data.txt", "r") as longitude_fd:
        lons = longitude_fd.readlines()
    longitude_fd.close()

    #print(len(airspeeds), len(corrected_aoas), len(indicated_aoas), len(lats), len(lons))

    # Length of airspeeds == corrected_aoas == indicated_aoas
    for x in range(len(airspeeds)):
        airspeeds[x] = float(airspeeds[x].replace("\n",""))
        corrected_aoas[x] = float(corrected_aoas[x].replace("\n",""))
        indicated_aoas[x] = float(indicated_aoas[x].replace("\n",""))
    # Length of latitudes == longitudes
    for y in range(len(lats)):
        lats[y] = float(lats[y].replace("\n",""))
        lons[y] = float(lons[y].replace("\n",""))

    timer_end = time()
    print(f"Finished opening and analyzing flight data in {round(timer_end-timer_start,3)} seconds.")

    timer_start = time()
    print("Beginning flight data evaluation 2...")
    # Length of Airspeed, corrected_aoas, and indicated_aoas are 4 times that of length of latitudes and longitudes
    for index in range(len(airspeeds)):
        # Get our data points:
        current_airspeed = airspeeds[index]
        current_corrected_aoa = corrected_aoas[index]
        current_indicated_aoa = indicated_aoas[index]
        # The ADIRU "collects" them:
        transmitting_LRU.set_value('True Airspeed', f"{current_airspeed} knots")
        transmitting_LRU.set_value('Corrected Angle of Attack', f"{current_corrected_aoa} degrees")
        transmitting_LRU.set_value('Indicated Angle of Attack (Average)', f"{current_indicated_aoa} degrees")
        # ADIRU generates words based on those values:
        airspeed_word_bcd = transmitting_LRU.encode_word(0o230) # 0o230: "True Airspeed"
        airspeed_word_bnr = transmitting_LRU.encode_word(0o210) # 0o210: "True Airspeed"
        corrected_aoa_word = transmitting_LRU.encode_word(0o241) # 0o241: "Corrected Angle of Attack"
        indicated_aoa_word = transmitting_LRU.encode_word(0o221) # 0o221: "Indicated Angle of Attack (Average)"
        # For progress visualization:
        print(f"Sending words:\nAirspeed BCD:\t\t\t\t\t0b{airspeed_word_bcd},\nAirspeed BNR:\t\t\t\t\t0b{airspeed_word_bnr},")
        print(f"Corrected Angle of Attack:\t\t0b{corrected_aoa_word},\nIndicated Angle of Attack:\t\t0b{indicated_aoa_word},")
        # See if it alerts/logs correctly:
        IDS_test_numX.alert_or_log(airspeed_word_bcd)
        IDS_test_numX.alert_or_log(airspeed_word_bnr)
        IDS_test_numX.alert_or_log(corrected_aoa_word)
        IDS_test_numX.alert_or_log(indicated_aoa_word)
        # Repeat this for lat and lon, except every 4 words because it tx's 1/4 as much.
        if(index % 4 == 0):
            # Get the Lat/Lon
            current_lat = lats[index]
            current_lon = lons[index]
            # The ADIRU "collects" them
            transmitting_LRU.set_value('Present Position - Latitude', f"{current_lat} degrees")
            transmitting_LRU.set_value('Present Position - Longitude', f"{current_lon} degrees")
            # ADIRU generates words based on those values:
            lat_word_bnr = transmitting_LRU.encode_word(0o310) # 0o310: "Present Position - Latitude"
            lon_word_bnr = transmitting_LRU.encode_word(0o311) # 0o311: "Present Position - Longitude"
            print(f"Latitude BNR:\t\t\t\t\t0b{lat_word_bnr},\nLongitude BNR:\t\t\t\t\t0b{lon_word_bnr}")
            # Redundant:
            """
            # The ADIRU "reformats" them again
            if(current_lat < 0.0):
                lat_str = f"S {round(current_lat,0)} Deg {str(round(current_lat, 3))[3:]}"
            else:
                lat_str = f"N {round(current_lat,0)} Deg {str(round(current_lat, 3))[3:]}"
            if(current_lon < 0.0):
                lon_str = f"W {round(current_lon,0)} Deg {str(round(current_lon, 3))[3:]}"
            else:
                lon_str = f"E {round(current_lon,0)} Deg {str(round(current_lon, 3))[3:]}"
            transmitting_LRU.set_value('Present Position - Latitude', lat_str)
            transmitting_LRU.set_value('Present Position - Longitude', lon_str)
            # ADIRU generates words based on those values:
            lat_word_bcd = transmitting_LRU.encode_word(0o010) # 0o010: "Present Position - Latitude"
            lon_word_bcd = transmitting_LRU.encode_word(0o011) # 0o011: "Present Position - Longitude"
            IDS_test_numX.alert_or_log(lon_word_bcd)
            IDS_test_numX.alert_or_log(lat_word_bcd)
            """
            IDS_test_numX.alert_or_log(lat_word_bnr)
            IDS_test_numX.alert_or_log(lon_word_bnr)
        # Clear some space to better see each word.
        print("\n\n")
    timer_end = time()
    print(f"This concludes Eval 2. It took {round(timer_end-timer_start,3)} seconds.")

if __name__ == '__main__':
    main()