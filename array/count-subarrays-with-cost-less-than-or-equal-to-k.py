"""
Count Subarrays With Cost Less Than or Equal to K
Difficulty: Medium

Description:
This problem asks us to count the number of subarrays `nums[l..r]` whose calculated cost is less than or equal to a given integer `k`. The cost of a subarray is defined as `(max(nums[l..r]) - min(nums[l..r])) * (r - l + 1)`.

Example:
Input: nums = [1,3,2], k = 4
Output: 5
Explanation: The valid subarrays are [1] (cost 0), [3] (cost 0), [2] (cost 0), [1,3] (cost 4), and [3,2] (cost 2). All these costs are less than or equal to 4.

Approach:
We employ a two-pointer sliding window technique, where `l` is the left boundary and `r` is the right boundary. For each `r` iterating from `0` to `n-1`, we expand the window to include `nums[r]`. To efficiently determine the maximum and minimum elements within the current window `nums[l..r]` in O(1) time, we maintain two monotonic deques: `max_deque` stores indices of elements in non-increasing order of their values, and `min_deque` stores indices in non-decreasing order. After expanding the window with `nums[r]`, we check the cost of the subarray `nums[l..r]`. If this cost exceeds `k`, we must shrink the window from the left by incrementing `l` and removing any indices no longer within the `[l, r]` range from our deques. This shrinking continues until the cost `(max(nums[l..r]) - min(nums[l..r])) * (r - l + 1)` becomes less than or equal to `k`. Crucially, for a fixed left endpoint `l`, the cost function is monotonically non-decreasing as `r` increases (because `max-min` is non-decreasing and `length` is strictly increasing). Therefore, if `nums[l..r]` satisfies the cost condition, all subarrays `nums[l'..r]` where `l <= l' <= r` also satisfy it. For each valid window `[l, r]` ending at `r`, we add `(r - l + 1)` to our total count.

Time Complexity: O(N)
Space Complexity: O(N)
"""
import collections
from typing import List

class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        total_count = 0
        l = 0  # Left pointer of the sliding window
        
        # Monotonic deques to find min/max in O(1) for the current window [l, r]
        # max_deque stores indices of elements such that nums[indices] is in decreasing order
        # min_deque stores indices of elements such that nums[indices] is in increasing order
        max_deque = collections.deque()
        min_deque = collections.deque()
        
        for r in range(n):
            # 1. Add nums[r] to the window and update deques
            # Maintain max_deque: remove elements smaller than or equal to nums[r] from the right
            while max_deque and nums[max_deque[-1]] <= nums[r]:
                max_deque.pop()
            max_deque.append(r)
            
            # Maintain min_deque: remove elements larger than or equal to nums[r] from the right
            while min_deque and nums[min_deque[-1]] >= nums[r]:
                min_deque.pop()
            min_deque.append(r)
            
            # 2. Shrink window from left (l) if cost exceeds k
            # The inner loop will move 'l' forward until the window [l, r] becomes valid
            while l <= r: 
                current_max = nums[max_deque[0]]
                current_min = nums[min_deque[0]]
                current_length = r - l + 1
                
                # Calculate cost. Python's integers handle arbitrary size, preventing overflow.
                current_cost = (current_max - current_min) * current_length
                
                if current_cost <= k:
                    # Current window [l, r] is valid. Break to count subarrays.
                    break
                else:
                    # Cost is too high, shrink window from left by incrementing 'l'
                    l += 1
                    # Remove elements from deques if their indices are now outside the new window [l, r]
                    if max_deque and max_deque[0] < l:
                        max_deque.popleft()
                    if min_deque and min_deque[0] < l:
                        min_deque.popleft()
            
            # After the inner while loop, the window [l, r] is the largest valid window ending at 'r'.
            # All subarrays nums[l'..r] for l <= l' <= r are also valid because the cost function
            # is monotonically non-decreasing for a fixed 'l' and increasing 'r'.
            # The number of such valid subarrays is (r - l + 1).
            # Note: Since k >= 0 and cost(x,x) = 0 for any single element,
            # 'l' will never exceed 'r', meaning (r - l + 1) will always be at least 1.
            total_count += (r - l + 1)
            
        return total_count

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.countSubarrays(nums = [1,3,2], k = 4) == 5, f"Test Case 1 Failed: Expected 5, Got {s.countSubarrays(nums = [1,3,2], k = 4)}"
    # Example 2
    assert s.countSubarrays(nums = [5,5,5,5], k = 0) == 10, f"Test Case 2 Failed: Expected 10, Got {s.countSubarrays(nums = [5,5,5,5], k = 0)}"
    # Example 3
    assert s.countSubarrays(nums = [1,2,3], k = 0) == 3, f"Test Case 3 Failed: Expected 3, Got {s.countSubarrays(nums = [1,2,3], k = 0)}"
    # Custom test case: single element
    assert s.countSubarrays(nums = [10], k = 100) == 1, f"Test Case 4 Failed: Expected 1, Got {s.countSubarrays(nums = [10], k = 100)}"
    # Custom test case: large k, all valid
    assert s.countSubarrays(nums = [1,2,3,4,5], k = 10**15) == 15, f"Test Case 5 Failed: Expected 15, Got {s.countSubarrays(nums = [1,2,3,4,5], k = 10**15)}"
    # Custom test case: mixed values, small k (only single element subarrays satisfy k=1)
    assert s.countSubarrays(nums = [10,1,10,1], k = 1) == 4, f"Test Case 6 Failed: Expected 4, Got {s.countSubarrays(nums = [10,1,10,1], k = 1)}"

    print("All tests passed!")