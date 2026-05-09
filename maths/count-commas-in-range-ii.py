"""
Count Commas in Range II
Difficulty: Medium

Description:
This problem requires calculating the total number of commas used when formatting all integers from 1 to `n` according to standard rules. A comma is inserted every three digits from the right, and numbers with fewer than four digits contain no commas.

Example:
Input: n = 1002
Output: 3
Explanation: The numbers "1,000", "1,001", and "1,002" each contain one comma, totaling 3 commas.

Approach:
The total number of commas can be efficiently calculated by summing the counts of numbers that possess at least a certain number of commas. Specifically, a number `x` with `k` commas contributes `k` to the total sum. This is equivalent to counting `x` once for each comma it contains. Thus, the total commas can be expressed as the sum of: (count of numbers in [1, n] with at least 1 comma) + (count of numbers in [1, n] with at least 2 commas) + ... and so on. A number `x` has at least `k` commas if `x` is greater than or equal to `10^(3k)`. We iterate for `k` from 1 upwards, where `10^(3k)` is the smallest number requiring `k` commas. For each `k`, we add `max(0, n - 10^(3k) + 1)` to the total, which counts how many numbers up to `n` have at least `k` commas. The iteration stops when `10^(3k)` exceeds `n`. Given `n <= 10^15`, `k` will go up to 5, as `10^(3*5) = 10^15`.

Time Complexity: O(log N) or effectively O(1). The number of iterations is proportional to `log_1000(N)`. For `N <= 10^15`, this is at most 5 iterations, making it a constant number of operations.
Space Complexity: O(1). The algorithm uses a constant amount of extra space.
"""
from typing import List, Optional

class Solution:
    def countCommas(self, n: int) -> int:
        total_commas = 0
        
        # current_threshold_for_k_commas represents 10^(3k), the smallest number that starts needing k commas.
        # For k=1, this is 10^3 (1,000).
        # For k=2, this is 10^6 (1,000,000).
        # And so on.
        current_threshold_for_k_commas = 1000 
        
        while current_threshold_for_k_commas <= n:
            # We count how many numbers in the range [1, n] have AT LEAST this many commas.
            # These are numbers from 'current_threshold_for_k_commas' up to 'n'.
            # The count of such numbers is (n - current_threshold_for_k_commas + 1).
            # This count is added to the total, effectively counting one comma for each of these numbers.
            num_values_contributing_this_comma_level = n - current_threshold_for_k_commas + 1
            
            total_commas += num_values_contributing_this_comma_level
            
            # Move to the next level of comma-grouping.
            # This means multiplying the current threshold by 1000 (e.g., from 10^3 to 10^6).
            # Python's integers handle arbitrary size, so overflow is not a concern for N up to 10^15.
            current_threshold_for_k_commas *= 1000
            
        return total_commas

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.countCommas(1002) == 3, f"Test Case 1 Failed: Input 1002, Expected 3, Got {s.countCommas(1002)}"
    
    # Example 2
    assert s.countCommas(998) == 0, f"Test Case 2 Failed: Input 998, Expected 0, Got {s.countCommas(998)}"
    
    # Custom test cases
    assert s.countCommas(1) == 0, f"Test Case 3 Failed: Input 1, Expected 0, Got {s.countCommas(1)}"
    assert s.countCommas(999) == 0, f"Test Case 4 Failed: Input 999, Expected 0, Got {s.countCommas(999)}"
    assert s.countCommas(1000) == 1, f"Test Case 5 Failed: Input 1000, Expected 1, Got {s.countCommas(1000)}"
    assert s.countCommas(1001) == 2, f"Test Case 6 Failed: Input 1001, Expected 2, Got {s.countCommas(1001)}"
    assert s.countCommas(999999) == 999000, f"Test Case 7 Failed: Input 999999, Expected 999000, Got {s.countCommas(999999)}"
    assert s.countCommas(1000000) == 999002, f"Test Case 8 Failed: Input 1000000, Expected 999002, Got {s.countCommas(1000000)}"
    assert s.countCommas(1_234_567) == 1_468_136, f"Test Case 9 Failed: Input 1,234,567, Expected 1,468,136, Got {s.countCommas(1_234_567)}"
    
    # Max n = 10^15
    assert s.countCommas(10**15) == 3998998998999005, f"Test Case 10 Failed: Input 10^15, Expected 3998998998999005, Got {s.countCommas(10**15)}"
    
    print("All tests passed!")

