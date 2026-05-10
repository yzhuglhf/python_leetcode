"""
Count Non Decreasing Arrays With Given Digit Sums
Difficulty: Hard

Description:
This problem asks us to count the number of valid arrays `arr` of length `n` where each `arr[i]` is between 0 and 5000,
the array `arr` is non-decreasing, and the sum of digits of `arr[i]` equals `digitSum[i]`.
The result should be returned modulo 10^9 + 7.

Example:
Input: digitSum = [25,1]
Output: 6
Explanation:
Numbers whose sum of digits is 25 are 799, 889, 898, 979, 988, and 997.
The only number whose sum of digits is 1 that can appear after these values while keeping the array non-decreasing is 1000.
Thus, the valid arrays are [799, 1000], [889, 1000], [898, 1000], [979, 1000], [988, 1000], and [997, 1000].
Hence, the answer is 6.

Approach:
This problem can be solved using dynamic programming. First, we precompute all numbers `x` in the range `[0, 5000]` and categorize them by their digit sum. A list `numbers_for_sum[s]` stores all such numbers whose digit sum is `s`, in increasing order. The maximum possible digit sum for a number up to 5000 is 31 (for 4999), but the `digitSum[i]` constraint is up to 50, so we prepare for sums up to 50.

Let `dp_prev_values` be a list representing the number of ways to form a valid non-decreasing array up to the previous index `i-1`. Specifically, `dp_prev_values[k]` stores the count of arrays ending with `numbers_for_sum[digitSum[i-1]][k]`.
For the base case `i=0`, `dp_prev_values` is initialized such that `dp_prev_values[k] = 1` for each valid number `numbers_for_sum[digitSum[0]][k]`, representing one way to start the array with that number.

We then iterate from `i=1` to `n-1`. For each `digitSum[i]`, we determine `dp_curr_values`. To compute `dp_curr_values[k]` for `arr[i] = numbers_for_sum[digitSum[i]][k]`, we need to sum `dp_prev_values[j]` for all `j` where `numbers_for_sum[digitSum[i-1]][j] <= numbers_for_sum[digitSum[i]][k]`. This sum can be efficiently calculated using prefix sums of `dp_prev_values`. We maintain a two-pointer approach to find the correct range for the prefix sum, leveraging the sorted nature of `numbers_for_sum` lists. After computing `dp_curr_values`, it becomes `dp_prev_values` for the next iteration.
If at any point `numbers_for_sum[digitSum[i]]` is empty, or `dp_prev_values` becomes empty, it means no valid arrays can be formed, so we return 0. Finally, the sum of all elements in the last `dp_prev_values` gives the total number of distinct valid arrays. All additions are performed modulo 10^9 + 7.

Time Complexity: O(MAX_VAL * log(MAX_VAL) + N * MAX_VAL).
The precomputation step takes O(MAX_VAL * log(MAX_VAL)) time (where MAX_VAL=5000 and log is base 10 for digit sum calculation).
The DP iteration runs N times (where N is `len(digitSum)`). Each iteration involves calculating prefix sums (O(MAX_VAL)) and then iterating through `numbers_for_sum[digitSum[i]]` (O(MAX_VAL)), with a two-pointer approach that ensures the total work for finding previous indices is O(MAX_VAL). So each DP step is O(MAX_VAL).
Thus, the total time complexity is dominated by O(N * MAX_VAL). For N=1000, MAX_VAL=5000, this is 1000 * 5000 = 5 * 10^6 operations, which is efficient enough.

Space Complexity: O(MAX_VAL).
The `numbers_for_sum` cache stores numbers up to MAX_VAL. `dp_prev_values`, `dp_curr_values`, and `prefix_sum_dp_prev` lists also take O(MAX_VAL) space.
"""
from typing import List, Optional

class Solution:
    MAX_VAL = 5000
    MAX_DIGIT_SUM_CONSTRAINT = 50 # As per problem constraints 0 <= digitSum[i] <= 50
    MOD = 10**9 + 7

    _numbers_for_sum: List[List[int]] = None # Cache for precomputed values

    @staticmethod
    def _get_digit_sum(num: int) -> int:
        """Helper function to calculate the sum of digits of a number."""
        s = 0
        temp_num = num
        while temp_num > 0:
            s += temp_num % 10
            temp_num //= 10
        return s

    @classmethod
    def _precompute_numbers_for_sum(cls):
        """Precomputes and caches all numbers up to MAX_VAL grouped by their digit sums."""
        if cls._numbers_for_sum is not None:
            return

        cls._numbers_for_sum = [[] for _ in range(cls.MAX_DIGIT_SUM_CONSTRAINT + 1)]
        for i in range(cls.MAX_VAL + 1):
            s = cls._get_digit_sum(i)
            # Only store if the digit sum is within the allowed constraint range [0, 50].
            # This check is mostly for robustness; the problem constraints for digitSum[i] already imply this.
            if s <= cls.MAX_DIGIT_SUM_CONSTRAINT:
                cls._numbers_for_sum[s].append(i)

    def countArrays(self, digitSum: List[int]) -> int:
        # Ensure precomputation is done before starting the DP
        Solution._precompute_numbers_for_sum()
        numbers_for_sum = Solution._numbers_for_sum

        n = len(digitSum)
        
        # Initialize dp_prev_values for the first element arr[0]
        s0 = digitSum[0]
        
        # If there are no numbers corresponding to digitSum[0] in [0, 5000], return 0.
        if not numbers_for_sum[s0]:
            return 0
        
        # dp_prev_values[k] represents the number of ways to form arr[0] using
        # numbers_for_sum[s0][k]. For the first element, each valid number is 1 way.
        dp_prev_values = [1] * len(numbers_for_sum[s0])

        # Iterate for subsequent elements arr[i] from index 1 to n-1
        for i in range(1, n):
            s_prev = digitSum[i-1]
            s_curr = digitSum[i]

            # If there are no numbers corresponding to digitSum[i] in [0, 5000], return 0.
            if not numbers_for_sum[s_curr]:
                return 0
            
            # If previous DP state became empty, it means no valid arrays could be formed up to i-1.
            # So, no valid arrays can be formed up to i.
            if not dp_prev_values: 
                return 0

            list_prev_nums = numbers_for_sum[s_prev]
            list_curr_nums = numbers_for_sum[s_curr]

            # Compute prefix sums for dp_prev_values.
            # prefix_sum_dp_prev[k] = sum(dp_prev_values[0]...dp_prev_values[k])
            prefix_sum_dp_prev = [0] * len(dp_prev_values)
            if dp_prev_values: # Ensure list is not empty before indexing
                prefix_sum_dp_prev[0] = dp_prev_values[0]
                for k in range(1, len(dp_prev_values)):
                    prefix_sum_dp_prev[k] = (prefix_sum_dp_prev[k-1] + dp_prev_values[k]) % self.MOD

            dp_curr_values = [0] * len(list_curr_nums)
            prev_num_idx = 0 # This pointer helps traverse list_prev_nums

            # For each number `curr_num` that can be arr[i]:
            # Find how many previous valid numbers `prev_num` (for arr[i-1]) satisfy `prev_num <= curr_num`.
            # Sum their corresponding counts from `dp_prev_values` using prefix sums.
            for k in range(len(list_curr_nums)):
                curr_num = list_curr_nums[k]
                
                # Advance prev_num_idx until list_prev_nums[prev_num_idx] is greater than curr_num
                # This means all elements from list_prev_nums[0] to list_prev_nums[prev_num_idx - 1]
                # are less than or equal to curr_num.
                while prev_num_idx < len(list_prev_nums) and list_prev_nums[prev_num_idx] <= curr_num:
                    prev_num_idx += 1
                
                # If prev_num_idx > 0, it means there are valid previous numbers.
                # The sum of ways for arr[i-1] values less than or equal to curr_num is
                # prefix_sum_dp_prev[prev_num_idx - 1].
                if prev_num_idx > 0:
                    dp_curr_values[k] = prefix_sum_dp_prev[prev_num_idx - 1]
                # If prev_num_idx is 0, no previous number satisfies the condition, so dp_curr_values[k] remains 0.
            
            dp_prev_values = dp_curr_values # Update dp_prev_values for the next iteration

        # The final answer is the sum of all ways to form the last element of the array.
        total_ways = sum(dp_prev_values) % self.MOD
        return total_ways


if __name__ == "__main__":
    s = Solution()

    # Example 1
    digitSum1 = [25, 1]
    expected1 = 6
    result1 = s.countArrays(digitSum1)
    print(f"Input: {digitSum1}, Output: {result1}, Expected: {expected1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"

    # Example 2
    digitSum2 = [1]
    expected2 = 4
    result2 = s.countArrays(digitSum2)
    print(f"Input: {digitSum2}, Output: {result2}, Expected: {expected2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"

    # Example 3
    digitSum3 = [2, 49, 23]
    expected3 = 0
    result3 = s.countArrays(digitSum3)
    print(f"Input: {digitSum3}, Output: {result3}, Expected: {expected3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"

    # Custom test case: All numbers are 0-sum, so arr can only be [0,0,...,0]
    digitSum4 = [0, 0, 0]
    expected4 = 1 # Only [0, 0, 0]
    result4 = s.countArrays(digitSum4)
    print(f"Input: {digitSum4}, Output: {result4}, Expected: {expected4}")
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"

    # Custom test case: longer array with repeating digitSum
    digitSum6 = [1,1,1,1,1]
    expected6 = 7 
    result6 = s.countArrays(digitSum6)
    print(f"Input: {digitSum6}, Output: {result6}, Expected: {expected6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"

    print("All tests passed!")
