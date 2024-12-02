#include <stdio.h>
#include <stdlib.h>

#include <sys/errno.h>

// Forward declarations
int compareLong(const void * a, const void * b);
long *resize_list(long *list, size_t *cur_size);
void sort_list(long *num_list, size_t list_len);
long number_freq(const long num, const long *num_list, const size_t list_len);

/**
 * @brief Long integer sort helper function for qsort()
 * @param a Pointer to first long integer
 * @param b Pointer to second long integer
 * @return Integer indicating sort order
 */
int compareLong(const void * a, const void * b) {
    return (*(long*)a - *(long*)b);
}

/**
 * @brief Resize a list of numbers to 2x the current size
 * @param list Pointer to a list of numbers to be resized
 * @param cur_size Pointer to the current size of the list
 * @return Pointer to the resized list
 */
long *resize_list(long *list, size_t *cur_size) {
    *cur_size*=2;
    long *temp_list = realloc(list, sizeof(long) * (*cur_size));
    if (temp_list == NULL) {
        printf("Unable to extend number list.");
        exit(2);
    }

    return temp_list;
}

/**
 * @brief Sort a list of numbers
 * @param num_list Pointer to a list of numbers to sort
 * @param list_len Size of number list
 */
void sort_list(long *num_list, const size_t list_len) {
}

/**
 * @brief Count the frequency of a number in a list of numbers
 * @param num Number to search for
 * @param num_list List of numbers to be searched
 * @param list_len Size of number list
 * @return Frequency of the number in the list
 */
long number_freq(const long num, const long *num_list, const size_t list_len) {
    long total = 0;

    for (size_t i=0; i<list_len; i++) {
        if (num_list[i] == num) {
            total++;
        }
    }

    return total;
}

int main(int argc, char **argv) {
    long *left_list = malloc(sizeof(long) * 100);
    long *right_list = malloc(sizeof(long) * 100);
    size_t left_list_size = 100;   // Size of allocated memory
    size_t right_list_size = 100;  // Size of allocated memory
    size_t left_list_nums = 0;     // Count of numbers in list
    size_t right_list_nums = 0;    // Count of numbers in list
    long left = 0;
    long right = 0;
    long distance = 0;
    long frequency = 0;
    // char *file_buf = malloc(sizeof(char) * 4096);

    FILE *input_file = fopen("input", "r");
    if (input_file == NULL) {
      printf("Error opening input file: %d\n", errno);
        return 1;
    }

    // Read input file
    // Split columns into separate lists
    while (fscanf(input_file, "%ld %ld", &left, &right) == 2) {
        printf("Left :%ld, Right: %ld\n", left, right);

        // Resize lists if necessary
        if (left_list_size < left_list_nums + 1) {
            left_list = resize_list(left_list, &left_list_size);
        }

        if (right_list_size < right_list_nums + 1) {
            right_list = resize_list(right_list, &right_list_size);
        }

        left_list[left_list_nums] = left;
        left_list_nums++;
        right_list[right_list_nums] = right;
        right_list_nums++;
    }

    // Sort the lists
    qsort(left_list, left_list_nums, sizeof(long), compareLong);
    qsort(right_list, right_list_nums, sizeof(long), compareLong);

    // Part 1:
    // Subtract each right element from each left element
    // Sum those results
    for (size_t i = 0; i< left_list_nums; i++) {
        distance += labs(left_list[i] - right_list[i]);
    }
    printf("Distance: %ld\n", distance);

    // Part 2:
    // Count the instances of each left element in right
    // Multiply that left element by the above count
    // Sum those results
    for (size_t i = 0; i< left_list_nums; i++) {
        frequency += left_list[i] * number_freq(left_list[i], right_list, left_list_nums);
    }
    printf("Similarity: %ld\n", frequency);

    fclose(input_file);
    free(left_list);
    free(right_list);
    return 0;
}
