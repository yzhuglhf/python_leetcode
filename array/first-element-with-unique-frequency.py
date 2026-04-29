"""
First Element with Unique Frequency
Difficulty: Medium

Description:
This problem requires finding the first element in an array whose frequency of occurrence is unique compared to all other elements. This means no other number in the array should appear the same number of times as the target element. The search must be done from left to right according to the original array order. If no such element exists, return -1.

Example:
Input: nums = [20,10,30,30]
Output: 30
Explanation: 20 appears once, 10 appears once, 30 appears twice. The frequency of 30 (which is 2) is unique because no other number appears exactly twice.

Approach:
The algorithm proceeds in three main steps. First, calculate the frequency of each number in the input array `nums` using a hash map (`num_frequencies`). This map stores `number -> its_frequency`. Second, calculate the frequency of these frequencies (i.e., how many distinct numbers share a particular frequency) using another hash map (`freq_counts`). This map stores `frequency_value -> count_of_numbers_that_have_this_frequency`. Finally, iterate through the original `nums` array from left to right. For each number, retrieve its frequency from `num_frequencies` and check its count in `freq_counts`. If `freq_counts` indicates that this particular frequency appears only once (meaning `freq_counts[current_freq] == 1`), then the current number is the first element with a unique frequency, and it is returned. If no such element is found after iterating through all numbers, return -1.

Time Complexity: O(N)
The algorithm iterates through `nums` once to build `num_frequencies`, then iterates through `num_frequencies.values()` once to build `freq_counts`, and finally iterates through `nums` once more to find the result. Each step takes O(N) time, where N is the length of `nums`. Thus, the total time complexity is O(N).

Space Complexity: O(N)
Both `num_frequencies` and `freq_counts` can store up to N distinct entries in the worst case (e.g., all numbers are distinct, or all frequencies are distinct). Therefore, the space complexity is O(N).
"""
from typing import List
import collections

class Solution:
    def firstUniqueFreq(self, nums: List[int]) -> int:
        # Step 1: Calculate frequencies of all numbers in nums.
        # num_frequencies: maps number -> its_frequency.
        # Example: [20,10,30,30] -> {20: 1, 10: 1, 30: 2}
        num_frequencies = collections.Counter(nums)

        # Step 2: Calculate frequencies of frequencies.
        # freq_counts: maps frequency_value -> count_of_numbers_that_have_this_frequency.
        # Example from above: frequencies are 1, 1, 2.
        # {1: 2, 2: 1} means frequency '1' appears twice (for 20 and 10),
        # and frequency '2' appears once (for 30).
        freq_counts = collections.Counter(num_frequencies.values())

        # Step 3: Find the first element with a unique frequency.
        # Iterate through the original nums array to maintain the left-to-right order.
        for num in nums:
            current_freq = num_frequencies[num]
            # A frequency is unique if its count in freq_counts is 1.
            # This means only ONE distinct number in nums has this specific frequency.
            if freq_counts[current_freq] == 1:
                return num
        
        # Step 4: If the loop completes, no element with a unique frequency was found.
        return -1

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.firstUniqueFreq(nums = [20,10,30,30]) == 30, "Test Case 1 Failed: [20,10,30,30]"

    # Example 2
    assert s.firstUniqueFreq(nums = [20,20,10,30,30,30]) == 20, "Test Case 2 Failed: [20,20,10,30,30,30]"

    # Example 3
    assert s.firstUniqueFreq(nums = [10,10,20,20]) == -1, "Test Case 3 Failed: [10,10,20,20]"

    # Custom Test Case 1: Single element
    assert s.firstUniqueFreq(nums = [10]) == 10, "Test Case 4 Failed: [10]"

    # Custom Test Case 2: All elements unique (each frequency 1)
    assert s.firstUniqueFreq(nums = [1, 2, 3, 4, 5]) == 1, "Test Case 5 Failed: [1,2,3,4,5]"

    # Custom Test Case 3: Mixed frequencies, first one is unique
    assert s.firstUniqueFreq(nums = [1,1,2,3,3,3]) == 1, "Test Case 6 Failed: [1,1,2,3,3,3]"
    # Explanation: num_freqs={1:2, 2:1, 3:3}, freq_counts={2:1, 1:1, 3:1}. All initial frequencies are unique.
    # 1 appears 2 times. Frequency 2 is unique. First element is 1.

    # Custom Test Case 4: More complex, first element is unique
    assert s.firstUniqueFreq(nums = [1,1,1,2,2,3,4]) == 1, "Test Case 7 Failed: [1,1,1,2,2,3,4]"
    # Explanation: num_freqs={1:3, 2:2, 3:1, 4:1}, freq_counts={3:1, 2:1, 1:2}
    # freq_counts[3] is 1 (for num 1) -> unique. Return 1.

    # Custom Test Case 5: All frequencies non-unique
    assert s.firstUniqueFreq(nums = [1,1,2,2,3,3]) == -1, "Test Case 8 Failed: [1,1,2,2,3,3]"
    # Explanation: num_freqs={1:2, 2:2, 3:2}, freq_counts={2:3}. Frequency 2 is not unique.

    print("All tests passed!")
