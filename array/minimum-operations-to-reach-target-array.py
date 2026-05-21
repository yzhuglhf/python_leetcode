"""
Minimum Operations to Reach Target Array
Difficulty: Medium

Description:
This problem asks for the minimum number of operations to transform an array `nums` into a `target` array of the same length. An operation involves choosing an integer `x`, identifying all maximal contiguous segments where `nums[i] == x`, and for each such segment `[l, r]`, simultaneously updating `nums[i]` to `target[i]` for all `i` from `l` to `r`. The goal is to find the minimum total number of such operations.

Example:
Input: nums = [7,3,7], target = [5,5,9]
Output: 2
Explanation:
1. Choose x = 7: maximal segments [0, 0] and [2, 2] are found (since nums[0]=7 and nums[2]=7).
   nums becomes [target[0], 3, target[2]], which is [5, 3, 9]. (1 operation)
2. Choose x = 3: maximal segment [1, 1] is found (since nums[1]=3).
   nums becomes [5, target[1], 9], which is [5, 5, 9]. (2 operations)
Thus, 2 operations are required.

Approach:
The problem can be efficiently solved by iterating through the arrays from left to right in a single pass. We maintain a `total_operations` count and a `current_active_value`. The `current_active_value` represents the value `x` of the "highest level" operation that is conceptually still active from the previous index and could potentially extend to the current one if the values match.

For each index `i` from `0` to `n-1`:
1.  **Determine the effective value for the current position**: Let `val_to_check` be `nums[i]`. If `nums[i] == target[i]`, this position is already correct. In this case, it acts as a "barrier" or "floor", effectively resetting any active segment from the left. We treat its `val_to_check` as `0` for comparison purposes. If `nums[i] != target[i]`, then `val_to_check` remains `nums[i]`, as this element needs to be changed.
2.  **Compare and increment operations**: If `val_to_check` is strictly greater than `current_active_value`, it implies that a new, higher "layer" or operation is required. We must perform an operation using `x = val_to_check`. This operation will globally affect all maximal segments where `nums[j]` currently equals `val_to_check`. We increment `total_operations` by 1.
3.  **Update `current_active_value`**: The `current_active_value` is then updated to `val_to_check`. This value serves as the `current_active_value` for the next iteration, reflecting the state of the "active layer" or "base value" carried over from the current position.

This approach works because an operation for a value `x` applies globally to all its maximal segments simultaneously. When `val_to_check > current_active_value`, it signifies that we have encountered a `nums[i]` (that needs fixing) which is "higher" than any `x` value that was actively being managed from the immediate left. This higher `nums[i]` necessarily requires a new operation (which covers all `nums[i]` globally). If `val_to_check <= current_active_value`, it means `nums[i]` is either part of the same layer (if `val_to_check == current_active_value`) or a lower layer (if `val_to_check < current_active_value`). In the latter case, the `current_active_value`'s operation segment ends, and `nums[i]` is a new lower segment. Operations for lower values are implicitly handled either earlier (if they were higher than some previous `current_active_value`) or would be initiated when they become a "peak" relative to their left neighbor.

Time Complexity: O(N) because we iterate through the arrays once.
Space Complexity: O(1) as we only use a few integer variables.
"""
from typing import List, Optional

class Solution:
    def minOperations(self, nums: List[int], target: List[int]) -> int:
        total_operations = 0
        # current_active_value represents the value 'x' of the operation that is currently
        # considered "active" or "covering" a contiguous block from the left.
        # It's effectively the highest 'x' value of a block that has propagated to the left.
        current_active_value = 0 

        for i in range(len(nums)):
            # Determine the effective value for the current position.
            # If nums[i] is already equal to target[i], this position is "fixed".
            # It acts as a barrier, resetting any active segment from the left,
            # so we treat its value as 0 for comparison.
            val_to_check = nums[i]
            if nums[i] == target[i]:
                val_to_check = 0
            
            # If the current effective value is greater than the current_active_value,
            # it means we've encountered a new, higher 'layer' that requires an operation.
            # This operation for 'val_to_check' will address all its maximal segments globally.
            if val_to_check > current_active_value:
                total_operations += 1
            
            # Update current_active_value to the effective value of the current position.
            # This value will serve as 'current_active_value' for the next iteration.
            current_active_value = val_to_check
            
        return total_operations

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, 2, 3]
    target1 = [2, 1, 3]
    expected1 = 2
    assert s.minOperations(nums1, target1) == expected1, f"Test 1 failed. Input: {nums1}, {target1}, Expected: {expected1}, Got: {s.minOperations(nums1, target1)}"
    print(f"Test 1 passed: {s.minOperations(nums1, target1)}")

    # Example 2
    nums2 = [4, 1, 4]
    target2 = [5, 1, 4]
    expected2 = 1
    assert s.minOperations(nums2, target2) == expected2, f"Test 2 failed. Input: {nums2}, {target2}, Expected: {expected2}, Got: {s.minOperations(nums2, target2)}"
    print(f"Test 2 passed: {s.minOperations(nums2, target2)}")

    # Example 3
    nums3 = [7, 3, 7]
    target3 = [5, 5, 9]
    expected3 = 2
    assert s.minOperations(nums3, target3) == expected3, f"Test 3 failed. Input: {nums3}, {target3}, Expected: {expected3}, Got: {s.minOperations(nums3, target3)}"
    print(f"Test 3 passed: {s.minOperations(nums3, target3)}")

    # Additional Test Case 1: All elements same and need change
    nums4 = [10, 10, 10]
    target4 = [20, 20, 20]
    expected4 = 1
    assert s.minOperations(nums4, target4) == expected4, f"Test 4 failed. Input: {nums4}, {target4}, Expected: {expected4}, Got: {s.minOperations(nums4, target4)}"
    print(f"Test 4 passed: {s.minOperations(nums4, target4)}")

    # Additional Test Case 2: No elements need change
    nums5 = [1, 2, 3]
    target5 = [1, 2, 3]
    expected5 = 0
    assert s.minOperations(nums5, target5) == expected5, f"Test 5 failed. Input: {nums5}, {target5}, Expected: {expected5}, Got: {s.minOperations(nums5, target5)}"
    print(f"Test 5 passed: {s.minOperations(nums5, target5)}")

    # Additional Test Case 3: Decreasing sequence of values needing change
    nums6 = [5, 4, 3]
    target6 = [1, 2, 1]
    expected6 = 1
    assert s.minOperations(nums6, target6) == expected6, f"Test 6 failed. Input: {nums6}, {target6}, Expected: {expected6}, Got: {s.minOperations(nums6, target6)}"
    print(f"Test 6 passed: {s.minOperations(nums6, target6)}")

    # Additional Test Case 4: Increasing sequence of values needing change
    nums7 = [3, 4, 5]
    target7 = [1, 2, 1]
    expected7 = 3
    assert s.minOperations(nums7, target7) == expected7, f"Test 7 failed. Input: {nums7}, {target7}, Expected: {expected7}, Got: {s.minOperations(nums7, target7)}"
    print(f"Test 7 passed: {s.minOperations(nums7, target7)}")

    # Additional Test Case 5: Complex alternating pattern
    nums8 = [1, 5, 2, 8, 3]
    target8 = [0, 0, 0, 0, 0]
    expected8 = 3 # 1 for x=1, 1 for x=5 (over 1), 1 for x=8 (over 2)
    assert s.minOperations(nums8, target8) == expected8, f"Test 8 failed. Input: {nums8}, {target8}, Expected: {expected8}, Got: {s.minOperations(nums8, target8)}"
    print(f"Test 8 passed: {s.minOperations(nums8, target8)}")

    print("All tests passed!")