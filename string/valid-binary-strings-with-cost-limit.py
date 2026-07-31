"""
Valid Binary Strings With Cost Limit
Difficulty: Medium

Description:
This problem asks us to generate all binary strings of a given length `n` that satisfy two conditions: they must not contain consecutive '1's, and their "cost" (sum of indices of '1's, 0-based) must not exceed `k`. The maximum length `n` is small (up to 12), making a backtracking approach feasible.

Example:
Input: n = 3, k = 1
Output: ["000","010","100"]

Approach:
The problem is solved using a backtracking (Depth-First Search) algorithm. A recursive function `backtrack(index, current_path, current_cost, last_char_was_one)` is used to build the binary strings character by character from left to right. `index` is the current position to fill, `current_path` is a list of characters forming the string so far, `current_cost` is the sum of indices of '1's placed, and `last_char_was_one` is a boolean flag to prevent consecutive '1's.

At each `index`, the function explores two branches:
1.  **Place '0'**: A '0' can always be placed. The `current_path` is extended with '0', `current_cost` remains unchanged, and `last_char_was_one` is set to `False` for the next recursive call.
2.  **Place '1'**: A '1' can only be placed if `last_char_was_one` is `False`. If allowed, the `new_cost_if_one` (current cost plus `index`) is calculated. This branch is only pursued if `new_cost_if_one` does not exceed `k`, effectively pruning invalid paths early. If valid, '1' is appended, and `last_char_was_one` is set to `True`.

In both cases, after the recursive call, the last character is popped from `current_path` to backtrack. The base case is when `index` reaches `n`, at which point the `current_path` (which already satisfies all conditions) is joined into a string and added to the global `result` list.

Time Complexity: O(F(n+2) * n)
Space Complexity: O(F(n+2) * n)
"""
from typing import List, Optional

class Solution:
    def generateValidStrings(self, n: int, k: int) -> list[str]:
        result = []
        
        # current_path: list of characters '0' or '1' representing the string built so far
        # current_cost: sum of indices where '1's are placed in current_path
        # last_char_was_one: boolean, true if the last placed char was '1' (at index-1)
        def backtrack(index: int, current_path: list[str], current_cost: int, last_char_was_one: bool):
            # Base case: string of length n is built
            if index == n:
                result.append("".join(current_path))
                return

            # Option 1: Place '0'
            # '0' can always be placed, and it doesn't affect the cost or consecutive '1's rule.
            current_path.append('0')
            backtrack(index + 1, current_path, current_cost, False)
            current_path.pop() # Backtrack: remove '0' for the next option

            # Option 2: Place '1'
            # '1' can only be placed if the last character was not '1'
            if not last_char_was_one:
                # Calculate the new cost if '1' is placed at the current index
                new_cost_if_one = current_cost + index
                
                # Pruning: Only proceed if placing '1' does not exceed the cost limit
                if new_cost_if_one <= k:
                    current_path.append('1')
                    backtrack(index + 1, current_path, new_cost_if_one, True)
                    current_path.pop() # Backtrack: remove '1'
        
        # Start the recursion from index 0, with an empty path, 0 cost, and no previous '1'
        backtrack(0, [], 0, False)
        return result

if __name__ == "__main__":
    s = Solution()

    # Test Case 1: Example from problem description
    n1, k1 = 3, 1
    expected1 = {"000", "010", "100"}
    actual1 = set(s.generateValidStrings(n1, k1))
    assert actual1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {actual1}"
    print(f"Test Case 1 Passed (n={n1}, k={k1}): {actual1}")

    # Test Case 2: Example from problem description
    n2, k2 = 1, 0
    expected2 = {"0", "1"}
    actual2 = set(s.generateValidStrings(n2, k2))
    assert actual2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {actual2}"
    print(f"Test Case 2 Passed (n={n2}, k={k2}): {actual2}")

    # Test Case 3: n = 2, k = 1
    # Valid strings without consecutive '1's: "00", "01", "10"
    # Costs: "00"->0, "01"->1, "10"->0
    # All costs (0, 1, 0) are <= k=1
    n3, k3 = 2, 1
    expected3 = {"00", "01", "10"}
    actual3 = set(s.generateValidStrings(n3, k3))
    assert actual3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {actual3}"
    print(f"Test Case 3 Passed (n={n3}, k={k3}): {actual3}")

    # Test Case 4: n = 4, k = 2
    # Strings without consecutive '1's:
    # "0000": cost=0 (valid)
    # "0001": cost=3 (>k=2)
    # "0010": cost=2 (valid)
    # "0100": cost=1 (valid)
    # "0101": cost=1+3=4 (>k=2)
    # "1000": cost=0 (valid)
    # "1001": cost=0+3=3 (>k=2)
    # "1010": cost=0+2=2 (valid)
    n4, k4 = 4, 2
    expected4 = {"0000", "0010", "0100", "1000", "1010"}
    actual4 = set(s.generateValidStrings(n4, k4))
    assert actual4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {actual4}"
    print(f"Test Case 4 Passed (n={n4}, k={k4}): {actual4}")

    # Test Case 5: n = 5, k = 0
    # Only "00000" has cost 0.
    n5, k5 = 5, 0
    expected5 = {"00000"}
    actual5 = set(s.generateValidStrings(n5, k5))
    assert actual5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {actual5}"
    print(f"Test Case 5 Passed (n={n5}, k={k5}): {actual5}")

    # Test Case 6: n = 5, k = 100 (large k, essentially no cost limit)
    # All non-consecutive '1's strings of length 5 should be returned.
    # Count: F(5+2) = F(7) = 13 (F_1=1, F_2=1, F_3=2, F_4=3, F_5=5, F_6=8, F_7=13)
    n6, k6 = 5, 100
    all_non_consecutive_strings = {
        "00000", "00010", "00100", "00101",
        "01000", "01001", "01010",
        "10000", "10010", "10100", "10101"
    } # Verified manually for non-consecutive '1's of length 5 (missing "00001" and "10001", "00101" for cost reasons usually).
      # Re-checking: Fibonacci numbers for strings without consecutive 1s start F(0)=1 (""), F(1)=2("0","1"), F(2)=3("00","01","10")
      # So for length n, it's F(n+2). F(7)=13, not 11 as manually listed.
      # The missing ones with "1" at index 4 (0-based) must have cost >= 4.
      # "00001" (cost 4), "00010" (cost 3), "00100" (cost 2), "00101" (cost 2+4=6),
      # "01000" (cost 1), "01001" (cost 1+4=5), "01010" (cost 1+3=4),
      # "10000" (cost 0), "10010" (cost 3), "10100" (cost 2), "10101" (cost 2+4=6)
      # Okay, my manual list was for length 5 strings *without* consecutive '1's.
      # "00000", "00010", "00100", "00101", "01000", "01001", "01010", "10000", "10010", "10100", "10101" -- this is 11 strings
      # The 2 missing strings are "00001" (cost 4), "10001" (cost 4).
      # So 13 strings for n=5:
      # {"00000", "00001", "00010", "00100", "00101", "01000", "01001", "01010", "10000", "10001", "10010", "10100", "10101"}
    expected6 = {"00000", "00001", "00010", "00100", "00101", "01000", "01001", "01010", "10000", "10001", "10010", "10100", "10101"}
    actual6 = set(s.generateValidStrings(n6, k6))
    assert actual6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {actual6}"
    print(f"Test Case 6 Passed (n={n6}, k={k6}): {actual6}")

    print("All tests passed!")

