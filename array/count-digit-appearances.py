"""
Count Digit Appearances
Difficulty: Medium

Description:
This problem requires counting the total occurrences of a specific digit across all numbers in a given integer array. For each number, its decimal representation is examined to determine how many times the target digit appears, and these individual counts are then summed up.

Example:
Input: nums = [12,54,32,22], digit = 2
Output: 4
Explanation: The digit '2' appears once in 12, zero times in 54, once in 32, and twice in 22, totaling 1 + 0 + 1 + 2 = 4 occurrences.

Approach:
The most straightforward approach involves iterating through each integer in the input array `nums`. For each number, convert it into its string representation. Similarly, convert the target `digit` into its string representation. Then, use the built-in string `count()` method to efficiently determine the number of times the digit-string appears within the number-string. Accumulate these counts in a running total. Finally, return the accumulated total count of the digit's appearances. This method handles all numbers and digits, including single-digit numbers and the digit 0.

Time Complexity: O(N * log10(M)), where N is the length of `nums` and M is the maximum value in `nums`.
For each of the N numbers, converting it to a string and then counting a character takes time proportional to the number of digits in that number, which is approximately log10(M).

Space Complexity: O(log10(M)), where M is the maximum value in `nums`.
This space is primarily used to store the string representation of the current number being processed. Since this space is reused for each number, the overall auxiliary space complexity depends on the maximum number of digits (i.e., the string length for the largest number).
"""
from typing import List, Optional

class Solution:
    def countDigitOccurrences(self, nums: List[int], digit: int) -> int:
        total_occurrences = 0
        s_digit = str(digit) # Convert the target digit to its string representation once

        for num in nums:
            s_num = str(num) # Convert the current number to its string representation
            total_occurrences += s_num.count(s_digit) # Count occurrences and add to total
            
        return total_occurrences

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.countDigitOccurrences(nums = [12,54,32,22], digit = 2) == 4, "Test Case 1 Failed"
    
    # Example 2
    assert s.countDigitOccurrences(nums = [1,34,7], digit = 9) == 0, "Test Case 2 Failed"
    
    # Test with digit 0
    assert s.countDigitOccurrences(nums = [10, 200, 3030, 4], digit = 0) == 5, "Test Case 3 Failed" # 1 in 10, 2 in 200, 2 in 3030, 0 in 4
    
    # Test with all same digits
    assert s.countDigitOccurrences(nums = [777, 7, 177], digit = 7) == 7, "Test Case 4 Failed" # 3 in 777, 1 in 7, 3 in 177
    
    # Test with single number, single digit
    assert s.countDigitOccurrences(nums = [5], digit = 5) == 1, "Test Case 5 Failed"
    
    # Test with no occurrences
    assert s.countDigitOccurrences(nums = [123, 456], digit = 7) == 0, "Test Case 6 Failed"

    # Test with large numbers
    assert s.countDigitOccurrences(nums = [1000000, 500000], digit = 0) == 11, "Test Case 7 Failed" # 6 zeros in 1000000, 5 zeros in 500000

    # Test with empty occurrences for a number
    assert s.countDigitOccurrences(nums = [111, 222, 333], digit = 4) == 0, "Test Case 8 Failed"
    
    print("All tests passed!")