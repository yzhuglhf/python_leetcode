"""
Rotate Non Negative Elements
Difficulty: Medium

Description:
This problem requires rotating only the non-negative elements of an array to the left by k positions, cyclically. Negative elements must remain fixed in their original places. After rotation, the non-negative elements are placed back into the array, filling only the positions that originally contained non-negative values.

Example:
Input: nums = [1,-2,3,-4], k = 3
Output: [3,-2,1,-4]

Approach:
The algorithm first iterates through the input array `nums` to identify all non-negative elements and their original indices. These are stored in two separate lists: `non_negative_values` and `non_negative_indices`. An edge case is handled where if there are zero or one non-negative elements, no effective rotation is possible, so the original array is returned. Otherwise, the `non_negative_values` list is rotated to the left by `k` positions (modulo the count of non-negative elements) using efficient list slicing. Finally, a copy of the original `nums` array is created. The elements from the `rotated_non_negative_values` list are then placed back into this copy at the positions specified by `non_negative_indices`, effectively reconstructing the array with only the non-negative elements rotated.

Time Complexity: O(N)
The initial pass to extract non-negative elements and indices is O(N). List slicing for rotation is O(M) where M is the count of non-negative elements (M <= N). The final pass to place elements back is O(M). Thus, the dominant factor is O(N).

Space Complexity: O(N)
Auxiliary space is used for `non_negative_values` (O(M)), `non_negative_indices` (O(M)), and the `result` array (O(N)). In the worst case, all elements are non-negative (M=N), leading to O(N) space complexity.
"""
from typing import List, Optional

class Solution:
    def rotateElements(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Separate non-negative elements and their original indices.
        non_negative_values = []
        non_negative_indices = []
        for i, num in enumerate(nums):
            if num >= 0:
                non_negative_values.append(num)
                non_negative_indices.append(i)

        # Step 2: Handle edge cases where rotation is not necessary or possible.
        # If there are no non-negative elements or only one, the array remains unchanged
        # because a single element cannot be meaningfully rotated, and an empty list
        # would cause modulo errors.
        if len(non_negative_values) <= 1:
            return nums # No rotation needed or possible for 0 or 1 non-negative elements.

        # Step 3: Perform left rotation on only the non_negative_values.
        n_nn = len(non_negative_values)
        k_effective = k % n_nn # Calculate effective rotation amount
        
        # Perform the actual rotation using slicing
        # This creates a new list by concatenating the tail and head after the split point.
        rotated_non_negative_values = non_negative_values[k_effective:] + non_negative_values[:k_effective]

        # Step 4: Construct the result array by placing rotated non-negative elements
        # back into their original non-negative positions.
        # Create a copy of the original array to preserve negative elements.
        result = list(nums) 
        
        for i in range(n_nn):
            original_idx = non_negative_indices[i]
            result[original_idx] = rotated_non_negative_values[i]
            
        # Step 5: Return the resulting array.
        return result

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, -2, 3, -4]
    k1 = 3
    expected1 = [3, -2, 1, -4]
    assert s.rotateElements(nums1, k1) == expected1, f"Test 1 failed: Input {nums1}, k={k1}, Expected {expected1}, Got {s.rotateElements(nums1, k1)}"

    # Example 2
    nums2 = [-3, -2, 7]
    k2 = 1
    expected2 = [-3, -2, 7]
    assert s.rotateElements(nums2, k2) == expected2, f"Test 2 failed: Input {nums2}, k={k2}, Expected {expected2}, Got {s.rotateElements(nums2, k2)}"

    # Example 3
    nums3 = [5, 4, -9, 6]
    k3 = 2
    expected3 = [6, 5, -9, 4]
    assert s.rotateElements(nums3, k3) == expected3, f"Test 3 failed: Input {nums3}, k={k3}, Expected {expected3}, Got {s.rotateElements(nums3, k3)}"

    # Additional Test Cases:

    # All non-negative elements
    nums4 = [1, 2, 3, 4, 5]
    k4 = 2
    expected4 = [3, 4, 5, 1, 2] 
    assert s.rotateElements(nums4, k4) == expected4, f"Test 4 failed: Input {nums4}, k={k4}, Expected {expected4}, Got {s.rotateElements(nums4, k4)}"

    # All negative elements
    nums5 = [-1, -2, -3, -4]
    k5 = 5
    expected5 = [-1, -2, -3, -4] # No non-negative elements to rotate
    assert s.rotateElements(nums5, k5) == expected5, f"Test 5 failed: Input {nums5}, k={k5}, Expected {expected5}, Got {s.rotateElements(nums5, k5)}"

    # Mixed elements, k > length of non-negative elements
    nums6 = [10, -1, 20, -2, 30] # Non-negative: [10, 20, 30]
    k6 = 7 # k_effective = 7 % 3 = 1. [10,20,30] -> [20,30,10]
    expected6 = [20, -1, 30, -2, 10]
    assert s.rotateElements(nums6, k6) == expected6, f"Test 6 failed: Input {nums6}, k={k6}, Expected {expected6}, Got {s.rotateElements(nums6, k6)}"

    # Array with a single non-negative element
    nums7 = [-5, 10, -2, -8] # Non-negative: [10]
    k7 = 100 # A single element rotated by any amount remains itself
    expected7 = [-5, 10, -2, -8] 
    assert s.rotateElements(nums7, k7) == expected7, f"Test 7 failed: Input {nums7}, k={k7}, Expected {expected7}, Got {s.rotateElements(nums7, k7)}"

    # Array with all zeros (zeros are non-negative)
    nums9 = [0, 0, 0, 0]
    k9 = 1
    expected9 = [0, 0, 0, 0] # [0,0,0,0] rotated by 1 -> [0,0,0,0]
    assert s.rotateElements(nums9, k9) == expected9, f"Test 9 failed: Input {nums9}, k={k9}, Expected {expected9}, Got {s.rotateElements(nums9, k9)}"
    
    # Array with mixed non-negative elements, including zero
    nums10 = [0, 1, 2]
    k10 = 1
    expected10 = [1, 2, 0] # [0,1,2] rotated by 1 -> [1,2,0]
    assert s.rotateElements(nums10, k10) == expected10, f"Test 10 failed: Input {nums10}, k={k10}, Expected {expected10}, Got {s.rotateElements(nums10, k10)}"

    print("All tests passed!")

