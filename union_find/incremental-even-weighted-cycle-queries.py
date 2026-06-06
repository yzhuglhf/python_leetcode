"""
Incremental Even-Weighted Cycle Queries
Difficulty: Hard

Description:
This problem asks us to count the number of edges successfully added to a graph. An edge [u, v, w] can only be added if, after its addition, all cycles in the graph have an even sum of edge weights. Edge weights are either 0 or 1.

Example:
Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,1]]
Output: 2
Explanation: Edges [0,1,1] and [1,2,1] are added. Adding [0,2,1] would create cycle 0-1-2-0 with total weight 1+1+1=3 (odd), so it's not added.

Approach:
The condition that "all cycles have an even sum of edge weights" implies that for any two nodes u and v, all paths between them must have the same parity (sum of weights modulo 2). This property allows us to assign a "potential" or "parity" value `p[i]` to each node `i` such that for any existing edge (u, v) with weight `w`, `(p[u] + p[v] + w)` is even, or equivalently, `p[u] ^ p[v] = w` (where `^` is XOR, treating values as 0 or 1).

We can use a Disjoint Set Union (DSU) data structure to manage connected components and these parity values. For each node `i`, we store `parent[i]` (its parent in the DSU tree) and `diff[i]` (the parity of the path weight from `i` to `parent[i]`).
The `find` operation performs path compression and accumulates `diff` values along the path to the root, effectively computing `(path_weight(i, root_i)) % 2`.
When processing an edge `(u, v)` with weight `w`:
1. Find the roots of `u` and `v`, say `root_u` and `root_v`, along with `diff_u` (parity of path `u` to `root_u`) and `diff_v` (parity of path `v` to `root_v`).
2. If `root_u` is the same as `root_v`: `u` and `v` are already connected. Adding `(u, v)` creates a cycle. The parity of the existing path from `u` to `v` (via `root_u`) is `(diff_u + diff_v) % 2`. For the new edge to be valid, the cycle formed must have an even sum, meaning `(w + (diff_u + diff_v) % 2)` must be even. This implies `w == (diff_u + diff_v) % 2`. If this condition holds, the edge is accepted; otherwise, it's rejected.
3. If `root_u` is different from `root_v`: `u` and `v` are in different components. Adding `(u, v)` merges them and doesn't create any cycle. The edge is always accepted. We merge `root_v` into `root_u` by setting `parent[root_v] = root_u`. The `diff[root_v]` is set to `(diff_u + w + diff_v) % 2`, representing the parity of the path `root_v` to `root_u` through the newly added edge.

The `numberOfEdgesAdded` method iterates through the edges, calling the DSU's `union` method. If `union` returns `True`, the edge is counted.

Time Complexity: O(E * α(N)), where E is the number of edges, N is the number of nodes, and α is the inverse Ackermann function, which is practically a very small constant. This simplifies to effectively O(N + E).
Space Complexity: O(N) for the parent and diff arrays in the DSU.
"""
from typing import List, Optional

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.diff = [0] * n  # diff[i] stores (path_weight(i, parent[i])) % 2

    def find(self, i: int) -> tuple[int, int]:
        """
        Finds the root of component `i` and the parity of the path from `i` to its root.
        Performs path compression.
        Returns: (root_node, parity_from_i_to_root)
        """
        if self.parent[i] == i:
            return i, 0
        
        # Path compression
        root, diff_to_root_parent = self.find(self.parent[i])
        self.parent[i] = root
        # Update diff[i]: 
        # path_parity(i, root) = path_parity(i, original_parent[i]) + path_parity(original_parent[i], root)
        self.diff[i] = (self.diff[i] + diff_to_root_parent) % 2
        return self.parent[i], self.diff[i]

    def union(self, u: int, v: int, w: int) -> bool:
        """
        Attempts to add an edge (u, v) with weight w.
        Returns True if the edge can be added (doesn't create an odd cycle), False otherwise.
        """
        root_u, diff_u = self.find(u)  # diff_u = (path_weight(u, root_u)) % 2
        root_v, diff_v = self.find(v)  # diff_v = (path_weight(v, root_v)) % 2

        if root_u == root_v:
            # u and v are already in the same connected component.
            # Adding edge (u,v) with weight w would create a cycle.
            # The parity of the path from u to v via their common root_u is (diff_u + diff_v) % 2.
            # For the cycle (u --w--> v --path--> u) to have an even total weight,
            # (w + (diff_u + diff_v) % 2) must be 0 (mod 2).
            # This is equivalent to w == (diff_u + diff_v) % 2.
            return (w + diff_u + diff_v) % 2 == 0
        else:
            # u and v are in different components. Merging them does not create any cycle.
            # The edge is always added.
            # Arbitrarily make root_v a child of root_u.
            self.parent[root_v] = root_u
            # We need to set diff[root_v], which represents path_parity(root_v, parent[root_v] = root_u).
            # Consider the path: root_u -> ... -> u --w--> v -> ... -> root_v.
            # The parity of this path is (path_parity(root_u, u) + w + path_parity(v, root_v)) % 2.
            # Since path_parity(x, y) == path_parity(y, x),
            # path_parity(root_u, u) is diff_u.
            # path_parity(v, root_v) is diff_v.
            # So, path_parity(root_v, root_u) = (diff_u + w + diff_v) % 2.
            self.diff[root_v] = (diff_u + w + diff_v) % 2
            return True

class Solution:
    def numberOfEdgesAdded(self, n: int, edges: List[List[int]]) -> int:
        dsu = DSU(n)
        added_edges_count = 0

        for u, v, w in edges:
            if dsu.union(u, v, w):
                added_edges_count += 1
        
        return added_edges_count

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.numberOfEdgesAdded(3, [[0,1,1],[1,2,1],[0,2,1]]) == 2

    # Example 2
    assert s.numberOfEdgesAdded(3, [[0,1,1],[1,2,1],[0,2,0]]) == 3
    
    # Custom test case: Disconnected components merging
    # Initial graph: {0}, {1}, {2}, {3}
    # Edge [0,1,1]: 0 and 1 merge. 0-1(1). dsu.parent=[0,0,2,3], dsu.diff=[0,1,0,0]. count=1
    # Edge [2,3,0]: 2 and 3 merge. 2-3(0). dsu.parent=[0,0,2,2], dsu.diff=[0,1,0,0]. count=2
    # Edge [1,2,1]: 1 (root 0, diff from 1 to 0 is 1) and 2 (root 2, diff from 2 to 2 is 0) merge.
    #   Merge root 2 to root 0. dsu.parent[2]=0.
    #   dsu.diff[2] = (diff_u (1->0) + w (1->2) + diff_v (2->2)) % 2 = (1 + 1 + 0) % 2 = 0.
    #   Graph: 0-1(1)-2(1)-3(0). All connected. count=3
    # Edge [0,3,1]: 0 (root 0, diff 0->0 is 0) and 3 (root 0, diff 3->0 is 0) are connected.
    #   Path from 0 to 3 via root 0 has parity (diff(0->0) + diff(3->0))%2 = (0+0)%2 = 0.
    #   Proposed edge 0-3 with weight 1. Cycle sum (1 + 0)%2 = 1. Odd. Rejected.
    # Final count = 3
    assert s.numberOfEdgesAdded(4, [[0,1,1],[2,3,0],[1,2,1],[0,3,1]]) == 3

    # All 0-weight edges, all accepted (forms a spanning tree, any cycle would be 0-sum).
    assert s.numberOfEdgesAdded(4, [[0,1,0],[1,2,0],[2,3,0],[0,3,0]]) == 4

    # All 1-weight edges in a line. Try to add another 1-weight edge.
    # 0--1(1) --2(1) --3(1)
    # Edge [0,1,1]: parent=[0,0,2,3], diff=[0,1,0,0]. count=1
    # Edge [1,2,1]: parent=[0,0,0,3], diff=[0,1,1,0]. count=2
    #   (diff from 2 to 0: diff(2->1)+diff(1->0) = 1+1 = 0)
    # Edge [2,3,1]: parent=[0,0,0,0], diff=[0,1,1,1]. count=3
    #   (diff from 3 to 0: diff(3->2)+diff(2->0) = 1+0 = 1)
    # Current DSU: root 0, diff(1->0)=1, diff(2->0)=0, diff(3->0)=1
    # Try edge [0,3,1]: 0 (root 0, diff 0) and 3 (root 0, diff 1).
    #   Check (w + diff(0->0) + diff(3->0))%2 = (1 + 0 + 1)%2 = 0. Even. Accepted.
    # Total count = 4
    assert s.numberOfEdgesAdded(4, [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]) == 4

    # Same as above, but with a 0-weight edge.
    # Current DSU state: root 0, diff(1->0)=1, diff(2->0)=0, diff(3->0)=1
    # Try edge [0,3,0]: 0 (root 0, diff 0) and 3 (root 0, diff 1).
    #   Check (w + diff(0->0) + diff(3->0))%2 = (0 + 0 + 1)%2 = 1. Odd. Rejected.
    # Total count = 3
    assert s.numberOfEdgesAdded(4, [[0,1,1],[1,2,1],[2,3,1],[0,3,0]]) == 3

    print("All tests passed!")
