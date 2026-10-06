"""
Minimum Number of String Groups Through Transformations
Difficulty: Hard

Description:
This problem asks us to partition an array of strings into the minimum number of groups, where strings in the same group are "equivalent". Two strings are equivalent if one can be transformed into the other. A transformation involves splitting a string into two subsequences: one for even-indexed characters (E) and one for odd-indexed characters (O). Both E and O can then be independently cyclically shifted any number of positions. The transformed string is reconstructed by placing the shifted E characters back into even indices and shifted O characters into odd indices.

Example:
Input: words = ["ntgwz","zwntg"]
Output: 1
Explanation: For "ntgwz", the even-indexed subsequence E is "ngz" and the odd-indexed subsequence O is "tw". Shifting "ngz" right by 1 position gives "zng", and shifting "tw" right by 1 position gives "wt". Reconstructing with "zng" at even indices and "wt" at odd indices yields "zwntg". Thus, "ntgwz" and "zwntg" are equivalent and belong to the same group.

Approach:
The problem defines an equivalence relation. To find the minimum number of groups, we need to count the number of unique equivalence classes. This can be achieved by mapping each string to a "canonical form" such that all equivalent strings map to the same canonical form, and non-equivalent strings map to different canonical forms. The number of unique canonical forms will be the answer.

For a string `s` to be transformable into `t`, they must have the same length. Let `E_s` and `O_s` be the even and odd subsequences of `s`, and `E_t` and `O_t` for `t`. The condition for equivalence is that `E_s` must be a cyclic shift of `E_t`, AND `O_s` must be a cyclic shift of `O_t`.

To achieve a canonical form for a string `S` under cyclic shifts, we can find its lexicographically smallest cyclic shift. For example, the cyclic shifts of "abc" are "abc", "bca", "cab". The lexicographically smallest is "abc". Thus, "abc" serves as the canonical form for all its cyclic shifts.

The algorithm proceeds as follows:
1.  Define a helper function `get_min_cyclic_shift(s: str)` that returns the lexicographically smallest cyclic shift of a given string `s`. This function must be efficient, running in O(length_of_s) time. A common linear-time algorithm involves concatenating the string with itself (`s + s`) and then using a two-pointer approach to find the minimal substring of length `len(s)` within the concatenated string.
2.  Initialize an empty set `canonical_forms` to store unique tuples of (min_E, min_O).
3.  For each `word` in the input `words` array:
    a.  Extract its even-indexed characters into a string `E_str`.
    b.  Extract its odd-indexed characters into a string `O_str`.
    c.  Compute `min_E = get_min_cyclic_shift(E_str)`.
    d.  Compute `min_O = get_min_cyclic_shift(O_str)`.
    e.  Add the tuple `(min_E, min_O)` to the `canonical_forms` set.
4.  The final answer is the number of elements in the `canonical_forms` set.

Time Complexity: O(L_total), where L_total is the sum of lengths of all strings in `words`. This is because extracting E and O, and then finding their minimum cyclic shifts, each take time proportional to the length of the string, and these operations are performed for each string. Set insertion and hashing also take time proportional to string lengths.
Space Complexity: O(L_total), as the `canonical_forms` set might store distinct representations for all strings, and each representation stores strings whose total length sums up to L_total.
"""
from typing import List, Optional

class Solution:
    def minimumGroups(self, words: List[str]) -> int:
        
        def get_min_cyclic_shift(s: str) -> str:
            """
            Computes the lexicographically smallest cyclic shift of a string in O(N) time.
            This is a standard two-pointer algorithm.
            """
            if not s:
                return ""
            
            n = len(s)
            s_double = s + s # Concatenate string with itself to handle wrap-around shifts easily
            
            i = 0  # Starting index of the current best candidate shift
            j = 1  # Starting index of the current candidate shift to compare
            k = 0  # Length of the common prefix
            
            # The loop continues as long as there are valid starting positions for both i and j
            # within the original string's length (n).
            while i < n and j < n:
                # Find the length of the common prefix between s_double[i:] and s_double[j:]
                # up to length n.
                while k < n and s_double[i + k] == s_double[j + k]:
                    k += 1
                
                if k == n: 
                    # If k reaches n, it means s[i:]+s[:i] and s[j:]+s[:j] are identical.
                    # We can break as we've found a minimal shift (or one of them).
                    break
                
                # If s_double[i+k] < s_double[j+k], then the shift starting at i is lexicographically smaller.
                # All shifts starting from j up to j+k (exclusive) are worse than i's shift.
                # So, j can be advanced past these positions.
                if s_double[i + k] < s_double[j + k]:
                    j += k + 1
                else: # s_double[i+k] > s_double[j+k], shift starting at j is smaller.
                    # Similarly, i can be advanced.
                    i += k + 1
                
                k = 0 # Reset common prefix length for the next comparison
                
                # If i and j become the same, increment j to ensure they point to distinct candidates.
                # This prevents infinite loops if i and j get stuck on the same position.
                if i == j:
                    j += 1
            
            # The smallest starting index for the cyclic shift is 'i' (or 'j' if 'i' was advanced past 'n').
            # Since the loop condition `i < n` ensures `i` stays within bounds, `i` is the correct result.
            return s[i:] + s[:i]

        canonical_forms = set()

        for word in words:
            E_chars = []
            O_chars = []
            for idx, char in enumerate(word):
                if idx % 2 == 0:
                    E_chars.append(char)
                else:
                    O_chars.append(char)
            
            E_str = "".join(E_chars)
            O_str = "".join(O_chars)
            
            min_E = get_min_cyclic_shift(E_str)
            min_O = get_min_cyclic_shift(O_str)
            
            canonical_forms.add((min_E, min_O))
        
        return len(canonical_forms)

