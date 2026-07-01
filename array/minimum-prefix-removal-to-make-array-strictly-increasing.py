"""
Minimum Prefix Removal to Make Array Strictly Increasing
Difficulty: Medium

Description:
Given an integer array `nums`, the task is to find the minimum length of a prefix that needs to be removed so that the remaining suffix of the array is strictly increasing. An empty array or a single-element array is considered strictly increasing. The length of the removed prefix can range from 0 (if the array is already strictly increasing) to `n` (if the entire array is removed, leaving an empty array).

Example:
Input: nums = [1,-1,2,3,3,4,5]
Output: 4
Explanation: Removing the prefix [1, -1, 2, 3] (length 4) leaves the remaining array [3, 4, 5], which is strictly increasing.

Approach:
The problem asks for the minimum length of a removed prefix, which is equivalent to finding the earliest possible starting index `j` such that the suffix `nums[j...n-1]` is strictly increasing. The length of the prefix removed would then be `j`. To minimize `j`, we need to find the longest possible strictly increasing suffix.

We can solve this by iterating through the array from right to left.
1. Initialize a variable `suffix_start_index` to `n-1` (where `n` is the length of `nums`). This represents the starting index of the current longest strictly increasing suffix found so far. The single element `nums[n-1]` always forms a strictly increasing suffix.
2. Iterate from `i = n-2` down to `0`.
3. In each iteration, compare `nums[i]` with `nums[i+1]`.
   - If `nums[i] < nums[i+1]`, it means `nums[i]` can be prepended to the strictly increasing suffix starting at `i+1` to form a new, longer strictly increasing suffix. So, we update `suffix_start_index = i`.
   - If `nums[i] >= nums[i+1]`, the strictly increasing property is broken. This means `nums[i]` cannot be part of the strictly increasing suffix that begins at `i+1`. Therefore, the longest strictly increasing suffix must start at `i+1` or an index further to the right. The `suffix_start_index` determined up to this point (which would be `i+1` from the previous valid comparison, or `n-1` if no elements could extend) is the final answer. We can stop the iteration because any further elements to the left (`< i`) would also be part of the prefix to be removed.
4. The final value of `suffix_start_index` is the minimum length of the prefix that must be removed.

This approach effectively finds the leftmost element that can be part of a strictly increasing suffix.

Time Complexity: O(N) because we iterate through the array at most once from right to left.
Space Complexity: O(1) as we only use a few constant extra variables.
"""
from typing import List, Optional

class Solution:
    def minimumPrefixLength(self, nums: List[int]) -> int:
        n = len(nums)

        # According to constraints, n >= 1.
        # If n=1, the array is already strictly increasing. The prefix length to remove is 0.
        # The loop below correctly handles n=1: suffix_start_index is initialized to 0.
        # The range(n-2, -1, -1) becomes range(-1, -1, -1), which is empty, so the loop doesn't run.
        # It then correctly returns 0.

        # suffix_start_index will store the starting index of the longest strictly increasing suffix.
        # Initialize to n-1, assuming the last element itself forms a strictly increasing suffix.
        # This is valid because a single-element array is always strictly increasing.
        suffix_start_index = n - 1

        # Iterate from the second to last element backwards.
        # We want to find the leftmost index 'i' such that nums[i...n-1] is strictly increasing.
        for i in range(n - 2, -1, -1):
            # If the current element is less than the next element,
            # it means it can extend the current strictly increasing suffix.
            if nums[i] < nums[i+1]:
                suffix_start_index = i
            else:
                # If nums[i] >= nums[i+1], the strictly increasing property is broken at this point.
                # This means nums[i] cannot be part of the strictly increasing suffix that starts at i+1.
                # The longest strictly increasing suffix must begin at i+1 or later.
                # So, the suffix_start_index we found just before this break point is final.
                # We can stop here, as any elements further to the left would also need to be removed.
                break
        
        # The length of the prefix to remove is the starting index of the remaining suffix.
        return suffix_start_index

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [1, -1, 2, 3, 3, 4, 5]
    expected1 = 4
    assert s.minimumPrefixLength(nums1) == expected1, f"Test 1 Failed: Input {nums1}, Expected {expected1}, Got {s.minimumPrefixLength(nums1)}"
    
    # Example 2
    nums2 = [4, 3, -2, -5]
    expected2 = 3
    assert s.minimumPrefixLength(nums2) == expected2, f"Test 2 Failed: Input {nums2}, Expected {expected2}, Got {s.minimumPrefixLength(nums2)}"
    
    # Example 3
    nums3 = [1, 2, 3, 4]
    expected3 = 0
    assert s.minimumPrefixLength(nums3) == expected3, f"Test 3 Failed: Input {nums3}, Expected {expected3}, Got {s.minimumPrefixLength(nums3)}"

    # Custom Test Cases
    # Single element array
    assert s.minimumPrefixLength([10]) == 0, "Test 4 Failed: Single element"
    
    # Two increasing elements
    assert s.minimumPrefixLength([1, 2]) == 0, "Test 5 Failed: Two increasing elements"
    
    # All decreasing
    assert s.minimumPrefixLength([5, 4, 3, 2, 1]) == 4, "Test 6 Failed: All decreasing (removed [5,4,3,2], left [1])"
    
    # Mixed decreasing/increasing
    assert s.minimumPrefixLength([1, 5, 2, 6, 3, 7]) == 4, "Test 7 Failed: Mixed 1 (removed [1,5,2,6], left [3,7])"
    
    # Ends with a small number, forcing more prefix removal
    assert s.minimumPrefixLength([1, 2, 3, 4, 5, 0]) == 5, "Test 8 Failed: Ends with small number (removed [1,2,3,4,5], left [0])"
    
    # Starts decreasing, then increases
    assert s.minimumPrefixLength([5, 4, 3, 2, 1, 10, 11]) == 5, "Test 9 Failed: Starts decreasing, then increases (removed [5,4,3,2,1], left [10,11])"
    
    # All same numbers (strictly increasing is broken immediately)
    assert s.minimumPrefixLength([1, 1, 1, 1]) == 3, "Test 10 Failed: All same (removed [1,1,1], left [1])"
    
    # Negative increasing numbers
    assert s.minimumPrefixLength([-5, -4, -3, -2, -1]) == 0, "Test 11 Failed: Negative increasing"

    # Zigzag pattern
    assert s.minimumPrefixLength([1, 2, 1, 2, 1, 2]) == 4, "Test 12 Failed: Zigzag (removed [1,2,1,2], left [1,2])"
    
    # Longer array, multiple breaks
    assert s.minimumPrefixLength([1, 10, 2, 20, 3, 30, 4, 40, 5, 50, 45, 60, 55]) == 10, "Test 13 Failed: Longer array" # [45, 60, 55] -> [45, 60] -> [45] -> 10,11
                                                                                               # (removed [1,10,2,20,3,30,4,40,5,50], left [45,60,55])
                                                                                               # [45, 60, 55] -> 55, not strictly increasing.
                                                                                               # [50, 45, 60, 55] -> 60, 55, not strictly increasing.
                                                                                               # -> suffix [55] -> start_index = 12
                                                                                               # i=11: nums[11]=60, nums[12]=55. 60 >= 55. break. suffix_start_index = 12
                                                                                               # So for [1, 10, 2, 20, 3, 30, 4, 40, 5, 50, 45, 60, 55], n=13
                                                                                               # suffix_start_index = 12 (for [55])
                                                                                               # i=11 (60): 60 >= 55. break.
                                                                                               # result is 12.
                                                                                               # My assertion is 10. Let's re-trace:
                                                                                               # [1, 10, 2, 20, 3, 30, 4, 40, 5, 50, 45, 60, 55]
                                                                                               # n = 13
                                                                                               # suffix_start_index = 12 (for [55])
                                                                                               # i=11 (nums[11]=60): 60 >= nums[12]=55. Break.
                                                                                               # Return suffix_start_index = 12.
                                                                                               # This seems correct for the logic. Removed [1..60] (length 12), left [55].
                                                                                               # My assertion of 10 was based on a faulty manual trace.
                                                                                               # Let's fix test 13.
    assert s.minimumPrefixLength([1, 10, 2, 20, 3, 30, 4, 40, 5, 50, 45, 60, 55]) == 12, "Test 13 Failed: Longer array"

    print("All tests passed!")

