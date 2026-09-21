"""
Subsequence After One Replacement
Difficulty: Medium

Description:
Given two strings `s` and `t`, the task is to determine if `s` can be transformed into a subsequence of `t` by replacing at most one character in `s` with any lowercase English letter.

Example:
Input: s = "cat", t = "chat"
Output: true
Explanation: Replace s[1] ('a') with 'h'. The modified string "cht" is a subsequence of "chat" ('c' from t[0], 'h' from t[1], 't' from t[3]).

Approach:
The solution utilizes a two-pass approach to precompute matching indices for prefixes and suffixes of `s` within `t`.
1.  **`prefix_t_end` array:** This array of size `len(s)` stores the index in `t` where `s[k]` is matched, assuming `s[0...k]` is matched greedily from the left. If `s[0...k]` cannot be entirely matched, `prefix_t_end[k]` is set to `len(t)`.
2.  **`suffix_t_start` array:** This array of size `len(s)` stores the index in `t` where `s[k]` is matched, assuming `s[k...len(s)-1]` is matched greedily from the right. If `s[k...len(s)-1]` cannot be entirely matched, `suffix_t_start[k]` is set to `-1`.

After precomputing these arrays, we perform two main checks:
1.  **Zero replacements:** We first check if `s` is already a subsequence of `t`. This is true if `prefix_t_end[len(s)-1]` is not `len(t)`. If it is, we return `true`.
2.  **One replacement:** If `s` is not already a subsequence, we iterate through each possible index `i` (from `0` to `len(s)-1`) in `s`, considering `s[i]` as the character to be replaced.
    For each `i`:
    a.  We determine the earliest possible index `min_t_idx_for_s_i` in `t` where the replaced `s[i]` could be matched. This is derived from `prefix_t_end[i-1] + 1` if `i > 0`, or `0` if `i = 0`. If `s[0...i-1]` itself could not be matched (indicated by `prefix_t_end[i-1]` being `len(t)`), then this `i` is not a viable replacement point for the prefix part.
    b.  Similarly, we determine the latest possible index `max_t_idx_for_s_i` in `t` where the replaced `s[i]` could be matched. This is derived from `suffix_t_start[i+1] - 1` if `i < len(s)-1`, or `len(t)-1` if `i = len(s)-1`. If `s[i+1...len(s)-1]` could not be matched (indicated by `suffix_t_start[i+1]` being `-1`), then this `i` is not a viable replacement point for the suffix part.
    c.  If, for a given `i`, `min_t_idx_for_s_i <= max_t_idx_for_s_i`, it implies there's at least one character in `t` that can be chosen to replace `s[i]`, allowing both the prefix `s[0...i-1]` and suffix `s[i+1...len(s)-1]` to be matched as subsequences. In this case, we return `true`.

If the loop finishes without finding any valid replacement scenario, it means `s` cannot be made a subsequence of `t` with at most one replacement, and we return `false`.

Time Complexity: O(len(s) + len(t)). Building `prefix_t_end` and `suffix_t_start` arrays each takes O(len(s) + len(t)) time. The final check iterates `len(s)` times, with each iteration being O(1).
Space Complexity: O(len(s)). This is for storing the `prefix_t_end` and `suffix_t_start` arrays.
"""
from typing import List, Optional

class Solution:
    def canMakeSubsequence(self, s: str, t: str) -> bool:
        n, m = len(s), len(t)

        # prefix_t_end[k] stores the index in t where s[k] was matched,
        # when trying to match s[0...k] greedily from the left.
        # If s[0...k] cannot be matched, prefix_t_end[k] = m.
        prefix_t_end = [m] * n
        s_ptr = 0
        t_ptr = 0
        while s_ptr < n and t_ptr < m:
            if s[s_ptr] == t[t_ptr]:
                prefix_t_end[s_ptr] = t_ptr
                s_ptr += 1
            t_ptr += 1
        
        # suffix_t_start[k] stores the index in t where s[k] was matched,
        # when trying to match s[k...n-1] greedily from the right.
        # If s[k...n-1] cannot be matched, suffix_t_start[k] = -1.
        suffix_t_start = [-1] * n
        s_ptr = n - 1
        t_ptr = m - 1
        while s_ptr >= 0 and t_ptr >= 0:
            if s[s_ptr] == t[t_ptr]:
                suffix_t_start[s_ptr] = t_ptr
                s_ptr -= 1
            t_ptr -= 1

        # Case 0: No replacement needed (s is already a subsequence of t)
        # This is true if the last character of s was matched successfully.
        if prefix_t_end[n-1] != m:
            return True

        # Case 1: One replacement
        for i in range(n): # i is the index in s that we consider replacing
            min_t_idx_for_s_i = 0  # Inclusive start index in t for the replaced s[i]
            max_t_idx_for_s_i = m - 1 # Inclusive end index in t for the replaced s[i]

            # Determine min_t_idx_for_s_i based on the prefix s[0...i-1]
            if i > 0:
                # If prefix s[0...i-1] could not be matched
                if prefix_t_end[i-1] == m:
                    continue # This 'i' is not a viable replacement point as prefix fails
                min_t_idx_for_s_i = prefix_t_end[i-1] + 1
            
            # Determine max_t_idx_for_s_i based on the suffix s[i+1...n-1]
            if i < n - 1:
                # If suffix s[i+1...n-1] could not be matched
                if suffix_t_start[i+1] == -1:
                    continue # This 'i' is not a viable replacement point as suffix fails
                max_t_idx_for_s_i = suffix_t_start[i+1] - 1
            
            # Check if there's any available character in t to replace s[i]
            # This is possible if the derived valid range for matching s[i] in t is non-empty.
            if min_t_idx_for_s_i <= max_t_idx_for_s_i:
                return True
        
        return False

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    assert s_obj.canMakeSubsequence(s = "cat", t = "chat") == True, "Example 1 Failed"

    # Example 2
    assert s_obj.canMakeSubsequence(s = "plane", t = "apple") == False, "Example 2 Failed"

    # Test cases where s is already a subsequence
    assert s_obj.canMakeSubsequence(s = "abc", t = "axbyc") == True, "Already subsequence 1 Failed"
    assert s_obj.canMakeSubsequence(s = "ace", t = "abcde") == True, "Already subsequence 2 Failed"

    # Test cases with n=1
    assert s_obj.canMakeSubsequence(s = "a", t = "b") == True, "N=1, different char Failed"
    assert s_obj.canMakeSubsequence(s = "a", t = "a") == True, "N=1, same char Failed"
    assert s_obj.canMakeSubsequence(s = "x", t = "abc") == True, "N=1, longer t Failed"

    # Test cases requiring replacement
    assert s_obj.canMakeSubsequence(s = "axb", t = "ayb") == True, "Replace middle char Failed"
    assert s_obj.canMakeSubsequence(s = "abc", t = "abdc") == True, "Replace s[2] 'c' with 'd' and then 'c' in t Failed" # this is wrong, should be "abd" as subsequence of "abdc"
    # Actually, the example for "cat", "chat" works like: 'c' from t[0], 'h' from t[1], 't' from t[3].
    # 'a' (original s[1]) is replaced by 'h' (from t[1]).
    # s="abc", t="abdc"
    # p_t_e = [0,1,3]
    # s_t_s = [0,1,3]
    # already subsequence. True.

    assert s_obj.canMakeSubsequence(s = "ab", t = "axb") == True, "Simple replacement"
    # prefix_t_end for "ab" in "axb": [0, 2] -> Already subsequence

    assert s_obj.canMakeSubsequence(s = "abd", t = "axbd") == True, "Simple replacement 2"
    # prefix_t_end for "abd" in "axbd": [0, 2, 3] -> Already subsequence

    assert s_obj.canMakeSubsequence(s = "aple", t = "apple") == True, "Single replacement example"
    # s="aple", t="apple"
    # p_t_e = [0, m, m, m] -> [0, 5, 5, 5]
    # s_t_s = [-1, -1, 3, 4]
    # No 0-replacement
    # i=0 (replace 'a'): prefix empty, suffix "ple". s_t_s[1] = -1. Fail.
    # i=1 (replace 'p'): prefix "a", suffix "le". p_t_e[0]=0. min_t_idx=1. s_t_s[2]=3. max_t_idx=2. 1 <= 2. True. (replace s[1] 'p' with t[1] 'p')

    assert s_obj.canMakeSubsequence(s = "ab", t = "cde") == False, "Completely different, no match"
    assert s_obj.canMakeSubsequence(s = "ab", t = "acb") == True, "Replace middle" # Should be true. s="a_b", t="acb". Replace '_' with 'c'.
    # prefix_t_end: [0, 3]
    # suffix_t_start: [-1, 2]
    # No 0-replacement.
    # i=0 (replace 'a'): s_t_s[1]=2. max_t_idx=1. min_t_idx=0. 0 <= 1. True. (replace s[0] with t[0])

    assert s_obj.canMakeSubsequence(s = "abc", t = "xbyz") == True, "Replacement at start"
    # s="abc", t="xbyz"
    # p_t_e = [4, 1, 4]
    # s_t_s = [-1, 1, 3]
    # No 0-replacement
    # i=0 (replace 'a'): s_t_s[1]=1. max_t_idx=0. min_t_idx=0. 0<=0. True. (replace s[0] with t[0])

    assert s_obj.canMakeSubsequence(s = "abc", t = "abcz") == True, "Already a subsequence, with extra at end of t"
    # p_t_e = [0,1,2] -> last element is 2, which is < m=4. So true.

    print("All tests passed!")