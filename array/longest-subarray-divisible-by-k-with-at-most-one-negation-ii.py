from typing import List

class Solution:
    def longestSubarray(self, nums: List[int], k: int) -> int:
        max_length = 0
        current_prefix_sum = 0
        
        # remainder_to_first_idx_P stores:
        # P[x] % k -> x
        # Where P[x] = sum(nums[0...x-1]) and P[0] = 0.
        # This map helps find the smallest starting index `i` (represented by `x`)
        # for a subarray ending at `j` (meaning its sum is P[j+1] - P[x]).
        # The key 0 (for remainder 0) is associated with index 0 (for P[0]).
        remainder_to_first_idx_P = {0: 0} 

        for j in range(len(nums)):
            current_prefix_sum += nums[j]
            
            # Ensure remainder is non-negative, as Python's % operator can return negative results for negative numbers
            current_rem_P_j_plus_1 = current_prefix_sum % k
            if current_rem_P_j_plus_1 < 0:
                current_rem_P_j_plus_1 += k
            
            # --- Case 1: No negation required ---
            # We are looking for an index `i` such that the sum of `nums[i...j]` is divisible by `k`.
            # This is equivalent to `(P[j+1] - P[i]) % k == 0`, or `P[j+1] % k == P[i] % k`.
            # We use `remainder_to_first_idx_P` to find the smallest `i` (stored as `x` in the map)
            # such that `P[x] % k` matches `P[j+1] % k`.
            if current_rem_P_j_plus_1 in remainder_to_first_idx_P:
                i_candidate_no_negation = remainder_to_first_idx_P[current_rem_P_j_plus_1]
                # The length of the subarray `nums[i_candidate_no_negation ... j]` is `(j + 1) - i_candidate_no_negation`.
                max_length = max(max_length, (j + 1) - i_candidate_no_negation)
            
            # --- Case 2: One negation at 'p=j' (the current rightmost element of the subarray) ---
            # We are looking for an index `i` such that the sum of `nums[i...j]` with `nums[j]` negated
            # is divisible by `k`. This means `(P[j+1] - P[i] - 2 * nums[j]) % k == 0`.
            # This simplifies to `P[i] % k == (P[j+1] - 2 * nums[j]) % k`.
            # `P[j+1]` is `current_prefix_sum`.
            target_rem_for_Pi = (current_prefix_sum - 2 * nums[j]) % k
            if target_rem_for_Pi < 0:
                target_rem_for_Pi += k
            
            # We query the `remainder_to_first_idx_P` map for this `target_rem_for_Pi`.
            # If found, `i_candidate_negation` will be the smallest `x` such that `P[x] % k` equals the target remainder.
            # This `i_candidate_negation` is guaranteed to be less than or equal to `j`,
            # because the `remainder_to_first_idx_P` map is populated with indices from `0` up to `j`.
            # Thus, the condition `i <= p` (where `p=j`) is implicitly satisfied.
            if target_rem_for_Pi in remainder_to_first_idx_P:
                i_candidate_negation = remainder_to_first_idx_P[target_rem_for_Pi]
                max_length = max(max_length, (j + 1) - i_candidate_negation)

            # Update the map with the current prefix sum remainder if it's the first time
            # seeing this remainder. This must be done after using `current_prefix_sum` for calculations
            # for cases 1 and 2 in the current iteration `j`, but before moving to `j+1`.
            # This ensures that `i_candidate` values retrieved from the map are for `P[x]` where `x <= j`.
            if current_rem_P_j_plus_1 not in remainder_to_first_idx_P:
                remainder_to_first_idx_P[current_rem_P_j_plus_1] = j + 1
        
        return max_length

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [4, 1, 2]
    k1 = 3
    assert s.longestSubarray(nums1, k1) == 3, f"Test 1 Failed: {s.longestSubarray(nums1, k1)}"

    # Example 2
    nums2 = [5, 3, 4]
    k2 = 7
    assert s.longestSubarray(nums2, k2) == 2, f"Test 2 Failed: {s.longestSubarray(nums2, k2)}"

    # Example 3
    nums3 = [2, 2, 5]
    k3 = 6
    assert s.longestSubarray(nums3, k3) == 2, f"Test 3 Failed: {s.longestSubarray(nums3, k3)}"

    # Custom Test Case: no valid subarray
    nums4 = [1, 2, 3]
    k4 = 7
    assert s.longestSubarray(nums4, k4) == 0, f"Test 4 Failed: {s.longestSubarray(nums4, k4)}"

    # Custom Test Case: Array with negative numbers
    nums5 = [-1, -2, 3, 4]
    k5 = 3
    # Subarray [-1, -2, 3, 4] sum = 4. Negate -1 -> [1, -2, 3, 4] sum = 6 (div by 3). Length 4.
    # Subarray [3, 4] sum = 7. Negate 3 -> [ -3, 4] sum = 1. Negate 4 -> [3, -4] sum = -1.
    # Subarray [-2, 3, 4] sum = 5. Negate -2 -> [2, 3, 4] sum = 9 (div by 3). Length 3.
    assert s.longestSubarray(nums5, k5) == 4, f"Test 5 Failed: {s.longestSubarray(nums5, k5)}"

    # Custom Test Case: All zeros
    nums6 = [0, 0, 0, 0]
    k6 = 5
    assert s.longestSubarray(nums6, k6) == 4, f"Test 6 Failed: {s.longestSubarray(nums6, k6)}"
    
    # Custom Test Case: Single element array
    nums7 = [10]
    k7 = 5
    assert s.longestSubarray(nums7, k7) == 1, f"Test 7 Failed: {s.longestSubarray(nums7, k7)}"

    # Custom Test Case: Max length should be 1 if sum cannot be changed
    nums8 = [1]
    k8 = 2
    assert s.longestSubarray(nums8, k8) == 0, f"Test 8 Failed: {s.longestSubarray(nums8, k8)}"

    print("All tests passed!")

