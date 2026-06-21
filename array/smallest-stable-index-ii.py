"""
Smallest Stable Index II
Difficulty: Medium

Description:
This problem asks us to find the smallest index `i` in an array `nums` where its "instability score" is less than or equal to a given integer `k`. The instability score for an index `i` is defined as the difference between the maximum value in the prefix `nums[0..i]` and the minimum value in the suffix `nums[i..n-1]`. If no such stable index exists, we should return -1.

Example:
Input: nums = [5,0,1,4], k = 3
Output: 3
Explanation: For index 3, max(nums[0..3]) is 5 and min(nums[3..3]) is 4. The instability score is 5 - 4 = 1, which is <= k=3. This is the first such index.

Approach:
The core idea is to efficiently calculate `max(nums[0..i])` and `min(nums[i..n-1])` for all possible indices `i`. We can achieve this by precomputing two auxiliary arrays: `prefix_max` and `suffix_min`. The `prefix_max` array stores the maximum value encountered from the beginning of the array up to each index, calculated in a single pass from left to right. Similarly, the `suffix_min` array stores the minimum value encountered from the end of the array back to each index, calculated in a single pass from right to left. After precomputing these arrays, we iterate from `i = 0` to `n-1`, calculate the instability score as `prefix_max[i] - suffix_min[i]`. The first index `i` for which this score is less than or equal to `k` is our answer, as we are looking for the *smallest* stable index. If no such index is found after checking all `i`, we return -1.

Time Complexity: O(n)
Space Complexity: O(n)
"""
from typing import List

class Solution:
    def firstStableIndex(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return -1 # According to constraints, n >= 1, but good for robustness

        # Step 1: Precompute prefix maximums
        # prefix_max[i] stores max(nums[0...i])
        prefix_max = [0] * n
        prefix_max[0] = nums[0]
        for i in range(1, n):
            prefix_max[i] = max(prefix_max[i-1], nums[i])

        # Step 2: Precompute suffix minimums
        # suffix_min[i] stores min(nums[i...n-1])
        suffix_min = [0] * n
        suffix_min[n-1] = nums[n-1]
        for i in range(n - 2, -1, -1):
            suffix_min[i] = min(suffix_min[i+1], nums[i])

        # Step 3: Iterate and find the smallest stable index
        for i in range(n):
            instability_score = prefix_max[i] - suffix_min[i]
            if instability_score <= k:
                return i
        
        # If no stable index is found after checking all possibilities
        return -1

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.firstStableIndex(nums=[5,0,1,4], k=3) == 3, f"Test Case 1 Failed: {s.firstStableIndex(nums=[5,0,1,4], k=3)}"

    # Example 2
    assert s.firstStableIndex(nums=[3,2,1], k=1) == -1, f"Test Case 2 Failed: {s.firstStableIndex(nums=[3,2,1], k=1)}"

    # Example 3
    assert s.firstStableIndex(nums=[0], k=0) == 0, f"Test Case 3 Failed: {s.firstStableIndex(nums=[0], k=0)}"

    # Additional test cases
    # All elements same, k=0
    assert s.firstStableIndex(nums=[10,10,10,10], k=0) == 0, f"Test Case 4 Failed: {s.firstStableIndex(nums=[10,10,10,10], k=0)}"
    
    # Large k, should find first index (0)
    assert s.firstStableIndex(nums=[1,2,3,4,5], k=100) == 0, f"Test Case 5 Failed: {s.firstStableIndex(nums=[1,2,3,4,5], k=100)}"

    # No stable index, larger array with high variance
    assert s.firstStableIndex(nums=[100, 1, 200, 2], k=10) == -1, f"Test Case 6 Failed: {s.firstStableIndex(nums=[100, 1, 200, 2], k=10)}"

    # Descending order, k=0 (no stable index unless all elements are the same)
    assert s.firstStableIndex(nums=[5,4,3,2,1], k=0) == -1, f"Test Case 7 Failed: {s.firstStableIndex(nums=[5,4,3,2,1], k=0)}"

    # Single element, k > 0
    assert s.firstStableIndex(nums=[10], k=5) == 0, f"Test Case 8 Failed: {s.firstStableIndex(nums=[10], k=5)}"

    # Ascending order, k=0 (only first element can be 0 if all are same, otherwise -1)
    assert s.firstStableIndex(nums=[1,2,3,4,5], k=0) == -0, f"Test Case 9 Failed: {s.firstStableIndex(nums=[1,2,3,4,5], k=0)}"
    # Instability scores:
    # i=0: max(1)=1, min(1,2,3,4,5)=1. Score = 0. So index 0 is stable.

    print("All tests passed!")