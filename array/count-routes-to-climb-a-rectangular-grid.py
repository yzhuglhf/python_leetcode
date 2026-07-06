"""
Count Routes to Climb a Rectangular Grid
Difficulty: Hard

Description:
This problem asks us to count distinct routes to climb a rectangular grid from any cell in the bottom row (n-1) to any cell in the top row (0). Moves are restricted to available cells, have a maximum Euclidean distance 'd', and can only move to the same row or the row directly above (r to r-1). A critical constraint is that staying on the same row for two consecutive turns is forbidden, unless the second turn is the final move to the top row. The final count must be returned modulo 10^9 + 7.

Example:
Input: grid = ["..","#."], d = 1
Output: 2
Explanation: The grid is 2x2. The two routes are:
1. Start at (1,1), move to (0,1). (Euclidean distance 1, valid)
2. Start at (1,1), move to (0,1), then move to (0,0). (First move distance 1, second move distance 1. Both valid.)
Note that for the second route, the move (0,1) -> (0,0) stays on the same row, but it's the last move to the top row, so it's allowed.

Approach:
This is a dynamic programming problem. We define `dp[r][c][state]` to count the number of distinct routes to reach cell `(r, c)`. The `state` variable is used to track the nature of the previous move, which is critical for enforcing the "cannot stay on the same row for two consecutive turns" constraint.
- `dp[r][c][0]`: Number of ways to reach `(r, c)` where the immediately preceding move was from `(r+1, c_prev)` (i.e., moved upwards from the row below).
- `dp[r][c][1]`: Number of ways to reach `(r, c)` where the immediately preceding move was from `(r, c_prev)` (i.e., stayed on the same row).

The DP transitions proceed row by row, from the bottom row (n-1) up to the top row (0):

1.  **Base Case (Row n-1):** For each available cell `(n-1, c)` in the bottom row, we initialize `dp[n-1][c][0] = 1`. This represents the start of a route. `dp[n-1][c][1]` remains 0, as a route cannot "stay on the same row" for its very first move.

2.  **Iterate `r` from `n-2` down to `1` (Intermediate Rows):**
    For each row `r`, we compute `dp[r][c][0]` and `dp[r][c][1]` for all available cells `(r, c)`.
    a.  **Calculating `dp[r][c][0]`**: A cell `(r, c)` can be reached from any `(r+1, c_prev)` such that the Euclidean distance `sqrt(((r+1)-r)^2 + (c_prev - c)^2) <= d`. This simplifies to `(c_prev - c)^2 <= d^2 - 1`. The `max_col_offset_up` is pre-calculated as `floor(sqrt(d^2 - 1))`. The previous move to `(r+1, c_prev)` could have been either `(r+2, ...)` to `(r+1, c_prev)` or `(r+1, ...)` to `(r+1, c_prev)`. Thus, `dp[r][c][0]` sums `(dp[r+1][c_prev][0] + dp[r+1][c_prev][1])` for all valid `c_prev` within the allowed column range.
    b.  **Calculating `dp[r][c][1]`**: A cell `(r, c)` can be reached from any `(r, c_prev)` (`c_prev != c`) such that `|c_prev - c| <= d`. Due to the "cannot stay on the same row for two consecutive turns" constraint, the previous move *to* `(r, c_prev)` must have been from `(r+1, ...)`. Hence, `dp[r][c][1]` sums only `dp[r][c_prev][0]` for valid `c_prev`.

3.  **Special Handling for Row `0` (Top Row):**
    The rules change for the top row because any move to row `0` is considered the *last* move of a route. Thus, the "cannot stay on the same row for two consecutive turns" constraint does not apply to a `(0, c_prev) -> (0, c)` move.
    a.  **Calculating `dp[0][c][0]`**: If `n > 1`, this is computed similarly to step 2a, but from `dp[1]` values. If `n=1`, `dp[0][c][0]` is already set by the base case.
    b.  **Calculating `dp[0][c][1]`**: For the top row, a `(0, c_prev) -> (0, c)` move is always valid. Therefore, `dp[0][c][1]` should sum `(dp[0][c_prev][0] + dp[0][c_prev][1])` for all valid `c_prev` (`c_prev != c`). This creates a dependency within the same row (`dp[0][c][1]` depends on `dp[0][c_prev][1]`), necessitating an iterative approach (like Bellman-Ford or repeated sweep-line passes) on row 0. We iterate `m+1` times to ensure all paths of varying lengths on row 0 are counted.

To optimize the range sums (which would otherwise be `O(M)`), prefix sums are used. For each row, relevant prefix sum arrays are computed in `O(M)` time, allowing each cell's DP value to be calculated in `O(1)`.

**Final Answer:**
Sum all `dp[0][c][0]` and `dp[0][c][1]` for all available cells `(0, c)` in the top row. All calculations are performed modulo `10^9 + 7`.

Time Complexity: O(N * M + M^2) - The main loop iterates N times. Inside, prefix sum calculations take O(M). The special handling for row 0 involves an iterative process that runs M+1 times, and each iteration takes O(M) for prefix sums and updates. Thus, `O(N*M)` for general rows and `O(M^2)` for the top row. Given N, M <= 750, this is approximately `750*750 + 750*750 = 2 * (5.6 * 10^5)` operations, which is efficient enough.
Space Complexity: O(N * M) - For the `dp` table.
"""
from typing import List
import math

class Solution:
    def numberOfRoutes(self, grid: List[str], d: int) -> int:
        n = len(grid)
        m = len(grid[0])
        MOD = 10**9 + 7

        # dp[r][c][0]: ways to reach (r, c) with last move from (r+1, c_prev)
        # dp[r][c][1]: ways to reach (r, c) with last move from (r, c_prev)
        dp = [[[0] * 2 for _ in range(m)] for _ in range(n)]

        # Pre-calculate max_col_offset_up for moves from r+1 to r
        # Euclidean distance: sqrt( ( (r+1)-r )^2 + (c_prev - c)^2 ) <= d
        # => 1 + (c_prev - c)^2 <= d^2
        # => (c_prev - c)^2 <= d^2 - 1
        # max_col_offset_up = floor(sqrt(max(0, d^2 - 1)))
        max_col_offset_up = math.isqrt(max(0, d * d - 1)) 

        # Base Case: bottom row (n - 1)
        for c in range(m):
            if grid[n - 1][c] == '.':
                dp[n - 1][c][0] = 1 # Can start from any available cell in the bottom row

        # Iterate rows from n-2 down to 1 (intermediate rows, not the very top row)
        for r in range(n - 2, 0, -1):
            # 1. Calculate dp[r][c][0] (moves from r+1 to r)
            prefix_sum_prev_row_total_dp = [0] * (m + 1)
            for c_prev in range(m):
                val_at_c_prev = 0
                if grid[r + 1][c_prev] == '.':
                    val_at_c_prev = (dp[r + 1][c_prev][0] + dp[r + 1][c_prev][1]) % MOD
                prefix_sum_prev_row_total_dp[c_prev + 1] = (prefix_sum_prev_row_total_dp[c_prev] + val_at_c_prev) % MOD

            for c in range(m):
                if grid[r][c] == '.':
                    left_col = max(0, c - max_col_offset_up)
                    right_col = min(m - 1, c + max_col_offset_up)
                    count = (prefix_sum_prev_row_total_dp[right_col + 1] - prefix_sum_prev_row_total_dp[left_col] + MOD) % MOD
                    dp[r][c][0] = count
            
            # 2. Calculate dp[r][c][1] (moves from r to r) for intermediate rows (r > 0)
            # The previous cell (r, c_prev) must have been reached from row r+1.
            current_row_dp0_prefix_sum = [0] * (m + 1)
            for c_prev in range(m):
                val_at_c_prev = dp[r][c_prev][0] 
                current_row_dp0_prefix_sum[c_prev + 1] = (current_row_dp0_prefix_sum[c_prev] + val_at_c_prev) % MOD

            for c in range(m):
                if grid[r][c] == '.':
                    left_col = max(0, c - d)
                    right_col = min(m - 1, c + d)
                    count = (current_row_dp0_prefix_sum[right_col + 1] - current_row_dp0_prefix_sum[left_col] + MOD) % MOD
                    count = (count - dp[r][c][0] + MOD) % MOD # Exclude move to same cell (c_prev != c)
                    dp[r][c][1] = count

        # Special handling for row 0 (the top row)
        # This part runs whether n=1 (r=0 is the only row) or n>1 (r=0 is the top of many rows).
        r = 0
        
        # If n > 1, compute dp[0][c][0] based on dp[1]
        # If n = 1, dp[0][c][0] is already correctly initialized in the base case
        if n > 1:
            prefix_sum_prev_row_total_dp = [0] * (m + 1)
            for c_prev in range(m):
                val_at_c_prev = 0
                if grid[r + 1][c_prev] == '.':
                    val_at_c_prev = (dp[r + 1][c_prev][0] + dp[r + 1][c_prev][1]) % MOD
                prefix_sum_prev_row_total_dp[c_prev + 1] = (prefix_sum_prev_row_total_dp[c_prev] + val_at_c_prev) % MOD

            for c in range(m):
                if grid[r][c] == '.':
                    left_col = max(0, c - max_col_offset_up)
                    right_col = min(m - 1, c + max_col_offset_up)
                    count = (prefix_sum_prev_row_total_dp[right_col + 1] - prefix_sum_prev_row_total_dp[left_col] + MOD) % MOD
                    dp[r][c][0] = count

        # Calculate dp[0][c][1] (moves from 0 to 0)
        # On the top row, any 'stay on same row' move is valid as it's the last move.
        # So, dp[0][c][1] can accumulate routes from (dp[0][c_prev][0] + dp[0][c_prev][1]).
        # This requires an iterative process (Bellman-Ford-like) to propagate routes across row 0.
        # We perform m+1 iterations to ensure all distinct paths of length up to M are considered.
        for _ in range(m + 1): 
            # Build prefix sums for the current sum of (dp[0][c_prev][0] + dp[0][c_prev][1])
            current_dp0_total_prefix_sum = [0] * (m + 1)
            for c_prev in range(m):
                val_at_c_prev = (dp[0][c_prev][0] + dp[0][c_prev][1]) % MOD
                current_dp0_total_prefix_sum[c_prev + 1] = (current_dp0_total_prefix_sum[c_prev] + val_at_c_prev) % MOD

            # Update dp[0][c][1] for each cell in row 0
            for c in range(m):
                if grid[0][c] == '.':
                    left_col = max(0, c - d)
                    right_col = min(m - 1, c + d)
                    
                    # Sum contributions from c_prev in range [left_col, right_col]
                    count_from_prev_c = (current_dp0_total_prefix_sum[right_col + 1] - current_dp0_total_prefix_sum[left_col] + MOD) % MOD
                    
                    # Subtract current cell's own total (dp[0][c][0] + dp[0][c][1])
                    # because a move implies c_prev != c.
                    # Add 2*MOD to handle potential negative results from subtraction before final modulo.
                    count_from_prev_c = (count_from_prev_c - (dp[0][c][0] + dp[0][c][1]) + 2 * MOD) % MOD
                    
                    # Accumulate these new ways into dp[0][c][1].
                    # Each iteration adds routes of a specific path length.
                    dp[0][c][1] = (dp[0][c][1] + count_from_prev_c) % MOD

        # Final summation for total routes ending in row 0
        total_routes = 0
        for c in range(m):
            total_routes = (total_routes + dp[0][c][0] + dp[0][c][1]) % MOD

        return total_routes

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.numberOfRoutes(grid=["..","#."], d=1) == 2, "Example 1 Failed"
    # Example 2
    assert s.numberOfRoutes(grid=["..","#."], d=2) == 4, "Example 2 Failed"
    # Example 3
    assert s.numberOfRoutes(grid=["#"], d=750) == 0, "Example 3 Failed"
    # Example 4
    assert s.numberOfRoutes(grid=[".."], d=1) == 4, "Example 4 Failed"
    
    # Custom Test 1: Simple 3x3 grid
    grid_3x3 = [
        "...",
        ".#.",
        "..."
    ]
    # d=1: (2,0)->(1,0) (no), (2,1)->(1,1) (no), (2,2)->(1,2) (no)
    # (2,0) cannot move to (1,0) directly as (1,0) is blocked.
    # (2,0) cannot move to (1,1) dist sqrt(1^2+1^2)=sqrt(2)>1.
    # So if d=1, routes cannot go up. Only if n=1 (already handled).
    # If d=1, n=3, output should be 0.
    assert s.numberOfRoutes(grid=grid_3x3, d=1) == 0, "Custom Test 1.1 Failed"
    
    # d=2: now diagonal moves (c_prev = c +/- 1) are allowed for 1-row-up moves.
    # (2,0) can move to (1,1) because dist sqrt(2) <= 2.
    # Bottom row available: (2,0), (2,1), (2,2)
    # Row 1 available: (1,1)
    # Row 0 available: (0,0), (0,1), (0,2)

    # Base: dp[2][0][0]=1, dp[2][1][0]=1, dp[2][2][0]=1. All others 0.

    # r = 1 (intermediate row)
    # dp[1][c][0]: moves from r+1=2 to r=1
    #   max_col_offset_up = floor(sqrt(2*2-1)) = floor(sqrt(3)) = 1
    #   c=0: grid[1][0] is '#'. Skip.
    #   c=1: grid[1][1] is '.'.
    #     From (2,0): (2,0) to (1,1). Dist sqrt(2)<=2. c_prev=0. (dp[2][0][0]+dp[2][0][1])=1+0=1
    #     From (2,1): (2,1) to (1,1). Dist 1<=2. c_prev=1. (dp[2][1][0]+dp[2][1][1])=1+0=1
    #     From (2,2): (2,2) to (1,1). Dist sqrt(2)<=2. c_prev=2. (dp[2][2][0]+dp[2][2][1])=1+0=1
    #     dp[1][1][0] = 1+1+1 = 3.
    #   c=2: grid[1][2] is '#'. Skip.

    # dp[1][c][1]: moves from r=1 to r=1. d=2.
    #   No valid previous cells on row 1 (all are '#'). So dp[1][c][1]=0 for all c.

    # r = 0 (top row)
    # dp[0][c][0]: moves from r+1=1 to r=0
    #   max_col_offset_up = 1
    #   c=0: grid[0][0] is '.'.
    #     From (1,1): (1,1) to (0,0). Dist sqrt(2)<=2. (dp[1][1][0]+dp[1][1][1])=3+0=3.
    #     dp[0][0][0] = 3.
    #   c=1: grid[0][1] is '.'.
    #     From (1,1): (1,1) to (0,1). Dist 1<=2. (dp[1][1][0]+dp[1][1][1])=3+0=3.
    #     dp[0][1][0] = 3.
    #   c=2: grid[0][2] is '.'.
    #     From (1,1): (1,1) to (0,2). Dist sqrt(2)<=2. (dp[1][1][0]+dp[1][1][1])=3+0=3.
    #     dp[0][2][0] = 3.

    # dp[0][c][1]: iterative Bellman-Ford on row 0.
    # Initial: dp[0][0][0]=3, dp[0][1][0]=3, dp[0][2][0]=3. All dp[0][c][1]=0.
    # Iteration 1: (using values at start of iter)
    #   prefix_sum_total = [0, (3+0), (3+0)+(3+0), (3+0)+(3+0)+(3+0)] = [0,3,6,9]
    #   c=0: dp[0][0][1] = paths from (0,1), (0,2) to (0,0).
    #     (d=2, so from c_prev in [0-2, 0+2] excluding 0 => [1,2])
    #     contrib from (0,1) and (0,2) (which are 3,3 resp.): 3+3 = 6.
    #     (6 - (dp[0][0][0]+dp[0][0][1])) = (6 - (3+0)) = 3.
    #     dp[0][0][1] = 0 + 3 = 3.
    #   c=1: dp[0][1][1] = paths from (0,0), (0,2) to (0,1).
    #     contrib from (0,0) and (0,2): 3+3=6.
    #     (6 - (dp[0][1][0]+dp[0][1][1])) = (6 - (3+0)) = 3.
    #     dp[0][1][1] = 0 + 3 = 3.
    #   c=2: dp[0][2][1] = paths from (0,0), (0,1) to (0,2).
    #     contrib from (0,0) and (0,1): 3+3=6.
    #     (6 - (dp[0][2][0]+dp[0][2][1])) = (6 - (3+0)) = 3.
    #     dp[0][2][1] = 0 + 3 = 3.
    # After Iter 1: dp[0][c][0]=3, dp[0][c][1]=3 for c in [0,1,2]. Total = 6*3 = 18.
    # Iteration 2:
    #   prefix_sum_total = [0, (3+3), (3+3)+(3+3), (3+3)+(3+3)+(3+3)] = [0,6,12,18]
    #   c=0: dp[0][0][1]. contrib from (0,1),(0,2) -> (0,0) sum (dp[0][1][0]+dp[0][1][1]) + (dp[0][2][0]+dp[0][2][1]) = 6+6=12.
    #     (12 - (dp[0][0][0]+dp[0][0][1])) = (12 - (3+3)) = 6.
    #     dp[0][0][1] = 3 + 6 = 9.
    # ... and so on.
    # Each iteration adds `(2^k * initial_total)`?
    # No, it's total paths from other cells.
    # The count will reach `m * initial_val` for each cell.
    # 3 * 3 = 9 initial paths that go 1 step (to a neighbor)
    # Total paths for (0,0) are: (0,0) initial (3), (0,1)->(0,0) (3), (0,2)->(0,0) (3)
    # Total for (0,0) is 3 + (3+3) = 9.
    # This seems like it will be total_routes = 3 * (1 + 2 * (m-1))
    # It depends on path length.
    # The total for each cell (0,c) from initial dp[0][c][0] is 3.
    # For a given cell (0,c), it can be reached from (0, c_prev) where c_prev in [max(0,c-d), min(m-1, c+d)] excluding c.
    # If d is large enough (e.g. m-1), then each cell can reach any other cell in one step.
    # In this case (m=3, d=2): Each cell can reach 2 other cells in one step.
    # Total routes ending at (0,0) is `dp[0][0][0] + dp[0][0][1]`.
    # `dp[0][0][0]`=3 (from row 1).
    # `dp[0][0][1]` comes from (0,1) and (0,2). Total paths to (0,1) or (0,2) are sum (dp[0][c'][0]+dp[0][c'][1]).
    # Initial states: [3,0],[3,0],[3,0]
    # Iter 1:
    # `dp[0][0][1]` receives 3 from (0,1) and 3 from (0,2). Total 6. `dp[0][0][1]=6`.
    # `dp[0][1][1]` receives 3 from (0,0) and 3 from (0,2). Total 6. `dp[0][1][1]=6`.
    # `dp[0][2][1]` receives 3 from (0,0) and 3 from (0,1). Total 6. `dp[0][2][1]=6`.
    # After iter 1: `dp[0]` totals are [3+6, 3+6, 3+6] = [9,9,9].
    # Total is 27.
    # Let's check with `m=2, d=1`: 4 routes. My previous trace got 4 routes.
    # Here, initial `dp[0][0][0]=1, dp[0][1][0]=1`.
    # Iter 1:
    # `dp[0][0][1]` receives 1 from (0,1). `dp[0][0][1]=1`.
    # `dp[0][1][1]` receives 1 from (0,0). `dp[0][1][1]=1`.
    # After iter 1: dp[0] totals are [1+1, 1+1] = [2,2]. Total 4.
    # This logic is consistent with the `m+1` iterations.
    # So for 3x3, d=2.
    # Total routes = sum(dp[0][c][0]+dp[0][c][1])
    # The sum of (dp[0][c][0]+dp[0][c][1]) at the end of each iteration `k` gives number of paths with up to `k` intra-row moves.
    # For `m=3, d=2`, the total possible routes are 3 starts. Each can move to 2 other cells.
    # (2,0)->(1,1)->(0,0)
    # (2,0)->(1,1)->(0,1)
    # (2,0)->(1,1)->(0,2)
    # (2,1)->(1,1)->(0,0)
    # ...
    # From 3 base starts, 3 paths reach (1,1). From (1,1), 3 paths reach (0,0). 3 paths reach (0,1). 3 paths reach (0,2).
    # This is 3 * 3 = 9 routes that use 1 vertical move and 0 horizontal moves. (dp[0][c][0] are 3 each)
    # From (0,0), can move to (0,1) (from (2,0)->(1,1)->(0,0) then to (0,1)).
    # And (0,0) can move to (0,2).
    # After iter 1, total sum (dp[0][c][0]+dp[0][c][1]) is 9 for each cell.
    # So total paths = 3 * 9 = 27.
    assert s.numberOfRoutes(grid=grid_3x3, d=2) == 27, "Custom Test 1.2 Failed"

    print("All tests passed!")

