"""
Count Good Integers on a Grid Path
Difficulty: Hard

Description:
This problem asks us to count "good" integers within a given range [l, r]. An integer x is considered good if, after being padded to 16 digits and placed onto a 4x4 grid in row-major order, the sequence of 7 digits visited along a path defined by a `directions` string is non-decreasing. The path always starts at (0,0) and moves 3 steps down and 3 steps right, ending at (3,3).

Example:
Input: l = 8, r = 10, directions = "DDDRRR"
Output: 2
Explanation: Numbers 8 and 9 are good. For x=8, the grid path forms [0,0,0,0,0,0,8] (non-decreasing). For x=9, the path is [0,0,0,0,0,0,9] (non-decreasing). For x=10, the path is [0,0,0,0,0,1,0] (not non-decreasing).

Approach:
The problem involves counting numbers within a range that satisfy a digit-based property, which is a classic application of Digit Dynamic Programming. We define a helper function `solve(N)` that counts good integers in the range `[0, N]`. The final answer will be `solve(r) - solve(l - 1)`.
The `solve(N)` function uses a recursive `dp(idx, tight, last_path_digit)` function with memoization.
- `idx`: The current digit position (from 0 to 15) we are placing in the 16-digit string representation of `N`.
- `tight`: A boolean flag indicating if we are currently restricted by the digits of `N`. If true, the current digit can only go up to `N_str[idx]`; otherwise, it can go up to 9.
- `last_path_digit`: The value of the most recent digit encountered on the path sequence that was processed. This is used to enforce the non-decreasing condition. It's initialized to -1, indicating no path digits have been encountered yet.
Before starting the DP, we pre-calculate the 7 grid coordinates (and their corresponding 16-digit string indices) that form the path. Since all path moves ('D' or 'R') strictly increase the grid index `row * 4 + col`, the path digits are always visited in increasing order of their string index. This simplifies the non-decreasing check, as `last_path_digit` always refers to a digit at a *previous* `idx` in the 16-digit string. For each `idx`, we iterate through possible digits, update the `tight` constraint, and if `idx` corresponds to a path point, we check if the `digit` satisfies `digit >= last_path_digit` before making a recursive call. The result is memoized.

Time Complexity: O(K * 2 * 10 * 10) = O(K * max_last_path_digit * max_digit_choices), where K is the number of digits (16). The states are (idx, tight, last_path_digit). `idx` has K+1 values (0 to K). `tight` has 2 values. `last_path_digit` has 11 values (-1 to 9). For each state, we iterate 10 times (digits 0-9). Thus, approximately 17 * 2 * 11 * 10 = 3740 operations, which is very efficient.
Space Complexity: O(K * 2 * 11) = O(K), for the memoization table.
"""
from typing import List, Optional
import functools

class Solution:
    def countGoodIntegersOnPath(self, l: int, r: str, directions: str) -> int:
        
        # 1. Pre-calculate the grid indices for the path
        # The path always starts at (0,0) and consists of 3 'D' and 3 'R' moves.
        # This results in 1 (start) + 6 (moves) = 7 cells visited.
        path_coords = []
        curr_r, curr_c = 0, 0
        path_coords.append((curr_r, curr_c)) # Starting cell (0,0)
        for move in directions:
            if move == 'D':
                curr_r += 1
            elif move == 'R':
                curr_c += 1
            path_coords.append((curr_r, curr_c))
        
        # Convert (row, col) coordinates to their corresponding index in the 16-digit string.
        # For a 4x4 grid in row-major order, cell (r, c) maps to string index r * 4 + c.
        # These are the indices in the 16-digit string whose values form the path sequence.
        target_indices = [r_coord * 4 + c_coord for r_coord, c_coord in path_coords]
        # Using a set for efficient O(1) average time lookup to check if an index is a path point.
        target_indices_set = set(target_indices)

        K = 16 # All numbers are processed as 16-digit strings

        # The core digit DP function: counts good integers in range [0, N]
        def solve(N: int) -> int:
            # Convert N to a 16-digit string, padded with leading zeros if necessary.
            N_str = str(N).zfill(K)

            # @functools.lru_cache automatically handles memoization for recursive functions.
            # State for DP: (idx, tight, last_path_digit)
            # - idx: The current digit position (0-indexed, from 0 to K-1) we are currently filling in the 16-digit number.
            # - tight: A boolean flag. True if we are restricted by the digits of N_str (meaning previous digits matched N_str exactly).
            #          False if we've already placed a digit smaller than N_str[j] at some previous position j, so subsequent digits can be anything from 0-9.
            # - last_path_digit: The value of the most recent digit that was part of the path sequence.
            #                    This is used to enforce the non-decreasing condition.
            #                    Initialized to -1 to indicate that no path digits have been encountered yet.
            @functools.lru_cache(None) # None means no size limit for the cache
            def dp(idx: int, tight: bool, last_path_digit: int) -> int:
                # Base case: If we have successfully filled all K digits, we have found one valid number.
                if idx == K:
                    return 1

                count = 0
                # Determine the upper limit for the current digit.
                # If 'tight' is true, the current digit cannot exceed N_str[idx].
                # Otherwise, it can be any digit from 0 to 9.
                upper_bound = int(N_str[idx]) if tight else 9

                # Iterate through all possible digits for the current position 'idx'.
                for digit in range(upper_bound + 1):
                    # Check if the current digit position 'idx' corresponds to a point on the grid path.
                    current_digit_for_path_check = last_path_digit # Default: no change
                    if idx in target_indices_set:
                        # If this 'idx' is a path point, we need to apply the non-decreasing condition.
                        # `last_path_digit != -1` ensures we only compare after the first path digit has been set.
                        if last_path_digit != -1 and digit < last_path_digit:
                            # If the current digit is smaller than the previous path digit,
                            # this number is not good. Skip this branch and try the next 'digit'.
                            continue
                        # If the condition is met (or it's the first path digit), update `current_digit_for_path_check`.
                        current_digit_for_path_check = digit

                    # Determine the 'new_tight' status for the next recursive call.
                    # 'new_tight' remains true only if we were previously 'tight' AND the current 'digit'
                    # chosen is exactly the 'upper_bound' (i.e., N_str[idx]).
                    new_tight = tight and (digit == upper_bound)
                    
                    # Recursively call dp for the next digit position (idx + 1).
                    count += dp(idx + 1, new_tight, current_digit_for_path_check)
                
                return count

            # Start the DP process: from the first digit (idx=0), initially tight (restricted by N_str),
            # and with no previous path digits recorded (last_path_digit=-1).
            return dp(0, True, -1)

        # The total count of good integers in the range [l, r] is calculated as:
        # (Count of good integers from 0 to r) - (Count of good integers from 0 to l-1).
        # This correctly isolates the count for numbers exactly within the [l, r] range.
        return solve(r) - solve(l - 1)

