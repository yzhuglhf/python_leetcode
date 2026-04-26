"""
Median of Two Sorted Arrays (LeetCode #4)
Difficulty: Hard

Description:
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log(min(m, n))).

Example:
nums1 = [1, 3], nums2 = [2]
Output: 2.0
Explanation: merged array = [1, 2, 3], median = 2.0

Approach:
Use binary search on the smaller array to partition both arrays such that the left half and right half have equal (or nearly equal) elements.
For each partition, ensure all elements on the left are less than or equal to all elements on the right. We binary search on the smaller array
to find the correct cut position. Once found, the median is either the middle element (odd total length) or the average of two middle elements (even total length).
The key insight is that if we partition at position i in nums1 and position j in nums2, we need: nums1[i-1] <= nums2[j] and nums2[j-1] <= nums1[i].

Time Complexity: O(log(min(m, n)))
Space Complexity: O(1)
"""
from typing import List


class Solution:
    def findMediaSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure nums1 is the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        m, n = len(nums1), len(nums2)
        left, right = 0, m
        
        while left <= right:
            partition1 = (left + right) // 2
            partition2 = (m + n + 1) // 2 - partition1
            
            # Handle edge cases for partition boundaries
            maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            minRight1 = float('inf') if partition1 == m else nums1[partition1]
            
            maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
            minRight2 = float('inf') if partition2 == n else nums2[partition2]
            
            # Check if we found the correct partition
            if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
                # If total length is even
                if (m + n) % 2 == 0:
                    return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0
                # If total length is odd
                else:
                    return float(max(maxLeft1, maxLeft2))
            
            # Adjust binary search bounds
            elif maxLeft1 > minRight2:
                right = partition1 - 1
            else:
                left = partition1 + 1
        
        return -1.0  # Should never reach here with valid input


if __name__ == "__main__":
    s = Solution()
    assert s.findMediaSortedArrays([1, 3], [2]) == 2.0
    assert s.findMediaSortedArrays([1, 2], [3, 4]) == 2.5
    assert s.findMediaSortedArrays([0, 0], [0, 0]) == 0.0
    assert s.findMediaSortedArrays([], [1]) == 1.0
    assert s.findMediaSortedArrays([2], []) == 2.0
    assert s.findMediaSortedArrays([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]) == 11.0
    print("All tests passed!")
