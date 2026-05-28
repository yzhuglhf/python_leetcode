import heapq
import math
from typing import List

"""
Minimum Cost to Buy Apples II
Difficulty: Hard

Description:
This problem asks us to find the minimum cost to acquire apples for each starting shop `i`. For each shop `i`, we have two options: buy apples locally at `prices[i]`, or travel empty to another shop `j`, buy apples there for `prices[j]`, and then return to shop `i` carrying apples. The cost of travel differs based on whether one is carrying apples or not, with roads having a `cost` for empty travel and `cost * taxi` for travel with apples.

Example:
Input: n = 2, prices = [8,3], roads = [[0,1,1,2]]
Output: [6,3]
Explanation: For shop 0, buying locally costs 8. Traveling to shop 1 (cost 1), buying for 3, and returning to shop 0 with apples (road 0-1 costs 1*2=2) costs 1+3+2=6. Min is 6. For shop 1, buying locally costs 3. Traveling to shop 0 (cost 1), buying for 8, and returning to shop 1 with apples (road 0-1 costs 1*2=2) costs 1+8+2=11. Min is 3.

Approach:
The problem requires finding minimum costs involving shortest paths on two different graphs: one for empty travel and one for travel with apples. We construct two adjacency lists: `adj_empty` where edge weights are `costi`, and `adj_with_apples` where edge weights are `costi * taxi`. Since we need to find shortest paths from all possible starting shops `i` to all possible intermediate shops `j` (for empty travel) and from all intermediate shops `j` back to all starting shops `i` (for travel with apples), we use Dijkstra's algorithm `N` times for each graph. This results in two `N x N` matrices, `all_dist_empty` and `all_dist_with_apples`, storing the shortest path distances between all pairs of nodes for each travel type. Finally, for each shop `i`, we calculate its minimum cost by taking the minimum of `prices[i]` (local purchase) and `all_dist_empty[i][j] + prices[j] + all_dist_with_apples[j][i]` for all possible intermediate shops `j`.

Time Complexity: O(N * (E log N)) where N is the number of shops and E is the number of roads. This is because we run Dijkstra's algorithm `N` times for each of the two graphs. Each Dijkstra run takes O(E log N) time using a min-priority queue.
Space Complexity: O(N^2 + E) to store the two adjacency lists and the two N x N distance matrices.
"""
class Solution:
    def minCost(self, n: int, prices: List[int], roads: List[List[int]]) -> List[int]:
        # Step 1: Initialize adjacency lists for two graphs
        # Graph 1: Travel empty (original cost)
        # Graph 2: Travel with apples (cost * taxi)
        adj_empty = [[] for _ in range(n)]
        adj_with_apples = [[] for _ in range(n)]

        for u, v, cost, taxi in roads:
            # Roads are bidirectional
            adj_empty[u].append((v, cost))
            adj_empty[v].append((u, cost))

            adj_with_apples[u].append((v, cost * taxi))
            adj_with_apples[v].append((u, cost * taxi))

        # Step 2: Dijkstra's algorithm function to find shortest paths from a source node
        def dijkstra(start_node: int, graph: List[List[tuple]]) -> List[int]:
            dist = [math.inf] * n
            dist[start_node] = 0
            # Priority queue stores (distance, node) to always process the node
            # with the smallest current distance first.
            pq = [(0, start_node)]

            while pq:
                d, u = heapq.heappop(pq)

                # If we've already found a shorter path to u, skip this one
                if d > dist[u]:
                    continue

                # Explore neighbors of u
                for v, weight in graph[u]:
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
                        heapq.heappush(pq, (dist[v], v))
            return dist

        # Step 3: Compute all-pairs shortest paths for travel empty
        # all_dist_empty[i][j] will store the minimum cost to travel from shop i to shop j empty
        all_dist_empty = []
        for i in range(n):
            all_dist_empty.append(dijkstra(i, adj_empty))

        # Step 4: Compute all-pairs shortest paths for travel with apples
        # all_dist_with_apples[j][i] will store the minimum cost to travel from shop j to shop i with apples
        all_dist_with_apples = []
        for i in range(n):
            all_dist_with_apples.append(dijkstra(i, adj_with_apples))

        # Step 5: Calculate the minimum total cost for each shop i
        ans = [0] * n
        for i in range(n):
            # Option 1: Buy locally at shop i
            min_cost_for_i = prices[i]

            # Option 2: Travel to shop j, buy there, and return
            for j in range(n):
                # Check if paths exist for both empty travel (i -> j) and full travel (j -> i)
                # If either path is unreachable (distance is infinity), this option is not viable.
                if all_dist_empty[i][j] == math.inf or all_dist_with_apples[j][i] == math.inf:
                    continue
                
                # Calculate total cost for buying at shop j and returning to i:
                # (cost to travel i->j empty) + (price at j) + (cost to travel j->i with apples)
                current_option_cost = all_dist_empty[i][j] + prices[j] + all_dist_with_apples[j][i]
                min_cost_for_i = min(min_cost_for_i, current_option_cost)
            
            ans[i] = min_cost_for_i
        
        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 2
    prices1 = [8,3]
    roads1 = [[0,1,1,2]]
    expected1 = [6,3]
    assert s.minCost(n1, prices1, roads1) == expected1, f"Test 1 Failed: Expected {expected1}, Got {s.minCost(n1, prices1, roads1)}"
    
    # Example 2
    n2 = 3
    prices2 = [9,4,6]
    roads2 = [[0,1,1,3],[1,2,4,2]]
    expected2 = [8,4,6]
    assert s.minCost(n2, prices2, roads2) == expected2, f"Test 2 Failed: Expected {expected2}, Got {s.minCost(n2, prices2, roads2)}"
    
    # Example 3
    n3 = 3
    prices3 = [10,11,1]
    roads3 = [[0,2,1,3],[1,2,3,4],[0,1,5,2]]
    expected3 = [5,11,1]
    assert s.minCost(n3, prices3, roads3) == expected3, f"Test 3 Failed: Expected {expected3}, Got {s.minCost(n3, prices3, roads3)}"
    
    # Additional Test Case: No roads
    n4 = 3
    prices4 = [10, 20, 30]
    roads4 = []
    expected4 = [10, 20, 30]
    assert s.minCost(n4, prices4, roads4) == expected4, f"Test 4 Failed: Expected {expected4}, Got {s.minCost(n4, prices4, roads4)}"
    
    # Additional Test Case: Single shop
    n5 = 1
    prices5 = [50]
    roads5 = []
    expected5 = [50]
    assert s.minCost(n5, prices5, roads5) == expected5, f"Test 5 Failed: Expected {expected5}, Got {s.minCost(n5, prices5, roads5)}"
    
    # Additional Test Case: Disconnected graph components
    # 0 --(1,2)-- 1    2 --(10,5)-- 3
    n6 = 4
    prices6 = [100, 10, 200, 30]
    roads6 = [[0,1,1,2],[2,3,10,5]]
    # Shop 0: local 100.
    # To 1: 0->1 empty (1), price[1] (10), 1->0 full (1*2=2) = 1+10+2 = 13.
    # Min for 0 is 13.
    # Shop 1: local 10.
    # To 0: 1->0 empty (1), price[0] (100), 0->1 full (1*2=2) = 1+100+2 = 103.
    # Min for 1 is 10.
    # Shop 2: local 200.
    # To 3: 2->3 empty (10), price[3] (30), 3->2 full (10*5=50) = 10+30+50 = 90.
    # Min for 2 is 90.
    # Shop 3: local 30.
    # To 2: 3->2 empty (10), price[2] (200), 2->3 full (10*5=50) = 10+200+50 = 260.
    # Min for 3 is 30.
    expected6 = [13, 10, 90, 30]
    assert s.minCost(n6, prices6, roads6) == expected6, f"Test 6 Failed: Expected {expected6}, Got {s.minCost(n6, prices6, roads6)}"

    print("All tests passed!")

