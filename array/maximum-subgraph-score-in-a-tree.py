"""
Maximum Subgraph Score in a Tree (LeetCode #4151)
Difficulty: Hard

Description:
This problem asks us to find, for each node in a given undirected tree, the maximum possible "score" of a connected subgraph that includes that specific node. The score of a subgraph is defined as the number of good nodes minus the number of bad nodes it contains. Nodes are marked good (1) or bad (0) in the input `good` array.

Example:
Input: n = 5, edges = [[1,0],[1,2],[1,3],[3,4]], good = [0,1,0,1,1]
Output: [2,3,2,3,3]
For instance, for node 0, the best connected subgraph is {0, 1, 3, 4} (3 good, 1 bad), score = 2. For node 1, the best subgraph is {1, 3, 4} (3 good, 0 bad), score = 3.

Approach:
This problem can be efficiently solved using a tree dynamic programming technique often referred to as "rerooting DP" or "two DFS passes".
First, we convert the `good` array into a `scores` array where `scores[i]` is 1 if `good[i]` is 1, and -1 if `good[i]` is 0. This way, the subgraph score is simply the sum of `scores` for all nodes in the subgraph.

1.  **First DFS (Bottom-Up - `dfs1`)**:
    We perform a DFS starting from an arbitrary root (e.g., node 0). For each node `u`, `dfs1` calculates `dp_down[u]`, which represents the maximum score of a connected subgraph containing `u` and *only* nodes within `u`'s subtree (relative to the current root). The value `dp_down[u]` is `scores[u]` plus the sum of `max(0, dp_down[v])` for all children `v` of `u`. We only add positive contributions from children because including a negative-scoring branch would reduce the score. During this pass, we initialize `ans[u] = dp_down[u]`.

2.  **Second DFS (Top-Down - `dfs2`)**:
    We perform another DFS, also starting from the same root. This pass propagates information from the parent to its children. For each node `u`, `dfs2` takes an argument `parent_max_score_from_above`. This argument represents the maximum score that `u` can gain by connecting to its parent `p` and extending upwards through `p` or sideways into `p`'s other children (excluding `u`'s own subtree).
    The total maximum score for `u` is then `dp_down[u]` (from `dfs1`) plus `max(0, parent_max_score_from_above)`.
    To calculate `parent_max_score_from_above` for a child `v` of `u`:
    It's `scores[u]` + `max(0, parent_max_score_from_above)` (passed to `u`) + `sum(max(0, dp_down[s])` for all siblings `s` of `v` (i.e., other children of `u`). To efficiently calculate this sum, we use prefix and suffix sums of `max(0, dp_down[s])` for all children `s` of `u`.

The final `ans` array will contain the maximum subgraph score for each node.

Time Complexity: O(N)
Building the adjacency list takes O(N) time. Each DFS pass visits every node and edge once. The prefix/suffix sum calculations for children of a node take time proportional to the node's degree. Summing degrees over all nodes is O(N). Therefore, the total time complexity is O(N).
Space Complexity: O(N)
The adjacency list, `scores`, `dp_down`, `ans` arrays, and the recursion stack (in the worst case of a skewed tree) all contribute O(N) space. Temporary arrays for prefix/suffix sums also take O(degree_max) space, which is O(N) in the worst case (star graph).
"""
import collections
from typing import List, Optional

class Solution:
    def maxSubgraphScore(self, n: int, edges: List[List[int]], good: List[int]) -> List[int]:
        # 1. Preprocessing: Build adjacency list and scores array
        adj = collections.defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # Convert good/bad to scores: 1 for good, -1 for bad
        scores = [1 if g == 1 else -1 for g in good]

        # dp_down[i]: Max score of a connected subgraph containing node i
        # and only nodes in the subtree rooted at i (when considering a temporary root).
        dp_down = [0] * n
        
        # ans[i]: Final answer for node i, representing the maximum score
        # for a connected subgraph containing i in the entire tree.
        ans = [0] * n

        # DFS 1 (Bottom-Up): Calculates dp_down values and initializes ans.
        # u: current node, p: parent of u in the current DFS path.
        def dfs1(u: int, p: int):
            current_score = scores[u]
            for v in adj[u]:
                if v == p:
                    continue
                dfs1(v, u)
                # Only add positive contributions from children's subgraphs.
                # If dp_down[v] is negative, including that branch would decrease the score.
                current_score += max(0, dp_down[v])
            
            dp_down[u] = current_score
            # Initialize ans[u] with the score from its subtree.
            ans[u] = dp_down[u]

        # DFS 2 (Top-Down): Propagates upward contributions and finalizes ans.
        # u: current node, p: parent of u.
        # parent_max_score_from_above: Max score from the part of the tree
        # connected through p to u, excluding u's own subtree.
        def dfs2(u: int, p: int, parent_max_score_from_above: int):
            # The total max score for node u is its dp_down value plus
            # any positive contribution from the parent direction.
            ans[u] += max(0, parent_max_score_from_above)
            
            # Collect children of u (excluding its parent p)
            children = [v for v in adj[u] if v != p]
            
            # If u has no children (other than its parent), no further recursion needed.
            if not children:
                return

            # Prepare for efficient calculation of sibling contributions using prefix/suffix sums.
            # children_contributions[i] stores max(0, dp_down[children[i]]).
            children_contributions = [max(0, dp_down[v]) for v in children]
            
            num_children = len(children_contributions)
            prefix_sums = [0] * (num_children + 1)
            suffix_sums = [0] * (num_children + 1)

            # Calculate prefix sums
            for i in range(num_children):
                prefix_sums[i+1] = prefix_sums[i] + children_contributions[i]
            
            # Calculate suffix sums
            for i in range(num_children - 1, -1, -1):
                suffix_sums[i] = suffix_sums[i+1] + children_contributions[i]
            
            # Iterate through each child to make recursive calls
            for i, v in enumerate(children):
                # Calculate the score that child 'v' can gain from 'u'
                # (i.e., 'v' connecting to 'u' and going up, or to u's other children).
                
                # Start with u's own score
                val_from_u_up = scores[u]
                # Add positive contribution from u's parent side
                val_from_u_up += max(0, parent_max_score_from_above)
                # Add positive contributions from children of u *before* v
                val_from_u_up += prefix_sums[i] 
                # Add positive contributions from children of u *after* v
                val_from_u_up += suffix_sums[i+1] 
                
                # Recursively call dfs2 for child v, passing its parent-side contribution.
                dfs2(v, u, val_from_u_up)

        # Start DFS1 from an arbitrary root (e.g., node 0). Parent is -1 (non-existent).
        dfs1(0, -1)
        
        # Start DFS2 from the same root. Initial parent_max_score_from_above is 0
        # as there's no parent to connect to from the root.
        dfs2(0, -1, 0)

        return ans

