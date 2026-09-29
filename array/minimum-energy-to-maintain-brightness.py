"""
Minimum Energy to Maintain Brightness
Difficulty: Medium

Description:
This problem asks us to find the minimum total energy required to satisfy a lighting brightness requirement across various time intervals. We are given `n` light bulbs, indexed 0 to n-1. Each bulb, when on, illuminates its own position and its two adjacent positions (if they exist). The total illumination at any time unit is the count of uniquely illuminated positions. For all time units covered by at least one active interval, this total illumination must be at least `brightness`. Each bulb consumes 1 unit of energy for every time unit it is on.

Example:
Input: n = 5, brightness = 5, intervals = [[6,12]]
Output: 14
Explanation: To illuminate 5 unique positions, we need to turn on 2 bulbs. For instance, turning on bulbs at positions 1 and 4 illuminates {0,1,2} and {3,4} respectively, covering all 5 positions {0,1,2,3,4}. The given interval [6,12] has a duration of 7 time units. Thus, the total energy consumed is 2 bulbs * 7 time units = 14.

Approach:
The problem can be decomposed into two independent sub-problems: determining the minimum number of bulbs required to meet the `brightness` target, and calculating the total accumulated duration of all active time intervals.

1.  **Minimum Bulbs (`min_bulbs_needed`)**: A single light bulb placed at an interior position (not 0 or n-1) can illuminate 3 distinct positions (p-1, p, p+1). Bulbs at the edges (0 or n-1) illuminate 2 positions. To maximize overall unique illumination for a given number of bulbs, they should be strategically spaced out to minimize overlap. In an ideal scenario, `k` bulbs can illuminate `3k` unique positions (e.g., by placing them at positions 1, 4, 7, etc., as long as `n` is sufficiently large). Since `brightness <= n` is a constraint, we just need to achieve `brightness` positions. Therefore, to satisfy `brightness` unique illuminated positions, we need at least `ceil(brightness / 3)` bulbs. This can be calculated using integer division as `(brightness + 2) // 3`.

2.  **Total Active Time**: The `intervals` array specifies time ranges during which the brightness requirement must be met. These intervals can overlap. To find the total cumulative duration, we first sort all intervals by their start times. Then, we iterate through the sorted intervals, merging any overlapping intervals into a consolidated list of disjoint intervals. For each interval `[start_i, end_i]` in the merged list, its duration is `end_i - start_i + 1`. The `total_active_time` is the sum of these durations for all merged intervals.

Finally, the minimum total energy required is the product of `min_bulbs_needed` and `total_active_time`.

Time Complexity: O(L log L), where L is the number of intervals (`intervals.length`). This complexity is dominated by the initial sorting of the intervals. The merging process and subsequent summation of interval lengths both take O(L) time.
Space Complexity: O(L) for storing the `merged_intervals` list. In the worst case, if no intervals overlap, this list will contain all L original intervals.
"""
from typing import List, Optional

class Solution:
    def minEnergy(self, n: int, brightness: int, intervals: List[List[int]]) -> int:
        # Step 1: Calculate the minimum number of bulbs required to achieve the target brightness.
        # Each optimally placed bulb can illuminate up to 3 distinct positions.
        # To cover 'brightness' positions, we need ceil(brightness / 3) bulbs.
        # In integer arithmetic, ceil(A/B) is equivalent to (A + B - 1) // B.
        # So, for brightness and 3 positions per bulb, it's (brightness + 3 - 1) // 3 = (brightness + 2) // 3.
        min_bulbs_needed = (brightness + 2) // 3

        # Step 2: Merge overlapping time intervals to find the total unique active time.
        # First, sort the intervals by their start times.
        intervals.sort()

        merged_intervals = []
        for current_start, current_end in intervals:
            # If merged_intervals is empty, or the current interval starts after the last merged interval ends,
            # then there is no overlap, so add the current interval as a new one.
            if not merged_intervals or current_start > merged_intervals[-1][1]:
                merged_intervals.append([current_start, current_end])
            # Otherwise, there is an overlap. Extend the end of the last merged interval
            # to cover the current interval's end.
            else:
                merged_intervals[-1][1] = max(merged_intervals[-1][1], current_end)
        
        # Calculate the total duration of all merged (disjoint) active intervals.
        total_active_time = 0
        for start, end in merged_intervals:
            total_active_time += (end - start + 1)
        
        # Step 3: The minimum total energy is the product of minimum bulbs and total active time.
        return min_bulbs_needed * total_active_time

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 5
    brightness1 = 5
    intervals1 = [[6,12]]
    expected1 = 14
    assert s.minEnergy(n1, brightness1, intervals1) == expected1, f"Test 1 failed: Expected {expected1}, got {s.minEnergy(n1, brightness1, intervals1)}"
    print(f"Test 1 passed. Output: {s.minEnergy(n1, brightness1, intervals1)}")

    # Example 2
    n2 = 2
    brightness2 = 1
    intervals2 = [[0,0],[2,2]]
    expected2 = 2
    assert s.minEnergy(n2, brightness2, intervals2) == expected2, f"Test 2 failed: Expected {expected2}, got {s.minEnergy(n2, brightness2, intervals2)}"
    print(f"Test 2 passed. Output: {s.minEnergy(n2, brightness2, intervals2)}")

    # Example 3
    n3 = 4
    brightness3 = 2
    intervals3 = [[1,3],[2,4]]
    expected3 = 4
    assert s.minEnergy(n3, brightness3, intervals3) == expected3, f"Test 3 failed: Expected {expected3}, got {s.minEnergy(n3, brightness3, intervals3)}"
    print(f"Test 3 passed. Output: {s.minEnergy(n3, brightness3, intervals3)}")

    # Additional Test Case: Multiple non-overlapping intervals
    n4 = 10
    brightness4 = 3
    intervals4 = [[0,1], [5,5], [10,12]]
    # min_bulbs_needed = (3+2)//3 = 1
    # total_active_time = (1-0+1) + (5-5+1) + (12-10+1) = 2 + 1 + 3 = 6
    # Energy = 1 * 6 = 6
    expected4 = 6
    assert s.minEnergy(n4, brightness4, intervals4) == expected4, f"Test 4 failed: Expected {expected4}, got {s.minEnergy(n4, brightness4, intervals4)}"
    print(f"Test 4 passed. Output: {s.minEnergy(n4, brightness4, intervals4)}")

    # Additional Test Case: All intervals overlap
    n5 = 10
    brightness5 = 3
    intervals5 = [[0,10], [1,9], [2,8]]
    # min_bulbs_needed = 1
    # Merged: [[0,10]]
    # total_active_time = (10-0+1) = 11
    # Energy = 1 * 11 = 11
    expected5 = 11
    assert s.minEnergy(n5, brightness5, intervals5) == expected5, f"Test 5 failed: Expected {expected5}, got {s.minEnergy(n5, brightness5, intervals5)}"
    print(f"Test 5 passed. Output: {s.minEnergy(n5, brightness5, intervals5)}")

    # Additional Test Case: Large values
    n6 = 10**6
    brightness6 = 10**6
    intervals6 = [[0, 10**9]]
    # min_bulbs_needed = (10**6 + 2) // 3 = 333334
    # total_active_time = (10**9 - 0 + 1) = 10**9 + 1
    # Energy = 333334 * (10**9 + 1)
    expected6 = 333334 * (10**9 + 1)
    assert s.minEnergy(n6, brightness6, intervals6) == expected6, f"Test 6 failed: Expected {expected6}, got {s.minEnergy(n6, brightness6, intervals6)}"
    print(f"Test 6 passed. Output: {s.minEnergy(n6, brightness6, intervals6)}")

    print("All tests passed!")
```