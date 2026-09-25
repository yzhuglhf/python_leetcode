"""
Number of Centered Subarrays
Difficulty: Medium

Description:
This problem asks us to count the number of "centered" subarrays within a given integer array `nums`. A subarray is defined as centered if the sum of its elements is equal to at least one element present within that same subarray. We need to return the total count of such centered subarrays.

Example:
Input: nums = [-1,1,0]
Output: 5
Explanation:
The centered subarrays are:
[-1] (sum -1, contains -1)
[1] (sum 1, contains 1)
[0] (sum 0, contains 0)
[1, 0] (sum 1, contains 1)
[-1, 1, 0] (sum 0, contains 0)

Approach:
The problem can be solved by iterating through all possible subarrays. We use a nested loop structure: the outer loop iterates through all possible starting indices `i`, and the inner loop iterates through all possible ending indices `j` (where `j >= i`). For each subarray `nums[i:j+1]`, we maintain its running sum (`current_sum`) and keep track of all elements encountered so far in that subarray using a hash set (`elements_in_subarray`). As we extend the subarray from `i` to `j`, we add `nums[j]` to `current_sum` and to `elements_in_subarray`. After updating, we check if `current_sum` is present in `elements_in_subarray`. If it is, we increment our total count of centered subarrays. This approach ensures that we check the condition for every valid subarray efficiently.

Time Complexity: O(N^2)
The outer loop runs N times, and the inner loop runs up to N times. Inside the inner loop, sum calculation, set insertion, and set lookup operations take O(1) time on average. Thus, the total time complexity is O(N * N) = O(N^2). Given N <= 500, N^2 = 250,000 operations, which is well within typical time limits.

Space Complexity: O(N)
In the worst case, the hash set `elements_in_subarray` might store up to N distinct elements for a subarray spanning almost the entire input array. Therefore, the space complexity is O(N).
"""
from typing import List, Optional

class Solution:
    def centeredSubarrays(self, nums: List[int]) -> int:
        count = 0
        n = len(nums)

        for i in range(n):
            current_sum = 0
            # A set to store elements of the current subarray nums[i...j]
            # This allows O(1) average time complexity for checking if current_sum
            # is present in the subarray's elements.
            elements_in_subarray = set()
            
            for j in range(i, n):
                # Extend the subarray to include nums[j]
                current_sum += nums[j]
                elements_in_subarray.add(nums[j])
                
                # Check if the sum of the current subarray is one of its elements
                if current_sum in elements_in_subarray:
                    count += 1
        
        return count

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.centeredSubarrays([-1,1,0]) == 5, "Test Case 1 Failed: [-1,1,0]"
    
    # Example 2
    assert s.centeredSubarrays([2,-3]) == 2, "Test Case 2 Failed: [2,-3]"
    
    # Custom Test Case 1: All single-element subarrays, no others
    assert s.centeredSubarrays([1,2,3]) == 3, "Test Case 3 Failed: [1,2,3]"
    
    # Custom Test Case 2: Array with zeros
    assert s.centeredSubarrays([0,0,0]) == 6, "Test Case 4 Failed: [0,0,0]"
    
    # Custom Test Case 3: Single element array
    assert s.centeredSubarrays([10]) == 1, "Test Case 5 Failed: [10]"

    # Custom Test Case 4: Longer array, mixed values
    # Manual check for [1, -1, 1, -1, 0]:
    # i=0: [1] sum 1 (in), [1,-1,1] sum 1 (in), [1,-1,1,-1,0] sum 0 (in) => 3
    # i=1: [-1] sum -1 (in), [-1,1,-1] sum -1 (in), [-1,1,-1,0] sum 0 (in) => 3
    # i=2: [1] sum 1 (in), [1,-1,0] sum 0 (in) => 2
    # i=3: [-1] sum -1 (in), [-1,0] sum -1 (in) => 2
    # i=4: [0] sum 0 (in) => 1
    # Total: 3 + 3 + 2 + 2 + 1 = 11
    assert s.centeredSubarrays([1, -1, 1, -1, 0]) == 11, "Test Case 6 Failed: [1,-1,1,-1,0]"

    print("All tests passed!")