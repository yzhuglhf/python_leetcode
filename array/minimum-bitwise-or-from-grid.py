"""
Minimum Bitwise OR From Grid
Difficulty: Medium

Description:
Given a 2D integer array `grid`, we must select exactly one integer from each row. The goal is to find the minimum possible bitwise OR of these selected integers. The problem asks for the smallest possible value `X` such that there exists a selection of numbers, one from each row, whose bitwise OR equals `X`.

Example:
Input: grid = [[1,5],[2,4]]
Output: 3
Explanation: Choosing 1 from the first row and 2 from the second row gives a bitwise OR of 1 | 2 = 3. This is the minimum possible OR value.

Approach:
This problem can be solved using binary search on the answer. We are looking for the minimum integer `X` that can be formed as a bitwise OR of one selected number from each row. The range for `X` is from 0 up to the maximum possible value (which is slightly above 10^5, specifically 2^17 - 1, since the maximum grid value is 10^5).

We define a helper function `check(target_OR)` which determines if it's possible to achieve a total bitwise OR that is less than or equal to `target_OR`. This function returns `True` if for every row, we can find at least one number `val` such that `(val | target_OR) == target_OR`. This condition means that `val` must be a bitwise submask of `target_OR` (i.e., all bits set in `val` must also be set in `target_OR`). If such a `val` can be found for every row, then we can construct an overall OR value `Y` such that `Y <= target_OR`. If any row does not contain such a `val`, then `check(target_OR)` returns `False`.

The binary search proceeds by initializing `low = 0` and `high = 2^17 - 1`. We maintain an `ans` variable, initially `high`. In each step, we calculate `mid = low + (high - low) // 2`. If `check(mid)` is `True`, it means `mid` (or something smaller) is a possible answer, so we update `ans = mid` and try to find an even smaller `target_OR` by setting `high = mid - 1`. If `check(mid)` is `False`, it means `mid` is too small to be a possible OR value, so we must look for a larger `target_OR` by setting `low = mid + 1`. The binary search continues until `low > high`, at which point `ans` will hold the minimum possible bitwise OR value.

Time Complexity: O(M * N * log(MAX_GRID_VAL))
The `check` function iterates through `M` rows and up to `N` elements per row, resulting in O(M * N) operations. The binary search performs `log(MAX_GRID_VAL)` iterations. Given `M * N <= 10^5` and `MAX_GRID_VAL <= 10^5` (so `log(MAX_GRID_VAL)` is approximately 17), the total time complexity is roughly `10^5 * 17`, which is efficient enough.

Space Complexity: O(1)
The space complexity is constant, as we only use a few variables for the binary search and the `check` function does not require additional data structures proportional to input size.
"""
from typing import List, Optional

class Solution:
    def minimumOR(self, grid: List[List[int]]) -> int:
        
        # Helper function to check if a target_OR is achievable or surpassable.
        # It returns True if there exists a selection of numbers (one from each row)
        # whose bitwise OR is less than or equal to target_OR.
        # This is equivalent to checking if for every row, we can select a number 'val'
        # such that 'val' is a bitwise submask of 'target_OR' (i.e., (val | target_OR) == target_OR).
        def check(target_OR: int) -> bool:
            for row in grid:
                found_valid_val_in_row = False
                for val in row:
                    # If val is a bitwise submask of target_OR, it means val does not set
                    # any bits that are not already set in target_OR.
                    # This implies that if we select such a 'val', it will not
                    # contribute to making the final OR result larger than target_OR
                    # (in terms of new bits being set).
                    if (val | target_OR) == target_OR:
                        found_valid_val_in_row = True
                        break
                if not found_valid_val_in_row:
                    return False
            return True

        # The maximum possible value for any element in the grid is 10^5.
        # 2^16 = 65536
        # 2^17 = 131072
        # So, the maximum possible OR value (if all bits up to 16 are set) is 2^17 - 1.
        # We use this as the upper bound for our binary search.
        max_possible_OR_value = (1 << 17) - 1 # 131071

        low = 0
        high = max_possible_OR_value
        ans = max_possible_OR_value # Initialize with the largest possible answer

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                # If mid is achievable, it could be our answer.
                # Try to find an even smaller answer in the left half.
                ans = mid
                high = mid - 1
            else:
                # If mid is not achievable, we need a larger target_OR.
                # Search in the right half.
                low = mid + 1
        
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.minimumOR([[1,5],[2,4]]) == 3, "Example 1 failed"
    
    # Example 2
    assert s.minimumOR([[3,5],[6,4]]) == 5, "Example 2 failed"
    
    # Example 3
    assert s.minimumOR([[7,9,8]]) == 7, "Example 3 failed"

    # Custom test case: single row, single column
    assert s.minimumOR([[100]]) == 100, "Single element grid failed"

    # Custom test case: multiple rows, single column
    assert s.minimumOR([[1],[2],[3]]) == 3, "Multiple rows, single column failed"

    # Custom test case: all numbers same (trivial)
    assert s.minimumOR([[5,5],[5,5]]) == 5, "All same numbers failed"

    # Custom test case: larger numbers, check max_possible_OR_value
    assert s.minimumOR([[100000],[99999]]) == 100031, "Large numbers failed"
    
    # Custom test case: a more complex grid with a non-obvious minimum
    assert s.minimumOR([[1,2,3],[4,5,6],[7,8,9]]) == 7, "Complex grid failed"

    print("All tests passed!")