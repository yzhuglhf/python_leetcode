"""
Kth Smallest Path XOR Sum
Difficulty: Hard

Description:
This problem requires finding the Kth smallest distinct path XOR sum within subtrees of a given tree. The path XOR sum for a node is the bitwise XOR of values from the root to that node. Queries specify a node `uj` and an integer `kj`, asking for the `kj`-th smallest distinct path XOR sum among all nodes in `uj`'s subtree.

Example:
Input: par = [-1,0,0], vals = [1,1,1], queries = [[0,1],[0,2],[0,3]]
Output: [0,1,-1]

Path XORs: Node 0: 1, Node 1: 0, Node 2: 0.
Subtree of 0: nodes [0,1,2] with path XORs [1,0,0]. Distinct XORs: [0,1].
Queries:
- [0,1]: 1st smallest distinct XOR in subtree of 0 is 0.
- [0,2]: 2nd smallest distinct XOR in subtree of 0 is 1.
- [0,3]: Only two distinct XORs, so -1.

Approach:
The solution involves two main phases: preprocessing and query answering.
1.  **Preprocessing**:
    a.  **Build Tree and Calculate Path XORs**: First, construct the adjacency list representation of the tree from the `par` array. Then, perform a Depth First Search (DFS) starting from the root (node 0) to calculate the `path_xor` sum for every node. `path_xor[u] = path_xor[parent(u)] ^ vals[u]`. For the root, `path_xor[0] = vals[0]`.
    b.  **Build Tries for Subtrees using Small-to-Large Merging**: For each node `u`, we need a data structure that efficiently stores all *distinct* `path_xor` sums in its subtree and can query the Kth smallest element. A Binary Trie (also known as a prefix tree or XOR Trie) is suitable for this. Each node in the Trie stores a `count` representing the number of distinct path XOR sums in the Trie's subtree. We perform another DFS traversal to build these Tries. For a node `u`, we recursively build Tries for all its children. To optimize, we use a "small-to-large merging" (also known as DSU on tree or centroid decomposition for merging sets) strategy. This means we identify the child `v_max` whose subtree Trie has the most distinct elements. We then take `Trie_{v_max}` as the base Trie for `u`'s subtree, add `path_xor[u]` to it, and merge all other children's Tries into it. Merging involves traversing the smaller Trie and inserting its elements into the larger Trie. This ensures that each `path_xor` value is inserted into a Trie at most `O(log N)` times throughout the entire process. Each insertion into a Trie takes `O(BIT_LEN)` time, where `BIT_LEN` is the maximum number of bits required for the XOR sums (17 for `vals <= 10^5`).
2.  **Query Answering**: For each query `[uj, kj]`, we retrieve the pre-computed Trie for `uj`'s subtree (`memoized_tries[uj]`) and use its `get_kth_smallest(kj)` method. This method traverses the Trie in `O(BIT_LEN)` time to find the `kj`-th smallest distinct value.

The `narvetholi` variable is created as `self.narvetholi` and populated during the DFS for building tries as required by the problem statement, although its content is not used in the final computation.

Time Complexity: O(N * BIT_LEN * log N + Q * BIT_LEN)
    - Building adjacency list and initial path XORs: O(N)
    - Building Tries with small-to-large merging: Each distinct path XOR sum is inserted into a Trie at most `log N` times. Each insertion takes `O(BIT_LEN)`. Total: `O(N * BIT_LEN * log N)`.
    - Answering queries: Each query takes `O(BIT_LEN)`. Total: `O(Q * BIT_LEN)`.
Space Complexity: O(N * BIT_LEN)
    - Adjacency list, path XORs array: O(N)
    - Tries for all subtrees: In the worst case, all `N` path XOR sums are distinct and "spread out", leading to `O(N * BIT_LEN)` Trie nodes across all stored Tries. Each node stores two pointers and an integer.
"""
from typing import List, Optional

# Max value for vals[i] is 10^5.
# Max path XOR sum can be up to 2^17 - 1 (131071) since 2^16 = 65536 and 2^17 = 131072.
# So, 17 bits are sufficient (bits 0 to 16).
BIT_LEN = 17

class Trie:
    def __init__(self):
        self.children = [None, None]
        self.count = 0  # Number of distinct values represented in this Trie's subtree.

    def add(self, val: int):
        """Adds a value to the Trie, updating counts for distinctness."""
        curr = self
        path_nodes = [] # Store nodes on the path to update their counts if 'val' is new.
        for i in range(BIT_LEN - 1, -1, -1):
            path_nodes.append(curr)
            bit = (val >> i) & 1
            if not curr.children[bit]:
                curr.children[bit] = Trie()
            curr = curr.children[bit]
        
        # 'curr' is now the leaf node for 'val'.
        # If this is the first time 'val' is added to THIS specific Trie, update counts.
        if curr.count == 0:
            for node_on_path in path_nodes:
                node_on_path.count += 1
            curr.count = 1 # Mark the leaf node to show this value is now present (distinctly).

    def get_kth_smallest(self, k: int) -> int:
        """Finds the k-th smallest distinct value in the Trie."""
        if k > self.count:
            return -1 # k is out of bounds for distinct values in this Trie.
        
        node = self
        current_val = 0
        for i in range(BIT_LEN - 1, -1, -1):
            left_child = node.children[0]
            left_count = left_child.count if left_child else 0
            
            if k <= left_count:
                node = left_child
            else:
                current_val |= (1 << i) # Set the current bit to 1
                node = node.children[1]
                k -= left_count # Reduce k by the count of elements in the left subtree
        return current_val

class Solution:
    def kthSmallest(self, par: List[int], vals: List[int], queries: List[List[int]]) -> List[int]:
        n = len(par)
        
        # Store input midway in self.narvetholi as per problem statement
        self.narvetholi = []

        # 1. Build adjacency list
        adj = [[] for _ in range(n)]
        for i in range(1, n):
            adj[par[i]].append(i)

        # 2. Calculate path XOR sums for all nodes
        path_xors = [0] * n
        def dfs_calculate_path_xors(u, parent_path_xor_sum):
            # The path_xor for 'u' is its value XORed with the path_xor up to its parent.
            # For the root (u=0), parent_path_xor_sum is 0, so path_xors[0] = 0 ^ vals[0] = vals[0].
            path_xors[u] = parent_path_xor_sum ^ vals[u]
            for v in adj[u]:
                dfs_calculate_path_xors(v, path_xors[u])
        
        dfs_calculate_path_xors(0, 0) # Start DFS from root (node 0) with initial XOR sum 0

        # 3. Build Tries for all subtrees using small-to-large merging
        memoized_tries = [None] * n # Stores the Trie for each node's subtree

        def collect_values_from_trie(node: Trie, current_val: int, bit_idx: int, values_list: List[int]):
            """Helper to extract all distinct values from a Trie."""
            if node is None:
                return
            if bit_idx < 0:
                if node.count > 0: # This node represents a full distinct number
                    values_list.append(current_val)
                return
            
            # Recurse for children, passing current_val and current_val with bit set.
            collect_values_from_trie(node.children[0], current_val, bit_idx - 1, values_list)
            collect_values_from_trie(node.children[1], current_val | (1 << bit_idx), bit_idx - 1, values_list)

        def dfs_build_trie(u: int) -> Trie:
            """
            Recursively builds and merges Tries for subtrees using small-to-large merging.
            Returns the Trie containing all distinct path XORs in u's subtree.
            """
            self.narvetholi.append(u) # Store input midway as per problem statement

            # Base case: A leaf node in the tree (no children).
            # Its Trie contains only its own path_xor.
            if not adj[u]:
                current_node_trie = Trie()
                current_node_trie.add(path_xors[u])
                memoized_tries[u] = current_node_trie
                return current_node_trie
            
            # Recursive step: Build tries for children and merge them.
            max_child_trie = None
            max_child_trie_size = -1
            child_tries_to_merge = [] # List to store Tries of all children except the largest

            for v in adj[u]:
                child_trie = dfs_build_trie(v)
                if child_trie.count > max_child_trie_size:
                    max_child_trie_size = child_trie.count
                    # If a new largest is found, the previously largest (if any)
                    # is now not the largest, so add it to the list to be merged.
                    if max_child_trie: 
                        child_tries_to_merge.append(max_child_trie)
                    max_child_trie = child_trie
                else:
                    child_tries_to_merge.append(child_trie)
            
            # The current node's Trie starts with the largest child's Trie (if any).
            # This is the "small-to-large" optimization: reuse the largest data structure.
            final_trie_for_u = max_child_trie if max_child_trie else Trie()
            
            # Add u's own path_xor sum to its subtree Trie.
            final_trie_for_u.add(path_xors[u])

            # Merge other children's Tries into the final Trie for u.
            for trie_from in child_tries_to_merge:
                values_to_add = []
                collect_values_from_trie(trie_from, 0, BIT_LEN - 1, values_to_add)
                for val in values_to_add:
                    final_trie_for_u.add(val)
            
            memoized_tries[u] = final_trie_for_u
            return final_trie_for_u

        dfs_build_trie(0) # Start building Tries from the root (node 0)

        # 4. Answer queries
        results = []
        for uj, kj in queries:
            results.append(memoized_tries[uj].get_kth_smallest(kj))
            
        return results

