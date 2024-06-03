import threading
from queue import Queue
import time
import random

class GlobalBus:
    def __init__(self, max_size = 100):
        self.voltageQueue = Queue(maxsize = max_size)
        self.lock = threading.Lock()

    def add_voltage(self, voltage):
        with self.lock:
            if(self.voltageQueue.full()):
                # Drop oldest voltage off the wire
                self.voltageQueue.get()
            # add new voltage -> This happens if the queue is full or not.
            self.voltageQueue.put(voltage)

    def get_voltage(self):
        with self.lock:
            try: # further down the queue the RX should get it
                # but not at position 100
                return list(self.voltageQueue.queue)[75]
            except IndexError:
                # the queue is empty so voltage should be with spec 0
                # There may be some noise raising the voltage up/down by half a volt
                return(random.uniform(-0.5, 0.5))

    # TODO This will have to be tested and used later
    # to simulate robustness of the bus
    def simulate_EMI_noise_interference(self, numAffectedVoltages = 5, emi_level = .25):

        if(emi_level < 0.0 or emi_level > 1.0):
            raise ValueError("Emi level must be between 0% (0.0) and 100% (1.0)")

        with self.lock:
            voltages_on_the_bus = list(self.voltageQueue.queue)
            # generate random indeces to affect
            volt_indeces = []
            for i in range(numAffectedVoltages):
                volt_indeces.append(random.randint(0,len(voltages_on_the_bus)-1))
            for vi in volt_indeces:
                voltage_range = (emi_level * voltages_on_the_bus[vi])
                multiplier = [-1,1][random.randrange(2)]
                voltage_change = multiplier * voltage_range
                voltages_on_the_bus[vi] += voltage_change
            for voltage in voltages_on_the_bus:
                self.voltageQueue.put(voltage)
