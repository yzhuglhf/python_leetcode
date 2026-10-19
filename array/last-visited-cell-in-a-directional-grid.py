"""
Last Visited Cell in a Directional Grid
Difficulty: Medium

Description:
This problem simulates movement within a grid where each cell contains a character ('L', 'R', 'U', 'D') indicating the next direction. Starting at (0, 0), the process continues by moving to the indicated cell, marking it visited. The simulation terminates if the next intended move would either lead outside the grid boundaries or to an already visited cell. The goal is to return the coordinates of the last successfully visited cell.

Example:
Input: grid = [["R","D"],["U","L"]]
Output: [1,0]
Explanation: The path is (0,0) -> (0,1) -> (1,1) -> (1,0). From (1,0), moving 'U' would lead to (0,0), which is already visited, so the process stops.

Approach:
The problem can be solved by directly simulating the movement. We maintain the current position (r, c) and a set to store all visited cell coordinates. Starting at (0,0), we add it to the visited set. In a loop, we determine the next potential cell based on the character in the current cell. Before making the move, we check two conditions: if the next cell is out of bounds or if it has already been visited. If either condition is true, the process ends, and the current (r, c) is the last successfully visited cell. Otherwise, we update (r, c) to the new cell and add it to the visited set, then continue the loop.

Time Complexity: O(m * n)
In the worst case, the simulation visits every cell in the grid exactly once before termination. Each step involves constant time operations (set lookup, set insertion, arithmetic).
Space Complexity: O(m * n)
A set is used to store all visited cell coordinates. In the worst case, all m * n cells might be visited and stored in the set.
"""
from typing import List, Optional

class Solution:
    def lastVisitedCell(self, grid: List[List[str]]) -> List[int]:
        m = len(grid)
        n = len(grid[0])

        # Direction mappings for row and column changes
        dr_dc = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }

        r, c = 0, 0
        visited = set()
        visited.add((r, c)) # Start at (0,0) and it's considered visited

        while True:
            # Determine the character at the current cell
            direction_char = grid[r][c]
            
            # Get the change in row and column based on the direction
            dr, dc = dr_dc[direction_char]

            # Calculate the next potential cell coordinates
            next_r, next_c = r + dr, c + dc

            # Check termination conditions:
            # 1. Out of bounds
            is_out_of_bounds = not (0 <= next_r < m and 0 <= next_c < n)
            
            # 2. Already visited
            is_already_visited = (next_r, next_c) in visited

            if is_out_of_bounds or is_already_visited:
                # If either condition is true, the process ends.
                # The last successfully visited cell was (r, c).
                return [r, c]
            else:
                # If the move is valid and the cell hasn't been visited,
                # move to the new cell and mark it as visited.
                r, c = next_r, next_c
                visited.add((r, c))

if __name__ == "__main__":
    s = Solution()

    # Example 1
    grid1 = [["R","D"],["U","L"]]
    assert s.lastVisitedCell(grid1) == [1,0], f"Test 1 Failed: {s.lastVisitedCell(grid1)}"

    # Example 2
    grid2 = [["R","R","R"]]
    assert s.lastVisitedCell(grid2) == [0,2], f"Test 2 Failed: {s.lastVisitedCell(grid2)}"

    # Test case: Grid with only one cell, move leads out of bounds
    grid3 = [["U"]]
    assert s.lastVisitedCell(grid3) == [0,0], f"Test 3 Failed: {s.lastVisitedCell(grid3)}"

    # Test case: Linear path to the end (right)
    grid4 = [["R","R","R","R","R"]]
    assert s.lastVisitedCell(grid4) == [0,4], f"Test 4 Failed: {s.lastVisitedCell(grid4)}"

    # Test case: Linear path to the end (down)
    grid5 = [["D"],["D"],["D"]]
    assert s.lastVisitedCell(grid5) == [2,0], f"Test 5 Failed: {s.lastVisitedCell(grid5)}"

    # Test case: Cycle immediately by attempting an out-of-bounds move from (0,0)
    grid6 = [["L"]] 
    assert s.lastVisitedCell(grid6) == [0,0], f"Test 6 Failed: {s.lastVisitedCell(grid6)}"

    # Test case: Complex path with a loop that terminates due to out-of-bounds
    grid7 = [
        ["R", "D", "L"],
        ["U", "R", "D"],
        ["L", "U", "R"]
    ]
    # Path: (0,0)->(0,1)->(1,1)->(1,2)->(2,2). From (2,2) 'R' goes to (2,3) which is out of bounds.
    assert s.lastVisitedCell(grid7) == [2,2], f"Test 7 Failed: {s.lastVisitedCell(grid7)}"
    
    # Test case: A spiral-like path that eventually hits a visited cell
    grid8 = [
        ["R", "D", "D"],
        ["U", "R", "L"],
        ["U", "U", "L"]
    ]
    # Path: (0,0)->(0,1)->(1,1)->(1,2). From (1,2) 'L' goes to (1,1), which is already visited.
    assert s.lastVisitedCell(grid8) == [1,2], f"Test 8 Failed: {s.lastVisitedCell(grid8)}"

    # Test case: Larger grid, simple path
    grid9 = [["R"]*10]
    assert s.lastVisitedCell(grid9) == [0,9], f"Test 9 Failed: {s.lastVisitedCell(grid9)}"

    print("All tests passed!")