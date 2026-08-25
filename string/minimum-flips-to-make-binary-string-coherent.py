"""
Minimum Flips to Make Binary String Coherent
Difficulty: Medium

Description:
A binary string is considered coherent if it does not contain "011" or "110" as subsequences. This problem asks for the minimum number of flips ('0' to '1' or '1' to '0') to make a given string coherent. The key is to identify all possible structures of coherent strings. After analyzing the forbidden subsequences "011" (a '0' appearing before two '1's) and "110" (two '1's appearing before a '0'), it can be deduced that a coherent string must conform to one of four fundamental patterns:
1. All '0's (e.g., "000").
2. All '1's (e.g., "111").
3. Exactly one '1' with all other characters being '0's (e.g., "00100", "100", "001").
4. A string that starts with '1', ends with '1', and has only '0's in between (e.g., "101", "1001"). Any deviations (e.g., two consecutive '1's, or '0's at the ends) would typically lead to a forbidden subsequence.

Example:
Input: s = "1010"
Output: 1
Explanation: To make "1010" coherent, we can flip s[0] to '0' to get "0010". This string (a single '1' surrounded by '0's, matching pattern 3) contains no "011" or "110" subsequences. Another option is to flip s[2] to '0' to get "1000", also costing 1 flip. The pattern "1001" (matching pattern 4) would cost 2 flips (s[2] '1'->'0', s[3] '0'->'1'). Thus, 1 flip is the minimum.

Approach:
The solution calculates the minimum flips required to transform the input string `s` into each of the four coherent target patterns described above and then returns the overall minimum among them.

1. **Target: All '0's (`0...0`)**: The cost is simply the total number of '1's in the input string `s`, as each '1' needs to be flipped to a '0'.
2. **Target: All '1's (`1...1`)**: The cost is the total number of '0's in the input string `s`, as each '0' needs to be flipped to a '1'.
3. **Target: Exactly one '1' (`0...010...0`)**: We iterate through each possible position `i` in `s` that could hold the single '1'. For a chosen position `i`:
   - If `s[i]` is '0', it needs 1 flip to become '1'. If `s[i]` is already '1', it needs 0 flips.
   - All other characters `s[j]` (where `j != i`) must be '0'. The number of flips for these characters is the count of '1's among them. This can be efficiently calculated as `(total_1_count - (1 if s[i] == '1' else 0))`.
   - The total flips for this specific `i` is the sum of these two parts. We keep track of the minimum cost found across all possible `i` for this pattern.
4. **Target: Starts with '1', ends with '1', only '0's in between (`10...01`)**: This pattern is only considered if the string length `N` is at least 2. The cost is calculated as follows:
   - `1` if `s[0]` is '0' (to flip it to '1'), else `0`.
   - `1` if `s[N-1]` is '0' (to flip it to '1'), else `0`.
   - For all characters `s[k]` in the middle part (from index 1 to `N-2`), `1` if `s[k]` is '1' (to flip it to '0'), else `0`. This is efficiently found using `s[1:N-1].count('1')`.

The final answer is the minimum of these four calculated costs. The problem constraints ensure `s.length >= 1`, so an empty string does not need to be explicitly handled beyond initialization.

Time Complexity: O(N), where N is the length of the string s. This is because we iterate through the string a constant number of times: once to count '0's and '1's, once for calculating costs for pattern 3, and once for pattern 4 (using string slice `count` which is also O(N)).
Space Complexity: O(1), as only a few variables are used to store counts and minimum costs.
"""
from typing import List, Optional

class Solution:
    def minFlips(self, s: str) -> int:
        n = len(s)

        # Calculate total counts of '0's and '1's
        total_ones = 0
        for char in s:
            if char == '1':
                total_ones += 1
        total_zeros = n - total_ones

        # --- Calculate cost for Pattern 1: Target string is all '0's (e.g., "000") ---
        # Cost is the number of '1's in the original string that need to be flipped to '0'.
        cost_all_zeros = total_ones

        # --- Calculate cost for Pattern 2: Target string is all '1's (e.g., "111") ---
        # Cost is the number of '0's in the original string that need to be flipped to '1'.
        cost_all_ones = total_zeros

        # --- Calculate cost for Pattern 3: Target string has exactly one '1' and all other characters are '0's (e.g., "00100") ---
        # We iterate through each possible position for the single '1'.
        # Initialize with a value that will definitely be greater than any actual cost.
        min_cost_single_one = float('inf')
        
        # This loop runs for n iterations. Since n >= 1, it will run at least once.
        for i in range(n):
            current_cost_p3 = 0
            
            # Cost to make s[i] a '1'
            if s[i] == '0':
                current_cost_p3 += 1
            
            # Cost to make all other characters '0's
            # This involves flipping '1's at positions other than i.
            # It's (total '1's in s) minus (1 if s[i] itself is '1' and we keep it, else 0).
            ones_to_flip_elsewhere = total_ones - (1 if s[i] == '1' else 0)
            current_cost_p3 += ones_to_flip_elsewhere
            
            min_cost_single_one = min(min_cost_single_one, current_cost_p3)

        # The overall minimum flips starts with costs from the first three patterns
        min_total_flips = min(cost_all_zeros, cost_all_ones, min_cost_single_one)

        # --- Calculate cost for Pattern 4: Target string starts with '1', ends with '1', and has only '0's in between (`10...01`) ---
        # This pattern is only applicable for string lengths of 2 or more.
        if n >= 2:
            cost_pattern4 = 0
            # Cost to make s[0] a '1'
            if s[0] == '0':
                cost_pattern4 += 1
            # Cost to make s[n-1] a '1'
            if s[n-1] == '0':
                cost_pattern4 += 1
            # Cost to make all characters s[1]...s[n-2] '0's
            # This is simply counting '1's in the middle substring s[1:n-1]
            cost_pattern4 += s[1:n-1].count('1')
            
            min_total_flips = min(min_total_flips, cost_pattern4)

        return min_total_flips

if __name__ == "__main__":
    s_obj = Solution()
    
    # Example 1
    assert s_obj.minFlips("1010") == 1, "Example 1 Failed"
    
    # Example 2
    assert s_obj.minFlips("0110") == 1, "Example 2 Failed"
    
    # Example 3
    assert s_obj.minFlips("1000") == 0, "Example 3 Failed"

    # Additional test cases
    assert s_obj.minFlips("0") == 0, "Test Case '0' Failed"
    assert s_obj.minFlips("1") == 0, "Test Case '1' Failed"
    assert s_obj.minFlips("000") == 0, "Test Case '000' Failed"
    assert s_obj.minFlips("111") == 0, "Test Case '111' Failed"
    assert s_obj.minFlips("010") == 0, "Test Case '010' Failed" # Pattern 3
    assert s_obj.minFlips("101") == 0, "Test Case '101' Failed" # Pattern 4
    assert s_obj.minFlips("001") == 0, "Test Case '001' Failed" # Pattern 3
    assert s_obj.minFlips("100") == 0, "Test Case '100' Failed" # Pattern 3
    assert s_obj.minFlips("1101") == 1, "Test Case '1101' Failed" # Flip s[0] to 0 -> "0101" (incoherent due to 011 or 110 logic) or flip s[1] to 0 -> "1001" (coherent, cost 1). Flip s[3] to 0 -> "1100" (incoherent).
    # For "1101": n=4, total_ones=3, total_zeros=1
    # P1 (0000): 3 flips
    # P2 (1111): 1 flip
    # P3 (0*10*):
    # i=0(1): 0+(3-1)=2 (to 1000)
    # i=1(1): 0+(3-1)=2 (to 0100)
    # i=2(0): 1+(3-0)=4 (to 0010)
    # i=3(1): 0+(3-1)=2 (to 0001)
    # min_cost_single_one = 2
    # P4 (10*1): Target 1001. s[0]=1, s[3]=1, s[1]=0, s[2]=0.
    # s[0] is '1' -> 0. s[3] is '1' -> 0. s[1:3] (s[1]='1', s[2]='0'). Flip s[1] -> 1. Total = 1.
    # min(3,1,2,1) = 1. Correct.
    
    assert s_obj.minFlips("0101") == 1, "Test Case '0101' Failed"
    # For "0101": n=4, total_ones=2, total_zeros=2
    # P1 (0000): 2 flips
    # P2 (1111): 2 flips
    # P3 (0*10*): (s[0]='0') -> 1 + (2-0)=3 (to 1000). (s[1]='1') -> 0 + (2-1)=1 (to 0100). (s[2]='0') -> 1 + (2-0)=3 (to 0010). (s[3]='1') -> 0 + (2-1)=1 (to 0001). min_cost_single_one=1
    # P4 (10*1): Target 1001. s[0]=1, s[3]=1, s[1]=0, s[2]=0.
    # s[0] is '0' -> 1. s[3] is '1' -> 0. s[1:3] (s[1]='1', s[2]='0'). Flip s[1] -> 1. Total = 2.
    # min(2,2,1,2) = 1. Correct.
    
    print("All tests passed!")