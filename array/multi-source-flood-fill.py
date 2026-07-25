import collections
from typing import List, Optional

class Solution:
    def colorGrid(self, n: int, m: int, sources: List[List[int]]) -> List[List[int]]:
        """
        Multi Source Flood Fill
        Difficulty: Medium

        Description:
        This problem involves simulating a multi-source flood fill process on a grid.
        Initially, some cells are colored by sources, and others are uncolored (0).
        At each time step, all currently colored cells simultaneously spread their color
        to adjacent uncolored cells. If an uncolored cell is reached by multiple colors
        at the same time step, it takes the maximum color value. The process stops when
        no more cells can be colored, and the final state of the grid is returned.

        Example:
        Input: n = 3, m = 3, sources = [[0,0,1],[2,2,2]]
        Output: [[1,1,2],[1,2,2],[2,2,2]]

        Approach:
        This problem can be solved using a Breadth-First Search (BFS) approach adapted for
        multi-source, level-by-level propagation with tie-breaking rules. We initialize a grid
        with initial colors and a `time_grid` to store the minimum time step at which each cell
        is colored. A deque `q` stores cells that are currently colored and will spread their
        colors in the next time step. In each BFS layer (representing one time step), we iterate
        through all cells in the current `q`. For each cell, we examine its four neighbors.
        If a neighbor is currently uncolored (indicated by `time_grid` being infinity), it becomes
        a candidate for coloring at the *next* time step. We collect all such candidates along
        with the maximum color that reaches them at this next time step in a `cells_for_next_layer`
        dictionary. After processing all cells for the current time step, we update the actual `grid`
        and `time_grid` for these newly colored cells and add them to the `q` for the subsequent time step.
        This ensures simultaneous spread and correct tie-breaking, processing layer by layer until no new
        cells are colored.

        Time Complexity: O(N * M)
        Each cell (r, c) is added to the queue at most once when it is first colored.
        When a cell is dequeued, we visit its four neighbors. This results in O(N * M) operations for grid traversal.
        The `cells_for_next_layer` dictionary stores potential updates for the current time step, and its processing also takes O(N * M) in the worst case (if all cells are candidates).
        Thus, the overall time complexity is proportional to the number of cells in the grid.

        Space Complexity: O(N * M)
        We use `grid` and `time_grid` which are both O(N * M).
        The queue `q` can hold up to O(N * M) elements in the worst case (e.g., if all cells in a row/column are colored in one step).
        The `cells_for_next_layer` dictionary can also store up to O(N * M) entries.
        Therefore, the space complexity is O(N * M).
        """
        grid = [[0] * m for _ in range(n)]
        # time_grid stores the time step at which a cell was first colored.
        # Initialize with float('inf') for uncolored cells.
        time_grid = [[float('inf')] * m for _ in range(n)]

        q = collections.deque()

        # Initialize the grid and queue with source cells
        for r_src, c_src, color_src in sources:
            grid[r_src][c_src] = color_src
            time_grid[r_src][c_src] = 0 # Source cells are colored at time 0
            q.append((r_src, c_src))

        # Directions for neighbors: (row_delta, col_delta)
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        current_time = 0
        
        while q:
            current_time += 1
            # A dictionary to collect potential updates for cells at the current_time step.
            # Key: (nr, nc) tuple, Value: maximum color that reached this cell at current_time.
            # Initialized with 0, which is safe since valid colors are >= 1.
            cells_for_next_layer = collections.defaultdict(int)
            
            # Process all cells that were colored in the previous time step (current_time - 1)
            # These cells will now spread their colors to `current_time`
            size = len(q)
            for _ in range(size):
                r, c = q.popleft()
                spreading_color = grid[r][c] # The color this cell is spreading

                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc

                    # Check boundary conditions
                    if 0 <= nr < n and 0 <= nc < m:
                        # If the neighbor cell is uncolored (time_grid is still inf)
                        # it is a candidate to be colored at `current_time`.
                        if time_grid[nr][nc] == float('inf'):
                            # Update with the maximum color if multiple paths reach it simultaneously
                            cells_for_next_layer[(nr, nc)] = max(cells_for_next_layer[(nr, nc)], spreading_color)

            # After processing all cells from the current layer (q),
            # apply the collected updates to the grid and prepare for the next layer.
            newly_colored_cells_count = 0
            for (nr, nc), max_spread_color in cells_for_next_layer.items():
                # If this cell (nr, nc) is indeed uncolored, color it and add to queue
                if time_grid[nr][nc] == float('inf'): 
                    grid[nr][nc] = max_spread_color
                    time_grid[nr][nc] = current_time
                    q.append((nr, nc)) # Add to queue for spreading in the next time step
                    newly_colored_cells_count += 1
            
            # If no new cells were colored in this time step, the process stops.
            if newly_colored_cells_count == 0:
                break
                
        return grid

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1, m1 = 3, 3
    sources1 = [[0,0,1],[2,2,2]]
    expected1 = [[1,1,2],[1,2,2],[2,2,2]]
    assert s.colorGrid(n1, m1, sources1) == expected1, f"Test Case 1 Failed: {s.colorGrid(n1, m1, sources1)}"
    # print(f"Test Case 1 Passed: {s.colorGrid(n1, m1, sources1)}")

    # Example 2
    n2, m2 = 3, 3
    sources2 = [[0,1,3],[1,1,5]]
    expected2 = [[3,3,3],[5,5,5],[5,5,5]]
    assert s.colorGrid(n2, m2, sources2) == expected2, f"Test Case 2 Failed: {s.colorGrid(n2, m2, sources2)}"
    # print(f"Test Case 2 Passed: {s.colorGrid(n2, m2, sources2)}")

    # Example 3
    n3, m3 = 2, 2
    sources3 = [[1,1,5]]
    expected3 = [[5,5],[5,5]]
    assert s.colorGrid(n3, m3, sources3) == expected3, f"Test Case 3 Failed: {s.colorGrid(n3, m3, sources3)}"
    # print(f"Test Case 3 Passed: {s.colorGrid(n3, m3, sources3)}")
    
    # Custom Test Case 4: Single source, large grid
    n4, m4 = 1, 5
    sources4 = [[0,0,10]]
    expected4 = [[10,10,10,10,10]]
    assert s.colorGrid(n4, m4, sources4) == expected4, f"Test Case 4 Failed: {s.colorGrid(n4, m4, sources4)}"
    # print(f"Test Case 4 Passed: {s.colorGrid(n4, m4, sources4)}")

    # Custom Test Case 5: Multiple sources, some overlapping reach
    n5, m5 = 4, 4
    sources5 = [[0,0,1],[0,3,10],[3,0,5],[3,3,20]]
    expected5 = [
        [1,1,10,10],
        [1,10,10,10],
        [5,10,20,20],
        [5,5,20,20]
    ]
    assert s.colorGrid(n5, m5, sources5) == expected5, f"Test Case 5 Failed: {s.colorGrid(n5, m5, sources5)}"
    # print(f"Test Case 5 Passed: {s.colorGrid(n5, m5, sources5)}")

    # Custom Test Case 6: Grid with n=1, m=1
    n6, m6 = 1, 1
    sources6 = [[0,0,100]]
    expected6 = [[100]]
    assert s.colorGrid(n6, m6, sources6) == expected6, f"Test Case 6 Failed: {s.colorGrid(n6, m6, sources6)}"
    # print(f"Test Case 6 Passed: {s.colorGrid(n6, m6, sources6)}")

    print("All tests passed!")

