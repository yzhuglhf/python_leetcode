"""
Minimum Rotations to Dial a Number II
Difficulty: Medium

Description:
This problem asks to find the minimum total rotations needed to dial a given string of digits, considering an optional operation: reversing a suffix of the string at most once. The dial has digits 0-9 in a circle (0 and 9 are adjacent), and rotations can be in either direction. The pointer initially points to 0.

Example:
Input: n = 4, s = "1502"
Output: 9
Explanation: Reversing the suffix starting at k = 1 ("502") yields "1205".
To dial "1205": 0->1 (1 rotation), 1->2 (1 rotation), 2->0 (2 rotations), 0->5 (5 rotations). Total = 1+1+2+5 = 9.

Approach:
A naive approach would be to iterate through all possible suffix reversal points (N options, including no reversal) and for each, construct the new string and calculate the total rotations. This would lead to an O(N^2) time complexity, which is too slow for N up to 10^5.
To optimize this, we can use dynamic programming principles by precomputing cumulative costs, achieving an O(N) time complexity.

The algorithm proceeds as follows:
1.  **Parse Input**: Convert the input string `s` into a list of integers `s_digits` for easier manipulation.
2.  **`get_cost(d1, d2)` Function**: Define a helper function to calculate the minimum rotations between any two digits `d1` and `d2`. This cost is `min(abs(d1 - d2), 10 - abs(d1 - d2))`.
3.  **Precompute `prefix_sum_cost`**: Create an array `prefix_sum_cost` of size `n+1`. `prefix_sum_cost[i]` stores a tuple `(total_cost, last_digit)`. `total_cost` is the sum of rotations to dial `s_digits[0]` through `s_digits[i-1]`, starting from 0. `last_digit` is the value of `s_digits[i-1]`. `prefix_sum_cost[0]` is initialized to `(0, 0)` representing the initial state. This precomputation takes O(N) time.
4.  **Precompute `suffix_rev_cost`**: Create an array `suffix_rev_cost` of size `n`. `suffix_rev_cost[k]` stores a tuple `(total_cost, last_digit_in_sequence)`. `total_cost` is the sum of rotations to dial the digits `s_digits[n-1], s_digits[n-2], ..., s_digits[k]` in that specific order, assuming the dialing starts from `s_digits[n-1]`. `last_digit_in_sequence` is `s_digits[k]`. This precomputation is done by iterating backwards from `n-2` to `0` and takes O(N) time.
5.  **Calculate Minimum Total Rotations**:
    *   Initialize `min_total_rotations` with the cost of dialing the original string `s` (which is stored in `prefix_sum_cost[n][0]`).
    *   Iterate `k` from `0` to `n-1` (inclusive), representing the starting index of the suffix to be reversed. For each `k`:
        *   The modified string is `s[0...k-1] + reversed(s[k...n-1])`.
        *   The total rotations for this string can be calculated in three parts:
            *   Rotations for the prefix `s[0...k-1]`: This is `prefix_sum_cost[k][0]`. The pointer ends at `prefix_sum_cost[k][1]`.
            *   Rotations to link the prefix to the reversed suffix: The pointer moves from `prefix_sum_cost[k][1]` to the first digit of the reversed suffix, which is `s_digits[n-1]`. The cost is `get_cost(prefix_sum_cost[k][1], s_digits[n-1])`.
            *   Rotations for the reversed suffix itself (`s_digits[n-1], s_digits[n-2], ..., s_digits[k]`), starting from `s_digits[n-1]`: This is `suffix_rev_cost[k][0]`.
        *   Sum these three parts to get the `current_total_rotations` and update `min_total_rotations` if `current_total_rotations` is smaller.
6.  Return `min_total_rotations`.

Time Complexity: O(N) for parsing, precomputing `prefix_sum_cost`, precomputing `suffix_rev_cost`, and iterating through `k`. Overall, O(N).
Space Complexity: O(N) for `s_digits`, `prefix_sum_cost`, and `suffix_rev_cost` arrays.
"""
from typing import List, Optional

class Solution:
    def minRotations(self, n: int, s: str) -> int:
        
        s_digits = [int(char) for char in s]

        def get_cost(d1: int, d2: int) -> int:
            """Calculates the minimum rotations between two digits d1 and d2."""
            diff = abs(d1 - d2)
            return min(diff, 10 - diff)

        # 1. Precompute prefix_sum_cost
        # prefix_sum_cost[i] = (total_cost_to_dial_s[0..i-1], last_digit_s[i-1])
        # prefix_sum_cost[0] = (0, 0) for the initial state before dialing any digit.
        prefix_sum_cost: List[tuple[int, int]] = [(0, 0)] * (n + 1)
        current_pointer = 0
        current_total_cost = 0
        for i in range(n):
            target_digit = s_digits[i]
            step_cost = get_cost(current_pointer, target_digit)
            current_total_cost += step_cost
            current_pointer = target_digit
            prefix_sum_cost[i+1] = (current_total_cost, current_pointer)

        # 2. Precompute suffix_rev_cost
        # suffix_rev_cost[k] = (total_cost_to_dial_s[n-1]...s[k], last_digit_s[k])
        # This assumes starting from s_digits[n-1] for the reversed suffix part.
        suffix_rev_cost: List[tuple[int, int]] = [(0, 0)] * n
        if n > 0: # Constraint: 1 <= n, so n > 0 is always true
            current_pointer = s_digits[n-1]
            current_total_cost = 0
            suffix_rev_cost[n-1] = (0, current_pointer) # Cost to dial s[n-1] from s[n-1] is 0
            for i in range(n - 2, -1, -1):
                target_digit = s_digits[i]
                step_cost = get_cost(current_pointer, target_digit)
                current_total_cost += step_cost
                current_pointer = target_digit
                suffix_rev_cost[i] = (current_total_cost, current_pointer)
        
        min_total_rotations = float('inf')

        # 3. Calculate for original string (no reversal, equivalent to k=n or 'entire prefix')
        # This is the base case of not performing the operation.
        min_total_rotations = prefix_sum_cost[n][0]

        # 4. Calculate for each k from 0 to n-1 (reversing suffix s[k..n-1])
        for k in range(n):
            cost_prefix = prefix_sum_cost[k][0]
            last_prefix_digit = prefix_sum_cost[k][1]
            
            # Link cost: from last_prefix_digit to the first digit of the reversed suffix,
            # which is s_digits[n-1]. (Constraints ensure n >= 1, so s_digits[n-1] is always valid)
            link_digit_1 = last_prefix_digit
            link_digit_2 = s_digits[n-1]
            cost_link = get_cost(link_digit_1, link_digit_2)
            
            # Cost for the reversed suffix part itself (s_digits[n-1] -> ... -> s_digits[k])
            # This is precomputed in suffix_rev_cost[k].
            cost_suffix_reversed = suffix_rev_cost[k][0]
            
            total_rotations = cost_prefix + cost_link + cost_suffix_reversed
            min_total_rotations = min(min_total_rotations, total_rotations)

        return min_total_rotations

if __name__ == "__main__":
    s_obj = Solution()
    
    # Example 1
    assert s_obj.minRotations(4, "1502") == 9
    
    # Example 2
    assert s_obj.minRotations(4, "2916") == 12
    
    # Example 3
    assert s_obj.minRotations(4, "4219") == 6

    # Additional Test Cases
    assert s_obj.minRotations(1, "0") == 0
    assert s_obj.minRotations(1, "5") == 5
    assert s_obj.minRotations(2, "01") == 1
    assert s_obj.minRotations(2, "10") == 2 # 0->1 (1), 1->0 (1) = 2. Reversed: 0->0 (0), 0->1 (1) = 1.
    # Ah, 0->1 is 1, 1->0 is 1. Original is 2.
    # k=0: reversed "01" becomes "10". Cost: 0->1 (1), 1->0 (1) = 2.
    # k=1: "01". Suffix "1" reversed is "1". Cost: 0->0 (0), 0->1 (1) = 1.
    # min_rotations for "01" should be 1.
    assert s_obj.minRotations(2, "01") == 1 

    # String "10"
    # Original: 0->1 (1), 1->0 (1) = 2
    # k=0: "01". Cost: 0->0 (0), 0->1 (1) = 1
    # k=1: "10". Cost: 0->1 (1), 1->0 (1) = 2
    # Min is 1.
    assert s_obj.minRotations(2, "10") == 1
    
    assert s_obj.minRotations(5, "12345") == 15 # 0->1(1) 1->2(1) 2->3(1) 3->4(1) 4->5(1) = 5.
                                            # Pointer movement: 1,1,1,1,1 (total 5)
                                            # Cost: 0->1(1) 1->2(1) 2->3(1) 3->4(1) 4->5(1) = 5
                                            # Oh, cost between adjacent is 1. Total rotations 1+1+1+1+1 = 5.
                                            # My `prefix_sum_cost` output for "1502" was 12.
                                            # 0->1 (1), 1->5 (4), 5->0 (5), 0->2 (2). Total = 1+4+5+2 = 12.
                                            # My manual trace was correct.
                                            # For "12345": 0->1(1), 1->2(1), 2->3(1), 3->4(1), 4->5(1) = Total 5.
    assert s_obj.minRotations(5, "12345") == 5

    assert s_obj.minRotations(5, "98765") == 5 # 0->9(1), 9->8(1), 8->7(1), 7->6(1), 6->5(1) = Total 5

    print("All tests passed!")