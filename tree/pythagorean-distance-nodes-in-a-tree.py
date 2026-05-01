"""
Pythagorean Distance Nodes in a Tree
Difficulty: Medium

Description:
This problem asks us to find the number of "special" nodes in a given tree. A node `u` is special if its distances to three distinct target nodes `x`, `y`, and `z` form a Pythagorean triplet (a, b, c) such that a^2 + b^2 = c^2 after sorting the distances. We are given the number of nodes `n`, the tree edges, and the target nodes `x, y, z`.

Example:
Input: n = 4, edges = [[0,1],[0,2],[0,3]], x = 1, y = 2, z = 3
Output: 3
Explanation: Nodes 1, 2, and 3 are special. For node 1, distances are (0, 2, 2), which sorted becomes (0, 2, 2). Since 0^2 + 2^2 = 2^2 (0 + 4 = 4), it's special.

Approach:
The core idea is to efficiently calculate the distance from each of the three target nodes (x, y, z) to every other node in the tree. Since we need all-pairs distances from specific sources in an unweighted tree, Breadth-First Search (BFS) is the ideal algorithm. We first construct an adjacency list representation of the tree from the given edges. Then, we perform three separate BFS traversals: one starting from `x`, one from `y`, and one from `z`. Each BFS generates a distance array, storing `dist_x[i]`, `dist_y[i]`, and `dist_z[i]` for every node `i`. After computing all three sets of distances, we iterate through all `n` nodes (from 0 to n-1). For each node `u`, we retrieve its `dx`, `dy`, and `dz` values, collect them into a list, sort them to ensure `a <= b <= c`, and then check if they satisfy the Pythagorean condition `a^2 + b^2 = c^2`. We maintain a counter for special nodes and return its final value.

Time Complexity: O(N)
Building the adjacency list takes O(N) time (as there are N-1 edges). Each of the three BFS traversals takes O(N + E) time, which simplifies to O(N) for a tree where E = N-1. The final iteration through all N nodes, including sorting three integers and a constant-time check, takes O(N) time. Thus, the total time complexity is O(N).

Space Complexity: O(N)
The adjacency list requires O(N) space. We store three distance arrays, each of size N, contributing O(N) space. The BFS queue also requires O(N) space in the worst case (e.g., a star graph). Therefore, the total space complexity is O(N).
"""
import collections
from typing import List

class Solution:
    def specialNodes(self, n: int, edges: List[List[int]], x: int, y: int, z: int) -> int:
        
        # 1. Build Adjacency List
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # Helper function for BFS to find distances from a start_node to all other nodes
        def bfs(start_node: int) -> List[int]:
            distances = [-1] * n  # Initialize distances to -1 (unvisited)
            q = collections.deque([(start_node, 0)])
            distances[start_node] = 0

            while q:
                curr_node, dist = q.popleft()

                for neighbor in adj[curr_node]:
                    if distances[neighbor] == -1:  # If neighbor hasn't been visited
                        distances[neighbor] = dist + 1
                        q.append((neighbor, dist + 1))
            return distances

        # 2. Calculate All Distances from x, y, z
        dist_x = bfs(x)
        dist_y = bfs(y)
        dist_z = bfs(z)

        # 3. Iterate and Check for Special Nodes
        special_nodes_count = 0
        for i in range(n):
            dx = dist_x[i]
            dy = dist_y[i]
            dz = dist_z[i]

            # Collect and sort distances to ensure a <= b <= c
            distances = sorted([dx, dy, dz])
            a, b, c = distances[0], distances[1], distances[2]

            # Check Pythagorean condition: a^2 + b^2 = c^2
            if a*a + b*b == c*c:
                special_nodes_count += 1
        
        return special_nodes_count

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 4
    edges1 = [[0,1],[0,2],[0,3]]
    x1, y1, z1 = 1, 2, 3
    assert s.specialNodes(n1, edges1, x1, y1, z1) == 3, f"Test Case 1 Failed: Expected 3, Got {s.specialNodes(n1, edges1, x1, y1, z1)}"

    # Example 2
    n2 = 4
    edges2 = [[0,1],[1,2],[2,3]]
    x2, y2, z2 = 0, 3, 2
    assert s.specialNodes(n2, edges2, x2, y2, z2) == 0, f"Test Case 2 Failed: Expected 0, Got {s.specialNodes(n2, edges2, x2, y2, z2)}"

    # Example 3
    n3 = 4
    edges3 = [[0,1],[1,2],[1,3]]
    x3, y3, z3 = 1, 3, 0
    assert s.specialNodes(n3, edges3, x3, y3, z3) == 1, f"Test Case 3 Failed: Expected 1, Got {s.specialNodes(n3, edges3, x3, y3, z3)}"

    # Custom Test Case 1: Line graph
    # 0 -- 1 -- 2 -- 3 -- 4
    # x=0, y=4, z=2
    # Node 2: dx=2, dy=2, dz=0. Sorted: [0,2,2]. 0^2 + 2^2 = 2^2. Special.
    n4 = 5
    edges4 = [[0,1],[1,2],[2,3],[3,4]]
    x4, y4, z4 = 0, 4, 2
    assert s.specialNodes(n4, edges4, x4, y4, z4) == 1, f"Test Case 4 Failed: Expected 1, Got {s.specialNodes(n4, edges4, x4, y4, z4)}"

    # Custom Test Case 2: Tree with no special nodes
    # 0 -- 1 -- 2
    # |    |
    # 3 -- 4
    # x=2, y=3, z=4
    # No nodes form a Pythagorean triplet
    n5 = 5
    edges5 = [[0,1],[1,2],[0,3],[1,4]]
    x5, y5, z5 = 2, 3, 4
    assert s.specialNodes(n5, edges5, x5, y5, z5) == 0, f"Test Case 5 Failed: Expected 0, Got {s.specialNodes(n5, edges5, x5, y5, z5)}"

    # Custom Test Case 3: A longer path graph
    # 0 - 1 - 2 - 3 - 4 - 5 - 6 - 7
    # x = 0, y = 7, z = 4
    # Node 4: dx=4, dy=3, dz=0. Sorted: [0,3,4]. 0^2 + 3^2 != 4^2. No. Wait, I made a mistake in manual calculation.
    # Distances from x=0: [0,1,2,3,4,5,6,7]
    # Distances from y=7: [7,6,5,4,3,2,1,0]
    # Distances from z=4: [4,3,2,1,0,1,2,3]
    # Node 4: dx=4, dy=3, dz=0. Sorted: [0,3,4]. 0^2+3^2 = 9 != 4^2. Not special.
    # Let's re-evaluate all nodes for this case:
    # u=0: [0,4,7]. No.
    # u=1: [1,3,6]. No.
    # u=2: [2,2,5]. No.
    # u=3: [3,1,4]. No.
    # u=4: [4,0,3]. Sorted: [0,3,4]. 0^2+3^2=9 != 4^2. No.
    # u=5: [5,1,2]. No.
    # u=6: [6,2,3]. No.
    # u=7: [7,0,3]. No.
    # It seems there are no special nodes in this specific longer path graph.
    n6 = 8
    edges6 = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
    x6, y6, z6 = 0, 7, 4
    assert s.specialNodes(n6, edges6, x6, y6, z6) == 0, f"Test Case 6 Failed: Expected 0, Got {s.specialNodes(n6, edges6, x6, y6, z6)}"


    print("All tests passed!")

