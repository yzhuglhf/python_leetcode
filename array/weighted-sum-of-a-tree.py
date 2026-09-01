"""
Weighted Sum of a Tree
Difficulty: Medium

Description:
This problem asks us to calculate the sum of weighted values for all nodes in a given rooted tree.
The weight of a node is determined by its value, its depth, and the overall height of the tree,
following the formula: nums[i] * (h - d + 1), where h is the tree's height and d is the node's depth.
The tree is rooted at node 0, and depth is 1-indexed (root at depth 1).

Example:
Input: parent = [-1,0,0,0,2,2], nums = [5,2,3,1,4,6]
Output: 37
Explanation: Tree height is 3.
Node 0 (depth 1, value 5) weight = 5*(3-1+1)=15.
Node 1 (depth 2, value 2) weight = 2*(3-2+1)=4.
Node 2 (depth 2, value 3) weight = 3*(3-2+1)=6.
Node 3 (depth 2, value 1) weight = 1*(3-2+1)=2.
Node 4 (depth 3, value 4) weight = 4*(3-3+1)=4.
Node 5 (depth 3, value 6) weight = 6*(3-3+1)=6.
Sum = 15+4+6+2+4+6 = 37.

Approach:
The solution involves three main steps. First, we transform the parent array representation into an adjacency list to easily traverse the tree from parent to children. Second, we perform a Breadth-First Search (BFS) starting from the root (node 0) to simultaneously calculate the depth of every node and determine the maximum depth, which is the overall height (h) of the tree. The root is explicitly set to depth 1, and subsequent nodes are assigned depths relative to their parents. Finally, with the tree height and all node depths determined, we iterate through each node, apply the given weight formula (nums[i] * (h - d + 1)), and sum up all individual node weights to get the final result.

Time Complexity: O(N)
Space Complexity: O(N)
"""
from typing import List, Optional
import collections

class Solution:
    def weightedSum(self, parent: List[int], nums: List[int]) -> int:
        n = len(parent)

        # Step 1: Build adjacency list
        # adj[u] will store a list of children of node u
        adj = [[] for _ in range(n)]
        for i in range(1, n):
            adj[parent[i]].append(i)

        # Step 2: Calculate depths for all nodes and determine tree height (h) using BFS
        depths = [0] * n  # depths[i] will store the depth of node i
        max_depth = 0     # This will become the height 'h' of the tree

        # BFS queue stores (node, current_depth)
        q = collections.deque([(0, 1)]) # Node 0 is the root, depth 1
        depths[0] = 1 # Set depth for the root

        while q:
            u, d = q.popleft()
            max_depth = max(max_depth, d) # Update max_depth if current node's depth is greater

            # Enqueue children with incremented depth
            for v in adj[u]:
                depths[v] = d + 1
                q.append((v, d + 1))
        
        h = max_depth # The height of the tree is the maximum depth found

        # Step 3: Calculate the total weighted sum
        total_weight_sum = 0
        for i in range(n):
            d = depths[i]
            # Weight formula: nums[i] * (h - d + 1)
            weight = nums[i] * (h - d + 1)
            total_weight_sum += weight
        
        return total_weight_sum

if __name__ == "__main__":
    s = Solution()

    # Example 1 from problem description
    parent1 = [-1,0,0,0,2,2]
    nums1 = [5,2,3,1,4,6]
    expected1 = 37
    assert s.weightedSum(parent1, nums1) == expected1, f"Test 1 Failed: Expected {expected1}, got {s.weightedSum(parent1, nums1)}"

    # Example 2 from problem description
    parent2 = [-1,0,1,2]
    nums2 = [1,2,3,4]
    expected2 = 20
    assert s.weightedSum(parent2, nums2) == expected2, f"Test 2 Failed: Expected {expected2}, got {s.weightedSum(parent2, nums2)}"

    # Test Case 3: Single node tree
    # Node 0, value 10. Depth 1, Height 1. Weight = 10 * (1 - 1 + 1) = 10.
    parent3 = [-1]
    nums3 = [10]
    expected3 = 10
    assert s.weightedSum(parent3, nums3) == expected3, f"Test 3 Failed: Expected {expected3}, got {s.weightedSum(parent3, nums3)}"

    # Test Case 4: A long chain (max height)
    # Tree: 0 -> 1 -> 2 -> 3 -> 4 -> 5
    # n=6, height=6
    # Node 0 (d=1, v=1): 1 * (6-1+1) = 6
    # Node 1 (d=2, v=1): 1 * (6-2+1) = 5
    # Node 2 (d=3, v=1): 1 * (6-3+1) = 4
    # Node 3 (d=4, v=1): 1 * (6-4+1) = 3
    # Node 4 (d=5, v=1): 1 * (6-5+1) = 2
    # Node 5 (d=6, v=1): 1 * (6-6+1) = 1
    # Total sum = 6 + 5 + 4 + 3 + 2 + 1 = 21
    parent4 = [-1, 0, 1, 2, 3, 4]
    nums4 = [1, 1, 1, 1, 1, 1]
    expected4 = 21
    assert s.weightedSum(parent4, nums4) == expected4, f"Test 4 Failed: Expected {expected4}, got {s.weightedSum(parent4, nums4)}"

    # Test Case 5: A wide tree (shallow height)
    # Tree: Node 0 is parent of 1,2,3,4,5.
    # n=6, height=2
    # Node 0 (d=1, v=10): 10 * (2-1+1) = 10 * 2 = 20
    # Node 1 (d=2, v=1): 1 * (2-2+1) = 1 * 1 = 1
    # Node 2 (d=2, v=1): 1 * (2-2+1) = 1 * 1 = 1
    # Node 3 (d=2, v=1): 1 * (2-2+1) = 1 * 1 = 1
    # Node 4 (d=2, v=1): 1 * (2-2+1) = 1 * 1 = 1
    # Node 5 (d=2, v=1): 1 * (2-2+1) = 1 * 1 = 1
    # Total sum = 20 + 1 + 1 + 1 + 1 + 1 = 25
    parent5 = [-1, 0, 0, 0, 0, 0]
    nums5 = [10, 1, 1, 1, 1, 1]
    expected5 = 25
    assert s.weightedSum(parent5, nums5) == expected5, f"Test 5 Failed: Expected {expected5}, got {s.weightedSum(parent5, nums5)}"

    # Test Case 6: Larger values, structure similar to Example 1
    parent6 = [-1,0,0,0,2,2]
    nums6 = [100,20,30,10,40,60]
    # h = 3
    # Node 0 (d=1, v=100): 100 * (3-1+1) = 100 * 3 = 300
    # Node 1 (d=2, v=20): 20 * (3-2+1) = 20 * 2 = 40
    # Node 2 (d=2, v=30): 30 * (3-2+1) = 30 * 2 = 60
    # Node 3 (d=2, v=10): 10 * (3-2+1) = 10 * 2 = 20
    # Node 4 (d=3, v=40): 40 * (3-3+1) = 40 * 1 = 40
    # Node 5 (d=3, v=60): 60 * (3-3+1) = 60 * 1 = 60
    # Total sum = 300 + 40 + 60 + 20 + 40 + 60 = 520
    expected6 = 520
    assert s.weightedSum(parent6, nums6) == expected6, f"Test 6 Failed: Expected {expected6}, got {s.weightedSum(parent6, nums6)}"

    print("All tests passed!")
```