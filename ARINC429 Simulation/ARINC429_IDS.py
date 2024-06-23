from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time

class arinv429_intrusion_detection_system:
    def __init__(self, bus_speed="low", BUS_CHANNELS=[]):
        # Set bus start time
        self.start_time = time()
        # Set bus channels.
        self.BUS_CHANNELS = BUS_CHANNELS
        # set ADIRU T/Rx bus speed
        self.bus_speed = bus_speed

        self.communication_chip = lru_rxr(bus_speed=self.bus_speed,
                                          BUS_CHANNELS=self.BUS_CHANNELS)

        self.rules = self.make_default_rules()

        self.default_filepath = r"C:/ARINC429_IDS/"

        self.buses = {}
        self.SDI = {}

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

    def get_rules(self):
        with open("ARINC429_rules.txt","r") as rules_fd:
            temp_rules = rules_fd.readlines()
        rules_fd.close()

        lines = []
        for line in temp_rules:
            if(line[0] == "#" or line == "\n"):
                continue
            else:
                line = line.split("#")[0] # remove endline comments
                lines.append(line)

        for cleanLine in lines:
            pass # find rules

    def alert(self):
        pass

    def log_words(self, channel_index):
        with open(self.default_filepath + r"Logs/" + f"Logs_{self.start_time}.txt", "a") as logs_fd:
            word = self.communication_chip.receive_given_word(channel_index)
            logs_fd.write(word)
        logs_fd.close()
        #bus_channel = self.BUS_CHANNELS[channel_index]

