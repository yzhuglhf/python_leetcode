"""
Minimum Generations to Target Point
Difficulty: Medium

Description:
This problem asks for the minimum number of generations required to produce a target 3D point. Generation 0 starts with given initial points. Subsequent generations (k >= 1) are formed by taking all distinct pairs of points accumulated from generations 0 through k-1, computing their component-wise average using floor division, and collecting the unique new points. The goal is to find the smallest generation 'k' where the target point first appears.

Example:
Input: points = [[0,0,0],[5,5,5]], target = [1,1,1]
Output: 2
Explanation: Gen 0 has (0,0,0) and (5,5,5). Gen 1 generates (2,2,2) from (0,0,0) and (5,5,5). Gen 2 generates (1,1,1) from (0,0,0) and (2,2,2).

Approach:
The key constraint is that all coordinate values (x, y, z) are between 0 and 6. This means the total number of unique possible points in 3D space is very small (7 * 7 * 7 = 343). This finite and small state space allows for a Breadth-First Search (BFS)-like approach to find the minimum number of generations.
We maintain a set `all_known_points` containing all unique points generated up to the current generation.
1. Initialize `all_known_points` with the given `points` and check if the `target` is already present (Generation 0).
2. If `target` is not found and there are fewer than two initial points, no new points can be generated, so return -1.
3. In a loop representing generations `k = 1, 2, ...`:
    a. Create a `newly_generated_points` set for points specific to this generation.
    b. Iterate through all distinct pairs of points `(p1, p2)` from `all_known_points`.
    c. For each pair, calculate `c = [floor((x1 + x2) / 2), floor((y1 + y2) / 2), floor((z1 + z2) / 2)]`.
    d. If `c` is a new point (not in `all_known_points`), add it to `newly_generated_points`.
    e. If `newly_generated_points` is empty after checking all pairs, it means no further progress is possible, and the target cannot be reached; return -1.
    f. Add all `newly_generated_points` to `all_known_points`.
    g. Check if `target` is in `newly_generated_points`. If yes, return the current generation `k`.

Time Complexity: O(P_max^3), where P_max is the maximum number of unique points possible (7^3 = 343). The outer loop runs at most P_max times, and in each iteration, we might iterate through O(P_max^2) pairs, with O(1) set operations.
Space Complexity: O(P_max), for storing all known unique points.
"""
import itertools
from typing import List, Optional

class Solution:
    def minGenerations(self, points: List[List[int]], target: List[int]) -> int:
        
        # Convert initial points and target to tuples for efficient set operations
        # and to handle them as immutable hashable objects.
        all_known_points = set(tuple(p) for p in points)
        target_tuple = tuple(target)
        
        # Generation 0 check: If the target is already among the initial points.
        if target_tuple in all_known_points:
            return 0
        
        # If there are fewer than 2 initial points, no new points can ever be generated.
        # Since target was not found in generation 0, it's impossible.
        if len(all_known_points) < 2:
            return -1
            
        generation = 0
        
        # BFS-like loop for generations. Each iteration represents one generation (k).
        while True:
            generation += 1
            newly_generated_points = set()
            
            # Iterate over all distinct pairs of points currently known (from gen 0 to k-1).
            # itertools.combinations(set, 2) automatically handles selecting distinct elements.
            # A point cannot be paired with itself, and pairing points with identical coordinates
            # is implicitly prevented by storing points in a set.
            for p1_tuple, p2_tuple in itertools.combinations(all_known_points, 2):
                x1, y1, z1 = p1_tuple
                x2, y2, z2 = p2_tuple
                
                # Compute the new point 'c' using floor division (// in Python).
                new_x = (x1 + x2) // 2
                new_y = (y1 + y2) // 2
                new_z = (z1 + z2) // 2
                
                new_point = (new_x, new_y, new_z)
                
                # If this new point has not been seen before, add it to the current generation's new points.
                if new_point not in all_known_points:
                    newly_generated_points.add(new_point)
            
            # If no new unique points were generated in this generation, 
            # we can't progress further. If the target hasn't been found, it's impossible.
            if not newly_generated_points:
                return -1
            
            # Add all newly generated points to our collection of all known points.
            all_known_points.update(newly_generated_points)
            
            # Check if the target is among the points *newly generated* in this generation.
            # This logic ensures we find the *smallest* k for which target appears *in* generation k,
            # meaning it wasn't available in generations 0 through k-1.
            if target_tuple in newly_generated_points:
                return generation
            

if __name__ == "__main__":
    s = Solution()

    # Example 1
    points1 = [[0,0,0],[6,6,6]]
    target1 = [3,3,3]
    assert s.minGenerations(points1, target1) == 1, f"Test Case 1 Failed: Expected 1, Got {s.minGenerations(points1, target1)}"

    # Example 2
    points2 = [[0,0,0],[5,5,5]]
    target2 = [1,1,1]
    assert s.minGenerations(points2, target2) == 2, f"Test Case 2 Failed: Expected 2, Got {s.minGenerations(points2, target2)}"

    # Example 3
    points3 = [[0,0,0],[2,2,2],[3,3,3]]
    target3 = [2,2,2]
    assert s.minGenerations(points3, target3) == 0, f"Test Case 3 Failed: Expected 0, Got {s.minGenerations(points3, target3)}"

    # Example 4
    points4 = [[1,2,3]]
    target4 = [5,5,5]
    assert s.minGenerations(points4, target4) == -1, f"Test Case 4 Failed: Expected -1, Got {s.minGenerations(points4, target4)}"

    # Custom Test Case: Target unreachable after max points
    points5 = [[0,0,0],[0,0,1]]
    target5 = [6,6,6] # A point far away, probably unreachable with these limited starting points
    # Let's manually trace:
    # Gen 0: {(0,0,0), (0,0,1)}
    # Gen 1: (0,0,0) (0,0,1) -> (0,0,0)
    # No new points generated. Should return -1.
    assert s.minGenerations(points5, target5) == -1, f"Test Case 5 Failed: Expected -1, Got {s.minGenerations(points5, target5)}"
    
    # Custom Test Case: More points, target reachable
    points6 = [[0,0,0],[6,0,0],[0,6,0],[0,0,6]]
    target6 = [1,1,1]
    # Gen 0: {(0,0,0), (6,0,0), (0,6,0), (0,0,6)}
    # Gen 1:
    # (0,0,0), (6,0,0) -> (3,0,0)
    # (0,0,0), (0,6,0) -> (0,3,0)
    # (0,0,0), (0,0,6) -> (0,0,3)
    # (6,0,0), (0,6,0) -> (3,3,0)
    # (6,0,0), (0,0,6) -> (3,0,3)
    # (0,6,0), (0,0,6) -> (0,3,3)
    # newly_generated_points = {(3,0,0), (0,3,0), (0,0,3), (3,3,0), (3,0,3), (0,3,3)}
    # target (1,1,1) not in Gen 1. all_known_points updated.
    # Gen 2:
    # (0,0,0), (3,0,0) -> (1,0,0)
    # (0,0,0), (0,3,0) -> (0,1,0)
    # (0,0,0), (0,0,3) -> (0,0,1)
    # ... Many more pairs
    # (0,0,0), (3,3,0) -> (1,1,0)
    # (0,0,0), (0,3,3) -> (0,1,1)
    # (0,0,0), (3,0,3) -> (1,0,1)
    # (3,0,0), (0,3,0) -> (1,1,0)
    # (1,0,0), (0,1,0) -> (0,0,0) (this is a duplicate, already in all_known_points)
    # (1,0,0), (0,1,0) will not generate (1,1,1)
    # It seems (0,0,0) combined with (some_point_with_3s) would give (1,1,1) in next gen.
    # (0,0,0) + (2,2,2) -> (1,1,1)
    # To get (2,2,2), we need e.g. (0,0,0) + (5,5,5) which isn't there, or (0,0,0) + (4,4,4) or (2,2,2)+(2,2,2) etc.
    # This might take a few generations.
    # The BFS guarantees minimal. It's too complex to manually trace all 343 points.
    # Let's trust the algorithm for this one.
    assert s.minGenerations(points6, target6) == 3, f"Test Case 6 Failed: Expected 3, Got {s.minGenerations(points6, target6)}"
    # (0,0,0) + (6,6,6) (if we had it) -> (3,3,3)
    # (0,0,0) + (4,4,4) -> (2,2,2)
    # (0,0,0) + (2,2,2) -> (1,1,1)
    # If we get (4,4,4) first, then (2,2,2), then (1,1,1)
    # (6,0,0) + (0,6,0) -> (3,3,0) (Gen 1)
    # (3,3,0) + (0,0,6) -> (1,1,3) (Gen 2)
    # (0,0,0) + (6,6,6) is not in initial
    # We need to construct (4,4,4) for (2,2,2) then (1,1,1)
    # (6,0,0) + (0,6,0) + (0,0,6) not a point.
    # Let's consider (0,0,0) and (6,6,6) as the only input for target (1,1,1)
    # Gen 0: {(0,0,0), (6,6,6)}
    # Gen 1: {(3,3,3)}
    # Gen 2:
    # (0,0,0), (3,3,3) -> (1,1,1) - Target found in Gen 2.
    # In points6, we have (0,0,0), (6,0,0), (0,6,0), (0,0,6).
    # Can we reach (6,6,6)? No. Can we reach (5,5,5)? No.
    # (6,0,0) + (0,6,0) -> (3,3,0) (Gen 1)
    # (6,0,0) + (0,0,6) -> (3,0,3) (Gen 1)
    # (0,6,0) + (0,0,6) -> (0,3,3) (Gen 1)
    # Gen 2 points: (0,0,0) + (3,3,0) -> (1,1,0)
    # (0,0,0) + (3,0,3) -> (1,0,1)
    # (0,0,0) + (0,3,3) -> (0,1,1)
    # Yes, (1,1,1) can be formed by averaging (0,0,0) and (2,2,2).
    # To get (2,2,2):
    # (6,0,0) + (0,6,0) + (0,0,6) can't average 3 points.
    # Consider (0,0,0) + some point. We need that "some point" to be (2,2,2) or (3,3,3) or (4,4,4).
    # The example given `points = [[0,0,0],[5,5,5]], target = [1,1,1]` -> 2.
    # We have points that sum to (6,6,6), (6,0,0), (0,6,0), (0,0,6) (all from initial points + combinations)
    # Can we get (2,2,2) in Gen 2?
    # Gen 1 has {(3,0,0), (0,3,0), (0,0,3), (3,3,0), (3,0,3), (0,3,3)}
    # Now in Gen 2, pairs from {(0,0,0), (6,0,0), (0,6,0), (0,0,6), and Gen 1 points}.
    # (3,0,0) + (0,3,0) -> (1,1,0)
    # (3,3,0) + (0,0,6) -> (1,1,3)
    # (3,0,3) + (0,3,0) -> (1,1,1)
    # Yes, (3,0,3) and (0,3,0) are both in Gen 1 (or Gen 0/Gen 1). They result in (1,1,1) in Gen 2.
    # Ah, (3,0,3) from (6,0,0) and (0,0,6)
    # And (0,3,0) from (0,6,0) and (0,0,0)
    # Both are Gen 1 points.
    # So (3,0,3) is in Gen 1, (0,3,0) is in Gen 1.
    # Averaging two points from Gen 1 gives (1,1,1) in Gen 2. My expected 3 was too high.
    # The actual result for Test Case 6 is 2. Let's correct it.
    assert s.minGenerations(points6, target6) == 2, f"Test Case 6 Failed: Expected 2, Got {s.minGenerations(points6, target6)}"


    print("All tests passed!")

