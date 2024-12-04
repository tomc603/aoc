#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// Maximum length of a valid instruction
#define MAX_INSTRUCTION_LEN 8


// State machine states for instruction processor
enum parse_state {
    parser_error = -1,
    parser_none = 0,
    parser_left_digit,
    parser_comma,
    parser_right_digit,
    parser_close_paren,
    parser_complete
};


// Forward declarations
long parse_instructions(const char *input);
void recover_instructions(const char *input, size_t len);


/**
 * @brief Process input data searching for valid instruction sets, returning the sum of the instructions.
 * @param input Data to search for valid instructions.
 * @return Sum of the products from the valid instructions.
 */
long parse_instructions(const char *input) {
    char token[] = "mul(";
    long total = 0;

    char *instruction = strstr(input, token);
    while (instruction != NULL) {
        int parse_len = 0;
        long a = 0;
        long b = 0;
        char left[4] = {0};
        char right[4] = {0};

        int parser_state = parser_none;
        instruction += strlen(token); // Go to the end of the start token
        while (
               instruction != NULL &&
               parse_len < MAX_INSTRUCTION_LEN + 1 &&
               parser_state != parser_error &&
               parser_state != parser_complete)
        {
            int digit_len = 0;

            switch (parser_state) {
                case parser_none:
                    // Parse up to 3 digits and copy them into the left digit buffer
                    while (digit_len < 3 && isdigit(instruction[digit_len]) > 0) {
                        left[digit_len] = instruction[digit_len];
                        digit_len++;
                        parse_len++;
                    }
                    instruction+=digit_len;
                    if (digit_len > 0) {
                        parser_state = parser_left_digit;
                    } else {
                        // Break out of the loop and look for the next instruction token.
                        parser_state = parser_error;
                    }
                    break;
                case parser_left_digit:
                    // Verify the current character is a comma
                    if (instruction[0] == ',') {
                        parser_state = parser_comma;
                        instruction++;
                        parse_len++;
                    } else {
                        // Break out of the loop and look for the next instruction token.
                        parser_state = parser_error;
                    }
                    break;
                case parser_comma:
                    // Parse up to 3 digits and copy them into the right digit buffer
                    while (digit_len < 3 && isdigit(instruction[digit_len]) > 0) {
                        right[digit_len] = instruction[digit_len];
                        digit_len++;
                        parse_len++;
                    }
                    instruction+=digit_len;
                    if (digit_len > 0) {
                        parser_state = parser_right_digit;
                    } else {
                        // Break out of the loop and look for the next instruction token.
                        parser_state = parser_error;
                    }
                    break;
                case parser_right_digit:
                    // Verify the current character is a close parenthesis
                    if (instruction[0] == ')') {
                        parser_state = parser_close_paren;
                        instruction++;
                        parse_len++;
                        break;
                    } else {
                        parser_state = parser_error;
                    }
                    break;
                case parser_close_paren:
                    // We have a full, valid instruction. Multiply left and right values.
                    a = atol(left);
                    b = atol(right);
                    total += a*b;
                    parser_state = parser_complete;
                    break;
                default:
                    // This should be impossible, since we set the state before entering this loop
                    fprintf(stderr, "ERROR: An unexpected error occurred while parsing instructions. Default state reached.\n");
                    parser_state = parser_error;
            }
        }

        // Find the next instruction token
        instruction = strstr(instruction, token);
    }
    return total;
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

    long part1 = parse_instructions(data_buf);
    printf("Part 1 Sum: %ld\n", part1);

    recover_instructions(data_buf, sizeof(data_buf) / sizeof(data_buf[0]));
    long part2 = parse_instructions(data_buf);
    printf("Part 2 Sum: %ld\n", part2);
}
