import collections
from typing import List, Optional

"""
Lexicographically Smallest Palindromic Permutation Greater Than Target
Difficulty: Hard

Description:
This problem asks for the lexicographically smallest palindromic permutation of a given string `s` that is strictly greater than a target string. If no such permutation exists, an empty string should be returned. The solution involves first checking if a palindromic permutation of `s` is even possible. Then, it uses a constructive approach, similar to finding the "next permutation," by iterating from right to left to find the first position where the permutation can differ from the target string and be greater, while ensuring the rest of the string forms the lexicographically smallest possible palindrome.

Example:
Input: s = "baba", target = "abba"
Output: "baab"

Approach:
1.  **Palindrome Possibility Check**: Count character frequencies in `s`. A string can form a palindrome if and only if at most one character has an odd frequency. If more than one character has an odd frequency, return an empty string. Identify this single odd-frequency character (if `n` is odd) as `mid_char_for_final_res`.
2.  **Separate Middle Character**: If the length `n` is odd, subtract one from the count of `mid_char_for_final_res` in `current_available_for_pairs`. This ensures `current_available_for_pairs` only tracks characters available for *pairs* in the first half of the palindrome, making all its counts even. `mid_char_for_final_res` is reserved for the exact center.
3.  **Phase 1: Find Pivot in Prefix**: Iterate `i` from `(n // 2) - 1` down to `0`. This `i` represents the rightmost index in the first half of the palindrome (`P[0...n//2-1]`) where we attempt to make `P[i] > target[i]`.
    *   For each `i`, first try to match `target[0...i-1]` for `P[0...i-1]`. Update `temp_chars_for_prefix_build` by consuming pairs of characters for `P[j]` and `P[n-1-j]` for `j` from `0` to `i-1`. If this matching is not possible (e.g., insufficient character count), continue to the next `i`.
    *   If matching is possible, iterate through characters `c` from `target[i] + 1` to `'z'`. If `c` is available in `temp_chars_for_prefix_build` (i.e., `temp_chars_for_prefix_build[c] >= 2`), we found a candidate for `P[i]`.
    *   Form the first half of the resulting palindrome: `prefix_to_pivot + c + smallest_remaining_chars`. The `smallest_remaining_chars` are chosen lexicographically from `temp_chars_for_prefix_build` after consuming two `c`'s for `P[i]` and `P[n-1-i]`.
    *   Construct the full palindrome `res_first_half_str + mid_char_for_final_res + res_first_half_str[::-1]` and return it.
4.  **Phase 2: Find Pivot in Middle (if `n` is odd)**: If Phase 1 does not find a solution, it implies that `P[0...n//2-1]` must exactly match `target[0...n//2-1]` to be a lexicographically smallest candidate. This phase is only relevant if `n` is odd.
    *   Check if `P[0...n//2-1]` can be formed by matching `target[0...n//2-1]`.
    *   If so, and if `mid_char_for_final_res` exists and is strictly greater than `target[n//2]`, then construct the palindrome using the matched prefix, `mid_char_for_final_res`, and the reversed prefix. Return this palindrome.
5.  **No Solution**: If neither phase yields a result, return an empty string.

Time Complexity: O(N * C), where N is the length of `s` and C is the size of the alphabet (26).
The outer loop for `i` runs `N/2` times. Inside, `j` loop runs `N/2` times. The character `c` loop runs `C` times. Inside that, building the suffix takes `O(N/2 + C)`. So, roughly `O(N/2 * (N/2 + C * (C + N/2)))` which simplifies to `O(N^2 * C)` in the worst case, but the inner loop for `chars_for_fill` is often limited by `N` total characters remaining for pairs rather than `N/2` repetitions of `C` character checks. A tighter analysis shows it's more like `O(N * C)` because character availability checks and updates are `O(C)`, and `sum` for prefix construction is limited by `N`. The `while` loop for `chars_for_fill` runs at most `N/2` times in total. The dominant part is `N/2 * C` from the nested `i` and `c` loops.

Space Complexity: O(N) for storing the result and `O(C)` for character counts, thus dominated by O(N).
"""

class Solution:
    def lexPalindromicPermutation(self, s: str, target: str) -> str:
        n = len(s)
        
        # 1. Initial Character Counts and Palindrome Possibility Check
        s_counts = collections.Counter(s)
        
        odd_char_count_initial = 0
        mid_char_for_final_res = ''
        for char_code in range(ord('a'), ord('z') + 1):
            char = chr(char_code)
            if s_counts[char] % 2 != 0:
                odd_char_count_initial += 1
                mid_char_for_final_res = char
        
        if odd_char_count_initial > 1:
            return "" # Cannot form any palindrome

        # 2. Separate Mid Character (if n is odd)
        # current_available_for_pairs will track characters available for pairs in the first half.
        # All counts in this counter will be even.
        current_available_for_pairs = s_counts.copy() 
        if n % 2 == 1:
            current_available_for_pairs[mid_char_for_final_res] -= 1 

        prefix_len = n // 2

        # 3. Phase 1: Iterate for Pivot `i` in the first half P[0...prefix_len-1]
        # `i` is the index in the first half of the palindrome, where we try to make P[i] > target[i].
        for i in range(prefix_len - 1, -1, -1):
            temp_chars_for_prefix_build = current_available_for_pairs.copy() 
            
            prefix_to_pivot = [] # Stores characters for P[0...i-1]
            can_match_target_prefix = True
            
            # Try to match target[0...i-1] for P[0...i-1] and its symmetric pairs.
            for j in range(i):
                char_t_j = target[j]
                if temp_chars_for_prefix_build[char_t_j] < 2:
                    can_match_target_prefix = False
                    break
                prefix_to_pivot.append(char_t_j)
                temp_chars_for_prefix_build[char_t_j] -= 2
            
            if not can_match_target_prefix:
                continue # Cannot match target prefix up to `i-1`, so this `i` is not a valid pivot. Try earlier `i`.

            # `temp_chars_for_prefix_build` now has counts of characters available for pairs
            # after forming P[0...i-1] and its reverse. All its counts are even.

            # 4. Try to find a character `c` for P[i] such that `c > target[i]`
            for char_code in range(ord(target[i]) + 1, ord('z') + 1):
                c = chr(char_code)
                
                # We need 2 'c's for P[i] and P[n-1-i] because `i` is in the first half.
                if temp_chars_for_prefix_build[c] >= 2: 
                    remaining_chars_after_pivot = temp_chars_for_prefix_build.copy()
                    remaining_chars_after_pivot[c] -= 2
                    
                    # Check if enough characters remain to fill the rest of the first half (lexicographically smallest)
                    count_of_remaining_pairs = sum(remaining_chars_after_pivot.values()) // 2
                    needed_pairs_for_suffix_prefix = prefix_len - (i + 1)
                    
                    if count_of_remaining_pairs >= needed_pairs_for_suffix_prefix:
                        # Found a valid pivot `i` and character `c`. Construct the result.
                        res_first_half_chars = prefix_to_pivot + [c]
                        
                        # Fill the rest of the first half (P[i+1...prefix_len-1]) with smallest available chars
                        for char_val in range(ord('a'), ord('z') + 1):
                            char_for_fill = chr(char_val)
                            while remaining_chars_after_pivot[char_for_fill] >= 2 and len(res_first_half_chars) < prefix_len:
                                res_first_half_chars.append(char_for_fill)
                                remaining_chars_after_pivot[char_for_fill] -= 2
                        
                        res_first_half_str = "".join(res_first_half_chars)
                        full_palindrome = res_first_half_str + mid_char_for_final_res + res_first_half_str[::-1]
                        return full_palindrome

        # 5. Phase 2: If Phase 1 yields no result, check for pivot in P[n//2] (only if n is odd)
        # This implies P[0...prefix_len-1] must match target[0...prefix_len-1].
        if n % 2 == 1:
            temp_chars_for_prefix_build = current_available_for_pairs.copy()
            prefix_match_target = []
            can_match_target_prefix_fully = True
            
            # Try to match target[0...prefix_len-1] fully
            for j in range(prefix_len): 
                char_t_j = target[j]
                if temp_chars_for_prefix_build[char_t_j] < 2:
                    can_match_target_prefix_fully = False
                    break
                prefix_match_target.append(char_t_j)
                temp_chars_for_prefix_build[char_t_j] -= 2
            
            if can_match_target_prefix_fully:
                # `mid_char_for_final_res` is the only character available to be the middle char.
                # Check if it's strictly greater than target[n//2].
                if mid_char_for_final_res and mid_char_for_final_res > target[n // 2]:
                    res_first_half_str = "".join(prefix_match_target)
                    full_palindrome = res_first_half_str + mid_char_for_final_res + res_first_half_str[::-1]
                    return full_palindrome

        # 6. If no such palindrome is found, return an empty string.
        return ""

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1: Basic case, next palindrome
    s = "baba"
    target = "abba"
    expected_output = "baab"
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    # Example 2: No greater palindrome
    s = "baba"
    target = "bbaa"
    expected_output = ""
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    # Example 3: No palindromic permutations
    s = "abc"
    target = "abb"
    expected_output = ""
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    # Example 4: Single palindromic permutation
    s = "aac"
    target = "abb"
    expected_output = "aca"
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    # Custom test: n is odd, pivot is middle character
    s = "abacaba" # can form "aabacabaa" -> actually "abacaba" itself
    target = "abacaba"
    # Possible permutations: aabcbaa, aacabaa, abacaba (lexicographically sorted)
    # The next palindrome after "abacaba" is "aabcbaa" using different char counts
    # The actual next permutation of "abacaba" is not easily found.
    # Let's verify with the logic that "abacaba" uses 'a':4, 'b':2, 'c':1. mid = 'c'
    # s = "aaabbc", target = "aaabbc" (n=6) no middle
    s = "abccba"
    target = "abccba"
    expected_output = "" # No greater palindrome if target itself is largest
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "topcoderopen" # cdeoopprt -> cooopprt
    # Let s = "aabbc" (n=5). a:2, b:2, c:1. mid='c'. available_for_pairs={'a':2, 'b':2, 'c':0}
    # Palindromic perms: aacbb, abbcb, baacb, bbaca, caaac, cbaac, cabbc
    # Lexicographically sorted: aabbc, abacaba, abbbc, baaab, babab, bbaab, bbaba, caaac, cabac, cabbc, cbaac, cbabc
    # Let's say s="aabbc", target="abbca" (n=5)
    # Palindromes for "aabbc": "abacaba" and "baacab" (typo, should be like "baab")
    # Correct palindromes for "aabbc": "abacaba", "baaab", "babaa", "caac", "cbabc"
    # Actually, aabbc -> aacbb, abcba, bacab, cabac, cbaabc -> 'a':2, 'b':2, 'c':1, mid='c'
    # Palindromes: aabacabaa (using actual char for prefix)
    # The permutations are: 'aabacabaa', 'abacabaa', 'baaacab', 'bbacaab'
    # Lexicographically sorted: aabba, abaca, b...
    s = "aabbc"
    target = "ababc" # a-b-a-b-c (target)
    # target prefix 'ab', mid 'c'.
    # Lex. smallest P > "ababc". P needs to be "abacaba" or "bacab"
    # "abacaba" is the string with char counts 'a':4, 'b':2, 'c':1. Here we have 'a':2, 'b':2, 'c':1.
    # So "abacaba" is not possible from "aabbc".
    # Palindromes for "aabbc": "aacbb", "ababa", "babab", "caaac"
    # Lex. smallest palindromes (a:2,b:2,c:1): aababaa, abacaba (no 'a' must be 4), ababa
    # Correct palindromes for "aabbc": "aabcbaa", "abacaba", "baabcab"
    # Let's list a few:
    # a c a b a -> aacba
    # a b a c a -> abaca
    # a b b c a -> abbca
    # b a a c b -> baacb
    # The palindromic permutations of `s = "aabbc"` (chars a:2, b:2, c:1):
    # aabcaa, abacaba, baaacab
    # aabcaa uses 4 a's, 2 b's. We only have 2 a's.
    # The available character counts are fixed: a:2, b:2, c:1.
    # Palindromes are: "abacaba" where 'c' is middle, 'ab' is prefix.
    # Another: "baacab" where 'c' is middle, 'ba' is prefix.
    s = "aabbc"
    target = "ababc" # "ababc" is not a palindrome and not using 'a':2 'b':2 'c':1 for n=5
    # The problem asks for PERMUTATION of `s`.
    # Permutations of "aabbc" that are palindromic:
    # 'a':2, 'b':2, 'c':1 => `n=5`. `mid_char = 'c'`. `prefix_len = 2`.
    # First half `P[0]P[1]`: must use `a:1, b:1`.
    # Possible prefixes: "ab", "ba".
    # Palindromes: "abcba", "bacab".
    # "abcba" (from "ab" prefix)
    # "bacab" (from "ba" prefix)
    # Lexicographically sorted: "abcba", "bacab".
    s = "aabbc"
    target = "abcba" # target is exactly the smallest palindrome
    expected_output = "bacab"
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "zyxw"
    target = "xxxx"
    expected_output = "" # No palindromic permutation
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "zzzz"
    target = "zzyy"
    expected_output = "" # Only "zzzz" is perm, not > "zzyy"
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "zzyy"
    target = "zyzy"
    expected_output = "yzz" # Only "yyzz" "yzy" "zzyy"
    # Palindromes for "zzyy": "yzzy", "zyyz"
    # "zzyy" and "yyzz"
    # Sorted: "yyzz", "zzzy"
    # s="zzyy" (n=4). y:2, z:2. No odd char.
    # prefix_len = 2. Prefix can be "yz" or "zy".
    # Palindromes: "yzzy", "zyyz".
    # "target = zyzy". Need > "zyzy".
    # "yzzy" is not > "zyzy".
    # "zyyz" is not > "zyzy".
    # My example here is wrong. Let's trace s="zzyy", target="zyzy". Output should be "".
    s = "zzyy"
    target = "zyzy"
    expected_output = ""
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "zzzy"
    target = "yyzz" # no valid palindrome for s. 3 z's and 1 y.
    # Palindromes for "zzzy": zyyz, zzyy. No, 3 z and 1 y means z is mid char.
    # "zzyyz" No, 3 z, 1y. Mid is 'z'. Prefix is 'zy'. Palindrome: 'zyzyz'.
    s = "zzzy"
    target = "yyyzz"
    # s="zzzy", n=4. Not a palindrome. z:3, y:1. 2 odd chars. Should return "".
    s = "zzzy"
    target = "yyyzz"
    expected_output = ""
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "aabb"
    target = "baba"
    expected_output = "" # only aabb, abba, baab, bbaa
    # Palindromes for "aabb": "abba", "baab".
    # "abba" is not > "baba". "baab" is not > "baba".
    s = "aabb"
    target = "baba"
    expected_output = ""
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    s = "abcdefg"
    target = "aaaaaaa"
    expected_output = "" # too many odd chars
    assert s_obj.lexPalindromicPermutation(s, target) == expected_output, f"Input: s='{s}', target='{target}', Expected: '{expected_output}', Got: '{s_obj.lexPalindromicPermutation(s, target)}'"

    print("All tests passed!")

