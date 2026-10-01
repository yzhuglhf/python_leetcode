"""
Minimum Deletion Cost to Make All Characters Equal
Difficulty: Medium

Description:
Given a string `s` and an array `cost` of deletion costs, the goal is to find the minimum total cost to delete characters such that the resulting string is non-empty and all its characters are identical. This implies selecting a single target character, deleting all occurrences of other characters, and keeping all occurrences of the chosen target character.

Example:
Input: s = "aabaac", cost = [1,2,3,4,1,10]
Output: 11
Explanation:
To achieve a string of equal characters, we can choose 'a', 'b', or 'c' as the target.
- If we choose 'a': We keep all 'a's (costs 1,2,4,1) and delete 'b' (cost 3) and 'c' (cost 10). Total cost = 3 + 10 = 13.
- If we choose 'b': We keep 'b' (cost 3) and delete all 'a's (costs 1,2,4,1) and 'c' (cost 10). Total cost = 1+2+4+1+10 = 18.
- If we choose 'c': We keep 'c' (cost 10) and delete all 'a's (costs 1,2,4,1) and 'b' (cost 3). Total cost = 1+2+3+4+1 = 11.
The minimum among these options is 11.

Approach:
The problem asks to obtain a non-empty string where all characters are the same. This means the final string will consist entirely of repetitions of a single character (e.g., "aaa", "b", "cc"). To find the minimum deletion cost, we can iterate through each unique character present in the input string `s` and consider it as the potential target character for the final string. For a chosen target character `C`, the minimum cost is achieved by deleting all characters in `s` that are *not* `C`, and keeping *all* occurrences of `C`. We calculate this cost for each possible target character and then return the overall minimum cost found.

To implement this, first, calculate the total sum of all deletion costs in the `cost` array. Then, create a dictionary to store the sum of costs for each unique character present in `s`. Finally, iterate through this dictionary: for each unique character `C` and its sum of costs `sum_C`, the cost to make `s` consist only of `C`'s is `(total_sum_of_all_costs - sum_C)`. The minimum of these calculated values will be the answer.

Time Complexity: O(N)
Space Complexity: O(N)
"""
from typing import List, Optional
import collections

class Solution:
    def minCost(self, s: str, cost: List[int]) -> int:
        
        # Calculate the total sum of all deletion costs. This will be used as a base.
        # This is O(N) operation.
        total_sum_of_all_costs = sum(cost)
        
        # Store the sum of costs for each unique character.
        # For example, char_cost_sums['a'] will be the sum of costs of all 'a's in s.
        char_cost_sums = collections.defaultdict(int)
        
        # Iterate through the string to populate char_cost_sums.
        # This is an O(N) operation.
        for i in range(len(s)):
            char_cost_sums[s[i]] += cost[i]
            
        min_overall_deletion_cost = float('inf')
        
        # Iterate through each unique character that appeared in the string 's'.
        # There are at most 26 unique lowercase English letters.
        # This loop runs at most 26 times.
        for sum_current_char_costs in char_cost_sums.values():
            # The cost to make the string consist only of 'char_code' is:
            # (Total sum of all costs) - (Sum of costs of 'char_code' occurrences).
            # This is because we delete all characters that are NOT 'char_code',
            # and keep ALL occurrences of 'char_code' (to minimize deletion cost for 'char_code's themselves).
            cost_for_this_char_option = total_sum_of_all_costs - sum_current_char_costs
            
            # Update the minimum overall deletion cost found so far
            min_overall_deletion_cost = min(min_overall_deletion_cost, cost_for_this_char_option)
            
        return min_overall_deletion_cost

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s1 = "aabaac"
    cost1 = [1,2,3,4,1,10]
    expected1 = 11
    assert s_obj.minCost(s1, cost1) == expected1, f"Test 1 Failed: s={s1}, cost={cost1}, Expected: {expected1}, Got: {s_obj.minCost(s1, cost1)}"

    # Example 2
    s2 = "abc"
    cost2 = [10,5,8]
    expected2 = 13
    assert s_obj.minCost(s2, cost2) == expected2, f"Test 2 Failed: s={s2}, cost={cost2}, Expected: {expected2}, Got: {s_obj.minCost(s2, cost2)}"

    # Example 3
    s3 = "zzzzz"
    cost3 = [67,67,67,67,67]
    expected3 = 0
    assert s_obj.minCost(s3, cost3) == expected3, f"Test 3 Failed: s={s3}, cost={cost3}, Expected: {expected3}, Got: {s_obj.minCost(s3, cost3)}"

    # Custom test: all different characters, one long
    s4 = "abcdefg"
    cost4 = [1,2,3,4,5,6,7]
    # Keep 'g' (cost 7), delete 'abcdef' (costs 1+2+3+4+5+6 = 21). Total = 21.
    expected4 = 21
    assert s_obj.minCost(s4, cost4) == expected4, f"Test 4 Failed: s={s4}, cost={cost4}, Expected: {expected4}, Got: {s_obj.minCost(s4, cost4)}"
    
    # Custom test: multiple occurrences of one character, others single
    s5 = "banana"
    cost5 = [1,2,3,4,5,6] # a: 1,3,5; b: 2; n: 4,6
    # Total sum of all costs = 1+2+3+4+5+6 = 21
    # Option 'a': sum_a_costs = 1+3+5 = 9. Cost = 21 - 9 = 12 (delete 'b','n','n')
    # Option 'b': sum_b_costs = 2. Cost = 21 - 2 = 19 (delete 'a','a','a','n','n')
    # Option 'n': sum_n_costs = 4+6 = 10. Cost = 21 - 10 = 11 (delete 'b','a','a','a')
    expected5 = 11
    assert s_obj.minCost(s5, cost5) == expected5, f"Test 5 Failed: s={s5}, cost={cost5}, Expected: {expected5}, Got: {s_obj.minCost(s5, cost5)}"

    # Custom test: single character string
    s6 = "a"
    cost6 = [100]
    expected6 = 0 # Keep 'a', no deletions needed. Total sum = 100. sum_a = 100. Cost = 100-100 = 0.
    assert s_obj.minCost(s6, cost6) == expected6, f"Test 6 Failed: s={s6}, cost={cost6}, Expected: {expected6}, Got: {s_obj.minCost(s6, cost6)}"

    # Custom test: two identical characters
    s7 = "aa"
    cost7 = [10, 20]
    expected7 = 0 # Keep both 'a's, cost 0. Total sum = 30. sum_a = 30. Cost = 30-30 = 0.
    assert s_obj.minCost(s7, cost7) == expected7, f"Test 7 Failed: s={s7}, cost={cost7}, Expected: {expected7}, Got: {s_obj.minCost(s7, cost7)}"

    # Custom test: two different characters
    s8 = "ab"
    cost8 = [10, 20]
    # Total sum = 30
    # Option 'a': sum_a_costs = 10. Cost = 30 - 10 = 20 (delete 'b')
    # Option 'b': sum_b_costs = 20. Cost = 30 - 20 = 10 (delete 'a')
    expected8 = 10
    assert s_obj.minCost(s8, cost8) == expected8, f"Test 8 Failed: s={s8}, cost={cost8}, Expected: {expected8}, Got: {s_obj.minCost(s8, cost8)}"

    print("All tests passed!")