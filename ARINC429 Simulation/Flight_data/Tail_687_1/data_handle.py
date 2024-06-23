import os
import scipy.io
import numpy as np

# https://stackoverflow.com/questions/874461/read-mat-files-in-python

data_type = input("What data do you want to gather?")

keys_to_english = {}

eng_Key_data = {}

directory = r'C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\ARINC429 Simulation\Flight_data\Tail_687_1'
files = os.listdir(directory)
for filename in files:
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
        print(data)
        english_key = value[0][0][3][0]
        print(english_key)
        keys_to_english[key] = english_key

        try:
            sdata = np.array([])
            for datapoint in data:
                datum = datapoint[0]
                sdata = np.concatenate(sdata, datum)
            eng_Key_data[english_key] = np.concatenate(eng_Key_data[english_key], sdata)
        except KeyError:
            sdata = np.array([])
            for datapoint in data:
                datum = datapoint[0]
                np.concatenate(sdata, datum)
            eng_Key_data[english_key] = sdata

        #print(value.split(b"array(['")[0].split(b"'")[0])
        #cont = input('')
    #data_sets = mat[]
    #print(data_sets[0])
#print(keys_to_english)

print(eng_Key_data)

