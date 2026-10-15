"""
Sum of GCD of Formed Pairs
Difficulty: Medium

Description:
This problem requires constructing a `prefixGcd` array where each element `prefixGcd[i]` is the greatest common divisor (GCD) of `nums[i]` and the maximum value encountered in `nums` up to index `i`. After construction, this array is sorted. Finally, pairs are formed by taking the smallest and largest elements, and the sum of their GCDs is calculated, ignoring the middle element if the array's length is odd.

Example:
Input: nums = [3,6,2,8]
Output: 5
Explanation: prefixGcd becomes [3,6,2,8], which sorts to [2,3,6,8]. Pairs (2,8) and (3,6) give GCDs 2 and 3 respectively. Sum = 2 + 3 = 5.

Approach:
First, initialize an empty list for `prefixGcd` and a variable `current_max` to track the maximum value seen so far in `nums`. Iterate through the input `nums` array, updating `current_max` at each step to be the maximum of its current value and `nums[i]`. For each `i`, calculate `gcd(nums[i], current_max)` and append it to `prefixGcd`. Once `prefixGcd` is fully populated, sort it in non-decreasing order. Then, use two pointers, `left` starting at the beginning and `right` starting at the end of the sorted `prefixGcd` array. While `left < right`, form a pair `(prefixGcd[left], prefixGcd[right])`, compute their GCD, add it to a running sum, and move `left` one step right and `right` one step left. The loop naturally stops when all pairs are formed, ignoring the middle element if `n` is odd.

Time Complexity: O(N log N + N log(max_val)) where N is the length of `nums` and `max_val` is the maximum value in `nums`. This accounts for `N` GCD computations and sorting `N` elements.
Space Complexity: O(N) for storing the `prefixGcd` array.
"""
from typing import List
import math # For math.gcd

class Solution:
    def gcdSum(self, nums: List[int]) -> int:
        n = len(nums)
        
        prefixGcd = []
        current_max = 0 # Initialize with 0. Since nums[i] >= 1, max(0, nums[0]) correctly sets current_max to nums[0] for the first iteration.

        # Step 1: Construct prefixGcd array
        for i in range(n):
            current_max = max(current_max, nums[i])
            prefixGcd.append(math.gcd(nums[i], current_max))
        
        # Step 2: Sort prefixGcd in non-decreasing order
        prefixGcd.sort()
        
        # Step 3: Form pairs, compute GCDs, and sum them
        total_gcd_sum = 0
        left = 0
        right = n - 1
        
        while left < right:
            total_gcd_sum += math.gcd(prefixGcd[left], prefixGcd[right])
            left += 1
            right -= 1
            
        return total_gcd_sum

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [2, 6, 4]
    expected1 = 2
    assert s.gcdSum(nums1) == expected1, f"Test Case 1 Failed: Input {nums1}, Expected {expected1}, Got {s.gcdSum(nums1)}"

    # Example 2
    nums2 = [3, 6, 2, 8]
    expected2 = 5
    assert s.gcdSum(nums2) == expected2, f"Test Case 2 Failed: Input {nums2}, Expected {expected2}, Got {s.gcdSum(nums2)}"

    # Custom Test Case 1: n = 1 (odd length, middle element ignored)
    nums3 = [5]
    expected3 = 0
    assert s.gcdSum(nums3) == expected3, f"Test Case 3 Failed: Input {nums3}, Expected {expected3}, Got {s.gcdSum(nums3)}"

    # Custom Test Case 2: All elements are the same
    nums4 = [7, 7, 7]
    expected4 = 7
    assert s.gcdSum(nums4) == expected4, f"Test Case 4 Failed: Input {nums4}, Expected {expected4}, Got {s.gcdSum(nums4)}"

    # Custom Test Case 3: Larger numbers, even length
    nums5 = [12, 18, 24, 30]
    # prefixGcd calculation:
    # i=0: nums[0]=12, mxi=12, gcd(12,12)=12. prefixGcd=[12]
    # i=1: nums[1]=18, mxi=18, gcd(18,18)=18. prefixGcd=[12,18]
    # i=2: nums[2]=24, mxi=24, gcd(24,24)=24. prefixGcd=[12,18,24]
    # i=3: nums[3]=30, mxi=30, gcd(30,30)=30. prefixGcd=[12,18,24,30]
    # Sorted: [12, 18, 24, 30]
    # Pairs:
    # gcd(12, 30) = 6
    # gcd(18, 24) = 6
    # Sum = 6 + 6 = 12
    expected5 = 12
    assert s.gcdSum(nums5) == expected5, f"Test Case 5 Failed: Input {nums5}, Expected {expected5}, Got {s.gcdSum(nums5)}"

    # Custom Test Case 4: Larger numbers, odd length
    nums6 = [10, 20, 15, 25, 5]
    # prefixGcd calculation:
    # i=0: nums[0]=10, mxi=10, gcd(10,10)=10. prefixGcd=[10]
    # i=1: nums[1]=20, mxi=20, gcd(20,20)=20. prefixGcd=[10,20]
    # i=2: nums[2]=15, mxi=20, gcd(15,20)=5. prefixGcd=[10,20,5]
    # i=3: nums[3]=25, mxi=25, gcd(25,25)=25. prefixGcd=[10,20,5,25]
    # i=4: nums[4]=5, mxi=25, gcd(5,25)=5. prefixGcd=[10,20,5,25,5]
    # Sorted: [5, 5, 10, 20, 25]
    # Pairs:
    # gcd(5, 25) = 5
    # gcd(5, 20) = 5
    # Middle element 10 is ignored.
    # Sum = 5 + 5 = 10
    expected6 = 10
    assert s.gcdSum(nums6) == expected6, f"Test Case 6 Failed: Input {nums6}, Expected {expected6}, Got {s.gcdSum(nums6)}"

    print("All tests passed!")