import os

import numpy as np
import string

from ARINC429_IDS import arinc429_intrusion_detection_system as IDS
from LRU_ADIRU_Simulator import air_data_inertial_reference_unit as ADIRU
from LRU_FMC_Simulator import flight_management_computer as FMC
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time, ctime
from datetime import datetime
from random import randint, choice


reference_IDS = IDS("low",[ARINC429BUS(),ARINC429BUS()])
equip_ids = reference_IDS.equip_ids
labels = reference_IDS.all_labels
SALs = reference_IDS.SALs

def create_rules_files(channel_number:int, LRU_number:int, rules_number:int):
    file_write = "!Outfiles\n"
    file_write += "alerts = \"<placeholder>\"\n"
    file_write += "logs = \"<placeholder>\"\n"
    file_write += "\n"

    channel_section = "!Channels\n"
    sdi_section = "!SDI\n"

    keys = []
    values = []
    for key, value in equip_ids.items():
        keys.append(key)
        values.append(value)

    connections_per_channel = LRU_number - 1

    all_lrus = set([])
    for c in range(channel_number):
        channel_conns = set([])
        channel_sdis = set([])

        lru_txr_ = choice(values).replace(" ","_")
        lru_txr_ = lru_txr_.replace("#","num")
        channel_begin_line = f'Channel{c+1}: {lru_txr_} -> '
        channel_sdis.add(f'Channel{c+1}: {lru_txr_} -> 00\n')
        sdi_r = 0b01

        all_lrus.add((lru_txr_,f'Channel{c+1}'))

        while(len(list(channel_conns)) < connections_per_channel): # For this eval we don't want repeat connections.
            lru_rxr_ = choice(values).replace(" ","_")
            lru_rxr_ = lru_rxr_.replace("#","num")
            while(lru_rxr_ == lru_txr_):
                lru_rxr_ = choice(values).replace(" ","_")
                lru_rxr_ = lru_rxr_.replace("#","num")
            channel_conns.add(channel_begin_line + f'{lru_rxr_}\n')
            #print(channel_begin_line + f'{lru_rxr_}\n')
            sdi_num = "0" * (2 - len(bin(sdi_r)[2:])) + bin(sdi_r)[2:]
            channel_sdis.add(f'Channel{c+1}: {lru_rxr_} -> {sdi_num}\n')

            all_lrus.add((lru_rxr_,f'Channel{c+1}'))

            sdi_r += 1
            if(sdi_r >= 0b100):
                sdi_r = 0b00

        channel_conns = list(channel_conns)
        for c_conn in channel_conns:
            channel_section += c_conn
        channel_section += '\n'
        sdis = list(channel_sdis)
        for sdi_line in sdis:
            sdi_section += sdi_line
        sdi_section += '\n'

    file_write += channel_section
    file_write += sdi_section

    lrus = list(all_lrus)

    file_write += "!Rules\n"

    for r in range(rules_number):
        lru, channel = choice(lrus)
        # Alert, log or both:
        rule = choice(["alert", "log", "alert/log"])
        rule += " "
        # Channel was already chosen for us:
        rule += channel
        # From here there should be a 1/100 chance of ending the rule here since that is valid
        if(choice([x for x in range(1,100)]) == 50):
            file_write += rule + '\n'
            continue
        rule += " "
        # Choose the label from the labels
        applicable_labels = []
        for label, sub_dict in labels.items():
            #print(sub_dict)
            for equip_id, encoding_type in sub_dict.items():
                try:
                    test_lru = equip_ids[equip_id].replace(" ","_")
                    test_lru = test_lru.replace("#","num")
                except KeyError:
                    continue
                #print(equip_id)
                if(test_lru != lru):
                    continue
                else:
                    applicable_labels.append( (label, encoding_type) )
        # Get a random label and how it's encoded from this:
        label_, encoding_info = choice(applicable_labels)
        label_ = oct(label_)
        # Add the label
        rule += label_
        rule += " "
        # From here there should be a 1/100 chance of ending the rule here since that is valid
        if(choice([x for x in range(1,101)]) == 50):
            file_write += rule + '\n'
            continue
        # Need to add the equip ID
        rule += lru
        rule += " "
        # For SSM later:
        SSM = [" ", "00 "]
        # Four options here:
        encoding_type = encoding_info[0]
        # 1 in 10 chance to just not check the data at all
        if(choice([x for x in range(10)]) == 9):
            pass
        else:
            chance = choice([1,2,3])
            if(chance == 1):
                rule += f"Encoding:{encoding_type}"
            elif(chance == 2):
                if(encoding_type == "BNR"):
                    bnr_res = encoding_info[1]
                    bnr_range = encoding_info[2]
                    #bnr_sig_digs = encoding_info[3]
                    if(bnr_range[0] - bnr_range[1] == 0.0): # DEAD VALUE
                        datum = 0.0
                    else:
                        try:
                            possible_values = np.arange(start=bnr_range[0],
                                                        stop=bnr_range[1],
                                                        step=bnr_res)
                            datum = choice(possible_values)
                        except ValueError:
                            #print(bnr_range,bnr_res)
                            step_ = abs(bnr_range[0] - bnr_range[1]) / 10.0
                            possible_values = np.arange(start=bnr_range[0],
                                                        stop=bnr_range[1],
                                                        step=step_ )
                            #input(f"{bnr_range,step_,possible_values}")
                            datum = choice(possible_values)
                        if(datum < 0.0):
                            SSM = [" ", " ", "11 "]
                        else:
                            SSM = [" ", " ", "00 "]
                        rule += f"data:{round(datum,5)}"
                elif(encoding_type == "BCD"):
                    bcd_res = encoding_info[1]
                    bcd_range = encoding_info[2]
                    try:
                        possible_values = np.arange(start=bcd_range[0],
                                                    stop=bcd_range[1],
                                                    step=bcd_res)
                        datum = choice(possible_values)
                        if(datum < 0.0):
                            SSM = [" ", " ", "11 "]
                        else:
                            SSM = [" ", " ", "00 "]
                        rule += f"data:{round(datum,3)}"
                    except ValueError:
                        input(f"BCD Value Error: {label_, encoding_info}")
                    except IndexError: # Dead value
                        #input(f"BCD Index Error: {label_, encoding_info}")
                        rule += f"data:0.0"
                    except TypeError: # This was a bug in the IDS
                        input(f"BCD Type Error: {label_, encoding_info}")
                    except ZeroDivisionError: # Dead value
                        rule += f"data:0.0"
                elif(encoding_type == "DISC"):
                    bits = ""
                    #init_bits = bin(randint(0,2 ** len('0000111100001111000')))[2:]
                    #bits = "0" * (19 - len(init_bits)) + init_bits
                    for x in range(19):
                        bits += choice(["0","1"])
                    rule += f"data:{bits}"
                    SSM = [" "]
                elif(encoding_type == "SAL"):
                    sals = []
                    for name, sal in SALs.items():
                        sals.append(sal)
                    rule += f"data:{oct(choice(sals))}"
                    SSM = [" "]
            else:
                start = randint(11,25)
                stop = randint(start+2, 27)
                while(stop <= start):
                    stop = randint(start, 27)
                bits = ""
                for x in range(start,stop-1):
                    bits += choice(["0","1"])
                #a = 0
                #b = 2 ** (stop - start - 1)
                #initial_bits = bin(randint(a, b))[2:]
                #bits = "0" * ((stop - start) - len(initial_bits) - 1) + initial_bits
                rule += f"bits[{start}:{stop})={bits}"
                SSM = [" "]
            rule += " "
        # SSM
        rule += choice(SSM)
        #rule += " "
        # Parity bit -> 1/3 chance of not checking, 1/3 chance of C and 1/3 chance of I
        rule += choice(["", "C", "I"])
        rule += " "
        # Time -> 50/50 record time vs not
        rule += choice(["", "time",])
        rule += " "
        # Message:
        if(rule.__contains__("alert")):
            rule += randomword(randint(0,100))
        else:
            rule += choice(["", randomword(randint(0,100))])

        for x in range(2,5):
            rule = rule.replace(x*" ", " ")
        file_write += rule + '\n'

    #print(file_write)
    with open(os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\Eval4_Rules.txt", "w") as thisrulesFile_fd:
        thisrulesFile_fd.write(file_write)
    thisrulesFile_fd.close()

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))

def _test_ids_metrics(channel_number:int, LRU_number:int, rules_number:int):
    # Test setup:
    start_time = time()
    IDS_test = IDS(bus_speed="low",
                   BUS_CHANNELS=[ARINC429BUS(),ARINC429BUS()],
                   rules_file=os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\Eval4_Rules.txt")
    end_time = time()
    IDS_test.alert_filepath = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\Alerts_Logs\Alerts_EVAL4.txt"
    IDS_test.log_filepath = os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\Alerts_Logs\Logs_EVAL4.txt"
    setup_time = end_time - start_time

    start_time = time()
    IDS_test.alert_or_log("01"*16)
    end_time = time()

    alert_log_time = end_time - start_time

    with open(os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\eval4_data.csv","a") as eval4data_fd:
        eval4data_fd.write(f"{channel_number},{LRU_number},{rules_number},{setup_time},{alert_log_time}\n")
    eval4data_fd.close()

def main():

    with open(os.getcwd() + r"\IDS_Rules_test_files\IDS_EVAL4_RULES_FILES\eval4_data.csv","w") as eval4data_fd:
        eval4data_fd.write("# of Channels,# of LRUs,# of Rules,Setup Time (seconds),Alert/Log Time on 1 word (seconds)\n")
    eval4data_fd.close()

    cnt = 1
    for arinc_channels in range(2):
        if(arinc_channels == 0):
            channels = 36
        else:
            channels = 48

        for numLRUs in range(2, 21):
            for numRules in range(1, 500):
                create_rules_files(channels, numLRUs, numRules)
                _test_ids_metrics(channels, numLRUs, numRules)
                print(f"Test #{cnt} of 189962 Done.")
                cnt += 1

if __name__ == '__main__':
    main()