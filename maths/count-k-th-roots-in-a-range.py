"""
Count K-th Roots in a Range
Difficulty: Medium

Description:
This problem asks us to count the number of perfect k-th powers within a given inclusive range [l, r]. A number y is a perfect k-th power if y = x^k for some integer x. We need to find how many such y exist where l <= y <= r.

Example:
Input: l = 8, r = 30, k = 2
Output: 3
Explanation: The perfect squares in the range [8, 30] are 9 (3^2), 16 (4^2), and 25 (5^2).

Approach:
To find the number of integers y in [l, r] that are perfect k-th powers (y = x^k), we effectively need to find the range of integers x such that l <= x^k <= r. This inequality can be split into two conditions: x^k >= l and x^k <= r. We are looking for integer values of x.

The strategy involves two binary searches:
1.  **Find `x_upper`**: Determine the largest integer `x` such that `x^k <= r`. This `x_upper` represents the maximum base whose k-th power is within or below the upper bound of the given range.
2.  **Find `x_lower`**: Determine the smallest integer `x` such that `x^k >= l`. This `x_lower` represents the minimum base whose k-th power is within or above the lower bound of the given range.

Once `x_lower` and `x_upper` are found, all integers `x` in the range `[x_lower, x_upper]` (inclusive) will yield a perfect k-th power `x^k` that falls within `[l, r]`. The count of such integers `x` is `x_upper - x_lower + 1`. If `x_lower` happens to be greater than `x_upper` (meaning no such `x` exists), the count is 0.

The binary search for `x` will operate on a range from `0` up to a maximum possible value. Since `r` can be up to `10^9` and `k` can be `1`, `x` can be as large as `10^9`. A safe upper bound for binary search is `10^9 + 2`. Python's arbitrary-precision integers handle the calculation of `mid^k` without overflow, even for large `mid` and `k` values.

Time Complexity: O(k * (log(MAX_VAL))^2), where `MAX_VAL` is the maximum possible value for `x` in the binary search (approximately `10^9`). Each binary search runs in O(log(MAX_VAL)) iterations. Inside each iteration, the calculation `mid ** k` for arbitrary-precision integers takes approximately O(k * log(mid)) time. Thus, each binary search contributes O(log(MAX_VAL) * k * log(MAX_VAL)).
Space Complexity: O(1), as only a few variables are used.
"""
from typing import List, Optional

class Solution:
    def countKthRoots(self, l: int, r: int, k: int) -> int:
        
        # Helper function to find the largest integer x such that x^k <= target
        def find_largest_x_le(target: int, k: int) -> int:
            # The maximum possible x is 10^9 (when k=1 and target=10^9).
            # A slightly larger upper bound (e.g., target + 2 or 10^9 + 2) is used for the search space.
            # Using 10^9 + 2 as a consistent, sufficiently large upper bound for x.
            low, high = 0, 10**9 + 2 
            ans = 0 # Initialize with the smallest possible value for x (0)

            while low <= high:
                mid = low + (high - low) // 2
                
                # Calculate mid^k. 0^k for k >= 1 is 0.
                # Python handles large integer powers without overflow.
                val = mid ** k 
                
                if val <= target:
                    # mid^k is within bounds, so mid is a possible answer.
                    # Try to find a larger x in the upper half.
                    ans = mid
                    low = mid + 1
                else:
                    # mid^k exceeds target, so mid is too large.
                    # Search in the lower half.
                    high = mid - 1
            return ans

        # Helper function to find the smallest integer x such that x^k >= target
        def find_smallest_x_ge(target: int, k: int) -> int:
            # Same search space for x as above.
            low, high = 0, 10**9 + 2 
            # Initialize with a value guaranteed to be too high,
            # to ensure any valid mid becomes the answer.
            ans = 10**9 + 2 

            while low <= high:
                mid = low + (high - low) // 2

                # Calculate mid^k.
                val = mid ** k
                
                if val >= target:
                    # mid^k is within bounds, so mid is a possible answer.
                    # Try to find a smaller x in the lower half.
                    ans = mid
                    high = mid - 1
                else:
                    # mid^k is less than target, so mid is too small.
                    # Search in the upper half.
                    low = mid + 1
            return ans

        # Find the largest base x_upper such that x_upper^k <= r
        x_upper = find_largest_x_le(r, k)
        
        # Find the smallest base x_lower such that x_lower^k >= l
        x_lower = find_smallest_x_ge(l, k)

        # The count of perfect k-th powers is the number of integers x in [x_lower, x_upper].
        # If x_lower > x_upper, it means no valid x was found in the range.
        if x_lower > x_upper:
            return 0
        else:
            return x_upper - x_lower + 1

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.countKthRoots(l = 1, r = 9, k = 3) == 2, "Example 1 failed"
    # Example 2
    assert s.countKthRoots(l = 8, r = 30, k = 2) == 3, "Example 2 failed"
    # Custom test: No perfect powers in range
    assert s.countKthRoots(l = 10, r = 15, k = 2) == 0, "Custom test 1 failed"
    # Custom test: Range contains 0
    assert s.countKthRoots(l = 0, r = 0, k = 5) == 1, "Custom test 2 failed"
    # Custom test: Large range, k=1
    assert s.countKthRoots(l = 0, r = 10**9, k = 1) == 10**9 + 1, "Custom test 3 failed"
    # Custom test: High k, no match
    assert s.countKthRoots(l = 10**9, r = 10**9, k = 30) == 0, "Custom test 4 failed"
    # Custom test: Single match in high k
    assert s.countKthRoots(l = 1, r = 1, k = 25) == 1, "Custom test 5 failed"
    print("All tests passed!")