"""
Sort Vowels by Frequency
Difficulty: Medium

Description:
This problem requires rearranging only the vowels within a given string `s` based on specific sorting criteria. Vowels are sorted first by their overall frequency in the string in non-increasing order. If multiple vowels have the same frequency, they are then sorted by the position of their first occurrence in the original string in non-decreasing order. Non-vowel characters and their positions remain unchanged.

Example:
Input: s = "aeiaaioooa"
Output: "aaaaoooiie"

Approach:
The solution involves a multi-step process. First, iterate through the input string to identify all vowel characters and their original indices. Simultaneously, calculate the total frequency for each unique vowel ('a', 'e', 'i', 'o', 'u') and record the first occurrence index for each unique vowel type. After collecting all individual vowel occurrences into a list, sort this list using a custom comparison key. The key for each vowel character will be a tuple: `(-frequency, first_occurrence_index)`, ensuring that vowels with higher frequencies come first, and among those with the same frequency, those appearing earlier in the string come first. Finally, iterate through the original vowel indices and replace the characters at these positions with the newly sorted vowels, preserving the positions of non-vowel characters. The modified list of characters is then joined back into a string.

Time Complexity: O(N log N)
The initial pass through the string to collect vowel information takes O(N) time. The dominant factor is sorting the list of extracted vowels. In the worst case, all characters are vowels, making the length of this list N, so sorting takes O(N log N). Placing the sorted vowels back takes O(N). String joining also takes O(N). Thus, the overall time complexity is O(N log N).

Space Complexity: O(N)
We use a list to store character representation of `s` (O(N)), a list for vowel indices (O(N) in worst case), and a list for extracted vowel characters (O(N) in worst case). Dictionaries for vowel counts and first occurrence indices store at most 5 entries, contributing O(1) space. Thus, the overall space complexity is O(N).
"""
import collections

class Solution:
    def sortVowels(self, s: str) -> str:
        VOWELS = frozenset({'a', 'e', 'i', 'o', 'u'})
        
        # Convert string to list for in-place modification
        s_list = list(s)
        
        # Stores original indices of vowel positions
        vowel_indices = [] 
        # Stores vowel characters encountered, in their original order
        found_vowels = [] 
        
        # To determine sorting priority for unique vowel types:
        # Stores total frequency of each unique vowel ('a', 'e', 'i', 'o', 'u')
        vowel_counts = collections.Counter()
        # Stores the first occurrence index for each unique vowel
        first_occurrence_idx = {}

        # First pass: collect all necessary information
        for i, char in enumerate(s):
            if char in VOWELS:
                vowel_indices.append(i)
                found_vowels.append(char)
                
                vowel_counts[char] += 1
                if char not in first_occurrence_idx:
                    first_occurrence_idx[char] = i
        
        # Define the custom sorting key function
        # Sort by frequency (non-increasing, so negate frequency),
        # then by first occurrence index (non-decreasing)
        def sort_key(vowel_char):
            freq = vowel_counts[vowel_char]
            first_idx = first_occurrence_idx[vowel_char]
            return (-freq, first_idx)
        
        # Sort the collected individual vowel characters using the custom key
        # If no vowels are found, found_vowels will be empty, and sort() will be O(1).
        if found_vowels:
            found_vowels.sort(key=sort_key)
        
        # Second pass: place the sorted vowels back into their original positions
        for i in range(len(vowel_indices)):
            original_idx = vowel_indices[i]
            sorted_vowel = found_vowels[i]
            s_list[original_idx] = sorted_vowel
            
        # Join the list of characters back into a string
        return "".join(s_list)

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    assert s_obj.sortVowels("leetcode") == "leetcedo", "Example 1 Failed"

    # Example 2
    assert s_obj.sortVowels("aeiaaioooa") == "aaaaoooiie", "Example 2 Failed"

    # Example 3
    assert s_obj.sortVowels("baeiou") == "baeiou", "Example 3 Failed"
    
    # Test case: No vowels
    assert s_obj.sortVowels("rhythm") == "rhythm", "No vowels test failed"

    # Test case: All vowels, all distinct frequencies (implicitly, since all unique and count is 1)
    # 'u':1 (idx 0), 'i':1 (idx 1), 'o':1 (idx 2), 'e':1 (idx 3), 'a':1 (idx 4)
    # Freqs are same. Sorted by first occ: u, i, o, e, a (original order)
    assert s_obj.sortVowels("uioea") == "uioea", "All vowels test failed (uioea)"
    
    # Test case: Multiple instances of some vowels, mixed with consonants
    # 'o': 3 (first at 1), 'e': 2 (first at 6)
    # Vowels in order of appearance: o, o, e, o, e
    # Sorted vowel sequence (by freq then first_occ): o, o, o, e, e
    # Original: t(0) o(1) p(2) c(3) o(4) d(5) e(6) r(7) o(8) p(9) e(10) n(11)
    # New:      t(0) o(1) p(2) c(3) o(4) d(5) o(6) r(7) e(8) p(9) e(10) n(11)
    assert s_obj.sortVowels("topcoderopen") == "topcodorepen", "Complex test (topcoderopen) failed"

    # Test case: All same frequency, already in first occurrence order
    assert s_obj.sortVowels("aeiou") == "aeiou", "All same freq, natural order test failed"

    # Test case: Single character vowel
    assert s_obj.sortVowels("a") == "a", "Single vowel test failed"

    # Test case: Single character consonant
    assert s_obj.sortVowels("z") == "z", "Single consonant test failed"

    print("All tests passed!")