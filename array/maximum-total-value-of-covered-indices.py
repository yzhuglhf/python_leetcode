"""
Maximum Total Value of Covered Indices
Difficulty: Medium

Description:
This problem asks us to maximize the total value of indices covered by tokens. Initially, tokens are placed at indices specified by a binary string `s`. Each token at index `i > 0` can either remain at `i` or move once to `i-1`. We must choose these moves optimally such that the sum of values `nums[idx]` for all distinct indices `idx` that contain at least one token is maximized.

Example:
Input: nums = [9,2,6,1], s = "0101"
Output: 15
Explanation: Initially, tokens are at indices 1 and 3. For the token at index 1, moving to index 0 (value 9) is better than staying at index 1 (value 2). For the token at index 3, moving to index 2 (value 6) is better than staying at index 3 (value 1). The final covered indices are {0, 2}, resulting in a total value of nums[0] + nums[2] = 9 + 6 = 15.

Approach:
The key insight is that each token's decision is independent of other tokens, and we only sum the values of *distinct* covered indices. For each index `i` where `s[i] == '1'`, if `i == 0`, the token must stay at index 0 because it cannot move further left. If `i > 0`, the token has two options: either stay at `i` (covering index `i`) or move to `i-1` (covering index `i-1`). To maximize the overall sum, this specific token should choose the option that covers the index with the higher value between `nums[i]` and `nums[i-1]`. We iterate through all initial token positions, make this greedy decision for each, and add the chosen target index to a set of `covered_indices`. Finally, we sum the `nums` values for all unique indices in this set to get the maximum total value.

Time Complexity: O(N)
The algorithm iterates through the input string `s` (and `nums`) once to determine the `covered_indices`, which takes O(N) time. Adding elements to a set takes amortized O(1) time. Subsequently, summing the values for the unique covered indices takes at most O(N) time (as there can be at most N distinct indices).
Space Complexity: O(N)
In the worst case, all N indices might be covered, requiring the `covered_indices` set to store up to N elements.
"""
from typing import List, Optional

class Solution:
    def maxTotal(self, nums: List[int], s: str) -> int:
        n = len(nums)
        
        # This set will store the final indices that are covered by tokens.
        covered_indices = set()
        
        # Iterate through all possible initial positions for tokens
        for i in range(n):
            if s[i] == '1': # If there's an initial token at index i
                if i == 0:
                    # A token at index 0 cannot move left. It must cover index 0.
                    covered_indices.add(0)
                else:
                    # A token at index i (where i > 0) has two options:
                    # 1. Stay at index i, covering nums[i].
                    # 2. Move to index i-1, covering nums[i-1].
                    # We choose the option that yields a higher value for this token.
                    if nums[i-1] >= nums[i]:
                        # Moving to i-1 is better or equal.
                        covered_indices.add(i-1)
                    else:
                        # Staying at i is better.
                        covered_indices.add(i)
        
        # Calculate the total value by summing nums[idx] for all unique covered indices.
        total_value = 0
        for idx in covered_indices:
            total_value += nums[idx]
            
        return total_value
