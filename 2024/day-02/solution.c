#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/errno.h>


#define LEVELS_DEFAULT_SIZE 5

struct levels_s
{
    long *values;
    size_t size;
    size_t num;
};


// Forward declarations
void parse_levels(long *levels, size_t *num, char *report);
long *levels_change(const long *levels, size_t num, long *changes);
bool all_positive(const long *changes, size_t changes_array_len);
bool all_negative(const long *changes, size_t changes_array_len);
bool safe(const long *changes, size_t changes_array_len);
bool dampened_safe(const long* levels, size_t levels_len);


/**
 * @brief Determine if all values in an array are positive.
 * @param changes Array containing changes in reactor levels.
 * @param changes_array_len Number of changes values in the array.
 * @return True if all numbers are positive.
 */
bool all_positive(const long *changes, const size_t changes_array_len)
{
    for (int i = 0; i < changes_array_len; i++)
        if (changes[i] < 0) return false;

    return true;
}

/**
 * @brief Determine if all values in an array are negative.
 * @param changes Array containing changes in reactor levels.
 * @param changes_array_len Number of changes values in the array.
 * @return True if all numbers are negative.
 */
bool all_negative(const long *changes, const size_t changes_array_len)
{
    for (int i = 0; i < changes_array_len; i++)
        if (changes[i] > 0) return false;

    return true;
}

/**
 * @brief Determine if the changes in reactor levels is safe or not.
 * @param changes Array of changes in reactor levels.
 * @param changes_array_len Number of changes in the array.
 * @return Boolean safety status of the reactor levels changes.
 */
bool safe(const long *changes, const size_t changes_array_len) {
    bool pos = all_positive(changes, changes_array_len);
    bool neg = all_negative(changes, changes_array_len);
    bool in_range = true;

    for (int i = 0; i < changes_array_len; i++) {
        if (labs(changes[i]) < 1 || labs(changes[i]) > 3) {
            return false;
        }
    }

    return (pos || neg) && in_range;
}

/**
 * @brief Determine the safety of the reactor levels, utilizing the problem dampener.
 * @param levels Array of levels values to check for safety.
 * @param levels_len Number of levels in the array.
 * @return Boolean safety status of the levels array.
 */
bool dampened_safe(const long* levels, const size_t levels_len) {
    // Test combinations of levels with one level removed
    // Calculate changes from each levels combination
    // If they pass safe, return true immediately

    size_t target_levels = levels_len - 1;
    size_t combinations_len = target_levels - 1;
    for (int skip = 0; skip < levels_len; skip++) {
        long combination_buffer[target_levels] = {};
        long changes[target_levels - 1] = {};
        int target = 0;
        for (int i = 0; i < levels_len; ++i) {
            if (i == skip) {
                continue;
            }

            combination_buffer[target] = levels[i];
            target++;
        }

        levels_change(combination_buffer, target_levels, changes);
        if (safe(changes, combinations_len)) {
            return true;
        }
    }

    return false;
}


/**
 * @brief Parse a string report containing levels.
 * @param levels Array to populate with levels values.
 * @param num Pointer to a value to populate with the number of levels in the report.
 * @param report String report to be parsed.
 */
void parse_levels(long *levels, size_t *num, char *report) {
    const char *str_value = strtok(report, " ");

    while (str_value != NULL) {
        levels[*num] = strtol(str_value, nullptr, 10);
        (*num)++;
        str_value = strtok(nullptr, " ");
    }
}

/**
 * @brief Calculate the change between levels values.
 * @param levels Array of levels values to calculate changes for.
 * @param num Number of levels in the array.
 * @param changes Pointer to an array to populate with change values.
 * @return Array of change values.
 */
long *levels_change(const long *levels, const size_t num, long *changes) {
    if (levels == NULL ) {
        fprintf(stderr, "ERROR: Null levels list passed to change calculator.\n");
        exit(1);
    }

    for (long i=1; i<num; i++)
        changes[i-1] = levels[i] - levels[i-1];

    return changes;
}

int main(int argc, char **argv) {
    char * line = nullptr;
    size_t line_len;
    long safe_count = 0;
    long dampened_safe_count = 0;

    FILE *input_file = fopen("input", "r");
    if (input_file == NULL) {
        printf("Error opening input file: %d\n", errno);
        return 1;
    }

    while (getline(&line, &line_len, input_file) > 0) {
        long levels[line_len] = {};
        size_t num = 0;

        parse_levels(levels, &num, line);
        long *changes[num - 1] = {};
        levels_change(levels, num, changes);

        if (safe(changes, num - 1)) {
            safe_count++;
        } else {
            // Perform part 2 only for changes arrays that failed the initial check
            if (dampened_safe(levels, num)) {
                dampened_safe_count++;
            }
        }

        num = 0;
    }
    printf("Safe count: %ld\n", safe_count);
    printf("Dampened safe count: %ld\n", safe_count + dampened_safe_count);

    fclose(input_file);
}
