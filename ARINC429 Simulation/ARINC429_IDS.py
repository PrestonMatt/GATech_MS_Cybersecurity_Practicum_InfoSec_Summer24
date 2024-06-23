from LRU_RX_Helper import arinc429_RX_Helpers as lru_rxr
from BusQueue_Simulator import GlobalBus as ARINC429BUS
from time import sleep, time

class arinv429_intrusion_detection_system:
    def __init__(self, bus_speed="low", BUS_CHANNELS=[]):
        # Set bus start time
        self.bus_start = time()
        # Set bus channels.
        self.BUS_CHANNELS = BUS_CHANNELS
        # set ADIRU T/Rx bus speed
        self.bus_speed = bus_speed

        self.communication_chip = lru_rxr()

        self.rules = {}
        self.make_default_rules()

        self.default_filepath = r"C:/ARINC429_IDS/"

    def make_default_rules(self):

        start_time = time()

        #default_filepath = r"C:/ARINC429_IDS/"
        with open("ARINC429_rules_template.txt","r") as template_fd:
            template_lines = template_fd.readlines()
        template_fd.close()
        with open(self.default_filepath + r"ARINC429_rules_defaults.txt","w") as default_rules_fd:
            default_rules_fd.write(template_lines)
        default_rules_fd.close()

        with open(self.default_filepath + r"Alerts/" + f"Alerts_{start_time}.txt", "a") as alerts_fd:
            alerts_fd.write(f"Starting New Alert Message Recording at {start_time}\n")
        alerts_fd.close()

        with open(self.default_filepath + r"Logs/" + f"Logs_{start_time}.txt", "a") as logs_fd:
            logs_fd.write(f"Starting New Alert Message Recording at {start_time}\n")
        logs_fd.close()

    def __str__(self):
        pass

    def get_rules(self):
        with open("ARINC429_rules.txt","r") as rules_fd:
            temp_rules = rules_fd.readlines()
        rules_fd.close()
        # Parse the rules - lines with # are comments
        # ! indicates a new section
        # i.e. in the form of:
        # !Channels
        # Orange: GPS -> ADIRU
        # Blue: ADIRU -> FMC
        # Purple: FMC -> RMS
        # Purple: FMC -> FAEC 1
        # Purple: FMC -> FAEC 2
        # Purple: FMC -> RWnBS
        # Green: FMC -> RMS
        # Green: FMC -> FAEC 1
        # Green: FMC -> FAEC 2
        # Green: FMC -> RWnBS
        # !Rules
        # <alert/log> <channel> <label> <SDI> <data> <SSM> <P> <message>
        # <alert/log> <channel> <bit[index:index] = "01..10"> <message>
        # <alert/log> <channel> <label> <BCD/BNR/DISC> <message>

    def alert(self):
        pass