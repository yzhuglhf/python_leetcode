"""
Maximum Manhattan Distance After All Moves
Difficulty: Medium

Description:
This problem asks us to find the maximum Manhattan distance from the origin (0, 0) after performing a sequence of moves. The moves can be 'U', 'D', 'L', 'R' (fixed directions) or '_' (a wildcard that can be replaced by any of 'U', 'D', 'L', 'R'). We want to maximize `|x| + |y|` for the final coordinates `(x, y)`.

Example:
Input: moves = "L_D_"
Output: 4
Explanation: After fixed moves 'L' and 'D', we are at (-1, -1) and have 2 wildcards. Each wildcard can be used to increase the Manhattan distance by 1, e.g., by choosing them as 'L' and 'D' respectively to reach (-2, -2). The final Manhattan distance is |-2| + |-2| = 4.

Approach:
The Manhattan distance is defined as `|x| + |y|`. We start at the origin (0, 0).
First, we iterate through the `moves` string to calculate the net displacement from the fixed moves ('U', 'D', 'L', 'R') and count the number of wildcard moves ('_').
Let `x_coord` and `y_coord` be the coordinates after all 'U', 'D', 'L', 'R' moves have been processed. Let `blanks` be the count of '_' characters.

Each wildcard move ('_') can be chosen to be 'U', 'D', 'L', or 'R'. We want to maximize `|x_final| + |y_final|`.
Consider the effect of a move on the Manhattan distance `|x| + |y|`:
- A move 'R' (increases `x` by 1): If `x` is non-negative, `|x|` increases by 1. If `x` is negative, `|x|` decreases by 1 (unless `x` crosses zero).
- A move 'L' (decreases `x` by 1): If `x` is non-positive, `|x|` increases by 1. If `x` is positive, `|x|` decreases by 1.
Similar logic applies to 'U' and 'D' for the `y` coordinate.

The crucial insight is that for any current position `(x, y)`, we can always choose a wildcard move such that it increases the Manhattan distance `|x| + |y|` by 1.
- If `x >= 0`, we can choose 'R'. The new `x` becomes `x+1`, and `|x+1| = |x|+1`. The total distance `|x|+|y|` increases by 1.
- If `x < 0`, we can choose 'L'. The new `x` becomes `x-1`, and `|x-1| = |x|+1`. The total distance `|x|+|y|` increases by 1.
The same logic applies to the `y` coordinate:
- If `y >= 0`, we can choose 'U'. The new `y` becomes `y+1`, and `|y+1| = |y|+1`.
- If `y < 0`, we can choose 'D'. The new `y` becomes `y-1`, and `|y-1| = |y|+1`.

Since each wildcard can be independently chosen to increase `|x|` or `|y|` by 1 (by moving further away from the origin along that specific axis), each of the `blanks` wildcards can contribute an additional +1 to the total Manhattan distance.
Therefore, the maximum Manhattan distance is simply `abs(x_coord) + abs(y_coord) + blanks`.

Time Complexity: O(N), where N is the length of the `moves` string, as we iterate through the string once.
Space Complexity: O(1), as we only use a few constant-space variables to store coordinates and wildcard counts.
"""
from typing import List, Optional

class Solution:
    def maxDistance(self, moves: str) -> int:
        x_coord = 0
        y_coord = 0
        blanks = 0

        for move in moves:
            if move == 'U':
                y_coord += 1
            elif move == 'D':
                y_coord -= 1
            elif move == 'L':
                x_coord -= 1
            elif move == 'R':
                x_coord += 1
            else:  # move == '_'
                blanks += 1
        
        # The maximum Manhattan distance is the sum of absolute coordinates
        # from the fixed moves, plus the number of wildcards. Each wildcard
        # can be strategically used to increase the total Manhattan distance by 1.
        return abs(x_coord) + abs(y_coord) + blanks

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.maxDistance("L_D_") == 4, f"Test Case 1 Failed: Expected 4, got {s.maxDistance('L_D_')}"
    
    # Example 2
    assert s.maxDistance("U_R") == 3, f"Test Case 2 Failed: Expected 3, got {s.maxDistance('U_R')}"
    
    # Custom Test Case 1: All fixed moves, resulting in origin
    assert s.maxDistance("UDLR") == 0, f"Test Case 3 Failed: Expected 0, got {s.maxDistance('UDLR')}"
    
    # Custom Test Case 2: Fixed moves with a net displacement, no blanks
    assert s.maxDistance("UUUR") == 4, f"Test Case 4 Failed: Expected 4, got {s.maxDistance('UUUR')}" # (1,3) -> |1|+|3|=4
    
    # Custom Test Case 3: All blanks
    assert s.maxDistance("___") == 3, f"Test Case 5 Failed: Expected 3, got {s.maxDistance('___')}" # (0,0) with 3 blanks -> 0+0+3=3
    
    # Custom Test Case 4: Mixed, some moves cancel out, blanks remaining
    assert s.maxDistance("R_L") == 1, f"Test Case 6 Failed: Expected 1, got {s.maxDistance('R_L')}" # (0,0) with 1 blank -> 0+0+1=1
    
    # Custom Test Case 5: Complex mix
    assert s.maxDistance("ULDR_R_U_D") == 4, f"Test Case 7 Failed: Expected 4, got {s.maxDistance('ULDR_R_U_D')}"
    # U: (0,1)
    # L: (-1,1)
    # D: (-1,0)
    # R: (0,0)
    # _: (0,0), blanks=1
    # R: (1,0), blanks=1
    # _: (1,0), blanks=2
    # U: (1,1), blanks=2
    # _: (1,1), blanks=3
    # D: (1,0), blanks=3
    # Final: x=1, y=0, blanks=3 -> abs(1)+abs(0)+3 = 4

    print("All tests passed!")

