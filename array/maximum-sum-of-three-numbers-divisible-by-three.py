"""
Maximum Sum of Three Numbers Divisible by Three
Difficulty: Medium

Description:
Given an array of integers `nums`, the goal is to find the maximum possible sum of exactly three numbers from `nums` such that their sum is divisible by three. If no such triplet exists, the function should return 0. All numbers in the input array are positive.

Example:
Input: nums = [4,2,3,1]
Output: 9

Approach:
The problem constraints dictate choosing exactly three numbers whose sum is divisible by three. This means the sum of their remainders when divided by three must also be divisible by three. We categorize all numbers in `nums` into three lists: `rem0` (numbers divisible by 3), `rem1` (numbers with remainder 1), and `rem2` (numbers with remainder 2). Each list is then sorted in descending order to easily access the largest numbers. There are only four unique combinations of remainders for three numbers that sum to a multiple of three: (0,0,0), (1,1,1), (2,2,2), and (0,1,2). We check the maximum sum for each of these four cases by picking the largest available numbers from the respective sorted lists. The highest sum found across all valid cases is the result, defaulting to 0 if no such triplet can be formed.

Time Complexity: O(N log N) due to sorting the numbers categorized by their remainders. In the worst case, all numbers could fall into one category, requiring sorting of N elements.
Space Complexity: O(N) to store the numbers in three separate lists based on their remainders.
"""
from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        rem0 = [] # Numbers with remainder 0 when divided by 3
        rem1 = [] # Numbers with remainder 1 when divided by 3
        rem2 = [] # Numbers with remainder 2 when divided by 3

        # Categorize numbers based on their remainder modulo 3
        for num in nums:
            remainder = num % 3
            if remainder == 0:
                rem0.append(num)
            elif remainder == 1:
                rem1.append(num)
            else: # remainder == 2
                rem2.append(num)
        
        # Sort lists in descending order to easily pick the largest numbers
        rem0.sort(reverse=True)
        rem1.sort(reverse=True)
        rem2.sort(reverse=True)

        max_sum = 0

        # Case 1: Pick three numbers with remainder 0 (0 + 0 + 0) % 3 == 0
        if len(rem0) >= 3:
            current_sum = rem0[0] + rem0[1] + rem0[2]
            max_sum = max(max_sum, current_sum)
        
        # Case 2: Pick three numbers with remainder 1 (1 + 1 + 1) % 3 == 0
        if len(rem1) >= 3:
            current_sum = rem1[0] + rem1[1] + rem1[2]
            max_sum = max(max_sum, current_sum)
        
        # Case 3: Pick three numbers with remainder 2 (2 + 2 + 2) % 3 == 0
        if len(rem2) >= 3:
            current_sum = rem2[0] + rem2[1] + rem2[2]
            max_sum = max(max_sum, current_sum)
        
        # Case 4: Pick one number with remainder 0, one with remainder 1, and one with remainder 2 (0 + 1 + 2) % 3 == 0
        if len(rem0) >= 1 and len(rem1) >= 1 and len(rem2) >= 1:
            current_sum = rem0[0] + rem1[0] + rem2[0]
            max_sum = max(max_sum, current_sum)
        
        return max_sum

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.maximumSum([4,2,3,1]) == 9, "Test Case 1 Failed: Example 1"
    # Example 2
    assert s.maximumSum([2,1,5]) == 0, "Test Case 2 Failed: Example 2"
    
    # Additional test cases
    assert s.maximumSum([1,1,1,1]) == 3, "Test Case 3 Failed: All R1s"
    assert s.maximumSum([3,6,9]) == 18, "Test Case 4 Failed: All R0s"
    assert s.maximumSum([2,5,8,1,4,7]) == 15, "Test Case 5 Failed: Max from R1s or R2s"
    assert s.maximumSum([10,20,30,1,2]) == 60, "Test Case 6 Failed: (0,0,0) with large numbers"
    assert s.maximumSum([1,2,3,4,5,6,7,8,9,10]) == 27, "Test Case 7 Failed: Mixed large list" # (10,8,9) sum 27
    assert s.maximumSum([1,1,2,2]) == 0, "Test Case 8 Failed: No triplet possible"
    assert s.maximumSum([1,1,1]) == 3, "Test Case 9 Failed: Minimum length array"
    assert s.maximumSum([100000, 100000, 100000]) == 300000, "Test Case 10 Failed: Max values"

    print("All tests passed!")