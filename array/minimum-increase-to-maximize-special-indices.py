"""
Minimum Increase to Maximize Special Indices
Difficulty: Medium

Description:
This problem asks us to maximize the number of "special" indices in an array, where a special index `i` satisfies `nums[i] > nums[i-1]` and `nums[i] > nums[i+1]`. If multiple ways achieve the maximum number of special indices, we must choose the one that requires the minimum total number of operations (increasing `nums[i]` by 1). Indices 0 and n-1 cannot be special.

Example:
Input: nums = [5,2,1,4,3]
Output: 4
Explanation:
The goal is to achieve the maximum number of special indices (which is 2 in this case, by making indices 1 and 3 special, as adjacent indices cannot both be special) with minimum total operations.
1. To make index 1 special: `nums[1]` needs to be `max(nums[0], nums[2]) + 1 = max(5,1) + 1 = 6`. This requires `6 - 2 = 4` operations. The array becomes `[5,6,1,4,3]`.
2. To make index 3 special: `nums[3]` needs to be `max(nums[2], nums[4]) + 1 = max(1,3) + 1 = 4`. This requires `4 - 4 = 0` operations (since `nums[3]` is already 4). The array remains `[5,6,1,4,3]`.
With indices 1 and 3 special, we achieve 2 special indices with a total cost of 4. This is the maximum achievable number of special indices, and 4 is the minimum cost for it.

Approach:
The problem can be modeled as selecting non-adjacent elements (potential special indices) from the range `1` to `n-2` such that a combined objective function (maximize special index count, then minimize total operations) is optimized. This is a classic dynamic programming problem. We define `dp[i]` as a tuple `(max_special_indices, min_operations)` representing the optimal solution for the suffix of the array starting from index `i` up to `n-1`. Since an index `i` being special depends on `nums[i-1]` and `nums[i+1]`, and making `i` special prevents `i-1` and `i+1` from being special, we iterate backwards from `n-2` down to `1`. For each index `i`, we have two choices:
1. Do not make `i` special: In this case, the result for `dp[i]` is simply `dp[i+1]` (the optimal result from the next index onwards).
2. Make `i` special: First, calculate the cost `C_i` to make `nums[i]` strictly greater than both `nums[i-1]` and `nums[i+1]`. The minimum `nums[i]` needs to be is `max(nums[i-1], nums[i+1]) + 1`. The cost is `max(0, (max(nums[i-1], nums[i+1]) + 1) - nums[i])`. If `i` is made special, then `i+1` cannot be special. Thus, we add 1 to the special count and `C_i` to the total operations, and combine this with the optimal result from `dp[i+2]` (skipping `i+1`).
We take the better result between these two options using a helper `combine` function that prioritizes a higher special index count, then a lower operation count. The base cases for `dp[n]` and `dp[n+1]` are `(0,0)` (representing no special indices or cost beyond the array bounds). The final answer is `dp[1][1]` (the minimum operations required for the maximum special indices considering the array from index 1).

Time Complexity: O(N) because we iterate through the relevant part of the array once (from `n-2` down to `1`), performing constant time operations in each step.
Space Complexity: O(N) for the DP array. This can be optimized to O(1) as `dp[i]` only depends on `dp[i+1]` and `dp[i+2]`.
"""
from typing import List, Optional

class Solution:
    def minIncrease(self, nums: List[int]) -> int:
        n = len(nums)

        # Base case: if n < 3, no indices can be special (indices 0 and n-1 cannot be special).
        if n < 3:
            return 0

        # Helper function to combine results (max_count, then min_cost)
        def combine(res1: tuple[int, int], res2: tuple[int, int]) -> tuple[int, int]:
            if res1[0] > res2[0]:
                return res1
            if res2[0] > res1[0]:
                return res2
            # If counts are equal, choose the one with minimum operations
            return (res1[0], min(res1[1], res2[1]))

        # dp[i] will store (max_special_indices, min_operations) for the suffix
        # of the array starting from index i up to n-1.
        # We need dp[i+1] and dp[i+2], so dp array size n+2 is used for convenience
        # to handle out-of-bounds accesses for the last few iterations gracefully.
        # dp[n] and dp[n+1] implicitly act as base cases (0 special indices, 0 cost).
        dp = [(0, 0)] * (n + 2)

        # Iterate from n-2 down to 1. These are the only indices that can potentially be special.
        for i in range(n - 2, 0, -1):
            # Option 1: Do not make index i special
            # The result for dp[i] in this case is simply the optimal result
            # from index i+1 onwards.
            option_not_special = dp[i + 1]

            # Option 2: Make index i special
            # Calculate the cost to make nums[i] a peak.
            # It needs to be strictly greater than both nums[i-1] and nums[i+1].
            # The minimum required value for nums[i] is max(nums[i-1], nums[i+1]) + 1.
            target_val_for_i = max(nums[i - 1], nums[i + 1]) + 1
            cost_to_make_i_special = max(0, target_val_for_i - nums[i])

            # If index i is made special, then index i+1 cannot be special
            # (because special indices cannot be adjacent).
            # So, we add 1 to the special count (for index i) and
            # the cost to make i special, then combine this with the optimal result
            # from index i+2 onwards.
            option_special = (1 + dp[i + 2][0], cost_to_make_i_special + dp[i + 2][1])

            # Choose the better of the two options using our combine logic.
            dp[i] = combine(option_not_special, option_special)

        # The final answer is the minimum operations required for the maximum
        # number of special indices considering the array from index 1.
        return dp[1][1]

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.minIncrease([1, 2, 2]) == 1, "Example 1 Failed"

    # Example 2
    assert s.minIncrease([2, 1, 1, 3]) == 2, "Example 2 Failed"

    # Example 3
    assert s.minIncrease([5, 2, 1, 4, 3]) == 4, "Example 3 Failed"

    # Custom test cases
    # No operations needed for an already peaked array
    assert s.minIncrease([1, 3, 1, 5, 1]) == 0, "Custom Test 1 Failed"

    # No operations needed, even if some values are very low. Optimal to make non-costly peaks.
    assert s.minIncrease([1, 2, 0, 2, 1]) == 0, "Custom Test 2 Failed"

    # All identical elements, need to increase some to form peaks
    assert s.minIncrease([1, 1, 1, 1, 1]) == 2, "Custom Test 3 Failed"

    # Large values, test for correctness with large costs
    assert s.minIncrease([10**9, 1, 10**9, 1, 10**9]) == 2 * (10**9), "Custom Test 4 Failed"

    # Smallest n (n=3) - already a peak
    assert s.minIncrease([1, 2, 1]) == 0, "Smallest n test 1 Failed"
    
    # Smallest n (n=3) - needs operations
    assert s.minIncrease([1, 1, 1]) == 1, "Smallest n test 2 Failed"

    print("All tests passed!")