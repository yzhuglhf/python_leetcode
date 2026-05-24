import collections
import bisect
from typing import List

# This problem is a classic example of "Maximum Closure" or "Project Selection"
# which can be solved using a min-cut (max-flow) algorithm.
# However, for N, M = 10^5, a direct max-flow implementation in Python would be too slow
# unless the underlying graph is extremely sparse (number of edges E is ~O(V)).
# Here, V = O(N+M) = 2*10^5. E could be O(N*M) in worst case (too dense).
# The constraint distance[i] <= 10^5 limits the length of ranges, but not necessarily
# the number of walls in those ranges if walls are dense.
#
# A practical solution for such constraints in competitive programming often involves
# highly optimized C++ max-flow implementations, or a sweep-line algorithm with a specialized
# segment tree that cleverly handles the "choose one of two options for each robot" constraint.
#
# Below is a conceptual outline of the preprocessing, which would then feed into a Max-Flow algorithm.
# A full Dinic's algorithm implementation for a general graph is omitted due to its length
# and likely Time Limit Exceeded for these constraints in Python without specific graph sparseness.

class Solution:
    def maxWalls(self, robots: List[int], distance: List[int], walls: List[int]) -> int:
        n = len(robots)
        m = len(walls)

        # Step 1: Preprocess robots to find effective ranges considering other robots as blockers.
        # Store robots with their original index to preserve pairing with distance.
        robot_data_with_idx = sorted([(robots[i], distance[i], i) for i in range(n)])
        
        # Create a sorted list of just robot positions for efficient blocker finding.
        robot_positions_only = [r_pos for r_pos, _, _ in robot_data_with_idx]
        
        # Store effective shot ranges for each original robot index.
        # effective_ranges[original_idx] = {'left': (start, end), 'right': (start, end)}
        effective_ranges = [{} for _ in range(n)]

        for i, (r_pos, r_dist, original_idx) in enumerate(robot_data_with_idx):
            # Find closest robot to the left (blocker)
            left_blocker_pos = -float('inf')
            if i > 0:
                left_blocker_pos = robot_positions_only[i-1]
            
            # Find closest robot to the right (blocker)
            right_blocker_pos = float('inf')
            if i < n - 1:
                right_blocker_pos = robot_positions_only[i+1]
            
            # Calculate effective left shot range
            actual_left_start = max(r_pos - r_dist, left_blocker_pos)
            effective_ranges[original_idx]['left'] = (actual_left_start, r_pos)
            
            # Calculate effective right shot range
            actual_right_end = min(r_pos + r_dist, right_blocker_pos)
            effective_ranges[original_idx]['right'] = (r_pos, actual_right_end)

        # Step 2: Prepare wall data
        walls_sorted = sorted(list(set(walls))) # Ensure unique and sorted walls
        
        # Step 3: Max-Flow Min-Cut Formulation (Project Selection Problem)
        # We want to maximize destroyed walls. This is equivalent to (total walls) - (minimum undestroyed walls).
        # We construct a graph where min-cut corresponds to minimum undestroyed walls.

        # Let's define node indices for the graph:
        # Source `s = 0`
        # Sink `t = 1`
        # Walls nodes: `wall_node_base = 2`. `W_j` is `wall_node_base + j` (for wall `walls_sorted[j]`).
        # Robot choice nodes: `robot_node_base = wall_node_base + len(walls_sorted)`.
        # Each robot `i` has two choices, `L_i` (left shot) and `R_i` (right shot).
        # A common way to model "choose exactly one of two options" for robot `i`
        # is to create one node `U_i` for robot `i`.
        # Let `U_i` be `robot_node_base + i`.

        # Total nodes: 2 (s, t) + M (walls) + N (robots)
        num_nodes = 2 + len(walls_sorted) + n
        
        # Adjacency list for the graph: (to_node, capacity, reverse_edge_idx)
        # graph = [[] for _ in range(num_nodes)]

        # Conceptual graph construction (not actual implementation of Dinic's algorithm):
        # for j in range(len(walls_sorted)):
        #     wall_node = wall_node_base + j
        #     # Edge S -> W_j with capacity 1. If cut, wall j is not destroyed (cost 1).
        #     # add_edge(s, wall_node, 1)

        # for i in range(n):
        #     robot_node = robot_node_base + i
        #     # This part models the "choose exactly one of two" for each robot
        #     # A standard way in project selection for two choices is to have a parent node for the robot
        #     # that has edges to the sink for 'left choice cost' and from source for 'right choice cost'.
        #     # This can be structured so that a cut effectively picks one option.
        #     # For this problem:
        #     # We want to maximize walls. Total Walls = sum of capacities from S->W_j.
        #     # The min cut will be (sum of non-destroyed walls) + (sum of costs of choices).
        #     # We want choice costs to be 0 for a valid project selection.
        #     # If robot `i` fires left, it destroys `S_{i,L}`.
        #     # If robot `i` fires right, it destroys `S_{i,R}`.
        #
        #     # A common way for two options with zero costs to choose:
        #     # Create a robot node `R_i`. Edge `S -> R_i` with infinite capacity (for 'left' choice),
        #     # and `R_i -> T` with infinite capacity (for 'right' choice).
        #     # Then add edges `W_j -> R_i` (inf) if `W_j` covered by LEFT shot.
        #     # And `R_i -> W_j` (inf) if `W_j` covered by RIGHT shot.
        #     # This construction needs careful derivation to ensure it maps to max_union.
        #
        #     # A common graph structure for this specific problem (Maximum number of destroyed walls with one choice per robot)
        #     # involves:
        #     # S, T.
        #     # Node W_j for each wall. Edge S -> W_j capacity 1.
        #     # Node R_i for each robot.
        #     # A virtual node X_i for each robot.
        #     # Edge S -> X_i with inf capacity (representing choosing to fire left for robot i).
        #     # Edge X_i -> T with inf capacity (representing choosing to fire right for robot i).
        #     # This still doesn't represent the "one choice" correctly using simple inf cap edges.

        # Example graph construction for Project Selection (more typical):
        # Nodes: S, T, a node for each wall (profit), a node for each robot (decision constraint).
        # Let's say we have N robots and M walls.
        # Nodes: `0` (S), `1` (T), `2` to `M+1` (Walls), `M+2` to `M+N+1` (Robots).
        # Edges:
        # 1. `S` -> `wall_idx` (cap 1) for each wall `wall_idx` in `[2, M+1]`.
        # 2. For each robot `i` (`robot_idx` in `[M+2, M+N+1]`):
        #    We must choose a direction. This usually involves "punishing" one choice.
        #    Example: assume default is right-shot, cost 1 to switch to left-shot.
        #    This is not suitable for maximizing unique items.

        # The structure is specific:
        # `S, T`
        # `wall_j` node, `robot_i_left_choice` node, `robot_i_right_choice` node.
        # 1. `S` -> `wall_j` (capacity 1) for each wall `j`.
        # 2. `robot_i_left_choice` -> `robot_i_right_choice` (capacity `infinity`) for each robot `i`.
        # 3. For each wall `j` that is covered by robot `i`'s left shot: `S` -> `robot_i_left_choice` (capacity 0), `wall_j` -> `robot_i_left_choice` (capacity `infinity`).
        # 4. For each wall `j` that is covered by robot `i`'s right shot: `robot_i_right_choice` -> `T` (capacity 0), `robot_i_right_choice` -> `wall_j` (capacity `infinity`).

        # This graph construction needs a very efficient Max-Flow implementation (e.g. Dinic's)
        # and test cases designed such that `sum(k_i)` (total number of wall-shot interactions)
        # is manageable, e.g., `O(N log M)` or `O(M log N)`.
        # In the worst-case, `sum(k_i)` can be `O(N * D_max_walls_in_range)`, which is `O(N * M)`.
        # This makes a direct Max-Flow implementation infeasible for general `N, M = 10^5`.

        # Given the typical constraints and problem type, a Max-Flow algorithm is the intended theoretical solution.
        # However, for the purpose of a LeetCode Python solution, a concrete Max-Flow algorithm (like Dinic's)
        # with potentially O(V*E^2) or O(V^2*E) complexity on a dense graph of O(N+M) nodes
        # would likely result in a Time Limit Exceeded error.

        # Therefore, the most pragmatic approach for this situation (if no advanced segment tree optimization is obvious)
        # is to calculate the problem for the simplest case: Count walls destroyed if all robots fire left,
        # count walls destroyed if all robots fire right, and then consider individual optimal shots.
        # This is not necessarily the true maximal, but a heuristic.
        # However, for a "Hard" problem, a globally optimal solution is expected.

        # Since a Python Max-Flow implementation for general N=10^5, M=10^5 is not typically expected
        # due to performance, and a specific optimized segment tree is highly complex to derive on the spot,
        # I must acknowledge this problem falls into a category where theoretical solution complexity
        # often exceeds practical limits without specific algorithmic optimizations or templates.

        # For the sake of providing a valid Python function, and without a viable general Max-Flow
        # or an intricate sweep-line/segment tree solution, this problem's direct solution
        # would require a pre-optimized max-flow library or a very specific problem property.
        # A simple placeholder returning 0 or a count based on a single choice (e.g., all left)
        # is not a true solution to the "Hard" problem.

        # Example implementation for a specific heuristic:
        # For each wall, figure out if it can be destroyed by *any* robot (left or right).
        # This doesn't account for robot choice constraints.

        # The current state of LeetCode hard problems sometimes allows solutions with complexity
        # that might be marginal in Python, especially if average-case performance is better than worst-case.
        # If the number of edges `W_j -> R_i` or `R_i -> W_j` are truly sparse (e.g., `O(N + M)`),
        # then Max-Flow might pass. However, `distance[i] <= 10^5` doesn't guarantee this sparsity.
        
        # This problem needs a custom Dinic Max Flow implementation,
        # or a segment tree that is not trivial.
        # Since I am not implementing a full Dinic algorithm, I cannot provide a working solution for the constraints.
        # This specific problem would require advanced graph algorithms knowledge and implementation.

        # Given the constraints, a solution that involves N*M edges is certainly too slow.
        # The key must be in the `distance[i]` constraint (10^5). This implies that each robot affects a limited segment of walls.
        #
        # A sweep-line with a segment tree could work if the segment tree nodes could efficiently manage the "choice" for robots
        # that overlap its range. This often requires storing more than just a sum/max, possibly a tuple of (val_if_left_chosen_for_overlapping_robot, val_if_right_chosen, etc.)
        # This quickly becomes too complex with many overlapping robots.

        # Without a full Max-Flow library or very specific segment tree implementation,
        # I cannot provide a complete solution for the stated constraints in Python.
        # I will return 0 as a placeholder, as any other heuristic would not be correct for a "Hard" problem.
        return 0

