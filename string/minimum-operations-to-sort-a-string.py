"""
Minimum Operations to Sort a String
Difficulty: Medium

Description:
The problem asks for the minimum number of operations to sort a given string `s` in non-descending alphabetical order. An operation involves selecting any substring of `s` that is not the entire string and sorting it. If it's impossible to sort, return -1.

Example:
Input: s = "card"
Output: 2
Explanation:
1. Sort substring "car" (s[0:3]) to "acr". s becomes "acrd".
2. Sort substring "rd" (s[2:4]) to "dr". s becomes "acdr", which is sorted.

Approach:
The solution categorizes the number of operations based on the string's length and its initial "sortedness".

1.  **Base Cases:**
    *   **Already Sorted (0 operations):** If the string `s` is already sorted, no operations are needed.
    *   **Length 2 and Not Sorted (-1 operations):** If `s` has length 2 (e.g., "gf", "ba") and is not sorted, it's impossible to sort. The only non-entire substrings are single characters, which sorting does not change. We cannot sort the full string.

2.  **General Case (N > 2 and Not Sorted):** For strings longer than 2 characters, it's always possible to sort them. The number of operations will be 1, 2, or 3.
    *   First, determine `target_list`, which is the sorted version of `s`.
    *   Find the indices of the "mismatched" segment:
        *   `L`: The first index where `s[L]` differs from `target_list[L]`.
        *   `R`: The last index where `s[R]` differs from `target_list[R]`.
        (These indices must exist since the string is not sorted).

    *   **Scenario A: 1 Operation (`R - L + 1 < N`)**
        If the mismatched segment `s[L...R]` is *not* the entire string (i.e., `L > 0` or `R < N-1`), it means either a prefix `s[:L]` or a suffix `s[R+1:]` (or both) is already correctly sorted. We can select and sort the substring `s[L...R]`. This operation is allowed because it's not the entire string. After sorting this segment, `s` will match `target_list`. Thus, 1 operation suffices. (e.g., "dog" -> "dgo" by sorting "og").

    *   **Scenario B: More than 1 Operation (`R - L + 1 == N`)**
        If `L=0` and `R=N-1`, the entire string `s[0...N-1]` is mismatched. Since we cannot sort the entire string in one operation, it will take more than 1 operation. To determine if it's 2 or 3 operations, we simulate one strategic operation:
        *   Apply one allowed operation: sort the prefix `s[0...N-2]`. This changes `s[0...N-2]` while leaving `s[N-1]` untouched.
        *   Let the string after this operation be `s_after_op1_list`.
        *   Find new mismatched indices `L_prime` and `R_prime` for `s_after_op1_list` compared to `target_list`.
        *   **Sub-scenario B.1: 2 Operations (`R_prime - L_prime + 1 < N`)**
            If, after the first operation (`sort s[0...N-2]`), the *remaining* mismatched segment `s_after_op1_list[L_prime...R_prime]` is now a non-entire substring, then one more operation suffices to sort `s_after_op1_list[L_prime...R_prime]`. Total operations: 1 (for `s[0...N-2]`) + 1 (for `s_after_op1_list[L_prime...R_prime]`) = 2. (e.g., "card" -> "acrd" -> "acdr").
        *   **Sub-scenario B.2: 3 Operations (`R_prime - L_prime + 1 == N`)**
            If, even after the first operation (`sort s[0...N-2]`), the *entire* string `s_after_op1_list` still needs sorting (i.e., `L_prime=0` and `R_prime=N-1`), this specific condition is observed to occur only when `N=3` (e.g., "cba" -> "bca"). Such strings require 3 operations.

Time Complexity: O(N log N) because sorting operations (`sorted()` and `list.sort()`) on a string of length N take O(N log N). Finding indices L/R and L_prime/R_prime takes O(N).
Space Complexity: O(N) for storing list versions of strings and temporary sorted segments.
"""
from typing import List, Optional

class Solution:
    def minOperations(self, s: str) -> int:
        n = len(s)

        # Helper function to check if a list of characters is sorted
        def is_sorted(char_list: List[str]) -> bool:
            for i in range(len(char_list) - 1):
                if char_list[i] > char_list[i+1]:
                    return False
            return True
        
        # Convert string to list for mutability and easier manipulation
        s_list = list(s)

        # Case 0: The string is already sorted
        if is_sorted(s_list):
            return 0

        # Case -1: String of length 2 that is not sorted (e.g., "gf", "ba")
        # Cannot sort the entire string, and single-char substrings do nothing.
        if n == 2:
            return -1
        
        # For n > 2 and not sorted, it's always possible to sort the string.
        # The number of operations will be 1, 2, or 3.
        
        # Determine the target sorted version of the string
        target_list = sorted(s_list)

        # Find the first index L where s_list[L] differs from target_list[L]
        L = -1
        for i in range(n):
            if s_list[i] != target_list[i]:
                L = i
                break
        
        # Find the last index R where s_list[R] differs from target_list[R]
        R = -1
        for i in range(n - 1, -1, -1):
            if s_list[i] != target_list[i]:
                R = i
                break
        
        # L and R must have been found because the string is not sorted.

        # If the mismatched segment s_list[L...R] is NOT the entire string:
        # This means either s_list[0...L-1] is already correct, or s_list[R+1...N-1] is already correct (or both).
        # We can sort the segment s_list[L...R] in one operation.
        # This operation is allowed because it's not the entire string (R - L + 1 < N).
        # This will correctly place all characters and sort the string.
        if R - L + 1 < n:
            return 1
        
        # If R - L + 1 == n, it means L=0 and R=n-1.
        # The entire string is mismatched. We cannot sort the entire string in one operation.
        # So, it will take at least 2 operations.
        
        # Simulate one specific allowed operation: sort the prefix s_list[0...n-2].
        # This leaves the last character s_list[n-1] untouched.
        
        temp_prefix_list = s_list[:-1] # Get s_list[0...n-2]
        temp_prefix_list.sort()        # Sort this prefix segment
        
        s_after_op1_list = temp_prefix_list + [s_list[n-1]] # Reconstruct the string
        
        # After this first operation, check the state of s_after_op1_list.
        # It's highly unlikely to be sorted directly if L=0, R=n-1 initially,
        # but this check ensures correctness for any edge case.
        if is_sorted(s_after_op1_list):
            return 1 # This would indicate that sorting s[0...N-2] was sufficient.

        # The string is still not sorted after the first operation.
        # Find new mismatched indices L_prime and R_prime for s_after_op1_list against target_list.
        L_prime = -1
        for i in range(n):
            if s_after_op1_list[i] != target_list[i]:
                L_prime = i
                break
        
        R_prime = -1
        for i in range(n - 1, -1, -1):
            if s_after_op1_list[i] != target_list[i]:
                R_prime = i
                break
        
        # If the new mismatched segment s_after_op1_list[L_prime...R_prime] is NOT the entire string:
        # This means the first operation successfully changed the string such that the remaining
        # unsorted part is a non-entire substring. One more operation on this segment suffices.
        # Total operations: 1 (for s[0...n-2]) + 1 (for s_after_op1_list[L_prime...R_prime]) = 2.
        if R_prime - L_prime + 1 < n:
            return 2
        else: # R_prime - L_prime + 1 == n, meaning L_prime=0 and R_prime=n-1
            # Even after the first operation, the *entire* string still needs sorting.
            # This specific situation occurs when n=3 (e.g., "cba" -> "bca").
            # In such cases, a third operation is required.
            return 3

if __name__ == "__main__":
    s_obj = Solution()
    
    # Test cases from problem description
    assert s_obj.minOperations("dog") == 1, "Example 1 Failed: dog"
    assert s_obj.minOperations("card") == 2, "Example 2 Failed: card"
    assert s_obj.minOperations("gf") == -1, "Example 3 Failed: gf"

    # Additional test cases
    assert s_obj.minOperations("abc") == 0, "Test Case 1 Failed: already sorted"
    assert s_obj.minOperations("cba") == 3, "Test Case 2 Failed: cba"
    assert s_obj.minOperations("bac") == 1, "Test Case 3 Failed: bac"
    assert s_obj.minOperations("ab") == 0, "Test Case 4 Failed: ab"
    assert s_obj.minOperations("azby") == 2, "Test Case 5 Failed: azby" # azby -> abzy -> abcy
    assert s_obj.minOperations("dcba") == 2, "Test Case 6 Failed: dcba" # dcba -> bcd_a -> abcd
    assert s_obj.minOperations("fedcba") == 2, "Test Case 7 Failed: fedcba" # Longer reverse sorted

    print("All tests passed!")

