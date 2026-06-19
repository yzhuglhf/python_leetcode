"""
Maximum Score of a Split
Difficulty: Medium

Description:
This problem asks us to find the maximum score achievable by splitting an integer array `nums` into two non-empty parts at an index `i`. The score for a split at `i` is defined as the sum of elements from `nums[0]` to `nums[i]` (prefix sum) minus the minimum element from `nums[i+1]` to `nums[n-1]` (suffix minimum). We need to iterate through all valid split points `i` (from `0` to `n-2`) and return the highest score found.

Example:
Input: nums = [10,-1,3,-4,-5]
Output: 17
Explanation: The optimal split is at i = 2. Here, prefixSum(2) = (10 + (-1) + 3) = 12, and suffixMin(2) = min(nums[3], nums[4]) = min(-4, -5) = -5. The score is 12 - (-5) = 17.

Approach:
A straightforward approach to calculate `prefixSum(i)` and `suffixMin(i)` for each `i` would result in an O(N^2) time complexity, which is inefficient for large input arrays. To optimize this, we can use dynamic programming by precomputing all prefix sums and all suffix minimums. First, we create a `prefix_sums` array where `prefix_sums[k]` stores the cumulative sum of elements from `nums[0]` up to `nums[k]`. This array can be built in a single pass from left to right. Second, we create a `suffix_mins` array where `suffix_mins[k]` stores the minimum value among elements from `nums[k]` up to `nums[n-1]`. This array can be built in a single pass from right to left. Both precomputation steps take O(N) time. After these arrays are ready, we iterate through all valid split indices `i` (from `0` to `n-2`). For each `i`, `prefixSum(i)` is directly `prefix_sums[i]`, and `suffixMin(i)` is directly `suffix_mins[i+1]`. We calculate the score `prefix_sums[i] - suffix_mins[i+1]` and continuously update a `max_score` variable. Finally, we return the `max_score`.

Time Complexity: O(N)
The computation of the `prefix_sums` array takes O(N) time. Similarly, the computation of the `suffix_mins` array also takes O(N) time. The final loop iterates `N-1` times, performing constant-time lookups and arithmetic operations in each iteration, contributing O(N) to the total time. Thus, the overall time complexity is O(N).
Space Complexity: O(N)
We use two auxiliary arrays, `prefix_sums` and `suffix_mins`, each of size N. Therefore, the space complexity is O(N).
"""
import math
from typing import List, Optional

class Solution:
    def maximumScore(self, nums: List[int]) -> int:
        n = len(nums)

        # Step 1: Precompute prefix sums
        # prefix_sums[k] stores the sum of nums[0]...nums[k]
        prefix_sums = [0] * n
        prefix_sums[0] = nums[0]
        for i in range(1, n):
            prefix_sums[i] = prefix_sums[i-1] + nums[i]

        # Step 2: Precompute suffix minimums
        # suffix_mins[k] stores the minimum of nums[k]...nums[n-1]
        suffix_mins = [0] * n
        suffix_mins[n-1] = nums[n-1]
        for i in range(n - 2, -1, -1): # Iterate from n-2 down to 0
            suffix_mins[i] = min(nums[i], suffix_mins[i+1])
        
        # Step 3: Iterate through all possible split indices i
        # A split index i must be 0 <= i < n - 1.
        # This means i goes from 0 up to n - 2 (inclusive).
        max_score = -math.inf # Initialize with negative infinity to correctly find the maximum score

        for i in range(n - 1):
            # For a split at index i:
            # prefixSum(i) is retrieved from prefix_sums[i]
            # suffixMin(i) is the minimum of nums[i+1]...nums[n-1], which is stored in suffix_mins[i+1]
            
            current_prefix_sum = prefix_sums[i]
            current_suffix_min = suffix_mins[i+1]
            
            current_score = current_prefix_sum - current_suffix_min
            max_score = max(max_score, current_score)
            
        return int(max_score) # Cast to int as the problem asks for an integer return value

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [10,-1,3,-4,-5]
    expected1 = 17
    assert s.maximumScore(nums1) == expected1, f"Test Case 1 Failed: Input: {nums1}, Expected: {expected1}, Got: {s.maximumScore(nums1)}"

    # Example 2
    nums2 = [-7,-5,3]
    expected2 = -2
    assert s.maximumScore(nums2) == expected2, f"Test Case 2 Failed: Input: {nums2}, Expected: {expected2}, Got: {s.maximumScore(nums2)}"

    # Example 3
    nums3 = [1,1]
    expected3 = 0
    assert s.maximumScore(nums3) == expected3, f"Test Case 3 Failed: Input: {nums3}, Expected: {expected3}, Got: {s.maximumScore(nums3)}"

    # Additional test case: All positive numbers
    nums4 = [1,2,3,4,5] # i=3: prefixSum(3)=10, suffixMin(3)=5. Score = 10-5 = 5
    expected4 = 5
    assert s.maximumScore(nums4) == expected4, f"Test Case 4 Failed: Input: {nums4}, Expected: {expected4}, Got: {s.maximumScore(nums4)}"

    # Additional test case: All negative numbers
    nums5 = [-1,-2,-3,-4,-5] # i=0: prefixSum(0)=-1, suffixMin(0)=-5. Score = -1 - (-5) = 4
    expected5 = 4
    assert s.maximumScore(nums5) == expected5, f"Test Case 5 Failed: Input: {nums5}, Expected: {expected5}, Got: {s.maximumScore(nums5)}"

    # Edge case: N=2, first positive, second negative
    nums6 = [5, -10] # i=0: prefixSum(0)=5, suffixMin(0)=-10. Score = 5 - (-10) = 15
    expected6 = 15
    assert s.maximumScore(nums6) == expected6, f"Test Case 6 Failed: Input: {nums6}, Expected: {expected6}, Got: {s.maximumScore(nums6)}"

    # Edge case: N=2, first negative, second positive
    nums7 = [-10, 5] # i=0: prefixSum(0)=-10, suffixMin(0)=5. Score = -10 - 5 = -15
    expected7 = -15
    assert s.maximumScore(nums7) == expected7, f"Test Case 7 Failed: Input: {nums7}, Expected: {expected7}, Got: {s.maximumScore(nums7)}"

    # Test case with larger values and mixed signs
    nums8 = [100, -200, 300, -50, 400, -1000, 500]
    # N=7. i runs from 0 to 5.
    # prefix_sums: [100, -100, 200, 150, 550, -450, 50]
    # suffix_mins: [-1000, -1000, -1000, -1000, -1000, -1000, 500] (from right: 500, -1000, -1000, -50, -50, -50, -50)
    # The example walk-through for suffix_mins was incorrect; corrected calculation:
    # suffix_mins[6] = 500
    # suffix_mins[5] = min(nums[5], suffix_mins[6]) = min(-1000, 500) = -1000
    # suffix_mins[4] = min(nums[4], suffix_mins[5]) = min(400, -1000) = -1000
    # suffix_mins[3] = min(nums[3], suffix_mins[4]) = min(-50, -1000) = -1000
    # suffix_mins[2] = min(nums[2], suffix_mins[3]) = min(300, -1000) = -1000
    # suffix_mins[1] = min(nums[1], suffix_mins[2]) = min(-200, -1000) = -1000
    # suffix_mins[0] = min(nums[0], suffix_mins[1]) = min(100, -1000) = -1000
    # Corrected suffix_mins: [-1000, -1000, -1000, -1000, -1000, -1000, 500]

    # Scores:
    # i=0: pS[0]=100, sM[1]=-1000. Score = 100 - (-1000) = 1100
    # i=1: pS[1]=-100, sM[2]=-1000. Score = -100 - (-1000) = 900
    # i=2: pS[2]=200, sM[3]=-1000. Score = 200 - (-1000) = 1200
    # i=3: pS[3]=150, sM[4]=-1000. Score = 150 - (-1000) = 1150
    # i=4: pS[4]=550, sM[5]=-1000. Score = 550 - (-1000) = 1550
    # i=5: pS[5]=-450, sM[6]=500. Score = -450 - 500 = -950
    expected8 = 1550
    assert s.maximumScore(nums8) == expected8, f"Test Case 8 Failed: Input: {nums8}, Expected: {expected8}, Got: {s.maximumScore(nums8)}"


    print("All tests passed!")

