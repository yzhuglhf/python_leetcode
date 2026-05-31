"""
Count Elements With at Least K Greater Values
Difficulty: Medium

Description:
This problem asks us to count elements in an array `nums` that are "qualified." An element is qualified if there are at least `k` other elements in the array strictly greater than it. We need to return the total count of such qualified elements.

Example:
Input: nums = [3,1,2], k = 1
Output: 2
Explanation: After sorting, nums is [1,2,3]. The element `1` has two greater values (2, 3), and `2` has one greater value (3). Both satisfy `at least k=1` greater values. The element `3` has no greater values. Thus, 2 elements are qualified.

Approach:
The most efficient approach involves sorting the array first. After sorting `nums` in ascending order, we observe a crucial property: an element `x` is qualified if and only if it is strictly less than the element at index `n - k` in the sorted array (where `n` is the length of `nums`). This is because any element `x` smaller than `nums[n-k]` will have at least `k` elements (specifically, `nums[n-k]` through `nums[n-1]`) that are strictly greater than it. Conversely, any element `x` greater than or equal to `nums[n-k]` will have fewer than `k` elements strictly greater than it. With this understanding, we sort the array, handle the `k=0` edge case by returning `n` (as all elements are qualified), then determine the `threshold_val = nums[n-k]`. Finally, we count all elements in the sorted array that are strictly less than `threshold_val` using `bisect_left`, which gives us the total number of qualified elements.

Time Complexity: O(N log N) due to the sorting step. The `bisect_left` operation takes O(log N), which is dominated by the sort.
Space Complexity: O(log N) for the auxiliary space used by Python's Timsort algorithm (in-place sort). If a copy of the list were made, it would be O(N).
"""
import bisect
from typing import List, Optional # Optional not strictly necessary for this problem, but kept for consistency with LeetCode's boilerplate.

class Solution:
    def countElements(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Edge case: If k is 0, any element trivially has at least 0 elements greater than it.
        # Thus, all n elements in the array are qualified.
        if k == 0:
            return n

        # Step 1: Sort the array in ascending order.
        # This operation takes O(N log N) time.
        nums.sort()

        # Step 2: Determine the threshold value.
        # An element 'x' is qualified if and only if it is strictly less than `nums[n - k]`.
        # Let `threshold_val = nums[n - k]`.
        #
        # Proof sketch:
        # - If `x < nums[n - k]`: All elements from `nums[n - k]` to `nums[n - 1]` (inclusive) are >= `nums[n - k]`.
        #   There are `n - (n - k) = k` such elements. Since `x < nums[n - k]`, all these `k` elements are strictly greater than `x`.
        #   Thus, `x` is qualified.
        # - If `x >= nums[n - k]`: The count of elements strictly greater than `x` is `n - bisect_right(nums, x)`.
        #   Since `x >= nums[n - k]`, `bisect_right(nums, x)` will return an index `p` such that `p > n - k` (or `p = n-k` if all elements `nums[n-k]...nums[n-1]` are strictly greater than `x` and `x` is smaller than `nums[n-k]`, which contradicts `x >= nums[n-k]`).
        #   More precisely, if `x >= nums[n-k]`, then `bisect_right(nums, x)` must be an index `p >= n-k+1` (because `nums[n-k]` itself is not strictly greater than `x`).
        #   Thus, `n - p <= n - (n - k + 1) = k - 1`. This means `x` has strictly fewer than `k` elements greater than it, so it is not qualified.
        #
        # The index `n - k` is valid because `0 <= k < n`, implying `1 <= n - k <= n - 1`.
        threshold_val = nums[n - k]

        # Step 3: Count elements strictly less than `threshold_val`.
        # `bisect_left(nums, value)` returns the insertion point for `value` in `nums`
        # that maintains sorted order. All elements before this index are strictly less than `value`.
        # This count represents the total number of qualified elements.
        qualified_count = bisect.bisect_left(nums, threshold_val)

        return qualified_count

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.countElements(nums = [3,1,2], k = 1) == 2, "Example 1 Failed"

    # Example 2
    assert s.countElements(nums = [5,5,5], k = 2) == 0, "Example 2 Failed"

    # Test case k=0
    assert s.countElements(nums = [1,2,3,4,5], k = 0) == 5, "Test k=0 Failed"
    assert s.countElements(nums = [1], k = 0) == 1, "Test k=0 with single element Failed"

    # Test case with duplicates and various k
    assert s.countElements(nums = [1,2,2,3,4], k = 1) == 4, "Test with duplicates k=1 Failed" # 1,2,2,3 are qualified (<4)
    assert s.countElements(nums = [1,2,2,3,4], k = 2) == 3, "Test with duplicates k=2 Failed" # 1,2,2 are qualified (<3)
    assert s.countElements(nums = [1,2,2,3,4], k = 3) == 1, "Test with duplicates k=3 Failed" # 1 is qualified (<2)
    assert s.countElements(nums = [1,2,2,3,4], k = 4) == 0, "Test with duplicates k=4 Failed" # None qualified (<1)

    # Test with all elements same
    assert s.countElements(nums = [7,7,7,7], k = 1) == 0, "Test all same k=1 Failed"
    assert s.countElements(nums = [7,7,7,7], k = 3) == 0, "Test all same k=3 Failed"

    # Larger array with distinct elements
    assert s.countElements(nums = [10, 20, 30, 40, 50], k = 1) == 4, "Large distinct k=1 Failed" # <50
    assert s.countElements(nums = [10, 20, 30, 40, 50], k = 2) == 3, "Large distinct k=2 Failed" # <40
    assert s.countElements(nums = [10, 20, 30, 40, 50], k = 4) == 1, "Large distinct k=4 Failed" # <20

    print("All tests passed!")