"""
Minimum Operations to Transform Array into Alternating Prime
Difficulty: Medium

Description:
This problem asks for the minimum operations to transform a given integer array into an alternating prime array. This means elements at even indices must be prime numbers, and elements at odd indices must be non-prime numbers. An operation consists of incrementing any element by 1, and we aim to minimize the total operations.

Example:
Input: nums = [1,2,3,4]
Output: 3

Approach:
The key insight is that the operations on each element are independent of others. Thus, we can calculate the minimum operations needed for each element to satisfy its alternating prime condition and sum these individual costs. To efficiently determine primality and find the nearest prime/non-prime, we precompute this information up to a certain limit (determined by the maximum possible value of `nums[i]` plus a small offset) using the Sieve of Eratosthenes.

First, we define a `SIEVE_LIMIT` slightly larger than the maximum possible `nums[i]` (10^5) to account for needing to find the next prime or non-prime value. We then run the Sieve of Eratosthenes to populate a boolean array `_is_prime`, marking each number up to `SIEVE_LIMIT` as prime or non-prime. After the sieve, we precompute two auxiliary arrays: `_next_prime[k]` stores the smallest prime number greater than or equal to `k`, and `_next_non_prime[k]` stores the smallest non-prime number greater than or equal to `k`. These are filled by iterating backward from `SIEVE_LIMIT` down to 0, efficiently propagating the next prime/non-prime information. Finally, we iterate through the input array `nums`. For each element `nums[i]`: if `i` is even, we calculate `_next_prime[nums[i]] - nums[i]`; if `i` is odd, we calculate `_next_non_prime[nums[i]] - nums[i]`. The sum of these differences gives the total minimum operations. This precomputation is cached at the class level to run only once.

Time Complexity: O(M * log(log M) + N), where M is the sieve limit (approx. 10^5) and N is the length of `nums`. The sieve takes O(M * log(log M)), precomputing `_next_prime` and `_next_non_prime` takes O(M), and iterating through `nums` takes O(N).
Space Complexity: O(M), for storing the `_is_prime` array and the `_next_prime` and `_next_non_prime` arrays.
"""
from typing import List, Optional

class Solution:
    # Sieve limit based on problem constraints: max nums[i] is 10^5.
    # The next prime after 10^5 is 100003. We need to cover this, so 100005 is a safe upper bound.
    SIEVE_LIMIT = 100005 
    
    # Class-level caches for precomputed data to avoid re-calculating for multiple test cases
    _is_prime: List[bool] = []
    _next_prime: List[int] = []
    _next_non_prime: List[int] = []

    def _precompute_primes(self):
        """
        Precomputes prime numbers using Sieve of Eratosthenes and
        then fills _next_prime and _next_non_prime arrays.
        This method ensures it runs only once.
        """
        if self._is_prime:  # Check if data has already been computed
            return

        # Step 1: Sieve of Eratosthenes
        self._is_prime = [True] * (self.SIEVE_LIMIT + 1)
        self._is_prime[0] = self._is_prime[1] = False  # 0 and 1 are not prime
        for p in range(2, int(self.SIEVE_LIMIT**0.5) + 1):
            if self._is_prime[p]:
                for multiple in range(p*p, self.SIEVE_LIMIT + 1, p):
                    self._is_prime[multiple] = False
        
        # Step 2: Precompute _next_prime and _next_non_prime arrays
        # _next_prime[k] = smallest prime >= k
        # _next_non_prime[k] = smallest non-prime >= k
        self._next_prime = [0] * (self.SIEVE_LIMIT + 1)
        self._next_non_prime = [0] * (self.SIEVE_LIMIT + 1)
        
        last_prime_found = -1        # Stores the last prime number encountered during backward iteration
        last_non_prime_found = -1    # Stores the last non-prime number encountered

        # Iterate backward to fill these arrays efficiently
        # For k, if it's prime, then _next_prime[k] is k. Else, it's the same as _next_prime[k+1].
        # Similar logic for _next_non_prime.
        for k in range(self.SIEVE_LIMIT, -1, -1):
            if self._is_prime[k]:
                last_prime_found = k
            else:
                last_non_prime_found = k
            
            # These values will propagate correctly down to 0 and 1
            self._next_prime[k] = last_prime_found
            self._next_non_prime[k] = last_non_prime_found

    def minOperations(self, nums: List[int]) -> int:
        self._precompute_primes()  # Ensure precomputation runs only once

        total_operations = 0
        for i, val in enumerate(nums):
            if i % 2 == 0:  # Even index: must be prime
                # Find the smallest prime target_val >= val
                target_val = self._next_prime[val]
                total_operations += (target_val - val)
            else:  # Odd index: must be non-prime
                # Find the smallest non-prime target_val >= val
                target_val = self._next_non_prime[val]
                total_operations += (target_val - val)
        
        return total_operations

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.minOperations([1,2,3,4]) == 3, "Example 1 Failed"
    # Example 2
    assert s.minOperations([5,6,7,8]) == 0, "Example 2 Failed"
    # Example 3
    assert s.minOperations([4,4]) == 1, "Example 3 Failed"
    
    # Custom test cases
    assert s.minOperations([1]) == 1, "Single element even index 1 -> prime" # 1 to 2
    assert s.minOperations([2]) == 0, "Single element even index 2 -> prime" # 2 is prime
    assert s.minOperations([3]) == 0, "Single element even index 3 -> prime" # 3 is prime
    assert s.minOperations([4]) == 1, "Single element even index 4 -> prime" # 4 to 5
    
    assert s.minOperations([2, 2]) == 2, "Even index 2 (prime) ok, Odd index 2 (prime) -> non-prime (4)" # 0 + (4-2) = 2
    assert s.minOperations([2, 3]) == 1, "Even index 2 (prime) ok, Odd index 3 (prime) -> non-prime (4)" # 0 + (4-3) = 1
    assert s.minOperations([100000]) == 3, "Largest non-prime to next prime" # 100000 to 100003
    assert s.minOperations([99989]) == 0, "Largest prime is prime" # 99989 is prime
    assert s.minOperations([99989, 99989]) == 1, "Largest prime to non-prime" # 0 + (99990 - 99989) = 1
    
    print("All tests passed!")