"""
Count Subarrays With Even Odd Ratio II
Difficulty: Hard

Description:
This problem asks us to count valid subarrays where the ratio of even elements (x) to odd elements (y) satisfies x/y <= a/b, given that y > 0. The core idea is to transform the ratio condition x/y <= a/b into x*b - a*y <= 0, which also implicitly satisfies y > 0, simplifying the problem to counting subarrays with non-positive "weighted sums". We convert the input array `nums` into a `vals` array, where even numbers map to `b` and odd numbers map to `-a`.

Example:
Input: nums = [1,2,1,2], a = 3, b = 2
Output: 7
Explanation: For the subarray [1,2], x=1, y=1. The ratio 1/1 is less than or equal to 3/2, so it's valid. The problem states there are 7 such subarrays in total.

Approach:
The problem's condition `y > 0` and `x / y <= a / b` can be rewritten. Since `y > 0` and `b > 0` (from constraints), we can cross-multiply to get `x * b <= a * y`. Rearranging this gives `x * b - a * y <= 0`. A crucial simplification is that this inequality `x * b - a * y <= 0` *automatically implies* `y > 0`. If `y` were 0, then all elements in the subarray would be even, meaning `x` equals the subarray's length (`length >= 1`). The inequality would become `length * b <= 0`, which is impossible since `length >= 1` and `b >= 1`. Thus, we only need to count subarrays that satisfy `x * b - a * y <= 0`.

To compute `x * b - a * y` efficiently for any subarray, we transform the original `nums` array into a `vals` array: `vals[i] = b` if `nums[i]` is even, and `vals[i] = -a` if `nums[i]` is odd. Then, the sum of `vals` for a subarray `nums[i..j]` is exactly `x * b - a * y`.
The problem now reduces to counting subarrays `vals[i..j]` whose sum is less than or equal to 0. This is a classic problem solvable using prefix sums and a Fenwick Tree (BIT).
1.  Compute prefix sums `P` for the `vals` array, where `P[k]` is the sum of `vals[0]` through `vals[k-1]`, and `P[0] = 0`. The sum of `vals[i..j]` is `P[j+1] - P[i]`.
2.  We need to count pairs `(i, j)` with `0 <= i <= j < n` such that `P[j+1] - P[i] <= 0`, which is `P[i] >= P[j+1]`.
3.  Since prefix sums can be very large or small, we use coordinate compression. Collect all unique values from `P`, sort them, and map each value to a 1-based rank (index).
4.  Initialize a Fenwick Tree (BIT) with the size equal to the number of unique prefix sums.
5.  Initialize `ans = 0`. Add the rank of `P[0]` to the BIT.
6.  Iterate `j` from `0` to `n-1`:
    a.  Let `current_prefix_sum = P[j+1]`. Get its rank `current_rank`.
    b.  Query the BIT to find how many prefix sums `P[k]` (where `k <= j`) that have been added to the BIT have a rank greater than or equal to `current_rank`. This count gives us the number of `i` values that satisfy `P[i] >= P[j+1]`. Add this count to `ans`.
    c.  Add `current_rank` to the BIT to include `P[j+1]` for future queries (as a potential `P[i]`).
7.  Return `ans`.

Time Complexity: O(N log N). This arises from O(N) for generating `vals` and prefix sums, O(N log N) for coordinate compression (collecting unique values and sorting), and O(N log M) for the `N` BIT operations (each taking `O(log M)` time, where `M` is the number of unique prefix sums, `M <= N+1`).
Space Complexity: O(N) for storing the `vals` array, `prefix_sums` array, `unique_prefix_sums` list, `rank_map`, and the Fenwick Tree.
"""
from typing import List
import bisect

class FenwickTree:
    def __init__(self, size):
        # The tree array is 1-indexed. size is the maximum rank.
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index: int, delta: int):
        # Adds delta to the element at `index`.
        # `index` must be 1-based.
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index: int) -> int:
        # Returns the sum of elements from 1 to `index` (inclusive).
        # `index` must be 1-based.
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & (-index)
        return s

    def query_suffix(self, start_index: int) -> int:
        # Returns the sum of elements from `start_index` to `self.size` (inclusive).
        # `start_index` must be 1-based.
        # This is calculated as (total sum up to self.size) - (sum up to start_index - 1).
        return self.query(self.size) - self.query(start_index - 1)

class Solution:
    def countRatioSubarrays(self, nums: List[int], a: int, b: int) -> int:
        n = len(nums)
        
        # Step 1: Transform nums into vals based on even/odd and a/b ratio
        # vals[i] = b if nums[i] is even, -a if nums[i] is odd
        vals = []
        for num in nums:
            if num % 2 == 0:  # Even
                vals.append(b)
            else:  # Odd
                vals.append(-a)
        
        # Step 2: Calculate prefix sums of vals
        # P[k] = sum(vals[0..k-1]), P[0]=0.
        # Sum of vals[i..j] = P[j+1] - P[i]. We need P[j+1] - P[i] <= 0  =>  P[i] >= P[j+1].
        prefix_sums = [0] * (n + 1)
        for i in range(n):
            prefix_sums[i+1] = prefix_sums[i] + vals[i]
            
        # Step 3: Coordinate compression for prefix sums
        # Get all unique prefix sum values, sort them, and map to 1-based ranks.
        unique_prefix_sums = sorted(list(set(prefix_sums)))
        
        # We can use bisect_left to find ranks on the fly, which avoids creating a large dictionary
        # if the number of unique elements is close to N.
        # rank_map = {val: i + 1 for i, val in enumerate(unique_prefix_sums)}
        
        # Step 4: Use Fenwick Tree (BIT)
        ft = FenwickTree(len(unique_prefix_sums))
        ans = 0
        
        # Add P[0] to the BIT. P[0] is the prefix sum for the empty prefix.
        # It serves as the P[i] for subarrays starting at index 0.
        # `bisect_left(list, value)` returns the index where value can be inserted to maintain order.
        # Add 1 to make it 1-based rank for Fenwick Tree.
        initial_rank = bisect.bisect_left(unique_prefix_sums, prefix_sums[0]) + 1
        ft.update(initial_rank, 1)
        
        for j in range(n):
            # current_prefix_sum is P[j+1], which represents the sum of vals[0...j].
            current_prefix_sum = prefix_sums[j+1]
            current_rank = bisect.bisect_left(unique_prefix_sums, current_prefix_sum) + 1
            
            # Query the BIT for elements with rank >= current_rank.
            # These are the P[i] values (for i <= j) such that P[i] >= P[j+1].
            ans += ft.query_suffix(current_rank)
            
            # Add the current prefix sum P[j+1] (its rank) to the BIT for future queries.
            ft.update(current_rank, 1)
            
        return ans

