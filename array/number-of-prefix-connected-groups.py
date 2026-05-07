"""
Number of Prefix Connected Groups
Difficulty: Medium

Description:
This problem asks us to count the number of distinct groups of words where each group contains at least two words that share the same prefix of a given length `k`. Words shorter than `k` are ignored as they cannot form a k-length prefix. Duplicate strings in the input array are treated as separate words, meaning they contribute individually to a group if their prefix matches.

Example:
Input: words = ["bat","dog","dog","doggy","bat"], k = 3
Output: 2
Explanation:
Words with prefix "bat": ["bat" (index 0), "bat" (index 4)]. This forms a group of size 2.
Words with prefix "dog": ["dog" (index 1), "dog" (index 2), "doggy" (index 3)]. This forms a group of size 3.
Both groups contain at least two words, so the total count is 2.

Approach:
The most efficient way to solve this problem is to group words by their k-length prefixes and then count how many of these groups have at least two words. We can achieve this using a hash map (dictionary in Python).
1. Initialize a `defaultdict(int)` to store the frequency of each k-length prefix encountered.
2. Iterate through each `word` in the input `words` list.
3. For each `word`, first check if its length is less than `k`. If it is, this word cannot form a k-length prefix, so we ignore it and continue to the next word.
4. If the word's length is `k` or greater, extract its first `k` characters to form the `prefix`.
5. Increment the count for this `prefix` in our hash map.
6. After processing all words, initialize a `connected_groups_count` to 0.
7. Iterate through the values (counts) in the hash map. For each `count`, if it is 2 or greater, it signifies that at least two words share this particular prefix, thus forming a valid connected group. Increment `connected_groups_count` for such cases.
8. Finally, return `connected_groups_count`.

Time Complexity: O(N*k), where N is the number of words in `words` and k is the given prefix length.
Iterating through N words takes O(N) time. For each word, extracting a slice of length `k` (e.g., `word[0:k]`) takes O(k) time. Hashing this `k`-length prefix and updating its count in the dictionary also takes O(k) time on average. Therefore, populating the dictionary takes O(N*k). The final iteration through dictionary values takes at most O(N) time (as there can be at most N distinct prefixes). Overall, the dominant factor is O(N*k).

Space Complexity: O(N*k), where N is the number of words and k is the given prefix length.
In the worst-case scenario, all N words could have distinct prefixes of length `k`. The dictionary would then store N entries, where each key is a string of length `k`. Thus, the total space required for the keys is O(N*k).
"""
from typing import List, Optional
import collections

class Solution:
    def prefixConnected(self, words: List[str], k: int) -> int:
        # Use a defaultdict to store counts of each k-length prefix
        # default value for int is 0, so new prefixes start with count 0 and then get incremented to 1
        prefix_counts = collections.defaultdict(int)

        # Iterate through each word in the input list
        for word in words:
            # Check if the word is long enough to have a k-length prefix
            if len(word) >= k:
                # Extract the k-length prefix
                prefix = word[0:k]
                # Increment the count for this prefix
                prefix_counts[prefix] += 1
        
        # Initialize a counter for groups with at least two words
        connected_groups_count = 0

        # Iterate through the counts of words for each prefix
        for count in prefix_counts.values():
            # If a prefix has been shared by 2 or more words, it forms a connected group
            if count >= 2:
                connected_groups_count += 1
        
        return connected_groups_count

if __name__ == "__main__":
    s = Solution()

    # Example 1
    words1 = ["apple","apply","banana","bandit"]
    k1 = 2
    expected1 = 2
    assert s.prefixConnected(words1, k1) == expected1, f"Test Case 1 Failed: Input: {words1}, k={k1}, Expected: {expected1}, Got: {s.prefixConnected(words1, k1)}"

    # Example 2
    words2 = ["car","cat","cartoon"]
    k2 = 3
    expected2 = 1
    assert s.prefixConnected(words2, k2) == expected2, f"Test Case 2 Failed: Input: {words2}, k={k2}, Expected: {expected2}, Got: {s.prefixConnected(words2, k2)}"

    # Example 3
    words3 = ["bat","dog","dog","doggy","bat"]
    k3 = 3
    expected3 = 2
    assert s.prefixConnected(words3, k3) == expected3, f"Test Case 3 Failed: Input: {words3}, k={k3}, Expected: {expected3}, Got: {s.prefixConnected(words3, k3)}"

    # Custom Test Case 4: No groups (all unique prefixes or groups of size 1)
    words4 = ["a", "b", "cde", "defg"]
    k4 = 1
    expected4 = 0
    assert s.prefixConnected(words4, k4) == expected4, f"Test Case 4 Failed: Input: {words4}, k={k4}, Expected: {expected4}, Got: {s.prefixConnected(words4, k4)}"

    # Custom Test Case 5: Words too short are ignored
    words5 = ["apple", "ap", "apply", "b", "banana"]
    k5 = 3
    expected5 = 1 # "apple" and "apply" share "app". "ap", "b", "banana" are ignored ("banana" has "ban", unique)
    assert s.prefixConnected(words5, k5) == expected5, f"Test Case 5 Failed: Input: {words5}, k={k5}, Expected: {expected5}, Got: {s.prefixConnected(words5, k5)}"
    
    # Custom Test Case 6: All words share the same prefix for k=1
    words6 = ["apple", "apply", "apricot", "apology"]
    k6 = 1
    expected6 = 1 # All start with 'a'
    assert s.prefixConnected(words6, k6) == expected6, f"Test Case 6 Failed: Input: {words6}, k={k6}, Expected: {expected6}, Got: {s.prefixConnected(words6, k6)}"

    # Custom Test Case 7: Empty words list
    words7 = []
    k7 = 2
    expected7 = 0
    assert s.prefixConnected(words7, k7) == expected7, f"Test Case 7 Failed: Input: {words7}, k={k7}, Expected: {expected7}, Got: {s.prefixConnected(words7, k7)}"

    # Custom Test Case 8: All words are too short
    words8 = ["a", "b", "c"]
    k8 = 2
    expected8 = 0
    assert s.prefixConnected(words8, k8) == expected8, f"Test Case 8 Failed: Input: {words8}, k={k8}, Expected: {expected8}, Got: {s.prefixConnected(words8, k8)}"

    # Custom Test Case 9: All words have length k, all distinct
    words9 = ["abc", "def", "ghi"]
    k9 = 3
    expected9 = 0
    assert s.prefixConnected(words9, k9) == expected9, f"Test Case 9 Failed: Input: {words9}, k={k9}, Expected: {expected9}, Got: {s.prefixConnected(words9, k9)}"

    print("All tests passed!")

