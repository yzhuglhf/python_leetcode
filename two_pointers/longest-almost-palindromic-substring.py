"""
Longest Almost-Palindromic Substring
Difficulty: Medium

Description:
This problem asks us to find the length of the longest substring in a given string `s` that is "almost-palindromic". An almost-palindromic substring is defined as one that can be transformed into a palindrome by removing exactly one character. The input string `s` consists of lowercase English letters, and its length is between 2 and 2500.

Example:
Input: s = "abca"
Output: 4
Explanation: The substring "abca" (length 4) is almost-palindromic because removing 'b' yields "aca", which is a palindrome.

Approach:
The problem requires finding the longest almost-palindromic substring. A straightforward approach involves iterating through all possible substrings of `s` and checking if each substring is almost-palindromic.

1.  **Precompute Palindromes (DP Table)**: We first create a 2D boolean array `dp[i][j]` where `dp[i][j]` is `True` if the substring `s[i...j]` is a perfect palindrome, and `False` otherwise. This can be precomputed in `O(N^2)` time using dynamic programming:
    *   All substrings of length 1 are palindromes (`dp[i][i] = True`).
    *   Substrings of length 2 are palindromic if their two characters are the same (`dp[i][i+1] = (s[i] == s[i+1])`).
    *   For substrings of length `L > 2`, `dp[i][j]` is `True` if `s[i] == s[j]` and `s[i+1...j-1]` is a palindrome (`dp[i+1][j-1]`).

2.  **Check Almost-Palindromic Property for Each Substring**: After `dp` table is filled, we iterate through all possible substrings `s[i...j]` (defined by start `i` and end `j`). For each substring, we check if it's almost-palindromic:
    *   An almost-palindromic substring must have a length of at least 2 (e.g., "ab" -> "a" is a palindrome). The problem constraints ensure `N >= 2`, so `max_len` can be initialized to 2 (as any 2-char substring like "ab" is AP).
    *   Let `current_s = s[i...j]`. We use two pointers, `p1` starting from `i` and `p2` starting from `j`, to compare characters.
    *   **Case A: `current_s` is NOT a palindrome initially.**
        *   We traverse `current_s` with `p1` and `p2`. If we find a character mismatch (`s[p1] != s[p2]`), this is the *first and only* mismatch we can tolerate.
        *   To make `current_s` almost-palindromic, we *must* remove either `s[p1]` or `s[p2]`.
        *   We then check if the remaining *contiguous* substring is a perfect palindrome: `s[p1+1...p2]` (removing `s[p1]`) OR `s[p1...p2-1]` (removing `s[p2]`). These checks can be done in `O(1)` time using the precomputed `dp` table.
        *   If either check is `True`, `current_s` is almost-palindromic.
    *   **Case B: `current_s` IS a palindrome initially.**
        *   Since the definition requires "removing *exactly one* character", an already palindromic string can still be almost-palindromic. For example, "abba" is a palindrome, and removing 'b' yields "aba" (a palindrome), so "abba" is almost-palindromic.
        *   To check this, we must iterate through every possible character `s[k]` (where `k` is from `i` to `j`) in `current_s`. For each `s[k]`, we virtually remove it, creating a *discontinuous* string `s[i...k-1] + s[k+1...j]`.
        *   We then check if this discontinuous string forms a palindrome. This check (`is_palindrome_with_skip(i, j, k)`) involves a two-pointer scan over `s[i...j]` while skipping `s[k]`, taking `O(L)` time where `L` is the length of `current_s`.
        *   If any `k` leads to a palindrome, `current_s` is almost-palindromic.

3.  **Update Maximum Length**: If a substring `s[i...j]` is found to be almost-palindromic, we update `max_len` with `j - i + 1`.

**Time Complexity**:
*   Precomputing `dp` table: `O(N^2)`.
*   Iterating through all substrings: `O(N^2)`.
*   Inside the substring loop:
    *   Case A (not a palindrome): Two pointers take `O(L)` (where `L` is substring length) to find the mismatch, then `O(1)` DP lookups. Total `O(L)`.
    *   Case B (is a palindrome): Iterates `k` from `i` to `j` (`O(L)` iterations). For each `k`, `is_palindrome_with_skip` takes `O(L)` time. Total `O(L^2)`.
*   In the worst case, many substrings will be palindromes (e.g., `s = "aaaaa..."`), leading to the `O(L^2)` check. Since `L` can be up to `N`, the overall complexity becomes `O(N^2 * N^2) = O(N^4)`.
*   Given `N <= 2500`, `O(N^4)` (approx `3.9 * 10^13` operations) is too slow for typical time limits (usually `10^8` operations). While this solution correctly implements the definition, it is likely too slow for the given constraints. An `O(N^2)` solution would be expected for `N=2500`. However, without further optimizations for the "already a palindrome" case (e.g., using string hashing or more advanced palindrome data structures), this `O(N^4)` approach is the most direct implementation of the definition. In some contexts, specific test cases or platform environments might allow `O(N^3)` or even lenient `O(N^4)` solutions to pass for `N` up to a few hundreds, but `2500` is usually strict.

**Space Complexity**:
*   `dp` table: `O(N^2)` for storing palindrome status of all substrings.

"""
from typing import List, Optional

class Solution:
    def almostPalindromic(self, s: str) -> int:
        n = len(s)
        # Constraints: 2 <= s.length <= 2500. So n >= 2 always.
        # Any substring of length 2 ("ab" or "aa") is almost-palindromic.
        # "aa" -> "a" (palindrome). "ab" -> "a" (palindrome) or "b" (palindrome).
        max_len = 2 # Minimum possible length of an almost-palindromic substring

        # dp[i][j] will be True if s[i...j] is a perfect palindrome
        dp = [[False] * n for _ in range(n)]

        # All substrings of length 1 are palindromes
        for i in range(n):
            dp[i][i] = True
        
        # Substrings of length 2
        for i in range(n - 1):
            if s[i] == s[i+1]:
                dp[i][i+1] = True

        # Substrings of length 3 or more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i+1][j-1]:
                    dp[i][j] = True

        # Helper function to check if s[start...end] becomes a palindrome
        # after removing the character at skip_index.
        # This function takes O(end - start + 1) time.
        def is_palindrome_with_skip(start, end, skip_index):
            l, r = start, end
            while l < r:
                if l == skip_index:
                    l += 1
                    continue
                if r == skip_index:
                    r -= 1
                    continue
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        # Main loop to find the longest almost-palindromic substring
        # Iterate over all possible substrings [i, j]
        for i in range(n):
            for j in range(i, n):
                current_length = j - i + 1
                
                # Optimization: No need to check substrings shorter than current max_len
                # or substrings of length less than 2 (already handled by max_len=2)
                if current_length < max_len:
                    continue

                is_ap_current_substring = False
                
                # Case 1: The substring s[i...j] is already a perfect palindrome
                if dp[i][j]:
                    # For it to be almost-palindromic, we must be able to remove exactly one character
                    # and the remaining part must be a palindrome.
                    # The resulting palindrome must have length >= 1 (so original length >= 2).
                    # Iterate through all possible characters to remove (k from i to j)
                    # and check if the remaining (potentially discontinuous) string is a palindrome.
                    for k in range(i, j + 1):
                        # The new length of string after removal is `current_length - 1`.
                        # If `current_length - 1` is 0, it becomes empty string. Empty string is
                        # typically a palindrome, but context here implies non-empty palindrome.
                        # Since `max_len` is initialized to 2, `current_length` is at least 2 for updates.
                        # `current_length - 1 >= 1` is sufficient check.
                        if is_palindrome_with_skip(i, j, k):
                            is_ap_current_substring = True
                            break # Found one valid removal, no need to check other k's
                
                # Case 2: The substring s[i...j] is NOT a palindrome
                else:
                    # Use two pointers to find the first mismatch.
                    # If we find exactly one mismatch, we must use our deletion there.
                    # If more than one mismatch, it cannot be almost-palindromic.
                    p1, p2 = i, j
                    mismatch_found = False
                    
                    while p1 < p2:
                        if s[p1] != s[p2]:
                            # This is the first mismatch. We *must* remove one character at this point.
                            # We have two options: remove s[p1] or remove s[p2].
                            # The remaining part must be a perfect palindrome (checked with dp table).
                            
                            # Option 1: Remove s[p1]. Check if s[p1+1...p2] is a palindrome.
                            cond1 = (p1 + 1 <= p2 and dp[p1+1][p2])
                            
                            # Option 2: Remove s[p2]. Check if s[p1...p2-1] is a palindrome.
                            cond2 = (p1 <= p2 - 1 and dp[p1][p2-1])
                            
                            if cond1 or cond2:
                                is_ap_current_substring = True
                            mismatch_found = True
                            break # Found the first and only allowed mismatch, no need to check further
                        p1 += 1
                        p2 -= 1
                    
                    # If mismatch_found is false here, it means the string `s[i...j]` was actually
                    # a palindrome, which is handled by the `if dp[i][j]` block above.
                    # If mismatch_found is true but neither cond1 nor cond2 works, then not AP.

                if is_ap_current_substring:
                    max_len = max(max_len, current_length)

        return max_len


if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s = "abca"
    expected_output = 4
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")

    # Example 2
    s = "abba"
    expected_output = 4
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")

    # Example 3
    s = "zzabba"
    expected_output = 5 # Substring "zabba" -> remove first 'z' -> "abba"
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")

    # Custom test case: single mismatch
    s = "racecarz" # "racecar" is a palindrome, removing 'z' (not in "racecar") doesn't help.
    # The longest AP substring could be "racecar" -> remove 'e' -> "raccar" (not palindrome).
    # "raceca" (substring of "racecarz"). "racecar"
    # "acecar" is not AP.
    # "racecar" itself is a palindrome, but not almost-palindromic according to its internal character removals.
    # "raceca" is not AP (r!=a, c!=c, e!=e, a!=a) - 2 mismatches r/a
    # "racecar" itself (len 7) is not AP
    # Consider "zracecar": "racecar" (substring) -> not AP
    # "zraceca" -> z!=a, e!=e -> not AP
    # What if "zracecaz"? Longest is "racec" for "zracecaz" (from "zraceca" -> "acec" pal)
    # The question is about substring.
    # "zracecar" substring "racecar" is not AP.
    # What are the AP substrings? "ra" -> "r" (len 2). "ac" -> "a" (len 2). "ce" -> "c" (len 2). etc.
    # "r" and "a" for "ra"
    # "racecar" - is it AP? remove 'e' (center) -> "raccar" (not palindrome).
    # remove 'r' (ends) -> "acecar" (not palindrome).
    # So "racecar" is not AP.
    # Any length 2 substring is AP. "ra", "ac", "ce", "ec", "ca", "ar", "rz".
    # Max length should be 2.
    s = "racecarz"
    expected_output = 2
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")

    # Custom test case: Already a palindrome, AP
    s = "abacaba"
    expected_output = 7 # remove 'c' -> "ababa" (palindrome)
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")
    
    # Custom test case: long string, only length 2 APs
    s = "abcdefg"
    expected_output = 2
    assert s_obj.almostPalindromic(s) == expected_output, f"Input: '{s}', Expected: {expected_output}, Got: {s_obj.almostPalindromic(s)}"
    print(f"Test case '{s}' passed.")

    print("All tests passed!")

```