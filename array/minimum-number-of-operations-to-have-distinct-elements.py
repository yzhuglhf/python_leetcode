"""
Minimum Number of Operations to Have Distinct Elements
Difficulty: Medium

Description:
This problem asks for the minimum number of operations to make an array distinct. An operation involves removing the first three elements of the current array (or fewer if less than three remain). We need to count how many such operations are required until the remaining elements are all unique or the array becomes empty.

Example:
Input: nums = [3,8,3,6,5,8]
Output: 1
Explanation: Initially, the array contains duplicates (3 and 8). After one operation, the first three elements ([3,8,3]) are removed, leaving [6,5,8]. These elements are all distinct, so we stop.

Approach:
The problem requires finding the minimum operations by iteratively removing elements from the front of the array and checking for distinctness. A naive approach of slicing the array and creating a new set in each step would lead to O(N^2) time complexity. To optimize, we use a `collections.Counter` to maintain the frequency of elements in the *currently considered* portion of the array. We also track `distinct_multiples`, which is the count of unique numbers that appear more than once. When `distinct_multiples` becomes zero, it means all remaining elements are distinct. In each operation, we update the `Counter` for the three elements being removed (if they exist) and adjust `distinct_multiples` accordingly in O(1) time per element. This leads to an efficient O(N) overall time complexity.

Time Complexity: O(N)
Space Complexity: O(U) where U is the number of unique elements in nums, worst case O(N)
"""
from typing import List, Optional
from collections import Counter

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        
        # Use Counter to store frequencies of all elements in the initial array.
        current_counts = Counter(nums)
        
        # distinct_multiples tracks the number of unique values that appear more than once.
        # If this count is 0, it means all elements in the current effective array are distinct.
        distinct_multiples = 0
        for count in current_counts.values():
            if count > 1:
                distinct_multiples += 1
        
        operations = 0
        # start_idx points to the first element of the current effective array.
        start_idx = 0 
        
        while True:
            # Condition to stop: if there are no unique values appearing more than once,
            # then the current effective array contains only distinct elements (or is empty).
            if distinct_multiples == 0:
                return operations
            
            # Increment operation count as we are about to perform one
            operations += 1
            
            # Simulate removing up to three elements from the beginning of the effective array.
            # The loop runs for elements at indices start_idx, start_idx+1, start_idx+2,
            # ensuring we don't go past the end of the original nums array.
            for i in range(start_idx, min(start_idx + 3, len(nums))):
                num_to_remove = nums[i]
                current_counts[num_to_remove] -= 1
                
                # If an element's count drops to 1, it means it was previously
                # a 'duplicate' (count > 1) and now it is not. So, we decrement
                # distinct_multiples.
                if current_counts[num_to_remove] == 1:
                    distinct_multiples -= 1
                    
            # Advance the start_idx for the next iteration (simulating removal)
            start_idx += 3 

if __name__ == "__main__":
    s = Solution()
    assert s.minOperations([3,8,3,6,5,8]) == 1
    assert s.minOperations([2,2]) == 1
    assert s.minOperations([4,3,5,1,2]) == 0
    assert s.minOperations([1,2,3]) == 0
    assert s.minOperations([]) == 0
    assert s.minOperations([1]) == 0
    assert s.minOperations([1,1,1,1,1,1,1]) == 2
    assert s.minOperations([1,2,1,2,3,4,1,2]) == 2
    assert s.minOperations([1,1]) == 1
    assert s.minOperations([1,1,1]) == 1
    print("All tests passed!")
