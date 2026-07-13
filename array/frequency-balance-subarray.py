"""
Frequency Balance Subarray
Difficulty: Medium

Description: The problem asks to find the length of the longest "frequency balance subarray" within a given integer array. A subarray is considered frequency balanced if it contains only one distinct value. Otherwise, if it has multiple distinct values, it is balanced if there exists a positive integer `f` such that every distinct value in the subarray occurs either `f` or `2*f` times, and crucially, both frequencies `f` and `2*f` must be present among the distinct values.

Example:
Input: `nums = [1,2,2,1,2,3,3,3]`
Output: `5`
Explanation: The longest frequency balance subarray is `[2, 1, 2, 3, 3]`. In this subarray, the number `1` appears once, and numbers `2` and `3` each appear twice. If we choose `f=1`, then all distinct values occur either `f` (1 time) or `2*f` (2 times). Both frequencies `1` and `2` are present among the distinct values.

Approach:
This problem is solved by iterating through all possible subarrays using a nested loop approach. The outer loop `i` defines the start of the subarray, and the inner loop `j` extends the subarray to its end `nums[i:j+1]`. For each subarray, we maintain two dictionaries: `num_counts` stores the frequency of each distinct number in the current subarray, and `freq_counts` maps frequency values to the count of distinct numbers that occur with that frequency (e.g., `freq_counts[k]` would be the number of distinct elements appearing `k` times). When a new element `nums[j]` is added, `num_counts` is updated, and `freq_counts` is efficiently updated by decrementing the count for the old frequency of `nums[j]` and incrementing the count for its new frequency. After updating, a constant-time check determines if the current subarray satisfies the frequency balance conditions: either it has only one distinct value, or it has exactly two distinct frequency values, one of which is double the other. The maximum length of such a balanced subarray found across all iterations is tracked and returned.

Time Complexity: O(N^2)
Space Complexity: O(N)
"""
import collections
from typing import List, Optional

class Solution:
    def getLength(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # A single element subarray is always frequency balanced (rule 1).
        # So, the minimum possible answer for n >= 1 is 1.
        max_len = 1 

        # Iterate over all possible starting points for a subarray
        for i in range(n):
            # num_counts stores the frequency of each number in the current subarray nums[i...j]
            num_counts = collections.defaultdict(int)
            
            # freq_counts stores {frequency_value: count_of_numbers_having_that_frequency_value}
            # For example, if {1:2, 5:2, 8:3} are num_counts, then freq_counts would be {2:2, 3:1}
            freq_counts = collections.defaultdict(int) 

            # Iterate over all possible ending points for a subarray starting at i
            for j in range(i, n):
                current_num = nums[j]
                
                # Step 1: Update freq_counts based on the old frequency of current_num
                # If current_num was already present, its old frequency needs to be removed from freq_counts
                old_freq = num_counts[current_num]
                if old_freq > 0:
                    freq_counts[old_freq] -= 1
                    # If no other number had this old_freq, remove it from freq_counts
                    if freq_counts[old_freq] == 0:
                        del freq_counts[old_freq]
                
                # Step 2: Update num_counts for current_num
                num_counts[current_num] += 1
                new_freq = num_counts[current_num]
                
                # Step 3: Update freq_counts based on the new frequency of current_num
                freq_counts[new_freq] += 1

                # Step 4: Check if the current subarray nums[i:j+1] is frequency balanced
                
                num_distinct_values = len(num_counts)
                num_distinct_frequencies = len(freq_counts)

                is_current_subarray_balanced = False

                if num_distinct_values == 1:
                    # Rule 1: If the subarray contains only one distinct value, it is frequency balanced.
                    is_current_subarray_balanced = True
                elif num_distinct_values > 1:
                    # Rule 2: Otherwise (more than one distinct value), there must exist a positive integer f such that:
                    #         - Every distinct value in the subarray occurs either f or 2*f times.
                    #         - And both frequencies f and 2*f must occur among the distinct values.

                    if num_distinct_frequencies == 1:
                        # If all distinct values have the same frequency (e.g., [1,1,2,2]), this fails Rule 2
                        # because it requires *both* f and 2*f to occur. Here, only one frequency occurs.
                        is_current_subarray_balanced = False
                    elif num_distinct_frequencies == 2:
                        # There are two distinct frequencies. Check if one is exactly double the other.
                        f1, f2 = list(freq_counts.keys())
                        if (f1 == 2 * f2) or (f2 == 2 * f1):
                            is_current_subarray_balanced = True
                        else:
                            is_current_subarray_balanced = False
                    else: # num_distinct_frequencies > 2
                        # More than two distinct frequencies, which cannot satisfy Rule 2.
                        is_current_subarray_balanced = False
                
                if is_current_subarray_balanced:
                    max_len = max(max_len, j - i + 1)
                    
        return max_len

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.getLength([1,2,2,1,2,3,3,3]) == 5, "Test Case 1 Failed"
    
    # Example 2
    assert s.getLength([5,5,5,5]) == 4, "Test Case 2 Failed"
    
    # Example 3
    assert s.getLength([1,2,3,4]) == 1, "Test Case 3 Failed"
    
    # Additional test cases
    # All distinct elements, only length 1 subarrays are balanced
    assert s.getLength([1,1,2,2]) == 3, "Test Case 4 Failed" # [1,1,2] is balanced (f=1, 2f=2)
    assert s.getLength([1,1,1,2,2,3]) == 3, "Test Case 5 Failed" # [1,1,1] is balanced
    assert s.getLength([1]) == 1, "Test Case 6 Failed" # Single element
    assert s.getLength([1,2,1,2,3]) == 5, "Test Case 7 Failed" # [1,2,1,2,3] is balanced (f=1, 2f=2)
    assert s.getLength([1,2,3,1,2,4,4]) == 7, "Test Case 8 Failed" # [1,2,3,1,2,4,4] is balanced (f=1, 2f=2)

    print("All tests passed!")