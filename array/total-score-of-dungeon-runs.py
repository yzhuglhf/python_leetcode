"""
Total Score of Dungeon Runs
Difficulty: Medium

Description:
This problem asks us to calculate the sum of scores obtained from starting at each possible room `j` (from 1 to `n`) and proceeding to room `n`. For a given starting room `j`, a point is earned in room `k` (where `j <= k <= n`) if the health remaining after taking `damage[k-1]` is at least `requirement[k-1]`. We need to sum `score(j)` for all `j` from 1 to `n`.

Example:
Input: hp = 11, damage = [3,6,7], requirement = [4,2,5]
Output: 3
Explanation:
score(1) = 2:
  Start with 11 hp.
  Room 1: 11 - 3 = 8. 8 >= 4 (point!). HP = 8.
  Room 2: 8 - 6 = 2. 2 >= 2 (point!). HP = 2.
  Room 3: 2 - 7 = -5. -5 < 5 (no point). HP = -5.
score(2) = 1:
  Start with 11 hp.
  Room 2: 11 - 6 = 5. 5 >= 2 (point!). HP = 5.
  Room 3: 5 - 7 = -2. -2 < 5 (no point). HP = -2.
score(3) = 0:
  Start with 11 hp.
  Room 3: 11 - 7 = 4. 4 < 5 (no point). HP = 4.
Total score = 2 + 1 + 0 = 3.

Approach:
The problem asks to sum scores across all possible starting rooms. A naive O(N^2) approach of simulating each `score(j)` would be too slow for N up to 10^5. We can optimize this by observing the condition for earning a point. For a room `k` (1-indexed), starting from room `j` (1-indexed), a point is earned if `hp - (total damage from room j to k) >= requirement[k-1]`.

Let `pref_damage[i]` be the sum of `damage[0]` through `damage[i-1]`, with `pref_damage[0] = 0`. This means `pref_damage[i]` is the total damage from rooms 1 to `i`. The total damage from room `j` to `k` can then be expressed as `pref_damage[k] - pref_damage[j-1]`.
Substituting this into the condition:
`hp - (pref_damage[k] - pref_damage[j-1]) >= requirement[k-1]`
Rearranging the terms, we get:
`pref_damage[j-1] >= requirement[k-1] + pref_damage[k] - hp`

For each room `k` (from 1 to `n`), we want to count how many `j` (from 1 to `k`) satisfy this condition. The left side, `pref_damage[j-1]`, depends on the starting room `j`. The right side, `requirement[k-1] + pref_damage[k] - hp`, is a constant for a fixed `k`.
This structure suggests using a data structure that can efficiently count elements greater than or equal to a certain value. A Fenwick tree (or Binary Indexed Tree, BIT) is suitable for this.

Since the values `pref_damage[j-1]` and `requirement[k-1] + pref_damage[k] - hp` can be very large (up to 10^9), we need coordinate compression. We collect all relevant values (`pref_damage` values and all `target_value` thresholds), sort them, and map them to ranks (1 to `U`, where `U` is the number of unique values).

The algorithm proceeds as follows:
1. Compute the `pref_damage` array. `pref_damage[i]` stores the cumulative damage up to room `i` (1-indexed).
2. Collect all `pref_damage` values (for `j-1` in `pref_damage[j-1]`) and all `target_value` thresholds (`requirement[k-1] + pref_damage[k] - hp` for each `k`) into a set. Sort this set to get unique sorted coordinates and create a mapping from value to 1-based rank.
3. Initialize a Fenwick Tree with size equal to the number of unique coordinates.
4. Add `pref_damage[0]` (representing `j=1` or starting before room 1) to the Fenwick Tree. This value is `0`.
5. Iterate `k_idx` from `0` to `n-1` (representing the current 0-indexed room).
   a. Calculate the `target_value` for room `k_idx+1`.
   b. Query the Fenwick Tree to count how many `pref_damage[p]` (for `p` from `0` to `k_idx`, which are the values added so far representing `j` from `1` to `k_idx+1`) are greater than or equal to `target_value`. Each such count adds to the total score.
   c. After processing queries for room `k_idx+1`, add `pref_damage[k_idx+1]` (representing a potential starting point `j=k_idx+2`) to the Fenwick Tree for use in subsequent iterations.
The sum of all counts accumulated is the final answer.

Time Complexity: O(N log N) due to sorting for coordinate compression and N Fenwick Tree operations, each taking O(log U) time, where U is the number of unique coordinates (at most 2N+1).
Space Complexity: O(N) for storing the prefix sums, coordinates, mapping, and the Fenwick Tree.
"""
from typing import List

class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, delta):
        # index should be 1-based
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index):
        # index should be 1-based, queries sum from 1 to index
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & (-index)
        return s

class Solution:
    def totalScore(self, hp: int, damage: List[int], requirement: List[int]) -> int:
        n = len(damage)

        # 1. Compute prefix_sum_damage array
        # pref_damage[i] = sum of damage from room 1 to room i (1-indexed)
        # pref_damage[0] = 0
        pref_damage = [0] * (n + 1)
        for i in range(n):
            pref_damage[i+1] = pref_damage[i] + damage[i]

        # 2. Collect all values for coordinate compression
        # These include all pref_damage values (for j-1) and all target_values (for querying)
        all_coords = set()
        for val in pref_damage:
            all_coords.add(val)
        
        for k_idx in range(n): # k_idx is 0-indexed room number
            # k is 1-indexed room number (k_idx + 1)
            # requirement[k_idx] is for room k
            # pref_damage[k_idx + 1] is sum of damage up to room k
            # target_value_for_k = requirement[k-1] + pref_damage[k] - hp
            target_val_for_k = requirement[k_idx] + pref_damage[k_idx + 1] - hp
            all_coords.add(target_val_for_k)
        
        unique_sorted_coords = sorted(list(all_coords))
        # Map values to 1-based ranks for Fenwick Tree
        coord_to_rank = {val: i + 1 for i, val in enumerate(unique_sorted_coords)}
        
        # 3. Initialize Fenwick Tree
        bit_size = len(unique_sorted_coords)
        bit = FenwickTree(bit_size)
        
        total_overall_score = 0
        
        # 4. Add pref_damage[0] to BIT before the loop
        # pref_damage[0] corresponds to the case where j=1 (starting at room 1).
        # This makes pref_damage[0] available for queries when k=1.
        bit.update(coord_to_rank[pref_damage[0]], 1)
        
        # 5. Iterate through rooms (k_idx from 0 to n-1)
        # k_idx represents the 0-indexed current room.
        # This means the 1-indexed room number is k_idx + 1.
        for k_idx in range(n):
            # a. Query: For current room (k_idx + 1), count how many valid starting points j
            #    (1 <= j <= k_idx + 1) satisfy the condition pref_damage[j-1] >= target_val_for_k.
            #    The pref_damage[j-1] values available in BIT at this point are pref_damage[0]...pref_damage[k_idx].
            
            # target_value for current room (k_idx + 1)
            target_val_for_k = requirement[k_idx] + pref_damage[k_idx + 1] - hp
            
            # Find the rank of the target_val_for_k.
            # We want to count elements with value >= target_val_for_k.
            # In ranks, this means rank >= rank_target.
            # So, query total count (bit.query(bit_size)) minus count of elements with rank < rank_target (bit.query(rank_target - 1)).
            rank_target = coord_to_rank[target_val_for_k]
            count = bit.query(bit_size) - bit.query(rank_target - 1)
            total_overall_score += count
            
            # b. Update: Add pref_damage[k_idx + 1] to the BIT for future queries.
            #    pref_damage[k_idx + 1] corresponds to starting point j = (k_idx + 1) + 1.
            #    This makes it available for queries when rooms (k_idx + 2) and later are processed.
            #    This is crucial to ensure that for room K, all pref_damage[0]...pref_damage[K-1] are available.
            bit.update(coord_to_rank[pref_damage[k_idx + 1]], 1)
            
        return total_overall_score

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.totalScore(hp = 11, damage = [3,6,7], requirement = [4,2,5]) == 3, "Example 1 Failed"
    # Example 2
    assert s.totalScore(hp = 2, damage = [10000,1], requirement = [1,1]) == 1, "Example 2 Failed"
    
    # Custom Test 1: Single room, point earned
    assert s.totalScore(hp = 10, damage = [5], requirement = [3]) == 1, "Custom Test 1 Failed"
    
    # Custom Test 2: Single room, no point earned
    assert s.totalScore(hp = 5, damage = [10], requirement = [1]) == 0, "Custom Test 2 Failed"

    # Custom Test 3: Multiple rooms, varied points
    assert s.totalScore(hp = 20, damage = [5,5,5], requirement = [5,5,5]) == 6, "Custom Test 3 Failed"
    # Explanation for Custom Test 3:
    # hp=20, damage=[5,5,5], requirement=[5,5,5]
    # pref_damage = [0, 5, 10, 15]
    #
    # k=1 (room 1): target = req[0]+pref[1]-hp = 5+5-20 = -10.
    #   pref[0]=0 >= -10 (Yes). Count=1. Total=1.
    #   BIT adds pref[1]=5. BIT has {0,5}
    #
    # k=2 (room 2): target = req[1]+pref[2]-hp = 5+10-20 = -5.
    #   pref[0]=0 >= -5 (Yes)
    #   pref[1]=5 >= -5 (Yes). Count=2. Total=1+2=3.
    #   BIT adds pref[2]=10. BIT has {0,5,10}
    #
    # k=3 (room 3): target = req[2]+pref[3]-hp = 5+15-20 = 0.
    #   pref[0]=0 >= 0 (Yes)
    #   pref[1]=5 >= 0 (Yes)
    #   pref[2]=10 >= 0 (Yes). Count=3. Total=3+3=6.
    #   BIT adds pref[3]=15. BIT has {0,5,10,15}
    # Final total = 6.

    # Custom Test 4: All negative health, no points
    assert s.totalScore(hp = 1, damage = [10,10,10], requirement = [1,1,1]) == 0, "Custom Test 4 Failed"
    
    # Custom Test 5: Large values, but simple scenario
    assert s.totalScore(hp = 10**9, damage = [1], requirement = [1]) == 1, "Custom Test 5 Failed"

    print("All tests passed!")