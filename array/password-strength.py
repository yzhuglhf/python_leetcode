"""
Password Strength
Difficulty: Medium

Description:
This problem asks us to calculate a "strength" score for a given password string based on the distinct types of characters it contains. Points are awarded for each distinct lowercase letter (1 point), uppercase letter (2 points), digit (3 points), and specific special characters (!@#$) (5 points). Each character contributes at most once, meaning only distinct characters of each type are considered.

Example:
Input: password = "aA1!"
Output: 11
Explanation: Distinct characters are 'a', 'A', '1', '!'. Strength = 1 (a) + 2 (A) + 3 (1) + 5 (!) = 11.

Approach:
The core requirement is to count points for *distinct* characters across different categories. A straightforward way to handle distinct characters is to first convert the input `password` string into a `set`. This automatically removes duplicate characters, ensuring each unique character is processed exactly once. After obtaining the set of distinct characters, we iterate through each character in this set. For each character, we determine its type using built-in string methods like `islower()`, `isupper()`, and `isdigit()`, or by checking if it belongs to a predefined set of special characters. Based on its type, we add the corresponding points to a running total. Finally, this total represents the password strength.

Time Complexity: O(N), where N is the length of the `password` string.
Creating the `set` from the password takes O(N) time. Iterating through the distinct characters in the set takes O(C) time, where C is the number of distinct characters. Since the set of possible characters is small and fixed (English letters, digits, and 4 specific specials, max 66 distinct characters), C is effectively a constant. Thus, the overall time complexity is dominated by the set creation, making it O(N).

Space Complexity: O(1).
The `set` used to store distinct characters will contain at most a fixed number of unique characters (26 lowercase + 26 uppercase + 10 digits + 4 special characters = 66 total possible distinct characters). This maximum size is constant and does not depend on the length of the input password string N. Therefore, the space complexity is O(1).
"""
from typing import List, Optional

class Solution:
    def passwordStrength(self, password: str) -> int:
        
        strength = 0
        
        # Use a set to automatically handle distinct characters
        seen_chars = set(password)
        
        # Define the set of special characters for O(1) lookup
        special_chars_set = {'!', '@', '#', '$'}
        
        for char in seen_chars:
            if char.islower():
                strength += 1
            elif char.isupper():
                strength += 2
            elif char.isdigit():
                strength += 3
            elif char in special_chars_set:
                strength += 5
                
        return strength

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.passwordStrength("aA1!") == 11, "Example 1 failed"
    
    # Example 2
    assert s.passwordStrength("bbB11#") == 11, "Example 2 failed"
    
    # Additional test cases
    assert s.passwordStrength("abc") == 3, "Test Case 3 failed: all lowercase"
    assert s.passwordStrength("ABC") == 6, "Test Case 4 failed: all uppercase"
    assert s.passwordStrength("123") == 9, "Test Case 5 failed: all digits"
    assert s.passwordStrength("!@#$") == 20, "Test Case 6 failed: all specials"
    assert s.passwordStrength("aAaA111!!!") == 11, "Test Case 7 failed: duplicates"
    assert s.passwordStrength("") == 0, "Test Case 8 failed: empty string"
    assert s.passwordStrength("HelloWorld123!!") == 1 + 2 + 3 + 5, "Test Case 9 failed: mixed"
    assert s.passwordStrength("zZ9$") == 1 + 2 + 3 + 5, "Test Case 10 failed: edge chars"

    print("All tests passed!")