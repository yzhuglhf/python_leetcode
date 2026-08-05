"""
Create Grid With Exactly K Paths I
Difficulty: Medium

Description:
This problem asks us to construct an m x n grid using only '.' (free cell) and '#' (obstacle cell) such that there are exactly k valid paths from (0, 0) to (m-1, n-1). Valid paths consist only of right or down moves through free cells. The constraints are small (m, n <= 10, k <= 4), suggesting that a simple, constructive approach based on patterns for small k values might exist.

Example:
Input: m = 2, n = 3, k = 2
Output: ["...", "#.."]
Explanation: There are exactly k = 2 valid paths from (0, 0) to (1, 2) in this grid:
(0, 0) -> (0, 1) -> (0, 2) -> (1, 2)
(0, 0) -> (0, 1) -> (1, 1) -> (1, 2)

Approach:
The solution employs a helper function `count_paths` to dynamically count the number of valid paths in any given grid configuration. This function fills a DP table `dp[r][c]` representing the number of paths from `(r, c)` to `(m-1, n-1)`. The main `createGrid` function then proceeds with a series of conditional constructions based on the values of `m`, `n`, and `k`.

1.  **Base Cases (m=1 or n=1):** If the grid is 1-dimensional, there's only one possible path (a straight line) if it's all free. Thus, if `k=1`, an all-free grid is returned. Otherwise, if `k>1`, no such grid exists, and an empty list is returned.

2.  **Initial All-Free Grid Check:** An all-free grid (all '.') represents the maximum possible number of paths. The `count_paths` function is used to determine this.
    *   If this count is exactly `k`, the all-free grid is the solution.
    *   If this count is less than `k`, it's impossible to achieve `k` paths (obstacles can only reduce paths), so an empty list is returned.

3.  **Constructing for Specific `k` (when all-free paths > `k`):** If the all-free grid has more than `k` paths, we strategically place obstacles to reduce the path count to exactly `k`.
    *   **`k=1`:** A single path is created along the top row to `(0, n-1)` and then down the rightmost column to `(m-1, n-1)`. All other cells `(r, c)` where `r >= 1` and `c <= n-2` are blocked with `'#'`. This isolates a single path. This construction is valid for `m, n >= 2`.
    *   **`k=2`:** This is built upon the `k=1` construction. After creating the `k=1` path, one additional cell `(1, n-2)` is opened (changed from `'#'` to `'.'`). This opens up a second distinct path. This requires `m>=2` and `n>=2`.
    *   **`k=3`:** This builds upon the `k=2` construction. One more cell `(2, n-2)` is opened (from `'#'` to `'.'`). This creates a third distinct path. This requires `m>=3` and `n>=2`.
    *   **`k=4`:** This strategy uses a different pattern inspired by Example 2 (`m=3, n=3, k=4`). The grid is initialized as all `'.'`, and then obstacles are placed at `(0, n-1)` and `(m-1, 0)`. These obstacles block specific sets of paths, yielding exactly 4 paths for appropriate `m,n` values (e.g., when `m,n >= 3` and the total paths are high enough to be reduced to 4).

This set of constructions covers all valid `k` values under the problem constraints, leveraging the "any grid" aspect to simplify the logic to specific patterns.

Time Complexity: O(m*n) for the `count_paths` function. Each grid construction involves iterating through the grid at most a constant number of times for a fixed `k`, leading to O(m*n) for grid construction as well. Therefore, the overall time complexity is O(m*n).
Space Complexity: O(m*n) for storing the grid and the DP table in the `count_paths` function.
"""
from typing import List, Optional

class Solution:
    def count_paths(self, grid: List[List[str]], m: int, n: int) -> int:
        # Check if start or end cells are blocked. If so, no paths.
        if grid[0][0] == '#' or grid[m-1][n-1] == '#':
            return 0

        dp = [[0 for _ in range(n)] for _ in range(m)]
        
        # Base case: The destination has 1 path to itself (if it's not an obstacle)
        dp[m-1][n-1] = 1

        # Fill DP table from bottom-right to top-left
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                # If current cell is an obstacle, no paths through it
                if grid[r][c] == '#':
                    dp[r][c] = 0
                    continue
                
                # If it's the destination cell, it's already set
                if r == m - 1 and c == n - 1:
                    continue 

                # Sum paths from down and right neighbors
                down_paths = dp[r+1][c] if r + 1 < m else 0
                right_paths = dp[r][c+1] if c + 1 < n else 0
                
                dp[r][c] = down_paths + right_paths
        
        return dp[0][0]

    def createGrid(self, m: int, n: int, k: int) -> List[str]:
        # Helper to convert internal grid representation (list of lists of chars) to list of strings
        def grid_to_str_list(grid_list: List[List[str]]) -> List[str]:
            return ["".join(row) for row in grid_list]

        # 1. Handle edge cases for m=1 or n=1 (1-dimensional grids)
        if m == 1 or n == 1:
            if k == 1:
                return grid_to_str_list([['.' for _ in range(n)] for _ in range(m)])
            else: # For 1-D grid, only 1 path is possible (if free). So k > 1 is impossible.
                return []

        # 2. Initial check: all-free grid (all '.')
        all_dots_grid = [['.' for _ in range(n)] for _ in range(m)]
        paths_all_dots = self.count_paths(all_dots_grid, m, n)
        
        if paths_all_dots == k:
            return grid_to_str_list(all_dots_grid)
        
        if paths_all_dots < k: # If max possible paths < k, it's impossible
            return []

        # 3. Construct specific grids for k=1, 2, 3, 4 (when paths_all_dots > k)
        # We know m, n are both >= 2 here due to earlier checks.

        res_grid_chars: List[List[str]]

        if k == 1:
            res_grid_chars = [['.' for _ in range(n)] for _ in range(m)]
            # Construct a single path along the top row and down the last column.
            # Block all cells (r, c) where r >= 1 and c <= n-2.
            # Example for m=3, n=3:
            # . . .
            # # # .
            # # # .
            for r in range(1, m):
                for c in range(n - 1):
                    res_grid_chars[r][c] = '#'
            return grid_to_str_list(res_grid_chars)

        elif k == 2:
            res_grid_chars = [['.' for _ in range(n)] for _ in range(m)]
            # Start with the k=1-like base grid
            for r in range(1, m):
                for c in range(n - 1):
                    res_grid_chars[r][c] = '#'
            # Open up a second path by freeing cell (1, n-2)
            # This cell is valid because m >= 2 and n >= 2
            # Example for m=3, n=3:
            # . . .
            # # . .  (cell (1,1) is opened)
            # # # .
            res_grid_chars[1][n-2] = '.'
            return grid_to_str_list(res_grid_chars)

        elif k == 3:
            res_grid_chars = [['.' for _ in range(n)] for _ in range(m)]
            # Start with the k=1-like base grid
            for r in range(1, m):
                for c in range(n - 1):
                    res_grid_chars[r][c] = '#'
            # Open (1, n-2) for the second path
            res_grid_chars[1][n-2] = '.'
            # Open (2, n-2) for the third path (requires m >= 3)
            # Example for m=3, n=3:
            # . . .
            # # . .
            # # . .  (cell (2,1) is opened)
            if m >= 3:
                res_grid_chars[2][n-2] = '.'
            return grid_to_str_list(res_grid_chars)

        elif k == 4:
            # Use a pattern inspired by Example 2 (m=3, n=3, k=4)
            # This pattern places obstacles at (0, n-1) and (m-1, 0) in an otherwise all-free grid.
            # Example for m=3, n=3:
            # . . #
            # . . .
            # # . .
            res_grid_chars = [['.' for _ in range(n)] for _ in range(m)]
            
            # Place obstacle at (0, n-1) if it's not the starting cell (0,0)
            if n - 1 > 0: 
                res_grid_chars[0][n-1] = '#'
            
            # Place obstacle at (m-1, 0) if it's not the starting cell (0,0)
            if m - 1 > 0:
                res_grid_chars[m-1][0] = '#'
            
            return grid_to_str_list(res_grid_chars)

        # Fallback: Should not be reached given the constraints and expected problem behavior
        # (i.e., one of the above patterns should always work for valid k,m,n)
        return []

if __name__ == "__main__":
    s = Solution()

    # Example 1
    m1, n1, k1 = 2, 3, 2
    output1 = s.createGrid(m1, n1, k1)
    # Expected: ["...", "#.."]
    assert output1 == ["...", "#.."], f"Example 1 failed: Input m={m1}, n={n1}, k={k1}, Expected ['...', '#..'], Got {output1}"
    assert s.count_paths([list(row) for row in output1], m1, n1) == k1

    # Example 2
    m2, n2, k2 = 3, 3, 4
    output2 = s.createGrid(m2, n2, k2)
    # Expected: ["..#", "...", "#.."]
    assert output2 == ["..#", "...", "#.."], f"Example 2 failed: Input m={m2}, n={n2}, k={k2}, Expected ['..#', '...', '#..'], Got {output2}"
    assert s.count_paths([list(row) for row in output2], m2, n2) == k2

    # Example 3
    m3, n3, k3 = 1, 4, 2
    output3 = s.createGrid(m3, n3, k3)
    # Expected: []
    assert output3 == [], f"Example 3 failed: Input m={m3}, n={n3}, k={k3}, Expected [], Got {output3}"

    # Test case: m=1, n=1, k=1
    m4, n4, k4 = 1, 1, 1
    output4 = s.createGrid(m4, n4, k4)
    assert output4 == ["."], f"Test Case 4 failed: Input m={m4}, n={n4}, k={k4}, Expected ['.'], Got {output4}"
    assert s.count_paths([list(row) for row in output4], m4, n4) == k4

    # Test case: m=2, n=2, k=1
    m5, n5, k5 = 2, 2, 1
    output5 = s.createGrid(m5, n5, k5)
    # Expected based on k=1 strategy: ["..", "##"] -> paths 1
    assert output5 == ["..", "##."], f"Test Case 5 failed: Input m={m5}, n={n5}, k={k5}, Expected ['..', '##.'], Got {output5}"
    assert s.count_paths([list(row) for row in output5], m5, n5) == k5
    
    # Test case: m=2, n=2, k=2 (all dots)
    m6, n6, k6 = 2, 2, 2
    output6 = s.createGrid(m6, n6, k6)
    # Expected: ["..", ".."]
    assert output6 == ["..", ".."], f"Test Case 6 failed: Input m={m6}, n={n6}, k={k6}, Expected ['..', '..'], Got {output6}"
    assert s.count_paths([list(row) for row in output6], m6, n6) == k6

    # Test case: m=3, n=3, k=1
    m7, n7, k7 = 3, 3, 1
    output7 = s.createGrid(m7, n7, k7)
    # Expected based on k=1 strategy: ["...", "##.", "##."]
    assert output7 == ["...", "##.", "##."], f"Test Case 7 failed: Input m={m7}, n={n7}, k={k7}, Expected ['...', '##.', '##.'], Got {output7}"
    assert s.count_paths([list(row) for row in output7], m7, n7) == k7
    
    # Test case: m=3, n=3, k=2
    m8, n8, k8 = 3, 3, 2
    output8 = s.createGrid(m8, n8, k8)
    # Expected based on k=2 strategy: ["...", "#..", "##."]
    assert output8 == ["...", "#..", "##."], f"Test Case 8 failed: Input m={m8}, n={n8}, k={k8}, Expected ['...', '#..', '##.'], Got {output8}"
    assert s.count_paths([list(row) for row in output8], m8, n8) == k8

    # Test case: m=3, n=3, k=3
    m9, n9, k9 = 3, 3, 3
    output9 = s.createGrid(m9, n9, k9)
    # Expected based on k=3 strategy: ["...", "#..", "#.."]
    assert output9 == ["...", "#..", "#.."], f"Test Case 9 failed: Input m={m9}, n={n9}, k={k9}, Expected ['...', '#..', '#..'], Got {output9}"
    assert s.count_paths([list(row) for row in output9], m9, n9) == k9

    # Test cases where max paths is less than k
    m10, n10, k10 = 2, 2, 3 
    output10 = s.createGrid(m10, n10, k10)
    assert output10 == [], f"Test Case 10 failed: Input m={m10}, n={n10}, k={k10}, Expected [], Got {output10}"

    m11, n11, k11 = 2, 3, 4
    output11 = s.createGrid(m11, n11, k11)
    assert output11 == [], f"Test Case 11 failed: Input m={m11}, n={n11}, k={k11}, Expected [], Got {output11}"

    print("All tests passed!")

