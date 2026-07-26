"""
Maximum Value of Concatenated Binary Segments
Difficulty: Hard

Description:
This problem requires arranging a set of binary segments, each defined by a count of '1's followed by a count of '0's, to form a single concatenated binary string with the maximum possible integer value. The result should be returned modulo 10^9 + 7.

Example:
Input: nums1 = [1,2], nums0 = [1,0]
Output: 14
Explanation: Segments are "10" and "11". Sorting them as "11" followed by "10" yields "1110", which has a decimal value of 14.

Approach:
To maximize the value of a concatenated binary string, '1's should be placed as far left as possible and '0's as far right as possible. This implies a greedy approach where segments are sorted based on their "density" of '1's relative to '0's. Specifically, for two segments (n1_a, n0_a) and (n1_b, n0_b), segment 'a' should precede 'b' if `n1_a / n0_a` is effectively greater than `n1_b / n0_b`. To avoid division by zero and floating-point issues, this comparison is handled by cross-multiplication: `n1_a * n0_b > n1_b * n0_a`. After sorting all segments according to this criterion (descending order of `n1/n0`), the maximum value is constructed by iterating through the sorted segments. For each segment (n1, n0), the currently accumulated `total_value` is first shifted left by the current segment's total length (`n1 + n0`) by multiplying `total_value` by `2^(n1+n0)`. Then, the value contributed by the current segment's ones, which is `(2^n1 - 1) * 2^n0`, is added. All intermediate and final calculations are performed modulo 10^9 + 7.

Time Complexity: O(N log N + N log(max_segment_length)), where N is the number of segments and max_segment_length is the maximum length of a single segment (up to 2*10^4). The sorting step, O(N log N), typically dominates.
Space Complexity: O(N) for storing the segments.
"""
import functools
from typing import List, Optional

class Solution:
    def maxValue(self, nums1: List[int], nums0: List[int]) -> int:
        n = len(nums1)
        segments = []
        for i in range(n):
            segments.append((nums1[i], nums0[i]))

        # Sort segments using a custom comparison function.
        # The goal is to place segments with a higher ratio of 1s to 0s earlier.
        # For two segments (n1_a, n0_a) and (n1_b, n0_b),
        # we want (n1_a, n0_a) to come before (n1_b, n0_b) if n1_a/n0_a > n1_b/n0_b.
        # This is equivalent to n1_a * n0_b > n1_b * n0_a (cross-multiplication to avoid division).
        # For functools.cmp_to_key, the comparison function should return:
        #   - a negative value if the first argument comes before the second
        #   - a positive value if the first argument comes after the second
        #   - zero if their order doesn't matter (they are equal for sorting purposes)
        # So, we return (n1_b * n0_a) - (n1_a * n0_b).
        # If n1_a * n0_b > n1_b * n0_a (meaning segment 'a' is "better" and should come first),
        # then (n1_b * n0_a) - (n1_a * n0_b) will be negative, correctly placing 'a' before 'b'.
        segments.sort(key=functools.cmp_to_key(lambda a, b: (b[0] * a[1]) - (a[0] * b[1])))

        MOD = 10**9 + 7
        total_value = 0

        for n1, n0 in segments:
            # Calculate the value of the '1's within the current segment (e.g., "111" has value 7).
            # This is (2^n1 - 1). If n1=0, this is 0, which is correct.
            value_of_current_segment_ones = (pow(2, n1, MOD) - 1) % MOD 
            
            # Shift the previously accumulated total_value to the left.
            # This makes space for the current segment at the most significant positions.
            # The amount of shift is the total length of the current segment (n1 + n0).
            total_value = (total_value * pow(2, n1 + n0, MOD)) % MOD

            # Add the contribution of the current segment's ones.
            # These ones are followed by n0 zeros within their own segment.
            # So, their intrinsic value is effectively shifted left by n0 positions relative to the end of the segment.
            total_value = (total_value + value_of_current_segment_ones * pow(2, n0, MOD)) % MOD

        return total_value

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1_1 = [1,2]
    nums0_1 = [1,0]
    expected_1 = 14
    result_1 = s.maxValue(nums1_1, nums0_1)
    assert result_1 == expected_1, f"Example 1 failed. Expected: {expected_1}, Got: {result_1}"
    print(f"Example 1 passed. Output: {result_1}")

    # Example 2
    nums1_2 = [3,1]
    nums0_2 = [0,3]
    expected_2 = 120
    result_2 = s.maxValue(nums1_2, nums0_2)
    assert result_2 == expected_2, f"Example 2 failed. Expected: {expected_2}, Got: {result_2}"
    print(f"Example 2 passed. Output: {result_2}")

    # Custom Test 1: All ones segments
    nums1_3 = [1,1,1]
    nums0_3 = [0,0,0]
    expected_3 = 7 # "111" value is 7
    result_3 = s.maxValue(nums1_3, nums0_3)
    assert result_3 == expected_3, f"Custom Test 1 failed. Expected: {expected_3}, Got: {result_3}"
    print(f"Custom Test 1 passed. Output: {result_3}")

    # Custom Test 2: All zeros segments
    nums1_4 = [0,0,0]
    nums0_4 = [1,1,1]
    expected_4 = 0 # "000" value is 0
    result_4 = s.maxValue(nums1_4, nums0_4)
    assert result_4 == expected_4, f"Custom Test 2 failed. Expected: {expected_4}, Got: {result_4}"
    print(f"Custom Test 2 passed. Output: {result_4}")

    # Custom Test 3: Mixed segments, order critical
    nums1_5 = [1, 2]
    nums0_5 = [2, 1]
    # Segments: S0=(1,2) -> "100", S1=(2,1) -> "110"
    # n1/n0 for S0: 1/2 = 0.5
    # n1/n0 for S1: 2/1 = 2
    # Sorted order: S1 then S0 => "110" + "100" = "110100"
    # Value: 32 + 16 + 4 = 52
    expected_5 = 52
    result_5 = s.maxValue(nums1_5, nums0_5)
    assert result_5 == expected_5, f"Custom Test 3 failed. Expected: {expected_5}, Got: {result_5}"
    print(f"Custom Test 3 passed. Output: {result_5}")
    
    # Custom Test 4: Larger values, check modulo
    nums1_6 = [10000, 1]
    nums0_6 = [0, 10000]
    # S0=(10000, 0) -> 10000 ones
    # S1=(1, 10000) -> 1 one, 10000 zeros
    # Sorted order: S0 then S1
    # String: "1"*10000 + "1" + "0"*10000
    # Value is (2^10000 - 1) * 2^(1+10000) + (2^1 - 1) * 2^10000
    # Which simplifies to (2^10001 - 1) * 2^10000
    # This is equivalent to 2^(10000+10000) + 2^10000 - 2^10000 - 2^10000. Wait, no.
    # The string is 1...1 (10000 times) followed by 1 (1 time) followed by 0...0 (10000 times)
    # Total ones = 10001. Total zeros = 10000.
    # Value = (2^10001 - 1) * 2^10000
    # Let MOD = 10^9 + 7
    # For (n1,n0) = (10000, 0): total_value = (pow(2, 10000, MOD) - 1) % MOD
    # For (n1,n0) = (1, 10000):
    #   total_value = (total_value * pow(2, 1+10000, MOD)) % MOD
    #   total_value = (total_value + (pow(2,1,MOD)-1)*pow(2,10000,MOD)) % MOD
    # This is ( (pow(2,10000,MOD)-1) * pow(2,10001,MOD) + 1*pow(2,10000,MOD) ) % MOD
    # Which is ( pow(2,20001,MOD) - pow(2,10001,MOD) + pow(2,10000,MOD) ) % MOD
    # This value is `(pow(2, 10001, MOD) - 1) * pow(2, 10000, MOD)`.
    # Let's calculate:
    # pow2_10000 = pow(2, 10000, MOD)
    # pow2_10001 = pow(2, 10001, MOD)
    # val_s0 = (pow2_10000 - 1) % MOD
    # temp_val = (val_s0 * pow2_10001) % MOD
    # val_s1 = (pow(2,1,MOD) - 1) % MOD
    # expected_6 = (temp_val + val_s1 * pow2_10000) % MOD
    # print(f"Precalculated expected_6: {expected_6}") # Precalculated = 527582502

    # A more direct calculation for the final string "1"*10001 + "0"*10000
    # Value = (2^10001 - 1) * 2^10000
    val_2_10001 = pow(2, 10001, MOD)
    val_2_10000 = pow(2, 10000, MOD)
    expected_6 = ((val_2_10001 - 1 + MOD) % MOD * val_2_10000) % MOD
    
    result_6 = s.maxValue(nums1_6, nums0_6)
    assert result_6 == expected_6, f"Custom Test 4 failed. Expected: {expected_6}, Got: {result_6}"
    print(f"Custom Test 4 passed. Output: {result_6}")

    print("All tests passed!")

