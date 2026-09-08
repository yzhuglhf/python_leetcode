"""
Number of ZigZag Arrays I
Difficulty: Hard

Description:
This problem asks us to count the total number of arrays of a given length `n`, where each element lies within the range `[l, r]`. The arrays must satisfy three specific conditions to be considered "ZigZag": all elements must be within the specified range, no two adjacent elements can be equal, and no three consecutive elements can form a strictly increasing or strictly decreasing sequence. The final count should be returned modulo 10^9 + 7.

Example:
Input: n = 3, l = 1, r = 3
Output: 10
Explanation: There are 10 valid ZigZag arrays of length n = 3 using values in the range [1, 3]. Examples include [1, 2, 1], [1, 3, 2], [2, 1, 3], etc. Each of these arrays demonstrates the alternating increasing/decreasing pattern required by the ZigZag conditions.

Approach:
This problem is efficiently solved using dynamic programming with space optimization. We define two DP states for each array length `i` and each possible last element's value `val`:
1. `dp_inc[v_idx]`: Stores the number of valid ZigZag arrays of length `i` that end with the value `l + v_idx`, where the transition from `arr[i-2]` to `arr[i-1]` (which is `l + v_idx`) was strictly increasing (`arr[i-2] < arr[i-1]`).
2. `dp_dec[v_idx]`: Stores the number of valid ZigZag arrays of length `i` that end with the value `l + v_idx`, where the transition from `arr[i-2]` to `arr[i-1]` was strictly decreasing (`arr[i-2] > arr[i-1]`).

The crucial "ZigZag" condition implies that if the previous step was increasing, the current step must be decreasing, and vice-versa.
To compute `dp_inc[curr_v_idx]` for length `i` (representing `l + curr_v_idx`), we need to sum `dp_dec[prev_v_idx]` for all `prev_v_idx` such that `l + prev_v_idx < l + curr_v_idx`. This means we are counting sequences `... < prev_val > curr_val`.
Similarly, to compute `dp_dec[curr_v_idx]`, we sum `dp_inc[prev_v_idx]` for all `prev_v_idx` such that `l + prev_v_idx > l + curr_v_idx`. This counts sequences `... > prev_val < curr_val`.

These summations are optimized using prefix sums for `dp_dec` (for `prev_v_idx < curr_v_idx`) and suffix sums for `dp_inc` (for `prev_v_idx > curr_v_idx`).

The base case is established for arrays of length `i = 2`. For an array `[prev_val, curr_val]`, `dp_inc[curr_v_idx]` is the count of `prev_val`s less than `curr_val` (which is `curr_val - l`), and `dp_dec[curr_v_idx]` is the count of `prev_val`s greater than `curr_val` (which is `r - curr_val`).

The DP arrays are updated iteratively from length `i = 3` up to `n`. At each step, we calculate the `prefix_sum_dec` and `suffix_sum_inc` from the arrays of length `i-1`, then use these to populate the `next_dp_inc` and `next_dp_dec` arrays for length `i`. Finally, the total number of valid ZigZag arrays of length `n` is the sum of all elements in the final `dp_inc` and `dp_dec` arrays, taken modulo 10^9 + 7.

Time Complexity: O(n * M), where `n` is the array length and `M = r - l + 1` is the size of the value range.
Space Complexity: O(M), for storing the current DP states (`dp_inc`, `dp_dec`) and auxiliary arrays for prefix/suffix sums.
"""
from typing import List, Optional

class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 10**9 + 7
        M = r - l + 1 # Number of possible distinct values (r - l + 1)

        # dp_inc[v_idx]: Stores count of arrays of current length ending with (l + v_idx),
        # where the last step was strictly increasing (arr[k-2] < arr[k-1]).
        # dp_dec[v_idx]: Stores count of arrays of current length ending with (l + v_idx),
        # where the last step was strictly decreasing (arr[k-2] > arr[k-1]).
        
        # Base case for arrays of length 2: [prev_val, curr_val]
        # Any prev_val != curr_val is valid.
        dp_inc = [0] * M
        dp_dec = [0] * M

        for v_idx in range(M):
            curr_val = l + v_idx
            # For an increasing step (prev_val < curr_val):
            # prev_val can be any integer from l to curr_val - 1.
            # There are (curr_val - l) such choices.
            dp_inc[v_idx] = (curr_val - l)

            # For a decreasing step (prev_val > curr_val):
            # prev_val can be any integer from curr_val + 1 to r.
            # There are (r - curr_val) such choices.
            dp_dec[v_idx] = (r - curr_val)

        # Iterate for array lengths from 3 up to n
        for i in range(3, n + 1):
            next_dp_inc = [0] * M # DP states for length `i`
            next_dp_dec = [0] * M

            # Calculate prefix sums for dp_dec and suffix sums for dp_inc
            # These allow O(1) retrieval of sum(dp_dec[j] for j < k) and sum(dp_inc[j] for j > k)
            
            # prefix_sum_dec[k] = sum(dp_dec[j] for j <= k)
            prefix_sum_dec = [0] * M
            current_sum = 0
            for v_idx in range(M):
                current_sum = (current_sum + dp_dec[v_idx]) % MOD
                prefix_sum_dec[v_idx] = current_sum

            # suffix_sum_inc[k] = sum(dp_inc[j] for j >= k)
            suffix_sum_inc = [0] * M
            current_sum = 0
            for v_idx in range(M - 1, -1, -1): # Iterate backwards for suffix sums
                current_sum = (current_sum + dp_inc[v_idx]) % MOD
                suffix_sum_inc[v_idx] = current_sum

            for curr_v_idx in range(M):
                # To form a sequence ending with `... < prev_val > curr_val` (next_dp_inc[curr_v_idx]):
                # The previous array `...prev_val` must have ended with a decreasing step (`dp_dec[prev_v_idx]`).
                # We sum `dp_dec[prev_v_idx]` for all `prev_v_idx` such that `l + prev_v_idx < l + curr_v_idx`.
                # This corresponds to `prev_v_idx < curr_v_idx`.
                if curr_v_idx > 0:
                    next_dp_inc[curr_v_idx] = prefix_sum_dec[curr_v_idx - 1]
                # If curr_v_idx is 0 (value `l`), no `prev_val` can be smaller than `l`.
                else:
                    next_dp_inc[curr_v_idx] = 0

                # To form a sequence ending with `... > prev_val < curr_val` (next_dp_dec[curr_v_idx]):
                # The previous array `...prev_val` must have ended with an increasing step (`dp_inc[prev_v_idx]`).
                # We sum `dp_inc[prev_v_idx]` for all `prev_v_idx` such that `l + prev_v_idx > l + curr_v_idx`.
                # This corresponds to `prev_v_idx > curr_v_idx`.
                if curr_v_idx < M - 1:
                    next_dp_dec[curr_v_idx] = suffix_sum_inc[curr_v_idx + 1]
                # If curr_v_idx is M-1 (value `r`), no `prev_val` can be larger than `r`.
                else:
                    next_dp_dec[curr_v_idx] = 0
            
            # Update the dp arrays for the next iteration (length i+1)
            dp_inc = next_dp_inc
            dp_dec = next_dp_dec

        # After iterating up to length `n`, sum all valid arrays
        total_count = 0
        for v_idx in range(M):
            total_count = (total_count + dp_inc[v_idx] + dp_dec[v_idx]) % MOD
        
        return total_count

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.zigZagArrays(n=3, l=4, r=5) == 2, "Example 1 Failed"
    # Example 2
    assert s.zigZagArrays(n=3, l=1, r=3) == 10, "Example 2 Failed"
    # Custom Test Case 1: M=2, n=4 (Values: [1,2]) -> [1,2,1,2], [2,1,2,1]
    assert s.zigZagArrays(n=4, l=1, r=2) == 2, "Custom Test Case 1 Failed: n=4, l=1, r=2"
    # Custom Test Case 2: M=4, n=3 (Values: [1,2,3,4])
    # Verified by detailed walkthrough: 28
    assert s.zigZagArrays(n=3, l=1, r=4) == 28, "Custom Test Case 2 Failed: n=3, l=1, r=4"
    # Custom Test Case 3: M=4, n=5 (Values: [1,2,3,4])
    # Verified by detailed walkthrough: 140
    assert s.zigZagArrays(n=5, l=1, r=4) == 140, "Custom Test Case 3 Failed: n=5, l=1, r=4"
    # Max N, Min M (n=2000, l=1, r=2). Values are just 1 and 2. Should always be 2.
    assert s.zigZagArrays(n=2000, l=1, r=2) == 2, "Max N, Min M Failed"
    # Max M, Min N (n=3, l=1, r=2000). M = 2000.
    # For n=3, the total count is M * (M-1) * (2*M-1) / 3.
    # For M=2000: 2000 * 1999 * (2*2000 - 1) / 3 = 2000 * 1999 * 3999 / 3 = 2000 * 1999 * 1333 = 5330666000.
    # Result modulo 10^9 + 7: 5330666000 % 1000000007 = 330665965.
    assert s.zigZagArrays(n=3, l=1, r=2000) == 330665965, "Max M, Min N Failed"

    print("All tests passed!")

