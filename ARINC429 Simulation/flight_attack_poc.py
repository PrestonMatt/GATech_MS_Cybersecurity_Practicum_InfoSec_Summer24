import subprocess

def main():
    p = subprocess.Popen(['./mxProgram'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Enter the number of words to generate:
    print(p.recvline().decode('latin1'))
    p.sendline('100')
    for x in range(100):
        # Enter the word:
        print(p.recvline().decode('latin1'))
        # '0110110011000011110000000000000' -> word that shifts plan down.
        p.sendline(int('01101100110000111100000000000000', 2))


if __name__ == '__main__':
    main()