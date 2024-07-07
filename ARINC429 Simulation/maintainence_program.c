#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Function to generate a 32-bit binary word
void generate_word(char *buffer) {
    char buff[32];
    char input[32];
    printf("Enter the word: ");
    gets(input);
    unsigned int word = atoi(input);
    print_bits(word);
}

// send the word over (print to std out)
void print_bits(unsigned int num){
    int bits = sizeof(num) * 8;
    for(int i = bits - 1; i >= 0; i--){
        unsigned int mask = 1 << i;
        printf("%d", (num & mask) ? 1 : 0);
    }
    printf("\n");
}

int main() {
    char buffer[32];  // Buffer to hold a single 32-bit word
    char input[100];  // Vulnerable buffer for user input

    srand(time(NULL)); // Seed the random number generator

    printf("Enter the number of words to generate: ");
    gets(input);  // Unsafe function, vulnerable to buffer overflow

    int num_words = atoi(input);  // Convert user input to integer

    for (int i = 0; i < num_words; i++) {
        generate_word(buffer);
        printf("%s\n", buffer);
    }

    return 0;
}
