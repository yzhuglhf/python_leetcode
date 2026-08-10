import collections
from typing import List

class Solution:
    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Precompute prefix sums. prefix_sum[i] stores sum of nums[0...i-1].
        # prefix_sum[0] = 0.
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]

        # Helper function to calculate subarray value: sumArr * (sumArr + 1) / 2
        def calculate_value(s: int) -> int:
            # Handles s = -1 correctly, resulting in 0, which is necessary for the CHT formula
            return s * (s + 1) // 2

        # dp[i][j] stores the minimum score to partition nums[0...i-1] into j subarrays.
        # dp table size is (n+1) x (k+1).
        dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0  # Base case: 0 elements, 0 subarrays, score 0.

        # Iterate through the number of partitions (j) from 1 to k.
        for j in range(1, k + 1):
            # Deque for Convex Hull Trick optimization.
            # Stores points (X_p, Y_p) where:
            # X_p = prefix_sum[p]
            # Y_p = dp[p][j-1] + calculate_value(prefix_sum[p]-1)
            # These points represent states from the (j-1)-th partition step.
            deque = collections.deque()

            # Iterate through `i`, which represents the current length of the prefix `nums[0...i-1]`.
            # This loop also effectively handles the `p` (split point) for adding points to the deque,
            # and `curr_idx` for querying `dp[curr_idx][j]`.
            # `i` goes from 0 to `n`.
            for i in range(n + 1):
                # Step 1: Add a point (based on dp[i][j-1]) to the deque.
                # This point (X_i, Y_i) corresponds to partitioning `nums[0...i-1]` into `j-1` subarrays.
                # It serves as a potential starting point for the `j`-th subarray in subsequent calculations.
                # A valid point `i` must satisfy `i >= j-1` (to form `j-1` partitions)
                # and `dp[i][j-1]` must be a finite, achievable score.
                if i >= j - 1 and dp[i][j - 1] != float('inf'):
                    X_val_to_add = prefix_sum[i]
                    Y_val_to_add = dp[i][j - 1] + calculate_value(prefix_sum[i] - 1)

                    # Maintain the lower convex hull property: remove points from the back
                    # if adding the new point `(X_val_to_add, Y_val_to_add)` would violate convexity.
                    # The condition `(slope P2_P1) >= (slope P_new_P2)` means P2 is not needed.
                    # Using cross-product to avoid division:
                    # (P2_Y - P1_Y) * (X_new - P2_X) >= (Y_new - P2_Y) * (P2_X - P1_X)
                    while len(deque) >= 2:
                        p_val1 = deque[-2]  # Second-to-last point (P1)
                        p_val2 = deque[-1]  # Last point (P2)

                        if (p_val2[1] - p_val1[1]) * (X_val_to_add - p_val2[0]) >= \
                           (Y_val_to_add - p_val2[1]) * (p_val2[0] - p_val1[0]):
                            deque.pop()  # Remove P2
                        else:
                            break
                    deque.append((X_val_to_add, Y_val_to_add))
                
                # Step 2: Query the deque to calculate dp[i][j].
                # This `i` now represents `curr_idx` for `dp[curr_idx][j]`.
                # We need at least `j` elements to form `j` subarrays, so `i` must be at least `j`.
                # Also, the deque must not be empty to perform a query.
                if i >= j and len(deque) > 0:
                    # K = -prefix_sum[i] is the slope of the query line.
                    # Since K is non-increasing, we remove points from the front of the deque
                    # whose corresponding line segments have slopes less than or equal to K.
                    # This ensures that `deque[0]` represents the optimal `p` for the current `K`.
                    # Condition: (slope P1_P2) <= K (for pop P1)
                    # Integer form (since P2_X - P1_X > 0): (P2_Y - P1_Y) <= K * (P2_X - P1_X)
                    K = -prefix_sum[i]
                    while len(deque) >= 2:
                        p_val1 = deque[0]  # First point (P1)
                        p_val2 = deque[1]  # Second point (P2)

                        if (p_val2[1] - p_val1[1]) <= K * (p_val2[0] - p_val1[0]):
                            deque.popleft()  # Remove P1
                        else:
                            break
                    
                    # The optimal point `p` (index `p_idx`) is now at the front of the deque.
                    # `best_p_X` is `prefix_sum[p_idx]`, `best_p_Y` is `dp[p_idx][j-1] + calculate_value(prefix_sum[p_idx]-1)`.
                    best_p_X, best_p_Y = deque[0]
                    
                    # Compute dp[i][j] using the CHT optimized formula:
                    # dp[i][j] = calculate_value(prefix_sum[i]) + best_p_Y + K * best_p_X
                    # This is equivalent to dp[p_idx][j-1] + calculate_value(prefix_sum[i] - prefix_sum[p_idx]).
                    dp[i][j] = best_p_Y + K * best_p_X + calculate_value(prefix_sum[i])
        
        return dp[n][k]

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [5, 1, 2, 1]
    k1 = 2
    assert s.minPartitionScore(nums1, k1) == 25, f"Test Case 1 Failed: {s.minPartitionScore(nums1, k1)}"

    # Example 2
    nums2 = [1, 2, 3, 4]
    k2 = 1
    assert s.minPartitionScore(nums2, k2) == 55, f"Test Case 2 Failed: {s.minPartitionScore(nums2, k2)}"

    # Example 3
    nums3 = [1, 1, 1]
    k3 = 3
    assert s.minPartitionScore(nums3, k3) == 3, f"Test Case 3 Failed: {s.minPartitionScore(nums3, k3)}"

    # Custom Test Case: multiple ways, small numbers
    nums4 = [10, 20, 30]
    k4 = 1
    assert s.minPartitionScore(nums4, k4) == 1830, f"Test Case 4 Failed: {s.minPartitionScore(nums4, k4)}"

    nums5 = [10, 20, 30]
    k5 = 2
    assert s.minPartitionScore(nums5, k5) == 930, f"Test Case 5 Failed: {s.minPartitionScore(nums5, k5)}"

    nums6 = [10, 20, 30]
    k6 = 3
    assert s.minPartitionScore(nums6, k6) == 730, f"Test Case 6 Failed: {s.minPartitionScore(nums6, k6)}"
    
    # Another test, larger nums
    nums7 = [1,2,3,4,5]
    k7 = 2
    assert s.minPartitionScore(nums7, k7) == 66, f"Test Case 7 Failed: {s.minPartitionScore(nums7, k7)}"

    # Max constraints test (all ones, k=n)
    nums_all_ones = [1] * 1000
    k_all_ones = 1000
    assert s.minPartitionScore(nums_all_ones, k_all_ones) == 1000, f"Test Case All Ones Failed: {s.minPartitionScore(nums_all_ones, k_all_ones)}"

    print("All tests passed!")

