"""
Minimum Cost Path with Alternating Directions III
Difficulty: Hard

Description:
This problem asks for the minimum cost to reach a target cell (m-1, n-1) in a grid, starting from (0,0). The cost calculation involves an initial entry cost, subsequent cell entry costs, and penalties for violating alternating move directions or waiting. Moves alternate between odd-numbered actions (right/down) and even-numbered actions (left/up), with penalties applied for non-compliant moves or waiting.

Example:
Input: m = 2, n = 2, penalty = [[5,3],[1,4]]
Output: 8
Explanation: The optimal path involves starting at (0,0) (cost 1), moving down to (1,0) (cost 2, odd-compliant), then moving right to (1,1) (cost 4 + penalty[1][0]=1 for even-parity violation). Total cost: 1 + 2 + 4 + 1 = 8.

Approach:
This problem can be modeled as a shortest path problem on a graph, where each node represents a cell (r, c) and the parity of the next action to be taken. Specifically, a state can be defined as `(r, c, next_action_parity)`, where `r` and `c` are row and column indices, and `next_action_parity` indicates whether the *next* action will be odd-numbered (1) or even-numbered (0). We use Dijkstra's algorithm to find the minimum cost.

The `dist[r][c][parity]` array stores the minimum cost to reach cell `(r, c)` such that the next action to be taken has `parity`. Initially, `dist[0][0][1]` is set to `(0+1)*(0+1)` because after the initial entry cost, the first action (action #1) is odd. A priority queue stores `(cost, r, c, next_action_parity)` tuples. In each step, we extract the state with the minimum cost from the priority queue and explore possible transitions:
1.  **Waiting:** Stay at `(r, c)`. Pay `penalty[r][c]`. The `next_action_parity` flips (e.g., if the current action was odd, the next action becomes even).
2.  **Moving:** Move to an adjacent cell `(nr, nc)`. Pay the destination's entrance cost `(nr+1)*(nc+1)`. If the move direction violates the current `next_action_parity` rule (e.g., moving left when the next action should be odd), an additional `penalty[r][c]` is paid, where `(r, c)` is the cell you move from. The `next_action_parity` always flips after any move.

We update `dist` values and push new states to the priority queue if a shorter path is found. The algorithm terminates when the priority queue is empty. The final answer is the minimum of `dist[m-1][n-1][0]` and `dist[m-1][n-1][1]`, representing the minimum cost to reach the target cell regardless of what the parity of the subsequent action would be.

Time Complexity: O(M * N * log(M * N))
There are `M * N * 2` possible states. Each state is pushed and popped from the priority queue at most once. For each state, we consider up to 5 transitions (wait, move right, left, up, down). Each heap operation takes `O(log(number_of_states))`. Thus, the total time complexity is `O(number_of_states * number_of_transitions_per_state * log(number_of_states)) = O(M * N * 5 * log(M * N * 2))`, which simplifies to `O(M * N * log(M * N))`. Given `M * N <= 10^5`, this is efficient enough.

Space Complexity: O(M * N)
The `dist` array stores `M * N * 2` integer values. The priority queue can store up to `M * N * 2` states in the worst case. Both contribute `O(M * N)` space.
"""
import heapq
from typing import List, Optional

class Solution:
    def minCost(self, m: int, n: int, penalty: List[List[int]]) -> int:
        # dist[r][c][parity] stores the minimum cost to reach cell (r, c)
        # such that the NEXT action to be taken has the given parity.
        # parity = 1 means next action is odd-numbered (Action #1, #3, etc.)
        # parity = 0 means next action is even-numbered (Action #2, #4, etc.)
        
        # Initialize distances with infinity
        dist = [[[float('inf')] * 2 for _ in range(n)] for _ in range(m)]

        # Priority queue stores tuples: (current_total_cost, r, c, next_action_parity)
        # It will always extract the state with the minimum current_total_cost.
        pq = []

        # Starting at (0, 0). Initial entrance cost is (0+1)*(0+1) = 1.
        # After this initial entry, the first 'action' (Action #1) will be taken.
        # Action #1 is odd, so next_action_parity = 1.
        initial_cost = (0 + 1) * (0 + 1)
        dist[0][0][1] = initial_cost
        heapq.heappush(pq, (initial_cost, 0, 0, 1))

        # Directions for moves: Right, Left, Down, Up
        # These correspond to move_type_idx 0, 1, 2, 3 respectively.
        moves = [(0, 1),   # 0: Right (dr, dc)
                 (0, -1),  # 1: Left
                 (1, 0),   # 2: Down
                 (-1, 0)]  # 3: Up

        # Define rule-compliant moves based on the next_action_parity.
        # If next action is odd (parity = 1), compliant moves are Right (index 0) or Down (index 2).
        odd_compliant_moves_idx = {0, 2}
        # If next action is even (parity = 0), compliant moves are Left (index 1) or Up (index 3).
        even_compliant_moves_idx = {1, 3}

        while pq:
            current_cost, r, c, next_action_parity = heapq.heappop(pq)

            # If we've already found a shorter path to this state, skip it.
            if current_cost > dist[r][c][next_action_parity]:
                continue

            # --- Option 1: Wait in current cell (r, c) ---
            # Cost of waiting: penalty[r][c]
            wait_penalty = penalty[r][c]
            new_cost_wait = current_cost + wait_penalty
            
            # Parity always flips after any action (wait or move).
            new_next_action_parity_wait = 1 - next_action_parity 

            if new_cost_wait < dist[r][c][new_next_action_parity_wait]:
                dist[r][c][new_next_action_parity_wait] = new_cost_wait
                heapq.heappush(pq, (new_cost_wait, r, c, new_next_action_parity_wait))

            # --- Option 2: Move to an adjacent cell ---
            for move_type_idx, (dr, dc) in enumerate(moves):
                nr, nc = r + dr, c + dc

                # Check boundary conditions
                if 0 <= nr < m and 0 <= nc < n:
                    # Cost to enter the destination cell (nr, nc)
                    destination_entrance_cost = (nr + 1) * (nc + 1)
                    action_cost = destination_entrance_cost
                    
                    # Determine if the move is rule-compliant
                    is_rule_compliant = False
                    if next_action_parity == 1: # Next action is odd-numbered
                        if move_type_idx in odd_compliant_moves_idx:
                            is_rule_compliant = True
                    else: # Next action is even-numbered
                        if move_type_idx in even_compliant_moves_idx:
                            is_rule_compliant = True
                    
                    # If the move violates the parity rule, add penalty[r][c]
                    # The penalty is paid from the cell you move FROM.
                    if not is_rule_compliant:
                        action_cost += penalty[r][c] 

                    new_cost_move = current_cost + action_cost
                    # Parity always flips after any action (wait or move).
                    new_next_action_parity_move = 1 - next_action_parity 

                    if new_cost_move < dist[nr][nc][new_next_action_parity_move]:
                        dist[nr][nc][new_next_action_parity_move] = new_cost_move
                        heapq.heappush(pq, (new_cost_move, nr, nc, new_next_action_parity_move))
        
        # The final answer is the minimum cost to reach (m-1, n-1)
        # This can be achieved with the next action being either odd or even.
        return min(dist[m-1][n-1][0], dist[m-1][n-1][1])

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    m1, n1 = 2, 2
    penalty1 = [[5,3],[1,4]]
    assert s.minCost(m1, n1, penalty1) == 8, f"Test Case 1 Failed: Expected 8, Got {s.minCost(m1, n1, penalty1)}"
    
    # Example 2
    m2, n2 = 2, 2
    penalty2 = [[0,7],[3,2]]
    assert s.minCost(m2, n2, penalty2) == 7, f"Test Case 2 Failed: Expected 7, Got {s.minCost(m2, n2, penalty2)}"
    
    # Example 3
    m3, n3 = 2, 3
    penalty3 = [[8,0,9],[7,4,1]]
    assert s.minCost(m3, n3, penalty3) == 12, f"Test Case 3 Failed: Expected 12, Got {s.minCost(m3, n3, penalty3)}"

    # Custom Test Case 1: Simple 1x2 grid, direct compliant move
    m4, n4 = 1, 2
    penalty4 = [[10, 20]]
    # Path: (0,0) init cost 1. Action 1 (odd): Move Right to (0,1). Compliant. Dest cost (0+1)*(1+1)=2. Total: 1+2=3.
    assert s.minCost(m4, n4, penalty4) == 3, f"Test Case 4 Failed: Expected 3, Got {s.minCost(m4, n4, penalty4)}"

    # Custom Test Case 2: Simple 1x2 grid, wait then move (penalty[0][0]=0 makes wait free, but move becomes non-compliant)
    m5, n5 = 1, 2
    penalty5 = [[0, 20]] 
    # Path: (0,0) init cost 1. Action 1 (odd): Wait at (0,0). Cost penalty[0][0]=0. Total: 1+0=1. Next is Action 2 (even).
    # Action 2 (even): Move Right to (0,1). Violates even rule. Dest cost 2 + penalty[0][0]=0. Total: 1+2+0=3.
    assert s.minCost(m5, n5, penalty5) == 3, f"Test Case 5 Failed: Expected 3, Got {s.minCost(m5, n5, penalty5)}"

    # Custom Test Case 3: 3x3 grid with all penalty 1, for a deeper trace. Result should be 18.
    m6, n6 = 3, 3
    penalty6 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert s.minCost(m6, n6, penalty6) == 18, f"Test Case 6 Failed: Expected 18, Got {s.minCost(m6, n6, penalty6)}"

    print("All tests passed!")

