"""
Palindromic Subarray Sum
Difficulty: Hard

Description:
This problem asks us to find the maximum possible sum among all contiguous subarrays of a given integer array `nums` that are palindromes. All elements in `nums` are positive, which simplifies the problem as longer palindromic extensions always yield a strictly larger sum for a given center.

Example:
Input: nums = [1,2,3,2,1,5,6]
Output: 9
Explanation: The contiguous subarray [1,2,3,2,1] is a palindrome with sum 9.

Approach:
The problem requires finding palindromic subarrays and their sums. A naive O(N^3) or O(N^2) approach (iterating all subarrays and checking for palindrome property) would be too slow for N up to 10^5. We need an O(N log N) or O(N) solution. A common technique to find palindromes efficiently is "expanding from center" combined with hashing and binary search.

The algorithm proceeds as follows:
1.  **Initialization**: Initialize `max_pal_sum` with the maximum single element in `nums`, as any single element is a palindrome.
2.  **Prefix Sums**: Compute an array `prefix_sums` where `prefix_sums[k]` stores the sum of `nums[0...k-1]`. This allows calculating the sum of any subarray `nums[start...end]` in O(1) time.
3.  **Hashing Precomputation**: To efficiently check if a subarray `nums[start...end]` is a palindrome, we use polynomial rolling hashes. We precompute two sets of hashes:
    *   `forward_hash`: Stores hashes of all prefixes `nums[0...k-1]`.
    *   `rev_prefix_hash`: Stores hashes of all prefixes of the reversed array `nums_rev` (where `nums_rev[i] = nums[N-1-i]`).
    We use two different prime bases and moduli (double hashing) to minimize collision probability. We also precompute powers of the bases for O(1) substring hash calculation.
4.  **Palindrome Check Function**: Create a helper function `is_palindrome_hash(start, end)` that uses the precomputed hashes to check if `nums[start...end]` is a palindrome in O(1) time. This involves comparing the forward hash of `nums[start...end]` with the forward hash of its reversed counterpart (which can be obtained from `rev_prefix_hash`).
5.  **Expand from Centers with Binary Search**:
    *   **Odd Length Palindromes**: Iterate through each index `i` from `0` to `N-1`. This `i` acts as the center of a potential odd-length palindrome. For each `i`, binary search for the maximum radius `k` such that `nums[i-k ... i+k]` is a palindrome, using `is_palindrome_hash`. Once the maximum `k` is found, calculate the sum of `nums[i-k ... i+k]` using `prefix_sums` and update `max_pal_sum`.
    *   **Even Length Palindromes**: Iterate through each index `i` from `0` to `N-2`. This pair `(i, i+1)` acts as the center of a potential even-length palindrome. For each `i`, binary search for the maximum half-length `k` such that `nums[i-k+1 ... i+k]` is a palindrome. Calculate its sum and update `max_pal_sum`.

Since all `nums[i]` are positive, a larger palindromic subarray (for a given center) will always have a larger sum. Therefore, we only need to find the longest palindrome for each center and calculate its sum.

Time Complexity: O(N log N). Precomputation of prefix sums and hashes takes O(N). There are O(N) possible centers (for both odd and even length palindromes), and for each center, we perform a binary search which takes O(log N) steps. Each step of binary search involves O(1) hash lookups and comparisons.
Space Complexity: O(N). We store prefix sums, hash tables, and powers of bases, all proportional to N.
"""
from typing import List, Optional
import random

class Solution:
    def getSum(self, nums: List[int]) -> int:
        n = len(nums)

        # Initialize max_pal_sum with the maximum single element.
        # Since all nums[i] >= 1, any single element is a palindrome and contributes
        # at least to the initial max_pal_sum.
        max_pal_sum = max(nums)

        # Precompute prefix sums for O(1) subarray sum queries.
        # prefix_sums[k] stores sum(nums[0...k-1]).
        # prefix_sums has length n+1.
        prefix_sums = [0] * (n + 1)
        for i in range(n):
            prefix_sums[i+1] = prefix_sums[i] + nums[i]
        
        # Helper function to get sum of nums[start...end] (inclusive).
        def get_subarray_sum(start, end):
            if start > end: # Should not occur with valid palindrome logic
                return 0
            return prefix_sums[end+1] - prefix_sums[start]

        # Hashing parameters for rolling hash. Using two sets of (base, mod)
        # to minimize collision probability (double hashing).
        # Bases are typically small primes. Moduli are large primes.
        B1, MOD1 = 31, 1_000_000_007
        B2, MOD2 = 37, 1_000_000_009

        # Precompute powers of bases modulo their respective MODs.
        # B_pow[k] stores B^k % MOD.
        B_pow1 = [1] * (n + 1)
        B_pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            B_pow1[i] = (B_pow1[i-1] * B1) % MOD1
            B_pow2[i] = (B_pow2[i-1] * B2) % MOD2

        # Precompute forward hashes.
        # forward_hash[k] stores the hash of nums[0...k-1].
        # forward_hash has length n+1.
        forward_hash1 = [0] * (n + 1)
        forward_hash2 = [0] * (n + 1)
        for i in range(n):
            forward_hash1[i+1] = (forward_hash1[i] * B1 + nums[i]) % MOD1
            forward_hash2[i+1] = (forward_hash2[i] * B2 + nums[i]) % MOD2
        
        # Precompute reverse prefix hashes.
        # rev_prefix_hash[k] stores the hash of nums_rev[0...k-1],
        # where nums_rev is the array nums reversed: [nums[n-1], nums[n-2], ..., nums[0]].
        # This allows O(1) lookup for hashes of reversed subarrays.
        rev_prefix_hash1 = [0] * (n + 1)
        rev_prefix_hash2 = [0] * (n + 1)
        for i in range(n):
            # nums_rev[i] corresponds to nums[n-1-i] in the original array.
            rev_prefix_hash1[i+1] = (rev_prefix_hash1[i] * B1 + nums[n-1-i]) % MOD1
            rev_prefix_hash2[i+1] = (rev_prefix_hash2[i] * B2 + nums[n-1-i]) % MOD2

        # Helper function to get the forward hash of the subarray nums[start...end].
        def get_forward_sub_hash(start, end, hash_arr, B_pow_arr, MOD):
            length = end - start + 1
            # (hash(0...end) - hash(0...start-1) * B^length) % MOD
            res = (hash_arr[end+1] - (hash_arr[start] * B_pow_arr[length]) % MOD + MOD) % MOD
            return res

        # Helper function to get the hash of the reversed subarray nums[start...end].
        # This is equivalent to getting the forward hash of nums_rev[N-1-end ... N-1-start].
        def get_reverse_sub_hash(start, end, hash_arr, B_pow_arr, MOD):
            # Calculate the corresponding start and end indices in the reversed array (nums_rev).
            rev_idx_start = n - 1 - end
            rev_idx_end = n - 1 - start
            length = rev_idx_end - rev_idx_start + 1
            # (hash(0...rev_idx_end) - hash(0...rev_idx_start-1) * B^length) % MOD
            res = (hash_arr[rev_idx_end+1] - (hash_arr[rev_idx_start] * B_pow_arr[length]) % MOD + MOD) % MOD
            return res

        # Helper function to check if nums[start...end] is a palindrome using double hashing.
        def is_palindrome_hash(start, end):
            if start >= end: # Single element or empty range is always a palindrome.
                return True
            
            # Compare hashes using the first (B1, MOD1) pair.
            h_f1 = get_forward_sub_hash(start, end, forward_hash1, B_pow1, MOD1)
            h_r1 = get_reverse_sub_hash(start, end, rev_prefix_hash1, B_pow1, MOD1)
            if h_f1 != h_r1:
                return False # Mismatch, not a palindrome.
            
            # Compare hashes using the second (B2, MOD2) pair for higher confidence.
            h_f2 = get_forward_sub_hash(start, end, forward_hash2, B_pow2, MOD2)
            h_r2 = get_reverse_sub_hash(start, end, rev_prefix_hash2, B_pow2, MOD2)
            if h_f2 != h_r2:
                return False # Mismatch, not a palindrome.
            
            return True # Hashes match for both, likely a palindrome.

        # Find max palindrome sum for odd length palindromes.
        # Each index 'i' acts as the center of a potential odd-length palindrome.
        for i in range(n):
            # Binary search for the maximum radius 'k'.
            # A palindrome centered at 'i' with radius 'k' spans from index (i-k) to (i+k).
            # 'k' can range from 0 (for [nums[i]]) up to min(i, n-1-i).
            low = 0
            high = min(i, n - 1 - i)
            max_k = 0 # Stores the maximum radius found.

            while low <= high:
                mid = low + (high - low) // 2
                start_idx = i - mid
                end_idx = i + mid
                if is_palindrome_hash(start_idx, end_idx):
                    max_k = mid # This radius 'mid' forms a palindrome.
                    low = mid + 1 # Try to expand further.
                else:
                    high = mid - 1 # 'mid' is too large, shrink search range.
            
            # Calculate sum of the longest odd palindrome found for this center 'i'.
            current_pal_sum = get_subarray_sum(i - max_k, i + max_k)
            max_pal_sum = max(max_pal_sum, current_pal_sum)

        # Find max palindrome sum for even length palindromes.
        # Each pair (i, i+1) acts as the center of a potential even-length palindrome.
        for i in range(n - 1): 
            # Binary search for the maximum half-length 'k'.
            # An even palindrome centered between 'i' and 'i+1' with half-length 'k'
            # spans from index (i-k+1) to (i+k).
            # 'k' can range from 1 (for [nums[i], nums[i+1]]) up to min(i+1, n-1-(i+1)+1).
            # i.e., min(i+1, n-1-i).
            low = 1
            high = min(i + 1, n - 1 - i)
            max_k = 0 # Stores the maximum half-length found.

            while low <= high:
                mid = low + (high - low) // 2
                start_idx = i - mid + 1
                end_idx = i + mid
                if is_palindrome_hash(start_idx, end_idx):
                    max_k = mid # This half-length 'mid' forms a palindrome.
                    low = mid + 1 # Try to expand further.
                else:
                    high = mid - 1 # 'mid' is too large, shrink search range.
            
            # Only consider if an even palindrome was actually found (max_k > 0).
            if max_k > 0:
                # Calculate sum of the longest even palindrome found for this center.
                current_pal_sum = get_subarray_sum(i - max_k + 1, i + max_k)
                max_pal_sum = max(max_pal_sum, current_pal_sum)
        
        return max_pal_sum

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.getSum([10,10]) == 20
    # Example 2
    assert s.getSum([1,2,3,2,1,5,6]) == 9
    # Example 3
    assert s.getSum([7,1,2,1,7,3,4,3,4]) == 18
    # Example 4
    assert s.getSum([1,2,3,4,5]) == 5
    # Example 5
    assert s.getSum([1000]) == 1000
    # Custom test cases
    assert s.getSum([1,1,1,1,1]) == 5
    assert s.getSum([1,2,2,1]) == 6
    assert s.getSum([1,2,1,2,1]) == 7
    assert s.getSum([5,4,3,2,1]) == 5
    assert s.getSum([1,2,3,4,3,2,1]) == 16
    assert s.getSum([100, 1, 100]) == 201
    assert s.getSum([100, 100]) == 200
    assert s.getSum([1,2,1,1,2,1]) == 6

    print("All tests passed!")

