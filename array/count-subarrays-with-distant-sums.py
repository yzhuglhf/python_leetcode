"""
Count Subarrays with Distant Sums
Difficulty: Hard

Description:
This problem asks us to count subarrays where the absolute difference between its sum and a given goal is at least k. This can be rephrased as finding subarrays whose sum S satisfies S >= goal + k or S <= goal - k. It's often easier to count the complement: subarrays that are NOT distant, meaning their sum S satisfies goal - k < S < goal + k. The total distant subarrays will then be (total subarrays) - (non-distant subarrays).

Example:
Input: nums = [1,2,1], goal = 4, k = 1
Output: 5
Explanation: The total subarrays are 6. The non-distant subarrays are those with sum S such that 3 < S < 5, i.e., S = 4. Only [1,2,1] has sum 4. So 6 - 1 = 5 distant subarrays.

Approach:
The problem is transformed into counting subarrays whose sum falls within certain ranges. Specifically, we need to count subarrays with sum S such that `S >= goal + k` or `S <= goal - k`. This is equivalent to `Total Subarrays - (subarrays such that goal - k < S < goal + k)`. The count of subarrays `S` such that `A < S < B` (i.e., `A+1 <= S <= B-1`) can be expressed using a helper function `f(X)` that counts subarrays with sum `S <= X`. The number of non-distant subarrays is then `f(goal + k - 1) - f(goal - k)`.
The function `f(X)` is implemented using prefix sums and a Fenwick Tree (BIT). We first compute all prefix sums `P[i] = nums[0] + ... + nums[i-1]` (with `P[0] = 0`). A subarray sum `nums[i..j]` is `P[j+1] - P[i]`. For a fixed right endpoint `j` (meaning `P[j+1]` is current prefix sum), we need to find previous prefix sums `P[i]` (`i <= j`) such that `P[j+1] - P[i] <= X`. This rearranges to `P[i] >= P[j+1] - X`.
To efficiently count such `P[i]` values, we use a Fenwick Tree. Since prefix sums can be very large, coordinate compression is applied to all relevant `P[x]` and `P[x]-X` values to map them to smaller, 0-indexed values suitable for the BIT. The Fenwick Tree allows efficient querying of counts within a range (sum of frequencies) and updating individual counts in O(log M) time, where M is the number of unique compressed coordinates.

Time Complexity: O(N log N)
The `count_subarrays_le_X` function iterates through `N+1` prefix sums. In each iteration, `bisect_left` (for coordinate compression) and Fenwick Tree operations (`update`, `query`) each take O(log M) time, where M is the number of unique coordinates (at most `2N` for `P[x]` and `P[x]-X` values). Since this function is called twice, the total time complexity is O(N log N).
Space Complexity: O(N)
The prefix sum array `P` takes O(N) space. The `all_coords` set, `sorted_coords` list, `val_to_idx` dictionary (for coordinate compression), and the `FenwickTree` itself all store up to O(N) distinct values or elements, leading to O(N) space complexity.
"""
from typing import List
import bisect

class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1) # 1-based indexing for BIT operations
        self.size = size

    def update(self, idx, delta):
        # idx is 0-based coordinate, convert to 1-based for BIT
        idx += 1 
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, idx):
        # idx is 0-based coordinate, convert to 1-based for BIT
        # To get sum up to idx (inclusive), query(idx)
        # To get sum from A to B (inclusive, with A, B 0-based coords), query(B) - query(A-1)
        idx += 1
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s

class Solution:
    def distantSubarrays(self, nums: List[int], goal: int, k: int) -> int:
        n = len(nums)
        
        # Calculate prefix sums
        # P[i] = sum(nums[0...i-1]), P[0] = 0
        P = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            
        # Total number of subarrays in an array of length n is n*(n+1)/2
        total_subarrays = n * (n + 1) // 2

        # Special case: If k = 0, the condition abs(sum - goal) >= 0 is always true.
        # So, all subarrays are considered distant.
        if k == 0:
            return total_subarrays

        # Helper function to count subarrays whose sum S <= X_limit
        # A subarray sum S[i..j] is P[j+1] - P[i].
        # We need to count pairs (i, j) where 0 <= i <= j < n such that P[j+1] - P[i] <= X_limit.
        # This is equivalent to P[i] >= P[j+1] - X_limit.
        def count_subarrays_le_X(X_limit):
            # Collect all relevant values for coordinate compression.
            # These are P values themselves, and (P_val - X_limit) values that will be used as thresholds.
            all_coords = set()
            for p_val in P:
                all_coords.add(p_val)
                all_coords.add(p_val - X_limit)
            
            # Sort unique values to create a mapping to compressed indices (0 to M-1).
            sorted_coords = sorted(list(all_coords))
            val_to_idx = {val: idx for idx, val in enumerate(sorted_coords)}
            M = len(sorted_coords) # Number of unique coordinates
            
            bit = FenwickTree(M)
            
            count = 0
            # Iterate through all possible right endpoints for subarrays.
            # `j` iterates from 0 to n. P[j] represents the prefix sum up to index j-1.
            # When j is fixed, P[j] is `current_prefix_sum`. We look for `P[i]` where `i < j`.
            for j in range(n + 1):
                current_prefix_sum = P[j]
                
                # The target threshold for P[i] is `current_prefix_sum - X_limit`.
                # We want to count P[i] values seen so far (for i < j) such that P[i] >= target_threshold.
                target_threshold = current_prefix_sum - X_limit
                
                # Use bisect_left to find the smallest index `idx` in `sorted_coords`
                # such that `sorted_coords[idx] >= target_threshold`. This `idx` is a 0-based coordinate.
                threshold_coord_idx = bisect.bisect_left(sorted_coords, target_threshold)
                
                # Query the Fenwick Tree:
                # `bit.query(M - 1)` gives the total count of all prefix sums added to the BIT so far.
                # `bit.query(threshold_coord_idx - 1)` gives the count of prefix sums that are
                # strictly less than `target_threshold` (i.e., correspond to compressed indices < threshold_coord_idx).
                # Their difference gives the count of prefix sums that are >= `target_threshold`.
                count += bit.query(M - 1) - bit.query(threshold_coord_idx - 1)
                
                # Add the current prefix sum `P[j]` to the BIT.
                # This `P[j]` will serve as a `P[i]` for future iterations (when considering `P[j'] - P[j]` for j' > j).
                bit.update(val_to_idx[current_prefix_sum], 1)
            
            return count

        # A subarray is *not* distant if goal - k < sum < goal + k.
        # This is equivalent to goal - k + 1 <= sum <= goal + k - 1.
        # We can calculate this range count using the `count_subarrays_le_X` helper function:
        # count(S <= goal + k - 1) - count(S <= goal - k)
        
        count_le_upper_bound = count_subarrays_le_X(goal + k - 1)
        count_le_lower_bound = count_subarrays_le_X(goal - k)
        
        count_not_distant = count_le_upper_bound - count_le_lower_bound
        
        # The final answer is total subarrays minus non-distant subarrays.
        return total_subarrays - count_not_distant

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [1,2,1]
    goal1 = 4
    k1 = 1
    assert s.distantSubarrays(nums1, goal1, k1) == 5, f"Test 1 failed: Expected 5, Got {s.distantSubarrays(nums1, goal1, k1)}"

    # Example 2
    nums2 = [2,-1,3]
    goal2 = 2
    k2 = 2
    assert s.distantSubarrays(nums2, goal2, k2) == 2, f"Test 2 failed: Expected 2, Got {s.distantSubarrays(nums2, goal2, k2)}"

    # Example 3
    nums3 = [-3,1,2]
    goal3 = 0
    k3 = 3
    assert s.distantSubarrays(nums3, goal3, k3) == 2, f"Test 3 failed: Expected 2, Got {s.distantSubarrays(nums3, goal3, k3)}"

    # Additional Test: k = 0 (all subarrays are distant)
    nums4 = [1,2,3]
    goal4 = 5
    k4 = 0
    # Total subarrays = 3*(3+1)/2 = 6
    assert s.distantSubarrays(nums4, goal4, k4) == 6, f"Test 4 (k=0) failed: Expected 6, Got {s.distantSubarrays(nums4, goal4, k4)}"

    # Additional Test: No distant subarrays
    nums5 = [1,1,1]
    goal5 = 2
    k5 = 10
    # Possible sums: 1, 1, 1, 2, 2, 3
    # abs(sum - goal) >= 10 => abs(sum - 2) >= 10
    # Sums are 1,2,3. abs(1-2)=1, abs(2-2)=0, abs(3-2)=1. All < 10.
    # Expected 0 distant subarrays.
    assert s.distantSubarrays(nums5, goal5, k5) == 0, f"Test 5 (no distant) failed: Expected 0, Got {s.distantSubarrays(nums5, goal5, k5)}"

    # Additional Test: All distant subarrays
    nums6 = [100]
    goal6 = 0
    k6 = 50
    # Sums: [100]. abs(100-0)=100. 100 >= 50. Distant.
    # Total subarrays = 1.
    assert s.distantSubarrays(nums6, goal6, k6) == 1, f"Test 6 (all distant) failed: Expected 1, Got {s.distantSubarrays(nums6, goal6, k6)}"

    # Large values test
    nums7 = [10**9, -10**9, 10**9]
    goal7 = 0
    k7 = 10**9
    # P = [0, 10^9, 0, 10^9]
    # Sums: [10^9], [-10^9], [10^9], [0], [0], [10^9]
    # abs(S-0) >= 10^9 => abs(S) >= 10^9
    # Distant: [10^9], [-10^9], [10^9], [10^9] (4 subarrays)
    # Non-distant: [0], [0] (2 subarrays)
    # Total = 6. Expected 4.
    assert s.distantSubarrays(nums7, goal7, k7) == 4, f"Test 7 (large values) failed: Expected 4, Got {s.distantSubarrays(nums7, goal7, k7)}"


    print("All tests passed!")

