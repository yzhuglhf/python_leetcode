"""
Number of Stable Subsequences
Difficulty: Hard

Description:
This problem asks us to count the number of subsequences from a given integer array `nums` that are "stable". A subsequence is stable if it does not contain three consecutive elements with the same parity (odd or even). The final count should be returned modulo 10^9 + 7.

Example:
Input: nums = [1,3,5]
Output: 6
Explanation: Stable subsequences are [1], [3], [5], [1, 3], [1, 5], and [3, 5]. Subsequence [1, 3, 5] is not stable because it contains three consecutive odd numbers.

Approach:
We solve this problem using dynamic programming. We maintain two arrays, `dp[0]` and `dp[1]`, each indexed by parity (0 for even, 1 for odd). `dp[0][p]` stores the total count of stable subsequences ending with an element of parity `p`, where the preceding element (if any) had a different parity, or it's a single-element subsequence (e.g., `[p]`, `[..., (1-p), p]`). `dp[1][p]` stores the total count of stable subsequences ending with an element of parity `p`, where the preceding element also had parity `p` (e.g., `[..., (1-p), p, p]`). For each `num` in `nums`, we calculate the number of *new* stable subsequences that can be formed by ending with `num`. These new counts are derived from previously accumulated `dp` states and then added to the respective `dp` states for `num`'s parity. Specifically, `num` can start a new subsequence (`[num]`), extend any subsequence ending in `(1-p)` to form `..., (1-p), p`, or extend any subsequence ending in `(1-p), p` to form `..., (1-p), p, p`. The final answer is the sum of all values across `dp[0]` and `dp[1]`, taken modulo 10^9 + 7.

Time Complexity: O(N) where N is the length of `nums`.
Space Complexity: O(1) as the DP table size is constant (2x2).
"""
from typing import List

class Solution:
    def countStableSubsequences(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # dp[0][p]: number of stable subsequences ending with an element of parity `p`,
        #           where the second-to-last element (if any) had parity `1-p`, OR it's a single-element subsequence.
        #           (e.g., [p], [..., (1-p), p])
        # dp[1][p]: number of stable subsequences ending with an element of parity `p`,
        #           where the second-to-last element also had parity `p`.
        #           (e.g., [..., (1-p), p, p])
        # Parity `p` can be 0 (even) or 1 (odd).
        dp = [[0, 0], [0, 0]] # dp[state_type][parity]
        
        for num in nums:
            p = num % 2 # Current number's parity
            other_p = 1 - p # The opposite parity
            
            # Calculate current_ending_p_single: number of new stable subsequences ending with `num`
            # that fit the dp[0][p] pattern.
            # These are:
            # 1. The subsequence consisting only of `num` itself: [num] (count = 1)
            # 2. Extending any stable subsequence ending with `other_p` (e.g., [..., (1-p)]) by appending `num`.
            #    This transition `(1-p) -> p` always forms a stable pair, thus contributes to dp[0][p].
            #    Both dp[0][other_p] (e.g., [..., p_prime, (1-p)]) and dp[1][other_p] (e.g., [..., p_prime, p_prime, (1-p)])
            #    can be extended.
            current_ending_p_single = (1 + dp[0][other_p] + dp[1][other_p]) % MOD
            
            # Calculate current_ending_p_double: number of new stable subsequences ending with `num`
            # that fit the dp[1][p] pattern.
            # These are:
            # 1. Extending any stable subsequence ending with `p` AND fitting dp[0][p] pattern
            #    (e.g., [..., (1-p), p]) by appending `num`.
            #    This transition `(1-p), p -> p` forms `(1-p), p, p`, which is stable.
            #    We cannot extend from dp[1][p] (e.g., [..., p_prime, p, p]) because appending `num`
            #    would form `..., p_prime, p, p, p`, which is unstable (three consecutive `p`s).
            current_ending_p_double = dp[0][p] % MOD
            
            # Update the total counts in dp.
            # The counts are cumulative for all subsequences ending at or before the current element.
            dp[0][p] = (dp[0][p] + current_ending_p_single) % MOD
            dp[1][p] = (dp[1][p] + current_ending_p_double) % MOD
            
        # The total number of stable subsequences is the sum of all counts in dp.
        # This includes subsequences ending with even/odd, and with different/same parity patterns.
        total_stable_subsequences = (dp[0][0] + dp[0][1] + dp[1][0] + dp[1][1]) % MOD
        
        return total_stable_subsequences

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [1, 3, 5]
    expected1 = 6
    assert s.countStableSubsequences(nums1) == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {s.countStableSubsequences(nums1)}"
    
    # Example 2
    nums2 = [2, 3, 4, 2]
    expected2 = 14
    assert s.countStableSubsequences(nums2) == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {s.countStableSubsequences(nums2)}"
    
    # Custom test case: Mixed parities
    nums3 = [1, 2, 1, 2, 1]
    expected3 = 30
    assert s.countStableSubsequences(nums3) == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {s.countStableSubsequences(nums3)}"

    # Custom test case: All same parity - should only allow 1-2 length subsequences
    nums4 = [1, 3, 5, 7]
    expected4 = 10
    assert s.countStableSubsequences(nums4) == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {s.countStableSubsequences(nums4)}"

    # Custom test case: Length 1 array
    nums5 = [100]
    expected5 = 1 # [100]
    assert s.countStableSubsequences(nums5) == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {s.countStableSubsequences(nums5)}"

    print("All tests passed!")