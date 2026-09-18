"""
Sum of Perfect Square Ancestors
Difficulty: Hard

Description:
This problem asks us to find the sum of ti for all non-root nodes i, where ti is the count of ancestors of i such that the product nums[i] * nums[ancestor] is a perfect square. A key property is that the product of two positive integers X and Y is a perfect square if and only if their square-free parts are identical.

Example:
Input: n = 3, edges = [[0,1],[1,2]], nums = [2,8,2]
Output: 3
Explanation: For node 1, its ancestor 0 has nums[0]=2, nums[1]=8. nums[0]*nums[1]=16 (perfect square). Thus t1=1.
For node 2, its ancestors are 1 and 0. nums[2]=2. nums[2]*nums[1]=16 (perfect square) and nums[2]*nums[0]=4 (perfect square). Thus t2=2.
The total sum is t1 + t2 = 1 + 2 = 3.

Approach:
The solution leverages the property that the product of two numbers is a perfect square if and only if their square-free parts are equal. We first precompute the square-free part for every number in the `nums` array. Then, we perform a Depth-First Search (DFS) starting from the root node 0. During the DFS, we maintain a frequency map (using `collections.Counter`) to keep track of the square-free parts encountered along the current path from the root to the current node's parent. When visiting a node `u`, we calculate `ti` for `u` by querying this frequency map for `sf_nums[u]`. After calculating `ti`, we add `sf_nums[u]` to the frequency map before recursively calling DFS on its children. Upon returning from a child's DFS call, we decrement the count for `sf_nums[u]` in the frequency map to correctly backtrack, ensuring the map always represents only the ancestors for subsequent sibling branches.

Time Complexity: O(N * sqrt(max_val_in_nums)) where N is the number of nodes and max_val_in_nums is the maximum value in the `nums` array. This is because we iterate through N numbers to compute their square-free parts, each taking up to O(sqrt(max_val_in_nums)) time, and then perform a single DFS traversal taking O(N) time.
Space Complexity: O(N) for the adjacency list, `sf_nums` array, DFS recursion stack, and the frequency map `sf_counts`.
"""
from typing import List
import collections

class Solution:
    def sumOfAncestors(self, n: int, edges: List[List[int]], nums: List[int]) -> int:
        
        def get_sf(num: int) -> int:
            """
            Calculates the square-free part of a positive integer.
            The square-free part of k is the product of its prime factors that appear an odd number of times
            in its prime factorization.
            """
            sf = 1
            d = 2
            temp_num = num
            # Iterate through potential prime factors up to sqrt(temp_num)
            # The loop condition d * d <= temp_num ensures we check factors up to sqrt(original num)
            while d * d <= temp_num:
                if temp_num % d == 0:
                    count = 0
                    while temp_num % d == 0:
                        count += 1
                        temp_num //= d
                    if count % 2 == 1: # If prime factor appears an odd number of times, include it in sf
                        sf *= d
                d += 1
            # If temp_num is still greater than 1 after the loop, it means the remaining temp_num
            # is a prime factor itself (and it appears once, thus odd count).
            if temp_num > 1:
                sf *= temp_num
            return sf

        # 1. Precompute square-free parts for all numbers in nums
        sf_nums = [get_sf(num) for num in nums]

        # 2. Build adjacency list for the tree structure
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        total_t_sum = 0
        # sf_counts stores the frequency of square-free values encountered in the current DFS path.
        # This map reflects the square-free parts of the ancestors of the currently visited node.
        sf_counts = collections.Counter()

        # 3. Perform DFS traversal to calculate sum of ti values
        def dfs(u: int, parent: int):
            nonlocal total_t_sum

            sf_val_u = sf_nums[u]
            
            # For the current node u (if it's not the root), check its ancestors.
            # The count sf_counts[sf_val_u] tells us how many ancestors of u have
            # the same square-free part as nums[u].
            if u != 0: # We only sum ti for nodes i in range [1, n-1]
                total_t_sum += sf_counts[sf_val_u]

            # Add current node u's square-free part to the counts for its descendants.
            # This makes u an 'ancestor' for its children in their DFS calls.
            sf_counts[sf_val_u] += 1

            # Recurse for all children of u
            for v in adj[u]:
                if v != parent: # Avoid going back up to the parent
                    dfs(v, u)
            
            # Backtrack: After visiting all descendants of u, remove u's square-free part
            # from sf_counts. This restores the state for siblings or other branches
            # in the DFS, ensuring sf_counts correctly reflects ancestors.
            sf_counts[sf_val_u] -= 1

        # Start the DFS from the root node (node 0) with a dummy parent (-1)
        dfs(0, -1)

        return total_t_sum

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    n1 = 3
    edges1 = [[0,1],[1,2]]
    nums1 = [2,8,2]
    expected1 = 3
    assert s.sumOfAncestors(n1, edges1, nums1) == expected1, f"Test 1 Failed: Expected {expected1}, Got {s.sumOfAncestors(n1, edges1, nums1)}"

    # Example 2
    n2 = 3
    edges2 = [[0,1],[0,2]]
    nums2 = [1,2,4]
    expected2 = 1
    assert s.sumOfAncestors(n2, edges2, nums2) == expected2, f"Test 2 Failed: Expected {expected2}, Got {s.sumOfAncestors(n2, edges2, nums2)}"

    # Example 3
    n3 = 4
    edges3 = [[0,1],[0,2],[1,3]]
    nums3 = [1,2,9,4]
    expected3 = 2
    assert s.sumOfAncestors(n3, edges3, nums3) == expected3, f"Test 3 Failed: Expected {expected3}, Got {s.sumOfAncestors(n3, edges3, nums3)}"
    
    # Additional Test Case: Single node tree
    n4 = 1
    edges4 = []
    nums4 = [100]
    expected4 = 0 # No nodes in range [1, n-1]
    assert s.sumOfAncestors(n4, edges4, nums4) == expected4, f"Test 4 Failed: Expected {expected4}, Got {s.sumOfAncestors(n4, edges4, nums4)}"

    # Additional Test Case: More complex tree with varied square-free parts
    n5 = 7
    edges5 = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
    nums5 = [1, 2, 3, 8, 12, 5, 27]
    # sf_nums: [1, 2, 3, 2, 3, 5, 3]
    # Node 0 (sf=1) - root
    # Node 1 (sf=2) - parent 0 (sf=1). sf_counts={1:1}. t1=sf_counts[2]=0. sf_counts={1:1, 2:1}
    #   Node 3 (sf=2) - parent 1 (sf=2). sf_counts={1:1, 2:1}. t3=sf_counts[2]=1. sf_counts={1:1, 2:2}
    #     -> Pop 3: sf_counts={1:1, 2:1}
    #   Node 4 (sf=3) - parent 1 (sf=2). sf_counts={1:1, 2:1}. t4=sf_counts[3]=0. sf_counts={1:1, 2:1, 3:1}
    #     -> Pop 4: sf_counts={1:1, 2:1}
    # -> Pop 1: sf_counts={1:1}
    # Node 2 (sf=3) - parent 0 (sf=1). sf_counts={1:1}. t2=sf_counts[3]=0. sf_counts={1:1, 3:1}
    #   Node 5 (sf=5) - parent 2 (sf=3). sf_counts={1:1, 3:1}. t5=sf_counts[5]=0. sf_counts={1:1, 3:1, 5:1}
    #     -> Pop 5: sf_counts={1:1, 3:1}
    #   Node 6 (sf=3) - parent 2 (sf=3). sf_counts={1:1, 3:1}. t6=sf_counts[3]=1. sf_counts={1:1, 3:2}
    #     -> Pop 6: sf_counts={1:1, 3:1}
    # -> Pop 2: sf_counts={1:1}
    # -> Pop 0: sf_counts={}
    # Total t = 0 (t1) + 1 (t3) + 0 (t4) + 0 (t2) + 0 (t5) + 1 (t6) = 2
    expected5 = 2 
    assert s.sumOfAncestors(n5, edges5, nums5) == expected5, f"Test 5 Failed: Expected {expected5}, Got {s.sumOfAncestors(n5, edges5, nums5)}"

    print("All tests passed!")

```