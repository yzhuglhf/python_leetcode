"""
Minimum Threshold Path With Limited Heavy Edges
Difficulty: Hard

Description:
This problem asks us to find the minimum integer threshold such that there exists a path from a given source node to a target node containing at most 'k' "heavy" edges. An edge is classified as heavy if its weight exceeds the threshold, and light otherwise. If no such path exists for any threshold, return -1.

Example:
Input: n = 6, edges = [[0,1,5],[1,2,3],[3,4,4],[4,5,1],[1,4,2]], source = 0, target = 3, k = 1
Output: 4
Explanation: With a threshold of 4, edges with weight <= 4 are light, and edges with weight > 4 are heavy. Only edge [0,1,5] is heavy. A path 0 -> 1 -> 4 -> 3 uses this single heavy edge, satisfying k=1. Any smaller threshold would require more than one heavy edge.

Approach:
The problem exhibits a monotonic property with respect to the threshold: if a path exists for a given threshold, it will also exist for any larger threshold (as more edges become light or stay light, reducing or keeping constant the number of heavy edges). This monotonicity allows us to use binary search on the threshold value. The search range for the threshold is from 0 (to handle cases like source==target) up to 10^9 + 1 (the maximum possible edge weight plus one, to ensure all real edge weights are covered).
For each candidate threshold value during the binary search, we need a `check` function to determine if a valid path (at most 'k' heavy edges) exists. This `check` function is efficiently implemented using a 0-1 Breadth-First Search (BFS). In this BFS, edges whose weights are less than or equal to the current `threshold_val` are treated as having a "cost" of 0 (light), and edges whose weights are strictly greater than `threshold_val` have a "cost" of 1 (heavy). The 0-1 BFS finds the minimum number of heavy edges required to reach any node from the source. If the minimum number of heavy edges to reach the target is less than or equal to 'k', the `check` function returns true, indicating that the current threshold is valid; otherwise, it returns false. The binary search then adjusts its range (`low` or `high`) based on the result of `check` to find the smallest valid threshold. If no threshold works (i.e., `check` always returns false), `ans` remains -1.

Time Complexity: O((N + E) * log(max_W))
-   The binary search performs `O(log(max_W))` iterations, where `max_W` is the maximum possible edge weight (10^9).
-   Inside each iteration, the `check` function (0-1 BFS) traverses the graph, taking `O(N + E)` time, where `N` is the number of nodes and `E` is the number of edges.
-   Overall, the total time complexity is `O((N + E) * log(max_W))`.

Space Complexity: O(N + E)
-   The adjacency list `adj` stores the graph, requiring `O(N + E)` space.
-   The `dist` array for the 0-1 BFS takes `O(N)` space.
-   The deque `dq` for the 0-1 BFS can store up to `O(N)` nodes in the worst case.
-   Therefore, the total space complexity is `O(N + E)`.
"""
from typing import List
import collections

class Solution:
    def minimumThreshold(self, n: int, edges: List[List[int]], source: int, target: int, k: int) -> int:
        
        # Build adjacency list
        # adj[u] will store a list of (neighbor_node, edge_weight) tuples
        adj = collections.defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w)) # Graph is undirected

        # check(threshold_val) function:
        # Determines if a path from 'source' to 'target' exists with at most 'k' heavy edges,
        # given the current 'threshold_val'.
        # Uses 0-1 BFS, where edge cost is 0 for light edges and 1 for heavy edges.
        def check(threshold_val: int) -> bool:
            # dist[i] stores the minimum number of heavy edges encountered to reach node i from 'source'.
            dist = [float('inf')] * n
            dist[source] = 0
            
            # Deque for 0-1 BFS:
            # Nodes reachable via 0-cost (light) edges are pushed to the front (higher priority).
            # Nodes reachable via 1-cost (heavy) edges are pushed to the back (lower priority).
            dq = collections.deque()
            dq.append(source)

            while dq:
                u = dq.popleft()

                # Optimization: If the current path to 'u' already exceeds 'k' heavy edges,
                # there's no need to extend this path further, as it won't be valid.
                if dist[u] > k:
                    continue

                for v, weight in adj[u]:
                    # An edge is heavy if its weight is strictly greater than the threshold.
                    heavy_cost = 1 if weight > threshold_val else 0
                    
                    # If we found a shorter path (in terms of heavy edges) to 'v'
                    if dist[u] + heavy_cost < dist[v]:
                        dist[v] = dist[u] + heavy_cost
                        if heavy_cost == 0:
                            dq.appendleft(v) # Prioritize light edges
                        else:
                            dq.append(v)     # Process heavy edges later
            
            # A valid path exists if the target can be reached with 'k' or fewer heavy edges.
            return dist[target] <= k

        # Binary search for the minimum threshold value.
        # The range for `threshold` is from 0 (e.g., if source == target, threshold 0 is valid)
        # up to 10^9 + 1 (the maximum possible edge weight is 10^9, so +1 ensures we can make all edges light).
        low = 0
        high = 10**9 + 1 
        ans = -1 # Initialize 'ans' to -1, which will be returned if no valid path is found.

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                # If a valid path exists with 'mid' as the threshold,
                # 'mid' is a potential answer. We try to find an even smaller threshold.
                ans = mid
                high = mid - 1 
            else:
                # If no valid path exists with 'mid' as the threshold,
                # we need a larger threshold to make more edges light.
                low = mid + 1

        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 6
    edges1 = [[0,1,5],[1,2,3],[3,4,4],[4,5,1],[1,4,2]]
    source1 = 0
    target1 = 3
    k1 = 1
    expected1 = 4
    assert s.minimumThreshold(n1, edges1, source1, target1, k1) == expected1, f"Test 1 Failed: Expected {expected1}, Got {s.minimumThreshold(n1, edges1, source1, target1, k1)}"

    # Example 2
    n2 = 6
    edges2 = [[0,1,3],[1,2,4],[3,4,5],[4,5,6]]
    source2 = 0
    target2 = 4
    k2 = 1
    expected2 = -1
    assert s.minimumThreshold(n2, edges2, source2, target2, k2) == expected2, f"Test 2 Failed: Expected {expected2}, Got {s.minimumThreshold(n2, edges2, source2, target2, k2)}"

    # Example 3
    n3 = 4
    edges3 = [[0,1,2],[1,2,2],[2,3,2],[3,0,2]]
    source3 = 0
    target3 = 0
    k3 = 0
    expected3 = 0
    assert s.minimumThreshold(n3, edges3, source3, target3, k3) == expected3, f"Test 3 Failed: Expected {expected3}, Got {s.minimumThreshold(n3, edges3, source3, target3, k3)}"

    # Additional Test Case: All edges heavy, k allows 1 heavy edge
    n4 = 3
    edges4 = [[0,1,10],[1,2,10]]
    source4 = 0
    target4 = 2
    k4 = 1
    expected4 = 10 # With threshold 10, both edges become light, path has 0 heavy edges.
    assert s.minimumThreshold(n4, edges4, source4, target4, k4) == expected4, f"Test 4 Failed: Expected {expected4}, Got {s.minimumThreshold(n4, edges4, source4, target4, k4)}"

    # Additional Test Case: No edges, source != target
    n5 = 2
    edges5 = []
    source5 = 0
    target5 = 1
    k5 = 0
    expected5 = -1
    assert s.minimumThreshold(n5, edges5, source5, target5, k5) == expected5, f"Test 5 Failed: Expected {expected5}, Got {s.minimumThreshold(n5, edges5, source5, target5, k5)}"

    # Additional Test Case: Larger k, single path, mixed weights
    n6 = 4
    edges6 = [[0,1,100],[1,2,10],[2,3,100]]
    source6 = 0
    target6 = 3
    k6 = 2
    expected6 = 10 # With threshold 10, edges (0,1,100) and (2,3,100) are heavy (2 total), (1,2,10) is light. Valid.
    assert s.minimumThreshold(n6, edges6, source6, target6, k6) == expected6, f"Test 6 Failed: Expected {expected6}, Got {s.minimumThreshold(n6, edges6, source6, target6, k6)}"

    print("All tests passed!")

