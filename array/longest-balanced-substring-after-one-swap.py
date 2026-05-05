"""
Longest Balanced Substring After One Swap
Difficulty: Medium

Description:
This problem asks for the maximum length of a balanced substring (equal number of '0's and '1's) after performing at most one swap of any two characters in the input string `s`. A single swap changes the positions of two characters, but does not alter the total counts of '0's and '1's in the entire string.

Example:
Input: s = "100001"
Output: 4
Explanation:
The string has four '0's and two '1's. The maximum possible length of a balanced substring is 2 * min(total_zeros, total_ones) = 2 * min(4, 2) = 4.
Swap '0' at index 2 with '1' at index 5. The string becomes "101000".
The substring "1010" (indices 0 to 3) has two '0's and two '1's, making it balanced with length 4.

Approach:
The problem can be solved in O(N) time using a prefix sum approach. We maintain a `current_balance` (count of '1's minus count of '0's). A balanced substring `s[L...R-1]` has `(count('1') - count('0')) = 0`. We can extend this idea to "almost balanced" substrings that can be made balanced with one swap.

Let `N0` and `N1` be the total counts of '0's and '1's in the entire string `s`.
We define `p0[k]` and `p1[k]` as the counts of '0's and '1's respectively in `s[0...k-1]`. These prefix sum arrays help quickly calculate `sub_zeros_count` and `sub_ones_count` for any substring `s[prev_idx...i-1]`.
The `current_balance` after processing `s[0...i-1]` is `p1[i] - p0[i]`.
We use a dictionary `balance_map` to store the first occurrence of each `current_balance` value encountered, mapping `balance_value` to `index`. `balance_map = {0: 0}` initializes a balance of 0 before index 0, allowing for substrings starting at index 0.

For each ending index `i` (from 1 to `n`):
1.  **No swap:** If `current_balance` is already in `balance_map`, it means there's a previous `prev_idx` where the balance was the same. The substring `s[prev_idx...i-1]` is balanced. Its length is `i - prev_idx`. Update `max_len`.

2.  **One swap (case 1: `zeros = ones + 2`):** A substring `s[prev_idx...i-1]` with `(count('0') - count('1')) = 2` (i.e., `current_balance - prev_balance = -2`, so `prev_balance = current_balance + 2`). This substring has two more '0's than '1's. We can make it balanced by changing one '0' in the substring to a '1'. This requires swapping an internal '0' with an external '1'. This is possible if there is at least one '1' outside the current substring (`N1 - sub_ones_count > 0`). If so, its length `i - prev_idx` is a candidate for `max_len`.

3.  **One swap (case 2: `ones = zeros + 2`):** A substring `s[prev_idx...i-1]` with `(count('1') - count('0')) = 2` (i.e., `current_balance - prev_balance = 2`, so `prev_balance = current_balance - 2`). This substring has two more '1's than '0's. We can make it balanced by changing one '1' in the substring to a '0'. This requires swapping an internal '1' with an external '0'. This is possible if there is at least one '0' outside the current substring (`N0 - sub_zeros_count > 0`). If so, its length `i - prev_idx` is a candidate for `max_len`.

Finally, we store the first occurrence of `current_balance` in `balance_map` to ensure we always find the longest possible substring for a given balance (which corresponds to maximizing `i - prev_idx`).

Time Complexity: O(N) - We iterate through the string once. Prefix sum arrays creation takes O(N). Dictionary operations (insertions and lookups) are amortized O(1).
Space Complexity: O(N) - For prefix sum arrays `p0`, `p1` (each of size N+1) and the `balance_map` dictionary (which can store up to N distinct balance values).
"""
from typing import List, Optional
import collections

class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0

        # Calculate total counts of '0's and '1's in the entire string
        total_zeros = s.count('0')
        total_ones = n - total_zeros

        # Prefix sums for counts of '0's and '1's
        # p0[k] = count of '0's in s[0...k-1]
        # p1[k] = count of '1's in s[0...k-1]
        # p0 and p1 are 1-indexed with respect to string length, so p0[0] and p1[0] are 0.
        p0 = [0] * (n + 1)
        p1 = [0] * (n + 1)
        for k in range(n):
            p0[k+1] = p0[k] + (1 if s[k] == '0' else 0)
            p1[k+1] = p1[k] + (1 if s[k] == '1' else 0)

        max_len = 0
        
        # balance_map stores the first index `k` (exclusive end index for prefix, meaning `s[0...k-1]`)
        # where a specific balance (count('1') - count('0')) was achieved.
        # Initial state: balance 0 is achieved before index 0, so map {0: 0}.
        balance_map = {0: 0} 
        current_balance = 0

        # Iterate through the string, with `i` representing the current exclusive end index
        # (i.e., we are considering prefixes s[0...i-1])
        for i in range(1, n + 1): 
            # Update current balance based on the character s[i-1]
            if s[i-1] == '1':
                current_balance += 1
            else:
                current_balance -= 1
            
            # Case 1: Substring s[prev_idx ... i-1] is balanced without any swap.
            # This happens if `current_balance` matches a `prev_balance` seen before.
            # The length of this substring is `i - prev_idx`.
            if current_balance in balance_map:
                prev_idx = balance_map[current_balance]
                max_len = max(max_len, i - prev_idx)
            
            # Case 2: Substring s[prev_idx ... i-1] has (count('0') = count('1') + 2).
            # This means its balance (count('1') - count('0')) is -2.
            # If `current_balance` is `X`, we are looking for a `prev_idx` where `prev_balance` was `X+2`.
            # To make it balanced, we need to change one '0' in the substring to '1'. This requires:
            #   a) The substring contains at least one '0' (which is guaranteed if `count('0') = count('1') + 2`).
            #   b) There is at least one '1' *outside* this substring to swap with.
            if (current_balance + 2) in balance_map:
                prev_idx = balance_map[current_balance + 2]
                sub_ones_count = p1[i] - p1[prev_idx] # Count of '1's in s[prev_idx ... i-1]
                # Check if there's at least one '1' outside the substring s[prev_idx ... i-1]
                if total_ones - sub_ones_count > 0:
                    max_len = max(max_len, i - prev_idx)

            # Case 3: Substring s[prev_idx ... i-1] has (count('1') = count('0') + 2).
            # This means its balance (count('1') - count('0')) is 2.
            # If `current_balance` is `X`, we are looking for a `prev_idx` where `prev_balance` was `X-2`.
            # To make it balanced, we need to change one '1' in the substring to '0'. This requires:
            #   a) The substring contains at least one '1' (guaranteed if `count('1') = count('0') + 2`).
            #   b) There is at least one '0' *outside* this substring to swap with.
            if (current_balance - 2) in balance_map:
                prev_idx = balance_map[current_balance - 2]
                sub_zeros_count = p0[i] - p0[prev_idx] # Count of '0's in s[prev_idx ... i-1]
                # Check if there's at least one '0' outside the substring s[prev_idx ... i-1]
                if total_zeros - sub_zeros_count > 0:
                    max_len = max(max_len, i - prev_idx)
            
            # Store only the first occurrence of `current_balance` to ensure we consider the longest possible prefix
            # that yields this balance, which helps in maximizing `i - prev_idx`.
            if current_balance not in balance_map:
                balance_map[current_balance] = i
                
        return max_len

if __name__ == "__main__":
    s_obj = Solution()
    assert s_obj.longestBalanced(s="100001") == 4
    assert s_obj.longestBalanced(s="111") == 0
    assert s_obj.longestBalanced(s="1010") == 4
    assert s_obj.longestBalanced(s="01") == 2
    assert s_obj.longestBalanced(s="0011") == 4
    assert s_obj.longestBalanced(s="00101") == 4
    assert s_obj.longestBalanced(s="11010") == 4
    assert s_obj.longestBalanced(s="0000") == 0
    assert s_obj.longestBalanced(s="1111") == 0
    assert s_obj.longestBalanced(s="00011100") == 6
    assert s_obj.longestBalanced(s="0001101") == 6
    assert s_obj.longestBalanced(s="100") == 2
    print("All tests passed!")

