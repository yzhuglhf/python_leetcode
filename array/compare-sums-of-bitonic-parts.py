"""
Compare Sums of Bitonic Parts
Difficulty: Medium

Description:
This problem involves analyzing a bitonic array, which is an array that strictly increases to a single peak element and then strictly decreases. The task is to split the array into two parts: an ascending part (from index 0 to the peak element, inclusive) and a descending part (from the peak element to index n-1, inclusive). The goal is to compare the sums of these two parts and return 0 if the ascending sum is greater, 1 if the descending sum is greater, or -1 if both sums are equal.

Example:
Input: nums = [1,3,2,1]
Output: 1
Explanation: Peak element is nums[1] = 3. The ascending part is [1, 3] with a sum of 4. The descending part is [3, 2, 1] with a sum of 6. Since the descending part has a larger sum (6 > 4), the function returns 1.

Approach:
The solution proceeds in three main steps. First, it identifies the index of the peak element. Since the array is strictly increasing until the peak and then strictly decreasing, the peak is the point where the increasing trend stops. This can be efficiently found using a linear scan: we iterate through the array, incrementing `peak_idx` as long as `nums[peak_idx]` is strictly less than `nums[peak_idx + 1]`. The loop terminates when `peak_idx` points to the peak element. Second, two separate sums are calculated: `sum_asc` for elements from index 0 up to `peak_idx` (inclusive), and `sum_desc` for elements from `peak_idx` to `n-1` (inclusive). It's crucial that the peak element is included in both sums as per the problem description. Finally, these two calculated sums are compared, and 0, 1, or -1 is returned based on the comparison result.

Time Complexity: O(N)
The linear scan to find the peak element takes O(N) time in the worst case (e.g., if the peak is near the end). Subsequently, calculating `sum_asc` iterates up to `peak_idx` elements, and calculating `sum_desc` iterates from `peak_idx` to `n-1` elements. In total, all elements of the array are visited approximately twice across these summing operations. Therefore, the overall time complexity is O(N).

Space Complexity: O(1)
The algorithm uses a constant number of variables (e.g., `n`, `peak_idx`, `sum_asc`, `sum_desc`) regardless of the input array size. No additional data structures that scale with `N` are created. Thus, the space complexity is O(1).
"""
from typing import List, Optional

class Solution:
    def compareBitonicSums(self, nums: list[int]) -> int:
        n = len(nums)

        # 1. Find the peak element's index
        # The peak is the point where the array stops strictly increasing.
        # We iterate while nums[peak_idx] is less than nums[peak_idx + 1].
        # The loop terminates when peak_idx points to the actual peak.
        peak_idx = 0
        while peak_idx < n - 1 and nums[peak_idx] < nums[peak_idx + 1]:
            peak_idx += 1
        
        # At this point, peak_idx holds the index of the peak element.

        # 2. Calculate the sum of the ascending part
        # The ascending part includes elements from index 0 up to peak_idx (inclusive).
        sum_asc = 0
        for i in range(peak_idx + 1):
            sum_asc += nums[i]
        
        # 3. Calculate the sum of the descending part
        # The descending part includes elements from peak_idx to n - 1 (inclusive).
        sum_desc = 0
        for i in range(peak_idx, n):
            sum_desc += nums[i]
            
        # 4. Compare the sums and return the appropriate result
        if sum_asc > sum_desc:
            return 0
        elif sum_desc > sum_asc:
            return 1
        else: # sum_asc == sum_desc
            return -1

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.compareBitonicSums(nums=[1,3,2,1]) == 1, "Example 1 Failed"
    
    # Example 2
    assert s.compareBitonicSums(nums=[2,4,5,2]) == 0, "Example 2 Failed"
    
    # Example 3
    assert s.compareBitonicSums(nums=[1,2,4,3]) == -1, "Example 3 Failed"

    # Additional test cases
    # Case: Symmetric array, sums should be equal
    assert s.compareBitonicSums(nums=[1, 2, 3, 4, 5, 4, 3, 2, 1]) == -1, "Test Case 4 Failed: Symmetric array"
    
    # Case: Descending part sum is greater
    assert s.compareBitonicSums(nums=[1, 5, 2]) == 1, "Test Case 5 Failed: Descending sum greater"

    # Case: Ascending part sum is greater (e.g., peak closer to start)
    assert s.compareBitonicSums(nums=[1, 10, 2, 3]) == 0, "Test Case 6 Failed: Ascending sum greater"

    # Case: Array that is primarily increasing (peak at the end)
    # The problem implies a "strictly decreasing" part, but if not, this is how it's handled.
    assert s.compareBitonicSums(nums=[1, 2, 3]) == 0, "Test Case 7 Failed: Primarily increasing"

    # Case: Array that is primarily decreasing (peak at the start)
    # The problem implies a "strictly increasing" part, but if not, this is how it's handled.
    assert s.compareBitonicSums(nums=[3, 2, 1]) == 1, "Test Case 8 Failed: Primarily decreasing"

    print("All tests passed!")

