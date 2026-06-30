"""
Palindromic Path Queries in a Tree
Difficulty: Hard

Description:
This problem involves an undirected tree where each node has an assigned character. We need to handle two types of queries: updating a node's character and determining if the characters on the unique path between two nodes can be rearranged into a palindrome. A string can be rearranged into a palindrome if at most one character appears an odd number of times.

Example:
Input: n = 3, edges = [[0,1],[1,2]], s = "aac", queries = ["query 0 2","update 1 b","query 0 2"]
Output: [true,false]

Approach:
The problem requires efficient path queries and point updates on a tree, which strongly suggests using Heavy-Light Decomposition (HLD) combined with a segment tree. For character frequency counting, we use bitmasks: each character 'a' through 'z' is mapped to a unique bit position (0 to 25). The XOR sum of these bitmasks along a path indicates which characters appear an odd number of times. A path's characters can form a palindrome if its total XOR sum mask has at most one bit set (i.e., `mask == 0` or `(mask & (mask - 1)) == 0`).

1.  **Preprocessing (O(N log N))**:
    *   **Adjacency List**: Build the tree's adjacency list.
    *   **DFS1 (Tree Properties)**: Perform a DFS to compute `parent`, `depth`, and `subtree_size` for all nodes. This also identifies the heavy child for each node (the child whose subtree has the largest size).
    *   **DFS2 (HLD Decomposition)**: Perform another DFS to decompose the tree into heavy paths. Nodes on a heavy path are assigned contiguous indices (`pos` array) in a linearized array. The `head` array stores the head of the heavy path each node belongs to. During this DFS, we populate `char_masks_linearized` with the initial bitmasks for each node's character, mapping `s[u]` to `char_masks_linearized[pos[u]]`. We also maintain a `node_char_masks` array to store the current character mask for each node, which will be updated directly.
    *   **LCA (Binary Lifting)**: Precompute `up[k][u]`, the `2^k`-th ancestor of node `u`, using binary lifting. This allows `O(log N)` LCA queries.
    *   **Segment Tree**: Build a segment tree over `char_masks_linearized`. Each node in the segment tree stores the XOR sum of character masks in its range.

2.  **Query Processing**:
    *   **`update ui c` (O(log N))**:
        1.  Compute the new bitmask for character `c`.
        2.  Update `node_char_masks[ui]` with the new mask.
        3.  Update the segment tree at `pos[ui]` with the new mask using `_update_segment_tree`.
    *   **`query ui vi` (O(log^2 N))**:
        1.  Find the `LCA(ui, vi)` using binary lifting (`_get_lca`).
        2.  Compute the XOR sum of character masks on the path from `ui` to `LCA(ui, vi)` (`_query_path_xor_hld(ui, lca)`).
        3.  Compute the XOR sum of character masks on the path from `vi` to `LCA(ui, vi)` (`_query_path_xor_hld(vi, lca)`).
        4.  The total path XOR sum `ui -> vi` is `xor_path(ui, lca) ^ xor_path(vi, lca) ^ node_char_masks[lca]`. The `node_char_masks[lca]` is XORed back because it's included twice (once in `xor_path(ui,lca)` and once in `xor_path(vi,lca)`), cancelling its effect. We need it to be included once.
        5.  Check if the resulting `total_path_xor` mask has `0` or `1` bit set using the `(mask & (mask - 1)) == 0` trick.

Time Complexity: O(N log N + Q log^2 N), where N is the number of nodes and Q is the number of queries.
Space Complexity: O(N log N) due to the binary lifting `up` table.
"""
import collections
import math
from typing import List, Optional

class Solution:
    def palindromePath(self, n: int, edges: List[List[int]], s: str, queries: List[str]) -> List[bool]:
        
        self.n = n
        self.adj = collections.defaultdict(list)
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        # HLD specific arrays
        self.parent = [-1] * n
        self.depth = [-1] * n
        self.size = [0] * n
        self.head = [-1] * n # head of the heavy path
        self.pos = [-1] * n  # position in the segment tree array (linearized tree)
        self.time = 0 # current time for DFS2 (for pos array)
        
        # Character masks for each node, updated by 'update' queries
        self.node_char_masks = [0] * n
        for i in range(n):
            self.node_char_masks[i] = 1 << (ord(s[i]) - ord('a'))
        
        # Array to build segment tree over (stores initial linearized char masks)
        self.char_masks_linearized = [0] * n 
        
        # Binary Lifting for LCA
        # LOGN needs to be large enough such that 2^(LOGN-1) >= N
        # N.bit_length() is equivalent to floor(log2(N)) + 1
        self.LOGN = n.bit_length() # max depth for binary lifting
        self.up = [[-1] * n for _ in range(self.LOGN)]

        # --- Phase 1: DFS1 to compute parent, depth, subtree size ---
        # root at 0, parent of root is -1, depth 0
        self._dfs1(0, -1, 0)

        # --- Phase 2: DFS2 to decompose into heavy-light paths and fill pos array ---
        # Root 0, parent -1, head of path 0
        self._dfs2(0, -1, 0) 

        # --- Phase 3: Binary Lifting for LCA precomputation ---
        # up[0][i] is parent[i]
        for i in range(n):
            self.up[0][i] = self.parent[i]
        # up[k][i] is 2^k-th ancestor of i
        for k in range(1, self.LOGN):
            for i in range(n):
                if self.up[k-1][i] != -1:
                    self.up[k][i] = self.up[k-1][self.up[k-1][i]]

        # --- Phase 4: Segment Tree Setup ---
        # Segment tree stores XOR sum of char masks
        # Its size is 4*N for worst case
        self.seg_tree_arr = [0] * (4 * n)
        self._build_segment_tree(1, 0, n - 1)

        # --- Process Queries ---
        results = []
        for query in queries:
            parts = query.split()
            if parts[0] == "update":
                u = int(parts[1])
                char_code = ord(parts[2]) - ord('a')
                new_mask = 1 << char_code
                self.node_char_masks[u] = new_mask
                self._update_segment_tree(1, 0, n - 1, self.pos[u], new_mask)
            else: # "query"
                u = int(parts[1])
                v = int(parts[2])
                
                lca_node = self._get_lca(u, v)
                
                xor_u_to_lca = self._query_path_xor_hld(u, lca_node)
                xor_v_to_lca = self._query_path_xor_hld(v, lca_node)
                
                # The character at LCA is included in both xor_u_to_lca and xor_v_to_lca.
                # So its contribution cancels out (XOR'd twice).
                # We need to XOR it back in once.
                total_path_xor = xor_u_to_lca ^ xor_v_to_lca ^ self.node_char_masks[lca_node]
                
                # Check if total_path_xor mask has at most one bit set
                is_palindrome_possible = (total_path_xor == 0) or ((total_path_xor & (total_path_xor - 1)) == 0)
                results.append(is_palindrome_possible)
        
        return results

    # --- HLD and LCA Helper Functions ---

    def _dfs1(self, u: int, p: int, d: int) -> None:
        """
        DFS1 computes parent, depth, and subtree size for each node.
        It also helps identify the heavy child.
        """
        self.parent[u] = p
        self.depth[u] = d
        self.size[u] = 1
        for v in self.adj[u]:
            if v == p:
                continue
            self._dfs1(v, u, d + 1)
            self.size[u] += self.size[v]

    def _dfs2(self, u: int, p: int, h: int) -> None:
        """
        DFS2 decomposes the tree into heavy-light paths.
        It populates head, pos, and char_masks_linearized arrays.
        """
        self.head[u] = h
        self.pos[u] = self.time
        self.char_masks_linearized[self.time] = self.node_char_masks[u]
        self.time += 1

        heavy_child = -1
        max_subtree_size = 0
        for v in self.adj[u]:
            if v == p:
                continue
            if self.size[v] > max_subtree_size:
                max_subtree_size = self.size[v]
                heavy_child = v
        
        if heavy_child != -1:
            self._dfs2(heavy_child, u, h) # Continue heavy path for heavy child

        for v in self.adj[u]:
            if v == p or v == heavy_child:
                continue
            self._dfs2(v, u, v) # Start new heavy path for light children

    def _get_lca(self, u: int, v: int) -> int:
        """
        Computes the Lowest Common Ancestor (LCA) of nodes u and v using binary lifting.
        """
        # Ensure u is deeper or at the same depth as v
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Lift u to the same depth as v
        for k in range(self.LOGN - 1, -1, -1):
            if self.up[k][u] != -1 and self.depth[self.up[k][u]] >= self.depth[v]:
                u = self.up[k][u]
        
        # If u is now v, then v was an ancestor of original u
        if u == v:
            return u
        
        # Lift u and v simultaneously until their parents are the same
        for k in range(self.LOGN - 1, -1, -1):
            if self.up[k][u] != -1 and self.up[k][v] != -1 and self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        
        return self.parent[u] # Parent of u (or v) is the LCA

    # --- Segment Tree Helper Functions ---

    def _build_segment_tree(self, idx: int, start: int, end: int) -> None:
        """
        Builds the segment tree. Each node stores the XOR sum of character masks in its range.
        """
        if start == end:
            self.seg_tree_arr[idx] = self.char_masks_linearized[start]
        else:
            mid = (start + end) // 2
            self._build_segment_tree(2 * idx, start, mid)
            self._build_segment_tree(2 * idx + 1, mid + 1, end)
            self.seg_tree_arr[idx] = self.seg_tree_arr[2 * idx] ^ self.seg_tree_arr[2 * idx + 1]

    def _update_segment_tree(self, idx: int, start: int, end: int, target_pos: int, new_val: int) -> None:
        """
        Updates the value at `target_pos` in the segment tree with `new_val`.
        """
        if start == end:
            self.seg_tree_arr[idx] = new_val
        else:
            mid = (start + end) // 2
            if start <= target_pos <= mid:
                self._update_segment_tree(2 * idx, start, mid, target_pos, new_val)
            else:
                self._update_segment_tree(2 * idx + 1, mid + 1, end, target_pos, new_val)
            self.seg_tree_arr[idx] = self.seg_tree_arr[2 * idx] ^ self.seg_tree_arr[2 * idx + 1]

    def _query_segment_tree(self, idx: int, start: int, end: int, l: int, r: int) -> int:
        """
        Queries the XOR sum of character masks in the range [l, r] in the segment tree.
        """
        # No overlap
        if r < start or end < l:
            return 0 # XOR identity element
        # Full overlap
        if l <= start and end <= r:
            return self.seg_tree_arr[idx]
        # Partial overlap
        mid = (start + end) // 2
        p1 = self._query_segment_tree(2 * idx, start, mid, l, r)
        p2 = self._query_segment_tree(2 * idx + 1, mid + 1, end, l, r)
        return p1 ^ p2
    
    # --- Path XOR Query using HLD ---
    def _query_path_xor_hld(self, u: int, ancestor: int) -> int:
        """
        Computes the XOR sum of char masks on the path from node `u` up to its ancestor `ancestor` (inclusive).
        `u` must be `ancestor` or a descendant of `ancestor`.
        """
        res_xor = 0
        while True:
            # If u and ancestor are on the same heavy path
            if self.head[u] == self.head[ancestor]:
                # Query the segment tree for the range from ancestor's pos to u's pos
                # Since ancestor is always 'above' u on the heavy path in linearization, pos[ancestor] <= pos[u].
                res_xor ^= self._query_segment_tree(1, 0, self.n - 1, self.pos[ancestor], self.pos[u])
                break # Path segment to ancestor covered
            else:
                # Query the segment tree for the entire heavy path from head[u] up to u
                res_xor ^= self._query_segment_tree(1, 0, self.n - 1, self.pos[self.head[u]], self.pos[u])
                # Move to the parent of the head of the current heavy path
                u = self.parent[self.head[u]]
        return res_xor


if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    n1 = 3
    edges1 = [[0,1],[1,2]]
    s1 = "aac"
    queries1 = ["query 0 2","update 1 b","query 0 2"]
    expected1 = [True, False]
    assert s_obj.palindromePath(n1, edges1, s1, queries1) == expected1, f"Example 1 Failed: {s_obj.palindromePath(n1, edges1, s1, queries1)}"

    # Example 2
    n2 = 4
    edges2 = [[0,1],[0,2],[0,3]]
    s2 = "abca"
    queries2 = ["query 1 2","update 0 b","query 2 3","update 3 a","query 1 3"]
    expected2 = [False,False,True]
    assert s_obj.palindromePath(n2, edges2, s2, queries2) == expected2, f"Example 2 Failed: {s_obj.palindromePath(n2, edges2, s2, queries2)}"
    
    # Custom Test 1: Single node tree
    n3 = 1
    edges3 = []
    s3 = "z"
    queries3 = ["query 0 0", "update 0 a", "query 0 0"]
    expected3 = [True, True] # "z" is palindrome (1 odd char), "a" is palindrome (1 odd char)
    assert s_obj.palindromePath(n3, edges3, s3, queries3) == expected3, f"Custom Test 1 Failed: {s_obj.palindromePath(n3, edges3, s3, queries3)}"

    # Custom Test 2: Path with all same characters
    n4 = 5
    edges4 = [[0,1],[1,2],[2,3],[3,4]]
    s4 = "aaaaa"
    queries4 = ["query 0 4", "update 2 b", "query 0 4"]
    # Path 0-1-2-3-4
    # Initially: s = "aaaaa", query 0 4 -> "aaaaa". 'a': 5. One odd count. -> True.
    # Update 2 to 'b': s = "aabaa".
    # Query 0 4: Path "aabaa". 'a': 4, 'b': 1. One odd count. -> True.
    expected4 = [True, True]
    assert s_obj.palindromePath(n4, edges4, s4, queries4) == expected4, f"Custom Test 2 Failed: {s_obj.palindromePath(n4, edges4, s4, queries4)}"

    # Custom Test 3: Larger case, more complex path
    n5 = 7
    edges5 = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
    s5 = "abcdefg" # node 0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g'
    queries5 = ["query 3 6", "update 0 a", "query 3 5"]
    
    # query 3 6: Path 3-1-0-2-6. Chars: 'd','b','a','c','g'. All appear once (5 unique). -> False.
    # update 0 a: s[0] remains 'a'. This update effectively changes nothing for char_mask(0).
    # query 3 5: Path 3-1-0-2-5. Chars: 'd','b','a','c','f'. All appear once (5 unique). -> False.
    expected5 = [False, False]
    assert s_obj.palindromePath(n5, edges5, s5, queries5) == expected5, f"Custom Test 4 Failed: {s_obj.palindromePath(n5, edges5, s5, queries5)}"


    print("All tests passed!")

