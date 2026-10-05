"""
Count Dominant Nodes in a Binary Tree
Difficulty: Medium

Description:
This problem asks us to count the number of "dominant" nodes in a complete binary tree. A node is considered dominant if its value is equal to the maximum value found within its own subtree (including itself). The input is the root of a complete binary tree, and we need to return the total count of such dominant nodes.

Example:
Input: root = [5,3,8,2,4,7,1]
Output: 5
Explanation: The dominant nodes are the leaf nodes 2, 4, 7, and 1, as well as the node with value 8 (since 8 is the maximum in its subtree [8,7,1]).

Approach:
The problem can be solved efficiently using a recursive Depth-First Search (DFS) approach, specifically a post-order traversal. We define a helper function `dfs` that, for each node, recursively calculates the maximum value present in its left subtree and right subtree. It then determines the maximum value for the current node's entire subtree by taking the maximum of the current node's value, the maximum from the left subtree, and the maximum from the right subtree. If the current node's value is equal to this overall maximum for its subtree, it is a dominant node, and we increment a counter. The `dfs` function then returns this overall maximum subtree value to its parent, enabling the parent to perform its own calculations. The base case for the recursion is when a node is `None`, in which case it returns `float('-inf')` to ensure it does not influence maximum calculations of actual nodes.

Time Complexity: O(N)
Space Complexity: O(log N)
"""
from typing import List, Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def countDominantNodes(self, root: TreeNode | None) -> int:
        self.dominant_count = 0

        def dfs(node: TreeNode | None) -> int:
            # Base case: if node is None, it contributes negative infinity to max calculations
            # This ensures that non-existent children don't falsely inflate the max.
            if not node:
                return float('-inf')

            # Recursively find the maximum value in the left and right subtrees
            max_val_left_subtree = dfs(node.left)
            max_val_right_subtree = dfs(node.right)

            # Calculate the maximum value within the current node's entire subtree.
            # This includes the node itself, the maximum from its left subtree, and the maximum from its right subtree.
            max_val_current_subtree = max(node.val, max_val_left_subtree, max_val_right_subtree)

            # If the current node's value is equal to the maximum value found in its subtree,
            # then this node is dominant. Increment the global counter.
            if node.val == max_val_current_subtree:
                self.dominant_count += 1
            
            # Return the maximum value of the current subtree to its parent node.
            # This value will be used by the parent for its own max calculation.
            return max_val_current_subtree

        # Start the DFS from the root of the tree.
        if root: # The problem constraints guarantee root is not None, but good practice.
            dfs(root)
        
        return self.dominant_count

if __name__ == "__main__":
    # Helper function to build a tree from the LeetCode list format
    def build_tree(nodes: List[Optional[int]]) -> Optional[TreeNode]:
        if not nodes:
            return None
        
        root_val = nodes[0]
        if root_val is None:
            return None

        root = TreeNode(root_val)
        q = deque([root])
        i = 1
        n = len(nodes)

        while q and i < n:
            current_node = q.popleft()

            # Left child
            if i < n and nodes[i] is not None:
                current_node.left = TreeNode(nodes[i])
                q.append(current_node.left)
            i += 1

            # Right child
            if i < n and nodes[i] is not None:
                current_node.right = TreeNode(nodes[i])
                q.append(current_node.right)
            i += 1
        
        return root

    s = Solution()

    # Example 1
    root1 = build_tree([5,3,8,2,4,7,1])
    assert s.countDominantNodes(root1) == 5, f"Test 1 Failed: Expected 5, Got {s.countDominantNodes(root1)}"

    # Example 2
    root2 = build_tree([1,2,3,1,2])
    assert s.countDominantNodes(root2) == 4, f"Test 2 Failed: Expected 4, Got {s.countDominantNodes(root2)}"

    # Test case: Single node tree
    root3 = build_tree([10])
    assert s.countDominantNodes(root3) == 1, f"Test 3 Failed: Expected 1, Got {s.countDominantNodes(root3)}"

    # Test case: All nodes have the same value (all should be dominant)
    root4 = build_tree([5,5,5,5,5,5,5])
    assert s.countDominantNodes(root4) == 7, f"Test 4 Failed: Expected 7, Got {s.countDominantNodes(root4)}"

    # Test case: Values generally increasing with depth, leaves are dominant
    # In this case, 4,5,6,7 are dominant. 2 (max in [2,4,5] is 5) is not. 3 (max in [3,6,7] is 7) is not. 1 (max in [1,2,3,4,5,6,7] is 7) is not.
    root5 = build_tree([1,2,3,4,5,6,7])
    assert s.countDominantNodes(root5) == 4, f"Test 5 Failed: Expected 4, Got {s.countDominantNodes(root5)}"
    
    # Test case: Mixed values where some internal nodes are dominant, some not
    #      10
    #     /  \
    #    8    12
    #   / \   / \
    #  7   9 11  15
    # Dominant: 7, 9, 11, 15 (leaves). Total: 4.
    # 8 (max in [8,7,9] is 9) - not dominant.
    # 12 (max in [12,11,15] is 15) - not dominant.
    # 10 (max in [10,8,12,7,9,11,15] is 15) - not dominant.
    root6 = build_tree([10,8,12,7,9,11,15])
    assert s.countDominantNodes(root6) == 4, f"Test 6 Failed: Expected 4, Got {s.countDominantNodes(root6)}"

    # Test case: Values decreasing such that all nodes are dominant
    #     10
    #    /  \
    #   9    8
    #  / \  / \
    # 7  6 5  4
    # Dominant: 7,6,5,4 (leaves). 9 (max in [9,7,6] is 9). 8 (max in [8,5,4] is 8). 10 (max in [10,9,8,7,6,5,4] is 10).
    # All 7 nodes are dominant.
    root7 = build_tree([10,9,8,7,6,5,4])
    assert s.countDominantNodes(root7) == 7, f"Test 7 Failed: Expected 7, Got {s.countDominantNodes(root7)}"

    print("All tests passed!")

```