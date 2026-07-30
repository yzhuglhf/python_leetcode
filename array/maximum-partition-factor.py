"""
Maximum Partition Factor
Difficulty: Hard

Description:
The problem asks to split a set of `n` points (given as `[xi, yi]` coordinates) into exactly two non-empty groups. The "partition factor" for a given split is defined as the minimum Manhattan distance among all pairs of points that belong to the same group. The objective is to find the maximum possible partition factor over all valid splits. A special rule is given for `n=2`: if there are only two points, they must form two groups of size one, contributing no intra-group pairs, and the partition factor is defined as 0.

Example:
Input: points = [[0,0],[0,2],[2,0],[2,2]]
Output: 4
Explanation: We split the points into two groups: `{[0, 0], [2, 2]}` and `{[0, 2], [2, 0]}`. In the first group, the Manhattan distance between [0,0] and [2,2] is |0-2|+|0-2|=4. In the second group, the distance between [0,2] and [2,0] is |0-2|+|2-0|=4. The minimum of these intra-group distances is `min(4, 4) = 4`, which is the maximum possible.

Approach:
This problem can be effectively solved using binary search on the answer. We are looking for the maximum value `X` such that it's possible to partition the `n` points into two non-empty groups `G1` and `G2`, where every pair of points within `G1` has a Manhattan distance of at least `X`, and similarly for `G2`.

The core idea is to define a `check(X)` function that determines if a partition factor of `X` is achievable. If `dist(p_i, p_j)` is the Manhattan distance between points `p_i` and `p_j`, then for `X` to be achievable, any pair `(p_i, p_j)` such that `dist(p_i, p_j) < X` *must* belong to different groups. This is a classic 2-coloring (bipartite graph checking) problem.

The `check(X)` function proceeds as follows:
1.  Construct a graph where each point is a node. An edge is added between `p_i` and `p_j` if their Manhattan distance `dist(p_i, p_j)` is less than `X`.
2.  Attempt to 2-color this graph (assign each node to one of two "colors" or groups) using Breadth-First Search (BFS) or Depth-First Search (DFS).
    *   Initialize all nodes as uncolored.
    *   Iterate through each node. If a node is uncolored, start a traversal (BFS/DFS) from it, assigning it 'color 1'. All its neighbors must then be assigned 'color 2', their neighbors 'color 1', and so on.
    *   If at any point during the traversal, we find a neighbor `v` of `u` that has already been colored with the same color as `u`, then the graph is not 2-colorable. In this case, `check(X)` returns `False`.
3.  If the traversal completes for all connected components without conflicts, the graph is 2-colorable, and `check(X)` returns `True`.
    *   If `n > 2` and the graph is 2-colorable, it's always possible to form two non-empty groups. If the graph has edges, the 2-coloring naturally yields two non-empty sets. If the graph has no edges (meaning all distances are `>= X`), we can simply put one point in `G1` and the rest in `G2` (since `n >= 3`), satisfying the non-empty group constraint.
    *   The special case `n=2` is handled separately at the beginning of `maxPartitionFactor` by returning 0, as specified in the problem statement.

The binary search works over the range of possible partition factors:
*   The minimum possible factor is 0.
*   The maximum possible Manhattan distance can be up to `2 * (10^8 - (-10^8))` in both x and y dimensions, summing to `4 * 10^8`. So, the upper bound for the binary search is `4 * 10^8 + 1`.
The `ans` variable tracks the maximum `X` for which `check(X)` returned `True`.

Time Complexity: O(N^2 * log(MAX_DIST))
-   The `check(X)` function: It iterates through all `N * (N-1) / 2` pairs of points to calculate distances and build the adjacency list, taking O(N^2) time. The BFS/DFS for 2-coloring also takes O(N + E) time, where E can be up to O(N^2), so it's O(N^2). Thus, `check(X)` is O(N^2).
-   The binary search performs `log(MAX_DIST)` iterations.
-   With `N=500`, `N^2 = 250,000`. `log(4 * 10^8)` is approximately 29. The total operations would be roughly `250,000 * 29`, which is around `7.25 * 10^6`, well within typical time limits for `N=500`.

Space Complexity: O(N^2)
-   The adjacency list `adj` can store up to O(N^2) edges in the worst case (a dense graph).
-   The `colors` array and BFS queue take O(N) space.

"""
import collections
from typing import List

class Solution:
    def maxPartitionFactor(self, points: List[List[int]]) -> int:
        n = len(points)

        # Handle the special case where n = 2 as per the problem description.
        # If n=2, both groups are size 1, there are no intra-group pairs.
        # The partition factor is explicitly defined as 0.
        if n == 2:
            return 0

        # `check(X)` function: determines if a partition factor of `X` is achievable.
        # This is true if the graph `G_X` (where an edge (i,j) exists if dist(p_i, p_j) < X)
        # is 2-colorable (bipartite).
        def check(X: int) -> bool:
            # Adjacency list for the graph G_X
            adj = collections.defaultdict(list)
            
            # Populate the adjacency list based on Manhattan distances < X
            for i in range(n):
                for j in range(i + 1, n):
                    # Calculate Manhattan distance
                    dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    if dist < X:
                        adj[i].append(j)
                        adj[j].append(i)
            
            # `colors` array: 0 for uncolored, 1 for color 1 (group 1), 2 for color 2 (group 2)
            colors = [0] * n 
            
            # Iterate through all nodes to handle disconnected components
            for i in range(n):
                if colors[i] == 0:  # If node `i` is uncolored, start a BFS from it
                    q = collections.deque([(i, 1)]) # Store (node, assigned_color)
                    colors[i] = 1 # Assign starting node `i` to color 1
                    
                    while q:
                        u, u_color = q.popleft()
                        
                        # Explore neighbors of `u`
                        for v in adj[u]:
                            if colors[v] == 0: # If neighbor `v` is uncolored
                                v_color = 3 - u_color # Assign the opposite color to `v`
                                colors[v] = v_color
                                q.append((v, v_color))
                            elif colors[v] == u_color: # Conflict: neighbor `v` has the same color as `u`
                                # This means the graph is not 2-colorable (contains an odd cycle)
                                return False # `X` is not achievable
            
            # If the loop completes without conflicts, the graph is 2-colorable.
            # For n > 2, a 2-colorable graph (with or without edges) allows forming two non-empty groups.
            # If there are edges, the 2-coloring naturally yields two non-empty sets.
            # If there are no edges, we can arbitrarily pick one point for G1 and the rest for G2.
            return True

        # Binary search for the maximum `X`
        # `low`: Smallest possible partition factor (0)
        # `high`: Largest possible Manhattan distance + 1 (exclusive upper bound)
        # Max coordinate value is 10^8, min is -10^8. Max difference is 2*10^8.
        # Max Manhattan distance is 2*10^8 + 2*10^8 = 4*10^8.
        low = 0
        high = 4 * 10**8 + 1 
        ans = 0 # Stores the maximum achievable partition factor found so far

        while low < high:
            mid = low + (high - low) // 2
            if check(mid):
                # If `mid` is achievable, then `mid` could be our answer,
                # and we try to find an even larger factor.
                ans = mid
                low = mid + 1
            else:
                # If `mid` is not achievable, we need to try a smaller factor.
                high = mid
        
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    points1 = [[0,0],[0,2],[2,0],[2,2]]
    assert s.maxPartitionFactor(points1) == 4, f"Test Case 1 Failed: {s.maxPartitionFactor(points1)}"
    
    # Example 2
    points2 = [[0,0],[0,1],[10,0]]
    assert s.maxPartitionFactor(points2) == 11, f"Test Case 2 Failed: {s.maxPartitionFactor(points2)}"
    
    # Custom test case: n=2
    points3 = [[1,1],[10,10]]
    assert s.maxPartitionFactor(points3) == 0, f"Test Case 3 Failed: {s.maxPartitionFactor(points3)}"

    # Custom test case: identical points
    points4 = [[0,0],[0,0],[1,1]]
    assert s.maxPartitionFactor(points4) == 2, f"Test Case 4 Failed: {s.maxPartitionFactor(points4)}"

    # Custom test case: complex graph, expect 1
    points5 = [[0,0],[1,0],[2,0],[3,0]]
    # Distances: d(0,1)=1, d(0,2)=2, d(0,3)=3, d(1,2)=1, d(1,3)=2, d(2,3)=1
    # Check(1): Edges for dist < 1 (none). True. ans=0, low=1
    # Check(2): Edges for dist < 2: (0,1), (1,2), (2,3).
    # 0-1-2-3. Bipartite. True. ans=1, low=2
    # Check(3): Edges for dist < 3: (0,1), (1,2), (2,3), (0,2), (1,3).
    # 0-1, 1-2, 2-3, 0-2, 1-3. All edges except (0,3).
    # Try coloring: 0:1, 1:2, 2:1. (0-1, 1-2, 0-2 checked).
    # Then 3 must be 2 (from 2-3), but 3 must be 1 (from 1-3). Conflict. Not bipartite. False. high=2.
    # So ans = 2.
    assert s.maxPartitionFactor(points5) == 2, f"Test Case 5 Failed: {s.maxPartitionFactor(points5)}"
    
    print("All tests passed!")