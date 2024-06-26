from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from LRU_TX_Helper import arinc429_TX_Helpers as lru_txr
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time
from queue import Queue

class arinc429_intrusion_detection_system:
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

        self.rules = None



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
                print(line.split(" "))
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
        parity_check = False
        time_notate = False
        message = line.split('"')[1]

        if(not (rule[0].__contains__("alert") or rule.__contains__("log")) ):
            raise ValueError("Rule must delineate between Alerting or Logging.")
        else:
            alert_log = rule[0]

        if(not rule[1] in self.get_channelnames()):
            raise ValueError("Rule must delineate between Channels.")
        else:
            channel = rule[1]

        rulez = Queue()
        [rulez.put(word) for word in rule]

        octal_flag = True
        SDI_flag = True
        data_flag = True
        SSM_flag = True
        parity_flag = True
        time_flag = True
        message_flag = True

        while(rulez.size() > 0):
            r = rulez.pop()
            # octal
            if(r.__contains__("0o") and octal_flag):
                octal_flag = False
                label = int(r,8)
                bitmask[0:8] = lru_txr.make_label_for_word(label)
            # SDI
            elif(SDI_flag and r+f"_{channel}" in self.sdis):
                SDI_flag = False
                bitmask[8:10] = self.sdis[r]
            # data -> TODO ADD data: to rules semantics
            # TODO make data have no spaces
            elif(data_flag and r.__contains__("bit[") or r.__contains__("data:")):
                data_flag = False
                if(r.__contains__("bit[")):
                    # TODO figure out what to do when this contradicts the label/sdi
                    rz = r.split("=")[1].replace('"','')
                    index1 = int(r.split("[")[0].split(":")[0])
                    index2 = int(r.split(":")[1].split(")")[0])
                    cnt = 0
                    for char in bitmask[index1:index2]:
                        try:
                            if(rz[cnt] != char):
                                raise ValueError("Bit mask contradicts other flags!!")
                        except IndexError: # reached past the bit mask.
                            break
                    bitmask[index1:index2] = rz
                    #bitmask += 19 - len(rz)
                else:
                    # TODO figure out to encode to DISC, BNR or BCD
                    pass
            elif(SSM_flag and (int(data_flag,2) >= 0 or int(data_flag,2) <= 4)):
                bitmask[29:31] = data_flag
                SSM_flag = False
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

        self.rules.add((alert_log,channel,bitmask,parity_check,time_notate,message))

    def get_channelnames(self)->list:
        channelnames = []
        for chan, value in self.channels.items():
            channelnames.append(chan)
        return(channelnames)

    def alert(self):
        pass

    def log_words(self, channel_index):
        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            word = self.communication_chip.receive_given_word(channel_index)
            logs_fd.write(word)
        logs_fd.close()
        #bus_channel = self.BUS_CHANNELS[channel_index]

