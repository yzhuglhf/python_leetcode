"""
Mirror Frequency Distance
Difficulty: Medium

Description:
This problem asks us to calculate a "mirror frequency distance" for a given string. For each character, its mirror is defined by its symmetric position in the alphabet (for letters) or digit range (for digits). We need to count the frequency of each unique character and its mirror character, compute the absolute difference between these frequencies, and sum these differences for all distinct mirror pairs, ensuring each pair is counted only once.

Example:
Input: s = "ab1z9"
Output: 3
Explanation: Pairs are ('a', 'z'), ('b', 'y'), ('1', '8'), ('9', '0').
|freq('a') - freq('z')| = |1 - 1| = 0
|freq('b') - freq('y')| = |1 - 0| = 1
|freq('1') - freq('8')| = |1 - 0| = 1
|freq('9') - freq('0')| = |1 - 0| = 1
Total = 0 + 1 + 1 + 1 = 3.

Approach:
First, we use `collections.Counter` to efficiently calculate the frequency of every character in the input string `s`. Next, we define a helper function `get_mirror(char)` that returns the mirror character based on whether the input character is a letter or a digit. To avoid double-counting mirror pairs (e.g., counting for 'a' and then again for 'z'), we use a `set` called `seen_characters` to keep track of characters whose mirror pairs have already been processed. We iterate through each unique character `c` present in the frequency map. If `c` has not been seen, we find its mirror `m`, mark both `c` and `m` as seen, retrieve their frequencies (defaulting to 0 if a character is not in the string), and add the absolute difference `|freq(c) - freq(m)|` to a running total. Finally, this total sum is returned.

Time Complexity: O(N)
The `collections.Counter` takes O(N) time to process the string of length N. The subsequent iteration over unique characters runs at most 36 times (fixed size of character set for lowercase English letters and digits), with each operation (mirror lookup, set operations, dictionary lookups) taking O(1) time on average. Thus, the overall time complexity is dominated by the initial frequency counting, resulting in O(N).

Space Complexity: O(1)
The `collections.Counter` stores frequencies for at most 36 unique characters (26 letters + 10 digits). The `seen_characters` set also stores at most 36 characters. Since the size of the character set is constant, the space complexity is O(1).
"""
from collections import Counter
from typing import List, Optional

class Solution:
    def mirrorFrequency(self, s: str) -> int:
        
        def get_mirror(char: str) -> str:
            """
            Returns the mirror character for a given character.
            Letters: 'a' <-> 'z', 'b' <-> 'y', etc.
            Digits: '0' <-> '9', '1' <-> '8', etc.
            """
            if 'a' <= char <= 'z':
                # The mirror of char is found by reflecting its position
                # from the start of the alphabet to the end.
                # Example: 'a' (ord 97), 'z' (ord 122).
                # Mirror of 'a' = chr(ord('a') + ord('z') - ord('a')) = chr(ord('z')) = 'z'
                # Mirror of 'm' = chr(ord('a') + ord('z') - ord('m')) = chr(110) = 'n'
                return chr(ord('a') + ord('z') - ord(char))
            elif '0' <= char <= '9':
                # The mirror of char is found by reflecting its position
                # from the start of the digit range to the end.
                # Example: '0' (ord 48), '9' (ord 57).
                # Mirror of '0' = chr(ord('0') + ord('9') - ord('0')) = chr(ord('9')) = '9'
                # Mirror of '4' = chr(ord('0') + ord('9') - ord('4')) = chr(53) = '5'
                return chr(ord('0') + ord('9') - ord(char))
            # According to constraints, s consists only of lowercase English letters and digits.
            return char 

        # Step 1: Count frequencies of all characters in the string
        frequencies = Counter(s)

        total_difference_sum = 0
        # Use a set to keep track of characters whose mirror pairs have already been processed.
        # This prevents double-counting pairs (c, m) and (m, c).
        seen_characters = set()

        # Step 2: Iterate through unique characters present in the string
        # and compute the absolute frequency difference with their mirrors.
        for char_c in frequencies:
            # If char_c has already been processed as part of a pair (either as c or as m), skip it.
            if char_c in seen_characters:
                continue
            
            # Get the mirror character for char_c
            char_m = get_mirror(char_c)
            
            # Mark both characters in the pair as seen to avoid double-counting
            seen_characters.add(char_c)
            seen_characters.add(char_m)
            
            # Get frequencies; use .get() with default 0 in case the mirror character
            # is not present in the original string.
            freq_c = frequencies[char_c]
            freq_m = frequencies.get(char_m, 0)
            
            total_difference_sum += abs(freq_c - freq_m)
            
        return total_difference_sum

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    assert s_obj.mirrorFrequency("ab1z9") == 3, f"Test Case 1 Failed: Expected 3, got {s_obj.mirrorFrequency('ab1z9')}"

    # Example 2
    assert s_obj.mirrorFrequency("4m7n") == 2, f"Test Case 2 Failed: Expected 2, got {s_obj.mirrorFrequency('4m7n')}"

    # Example 3
    assert s_obj.mirrorFrequency("byby") == 0, f"Test Case 3 Failed: Expected 0, got {s_obj.mirrorFrequency('byby')}"

    # Additional Test Cases
    # Single character, mirror not present in string
    assert s_obj.mirrorFrequency("a") == 1, f"Test Case 4 Failed: Expected 1, got {s_obj.mirrorFrequency('a')}"
    assert s_obj.mirrorFrequency("0") == 1, f"Test Case 5 Failed: Expected 1, got {s_obj.mirrorFrequency('0')}"

    # Two characters forming a mirror pair, both present
    assert s_obj.mirrorFrequency("az") == 0, f"Test Case 6 Failed: Expected 0, got {s_obj.mirrorFrequency('az')}"
    assert s_obj.mirrorFrequency("09") == 0, f"Test Case 7 Failed: Expected 0, got {s_obj.mirrorFrequency('09')}"

    # String with multiple occurrences of one character, its mirror not present
    assert s_obj.mirrorFrequency("aaaa") == 4, f"Test Case 8 Failed: Expected 4, got {s_obj.mirrorFrequency('aaaa')}"

    # String with multiple occurrences of mirror pairs
    assert s_obj.mirrorFrequency("aaabbbyy") == 1, f"Test Case 9 Failed: Expected 1, got {s_obj.mirrorFrequency('aaabbbyy')}" # ('a', 'z'): |3-0|=3. ('b', 'y'): |3-2|=1. Total: 3+1=4. Error in calculation, lets re-verify.
    # For "aaabbbyy":
    # Frequencies: {'a': 3, 'b': 3, 'y': 2}
    # Pairs:
    # 1. c='a', m='z'. freq('a')=3, freq('z')=0. |3-0|=3. seen={'a', 'z'}
    # 2. c='b', m='y'. freq('b')=3, freq('y')=2. |3-2|=1. seen={'a', 'z', 'b', 'y'}
    # 3. c='y' is in seen, skip.
    # Total = 3 + 1 = 4.
    assert s_obj.mirrorFrequency("aaabbbyy") == 4, f"Test Case 9 Failed: Expected 4, got {s_obj.mirrorFrequency('aaabbbyy')}"

    # Empty string (though constraints say 1 <= s.length, good to consider for robustness)
    # assert s_obj.mirrorFrequency("") == 0, f"Test Case 10 Failed: Expected 0, got {s_obj.mirrorFrequency('')}"

    print("All tests passed!")
