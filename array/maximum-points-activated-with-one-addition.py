"""
Maximum Points Activated with One Addition
Difficulty: Hard

Description:
This problem asks us to find the maximum number of points that can be activated by adding one new point (x, y) to an existing set of points. The activation rule is that if a point is activated, all other points sharing its x-coordinate or y-coordinate also become activated, and this process cascades. This implies a graph problem where unique x and y coordinates are nodes, and an original point (xi, yi) creates an edge between the coordinate node xi and the coordinate node yi. The activation process effectively activates all points whose x and y coordinates belong to the same connected component in this graph.

Example:
Input: points = [[1,1],[1,2],[2,2]]
Output: 4
Explanation: If we add and activate point (1, 3): (1,3) activates (1,1) and (1,2) due to shared x=1. Then (1,2) activates (2,2) due to shared y=2. Total activated points are (1,3), (1,1), (1,2), (2,2), which is 4.

Approach:
The problem can be modeled using a Disjoint Set Union (DSU) data structure. We treat each unique x-coordinate and each unique y-coordinate from the input `points` as a node in our DSU. When an original point `(x, y)` is given, it implies a connection (an edge) between coordinate `x` and coordinate `y`. We perform a `union` operation on `x` and `y`. For each component identified by its root, we maintain two pieces of information: the total number of unique coordinates (`coords`) within the component (used for union by size optimization), and the total number of original `points` (edges) within the component.

After processing all given `points`:
1.  Initialize DSU structure where `parent` maps coordinates to their parents and `comp_info` maps root coordinates to a dictionary containing `{'coords': int, 'points': int}`.
2.  Iterate through each `(x, y)` in the input `points`. For each pair, call `union(x, y)` to merge their respective components. After the union, increment the `points` count of the resulting component's root by one, representing the addition of this original point (edge).
3.  After all original points are processed, collect the `points` counts from all final roots in `comp_info`. These counts represent the number of activated points if one point from that specific component is activated.
4.  Sort these `points` counts in descending order.
5.  Determine the maximum possible activated points by considering three scenarios for adding the single new point:
    *   **Base case (1 point):** Add a point `(X, Y)` where both `X` and `Y` are new coordinates not present in the original `points`. This activates only the new point itself. The result is 1.
    *   **Scenario 1 (Largest + 1 point):** Add a point `(X, Y)` that connects to an existing component (e.g., `X` is in the largest component, `Y` is new, or vice-versa, or both `X,Y` are in the largest component). This activates all points in the largest component plus the new point itself. The result is `(largest_component_points_count + 1)`.
    *   **Scenario 2 (Two largest + 1 point):** Add a point `(X, Y)` that connects the two largest existing components (e.g., `X` is in the largest component, `Y` is in the second largest component). This activates all points in both components plus the new point itself. The result is `(largest_component_points_count + second_largest_component_points_count + 1)`.
The maximum of these possibilities is the answer.

Time Complexity: O(N log N)
    - Initializing and processing `N` points with DSU operations (find and union with path compression and union by size) takes amortized O(N * alpha(C)), where `C` is the number of unique coordinates (at most 2N) and alpha is the inverse Ackermann function, which is practically constant. So, this part is O(N).
    - Extracting component sizes is O(C).
    - Sorting the component sizes takes O(C log C). Since C is at most 2N, this dominates and leads to O(N log N).
Space Complexity: O(N)
    - DSU `parent` and `comp_info` dictionaries store information for at most `2N` unique coordinates.
    - The list of component points counts takes at most O(N) space.
"""
from typing import List, Optional

class Solution:
    def maxActivated(self, points: List[List[int]]) -> int:
        
        # DSU structure using dictionaries for coordinate values
        # self.parent: maps a coordinate (int) to its parent coordinate (int)
        # self.comp_info: maps a root coordinate (int) to a dict {'coords': int, 'points': int}
        #   'coords': number of unique x/y coordinates (nodes) in the component. Used for union by size optimization.
        #   'points': number of original points (edges) in the component. This is the value we're trying to maximize.
        self.parent = {}
        self.comp_info = {}

        def find(i: int) -> int:
            """Finds the root of the component containing coordinate i, with path compression."""
            # If 'i' is encountered for the first time, initialize its DSU entry.
            if i not in self.parent:
                self.parent[i] = i
                self.comp_info[i] = {'coords': 1, 'points': 0} # New coordinate forms a component of size 1 (1 node, 0 edges)
            
            # If 'i' is its own parent, it's the root.
            if self.parent[i] == i:
                return i
            
            # Path compression: set parent to the root of its parent.
            self.parent[i] = find(self.parent[i])
            return self.parent[i]

        def union(i: int, j: int) -> int:
            """
            Unites the components containing coordinates i and j.
            Uses union by size (number of coordinates) for optimization.
            Returns the root of the new (or existing) combined component.
            """
            root_i = find(i)
            root_j = find(j)
            
            if root_i != root_j:
                # Union by size: attach the smaller component to the larger component.
                # This keeps tree height minimal, optimizing future find operations.
                if self.comp_info[root_i]['coords'] < self.comp_info[root_j]['coords']:
                    root_i, root_j = root_j, root_i # Swap to ensure root_i is the larger component
                
                self.parent[root_j] = root_i # Make root_i the parent of root_j
                
                # Update the combined component's properties
                self.comp_info[root_i]['coords'] += self.comp_info[root_j]['coords']
                self.comp_info[root_i]['points'] += self.comp_info[root_j]['points']
                
                # Remove the merged component's info as it's no longer a root
                del self.comp_info[root_j] 
            
            return root_i # Returns the root of the component containing both i and j
        
        # Process all given points to build the initial connected components
        for x, y in points:
            root = union(x, y)
            # Each original point (x,y) acts as an edge in our coordinate graph.
            # Increment the 'points' count for the component this edge belongs to.
            self.comp_info[root]['points'] += 1 

        # Collect the 'points' count for all final root components
        # These represent the number of points activated within each component formed by existing points.
        component_points_counts = []
        for root in self.comp_info:
            if self.parent[root] == root: # Ensure we only consider actual roots of components
                component_points_counts.append(self.comp_info[root]['points'])
        
        # Sort component sizes (by points count) in descending order to easily access largest components
        component_points_counts.sort(reverse=True)
        
        # Calculate maximum activated points based on different scenarios for adding one new point:
        
        # Scenario A: Add a new point (X, Y) where X and Y are completely new coordinates.
        # This point activates only itself. So, a minimum of 1 point is always possible.
        max_activated_points = 1 
        
        # Scenario B: Add a new point (X, Y) that connects to an existing component or within it.
        # For example, X is an existing coordinate in the largest component, and Y is a new coordinate.
        # Or, both X and Y are existing coordinates in the largest component.
        # In these cases, the new point itself gets activated in addition to all points already
        # activated within that largest component.
        if component_points_counts: # If there are any existing components
            max_activated_points = max(max_activated_points, component_points_counts[0] + 1)
        
        # Scenario C: Add a new point (X, Y) such that it merges the two largest existing components.
        # For example, X is an existing coordinate in the largest component, and Y is an existing
        # coordinate in the second largest component.
        # The new point (X, Y) itself gets activated, along with all points in the two merged components.
        if len(component_points_counts) >= 2:
            max_activated_points = max(max_activated_points, component_points_counts[0] + component_points_counts[1] + 1)
            
        return max_activated_points

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    points1 = [[1,1],[1,2],[2,2]]
    assert s.maxActivated(points1) == 4, f"Test 1 Failed: Expected 4, got {s.maxActivated(points1)}"

    # Example 2
    points2 = [[2,2],[1,1],[3,3]]
    assert s.maxActivated(points2) == 3, f"Test 2 Failed: Expected 3, got {s.maxActivated(points2)}"

    # Example 3
    points3 = [[2,3],[2,2],[1,1],[4,5]]
    assert s.maxActivated(points3) == 4, f"Test 3 Failed: Expected 4, got {s.maxActivated(points3)}"
    
    # Custom Test 1: Empty points list
    points_empty = []
    assert s.maxActivated(points_empty) == 1, f"Test Empty Failed: Expected 1, got {s.maxActivated(points_empty)}"

    # Custom Test 2: Single point
    points_single = [[10,20]]
    assert s.maxActivated(points_single) == 2, f"Test Single Failed: Expected 2, got {s.maxActivated(points_single)}"

    # Custom Test 3: Two disconnected components, each with 1 point
    points_two_disconnected_1 = [[1,1],[2,2]]
    assert s.maxActivated(points_two_disconnected_1) == 3, f"Test Two Disconnected 1 Failed: Expected 3, got {s.maxActivated(points_two_disconnected_1)}"

    # Custom Test 4: Two disconnected components, larger one with 2 points
    points_two_disconnected_2 = [[1,1],[1,2],[3,3]]
    # Comp1: (1,1), (1,2) -> {coords: 2, points: 2} (root=1, containing coords {1,2})
    # Comp2: (3,3) -> {coords: 1, points: 1} (root=3, containing coords {3})
    # Sorted points counts: [2, 1]
    # Max: max(1, 2+1, 2+1+1) = max(1, 3, 4) = 4
    assert s.maxActivated(points_two_disconnected_2) == 4, f"Test Two Disconnected 2 Failed: Expected 4, got {s.maxActivated(points_two_disconnected_2)}"

    # Custom Test 5: All points on one line (e.g., same x-coord)
    points_line_x = [[1,1],[1,2],[1,3],[1,4]]
    # All merge into one component. Root 1, points=4
    # Max: max(1, 4+1) = 5
    assert s.maxActivated(points_line_x) == 5, f"Test Line X Failed: Expected 5, got {s.maxActivated(points_line_x)}"

    # Custom Test 6: Larger coordinates
    points_large_coords = [[1000000000, 1],[1, 1000000000]]
    # (1e9, 1): union(1e9, 1). Comp with root 1e9, points=1
    # (1, 1e9): union(1, 1e9). Finds 1 and 1e9 already in the same component. Root 1e9, points=2
    # One component with 2 points.
    # Max: max(1, 2+1) = 3
    assert s.maxActivated(points_large_coords) == 3, f"Test Large Coords Failed: Expected 3, got {s.maxActivated(points_large_coords)}"


    print("All tests passed!")

