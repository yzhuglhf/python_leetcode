"""
Count Fancy Numbers in a Range
Difficulty: Hard

Description:
The problem asks to count "fancy" numbers within a given range [l, r]. An integer is considered "good" if its digits form a strictly monotone sequence (strictly increasing or strictly decreasing); all single-digit integers are inherently good. An integer is "fancy" if it is good itself, or if the sum of its digits is good. The task is to return the total count of fancy integers in the inclusive range [l, r].

Example:
Input: l = 8, r = 10
Output: 3
Explanation:
- 8 is a single-digit integer, so it's good and thus fancy.
- 9 is a single-digit integer, so it's good and thus fancy.
- 10 has digits [1, 0], which form a strictly decreasing sequence, so 10 is good and thus fancy.
Therefore, the total count is 3.

Approach:
This problem is solved using digit dynamic programming (DP) due to the large range [l, r]. The approach involves calculating `countFancy(r) - countFancy(l - 1)`, where `countFancy(N)` is a helper function that counts all fancy numbers from 1 to `N`. The core of `countFancy(N)` is a recursive digit DP function, `_solve`, which uses memoization (`self.memo`) to store results of subproblems. The state for `_solve` is defined by `(idx, tight, is_leading_zero, prev_digit, monotonicity_state, current_sum)`. `idx` is the current digit position being considered (from left to right). `tight` indicates if the current digit's upper bound is restricted by the corresponding digit of `N`. `is_leading_zero` tracks if all preceding digits placed were zeros. `prev_digit` stores the last non-zero digit placed, essential for checking monotonicity. `monotonicity_state` tracks the sequence's pattern (initial/leading zeros, single digit, strictly increasing, strictly decreasing, or not monotone). `current_sum` accumulates the sum of digits of the number being built. A class-level precomputed array, `_is_good_sum_precomputed`, stores whether sums from 0 to 144 (maximum possible digit sum for a 10^15 number) are "good", optimizing the check for the digit sum condition.

Time Complexity: O(L * D * M * P * S)
- L: Maximum number of digits (approx. 16 for 10^15).
- D: Number of possible digits (0-9, so 10).
- M: Number of monotonicity states (5: -1, 0, 1, 2, 3).
- P: Number of possible previous digits (10: -1 for none, 0-9 for actual digit).
- S: Maximum possible digit sum (145: 0 to 144).
The total number of unique states is roughly 16 * 10 * 5 * 10 * 145 ≈ 1.16 million states. Each state computation involves a loop of at most 10 iterations. Therefore, the total time complexity is approximately O(1.16M * 10) which is in the order of 10^7 operations, making it efficient enough for the given constraints.

Space Complexity: O(L * M * P * S)
The space is dominated by the memoization table, which stores the results for all unique DP states. This is O(16 * 5 * 10 * 145) ≈ O(1.16 million) entries. The `_is_good_sum_precomputed` array contributes O(S) = O(145) space, which is negligible in comparison.
"""
from typing import List, Optional

class Solution:
    # Class-level attribute to store precomputed good sums.
    # This ensures it's computed only once across all test cases.
    _is_good_sum_precomputed: List[bool] = []
    
    def __init__(self):
        # Initialize _is_good_sum_precomputed if it hasn't been done yet.
        # Max sum of digits for 10^15 (a 16-digit number, e.g., 99...9) is 16 * 9 = 144.
        # So we precompute for sums from 0 to 144.
        if not Solution._is_good_sum_precomputed:
            Solution._is_good_sum_precomputed = [self._is_good_num_helper(i) for i in range(145)]
        
        # Instance-specific memoization table and string representation of N.
        # These will be reset for each call to countFancy.
        self.memo = {}
        self.N_str = "" # Placeholder, will be set in countFancy

    def _is_good_num_helper(self, num_int: int) -> bool:
        """
        Helper function to check if a number's digits form a strictly monotone sequence.
        Single-digit numbers are considered good.
        """
        s = str(num_int)
        n = len(s)
        if n <= 1:
            return True # Single digit numbers are always good

        # Check for strictly increasing sequence
        increasing = True
        for i in range(n - 1):
            if s[i] >= s[i+1]:
                increasing = False
                break
        if increasing:
            return True

        # Check for strictly decreasing sequence
        decreasing = True
        for i in range(n - 1):
            if s[i] <= s[i+1]:
                decreasing = False
                break
        return decreasing

    def _solve(self, idx: int, tight: bool, is_leading_zero: bool, prev_digit: int, monotonicity_state: int, current_sum: int) -> int:
        """
        Digit DP function to count fancy numbers up to self.N_str.
        
        Args:
            idx: Current digit position (0 to len(self.N_str) - 1).
            tight: True if we are restricted by the digits of self.N_str, False otherwise.
            is_leading_zero: True if all digits placed so far were 0.
            prev_digit: The last non-zero digit placed, or -1 if no non-zero digit has been placed yet.
            monotonicity_state: Tracks the sequence pattern of non-zero digits:
                - -1: Initial state or only leading zeros placed.
                - 0: Single non-zero digit placed (implicitly good).
                - 1: Strictly increasing sequence (e.g., '123').
                - 2: Strictly decreasing sequence (e.g., '321').
                - 3: Not strictly monotone (e.g., '121', '55').
            current_sum: Sum of digits placed so far.
        
        Returns:
            Number of fancy integers formed from this state.
        """
        
        # Memoization check
        state = (idx, tight, is_leading_zero, prev_digit, monotonicity_state, current_sum)
        if state in self.memo:
            return self.memo[state]

        # Base case: All digits processed
        if idx == len(self.N_str):
            # If `is_leading_zero` is true here, it means the number formed was effectively 0.
            # Since problem constraints state `l >= 1`, we don't count 0.
            if is_leading_zero:
                return 0
            
            # A valid non-zero number has been formed. Check if it's fancy.
            # Condition 1: Check if the number itself is good.
            is_num_good = False
            if monotonicity_state == 0 or monotonicity_state == 1 or monotonicity_state == 2:
                is_num_good = True
            
            # Condition 2: Check if its sum of digits is good.
            # `current_sum` will be at most 144, so it's a valid index for the precomputed list.
            is_sum_good = Solution._is_good_sum_precomputed[current_sum]
            
            if is_num_good or is_sum_good:
                return 1
            else:
                return 0

        ans = 0
        # Determine the upper bound for the current digit.
        # If tight, it's restricted by N_str[idx]; otherwise, it can be 0-9.
        upper_bound = int(self.N_str[idx]) if tight else 9

        for digit in range(upper_bound + 1):
            new_tight = tight and (digit == upper_bound)
            
            if is_leading_zero and digit == 0:
                # If we are still placing leading zeros,
                # prev_digit and monotonicity_state remain in their 'initial' states.
                # current_sum remains 0.
                ans += self._solve(idx + 1, new_tight, True, -1, -1, 0)
            else:
                # This is the first non-zero digit, or a subsequent digit.
                new_monotonicity_state = monotonicity_state
                new_prev_digit = digit # Update prev_digit to the current digit for next step.
                new_sum = current_sum + digit

                if is_leading_zero:
                    # If this is the first non-zero digit, it forms a single-digit number for now (state 0).
                    new_monotonicity_state = 0 
                else:
                    # Otherwise, compare with the previously placed non-zero digit.
                    if monotonicity_state == 0: # Was a single digit number, now becoming multi-digit.
                        if digit > prev_digit:
                            new_monotonicity_state = 1 # Now increasing
                        elif digit < prev_digit:
                            new_monotonicity_state = 2 # Now decreasing
                        else: # digit == prev_digit
                            new_monotonicity_state = 3 # Not strictly monotone (e.g., 55)
                    elif monotonicity_state == 1: # Was increasing. Check if it continues.
                        if digit <= prev_digit: # Current digit breaks increasing pattern.
                            new_monotonicity_state = 3 
                    elif monotonicity_state == 2: # Was decreasing. Check if it continues.
                        if digit >= prev_digit: # Current digit breaks decreasing pattern.
                            new_monotonicity_state = 3 
                    # If monotonicity_state was already 3, it remains 3.
                
                ans += self._solve(idx + 1, new_tight, False, new_prev_digit, new_monotonicity_state, new_sum)

        # Store result in memo and return.
        self.memo[state] = ans
        return ans

    def countFancy(self, l: int, r: int) -> int:
        # Calculate count of fancy numbers up to r.
        self.memo = {} # Clear memo for a fresh calculation for 'r'
        self.N_str = str(r)
        count_r = self._solve(0, True, True, -1, -1, 0)

        # Calculate count of fancy numbers up to l-1.
        self.memo = {} # Clear memo for the next calculation for 'l-1'
        self.N_str = str(l - 1)
        count_l_minus_1 = self._solve(0, True, True, -1, -1, 0)

        return count_r - count_l_minus_1

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.countFancy(8, 10) == 3, f"Test Case 1 Failed: Expected 3, got {s.countFancy(8, 10)}"
    # Example 2
    assert s.countFancy(12340, 12341) == 1, f"Test Case 2 Failed: Expected 1, got {s.countFancy(12340, 12341)}"
    # Example 3
    assert s.countFancy(123456788, 123456788) == 0, f"Test Case 3 Failed: Expected 0, got {s.countFancy(123456788, 123456788)}"
    # Additional test cases
    assert s.countFancy(1, 9) == 9, "Test Case 4 Failed: Expected 9 for 1-9"
    assert s.countFancy(1, 10) == 10, "Test Case 5 Failed: Expected 10 for 1-10"
    assert s.countFancy(1, 20) == 20, "Test Case 6 Failed: Expected 20 for 1-20"
    assert s.countFancy(98, 102) == 5, f"Test Case 8 Failed: Expected 5, got {s.countFancy(98, 102)}"
    print("All tests passed!")

