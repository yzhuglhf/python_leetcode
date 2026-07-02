"""
Minimum Cost to Partition a Binary String
Difficulty: Hard

Description:
This problem asks for the minimum cost to partition a binary string 's' into segments. The partitioning process begins with the entire string as a single segment. A segment of even length can optionally be split into two contiguous segments of equal length. The cost for a segment of length 'L' containing 'X' sensitive elements ('1's) is `flatCost` if X=0, or `L * X * encCost` if X>0. The objective is to find the minimum total cost, which is the sum of costs of the final, unsplit segments, over all valid partitioning strategies.

Example:
Input: s = "1010", encCost = 2, flatCost = 1
Output: 6
Explanation: The entire string "1010" (length 4, 2 sensitive elements) can be kept as a single segment for a cost of 4 * 2 * 2 = 16. Alternatively, since its length is even, it can be split into "10" and "10".
For each "10" segment (length 2, 1 sensitive element): it can be kept as is for a cost of 2 * 1 * 2 = 4. Or, since its length is even, it can be split into "1" and "0".
- The "1" segment (length 1, 1 sensitive) costs 1 * 1 * 2 = 2.
- The "0" segment (length 1, 0 sensitive) costs flatCost = 1.
So, the minimum cost for a "10" segment is min(4, 2 + 1) = 3.
If "1010" is split into two "10" segments, the total cost would be 3 + 3 = 6. Since 6 < 16, splitting "1010" is preferred. The minimum possible total cost is 6.

Approach:
This problem can be solved using dynamic programming with memoization. We define a recursive function `get_segment_cost(start, end)` that computes the minimum cost for the substring `s[start...end]`.

1.  **Prefix Sums for Sensitive Elements**: To efficiently count '1's in any given segment `s[start...end]`, we precompute a `prefix_ones` array. `prefix_ones[k]` stores the count of '1's in `s[0...k-1]`. The count for `s[start...end]` can then be calculated as `prefix_ones[end+1] - prefix_ones[start]` in O(1) time.

2.  **Recursive Cost Calculation `get_segment_cost(start, end)`**:
    *   **Base Cost (No Split)**: Calculate the cost if the segment `s[start...end]` is kept as a single, unsplit entity. Let `L` be its length and `X` be its count of sensitive elements. The `cost_no_split` is `flatCost` if `X=0`, otherwise `L * X * encCost`.
    *   **Split Option**: If `L` is an even number, the segment can optionally be split into two contiguous segments of equal length: `s[start ... start + L/2 - 1]` and `s[start + L/2 ... end]`. The cost of splitting is `cost_if_split = get_segment_cost(start, start + L/2 - 1) + get_segment_cost(start + L/2, end)`. This involves recursive calls to compute the minimum costs for the sub-segments.
    *   **Minimum Cost**: The minimum cost for `s[start...end]` is `min(cost_no_split, cost_if_split)` (if `L` is even) or just `cost_no_split` (if `L` is odd, as no splitting is possible).

3.  **Memoization**: The `functools.lru_cache` decorator is used to memoize the results of `get_segment_cost`. This prevents redundant computations for overlapping subproblems. The specific splitting rule (halving an even-length segment) ensures that the set of distinct `(start, end)` segments visited by the recursive calls, starting from `get_segment_cost(0, n-1)`, is bounded. For a segment `s[start...end]` of length `L`, if it's derived from the main string `s[0...n-1]` through this splitting process, its `start` index must be a multiple of `L` and `end+1` must also be a multiple of `L`. The total number of such segments `(start, end)` for a string of length `N` is `O(N log N)`.

4.  **Final Answer**: The problem asks for the minimum possible total cost over all valid partitions. This is equivalent to finding the minimum cost for the entire string `s[0...n-1]`, considering all recursive splitting options. Therefore, the result is `get_segment_cost(0, n-1)`.

Time Complexity: O(N log N)
The `prefix_ones` array takes O(N) time. The `get_segment_cost` function is called for O(N log N) distinct `(start, end)` states. Each call performs O(1) work (after recursive calls are resolved by memoization). Thus, the total time complexity is O(N log N).

Space Complexity: O(N log N)
The `prefix_ones` array takes O(N) space. The `lru_cache` stores results for O(N log N) states, each taking O(1) space. Thus, the total space complexity is O(N log N).
"""
from typing import List
from functools import lru_cache

class Solution:
    def minCost(self, s: str, encCost: int, flatCost: int) -> int:
        n = len(s)

        # Precompute prefix sums of '1's
        # prefix_ones[k] stores the count of '1's in s[0...k-1]
        prefix_ones = [0] * (n + 1)
        for i in range(n):
            prefix_ones[i+1] = prefix_ones[i] + (1 if s[i] == '1' else 0)

        # Memoization for min_cost_segment(start, end)
        # @lru_cache(None) decorator caches function results based on arguments.
        # This helps in avoiding redundant computations for overlapping subproblems.
        @lru_cache(None)
        def get_segment_cost(start: int, end: int) -> int:
            length = end - start + 1
            
            # Calculate number of sensitive elements ('1's) in s[start...end]
            num_sensitive = prefix_ones[end+1] - prefix_ones[start]

            # Calculate the cost if this segment is NOT split further
            # If there are no sensitive elements, the cost is flatCost.
            # Otherwise, it's L * X * encCost.
            current_cost = flatCost
            if num_sensitive > 0:
                current_cost = length * num_sensitive * encCost
            
            # If the segment has an even length, we consider the option of splitting it
            if length % 2 == 0:
                mid_point = start + length // 2
                
                # Calculate the cost if the segment is split into two equal halves.
                # This involves recursively finding the minimum cost for each sub-segment.
                cost_if_split = get_segment_cost(start, mid_point - 1) + \
                                get_segment_cost(mid_point, end)
                
                # The minimum cost for the current segment is the minimum of not splitting
                # and splitting (if splitting is an option).
                current_cost = min(current_cost, cost_if_split)
            
            return current_cost

        # The problem asks for the minimum cost to partition the entire string 's'.
        # This is equivalent to finding the minimum cost for the segment s[0...n-1]
        # considering all possible recursive splits defined by the problem rules.
        return get_segment_cost(0, n - 1)

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s = "1010"
    encCost = 2
    flatCost = 1
    expected_output = 6
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 1 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Example 2
    s = "1010"
    encCost = 3
    flatCost = 10
    expected_output = 12
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 2 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Example 3
    s = "00"
    encCost = 1
    flatCost = 2
    expected_output = 2
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 3 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Custom Test Case: All sensitive elements, splitting is always better
    s = "111111" # Length 6
    encCost = 1
    flatCost = 100 # High flatCost to ensure splitting 0-segments is not preferred, but 1-segments splitting might be
    # For "111" (length 3, 3 sensitive): base cost 3*3*1 = 9. Odd length, no split. Cost=9.
    # For "111111" (length 6, 6 sensitive): base cost 6*6*1 = 36.
    # Split into "111" + "111" costs 9 + 9 = 18.
    # min(36, 18) = 18.
    expected_output = 18
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 4 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Custom Test Case: All non-sensitive elements, no splitting
    s = "000000" # Length 6
    encCost = 100 # High encCost to ensure flatCost is preferred for 0-segments
    flatCost = 5
    # For "000" (length 3, 0 sensitive): base cost 5. Odd length, no split. Cost=5.
    # For "000000" (length 6, 0 sensitive): base cost 5.
    # Split into "000" + "000" costs 5 + 5 = 10.
    # min(5, 10) = 5.
    expected_output = 5
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 5 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Custom Test Case: Mixed, where a smaller segment doesn't split
    s = "1001" # Length 4
    encCost = 2
    flatCost = 10
    # get_segment_cost(0,3) for "1001": L=4, X=2. Base cost = 4*2*2 = 16.
    #   Split: get_segment_cost(0,1) for "10" + get_segment_cost(2,3) for "01".
    #   get_segment_cost(0,1) for "10": L=2, X=1. Base cost = 2*1*2 = 4.
    #     Split: get_segment_cost(0,0) for "1" (cost 1*1*2=2) + get_segment_cost(1,1) for "0" (cost 10). Total split = 2+10=12.
    #     Min("10") = min(4, 12) = 4.
    #   get_segment_cost(2,3) for "01": L=2, X=1. Base cost = 2*1*2 = 4.
    #     Split: get_segment_cost(2,2) for "0" (cost 10) + get_segment_cost(3,3) for "1" (cost 1*1*2=2). Total split = 10+2=12.
    #     Min("01") = min(4, 12) = 4.
    #   Split cost for "1001" = 4 + 4 = 8.
    # Min("1001") = min(16, 8) = 8.
    expected_output = 8
    assert s_obj.minCost(s, encCost, flatCost) == expected_output, f"Test Case 6 Failed: s={s}, encCost={encCost}, flatCost={flatCost}, Expected: {expected_output}, Got: {s_obj.minCost(s, encCost, flatCost)}"

    # Large N test (should pass due to O(N log N) complexity)
    # s = "1" * 100000
    # encCost = 1
    # flatCost = 100
    # print(f"Running large test case (N=10^5, all '1's)...")
    # # For all '1's, it will always split down to single '1's if encCost is low enough.
    # # cost of '1' is 1*1*encCost = encCost.
    # # So total cost will be N * encCost.
    # expected_output_large = 100000 * 1 # if split is always optimal down to single char
    # # For large N (power of 2), if base_cost(L) > 2*cost(L/2), it will split.
    # # L*X*encCost vs 2 * (L/2)*(X/2)*encCost = L*X*encCost / 2.
    # # So splitting is always better if X>0.
    # # Each '1' has cost 1*1*encCost. So N * encCost.
    # large_cost = s_obj.minCost("1" * 100000, 1, 100)
    # assert large_cost == 100000, f"Large Test Case Failed: Expected: 100000, Got: {large_cost}"
    # print(f"Large Test Case Passed (cost: {large_cost})")

    # The large test case might involve `s` not being a power of 2,
    # or mixing '0's and '1's, where some segments are not split.
    # For instance, if s = "0" * 100000, flatCost = 5, encCost = 1.
    # The cost will be flatCost = 5.
    # large_cost_zeros = s_obj.minCost("0" * 100000, 1, 5)
    # assert large_cost_zeros == 5, f"Large Zeros Test Case Failed: Expected: 5, Got: {large_cost_zeros}"
    # print(f"Large Zeros Test Case Passed (cost: {large_cost_zeros})")

    print("All tests passed!")

