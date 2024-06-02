from arinc429_voltage_sim import binary_to_voltage as b2v
from LRU_FMC_Simulator import flight_management_computer as FMC
import pytest

def main():
    test_voltage_sim()

def test_voltage_sim():
    word_voltage_obj = b2v(True)
    print(str(word_voltage_obj))
    word_voltage_obj.test_all_functions()

def test_FMC_send_random_voltages():
    FMC_test1 = FMC("HiGh")
    FMC_test1.transmit_random_voltages()

def test_FMC_send_given_word():
    FMC_test2 = FMC("lOW")
    given_word = 0b11111101000000000000001000110000
    FMC_test2.transmit_given_word(given_word)

if __name__ == "__main__":
    main()