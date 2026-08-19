"""
Minimum K to Reduce Array Within Limit
Difficulty: Medium

Description:
This problem asks us to find the smallest positive integer `k` that satisfies a specific condition. The condition requires that the total number of operations, `nonPositive(nums, k)`, needed to make every element in `nums` non-positive by repeatedly subtracting `k` from them, must be less than or equal to `k^2`. For each number `num` in the array, `ceil(num / k)` operations are required.

Example:
Input: nums = [3,7,5]
Output: 3
Explanation: When k = 3, nonPositive(nums, 3) = ceil(3/3) + ceil(7/3) + ceil(5/3) = 1 + 3 + 2 = 6. Since 6 <= 3^2 (which is 9), k=3 is a valid candidate. For k=2, nonPositive(nums, 2) = ceil(3/2) + ceil(7/2) + ceil(5/2) = 2 + 4 + 3 = 9. Since 9 > 2^2 (which is 4), k=2 is not valid. Thus, 3 is the minimum k.

Approach:
The core of the problem lies in finding the minimum `k` such that `sum(ceil(num / k) for num in nums) <= k^2`. Let `f(k) = sum(ceil(num / k))` and `g(k) = k^2`. The function `f(k)` is monotonically non-increasing as `k` increases, because a larger `k` means fewer or the same number of operations per element. The function `g(k)` is monotonically increasing. This characteristic (non-increasing `f(k)` and increasing `g(k)`) makes binary search an efficient approach to find the smallest `k` that satisfies `f(k) <= g(k)`. We define a `check(k)` function that calculates `f(k)` by summing `(num + k - 1) // k` (which is equivalent to `ceil(num / k)` for positive integers) for all `num` in `nums`, and then compares this sum to `g(k) = k^2`. The binary search is performed over a suitable range for `k` (from `1` up to `10^5 + 1`, as `k` will not exceed `max(nums)` which is at most `10^5`). If `check(mid)` returns true, `mid` is a possible answer, so we record it and try a smaller `k` by setting `high = mid - 1`. If `check(mid)` returns false, we need a larger `k`, so we set `low = mid + 1`. The smallest valid `k` found is ultimately returned.

Time Complexity: O(N * log(MAX_K)) where N is the length of `nums` and `MAX_K` is the upper bound for `k` (approximately 10^5). Each `check(k)` operation takes O(N) time, and the binary search performs `log(MAX_K)` iterations.
Space Complexity: O(1) as only a few variables are used during the computation.
"""
from typing import List, Optional

class Solution:
    def minimumK(self, nums: List[int]) -> int:
        
        # Helper function to check if a given k satisfies the condition
        def check(k: int) -> bool:
            operations_needed = 0
            for num in nums:
                # Calculate ceil(num / k) using integer division
                # For positive integers a, b, ceil(a / b) can be calculated as (a + b - 1) // b
                operations_needed += (num + k - 1) // k
            
            # Check if total operations <= k^2
            return operations_needed <= k * k

        # Binary search for the minimum k
        low = 1
        # The maximum possible value for nums[i] is 10^5.
        # If k > max(nums[i]), then operations_needed is simply len(nums).
        # We need len(nums) <= k*k. Since max(len(nums)) is 10^5, k would need to be at least sqrt(10^5) approx 317.
        # This implies k will not exceed max(nums) (which is 10^5) because a k slightly larger than max(nums) would
        # quickly satisfy the condition. Thus, 10^5 + 1 is a safe upper bound for k.
        high = 10**5 + 1
        ans = high # Initialize ans with a value that is guaranteed to be overwritten

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                ans = mid       # mid is a possible answer, try for a smaller k
                high = mid - 1
            else:
                low = mid + 1   # mid is too small, need a larger k
        
        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [3, 7, 5]
    expected1 = 3
    assert s.minimumK(nums1) == expected1, f"Test Case 1 Failed: Input {nums1}, Expected {expected1}, Got {s.minimumK(nums1)}"

    # Example 2
    nums2 = [1]
    expected2 = 1
    assert s.minimumK(nums2) == expected2, f"Test Case 2 Failed: Input {nums2}, Expected {expected2}, Got {s.minimumK(nums2)}"

    # Custom Test Case 1: Large single number
    nums3 = [100000]
    expected3 = 317 
    # For k=316: ops = ceil(100000/316) = 317. k^2 = 316^2 = 99856. 317 > 99856 (False).
    # For k=317: ops = ceil(100000/317) = 316. k^2 = 317^2 = 100489. 316 <= 100489 (True).
    assert s.minimumK(nums3) == expected3, f"Test Case 3 Failed: Input {nums3}, Expected {expected3}, Got {s.minimumK(nums3)}"

    # Custom Test Case 2: Many small numbers
    nums4 = [1] * 10 # [1,1,1,1,1,1,1,1,1,1]
    expected4 = 4 
    # For k=3: ops = 10 * ceil(1/3) = 10. k^2 = 3^2 = 9. 10 > 9 (False).
    # For k=4: ops = 10 * ceil(1/4) = 10. k^2 = 4^2 = 16. 10 <= 16 (True).
    assert s.minimumK(nums4) == expected4, f"Test Case 4 Failed: Input {nums4}, Expected {expected4}, Got {s.minimumK(nums4)}"

    # Custom Test Case 3: Mixed numbers
    nums5 = [10, 20, 30]
    expected5 = 4
    # For k=3: ops = ceil(10/3)+ceil(20/3)+ceil(30/3) = 4+7+10 = 21. k^2=9. 21 > 9 (False).
    # For k=4: ops = ceil(10/4)+ceil(20/4)+ceil(30/4) = 3+5+8 = 16. k^2=16. 16 <= 16 (True).
    assert s.minimumK(nums5) == expected5, f"Test Case 5 Failed: Input {nums5}, Expected {expected5}, Got {s.minimumK(nums5)}"

    # Custom Test Case 4: Larger numbers, requiring a moderate k
    nums6 = [50000, 60000, 70000]
    expected6 = 57
    # For k=56: ops = ceil(50000/56)+ceil(60000/56)+ceil(70000/56) = 893+1072+1250 = 3215. k^2=56^2=3136. 3215 > 3136 (False).
    # For k=57: ops = ceil(50000/57)+ceil(60000/57)+ceil(70000/57) = 878+1053+1229 = 3160. k^2=57^2=3249. 3160 <= 3249 (True).
    assert s.minimumK(nums6) == expected6, f"Test Case 6 Failed: Input {nums6}, Expected {expected6}, Got {s.minimumK(nums6)}"

    print("All tests passed!")
