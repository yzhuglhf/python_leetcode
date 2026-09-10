"""
Process String with Special Operations II
Difficulty: Hard

Description:
This problem requires processing a string `s` with various operations (append character, remove last, duplicate, reverse) to build a final string. The challenge is that the final string's length and the target index `k` can be extremely large (up to 10^15), preventing explicit string construction. We need to find the `k`-th character of this conceptual string.

Example:
Input: s = "a#b%*", k = 1
Output: "a"
Explanation: The string processes as follows: "a" -> "aa" -> "aab" -> "baa" -> "ba". The character at index 1 of "ba" is 'a'.

Approach:
The core idea is to simulate the string building process by tracking only the current length and a history of operations. Since `k` can be very large, we cannot construct the actual string. Instead, after computing the final length of the string, we traverse the operation history in reverse. For each operation, we transform the target index `k` to its equivalent position in the string *before* that operation was applied. We also maintain a `reversed_status` boolean, which toggles with each '%' operation, indicating if the current conceptual string segment is logically reversed.

The `history` list stores tuples of `(operation_type, related_value, length_before_operation)`.
1.  **Forward Pass:** Iterate through `s`. Maintain `current_length` (the length of the string if fully materialized). For each character in `s`:
    *   **Lowercase letter `c`:** Append `('char', c, current_length)` to `history`. Increment `current_length`.
    *   **`*`:** Append `('*', current_length)` to `history`. If `current_length > 0`, decrement `current_length`.
    *   **`#`:** Append `('#', current_length)` to `history`. Double `current_length`.
    *   **`%`:** Append `('%', current_length)` to `history`. `current_length` remains unchanged.
2.  **Backward Pass:** After processing all of `s`, if `k` is out of bounds of the final `current_length`, return `'.'`. Otherwise, initialize `current_k = k` (the 0-indexed target) and `effective_len = current_length`, `reversed_status = False`. Iterate through `history` in reverse order:
    *   **`char` operation:** Let `char_val` be the character and `len_before_this_append` be the length before this character was added.
        *   If `reversed_status` is true: if `current_k == 0`, we found the character (it's the first in the reversed string, which means it was the last appended). Otherwise, decrement `current_k` (to adjust for the removed 'last' character).
        *   If `reversed_status` is false: if `current_k == len_before_this_append`, we found the character (it was appended at the end). Otherwise, `current_k` remains unchanged.
        *   In both cases, if the character isn't found, decrement `effective_len` to conceptually remove it.
    *   **`*` operation:** This operation removed the last character. When undoing, the string conceptually grows by one. Set `effective_len` to `len_before_operation` (the length before `*` reduced it). `current_k` remains unchanged as it now refers to the same position in a longer conceptual string.
    *   **`#` operation:** This operation duplicated the string. `effective_len` represents the length of `S+S`. We need to find `k` in the original `S`. If `len_before_operation` (length of `S`) is 0, then the string was empty, `current_k` and `effective_len` remain 0. Otherwise, update `current_k = current_k % len_before_operation`. Set `effective_len = len_before_operation`. The `reversed_status` doesn't change, as `reversed(S+S)` is `reversed(S) + reversed(S)`, so `k` maps to an an equivalent position in `S` while maintaining `reversed_status`.
    *   **`%` operation:** This operation reversed the string. Toggle `reversed_status`. `current_k` and `effective_len` remain unchanged.
3.  If the loop finishes without returning a character, it means `k` must have pointed to an empty part of the string. This is implicitly handled by the initial `k >= current_length` check, as any valid `k` must eventually correspond to a 'char' operation. In such cases (which should theoretically not be reached for a valid `k`), `'.'` would be returned.

Time Complexity: O(S.length) - One pass to build history, one pass to trace k back.
Space Complexity: O(S.length) - To store the history of operations.
"""
from typing import List, Optional

class Solution:
    def processStr(self, s: str, k: int) -> str:
        history = []
        current_length = 0

        # Forward Pass: Build history and track current_length
        for char_s in s:
            if char_s.islower():
                history.append(('char', char_s, current_length))
                current_length += 1
            elif char_s == '*':
                # Store length BEFORE this operation
                history.append(('*', current_length))
                if current_length > 0:
                    current_length -= 1
            elif char_s == '#':
                # Store length BEFORE this operation
                history.append(('#', current_length))
                current_length *= 2
            elif char_s == '%':
                # Store length BEFORE this operation
                history.append(('%', current_length))
                # current_length remains unchanged for reverse

        # Check if k is out of bounds for the final string
        if k >= current_length:
            return '.'
        
        # Backward Pass: Trace k through the history
        current_k = k
        effective_len = current_length # Represents the length of the string at the current point in backward traversal
        reversed_status = False # True if current_k is referencing the string as if it were reversed

        for i in range(len(history) - 1, -1, -1):
            op_type, *args = history[i]
            
            # len_before_op_applied refers to the length of the string
            # *before* the operation at history[i] was applied.
            # This is crucial for undoing its effects on length and k.
            len_before_op_applied = args[-1]

            if op_type == 'char':
                char_val = args[0]
                
                # If the current conceptual string is reversed
                if reversed_status:
                    # If current_k points to the first character of the reversed string,
                    # it means it's the character that was originally appended last.
                    if current_k == 0:
                        return char_val
                    # Otherwise, it points to a character *before* this appended char
                    # in the reversed string. Adjust k.
                    current_k -= 1
                else: # current conceptual string is not reversed
                    # If current_k points to the last character of the original string,
                    # it means it's the character that was appended last.
                    # This character was appended at index `len_before_op_applied`.
                    if current_k == len_before_op_applied:
                        return char_val
                    # Otherwise, it points to a character *before* this appended char.
                    # No change to current_k, it just now refers to the same index
                    # in the string excluding the last char.
                
                # If we haven't found the character, it means current_k refers to
                # an earlier part of the string. So, conceptually remove this char.
                effective_len -= 1

            elif op_type == '*':
                # This operation removed a character.
                # To undo it, the string length becomes what it was *before* the '*'
                # removed the character.
                effective_len = len_before_op_applied
                # current_k does not change; it refers to the same position
                # in the conceptually longer string (before the last char was removed).

            elif op_type == '#':
                # This operation duplicated the string.
                # len_before_op_applied is the length of the string 'S' before 'S' became 'S+S'.
                
                # If the string was empty before duplication, it remains empty.
                if len_before_op_applied == 0:
                    current_k = 0 # If effective_len was 0 and k was 0, it stays 0.
                    effective_len = 0
                else:
                    # current_k refers to an index in S+S (possibly reversed).
                    # We map it back to an index in the original S.
                    # e.g., for S+S, index i maps to i % len(S).
                    current_k %= len_before_op_applied
                    effective_len = len_before_op_applied
                
                # The reversed_status remains the same because
                # reversed(S+S) == reversed(S) + reversed(S).
                # So if current_k mapped to the first half of (S+S) or (reversed(S)+reversed(S)),
                # the component string `S` (or `reversed(S)`) retains the same reversal property.

            elif op_type == '%':
                # This operation reversed the string.
                # We simply toggle the reversal status.
                reversed_status = not reversed_status
                # effective_len and current_k remain unchanged for this operation.
        
        # This point should theoretically not be reached if k was initially valid and the string
        # was not empty, as a character must eventually be found.
        # However, as a safeguard, if we exhaust history without returning, it's an invalid index.
        return '.'


if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s = "a#b%*"
    k = 1
    # Expected: "ba", k=1 is 'a'
    assert s_obj.processStr(s, k) == "a", f"Test 1 Failed: s={s}, k={k}"

    # Example 2
    s = "cd%#*#"
    k = 3
    # Expected: "dcddcd", k=3 is 'd'
    assert s_obj.processStr(s, k) == "d", f"Test 2 Failed: s={s}, k={k}"

    # Example 3
    s = "z*#"
    k = 0
    # Expected: "", k=0 is '.'
    assert s_obj.processStr(s, k) == ".", f"Test 3 Failed: s={s}, k={k}"

    # Custom Test 1: Simple append
    s = "abc"
    k = 0
    # Expected: "abc", k=0 is 'a'
    assert s_obj.processStr(s, k) == "a", f"Test 4 Failed: s={s}, k={k}"

    # Custom Test 2: Out of bounds
    s = "abc"
    k = 3
    # Expected: "abc", k=3 is '.'
    assert s_obj.processStr(s, k) == ".", f"Test 5 Failed: s={s}, k={k}"

    # Custom Test 3: Multiple reverses
    s = "abc%%"
    k = 0
    # Expected: "abc", k=0 is 'a'
    assert s_obj.processStr(s, k) == "a", f"Test 6 Failed: s={s}, k={k}"

    # Custom Test 4: Reverse and k
    s = "abc%"
    k = 0
    # Expected: "cba", k=0 is 'c'
    assert s_obj.processStr(s, k) == "c", f"Test 7 Failed: s={s}, k={k}"

    # Custom Test 5: Duplication and k
    s = "a#c"
    k = 2
    # Expected: "aac", k=2 is 'c'
    assert s_obj.processStr(s, k) == "c", f"Test 8 Failed: s={s}, k={k}"

    # Custom Test 6: Duplication and k in first half
    s = "ab#"
    k = 0
    # Expected: "abab", k=0 is 'a'
    assert s_obj.processStr(s, k) == "a", f"Test 9 Failed: s={s}, k={k}"

    # Custom Test 7: Duplication and k in second half
    s = "ab#"
    k = 3
    # Expected: "abab", k=3 is 'b'
    assert s_obj.processStr(s, k) == "b", f"Test 10 Failed: s={s}, k={k}"
    
    # Custom Test 8: Complex sequence with a large k
    s = "abcdefghijklmno#%*p"
    k = 100
    # Initial: "abcdefghijklmno" (len 15)
    # # : "abcdefghijklmnoabcdefghijklmno" (len 30)
    # % : "onmlkjihgfedcbabcdefghijklmno" (len 30)
    # * : "onmlkjihgfedcbabcdefghijklmn" (len 29)
    # p : "onmlkjihgfedcbabcdefghijklmnp" (len 30)
    # k=100 is out of bounds (final length 30)
    assert s_obj.processStr(s, k) == ".", f"Test 11 Failed: s={s}, k={k}"

    # Custom Test 9: Complex sequence with a valid k
    s = "a#b%*cd"
    k = 0
    # a -> "a"
    # # -> "aa"
    # b -> "aab"
    # % -> "baa"
    # * -> "ba"
    # c -> "bac"
    # d -> "bacd"
    # Final: "bacd", k=0 is 'b'
    assert s_obj.processStr(s, k) == "b", f"Test 12 Failed: s={s}, k={k}"

    # Custom Test 10: Empty string after ops, then append
    s = "a*b"
    k = 0
    # a -> "a"
    # * -> ""
    # b -> "b"
    # Final: "b", k=0 is 'b'
    assert s_obj.processStr(s, k) == "b", f"Test 13 Failed: s={s}, k={k}"

    # Custom Test 11: Empty string duplicated, then char
    s = "a*#b"
    k = 0
    # a -> "a"
    # * -> ""
    # # -> ""
    # b -> "b"
    # Final: "b", k=0 is 'b'
    assert s_obj.processStr(s, k) == "b", f"Test 14 Failed: s={s}, k={k}"

    print("All tests passed!")

