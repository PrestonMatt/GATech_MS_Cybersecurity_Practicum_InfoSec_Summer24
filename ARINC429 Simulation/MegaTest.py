from arinc429_voltage_sim import binary_to_voltage as b2v
import pytest

def main():
    test_voltage_sim()

def test_voltage_sim():
    word_voltage_obj = b2v(True)
    print(str(word_voltage_obj))
    word_voltage_obj.test_all_functions()

if __name__ == "__main__":
    main()