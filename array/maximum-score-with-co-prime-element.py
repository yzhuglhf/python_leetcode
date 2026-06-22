"""
Maximum Score with Co-Prime Element
Difficulty: Hard

Description:
This problem asks us to maximize a score defined as `selectedValue - modificationCost`. We can modify elements in `nums` to any value up to `maxVal`, costing 1 per change. The `selectedValue` is the final value of one chosen element `nums[i]`, which must be co-prime with all other elements `nums[j]` (after their potential modifications). The key insight is that `selectedValue` itself can be either a value within `[1, maxVal]` (if `nums[i]` is changed to it or was already it) OR an original `nums[k]` that is greater than `maxVal` (if `nums[i]` is chosen to be `nums[k]` and not modified).

Example:
Input: nums = [3,4,6], maxVal = 5
Output: 4
Explanation: We choose `selectedValue = 5`. Since 5 is not in `nums`, we must change one element to 5. Let's say we change `nums[2]` from 6 to 5 (cost 1). Now `nums` is effectively `[3,4,5]`. `selectedValue = 5` is co-prime with `3` and `4`. The total `modificationCost` is 1. The score is `5 - 1 = 4`.

Approach:
The problem can be solved by iterating through all possible `selectedValue` candidates and calculating the minimum `modificationCost` for each. There are two categories for `selectedValue`:
1.  `selectedValue` is `X`, where `1 <= X <= maxVal`.
2.  `selectedValue` is `Y`, where `Y` is an original element from `nums` and `Y > maxVal`. In this case, `Y` is chosen not to be modified.

For each `selectedValue` candidate, we need to calculate `modificationCost`. This cost is the number of elements in the *original* `nums` array (excluding the chosen `nums[i]`) that are not co-prime with `selectedValue`. This can be efficiently computed using the inclusion-exclusion principle based on prime factors.

Precomputation Steps:
1.  **Sieve of Eratosthenes**: Precompute the smallest prime factor (SPF) for all numbers up to `U = 10^5` (the maximum possible value of `nums[i]` or `maxVal`). This allows fast prime factorization. `O(U log log U)`.
2.  **Counts**: Store the frequency of each number in the input `nums` array in `counts[x]`. `O(len(nums))`.
3.  **Frequency of Multiples**: Compute `freq_multiples[d]`, which is the sum of `counts[k]` for all `k` that are multiples of `d` (up to `U`). This helps in the inclusion-exclusion calculation. `O(U log U)`.

Main Logic:
We iterate `possible_val` from 1 to `maxVal` (Category 1).
For each `possible_val`:
    a.  Find its distinct prime factors using the precomputed `spf` array.
    b.  Calculate `total_non_coprime_count` for `possible_val` using the inclusion-exclusion principle and `freq_multiples`. This count represents how many elements in the original `nums` array are *not* co-prime with `possible_val`.
    c.  Determine the `current_modification_cost`:
        i.  If `possible_val` already exists in `nums` (`counts[possible_val] > 0`): We can choose an instance of `possible_val` as `nums[i]` and not change it. If `possible_val > 1`, this instance of `possible_val` would have been counted in `total_non_coprime_count` (as `gcd(possible_val, possible_val) = possible_val != 1`), so we subtract 1 from `total_non_coprime_count`.
        ii. If `possible_val` does not exist in `nums` (`counts[possible_val] == 0`): We must change some `nums[i]` to `possible_val`, incurring a cost of 1. So, `current_modification_cost = 1 + total_non_coprime_count`.
    d.  Update `max_score = max(max_score, possible_val - current_modification_cost)`.

Additionally, we iterate through distinct `original_val` from `nums` that are `> maxVal` (Category 2).
For each such `original_val`:
    a.  We must choose this `original_val` as `selectedValue` and *not* modify it (cost 0 for `nums[i]`).
    b.  Calculate `total_non_coprime_count` for `original_val`.
    c.  Since `original_val > maxVal >= 1`, it's not co-prime with itself. One instance of `original_val` (the chosen `nums[i]`) does not contribute to modification cost. So, `current_modification_cost = total_non_coprime_count - 1`.
    d.  Update `max_score = max(max_score, original_val - current_modification_cost)`.

The maximum score found across all candidates is the result.

Time Complexity: O(U log U + (maxVal + N_distinct) * (log U + 2^k_max)), where U = 10^5, N_distinct is the number of distinct elements in `nums`, and k_max is the maximum number of distinct prime factors for a number up to U (k_max <= 6 for U=10^5). This simplifies to roughly O(U log U + U * 2^k_max).
Space Complexity: O(U) for `spf`, `counts`, and `freq_multiples` arrays.
"""
import math
from typing import List

class Solution:
    def maxScore(self, nums: List[int], maxVal: int) -> int:
        U = 100000  # Max possible value for nums[i] or maxVal based on constraints

        # Step 1: Precompute SPF (Smallest Prime Factor) using Sieve
        # spf[i] will store the smallest prime factor of i
        # For prime numbers, spf[i] will be i
        spf = list(range(U + 1))
        for i in range(2, int(math.sqrt(U)) + 1):
            if spf[i] == i:  # i is prime
                # Mark multiples of i, starting from i*i
                for multiple in range(i * i, U + 1, i):
                    if spf[multiple] == multiple:  # Only update if not already marked by a smaller prime
                        spf[multiple] = i

        # Step 2: Compute counts of each number in nums
        # `counts[x]` stores the frequency of number x in the input array `nums`.
        counts = [0] * (U + 1)
        for num in nums:
            # All nums[i] are <= U according to constraints (1 <= nums[i] <= 10^5)
            counts[num] += 1

        # Step 3: Compute freq_multiples[d]
        # `freq_multiples[d]` stores the total count of numbers in `nums` that are multiples of `d`.
        freq_multiples = [0] * (U + 1)
        for d in range(1, U + 1):
            for m in range(d, U + 1, d):
                freq_multiples[d] += counts[m]

        max_score = -float('inf')

        # Helper function to get distinct prime factors of a number `val`
        def get_distinct_prime_factors(val: int) -> List[int]:
            distinct_primes = []
            temp = val
            if temp == 1:
                return distinct_primes  # 1 has no prime factors
            while temp > 1:
                p = spf[temp]
                distinct_primes.append(p)
                while temp % p == 0:
                    temp //= p
            return distinct_primes

        # Helper function to calculate total_non_coprime_count for a given value `v`
        # This count represents how many elements in the *original* `nums` array are not co-prime with `v`.
        def calculate_total_non_coprime_count(val: int) -> int:
            if val == 1:
                return 0  # 1 is co-prime with all integers

            distinct_primes = get_distinct_prime_factors(val)
            
            non_coprime_count = 0
            num_distinct_primes = len(distinct_primes)

            # Iterate through all non-empty subsets of distinct_primes
            # This uses the inclusion-exclusion principle
            for i in range(1, 1 << num_distinct_primes):
                product = 1
                set_bits_count = 0  # Number of primes in current subset
                for j in range(num_distinct_primes):
                    if (i >> j) & 1:  # If j-th prime is in the current subset
                        product *= distinct_primes[j]
                        set_bits_count += 1
                
                # For `val <= U`, the `product` of its distinct prime factors (or any subset)
                # will also be `<= U`. So `freq_multiples[product]` is always a safe access.
                if set_bits_count % 2 == 1:  # Odd number of primes in subset
                    non_coprime_count += freq_multiples[product]
                else:  # Even number of primes in subset
                    non_coprime_count -= freq_multiples[product]
            return non_coprime_count

        # Case 1: The `selectedValue` (final value of nums[i]) is `X`, where 1 <= X <= maxVal.
        # This means `nums[i]` is either changed to X (cost 1) or was already X (cost 0).
        for possible_val in range(1, maxVal + 1):
            total_non_coprime_count = calculate_total_non_coprime_count(possible_val)
            
            current_modification_cost = total_non_coprime_count
            
            if counts[possible_val] > 0:  # If `possible_val` exists in original `nums`
                # One instance of `possible_val` can be chosen as `nums[i]` and not modified.
                # If `possible_val > 1`, this chosen instance would have been counted in `total_non_coprime_count`
                # (because `gcd(possible_val, possible_val) = possible_val != 1`).
                # We subtract 1 to reflect that it's not modified.
                if possible_val > 1:
                    current_modification_cost -= 1 
                # If `possible_val == 1`, `total_non_coprime_count` is 0, so no adjustment needed.
            else:  # `possible_val` does not exist in original `nums`
                # We must change some `nums[k]` to `possible_val`, which costs 1.
                current_modification_cost += 1
            
            max_score = max(max_score, possible_val - current_modification_cost)

        # Case 2: The `selectedValue` is `Y`, where `Y` is an original `nums[k]` and `Y > maxVal`.
        # In this scenario, we must choose `nums[i]` to be this `Y` and *not* modify it (cost 0 for nums[i]).
        # All other elements in `nums` (original values) that are not co-prime with `Y` must be modified.
        
        # To avoid redundant calculations for duplicate original values, we iterate over a set.
        distinct_nums_greater_than_maxVal = set(num for num in nums if num > maxVal)

        for original_val in distinct_nums_greater_than_maxVal:
            # We choose this `original_val` as our `selectedValue`. It is not modified.
            
            total_non_coprime_count = calculate_total_non_coprime_count(original_val)
            
            current_modification_cost = total_non_coprime_count
            
            # Since `original_val > maxVal`, and `maxVal >= 1`, `original_val` is guaranteed to be `> 1`.
            # `gcd(original_val, original_val) = original_val != 1`.
            # `total_non_coprime_count` includes one instance of `original_val` (if `counts[original_val] > 0`).
            # We explicitly choose one `original_val` from `nums` *not* to modify, so we subtract 1.
            current_modification_cost -= 1 
            
            max_score = max(max_score, original_val - current_modification_cost)

        return max_score


if __name__ == "__main__":
    s = Solution()

    # Example 1:
    nums1 = [3, 4, 6]
    maxVal1 = 5
    expected1 = 4
    result1 = s.maxScore(nums1, maxVal1)
    print(f"Input: nums={nums1}, maxVal={maxVal1}, Output: {result1}, Expected: {expected1}")
    assert result1 == expected1, f"Test 1 Failed: {result1}"

    # Example 2:
    nums2 = [1, 2, 3]
    maxVal2 = 4
    expected2 = 3
    result2 = s.maxScore(nums2, maxVal2)
    print(f"Input: nums={nums2}, maxVal={maxVal2}, Output: {result2}, Expected: {expected2}")
    assert result2 == expected2, f"Test 2 Failed: {result2}"

    # Example 3:
    nums3 = [2, 2]
    maxVal3 = 1
    expected3 = 1
    result3 = s.maxScore(nums3, maxVal3)
    print(f"Input: nums={nums3}, maxVal={maxVal3}, Output: {result3}, Expected: {expected3}")
    assert result3 == expected3, f"Test 3 Failed: {result3}"

    # Custom Test Case 1: All elements are already co-prime, choose maxVal
    nums4 = [7, 11, 13]
    maxVal4 = 17
    expected4 = 17 
    result4 = s.maxScore(nums4, maxVal4)
    print(f"Input: nums={nums4}, maxVal={maxVal4}, Output: {result4}, Expected: {expected4}")
    assert result4 == expected4, f"Test 4 Failed: {result4}"

    # Custom Test Case 2: nums has large values, maxVal is small
    nums5 = [100000, 99999]
    maxVal5 = 2
    expected5 = 100000
    result5 = s.maxScore(nums5, maxVal5)
    print(f"Input: nums={nums5}, maxVal={maxVal5}, Output: {result5}, Expected: {expected5}")
    assert result5 == expected5, f"Test 5 Failed: {result5}"

    # Custom Test Case 3: All same values, large numbers.
    nums6 = [77, 77, 77]
    maxVal6 = 5
    expected6 = 75
    result6 = s.maxScore(nums6, maxVal6)
    print(f"Input: nums={nums6}, maxVal={maxVal6}, Output: {result6}, Expected: {expected6}")
    assert result6 == expected6, f"Test 6 Failed: {result6}"

    # Custom Test Case 4: Single element.
    nums7 = [10]
    maxVal7 = 3
    expected7 = 10
    result7 = s.maxScore(nums7, maxVal7)
    print(f"Input: nums={nums7}, maxVal={maxVal7}, Output: {result7}, Expected: {expected7}")
    assert result7 == expected7, f"Test 7 Failed: {result7}"

    print("\nAll tests passed!")
