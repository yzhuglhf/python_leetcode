"""
Minimum Operations to Make Array Modulo Alternating I
Difficulty: Medium

Description:
This problem asks for the minimum operations to transform an array `nums` such that elements at even indices consistently have a remainder `x` when divided by `k`, and elements at odd indices consistently have a remainder `y` when divided by `k`. The integers `x` and `y` must be distinct and fall within the range `[0, k-1)`. An operation involves increasing or decreasing any element by 1.

Example:
Input: nums = [1,4,2,8], k = 3
Output: 2
Explanation: Choosing x=1 for even indices and y=2 for odd indices:
- nums[0]=1 (1%3=1, matches x).
- nums[1]=4 (4%3=1, needs to be 2, cost 1). Increment nums[1] to 5.
- nums[2]=2 (2%3=2, needs to be 1, cost 1). Decrement nums[2] to 1.
- nums[3]=8 (8%3=2, matches y).
Total operations = 1 + 1 = 2.

Approach:
The core idea is to find the optimal pair of distinct target remainders `(x, y)` that minimizes operations. The cost to change an element `num` (which has `num % k == r_actual`) to achieve a `target_remainder` is `abs(r_actual - target_remainder)`.
First, we pre-calculate the frequency of each possible remainder `0` to `k-1` for elements at even indices and odd indices separately. These frequencies are stored in `even_counts` and `odd_counts` arrays.
Next, we iterate through all possible pairs `(x, y)` where `0 <= x, y < k` and `x != y`. For each pair, we calculate the total operations required:
1. Operations for even indices: Sum of `(even_counts[r_actual] * abs(r_actual - x))` for all `r_actual` from `0` to `k-1`.
2. Operations for odd indices: Sum of `(odd_counts[r_actual] * abs(r_actual - y))` for all `r_actual` from `0` to `k-1`.
The sum of these two constitutes the total operations for the current `(x, y)` pair. We keep track of the minimum total operations found across all valid pairs. This minimum value is the answer.

Time Complexity: O(N + K^3)
- O(N) to iterate through the `nums` array and populate the `even_counts` and `odd_counts` arrays.
- O(K^2) for the nested loops iterating through all possible distinct pairs `(x, y)`.
- Inside each pair iteration, `calculate_ops` function takes O(K) time as it iterates through `k` possible actual remainders.
- Thus, the total time complexity is O(N + K*K*K) = O(N + K^3). Given `N, K <= 100`, this is efficient enough.
Space Complexity: O(K)
- To store the `even_counts` and `odd_counts` arrays, each of size `k`.
"""
from typing import List, Optional

class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        # Step 1: Count frequencies of remainders for even and odd indices
        # even_counts[r] will store how many even-indexed numbers have remainder r when divided by k
        even_counts = [0] * k
        # odd_counts[r] will store how many odd-indexed numbers have remainder r when divided by k
        odd_counts = [0] * k
        
        for i in range(n):
            remainder = nums[i] % k
            if i % 2 == 0:  # Even index
                even_counts[remainder] += 1
            else:  # Odd index
                odd_counts[remainder] += 1
        
        # Helper function to calculate operations for a given target remainder
        # `counts` is either even_counts or odd_counts
        # `target_remainder` is the desired x or y
        def calculate_ops(counts: List[int], target_remainder: int) -> int:
            ops = 0
            for r_actual in range(k):
                # For each actual remainder, add the cost to change it to target_remainder
                # multiplied by its frequency.
                ops += counts[r_actual] * abs(r_actual - target_remainder)
            return ops

        min_total_ops = float('inf')
        
        # Step 2: Iterate through all distinct pairs (x, y) where 0 <= x, y < k
        for x in range(k):
            for y in range(k):
                if x == y:
                    continue # x and y must be distinct as per problem statement
                
                # Calculate operations needed for current x and y
                ops_for_even = calculate_ops(even_counts, x)
                ops_for_odd = calculate_ops(odd_counts, y)
                
                # Update the minimum total operations
                min_total_ops = min(min_total_ops, ops_for_even + ops_for_odd)
        
        return min_total_ops

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1,4,2,8]
    k1 = 3
    expected1 = 2
    assert s.minOperations(nums1, k1) == expected1, f"Test 1 Failed: nums={nums1}, k={k1}, Expected: {expected1}, Got: {s.minOperations(nums1, k1)}"

    # Example 2
    nums2 = [1,1,1]
    k2 = 3
    expected2 = 1
    assert s.minOperations(nums2, k2) == expected2, f"Test 2 Failed: nums={nums2}, k={k2}, Expected: {expected2}, Got: {s.minOperations(nums2, k2)}"

    # Custom Test Case 1: All elements already satisfy x=0, y=1 with k=2
    nums3 = [0,1,0,1]
    k3 = 2
    expected3 = 0
    assert s.minOperations(nums3, k3) == expected3, f"Test 3 Failed: nums={nums3}, k={k3}, Expected: {expected3}, Got: {s.minOperations(nums3, k3)}"

    # Custom Test Case 2: Array with length 1.
    # For nums=[10], k=5: even_counts={0:1}, odd_counts={}
    # We can choose x=0 and any y != 0, e.g., y=1.
    # ops_even(0) = 0. ops_odd(1) = 0. Total = 0.
    nums4 = [10]
    k4 = 5
    expected4 = 0 
    assert s.minOperations(nums4, k4) == expected4, f"Test 4 Failed: nums={nums4}, k={k4}, Expected: {expected4}, Got: {s.minOperations(nums4, k4)}"

    # Custom Test Case 3: More complex scenario
    nums5 = [7, 8, 9, 10, 11]
    k5 = 4
    # Even indices: nums[0]=7, nums[2]=9, nums[4]=11
    # Remainders: 7%4=3, 9%4=1, 11%4=3 => even_counts = {0:0, 1:1, 2:0, 3:2}
    # Odd indices: nums[1]=8, nums[3]=10
    # Remainders: 8%4=0, 10%4=2 => odd_counts = {0:1, 1:0, 2:1, 3:0}
    # Test with x=3, y=0:
    # ops_even(x=3): (even_counts[1]*abs(1-3)) + (even_counts[3]*abs(3-3)) = (1*2) + (2*0) = 2
    # ops_odd(y=0): (odd_counts[0]*abs(0-0)) + (odd_counts[2]*abs(2-0)) = (1*0) + (1*2) = 2
    # Total = 2 + 2 = 4. This is the minimum.
    expected5 = 4
    assert s.minOperations(nums5, k5) == expected5, f"Test 5 Failed: nums={nums5}, k={k5}, Expected: {expected5}, Got: {s.minOperations(nums5, k5)}"

    print("All tests passed!")

