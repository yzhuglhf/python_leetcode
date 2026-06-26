"""
Count Non Adjacent Subsets in a Rooted Tree
Difficulty: Hard

Description:
This problem asks us to count non-empty subsets of nodes in a given rooted tree such that two conditions are met: the sum of values of selected nodes is divisible by `k`, and no two selected nodes are adjacent (i.e., a parent and its direct child cannot both be in the subset). The result should be returned modulo 10^9 + 7.

Example:
Input: parent = [-1,0,0,0], nums = [2,1,2,1], k = 3
Output: 2
Explanation: The valid subsets are {1, 2} (sum 1+2=3) and {2, 3} (sum 2+1=3). Node 0 is the root, and 1, 2, 3 are its children. The subsets {1,2} and {2,3} consist of non-adjacent nodes whose values sum to 3, which is divisible by 3.

Approach:
This problem can be solved using Dynamic Programming on Trees (Tree DP). For each node `u`, we need to determine the counts of valid non-adjacent subsets within its subtree, categorized by whether `u` itself is included in the subset and by the sum of node values modulo `k`.

We define two DP states for each node `u`:
1.  `dp[u][0]` is an array of size `k`, where `dp[u][0][r]` stores the number of ways to form a valid non-adjacent subset in the subtree rooted at `u`, *excluding* `u`, such that the sum of node values in this subset is congruent to `r` modulo `k`.
2.  `dp[u][1]` is an array of size `k`, where `dp[u][1][r]` stores the number of ways to form a valid non-adjacent subset in the subtree rooted at `u`, *including* `u`, such that the sum of node values in this subset is congruent to `r` modulo `k`.

We perform a Depth-First Search (DFS) starting from the root (node 0). For a leaf node `u`:
-   `dp[u][0][0] = 1`: one way to form an empty subset (sum 0) if `u` is not included.
-   `dp[u][1][nums[u] % k] = 1`: one way to form a subset containing only `u` (sum `nums[u] % k`) if `u` is included.

For an internal node `u`, we first recursively call `dfs` for all its children `v`. Then, we combine the DP results from its children:
Initialize `dp[u][0]` with `[1, 0, ..., 0]` (for empty set) and `dp[u][1]` with `[0, ..., nums[u]%k:1, ..., 0]` (for set `{u}`).
For each child `v` of `u`:
-   To update `dp[u][0]` (when `u` is not included): Since `u` is not included, `v` can either be included or not. We perform a convolution of the current `dp[u][0]` with `(dp[v][0] + dp[v][1])`. That is, for each `r1` in current `dp[u][0]` and `r2` in `(dp[v][0] + dp[v][1])`, we add `dp[u][0][r1] * (dp[v][0][r2] + dp[v][1][r2])` to `dp[u][0][(r1 + r2) % k]`.
-   To update `dp[u][1]` (when `u` is included): Since `u` is included, `v` cannot be included. We perform a convolution of the current `dp[u][1]` with `dp[v][0]`. That is, for each `r1` in current `dp[u][1]` and `r2` in `dp[v][0]`, we add `dp[u][1][r1] * dp[v][0][r2]` to `dp[u][1][(r1 + r2) % k]`.
All additions and multiplications are performed modulo `10^9 + 7`.

After the DFS completes for the root node (node 0), the total number of valid subsets whose sum is divisible by `k` is `(dp[0][0][0] + dp[0][1][0]) % MOD`.
Since the problem specifies "non-empty" subsets, and our DP state `dp[u][0][0]=1` initially accounts for the empty set, we must subtract 1 from the final result to exclude the globally empty subset.

Time Complexity: O(N * k^2). Building the adjacency list is O(N). The DFS visits each node once. For each node `u`, processing its children involves iterating through each child `v`. For each child, we perform two convolutions (merges) of `k`-sized arrays. Each convolution takes O(k^2) time. In a tree, the total number of child edges across all nodes is N-1. Thus, the total time for DP computations is O(N * k^2).
Space Complexity: O(N * k). The adjacency list takes O(N) space. The `dp` table stores two `k`-sized arrays for each of `N` nodes, resulting in O(N * k) space. The recursion stack for DFS can go up to O(N) in the worst case (skewed tree).
"""
import collections
from typing import List, Optional

class Solution:
    def countValidSubsets(self, parent: List[int], nums: List[int], k: int) -> int:
        n = len(parent)
        MOD = 10**9 + 7

        # Build adjacency list for children
        adj = collections.defaultdict(list)
        for i in range(1, n):
            adj[parent[i]].append(i)

        # dp[u][0] stores counts for subsets in subtree u, excluding u
        # dp[u][1] stores counts for subsets in subtree u, including u
        # Each is an array of size k, where index r stores count for sum % k == r
        dp = {} # Using a dictionary to store dp states for nodes

        def dfs(u: int):
            # Initialize dp states for current node u
            # dp[u][0] = [1, 0, ..., 0]: If u is not included, there's 1 way to get sum 0 (empty subset from u's subtree)
            # dp[u][1] = [0, ..., nums[u]%k:1, ..., 0]: If u is included, there's 1 way to get sum (nums[u]%k) (subset {u})
            dp[u] = [[0] * k, [0] * k]
            dp[u][0][0] = 1 
            dp[u][1][nums[u] % k] = 1

            for v in adj[u]:
                dfs(v) # Recursively solve for child v's subtree
                
                # Create temporary copies of dp[u] states before merging with child v's results.
                # This is crucial because dp[u] is being updated iteratively, and we need to use
                # the values before processing the current child v for proper convolution.
                current_dp0 = list(dp[u][0]) 
                current_dp1 = list(dp[u][1])
                
                # Initialize new dp arrays for the merged results
                next_dp0 = [0] * k
                next_dp1 = [0] * k

                # Perform convolution-like merge for dp[u][0] (u not included)
                for r_u in range(k):
                    if current_dp0[r_u] == 0: # Optimization: skip if no ways for this remainder
                        continue
                    for r_v in range(k):
                        # If u is not included, child v can either be included or not.
                        # So, sum ways from dp[v][0][r_v] and dp[v][1][r_v].
                        ways_from_child_v = (dp[v][0][r_v] + dp[v][1][r_v]) % MOD
                        
                        if ways_from_child_v > 0:
                            new_remainder = (r_u + r_v) % k
                            next_dp0[new_remainder] = (next_dp0[new_remainder] + current_dp0[r_u] * ways_from_child_v) % MOD

                # Perform convolution-like merge for dp[u][1] (u included)
                for r_u in range(k):
                    if current_dp1[r_u] == 0: # Optimization: skip if no ways for this remainder
                        continue
                    for r_v in range(k):
                        # If u is included, child v CANNOT be included.
                        # So, only consider ways from dp[v][0][r_v].
                        ways_from_child_v = dp[v][0][r_v]
                        
                        if ways_from_child_v > 0:
                            new_remainder = (r_u + r_v) % k
                            next_dp1[new_remainder] = (next_dp1[new_remainder] + current_dp1[r_u] * ways_from_child_v) % MOD
                
                # Update dp[u] with the merged results
                dp[u][0] = next_dp0
                dp[u][1] = next_dp1
        
        # Start the DFS from the root node (node 0)
        dfs(0) 

        # The total number of valid non-empty subsets with sum divisible by k (remainder 0)
        # is the sum of ways from dp[0][0][0] (root 0 not included) and dp[0][1][0] (root 0 included).
        total_valid_subsets = (dp[0][0][0] + dp[0][1][0]) % MOD

        # Our DP initialization includes the empty set (sum 0) in dp[u][0][0].
        # This empty set propagates up, resulting in one count for the global empty set in total_valid_subsets.
        # Since the problem asks for "non-empty" subsets, we must subtract 1.
        return (total_valid_subsets - 1 + MOD) % MOD

if __name__ == "__main__":
    s = Solution()

    # Example 1
    parent1 = [-1,0,1]
    nums1 = [1,2,3]
    k1 = 3
    assert s.countValidSubsets(parent1, nums1, k1) == 1, f"Test 1 Failed: Expected 1, Got {s.countValidSubsets(parent1, nums1, k1)}"

    # Example 2
    parent2 = [-1,0,0,0]
    nums2 = [2,1,2,1]
    k2 = 3
    assert s.countValidSubsets(parent2, nums2, k2) == 2, f"Test 2 Failed: Expected 2, Got {s.countValidSubsets(parent2, nums2, k2)}"

    # Custom Test 1: Simple case, k=1 (any sum is divisible by 1)
    parent3 = [-1,0,1]
    nums3 = [1,1,1]
    k3 = 1
    assert s.countValidSubsets(parent3, nums3, k3) == 4, f"Test 3 Failed: Expected 4, Got {s.countValidSubsets(parent3, nums3, k3)}"

    # Custom Test 2: More complex tree, k=5
    parent4 = [-1,0,0,0,1]
    nums4 = [5,1,2,3,4]
    k4 = 5
    assert s.countValidSubsets(parent4, nums4, k4) == 2, f"Test 4 Failed: Expected 2, Got {s.countValidSubsets(parent4, nums4, k4)}"

    # Custom Test 3: All values same, k=2, a path graph
    parent5 = [-1,0,1,2]
    nums5 = [1,1,1,1]
    k5 = 2
    assert s.countValidSubsets(parent5, nums5, k5) == 2, f"Test 5 Failed: Expected 2, Got {s.countValidSubsets(parent5, nums5, k5)}"

    print("All tests passed!")

