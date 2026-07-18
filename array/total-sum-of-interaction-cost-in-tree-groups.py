"""
Total Sum of Interaction Cost in Tree Groups
Difficulty: Hard

Description:
This problem asks us to calculate the sum of interaction costs for all unordered pairs of nodes (u, v)
such that u and v belong to the same group and u != v. The interaction cost between two nodes is defined as the
number of edges on the unique path connecting them in the tree.

Example:
Input: n = 3, edges = [[0,1],[1,2]], group = [1,1,1]
Output: 4
Explanation:
All nodes belong to group 1.
- Path (0,1) has 1 edge.
- Path (1,2) has 1 edge.
- Path (0,2) has 2 edges.
Total cost = 1 + 1 + 2 = 4.

Approach:
The problem can be efficiently solved using a single Depth First Search (DFS) traversal. The key insight is
to realize that the total interaction cost is the sum of contributions from each individual edge in the tree.
An edge (u, v) contributes 1 to the interaction cost between two nodes x and y if and only if removing
this edge disconnects x and y, placing them in different connected components.

We root the tree arbitrarily (e.g., at node 0). For any edge (u, v) where v is a child of u,
removing this edge splits the tree into two parts: the subtree rooted at v, and the rest of the tree (which includes u and its ancestors/other children).
The edge (u, v) contributes to the path length between a node 'a' and 'b' if 'a' is in the subtree of v
and 'b' is in the rest of the tree (or vice versa).

For each group 'g', we first compute `total_group_counts[g]`, which is the total number of nodes belonging to group 'g' in the entire tree.
During the DFS, for each node 'u' and its child 'v', the DFS function recursively computes `subtree_group_counts_v[g]`, which is the count of nodes
in group 'g' within the subtree rooted at 'v'. The number of nodes in group 'g' in the "rest of the tree"
(i.e., not in `subtree(v)`) is `total_group_counts[g] - subtree_group_counts_v[g]`.
The contribution of the edge (u, v) to the total sum for group 'g' is
`subtree_group_counts_v[g] * (total_group_counts[g] - subtree_group_counts_v[g])`.
We sum these contributions for all groups (1 to 20) and all edges in the tree. The DFS function also accumulates the group counts from its children
to return the total group counts for its own subtree to its parent. Python's default recursion limit needs to be increased for large N.

Time Complexity: O(N * MaxGroups) which simplifies to O(N) as MaxGroups (20) is a constant.
    - Building adjacency list: O(N)
    - Calculating total group counts: O(N)
    - DFS traversal: Each node is visited once. For each node, we iterate over its neighbors.
      When processing a child's returned subtree counts, we iterate over MaxGroups (20) group labels
      to calculate contributions for the edge and merge counts. Since there are O(N) nodes and O(N) edges,
      and each edge involves O(MaxGroups) operations, the total time for DFS is O(N * MaxGroups).
Space Complexity: O(N * MaxGroups) which simplifies to O(N) as MaxGroups (20) is a constant.
    - Adjacency list: O(N)
    - Total group counts array: O(MaxGroups)
    - DFS recursion stack: In the worst case (a path graph), the recursion depth is O(N).
      Each stack frame stores local variables, including an array of size MaxGroups for subtree counts.
      Therefore, stack space is O(N * MaxGroups).
"""
import sys
from typing import List, Optional

class Solution:
    def interactionCosts(self, n: int, edges: List[List[int]], group: List[int]) -> int:
        # Increase recursion limit for potentially deep trees, as N can be up to 10^5.
        sys.setrecursionlimit(n + 1000)

        # Build adjacency list for the tree
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # total_group_counts[g] will store the total number of nodes belonging to group g
        # Group labels are 1 to 20, so an array of size 21 is used (index 0 is unused).
        total_group_counts = [0] * 21
        for node_group in group:
            total_group_counts[node_group] += 1

        self.overall_total_cost = 0

        # dfs performs a Depth First Search.
        # It returns an array `subtree_counts_u` where `subtree_counts_u[g]` is the count
        # of nodes in group `g` within the subtree rooted at node `u`.
        def dfs(u: int, p: int) -> List[int]:
            # Initialize subtree_counts for the current node 'u'
            subtree_counts_u = [0] * 21
            subtree_counts_u[group[u]] = 1  # Node 'u' itself contributes to its group's count

            for v in adj[u]:
                if v == p:  # Skip parent node to avoid going back up the tree
                    continue
                
                # Recursively call DFS for child 'v'
                subtree_counts_v = dfs(v, u)

                # Calculate the contribution of the edge (u, v) to the total cost
                # An edge (u,v) contributes 1 to the path length between any node in subtree(v)
                # and any node in the rest of the tree.
                # We only care about pairs (x,y) where group[x] == group[y].
                for g in range(1, 21): # Iterate through all possible group labels (1 to 20)
                    count_in_v_subtree = subtree_counts_v[g]
                    
                    # If there are nodes of group 'g' in 'v's subtree, calculate contribution
                    if count_in_v_subtree > 0:
                        # Number of nodes of group 'g' NOT in 'v's subtree (i.e., in the rest of the tree)
                        count_in_rest_of_tree = total_group_counts[g] - count_in_v_subtree
                        
                        # Each pair (node_in_v_subtree, node_in_rest_of_tree) of the same group 'g'
                        # will have the edge (u,v) on its path.
                        self.overall_total_cost += count_in_v_subtree * count_in_rest_of_tree
                
                # Merge subtree_counts_v into subtree_counts_u.
                # This accumulates the counts from all children's subtrees into 'u's subtree count.
                for g in range(1, 21):
                    subtree_counts_u[g] += subtree_counts_v[g]
            
            return subtree_counts_u

        # Start the DFS traversal from node 0 (arbitrarily chosen root) with a parent of -1 (no parent).
        dfs(0, -1)
        
        return self.overall_total_cost

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 3
    edges1 = [[0,1],[1,2]]
    group1 = [1,1,1]
    expected1 = 4
    assert s.interactionCosts(n1, edges1, group1) == expected1, f"Test 1 failed: Expected {expected1}, got {s.interactionCosts(n1, edges1, group1)}"
    
    # Example 2
    n2 = 3
    edges2 = [[0,1],[1,2]]
    group2 = [3,2,3]
    expected2 = 2
    assert s.interactionCosts(n2, edges2, group2) == expected2, f"Test 2 failed: Expected {expected2}, got {s.interactionCosts(n2, edges2, group2)}"

    # Example 3
    n3 = 4
    edges3 = [[0,1],[0,2],[0,3]]
    group3 = [1,1,4,4]
    expected3 = 3
    assert s.interactionCosts(n3, edges3, group3) == expected3, f"Test 3 failed: Expected {expected3}, got {s.interactionCosts(n3, edges3, group3)}"

    # Example 4
    n4 = 2
    edges4 = [[0,1]]
    group4 = [9,8]
    expected4 = 0
    assert s.interactionCosts(n4, edges4, group4) == expected4, f"Test 4 failed: Expected {expected4}, got {s.interactionCosts(n4, edges4, group4)}"

    # Custom test case: Disconnected groups within the same component, star graph
    n5 = 5
    edges5 = [[0,1],[0,2],[0,3],[0,4]]
    group5 = [1,2,1,2,1] # Group 1: nodes 0, 2, 4. Group 2: nodes 1, 3.
    # Group 1 pairs: (0,2), (0,4), (2,4)
    #   (0,2): dist 1 (edge 0-2)
    #   (0,4): dist 1 (edge 0-4)
    #   (2,4): dist 2 (path 2-0-4)
    # Group 2 pairs: (1,3)
    #   (1,3): dist 2 (path 1-0-3)
    # Total: 1+1+2 + 2 = 6
    expected5 = 6
    assert s.interactionCosts(n5, edges5, group5) == expected5, f"Test 5 failed: Expected {expected5}, got {s.interactionCosts(n5, edges5, group5)}"

    # Custom test case: Path graph, mixed groups
    n6 = 5
    edges6 = [[0,1],[1,2],[2,3],[3,4]]
    group6 = [1,2,1,2,1]
    # Group 1: (0,2), (0,4), (2,4)
    #   (0,2): dist 2 (0-1-2)
    #   (0,4): dist 4 (0-1-2-3-4)
    #   (2,4): dist 2 (2-3-4)
    # Group 2: (1,3)
    #   (1,3): dist 2 (1-2-3)
    # Total: 2+4+2 + 2 = 10
    expected6 = 10
    assert s.interactionCosts(n6, edges6, group6) == expected6, f"Test 6 failed: Expected {expected6}, got {s.interactionCosts(n6, edges6, group6)}"

    print("All tests passed!")

```