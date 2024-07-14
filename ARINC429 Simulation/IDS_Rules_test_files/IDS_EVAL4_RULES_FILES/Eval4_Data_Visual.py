import matplotlib.pyplot as plt

with open('eval4_data.csv','r') as eval4_fd:
    data = eval4_fd.readlines()[1:]
eval4_fd.close()

print("There are three variables:")
print("\t - Number of buses (either 36 or 48)")
print("\t - Number of LRUs per bus (2 to 21)")
print("\t - Number of Rules (1 to 500)")

print("You have to choose 2 variables to fix. Input b for buses, l for LRUs and r for rules.")
fixed_vars = input("Pick 2 and only 2:")
if(len(fixed_vars.replace("\n","")) !=2 ):
    raise ValueError("You have to pick 2 variables to fix")

busNum = 0
lruNum = 0
ruleNum = 0

if(fixed_vars.__contains__("b")):
    busNum = input("Input bus number (36 or 48):")
    try:
        busNum = int(busNum.replace("\n",""))
        print(f"Got Entered bus # as {busNum}")
        if(busNum != 36 and busNum != 48):
            raise IndexError("invalid bus number")
    except ValueError:
        raise ValueError("Bus number is not an int.")

if(fixed_vars.__contains__("l")):
    lruNum = input("Input LRUs per bus (2 to 21):")
    try:
        lruNum = int(lruNum.replace("\n",""))
        print(f"Got Entered LRU # as {lruNum}")
        if(lruNum < 2 or lruNum > 21):
            raise IndexError("Invalid LRU number")
    except ValueError:
        raise ValueError("LRU number is not an int.")

if(fixed_vars.__contains__("r")):
    ruleNum = input("Input Rules per bus (1 to 500):")
    try:
        ruleNum = int(ruleNum.replace("\n",""))
        print(f"Got Entered Rule # as {ruleNum}")
        if(ruleNum < 1 or ruleNum > 500):
            raise IndexError("Invalid Rule number")
    except ValueError:
        raise ValueError("Rules number is not an int.")

print(busNum, lruNum, ruleNum)

bus_ = []
lrus_ = []
rules_ = []
setups_ = []
aloneword_ = []

for line in data:
    line = line.replace("\n","")
    line = line.split(',')
    #print(line)
    if(busNum != 0 and lruNum != 0):
        if(float(line[0]) == busNum and float(line[1]) == lruNum):
            #print(line)
            rules_.append(float(line[2]))
            setups_.append(float(line[3]))
            aloneword_.append(float(line[4]))
    if(busNum != 0 and ruleNum != 0):
        if(float(line[0]) == busNum and float(line[2]) == ruleNum):
            lrus_.append(float(line[1]))
            setups_.append(float(line[3]))
            aloneword_.append(float(line[4]))
    if(lruNum != 0 and ruleNum != 0):
        if(float(line[1]) == lruNum and float(line[2]) == ruleNum):
            bus_.append(float(line[0]))
            setups_.append(float(line[3]))
            aloneword_.append(float(line[4]))
#print(setups_,aloneword_)
# graph:
xs = []
y1s = []
y2s = []
if(busNum != 0 and lruNum != 0):
    xs = rules_
    xlabel = "Number of rules"
    figtitle1 = f"IDS Setup Time for fixed {busNum} buses and {lruNum} LRUs."
    figtitle2 = f"IDS Alert/Log Time on one word for fixed {busNum} buses and {lruNum} LRUs."
    figtitle3 = f"Stacked Area Chart of Cumulative IDS time taken for fixed {busNum} buses and {lruNum} LRUs."
if(busNum != 0 and ruleNum != 0):
    xs = lrus_
    xlabel = "Number of LRUs"
    figtitle1 = f"IDS Setup Time for fixed {busNum} buses and {ruleNum} rules."
    figtitle2 = f"IDS Alert/Log Time on one word for fixed {busNum} buses and {ruleNum} rules."
    figtitle3 = f"Stacked Area Chart of Cumulative IDS time taken for fixed {busNum} buses and {ruleNum} rules."
if(lruNum != 0 and ruleNum != 0):
    xs = bus_
    xlabel = "Number of Buses"
    figtitle1 = f"IDS Setup Time for fixed {lruNum} LRUs and {ruleNum} rules."
    figtitle2 = f"IDS Alert/Log Time on one word for fixed {lruNum} LRUs and {ruleNum} rules."
    figtitle3 = f"Stacked Area Chart of Cumulative IDS time taken for fixed {lruNum} LRUs and {ruleNum} rules."
y1s = setups_
y2s = aloneword_

plt.plot(xs, y1s,'go-')
plt.xlabel(xlabel)
plt.ylabel("Setup Time (sec)")
plt.title(figtitle1)
plt.grid(True)
plt.show()

plt.clf()
plt.plot(xs, y2s,'go-')
plt.xlabel(xlabel)
plt.ylabel("Setup Time (sec)")
plt.title(figtitle2)
plt.grid(True)
plt.show()
plt.clf()

plt.stackplot(xs, y1s, y2s, labels=['IDS Setup Time', 'Alert Time on One Word'])
plt.title(figtitle3)
plt.xlabel(xlabel)
plt.ylabel('Time Added by IDS.')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()