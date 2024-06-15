# My classes
from arinc429_voltage_sim import binary_to_voltage as b2v
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
# Python classes
from time import sleep, time


class global_positioning_system():
    # https://www.latlong.net/
    def __init__(self, bus_speed="low", channel=None, lat = "N 42 Deg 21.0'", lon = "W 71 Deg 23.0'"):
        if(not isinstance(channel, ARINC429BUS)):
            raise TypeError("Channel must be ARINC429BUS")
        self.channel = channel
        # set gps tx bus speed
        self.bus_speed = bus_speed
        # zero the bus clock.
        self.usec_start = time()
        self.latitude = lat
        self.longitude = lon

        self.communicator_chip = lru_txr(bus_speed = self.bus_speed,
                                    BUS_CHANNELS = [self.channel])

    def __str__(self):
        current_latitude = f"Current latitude: {self.determine_position()[0]}"
        current_longitude = f"Current longitude: {self.determine_position()[1]}"
        bus_channel = f"Bus Channel: {self.channel} and Speed: {self.bus_speed}"
        GPS_str = current_latitude + "\n" + current_longitude + "\n" + bus_channel
        return(GPS_str)

    # returns latitude and longitude based on position
    def determine_next_position(self) -> (str,str):
        lat_degrees = float(self.latitude.split(" ")[-1].replace("'",""))
        lon_degrees = float(self.longitude.split(" ")[-1].replace("'",""))
        new_lat_degrees = self.round_to_nearest_tenth(lat_degrees + 0.1)
        new_lon_degrees = self.round_to_nearest_tenth(lon_degrees + 0.1)

        lat = self.latitude.split("Deg")[0] + "Deg " + str(new_lat_degrees) + "'"
        lon = self.longitude.split("Deg")[0] + "Deg " + str(new_lon_degrees) + "'"

        self.set_position(lat, lon)
        return(lat, lon)

    def round_to_nearest_tenth(self,ll:float) -> float:
        return(round(ll,1))

    def determine_position(self) -> (str,str):
        return(self.latitude, self.longitude)
    def set_position(self, lat:str, lon:str):
        self.latitude = lat
        self.longitude = lon

    def from_lat_lon_to_word(self) -> (int,int):
        #lat, lon = self.determine_position()

        lat_label, _ = self.communicator_chip.make_label_for_word(int(0o010))
        lat_num = self.latitude.split(" ")[1]
        lat_deg = self.latitude.split(" ")[-1].replace("'","")
        lat_NS = self.latitude.split(" ")[0]
        if(lat_NS == "N"):
            SSM = "00"
        else:
            SSM = "11"
        lat_data = self.from_digits_to_data(lat_num,lat_deg)

        lat_word = lat_label + lat_data + SSM
        lat_word += self.communicator_chip.calc_parity(lat_word)
        # print(len(lat_label))
        # print(len(lat_data))
        # print(len(lat_word))

        lon_label, _ = self.communicator_chip.make_label_for_word(int(0o011))
        lon_num = self.longitude.split(" ")[1]
        lon_deg = self.longitude.split(" ")[-1].replace("'","")
        lon_data = self.from_digits_to_data(lon_num,lon_deg)
        lon_EW = self.longitude.split(" ")[0]
        if(lon_EW == "W"):
            SSM = "11"
        else:
            SSM = "00"

        lon_word = lon_label + lon_data + SSM
        lon_word += self.communicator_chip.calc_parity(lon_word)

        return(int(lat_word,2),int(lon_word,2))

    def from_digits_to_data(self,num:str,deg:str) -> str:
        degree = deg.replace(".","")
        degree = degree[::-1]
        number = num[::-1]

        digit1 = int(degree[0])
        dig1 = bin(digit1)[2:]
        dig1 = "0"*(4-len(dig1)) + dig1
        dig1 = dig1[::-1]

        digit2 = int(degree[1])
        dig2 = bin(digit2)[2:]
        dig2 = "0"*(4-len(dig2)) + dig2
        dig2 = dig2[::-1]

        digit3 = int(degree[2])
        dig3 = bin(digit3)[2:]
        dig3 = "0"*(4-len(dig3) )+ dig3
        dig3 = dig3[::-1]

        digit4 = int(number[0])
        dig4 = bin(digit4)[2:]
        dig4 = "0"*(4-len(dig4)) + dig4
        dig4 = dig4[::-1]

        digit5 = int(number[1])
        dig5 = bin(digit5)[2:]
        dig5 = "0"*(4-len(dig5)) + dig5
        dig5 = dig5[::-1]

        dig6 = "0"
        if(len(num)==3):
            dig6 = "1"

        data = dig1 + dig2 + dig3 + dig4 + dig5 + dig6
        return(data)

    def communicate_to_bus(self):
        # make word based on that
        word1, word2 = self.from_lat_lon_to_word()

        self.communicator_chip.transmit_given_word(word1, self.usec_start, self.channel)
        sleep(1) # wait for it to finish txing
        self.communicator_chip.transmit_given_word(word2, self.usec_start, self.channel)
        self.communicator_chip.visualize_LRU_transmissions(self.channel)
