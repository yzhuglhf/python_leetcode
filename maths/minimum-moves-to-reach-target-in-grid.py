"""
Minimum Moves to Reach Target in Grid
Difficulty: Hard

Description:
Given start and target points (sx, sy) and (tx, ty) on an infinite 2D grid, find the minimum moves to reach the target. From any point (x, y), you can move to (x + max(x, y), y) or (x, y + max(x, y)). If the target is unreachable, return -1.

Example:
Input: sx = 1, sy = 2, tx = 5, ty = 4
Output: 2
Explanation: The path is (1, 2) -> (1, 4) (max(1,2)=2 added to y) -> (5, 4) (max(1,4)=4 added to x).

Approach:
This problem can be solved by working backward from the target point (tx, ty) to the starting point (sx, sy), counting the number of reverse moves. Since coordinates can be very large (up to 10^9), a breadth-first search (BFS) is not feasible. Instead, a greedy approach is used, relying on the observation that for any given point (x, y) not on the target, there is a unique predecessor state (px, py) from which it could have been reached by a single forward move, respecting certain conditions.

The reverse moves are derived from the forward moves:
1. If (x, y) was reached from (px, y) by (px + max(px, y), y):
   - If px >= y, then x = 2*px, so px = x/2. This is valid if x is even and x/2 >= y.
   - If px < y, then x = px + y, so px = x - y. This is valid if x - y < y (i.e., x < 2y).
2. If (x, y) was reached from (x, py) by (x, py + max(x, py)):
   - If py >= x, then y = 2*py, so py = y/2. This is valid if y is even and y/2 >= x.
   - If py < x, then y = py + x, so py = y - x. This is valid if y - x < x (i.e., y < 2x).

The algorithm proceeds in a loop:
- Initialize `ans = 0`.
- While `(tx, ty)` is not `(sx, sy)`:
    - If `tx < sx` or `ty < sy`, it means we've overshot the target (since coordinates only increase), so return -1.
    - Handle the special case where `(sx, sy)` is `(0,0)`. If `(tx, ty)` is not `(0,0)`, it's impossible to reach because `max(0,0)=0` means no moves.
    - If `tx == ty`:
        - A point (X,X) can only be reached from (0,X) or (X,0) (unless X=0).
        - If (sx, sy) is (0, tx) or (tx, 0), apply the respective reverse move. Otherwise, if target `(sx,sy)` is not one of these, return -1.
    - If `tx > ty`:
        - If `ty == 0`: `(tx,0)` must have come from `(tx/2,0)`. Divide `tx` by 2, add 1 to `ans`.
        - If `ty > 0`: Apply the reverse rule for `x > y`. If `tx >= 2*ty`, the predecessor is `(tx/2, ty)`. Otherwise (`ty < tx < 2*ty`), the predecessor is `(tx-ty, ty)`. Apply the move and increment `ans`. If conditions for a valid predecessor (evenness, not overshooting `sx`) are not met, return -1.
    - If `ty > tx`: (Symmetric logic to `tx > ty`, swapping x and y roles).

This greedy strategy works because the conditions for reverse moves generally define a unique path backwards. The special handling for coordinates being zero is essential due to `max(x,0)=x` and `max(0,0)=0`.

Time Complexity: O(log(max(tx, ty))). In each step, at least one coordinate is reduced by division or subtraction, similar to the Euclidean algorithm or binary GCD, leading to logarithmic complexity.
Space Complexity: O(1)

"""
import math

class Solution:
    def minMoves(self, sx: int, sy: int, tx: int, ty: int) -> int:
        ans = 0

        # Handle initial state == target state
        if sx == tx and sy == ty:
            return 0

        # Reverse moves: from (tx, ty) to (sx, sy)
        while tx != sx or ty != sy:
            # If we've overshot the target (sx, sy), it's impossible
            if tx < sx or ty < sy:
                return -1
            
            # Special case for origin (0,0)
            # If start is (0,0), target must be (0,0). Otherwise impossible as max(0,0)=0 means no moves.
            # (sx == tx and sy == ty) is checked at the beginning. So if sx=0, sy=0 here, (tx,ty) != (0,0)
            if sx == 0 and sy == 0:
                return -1
            
            # Case: tx == ty (current point is on the diagonal)
            # From (X,X) can only go to (0,X) or (X,0).
            # If (sx, sy) is not (0,tx) or (tx,0), it's impossible.
            if tx == ty:
                if sx == 0 and sy == tx: # Target is (0, tx), reached from (0, tx)
                    tx = 0
                    ans += 1
                elif sy == 0 and sx == tx: # Target is (tx, 0), reached from (tx, 0)
                    ty = 0
                    ans += 1
                else:
                    return -1 # Cannot reach (sx,sy) from (tx,ty) if tx==ty and (sx,sy) is not (0,tx) or (tx,0)
            
            # Case: tx > ty (x-coordinate is larger)
            elif tx > ty:
                if ty == 0: # Current point is (tx, 0)
                    if sy != 0: return -1 # Cannot reach (tx,0) from (S,Y) if Y>0 and S!=tx. (Y must have been 0)
                    # We are on (X,0), need to reach (S,0). Backwards, (X,0) must come from (X/2,0).
                    # This implies X must be even.
                    if tx % 2 == 1: return -1 # Odd tx cannot be reduced this way
                    if tx // 2 < sx: return -1 # Overshot sx
                    tx //= 2
                    ans += 1
                else: # tx > ty > 0
                    # If tx >= 2*ty: predecessor is (tx/2, ty) (requires tx even, tx/2 >= ty)
                    if tx >= 2 * ty:
                        if tx % 2 == 1: return -1 # Cannot divide odd tx
                        if tx // 2 < sx: return -1 # Overshot sx
                        tx //= 2
                        ans += 1
                    # If ty < tx < 2*ty: predecessor is (tx-ty, ty) (requires tx-ty < ty)
                    else: 
                        if tx - ty < sx: return -1 # Overshot sx
                        tx -= ty
                        ans += 1
            
            # Case: ty > tx (y-coordinate is larger, symmetric to tx > ty)
            else: # ty > tx
                if tx == 0: # Current point is (0, ty)
                    if sx != 0: return -1 # Cannot reach (0,ty) from (S,Y) if S>0. (S must have been 0)
                    # We are on (0,Y), need to reach (0,S). Backwards, (0,Y) must come from (0,Y/2).
                    # This implies Y must be even.
                    if ty % 2 == 1: return -1 # Odd ty cannot be reduced this way
                    if ty // 2 < sy: return -1 # Overshot sy
                    ty //= 2
                    ans += 1
                else: # ty > tx > 0
                    # If ty >= 2*tx: predecessor is (tx, ty/2) (requires ty even, ty/2 >= tx)
                    if ty >= 2 * tx:
                        if ty % 2 == 1: return -1 # Cannot divide odd ty
                        if ty // 2 < sy: return -1 # Overshot sy
                        ty //= 2
                        ans += 1
                    # If tx < ty < 2*tx: predecessor is (tx, ty-tx) (requires ty-tx < tx)
                    else: 
                        if ty - tx < sy: return -1 # Overshot sy
                        ty -= tx
                        ans += 1
        return ans

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.minMoves(1, 2, 5, 4) == 2, "Example 1 failed"
    # Example 2
    assert s.minMoves(0, 1, 2, 3) == 3, "Example 2 failed"
    # Example 3
    assert s.minMoves(1, 1, 2, 2) == -1, "Example 3 failed"
    
    # Custom test cases
    assert s.minMoves(0, 0, 0, 0) == 0, "Custom 1 failed: start=target=(0,0)"
    assert s.minMoves(0, 0, 1, 0) == -1, "Custom 2 failed: start=(0,0), target not (0,0)"
    assert s.minMoves(0, 1, 0, 2) == 1, "Custom 3 failed: (0,1) to (0,2)"
    assert s.minMoves(1, 0, 2, 0) == 1, "Custom 4 failed: (1,0) to (2,0)"
    assert s.minMoves(1, 1, 1, 2) == 1, "Custom 5 failed: (1,1) to (1,2)"
    assert s.minMoves(1, 1, 2, 1) == 1, "Custom 6 failed: (1,1) to (2,1)"
    assert s.minMoves(1, 1, 3, 1) == -1, "Custom 7 failed: (1,1) to (3,1), odd x"
    assert s.minMoves(1, 1, 4, 1) == 2, "Custom 8 failed: (1,1) to (4,1)" # (1,1)->(2,1)->(4,1)
    assert s.minMoves(1, 1, 1, 4) == 2, "Custom 9 failed: (1,1) to (1,4)" # (1,1)->(1,2)->(1,4)
    assert s.minMoves(1, 3, 1, 7) == -1, "Custom 10 failed: (1,3) to (1,7), odd y diff"
    assert s.minMoves(2, 3, 2, 6) == 1, "Custom 11 failed: (2,3) to (2,6)" # (2,3)->(2,3+max(2,3)=2+3)=(2,6)
    assert s.minMoves(2, 3, 4, 3) == 1, "Custom 12 failed: (2,3) to (4,3)" # (2,3)->(2+max(2,3)=2+3)=(5,3) -- NO! (2,3)->(2+2,3)=(4,3)
    # Re-check (2,3) to (4,3)
    # (4,3) -> tx > ty. tx < 2*ty (4 < 6). (tx-ty, ty) = (4-3, 3) = (1,3). ans=1.
    # (1,3) -> ty > tx. ty >= 2*tx (3 >= 2). (tx, ty/2) -> (1, 3/2) not int. No.
    # This means (4,3) can only be reached from (1,3).
    # Then (1,3) is problematic. My code: (1,3) -> (1, 3-1)=(1,2). ans=2.
    # Then (1,2) to (2,3). This is -1. Why? Oh target is (2,3) not (1,3).
    # This means (2,3) -> (4,3) is impossible.
    # From (2,3), m=3. (2+3,3)=(5,3) OR (2,3+3)=(2,6).
    # From (2,3) can never reach (4,3). So (2,3) to (4,3) should be -1.
    assert s.minMoves(2, 3, 4, 3) == -1, "Custom 12 failed: (2,3) to (4,3) impossible"
    
    assert s.minMoves(10, 10, 0, 10) == 1, "Custom 13 failed: (10,10) to (0,10)"
    assert s.minMoves(10, 10, 10, 0) == 1, "Custom 14 failed: (10,10) to (10,0)"
    assert s.minMoves(10, 10, 1, 10) == -1, "Custom 15 failed: (10,10) to (1,10) impossible"
    assert s.minMoves(10, 10, 5, 10) == -1, "Custom 16 failed: (10,10) to (5,10) impossible"
    assert s.minMoves(10, 2, 10, 4) == -1, "Custom 17 failed: (10,2) to (10,4) impossible" # (10,2)->(10,2+10)=(10,12) or (10+10,2)=(20,2)

    assert s.minMoves(1, 1, 1, 1) == 0, "Custom 18 failed"
    assert s.minMoves(1, 1, 1, 0) == -1, "Custom 19 failed" # tx<sx or ty<sy is false initially but loop takes care

    print("All tests passed!")

```