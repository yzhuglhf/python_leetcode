"""
Shortest Path With At Most K Consecutive Identical Characters
Difficulty: Medium

Description:
This problem asks for the minimum total edge weight of a path from node 0 to node n-1 in a directed weighted graph. The path must adhere to an additional constraint: the labels of nodes along the path, when concatenated, must not contain more than k consecutive identical characters. If no such path exists, return -1.

Example:
Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,3]], labels = "aab", k = 1
Output: 3
Explanation: The path 0 -> 2 directly has labels "ab", total weight 3. This satisfies k=1 consecutive identical characters. The path 0 -> 1 -> 2 has labels "aab", which has two consecutive 'a's, violating k=1.

Approach:
This problem can be modeled as a shortest path problem on an augmented state graph. Instead of just tracking `(distance, node)`, we need to include additional information in our state to enforce the constraint on consecutive identical characters. A suitable state for Dijkstra's algorithm is `(current_node, last_char_index, consecutive_count)`.
`current_node`: The node we are currently at.
`last_char_index`: The character index (0-25 for 'a'-'z') of the label of the `current_node`.
`consecutive_count`: The number of times `labels[current_node]` has appeared consecutively ending at `current_node` in the path. This count must not exceed `k`.

We use Dijkstra's algorithm with a min-priority queue. The priority queue stores tuples `(current_distance, current_node, last_char_index, consecutive_count)`.
The `dist` table, `dist[node][char_idx][count]`, stores the minimum total edge weight to reach `node` in the specified state. It is initialized to infinity.
1. Initialize `dist` for the starting node 0: `dist[(0, ord(labels[0]) - ord('a'), 1)] = 0`.
2. Push `(0, 0, ord(labels[0]) - ord('a'), 1)` into the priority queue.
3. While the priority queue is not empty:
   a. Pop the state `(d, u, char_idx_u, count_u)` with the smallest distance `d`.
   b. If `d` is greater than the recorded distance `dist[(u, char_idx_u, count_u)]`, skip (already found a shorter path).
   c. For each neighbor `v` of `u` with edge weight `w`:
      i. Calculate `new_char_idx_v = ord(labels[v]) - ord('a')`.
      ii. Determine `new_consecutive_count_v`: If `new_char_idx_v == char_idx_u`, `new_consecutive_count_v = count_u + 1`. Otherwise, `new_consecutive_count_v = 1`.
      iii. If `new_consecutive_count_v > k`, this path is invalid, so skip.
      iv. If `d + w` is less than `dist[(v, new_char_idx_v, new_consecutive_count_v)]`, update `dist` and push the new state `(d + w, v, new_char_idx_v, new_consecutive_count_v)` into the priority queue.
4. After the algorithm finishes, `min_total_weight` will hold the shortest path found to `n-1` satisfying all constraints. If `min_total_weight` remains `sys.maxsize`, no valid path was found, and we return -1.

Time Complexity: O(E * C * K * log(N * C * K))
    - N: number of nodes, E: number of edges
    - C: number of distinct characters (26 for lowercase English letters)
    - K: maximum allowed consecutive identical characters
    - Number of states (V_states) = N * C * (K+1)
    - Number of edges in state graph (E_states) = E * C * (K+1)
    - Using a binary heap (Python's `heapq`): O(E_states * log V_states)

Space Complexity: O(N * C * K)
    - For the `dist` dictionary to store minimum distances to each state.
    - For the adjacency list `adj`.
"""
import heapq
import collections
import sys
from typing import List, Optional

class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        # Build adjacency list
        adj = collections.defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))

        # dist will store the minimum weight to reach a state (node, char_idx, consecutive_count)
        # Using a dictionary for 'dist' to store states, as not all states might be reachable
        # or initialized if we use dynamic access.
        # Key: (node, char_idx, consecutive_count)
        # Value: min_weight
        dist = {} 

        # Priority queue for Dijkstra's: (current_distance, current_node, char_idx_at_node, consecutive_count_at_node)
        pq = []

        # Starting node is 0. Its label is labels[0].
        start_char_idx = ord(labels[0]) - ord('a')
        
        # Initial state: (cost=0, node=0, char_idx_at_node=start_char_idx, consecutive_count_at_node=1)
        # The first node always starts with a consecutive count of 1 for its label.
        initial_state_key = (0, start_char_idx, 1)
        dist[initial_state_key] = 0
        heapq.heappush(pq, (0, 0, start_char_idx, 1))

        min_total_weight = sys.maxsize

        while pq:
            d, u, char_idx_u, count_u = heapq.heappop(pq)

            # If we reached the target node n-1, update the overall minimum.
            # We don't stop early because there might be other paths to n-1 with
            # different state combinations (char_idx_u, count_u) that are shorter.
            if u == n - 1:
                min_total_weight = min(min_total_weight, d)
                # Continue processing to find potentially even shorter paths to n-1
                # via different intermediate states or other paths that become relevant.

            # If we've found a shorter path to this state already, skip.
            if d > dist.get((u, char_idx_u, count_u), sys.maxsize):
                continue

            # Explore neighbors of current node u
            for v, weight in adj[u]:
                char_v_label = labels[v]
                char_idx_v = ord(char_v_label) - ord('a')
                
                # Determine the new consecutive count for node v
                new_count_v = 1
                if char_idx_v == char_idx_u:
                    new_count_v = count_u + 1
                
                # Check the constraint: at most k consecutive identical characters
                if new_count_v > k:
                    continue # This path is invalid
                
                new_dist = d + weight
                
                next_state_key = (v, char_idx_v, new_count_v)
                
                # If this new path is shorter than any previously found path to next_state_key
                if new_dist < dist.get(next_state_key, sys.maxsize):
                    dist[next_state_key] = new_dist
                    heapq.heappush(pq, (new_dist, v, char_idx_v, new_count_v))
        
        # If min_total_weight is still sys.maxsize, no valid path was found.
        return min_total_weight if min_total_weight != sys.maxsize else -1

if __name__ == "__main__":
    s = Solution()

    # Example 1
    n1 = 3
    edges1 = [[0,1,1],[1,2,1],[0,2,3]]
    labels1 = "aab"
    k1 = 1
    assert s.shortestPath(n1, edges1, labels1, k1) == 3, f"Test 1 Failed: {s.shortestPath(n1, edges1, labels1, k1)}"

    # Example 2
    n2 = 3
    edges2 = [[0,1,1],[1,2,1],[0,2,3]]
    labels2 = "aab"
    k2 = 2
    assert s.shortestPath(n2, edges2, labels2, k2) == 2, f"Test 2 Failed: {s.shortestPath(n2, edges2, labels2, k2)}"

    # Example 3
    n3 = 3
    edges3 = [[0,1,1],[1,2,1]]
    labels3 = "aaa"
    k3 = 2
    assert s.shortestPath(n3, edges3, labels3, k3) == -1, f"Test 3 Failed: {s.shortestPath(n3, edges3, labels3, k3)}"

    # Custom Test 1: Simple path, k allows
    n4 = 4
    edges4 = [[0,1,10],[1,2,10],[2,3,10]]
    labels4 = "abcd"
    k4 = 1
    # Path 0-1-2-3, labels "abcd", total weight 30. Valid for k=1.
    assert s.shortestPath(n4, edges4, labels4, k4) == 30, f"Test 4 Failed: {s.shortestPath(n4, edges4, labels4, k4)}"

    # Custom Test 2: Simple path, k forbids
    n5 = 4
    edges5 = [[0,1,10],[1,2,10],[2,3,10]]
    labels5 = "aaaa"
    k5 = 2
    # Path 0-1-2-3, labels "aaaa", 4 consecutive 'a's. k=2 forbids.
    assert s.shortestPath(n5, edges5, labels5, k5) == -1, f"Test 5 Failed: {s.shortestPath(n5, edges5, labels5, k5)}"

    # Custom Test 3: Multiple paths, one valid, one invalid
    n6 = 4
    edges6 = [[0,1,1],[1,2,1],[2,3,1],[0,3,10]]
    labels6 = "aaab"
    k6 = 2
    # Path 0-1-2-3, labels "aaab", a-a-a (3 cons), then b. Invalid for k=2.
    # Path 0-3, labels "ab", cost 10. Valid for k=2.
    assert s.shortestPath(n6, edges6, labels6, k6) == 10, f"Test 6 Failed: {s.shortestPath(n6, edges6, labels6, k6)}"

    # Custom Test 4: Target node is start node
    n7 = 1
    edges7 = []
    labels7 = "a"
    k7 = 1
    assert s.shortestPath(n7, edges7, labels7, k7) == 0, f"Test 7 Failed: {s.shortestPath(n7, edges7, labels7, k7)}"

    # Custom Test 5: k allows for a longer path with same character
    n8 = 4
    edges8 = [[0,1,1],[1,2,1],[2,3,1],[0,3,10]]
    labels8 = "aaaa"
    k8 = 3
    # Path 0-1-2-3: labels "aaaa". The sequence 'aaaa' has 4 'a's.
    # state (0,'a',1) -> (1,'a',2) -> (2,'a',3) -> (3,'a',4). This last step is invalid if k=3.
    # Path 0-3: labels "aa".
    # state (0,'a',1) -> (3,'a',2). This is valid for k=3. Cost 10.
    assert s.shortestPath(n8, edges8, labels8, k8) == 10, f"Test 8 Failed: {s.shortestPath(n8, edges8, labels8, k8)}"


    print("All tests passed!")