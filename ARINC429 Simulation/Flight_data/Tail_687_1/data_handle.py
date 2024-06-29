import os
import scipy.io
import numpy as np

# https://stackoverflow.com/questions/874461/read-mat-files-in-python

#data_type = input("What data do you want to gather?")

keys_to_english = {}

eng_Key_data = {}

types_of_data = set([])

directory = r'C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\Flight_data\Tail_687_1'
files = os.listdir(directory)
for filename in files:
    if(not filename.__contains__(".mat")): # for python / other files.
        continue
    mat = scipy.io.loadmat(os.path.join(directory, filename))
    for key, value in mat.items():
        if(key == "__header__" or
                key == "__version__" or
                key == "__globals__"):
            continue
        #print(key)
        #print(value)
        """
        value = [[ 
            ( 
            array( [ [ <sensor recordings> ] ],  <sensor varType> ), 
            array( [ [ <sampling rate> ] ], <optional rate varType> ), 
            array( [ <units> ], <units varType> )
            array( <parameter description>, <of type string> )
            array( <parameter ID>, <paramID varType> ) 
            )
        ]]
        """
        data = value[0][0][0]
        #print(data)
        english_key = value[0][0][3][0]
        types_of_data.add(english_key) 
        #print(english_key)
        keys_to_english[key] = english_key

        
        try:
            sdata = [] #np.array([])
            for datapoint in data:
                datum = datapoint[0]
                sdata.append(datum)
            #print(sdata)
            eng_Key_data[english_key] = np.concatenate( (eng_Key_data[english_key], np.array(sdata)) )
        except KeyError or ValueError:
            sdata = [] #np.array([])
            for datapoint in data:
                datum = datapoint[0]
                sdata.append(datum) #np.concatenate(sdata, datum)
            eng_Key_data[english_key] = np.array(sdata)
        #except ValueError:
        #    continue
        #except TypeError:
        #    continue
        #break

        #print(value.split(b"array(['")[0].split(b"'")[0])
        #cont = input('')
    #data_sets = mat[]
    #print(data_sets[0])
#print(keys_to_english)

#print(f"All Data Types:\n")
#for d_type in types_of_data:
#    print(f"{d_type}")

# Uncomment to get the text file.
"""
types_of_data = sorted(list(types_of_data))
with open(directory+r'\data_fields.txt', 'w') as dfields_fd:
    for dtype in types_of_data:
        dtype = dtype.lower()
        dtype = dtype.split(" ")
        
        d_type = ""
        for word in dtype:
            d_type += word[0].upper() + word[1:] + " "
        d_type = d_type[:-1] # take out last space.
        # Recapitalize the things that should be capitalized/take out stuff
        d_type = d_type.replace("Lsp","") # Not in the spec sheet.
        # ACMS = Aircraft Condition Monitoring System
        d_type = d_type.replace("Acms","Acms".upper())
        # APU = Aux Power Unit
        d_type = d_type.replace("Apu","Apu".upper())
        # Dude made a typo in his data lol
        d_type = d_type.replace("Avarage","Average")
        # DFGS = Digital Flight Guidance System
        d_type = d_type.replace("Dfgs","Dfgs".upper())
        # May be an abbreviation?
        d_type = d_type.replace("Antice","Anti Ice".upper())
        # FADEC = Full Authority Digital Engine Control -> FAEC
        d_type = d_type.replace("Fadec","Full Authority Engine Control")
        d_type = d_type.replace("L&r","Left and Right")
        d_type = d_type.replace("Gpws","Ground Proximity Warning System")
        # ILS = Instrument Landing System
        d_type = d_type.replace("Ils","ILS")
        d_type = d_type.replace("Tcas","TCAS")
        
        dfields_fd.write(d_type + "\n")
dfields_fd.close()
"""
print("Data Gathering Done!")
for da_type in sorted(list(types_of_data)):
    with open(directory+"\\"+f"{da_type.replace('/','_slash_')}_Tail_687_1_data.txt","w") as x_fd:
        dat = eng_Key_data[da_type]
        for d in dat:
            x_fd.write(str(d))
            x_fd.write("\n")
    x_fd.close()

cont = input('\n\n\nSEE DATA\n\n\n')
print(eng_Key_data)

