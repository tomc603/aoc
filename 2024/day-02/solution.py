#!/usr/bin/env python3

import itertools


def safe(report: list):
    # Calculate the differences between adjacent levels values
    # Check all levels values differences are positive or all levels values are negative
    # Check levels values are between 1 and 3 difference from their adjacent levels value
    level_change = [b - a for a, b in itertools.pairwise(report)]
    return (
            (all([l > 0 for l in level_change]) or all([l < 0 for l in level_change]))
            and
            (all([1 <= abs(l) <= 3 for l in level_change]))
    )

def dampened_safe(report: list):
    # If the report is safe in the strict regime, short circuit and return immediately
    if safe(report): return True

    # Otherwise, check if any combination of levels is safe after removing a single levels value
    return any([safe(levels) for levels in itertools.combinations(report, len(report) - 1)])


reports = [[int(y) for y in x.split()] for x in open("input", "r").readlines()]
safe_reports = sum([safe(report) for report in reports])
print(f"Safe reports: {safe_reports}")

dampened_reports = sum([dampened_safe(report) for report in reports])
print(f"Dampened safe reports: {dampened_reports}")
