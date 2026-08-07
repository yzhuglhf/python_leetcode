"""
Aggregate Two Time Series
Difficulty: Medium

Description:
Given two time series, each sorted by strictly increasing timestamp, we need to aggregate them by summing values at common timestamps. If a timestamp is not explicitly present in a series, its value is derived from the next available timestamp in that series; if no next timestamp exists, its value is 0. The output is a new series containing all unique timestamps from both inputs, with their summed values, sorted by timestamp.

Example:
Input: series1 = [[1,3],[4,1]], series2 = [[2,2],[5,2]]
Output: [[1,5],[2,3],[4,3],[5,2]]

Approach:
The core idea is to identify all unique timestamps across both input series, sort them, and then iterate through these sorted timestamps. For each timestamp, we determine its effective value from both series based on the "next available timestamp" rule. We use two pointers, one for each series. When processing a timestamp `ts`, we advance each series' pointer (`p1` for `series1`, `p2` for `series2`) until it points to the first element whose timestamp is greater than or equal to `ts`. If such an element exists for a series, its value is taken; otherwise, the value for that series at `ts` is 0. These two values are then summed and added to the result. This process ensures that `p1` and `p2` only move forward, efficiently determining the 'next available value' for each timestamp.

Time Complexity: O((N + M) log (N + M))
The dominant step is collecting all unique timestamps from both series (O(N + M) for set conversion) and then sorting them (O((N + M) log (N + M))). The subsequent iteration through these unique timestamps involves advancing two pointers, each traversing its respective series at most once, contributing O(N + M) to the time complexity. Therefore, the overall time complexity is determined by the sorting step.

Space Complexity: O(N + M)
We use a set to store unique timestamps and a list to store their sorted version, both of which can contain up to N + M elements. The result list also stores up to N + M elements.
"""
from typing import List, Optional

class Solution:
    def aggregateTimeSeries(self, series1: List[List[int]], series2: List[List[int]]) -> List[List[int]]:
        
        # 1. Collect all unique timestamps from both series
        all_timestamps_set = set()
        for ts, _ in series1:
            all_timestamps_set.add(ts)
        for ts, _ in series2:
            all_timestamps_set.add(ts)
        
        # 2. Sort the unique timestamps to iterate in increasing order
        sorted_timestamps = sorted(list(all_timestamps_set))
        
        # Initialize pointers for both series
        p1 = 0 # Pointer for series1
        p2 = 0 # Pointer for series2
        
        aggregated_series = []
        
        # 3. Iterate through each unique timestamp
        for current_ts in sorted_timestamps:
            val1_at_current_ts = 0
            val2_at_current_ts = 0
            
            # Determine the value from series1 at current_ts
            # Advance p1 until series1[p1][0] is >= current_ts
            # This ensures p1 points to the first element in series1 whose timestamp is >= current_ts
            while p1 < len(series1) and series1[p1][0] < current_ts:
                p1 += 1
            
            # If p1 is within bounds, series1[p1][1] is the "next available value" for current_ts
            if p1 < len(series1):
                val1_at_current_ts = series1[p1][1]
            # Otherwise (p1 is out of bounds), there is no next available timestamp in series1,
            # so val1_at_current_ts remains its initialized value of 0.
                
            # Determine the value from series2 at current_ts
            # Advance p2 until series2[p2][0] is >= current_ts
            while p2 < len(series2) and series2[p2][0] < current_ts:
                p2 += 1
            
            # If p2 is within bounds, series2[p2][1] is the "next available value" for current_ts
            if p2 < len(series2):
                val2_at_current_ts = series2[p2][1]
            # Otherwise (p2 is out of bounds), val2_at_current_ts remains 0.
            
            # Sum the values and add to the aggregated series
            aggregated_series.append([current_ts, val1_at_current_ts + val2_at_current_ts])
            
        return aggregated_series

if __name__ == "__main__":
    s = Solution()

    # Example 1
    series1_1 = [[1,3],[4,1]]
    series2_1 = [[2,2],[5,2]]
    expected_1 = [[1,5],[2,3],[4,3],[5,2]]
    assert s.aggregateTimeSeries(series1_1, series2_1) == expected_1, f"Example 1 failed: {s.aggregateTimeSeries(series1_1, series2_1)}"

    # Example 2
    series1_2 = [[1,5],[3,1]]
    series2_2 = [[2,2]]
    expected_2 = [[1,7],[2,3],[3,1]]
    assert s.aggregateTimeSeries(series1_2, series2_2) == expected_2, f"Example 2 failed: {s.aggregateTimeSeries(series1_2, series2_2)}"

    # Example 3
    series1_3 = [[1,5]]
    series2_3 = [[1000000000,2]]
    expected_3 = [[1,7],[1000000000,2]]
    assert s.aggregateTimeSeries(series1_3, series2_3) == expected_3, f"Example 3 failed: {s.aggregateTimeSeries(series1_3, series2_3)}"

    # Custom Test Case 1: Empty series
    series1_4 = []
    series2_4 = []
    expected_4 = []
    assert s.aggregateTimeSeries(series1_4, series2_4) == expected_4, f"Custom Test 4 (empty series) failed: {s.aggregateTimeSeries(series1_4, series2_4)}"

    # Custom Test Case 2: One empty series
    series1_5 = [[10,100]]
    series2_5 = []
    expected_5 = [[10,100]]
    assert s.aggregateTimeSeries(series1_5, series2_5) == expected_5, f"Custom Test 5 (one empty series) failed: {s.aggregateTimeSeries(series1_5, series2_5)}"

    # Custom Test Case 3: Overlapping timestamps
    series1_6 = [[1,10],[2,20]]
    series2_6 = [[1,5],[2,15]]
    expected_6 = [[1,15],[2,35]]
    assert s.aggregateTimeSeries(series1_6, series2_6) == expected_6, f"Custom Test 6 (overlapping timestamps) failed: {s.aggregateTimeSeries(series1_6, series2_6)}"

    # Custom Test Case 4: Timestamps only in series2, but covered by series1
    series1_7 = [[10,100]]
    series2_7 = [[1,1],[5,5],[15,15]]
    expected_7 = [[1,101],[5,105],[10,115],[15,15]]
    assert s.aggregateTimeSeries(series1_7, series2_7) == expected_7, f"Custom Test 7 (values from next/0) failed: {s.aggregateTimeSeries(series1_7, series2_7)}"
    
    # Custom Test Case 5: Disjoint timestamps
    series1_8 = [[1,10]]
    series2_8 = [[100,20]]
    expected_8 = [[1,30],[100,20]] # At ts=1, series1 has [1,10], series2 has [100,20] (next available). At ts=100, series1 has nothing next (0), series2 has [100,20].
    assert s.aggregateTimeSeries(series1_8, series2_8) == expected_8, f"Custom Test 8 (disjoint timestamps) failed: {s.aggregateTimeSeries(series1_8, series2_8)}"

    print("All tests passed!")
