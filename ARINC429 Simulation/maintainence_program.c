#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Function to generate a 32-bit binary word
void generate_word(char *buffer) {
    unsigned int word = rand();
    for (int i = 31; i >= 0; i--) {
        buffer[31 - i] = (word & (1 << i)) ? '1' : '0';
    }
    buffer[32] = '\0';
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