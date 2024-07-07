import subprocess

def main():
    print('Executing the attack.')
    p = subprocess.Popen(['./mxProgram.exe'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    # Function to read a line from the mxprogram
    def recv():
        return p.stdout.readline()

    # Function to send a line to the mxprogram
    def sendline(line):
        p.stdin.write(line + b'\n')
        p.stdin.flush()

    print('Inputting 100 words.')
    # 'Enter the number of words to generate:'
    #print(recv().strip())  # Read and print the first line from the mxprogram
    sendline(b'100')  # Send '100' words to the mxprogram
    for x in range(100):
        # 'Enter the word:'
        print(recv().strip())  # Read and print the next line
        sendline(bytes(int('01101100110000111100000000000000',2)))  # Send the binary string

    # Close the process's stdin and wait for the process to exit
    p.stdin.close()
    p.wait()

if __name__ == '__main__':
    main()