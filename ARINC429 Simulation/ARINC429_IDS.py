from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time
from queue import Queue

class arinc429_intrusion_detection_system:

    all_labels = {
        # Format:
        # Label 1 in octal: [(Equipment ID 1 in Hex, BCD/BNR/DISC),
        #                  (Equipment ID 2 in Hex, BCD/BNR/DISC),
        #                  ... ]
        # Label 2 in octal : ... etc ...
        # 0o0: [ <NOT USED> ],
        0o001: [],
        0o002: [],
        0o003: [],
        0o004: [],
        0o005: [],
        0o006: [],
        0o007: [],
        0o010: [],
        0o011: [],
        0o012: [],
        0o013: [],
        0o014: [],
        0o015: [],
        0o016: [],
        0o017: [],
        0o020: [],
        0o021: [],
        0o022: [],
        0o023: [],
        0o024: [],
        0o025: [],
        0o026: [],
        0o027: [],
        0o030: [],
        0o031: [],
        0o032: [],
        0o033: [],
        0o034: [],
        0o035: [],
        0o036: [],
        0o037: [],
        0o040: [],
        0o041: [],
        0o042: [],
        0o043: [],
        0o044: [],
        0o045: [],
        0o046: [],
        0o047: [],
        0o050: [],
        0o051: [],
        0o052: [],
        0o053: [],
        0o054: [],
        0o055: [],
        0o056: [],
        0o057: [],
        0o060: [],
        0o061: [],
        0o062: [],
        0o063: [],
        0o064: [],
        0o065: [],
        0o066: [],
        0o067: [],
        0o070: [],
        0o071: [],
        0o072: [],
        0o073: [],
        0o074: [],
        0o075: [],
        0o076: [],
        0o077: [],
        0o100: [],
        0o101: [],
        0o102: [],
        0o103: [],
        0o104: [],
        0o105: [],
        0o106: [],
        0o107: [],
        0o110: [],
        0o111: [],
        0o112: [],
        0o113: [],
        0o114: [],
        0o115: [],
        0o116: [],
        0o117: [],
        0o120: [],
        0o121: [],
        0o122: [],
        0o123: [],
        0o124: [],
        0o125: [],
        0o126: [],
        0o127: [],
        0o130: [],
        0o131: [],
        0o132: [],
        0o133: [],
        0o134: [],
        0o135: [],
        0o136: [],
        0o137: [],
        0o140: [],
        0o141: [],
        0o142: [],
        0o143: [],
        0o144: [],
        0o145: [],
        0o146: [],
        0o147: [],
        0o150: [],
        0o151: [],
        0o152: [],
        0o153: [],
        0o154: [],
        0o155: [],
        0o156: [],
        0o157: [],
        0o160: [],
        0o161: [],
        0o162: [],
        0o163: [],
        0o164: [],
        0o165: [],
        0o166: [],
        0o167: [],
        0o170: [],
        0o171: [],
        0o172: [],
        0o173: [],
        0o174: [],
        0o175: [],
        0o176: [],
        0o177: [],
        0o200: [],
        0o201: [],
        0o202: [],
        0o203: [],
        0o204: [],
        0o205: [],
        0o206: [],
        0o207: [],
        0o210: [],
        0o211: [],
        0o212: [],
        0o213: [],
        0o214: [],
        0o215: [],
        0o216: [],
        0o217: [],
        0o220: [],
        0o221: [],
        0o222: [],
        0o223: [],
        0o224: [],
        0o225: [],
        0o226: [],
        0o227: [],
        0o230: [],
        0o231: [],
        0o232: [],
        0o233: [],
        0o234: [],
        0o235: [],
        0o236: [],
        0o237: [],
        0o240: [],
        0o241: [],
        0o242: [],
        0o243: [],
        0o244: [],
        0o245: [],
        0o246: [],
        0o247: [],
        0o250: [],
        0o251: [],
        0o252: [],
        0o253: [],
        0o254: [],
        0o255: [],
        0o256: [],
        0o257: [],
        0o260: [],
        0o261: [],
        0o262: [],
        0o263: [],
        0o264: [],
        0o265: [],
        0o266: [],
        0o267: [],
        0o270: [],
        0o271: [],
        0o272: [],
        0o273: [],
        0o274: [],
        0o275: [],
        0o276: [],
        0o277: [],
        0o300: [],
        0o301: [],
        0o302: [],
        0o303: [],
        0o304: [],
        0o305: [],
        0o306: [],
        0o307: [],
        0o310: [],
        0o311: [],
        0o312: [],
        0o313: [],
        0o314: [],
        0o315: [],
        0o316: [],
        0o317: [],
        0o320: [],
        0o321: [],
        0o322: [],
        0o323: [],
        0o324: [],
        0o325: [],
        0o326: [],
        0o327: [],
        0o330: [],
        0o331: [],
        0o332: [],
        0o333: [],
        0o334: [],
        0o335: [],
        0o336: [],
        0o337: [],
        0o340: [],
        0o341: [],
        0o342: [],
        0o343: [],
        0o344: [],
        0o345: [],
        0o346: [],
        0o347: [],
        0o350: [],
        0o351: [],
        0o352: [],
        0o353: [],
        0o354: [],
        0o355: [],
        0o356: [],
        0o357: [],
        0o360: [],
        0o361: [],
        0o362: [],
        0o363: [],
        0o364: [],
        0o365: [],
        0o366: [],
        0o367: [],
        0o370: [],
        0o371: [],
        0o372: [],
        0o373: [],
        0o374: [],
        0o375: [],
        0o376: []
    }

    equip_ids = {
        # Format:
        # Equipement ID in hex: "Human Readable Name"
        0x0: "Not Used"
    }

    def __init__(self, bus_speed="low", BUS_CHANNELS=[], rules_file = r"C:\Users\mspreston\Desktop\Grad School Work\7 - Summer Semester 2024\Cybersecurity Practicum\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\ARINC429_rules.txt"):
        # Set bus start time
        self.start_time = time()
        # Set bus channels.
        self.BUS_CHANNELS = BUS_CHANNELS
        # set ADIRU T/Rx bus speed
        self.bus_speed = bus_speed

        self.communication_chip = lru_rxr(bus_speed=self.bus_speed,
                                          BUS_CHANNELS=self.BUS_CHANNELS)

        # Output files:
        self.default_filepath = r"C:/ARINC429_IDS/"
        # Input file
        self.rules_file = rules_file
        # Log File location =>
        self.log_filepath = ""
        # Alert File location =>
        self.alert_filepath = ""
        self.get_log_alert_file_path()

        self.channels = {}
        self.get_channel_connections()

        self.sdis = self.get_sdis()

        self.rules = []
        self.get_rules()
        self.n = 1 # number of words.

        #self.rules = self.make_default_rules()

        #self.default_filepath = r"C:/ARINC429_IDS/"
        #self.log_filepath =

        #self.buses = {}
        #self.SDI = {}

    def make_default_rules(self):

        #start_time = time()

        #default_filepath = r"C:/ARINC429_IDS/"
        with open("ARINC429_rules_template.txt","r") as template_fd:
            template_lines = template_fd.readlines()
        template_fd.close()
        with open(self.default_filepath + r"ARINC429_rules_defaults.txt","w") as default_rules_fd:
            default_rules_fd.write(template_lines)
        default_rules_fd.close()

        with open(self.default_filepath + r"Alerts/" + f"Alerts_{self.start_time}.txt", "a") as alerts_fd:
            alerts_fd.write(f"Starting New Alert Message Recording at {self.start_time}\n")
        alerts_fd.close()

        default_rules = {}

        return default_rules

        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            logs_fd.write(f"Starting New Alert Message Recording at {self.start_time}\n")
        logs_fd.close()

    def __str__(self):
        return(str(self.rules))

    def get_log_alert_file_path(self) -> str:
        # Log File location =>
        self.alert_filepath = self.default_filepath + r"Alerts/Logs.txt"
        # Alert File location =>
        self.log_filepath = self.default_filepath + r"Logs/Logs.txt"

        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        files_lines = []
        filines = False
        for line in lines:
            if(line.__contains__("!Outfile")):
                filines = True
            if(filines and line.__contains__("alerts")):
                self.alert_filepath = line.split(" ")[2].replace("\n","")
                #print(line.split(" "))
            if(filines and line.__contains__("logs")):
                self.log_filepath = line.split(" ")[2].replace("\n","")
                #print(line.split(" "))
            if(line.__contains__("!Channels")):
                return
        # else keep defaults:
        return

    def get_channel_connections(self):
        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        #files_lines = []
        filines = False
        for line in lines:
            if(line == "\n"):
                continue
            if(line.__contains__("!SDI")):
                break
                #filines = False
                #return
            if(filines): # and not line.__contains__("!Channels") or not line.__contains__("!SDI")):
                channel = line.split(":")[0].replace(":","")
                #print(line.split(":"))
                tx_to_rx = line.split(":")[1][1:].replace("\n","")
                try:
                    self.channels[channel].append(tx_to_rx)
                except KeyError:
                    self.channels[channel] = [tx_to_rx]
            if(line.__contains__("!Channels")):
                filines = True

    def get_sdis(self)->dict:

        sdis = {}

        lines = []
        with open(self.rules_file, "r") as rules_fd:
            lines = rules_fd.readlines()
        rules_fd.close()

        SDI_flag = False
        for line in lines:
            if(line == "\n"):
                continue
            if(line.__contains__("!Rules")):
                break
            if(SDI_flag):
                # remove endline comments
                line = line.split("#")[0]
                # remove full line comments
                if(line == "" or line == "\n"):
                    continue
                try:
                    channel = line.split(" ")[0].replace(":","")
                    sdi_name = line.split(" ")[1]
                    bitmask = line.split(" ")[3].replace("\n","")
                    sdis[sdi_name+"_"+channel] = bitmask
                except IndexError:
                    raise ValueError("SDI Lines formated incorrectly.")
            if(line.__contains__("!SDI")):
                SDI_flag = True

        return(sdis)

    def get_rules(self):
        with open("ARINC429_rules.txt","r") as rules_fd:
            temp_rules = rules_fd.readlines()
        rules_fd.close()

        rules_section = False
        for line in temp_rules:
            if(line[0] == "#" or line == "\n"):
                continue
            if(rules_section):
                line = line.split("#")[0] # remove endline comments
                self.handle_ruleline(line)
            if(line.__contains__("!Rules")):
                rules_section = True

        # Example formats:
        # <alert/log>* <channel>* <label> <SDI> <data> <SSM> <P> <Time> "<message (if alert)>"
        # <log>* <channel>* <label>/<bits>* -> logs the decoded data for this channel & label.
        # <alert/log>* <channel>* <bit[index1:index2) = "01..10"> "<message (if alert)>"
        # <alert/log>* <channel>* <label> <BCD/BNR/DISC> "<message (if alert)>"

    def handle_ruleline(self,line):
        rule = line.split(" ")

        alert_log = ""
        channel = ""
        bitmask = "0"*31
        parity_check = None
        time_notate = False
        message = ""
        try:
            message = line.split('"')[1]
        except IndexError:
            pass # message is already nothing.

        if(not (rule[0].__contains__("alert") or rule.__contains__("log")) ):
            print(f"Problem with rule: {line}")
            raise ValueError("Rule must delineate between Alerting or Logging.")
        else:
            alert_log = rule[0]

        if(not rule[1] in self.get_channelnames()):
            print(f"Problem with rule: {line}")
            raise ValueError("Rule must delineate between Channels.")
        else:
            channel = rule[1]

        rulez = Queue()
        [rulez.put(rule[i]) for i in range(1,len(rule))]

        octal_flag = True
        SDI_flag = True
        data_flag = True
        SSM_flag = True
        parity_flag = True
        time_flag = True
        #message_flag = True

        while(rulez.qsize() > 0):
            r = rulez.get()
            # octal
            if(r.__contains__("0o") and octal_flag):
                octal_flag = False
                label = int(r,8)
                label_chip = lru_txr()
                l, _ = label_chip.make_label_for_word(label)
                bitmask = self.replace_index(0,8,bitmask,l)
            # SDI
            elif(SDI_flag and r+f"_{channel}" in self.sdis):
                SDI_flag = False

                bitmask = self.replace_index(8,10,bitmask,self.sdis[r])
            # data -> TODO ADD data: to rules semantics
            # TODO make data have no spaces
            elif(data_flag and r.__contains__("bits[") or r.__contains__("data:")):
                data_flag = False
                if(r.__contains__("bits[")):
                    # TODO figure out what to do when this contradicts the label/sdi
                    rz = r.split("=")[1].replace('"','')
                    index1 = int(r.split("[")[1].split(":")[0])
                    index2 = int(r.split(":")[1].split(")")[0])
                    if((index2-1)-index1 != len(rz)):
                        print(f"Expected bitmask of length {(index2-1)-index1}, got {len(rz)}")
                        raise ValueError("Bit String to look for does not match length!")
                    cnt = 0
                    for char in bitmask[index1-1:index2]:
                        try:
                            if(char == "1" and rz[cnt] != char):
                                raise ValueError("Bit mask contradicts other flags!!")
                            cnt += 1
                        except IndexError: # reached past the bit mask.
                            break
                    bitmask = self.replace_index(index1-1,index2-2,bitmask,rz)
                    #bitmask += 19 - len(rz)
                else:
                    if(octal_flag != False): #Need the label
                        # May also need to do this without the equipment ID
                        raise ValueError(f"Label Needed in order to properly search word for given data: {r.split(':')[1]}")
                    # TODO figure out to encode to DISC, BNR or BCD
            elif(SSM_flag):
                try:
                    ssmThere = (int(r,2) >= 0 or int(r,2) <= 4)
                    if(ssmThere):
                        bitmask = self.replace_index(29,31,bitmask,r)
                        SSM_flag = False
                except ValueError:
                    pass
            elif(parity_flag and (r == "C" or r == "I")):
                parity_check = True if r == "C" else False
                parity_flag = False
            elif(time_flag and (r == "time")):
                time_flag = False
                time_notate = True
            #elif(message_flag and r.__contains__('"')):
            #    mess
            else:
                continue

        if(len(bitmask) != 31):
            raise ValueError("Error in parsing word!")

        self.rules.append((alert_log, channel, bitmask, parity_check, time_notate, message))

    def replace_index(self,index1:int,index2:int,ogstring:str,replacestr:str)->str:
        # ogstring[index1:index2] = replacestr
        new_str = ogstring[:index1] + replacestr + ogstring[index2:]
        return(new_str)

    def get_channelnames(self)->list:
        channelnames = []
        for chan, value in self.channels.items():
            channelnames.append(chan)
        return(channelnames)

    def alert_or_log(self, word:str):

        #self.rules.add(
        # 0 (alert_log,
        # 1 channel,
        # 2 bitmask,
        # 3 parity_check,
        # 4 time_notate,
        # 5 message)
        # )
        with open(self.log_filepath, "a") as log_fd:
            with open(self.alert_filepath,"a") as alert_fd:
                for tuple in self.rules:
                    parity = tuple[3]
                    time = tuple[4]
                    flag_this_tuple = False
                    # Part 1 Check if you should flag this word.
                    if(tuple[0].__contains__("alert")):
                        #TODO Check channel?
                        p_bitmask = tuple[2] + lru_txr.calc_parity(tuple[2])
                        bitmask = tuple[2] #+ lru_txr.calc_parity(tuple[2])
                        if(bitmask == 31*"0"):
                            flag_this_tuple = True
                        word_check = word[-1:]
                        if(int(bitmask,2) & int(word_check,2) == int(bitmask,2) ):
                            if( (parity == True and word[-1] == p_bitmask)
                            or (parity == False and word[-1] != p_bitmask) ):
                                # alert
                                flag_this_tuple = True
                            elif(parity == None):
                                # alert
                                flag_this_tuple = True
                    # Part 2: If the word is flagged, the log it appropriately.
                    if(flag_this_tuple and time):
                        if(tuple[0].__contains__("alert")):
                            alert_fd.write(f"{time()}: Alert! {tuple[5]}\n")
                        if(tuple.__contains__("log")):
                            log_fd.write(f"{time()}: {word} {tuple[5]}\n")
                    elif(flag_this_tuple and time == False):
                        if(tuple[0].__contains__("alert")):
                            alert_fd.write(f"Alert! {tuple[5]}\n")
                        if(tuple.__contains__("log")):
                            log_fd.write(f"Logged word #{self.n}: {word} {tuple[5]}\n")
            alert_fd.close()
        log_fd.close()

    def log_all_words(self, channel_index):
        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            word = self.communication_chip.receive_given_word(channel_index)
            logs_fd.write(word)
        logs_fd.close()
        #bus_channel = self.BUS_CHANNELS[channel_index]

