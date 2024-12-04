#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// Forward declarations
void parse_instructions(char *input);
void recover_instructions(const char *input, size_t len);


void parse_instructions(char *input) {
    // Check if ASCII character is 0-9: x > 47 && x < 58
    // Use state variables and a switch statement for each character.
    // The default case should reset the state variables.
}

/**
 * @brief Recover an instruction string to remove segments between "don't()" and "do()" values.
 * @param input Instruction string
 * @param len Length of the instruction string.
 */
void recover_instructions(const char *input, size_t len) {
    char stop[] = "don't()";
    char resume[] = "do()";

    char *start = strstr(input, stop);
    while (start != NULL) {
        char *end = strstr(start, resume);
        if (end == NULL) {
            // There is no resume token after a stop token.
            // Trim everything after stop token and return.
            memset(start, '\0', len - (start - input) - strlen(stop));
            return;
        }

        // Move the remaining contents leftward
        size_t move = len - (end - input) - strlen(resume);
        memmove(start, end + strlen(resume), move);

        // Null the remainder of the array
        size_t clear = len - move - (start - input);
        memset(start + move, '\0', clear);

        // Set up for the next iteration
        start = strstr(input, stop);
    }
}

int main(int argc, char **argv) {
    FILE *input_file = fopen("input", "r");
    if (input_file == NULL) {
        printf("Error opening input file: %d\n", errno);
        return 1;
    }

    if (fseek(input_file, 0, SEEK_END) != 0) {
        fprintf(stderr, "ERROR: Unable to seek to end of input file.\n");
        exit(1);
    }
    long pos = ftell(input_file);
    if (pos == -1) {
        fprintf(stderr, "ERROR: File position returned an invalid value. Errno %d.\n", errno);
        exit(1);
    }
    if (fseek(input_file, 0, SEEK_SET) != 0) {
        fprintf(stderr, "ERROR: Unable to seek to beginning of input file.\n");
        exit(1);
    }

    // Create a dynamic array and guarantee its last value is null for string safety.
    char data_buf[pos + 1] = {};
    fread(data_buf, sizeof(char), pos, input_file);
    data_buf[pos + 1] = '\0';
}
