"""
Minimum Distance Between Three Equal Elements II
Difficulty: Medium

Description:
This problem asks us to find the minimum "distance" among all "good" tuples (i, j, k) of three distinct indices. A tuple is good if the elements at these indices in the input array `nums` are equal: `nums[i] == nums[j] == nums[k]`. The distance is defined as `abs(i - j) + abs(j - k) + abs(k - i)`. We need to return the minimum distance or -1 if no good tuples exist.

Example:
Input: nums = [1,2,1,1,3]
Output: 6
Explanation: The minimum distance is achieved by the good tuple (0, 2, 3). (0, 2, 3) is a good tuple because nums[0] == nums[2] == nums[3] == 1. Its distance is abs(0 - 2) + abs(2 - 3) + abs(3 - 0) = 2 + 1 + 3 = 6.

Approach:
The core idea is to simplify the distance formula. For any three distinct indices i, j, k, if we sort them as `min_idx < mid_idx < max_idx`, the distance `abs(i - j) + abs(j - k) + abs(k - i)` simplifies to `2 * (max_idx - min_idx)`. This means we need to find three indices of the same value such that the difference between the maximum and minimum index among them is minimized.
The algorithm proceeds as follows:
1. First, we preprocess the input array `nums` to create a hash map (dictionary) where keys are the unique numbers in `nums`, and values are sorted lists of all indices where each number appears.
2. Initialize `min_dist` to a very large value (infinity).
3. Iterate through the lists of indices stored in the hash map. For each list:
    a. If the list contains fewer than three indices, it's impossible to form a good tuple for that number, so we skip it.
    b. If the list has three or more indices, we iterate through it using a sliding window of size three. For each window `[p_a, p_b, p_c]` (where `p_a`, `p_b`, `p_c` are consecutive indices from the sorted list), the potential good tuple `(p_a, p_b, p_c)` gives a distance of `2 * (p_c - p_a)`. We update `min_dist` with the minimum value found. This strategy ensures we minimize `(max_idx - min_idx)` because `p_a` and `p_c` are the minimal and maximal indices in the "closest" possible group of three.
4. Finally, if `min_dist` remains at its initial infinity value, it means no good tuples were found, and we return -1. Otherwise, we return the calculated `min_dist`.

Time Complexity: O(N)
The preprocessing step iterates through `nums` once, taking O(N) time. Populating the dictionary with indices for each number also sums up to O(N) operations. The subsequent iteration through the dictionary and its lists also processes each index from `nums` a constant number of times (at most once as `i_idx` and once as `k_idx`). Thus, the overall time complexity is linear, O(N), where N is the length of `nums`.
Space Complexity: O(N)
The `val_to_indices` dictionary stores all indices from the `nums` array. In the worst case (e.g., all elements are distinct or all elements are the same), it will store N indices, leading to O(N) space complexity.
"""
from typing import List, Optional
import collections

class Solution:
    def minimumDistance(self, nums: List[int]) -> int:
        # Step 1: Create a dictionary to store indices for each number.
        # `collections.defaultdict(list)` is used for convenience: if a key
        # is accessed for the first time, it automatically creates an empty list.
        # Indices are added in increasing order due to the `enumerate` loop.
        val_to_indices = collections.defaultdict(list)
        for i, num in enumerate(nums):
            val_to_indices[num].append(i)

        # Step 2: Initialize minimum distance to a very large value (infinity).
        min_dist = float('inf')

        # Step 3: Iterate through the lists of indices for each unique number.
        for indices_list in val_to_indices.values():
            # If a number appears fewer than 3 times, it's impossible to form a good tuple.
            if len(indices_list) < 3:
                continue
            
            # We need to find three indices (i, j, k) of the same value such that
            # 2 * (max(i,j,k) - min(i,j,k)) is minimized.
            # Since `indices_list` is already sorted, we check consecutive triplets
            # (p_a, p_b, p_c) where p_a = indices_list[x], p_b = indices_list[x+1],
            # p_c = indices_list[x+2]. The distance is 2 * (p_c - p_a).
            for j in range(len(indices_list) - 2):
                i_idx = indices_list[j]      # The smallest index in the triplet
                # indices_list[j+1]          # The middle index, distinct but not explicitly needed for distance calculation
                k_idx = indices_list[j+2]    # The largest index in the triplet
                
                # Calculate the distance for this specific triplet.
                current_dist = 2 * (k_idx - i_idx)
                
                # Update the overall minimum distance found so far.
                min_dist = min(min_dist, current_dist)
        
        # Step 4: After checking all possible triplets, return the result.
        # If `min_dist` is still infinity, it means no good tuples were found.
        return min_dist if min_dist != float('inf') else -1

if __name__ == "__main__":
    s = Solution()
    
    # Example 1: Basic case with a good tuple
    assert s.minimumDistance(nums = [1,2,1,1,3]) == 6, "Example 1 Failed"
    
    # Example 2: Another basic case, multiple values with enough occurrences
    assert s.minimumDistance(nums = [1,1,2,3,2,1,2]) == 8, "Example 2 Failed"
    
    # Example 3: No good tuples
    assert s.minimumDistance(nums = [1]) == -1, "Example 3 Failed"
    
    # Custom Test 1: All elements are the same, check min distance among consecutive triplets
    assert s.minimumDistance(nums = [5,5,5,5,5]) == 4, "Custom Test 1 Failed" # (0,1,2) -> 2*(2-0)=4, (1,2,3) -> 2*(3-1)=4, (2,3,4) -> 2*(4-2)=4
    
    # Custom Test 2: Only one value has enough occurrences, spread out
    assert s.minimumDistance(nums = [1,2,3,1,4,1]) == 10, "Custom Test 2 Failed" # Indices for 1 are [0,3,5], (0,3,5) is the only triplet for 1, 2*(5-0)=10
    
    # Custom Test 3: Multiple values, but none appear 3 or more times
    assert s.minimumDistance(nums = [1,1,2,2]) == -1, "Custom Test 3 Failed"
    
    # Custom Test 4: Multiple good tuples from different values, find the overall minimum
    # For value 10: indices [0,2,4], dist = 2*(4-0) = 8
    # For value 20: indices [1,5,6], dist = 2*(6-1) = 10
    assert s.minimumDistance(nums = [10, 20, 10, 30, 10, 20, 20]) == 8, "Custom Test 4 Failed"
    
    # Custom Test 5: No good tuples for a long array of unique values
    assert s.minimumDistance(nums = [i for i in range(1, 101)]) == -1, "Custom Test 5 Failed"
    
    print("All tests passed!")

