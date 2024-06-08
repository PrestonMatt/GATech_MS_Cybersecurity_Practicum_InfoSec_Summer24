import threading
from queue import Queue
import time
import random
import matplotlib.pyplot as plt

class GlobalBus:
    def __init__(self, max_size = 100):
        self.voltageQueue = Queue(maxsize = max_size)
        self.lock = threading.Lock()
        self.RX_pointer = 75

    def __str__(self):
        pass

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
                return list(self.voltageQueue.queue)[self.RX_pointer]
            except IndexError:
                # the queue is empty so voltage should be with spec 0
                # There may be some noise raising the voltage up/down by half a volt
                return(random.uniform(-0.5, 0.5))

    def get_all_voltage(self):
        with self.lock:
            return list(self.voltageQueue.queue)

    def queue_visual(self, update_interval = 5e-7, fig_title = "default"):
        # interactive plot
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot([], [], 'go--')

        fig.suptitle(fig_title)

        ax.set_xlim(self.voltageQueue.maxsize)
        ax.set_ylim(-14, 14) # within spec

        # https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
        while(True):
            #print("Updating voltage queue graph")
            voltages = self.get_all_voltage() # for debugging, not simulation
            line.set_xdata(range(len(voltages)))
            line.set_ydata(voltages)

            ax.set_xlim(0, max(len(voltages), 1))

            fig.canvas.draw()
            fig.canvas.flush_events()

            time.sleep(update_interval)

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
