"""
Find Nth Smallest Integer With K One Bits
Difficulty: Hard

Description:
This problem asks for the nth smallest positive integer whose binary representation contains exactly k one bits. The solution leverages binary search on the answer space combined with a digit dynamic programming approach to efficiently count numbers with k one bits up to a given value. The answer is guaranteed to be less than 2^50.

Example:
Input: n = 4, k = 2
Output: 9
Explanation: The 4 smallest positive integers with exactly 2 one bits are 3 (binary 11), 5 (binary 101), 6 (binary 110), and 9 (binary 1001). The 4th among these is 9.

Approach:
The problem is solved by performing a binary search on the possible range of the answer (from 1 up to 2^50). For each candidate number `x` in the binary search, a helper function `count_le(x)` is used to determine how many positive integers less than or equal to `x` have exactly `k` one bits (where `k` is the problem's input `k`). This `count_le` function is implemented using digit dynamic programming (DP). The DP state `dp(idx, current_ones, is_tight)` counts numbers by considering bits from the most significant position (`idx`) downwards, tracking the `current_ones` placed and whether the number being formed is `is_tight` (restricted by `x`'s bits). A precomputed combinations table (Pascal's triangle) is used to optimize DP states where `is_tight` is false, allowing direct calculation of C(remaining_bits, needed_ones). The binary search efficiently narrows down the answer until the `nth` smallest number is found.

Time Complexity: O(log(MAX_VAL) * B * K), where MAX_VAL is 2^50 (the upper bound for the answer), B is the maximum number of bits (approximately 50), and K is the maximum number of one bits (approximately 50). The precomputation of combinations takes O(B^2).
Space Complexity: O(B^2 + B*K), for storing the combinations table and the memoization table in the digit DP. Given B and K are of similar magnitude (up to 50), this simplifies to O(B^2).
"""
from typing import List, Optional

class Solution:
    # Class-level attributes to store precomputed combinations and memoization table.
    # This design ensures these resources are initialized once and shared across calls
    # to nthSmallest on the same Solution object, which is typical for LeetCode test setups.
    _comb = []
    _initialized_comb = False
    _memo = {} # Memoization table for the current `count_le` call
    _s_bin_str = "" # Binary string representation of the current number `num` in `count_le`
    _target_k = 0 # Target k value for the current `count_le` call

    def _init_combinations(self):
        """
        Initializes Pascal's triangle (combinations C(n, k)) up to C(50, 50).
        """
        if self._initialized_comb:
            return
        
        # The maximum number of bits for a number less than 2^50 is 50.
        # So, we need combinations up to C(50, j).
        max_bits = 50 
        self._comb = [[0 for _ in range(max_bits + 1)] for _ in range(max_bits + 1)]
        
        for i in range(max_bits + 1):
            self._comb[i][0] = 1 # C(i, 0) = 1
            for j in range(1, i + 1):
                self._comb[i][j] = self._comb[i-1][j-1] + self._comb[i-1][j]
        
        self._initialized_comb = True

    def nthSmallest(self, n: int, k: int) -> int:
        self._init_combinations()
        
        # Set the target k for the current `nthSmallest` call.
        self._target_k = k

        def count_le(num: int) -> int:
            """
            Counts positive integers y <= num that have exactly self._target_k one bits.
            """
            self._memo.clear() # Clear memoization table for each new `num`
            
            # 0 is not a positive integer. popcount(0) = 0.
            # Since k >= 1, 0 will never satisfy the condition, so no special handling for 0 is strictly needed here.
            if num == 0:
                return 0 
            
            self._s_bin_str = bin(num)[2:] # Binary string representation of `num`
            num_len = len(self._s_bin_str) # Length of the binary string

            def dp(idx: int, current_ones: int, is_tight: bool) -> int:
                """
                Digit DP recursive function.
                idx: current bit position (from left, MSB is idx=0)
                current_ones: number of '1' bits placed so far
                is_tight: True if the current prefix matches the prefix of `self._s_bin_str`,
                          False if it's already strictly smaller.
                """
                # If we have exceeded the target number of ones, this path is invalid.
                if current_ones > self._target_k:
                    return 0
                
                # If not tight, we can place any bit (0 or 1) for the remaining positions.
                # This means we just need to choose `remaining_ones` from `remaining_bits`.
                if not is_tight:
                    remaining_bits = num_len - idx
                    remaining_ones = self._target_k - current_ones
                    
                    # Check for invalid combinations (e.g., negative ones, more ones needed than bits available)
                    if remaining_ones < 0 or remaining_ones > remaining_bits:
                        return 0
                    
                    return self._comb[remaining_bits][remaining_ones]
                
                # Base case: All bits processed. Check if target_k was met.
                if idx == num_len:
                    return 1 if current_ones == self._target_k else 0
                
                # Memoization check
                state = (idx, current_ones, is_tight)
                if state in self._memo:
                    return self._memo[state]
                
                ans = 0
                # The upper bound for the current digit depends on `is_tight`.
                # If `is_tight` is true, the current digit cannot exceed the corresponding digit in `self._s_bin_str`.
                upper_bound_digit = int(self._s_bin_str[idx])
                
                # Iterate through possible digits (0 or 1) for the current position
                for digit in range(upper_bound_digit + 1):
                    new_tight = is_tight and (digit == upper_bound_digit)
                    new_ones = current_ones + (1 if digit == 1 else 0)
                    ans += dp(idx + 1, new_ones, new_tight)
                
                self._memo[state] = ans
                return ans
            
            return dp(0, 0, True)

        # Binary search for the nth smallest number
        low = 1
        # The problem guarantees the answer is strictly less than 2^50.
        # So, the search range is [1, 2^50 - 1]. We set `high` to 2^50 for convenience.
        high = 1 << 50 
        ans = high # Initialize ans to a value that's an upper bound for the actual answer

        while low <= high:
            mid = low + (high - low) // 2
            
            # Calculate how many numbers <= mid have exactly k ones
            count = count_le(mid)
            
            if count >= n:
                # If `count` is greater than or equal to `n`, `mid` could be our answer.
                # Or, the actual `nth` smallest number might be even smaller.
                ans = mid
                high = mid - 1
            else:
                # If `count` is less than `n`, `mid` is too small.
                # We need to look for larger numbers.
                low = mid + 1
        
        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.nthSmallest(n = 4, k = 2) == 9, "Example 1 Failed"
    # Example 2
    assert s.nthSmallest(n = 3, k = 1) == 4, "Example 2 Failed"
    
    # Custom Test Cases
    # Smallest positive integer with 1 one: 1 (binary 1)
    assert s.nthSmallest(n = 1, k = 1) == 1, "Custom Test 1 Failed"
    # Smallest positive integer with 2 ones: 3 (binary 11)
    assert s.nthSmallest(n = 1, k = 2) == 3, "Custom Test 2 Failed"
    # 2nd smallest positive integer with 2 ones: 5 (binary 101)
    assert s.nthSmallest(n = 2, k = 2) == 5, "Custom Test 3 Failed"
    # 50th smallest positive integer with 1 one. This is 2^(50-1) = 2^49.
    assert s.nthSmallest(n = 50, k = 1) == (1 << 49), "Custom Test 4 Failed"
    
    # Smallest positive integer with 50 ones. This is a number consisting of 50 '1' bits.
    # Which is (1 << 50) - 1.
    assert s.nthSmallest(n = 1, k = 50) == (1 << 50) - 1, "Custom Test 5 Failed"

    # A more complex test case: 10th smallest positive integer with 3 one bits.
    # Numbers with 3 ones: 7 (111), 11 (1011), 13 (1101), 14 (1110),
    # 19 (10011), 21 (10101), 22 (10110), 25 (11001), 26 (11010), 28 (11100)
    assert s.nthSmallest(n = 10, k = 3) == 28, "Custom Test 6 Failed"

    print("All tests passed!")

