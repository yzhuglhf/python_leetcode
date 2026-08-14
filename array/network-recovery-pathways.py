"""
Network Recovery Pathways
Difficulty: Hard

Description:
This problem asks us to find the maximum possible "path score" among all valid paths from node 0 to node n-1 in a directed acyclic graph. A path is valid if all its intermediate nodes are online, its total recovery cost does not exceed `k`, and its score is defined as the minimum edge cost along that path. We need to return the largest such minimum edge cost, or -1 if no valid path exists.

Example:
Input: edges = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]], online = [true,true,true,false,true], k = 12
Output: 6
Explanation: Node 3 is offline, making paths through it invalid. Path 0->1->4 has total cost 12 <= k and min edge cost 5. Path 0->2->4 has total cost 12 <= k and min edge cost 6. The maximum of these path scores is 6.

Approach:
The problem asks for the maximum of a minimum value, which is a classic pattern solvable with binary search on the answer. We binary search for the "path score" (let's call it `X`). For a given `X`, we need a `check(X)` function that determines if a valid path exists where all its edges have a cost of at least `X`, and the total cost of that path does not exceed `k`.

The `check(X)` function works as follows:
1.  **Graph Construction:** Build a temporary graph containing only edges `(u, v, cost)` from the original `edges` list that satisfy two conditions:
    *   `cost >= X` (to meet the minimum edge-cost requirement).
    *   `online[u]` is true and `online[v]` is true. This ensures that all nodes involved in a path are online. Since nodes 0 and n-1 are guaranteed online, this covers the "intermediate nodes must be online" rule as well.
2.  **Shortest Path in DAG:** Since the graph is a Directed Acyclic Graph (DAG) and edge weights (costs) are non-negative, we can find the shortest path from node 0 to node n-1 using a topological sort-based dynamic programming approach.
    *   Initialize `dist[i] = infinity` for all nodes `i`, and `dist[0] = 0`.
    *   Compute the in-degree for all nodes in the temporary graph.
    *   Initialize a queue with all nodes that have an in-degree of 0.
    *   While the queue is not empty, dequeue a node `u`. If `dist[u]` is infinity (meaning `u` is unreachable from node 0), skip it. For each neighbor `v` of `u` with edge cost `edge_cost`, relax the edge: `dist[v] = min(dist[v], dist[u] + edge_cost)`. Then, decrement `v`'s in-degree. If `v`'s in-degree becomes 0, enqueue `v`.
3.  **Result:** After processing all nodes, if `dist[n-1] <= k`, it means a path exists from 0 to n-1 satisfying the minimum edge cost and total cost constraints, so `check(X)` returns `true`. Otherwise, it returns `false`.

The binary search proceeds over the possible range of edge costs, `[0, 10^9]`. If `check(mid)` is true, it means `mid` is an achievable score, so we try for a higher score (`low = mid + 1`). If `check(mid)` is false, we must try a lower score (`high = mid - 1`). The `max_path_score` variable keeps track of the largest `mid` for which `check(mid)` returned true. If no valid path is found even for `X=0`, `max_path_score` remains -1.

Time Complexity: O((N + M) * log(C_max))
    - `N` is the number of nodes, `M` is the number of edges.
    - The `check` function involves building an adjacency list and in-degree array (O(M)), and then performing a topological sort-based shortest path calculation (O(N+M)). So, `check` is O(N+M).
    - The binary search performs `log(C_max)` iterations, where `C_max` is the maximum possible edge cost (10^9). `log(10^9)` is approximately 30.
    - Total time complexity: `O((N + M) * log(C_max))`. Given `N=5*10^4`, `M=10^5`, this is roughly `(5*10^4 + 10^5) * 30 = 1.5 * 10^5 * 30 = 4.5 * 10^6` operations, which is efficient enough.
Space Complexity: O(N + M)
    - Adjacency list and in-degree array: O(N + M).
    - Distance array: O(N).
    - Queue for topological sort: O(N).
    - Total space complexity: O(N + M).
"""
import heapq
import collections
from typing import List

class Solution:
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        n = len(online)

        def check(min_cost_threshold: int) -> bool:
            """
            Checks if there exists a path from 0 to n-1 such that:
            1. All edges on the path have cost >= min_cost_threshold.
            2. All nodes (including intermediate, 0, and n-1) on the path are online.
            3. The total cost of the path does not exceed k.
            """
            adj = [[] for _ in range(n)]
            in_degree = [0] * n # To compute topological order

            # Build the graph with filtered edges and compute in-degrees.
            # An edge (u, v, cost) is valid if:
            # - cost >= min_cost_threshold
            # - online[u] is true (which is implicitly true for u=0, n-1 as per problem)
            # - online[v] is true (which is implicitly true for v=0, n-1 as per problem)
            for u, v, cost in edges:
                if cost >= min_cost_threshold and online[u] and online[v]:
                    adj[u].append((v, cost))
                    in_degree[v] += 1
            
            # DP array for shortest path distances
            dist = [float('inf')] * n
            dist[0] = 0 # Starting node 0 has 0 cost

            # Queue for topological sort (Kahn's algorithm)
            q = collections.deque()
            for i in range(n):
                if in_degree[i] == 0:
                    q.append(i)
            
            # Process nodes in topological order to find shortest paths
            while q:
                u = q.popleft()

                # If node u is unreachable from source 0 in the current filtered graph,
                # we should not use it to relax other edges.
                if dist[u] == float('inf'):
                    continue
                
                for v, edge_cost in adj[u]:
                    # Relax edge (u, v)
                    if dist[u] + edge_cost < dist[v]:
                        dist[v] = dist[u] + edge_cost
                    
                    # Decrement in-degree of v and add to queue if it becomes 0
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        q.append(v)
            
            return dist[n-1] <= k

        # Binary search for the maximum possible path score (minimum edge cost)
        # The path score can range from 0 to 10^9 (max_costi)
        # max_costi is 10^9 as per constraints
        low, high = 0, 10**9 
        max_path_score = -1

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                # If a path exists where all edges are at least 'mid',
                # then 'mid' is an achievable path score.
                # We try to find a larger score.
                max_path_score = mid
                low = mid + 1
            else:
                # No path exists where all edges are at least 'mid'.
                # We need to try a smaller score.
                high = mid - 1
                
        return max_path_score

if __name__ == "__main__":
    s = Solution()

    # Example 1
    edges1 = [[0,1,5],[1,3,10],[0,2,3],[2,3,4]]
    online1 = [True,True,True,True]
    k1 = 10
    assert s.findMaxPathScore(edges1, online1, k1) == 3, f"Test 1 Failed: Expected 3, got {s.findMaxPathScore(edges1, online1, k1)}"

    # Example 2
    edges2 = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]]
    online2 = [True,True,True,False,True]
    k2 = 12
    assert s.findMaxPathScore(edges2, online2, k2) == 6, f"Test 2 Failed: Expected 6, got {s.findMaxPathScore(edges2, online2, k2)}"

    # Custom Test 1: No valid path (k too small)
    edges3 = [[0,1,5],[1,2,5]]
    online3 = [True,True,True]
    k3 = 9
    assert s.findMaxPathScore(edges3, online3, k3) == -1, f"Test 3 Failed: Expected -1, got {s.findMaxPathScore(edges3, online3, k3)}"

    # Custom Test 2: No valid path (offline node)
    edges4 = [[0,1,5],[1,2,5]]
    online4 = [True,False,True]
    k4 = 10
    assert s.findMaxPathScore(edges4, online4, k4) == -1, f"Test 4 Failed: Expected -1, got {s.findMaxPathScore(edges4, online4, k4)}"

    # Custom Test 3: Multiple paths, same max score
    edges5 = [[0,1,10],[1,3,5],[0,2,8],[2,3,7]]
    online5 = [True,True,True,True]
    k5 = 20
    assert s.findMaxPathScore(edges5, online5, k5) == 7, f"Test 5 Failed: Expected 7, got {s.findMaxPathScore(edges5, online5, k5)}"
    # Path 0->1->3: costs 10,5. Total 15. Min edge 5.
    # Path 0->2->3: costs 8,7. Total 15. Min edge 7. Max is 7.

    # Custom Test 4: Single edge path
    edges6 = [[0,1,100]]
    online6 = [True,True]
    k6 = 100
    assert s.findMaxPathScore(edges6, online6, k6) == 100, f"Test 6 Failed: Expected 100, got {s.findMaxPathScore(edges6, online6, k6)}"

    # Custom Test 5: All edges too expensive for k, but valid paths for smaller k
    edges7 = [[0,1,10],[1,2,10]]
    online7 = [True,True,True]
    k7 = 19
    assert s.findMaxPathScore(edges7, online7, k7) == -1, f"Test 7 Failed: Expected -1, got {s.findMaxPathScore(edges7, online7, k7)}" # min_cost_threshold=10 -> total 20 > 19

    print("All tests passed!")