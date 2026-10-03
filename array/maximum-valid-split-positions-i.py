"""
Maximum Valid Split Positions I
Difficulty: Medium

Description:
This problem asks us to find the maximum possible score of an array, which is defined as the number of valid split positions. We are allowed to remove at most one element from the initial array `nums`. A split position `i` in an array `arr` is valid if the greatest common divisor (GCD) of the elements before or at `i` equals the GCD of elements after `i`.

Example:
Input: nums = [10,30,15,10]
Output: 2
Explanation: Removing 15 yields arr = [10, 30, 10].
For i=0: gcd([10])=10, gcd([30,10])=10. Valid.
For i=1: gcd([10,30])=10, gcd([10])=10. Valid.
Total 2 valid splits.

Approach:
The problem allows removing at most one element. This implies two main scenarios: either no element is removed, or exactly one element is removed. Since the input array `nums` has length `N` (up to 1000), there are `N+1` possible arrays `arr` to consider (one for no removal, and `N` for removing each element `nums[j]` individually). We will iterate through all these `N+1` possibilities, calculate the score for each `arr`, and return the maximum score found.

To calculate the score for a given array `arr` of length `m`:
1. If `m <= 1`, it has no valid split positions, so the score is 0.
2. Otherwise, we precompute two auxiliary arrays: `prefix_gcd` and `suffix_gcd`.
   - `prefix_gcd[k]` stores `gcd(arr[0]...arr[k])`.
   - `suffix_gcd[k]` stores `gcd(arr[k]...arr[m-1])`.
   These can be computed efficiently: `prefix_gcd[k] = gcd(prefix_gcd[k-1], arr[k])` and `suffix_gcd[k] = gcd(arr[k], suffix_gcd[k+1])`. Each step takes `O(log(max_val))` time.
3. Iterate through all possible split positions `i` from `0` to `m-2`. For each `i`, check if `prefix_gcd[i] == suffix_gcd[i+1]`. If they are equal, increment the score.
4. Return the total score for this `arr`.

The overall algorithm will be:
1. Initialize `max_score = 0`.
2. Call `calculate_score(nums)` (no element removed) and update `max_score`.
3. For each index `j` from `0` to `N-1`:
   a. Construct `current_arr` by removing `nums[j]` from `nums` (i.e., `nums[:j] + nums[j+1:]`). This slicing and concatenation creates a new list.
   b. Call `calculate_score(current_arr)` and update `max_score`.
4. Return `max_score`.

Time Complexity: O(N^2 * log(max_val)). There are `N+1` potential arrays to examine. For each array of length `O(N)`, constructing it takes `O(N)` time (for slicing and concatenation), and then computing prefix/suffix GCDs and checking splits takes `O(N * log(max_val))` time. Thus, the total time complexity is `(N+1) * (O(N) + O(N * log(max_val)))` which simplifies to `O(N^2 * log(max_val))`. With `N=1000` and `max_val=10^9`, this is roughly `10^6 * 30 = 3 * 10^7` operations, which should pass within typical time limits.
Space Complexity: O(N). For each `arr` processed, `prefix_gcd` and `suffix_gcd` take `O(N)` space. The `current_arr` also takes `O(N)` space.
"""
import math
from typing import List, Optional

class Solution:
    def maxValidSplits(self, nums: list[int]) -> int:
        
        def calculate_score(arr: list[int]) -> int:
            m = len(arr)
            # An array of length 1 has no valid split positions.
            # An array of length 0 also has no valid split positions.
            if m <= 1:
                return 0

            # Compute prefix GCDs
            prefix_gcd = [0] * m
            prefix_gcd[0] = arr[0]
            for k in range(1, m):
                prefix_gcd[k] = math.gcd(prefix_gcd[k-1], arr[k])

            # Compute suffix GCDs
            suffix_gcd = [0] * m
            suffix_gcd[m-1] = arr[m-1]
            for k in range(m - 2, -1, -1):
                suffix_gcd[k] = math.gcd(arr[k], suffix_gcd[k+1])

            score = 0
            # A split position i means splitting arr into arr[0..i] and arr[i+1..m-1]
            # Valid split positions are from 0 up to m-2 (since arr[i+1..m-1] must not be empty)
            for i in range(m - 1): 
                if prefix_gcd[i] == suffix_gcd[i+1]:
                    score += 1
            return score

        max_score = 0
        N = len(nums)

        # Case 1: No element removed
        max_score = max(max_score, calculate_score(nums))

        # Case 2: Remove one element at each possible index j
        for j in range(N):
            # Construct the array with nums[j] removed
            current_arr = nums[:j] + nums[j+1:]
            max_score = max(max_score, calculate_score(current_arr))
        
        return max_score

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.maxValidSplits([10,30,15,10]) == 2, "Example 1 failed"

    # Example 2
    assert s.maxValidSplits([2,10,14]) == 1, "Example 2 failed"

    # Example 3
    assert s.maxValidSplits([2,4]) == 0, "Example 3 failed"

    # Custom Test Cases
    # All same elements (multiple splits possible)
    assert s.maxValidSplits([7,7,7,7]) == 3, "Custom Test 1 failed: [7,7,7,7]"

    # All different, no common GCD
    assert s.maxValidSplits([1,2,3,4,5]) == 0, "Custom Test 2 failed: [1,2,3,4,5]"
    
    # Array with 1s, gcd usually becomes 1
    assert s.maxValidSplits([1,2,3,1,2,3]) == 0, "Custom Test 3 failed: [1,2,3,1,2,3]"

    # Test with varying GCDs
    assert s.maxValidSplits([12, 18, 6, 30]) == 1, "Custom Test 4 failed: [12,18,6,30]"
    
    # Small length 2 array, no valid splits
    assert s.maxValidSplits([6, 9]) == 0, "Custom Test 5 failed: [6,9]"

    # Array where removing any element does not create valid splits
    assert s.maxValidSplits([4, 8, 2, 16]) == 0, "Custom Test 6 failed: [4,8,2,16]"

    # All ones, max splits
    assert s.maxValidSplits([1,1,1,1,1]) == 4, "Custom Test 7 failed: [1,1,1,1,1]"
    
    # Large numbers, should still work correctly
    assert s.maxValidSplits([1000000000, 500000000, 250000000]) == 0, "Custom Test 8 failed: [1e9, 5e8, 2.5e8]"


    print("All tests passed!")

