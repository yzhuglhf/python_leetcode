import math
from typing import List, Optional

class Solution:
    # Class-level variables to store precomputed sieve data
    _spf_sieve = None
    _primes_list = None
    _sieve_limit = 0

    def _precompute_spf(self, limit):
        # Only recompute if the limit is larger than previously computed
        if self._spf_sieve is not None and self._sieve_limit >= limit:
            return

        self._sieve_limit = limit
        # spf_sieve[i] stores the smallest prime factor of i
        self._spf_sieve = list(range(limit + 1))
        self._primes_list = [] # List of primes up to limit

        for i in range(2, limit + 1):
            if self._spf_sieve[i] == i:  # i is prime
                self._primes_list.append(i)
                # Mark multiples of i, starting from i*i
                for multiple in range(i * i, limit + 1, i):
                    # Only update if current multiple's spf hasn't been found yet (i.e., it's i itself)
                    if self._spf_sieve[multiple] == multiple:
                        self._spf_sieve[multiple] = i

    def _get_prime_factors_optimized(self, n):
        if n == 1:
            return []
        
        factors = set() # Use a set to store unique factors
        temp_n = n

        # Factor out primes using the precomputed _primes_list
        # This loop iterates through primes p up to sqrt(temp_n) or self._sieve_limit
        for p in self._primes_list:
            if p * p > temp_n: # Optimization: stop if p exceeds sqrt(temp_n)
                break
            if temp_n % p == 0:
                factors.add(p)
                while temp_n % p == 0:
                    temp_n //= p
        
        # If temp_n is still greater than 1 after the loop, it must be a prime factor itself.
        # This handles cases where n has a prime factor larger than self._sieve_limit.
        # (e.g., n = 999999937, or n = 2 * 500000003 where 500000003 is prime and > 32000)
        if temp_n > 1:
            factors.add(temp_n)
            
        return list(factors)

    def minStable(self, nums: List[int], maxC: int) -> int:
        n = len(nums)
        
        # Precompute primes up to sqrt(MAX_NUMS_VALUE) for efficient prime factorization.
        # Max nums[i] = 10^9, so sqrt(10^9) is approx 31622.
        # Using 32000 as a slightly larger limit for sieve.
        self._precompute_spf(32000) 

        # Precompute prime factors for all numbers in nums once.
        # This list will be used repeatedly in the `check` function.
        all_factors = [self._get_prime_factors_optimized(x) for x in nums]

        # check(target_sf) returns True if it's possible to achieve a stability factor
        # of at most `target_sf` using at most `maxC` modifications.
        def check(target_sf: int) -> bool:
            # L is the minimum length of a stable subarray that we want to eliminate.
            # If stability factor is target_sf, it means no stable subarray of length L or more exists.
            L = target_sf + 1

            # Special case: If target_sf is 0 (L=1), it means no stable subarrays should exist.
            # A subarray of length 1 is stable if its element is >= 2.
            # So, to have a stability factor of 0, all elements must be modified to 1.
            if L == 1:
                cost = 0
                for x in nums:
                    if x != 1:
                        cost += 1 # Count elements that are not 1, as they need to be modified.
                return cost <= maxC

            current_cost = 0
            # last_modified_idx stores the index of the most recently modified element (or an original '1').
            # Any element at or before last_modified_idx is considered 'broken' for all primes,
            # meaning it cannot be part of an active prime-stable run.
            last_modified_idx = -1 
            
            # prime_runs maps a prime `p` to the `start_index` of the current contiguous run
            # of multiples of `p`. This run is only considered 'active' if its `start_idx`
            # is greater than `last_modified_idx`.
            prime_runs = {} 

            for i in range(n):
                val = nums[i]

                # If the current element `val` is 1, or if index `i` is less than or equal to
                # `last_modified_idx` (meaning `nums[i]` is already part of a 'broken' segment),
                # then `nums[i]` cannot extend any prime run. It acts as a break point.
                if val == 1 or i <= last_modified_idx:
                    # Update `last_modified_idx` to `i` if `val` was an original '1',
                    # extending the 'broken' region.
                    last_modified_idx = max(last_modified_idx, i) 
                    prime_runs.clear() # All current prime runs are broken by this '1' or modification
                    continue

                # Get the precomputed prime factors for nums[i].
                factors = all_factors[i] 
                new_prime_runs = {}
                violation_detected = False

                for p in factors:
                    # Get the start index for the current run of multiples of `p`.
                    # If `p` was already in `prime_runs`, it means an active run for `p` continues,
                    # so we use its existing `start_idx`. Otherwise, a new run for `p` starts at `i`.
                    start_idx = prime_runs.get(p, i)
                    
                    # Check if this prime `p` forms a problematic segment of length `L` or more.
                    if i - start_idx + 1 >= L:
                        violation_detected = True
                        break # Found a violation for prime `p`, no need to check other factors for `nums[i]`
                    
                    # If no violation for `p`, continue its run.
                    new_prime_runs[p] = start_idx
                
                if violation_detected:
                    # If a violation is detected for any prime at index `i`, we must make a modification.
                    # The greedy strategy is to modify `nums[i]` to `1`. This modification
                    # breaks all currently active prime-stable runs that would otherwise extend past `i`.
                    current_cost += 1
                    last_modified_idx = i # `nums[i]` is now effectively 1
                    prime_runs.clear() # All prime runs are broken by this modification
                else:
                    # No violation, so update `prime_runs` for the next iteration based on `new_prime_runs`.
                    prime_runs = new_prime_runs

            return current_cost <= maxC

        # Binary search for the minimum possible stability factor.
        # The stability factor can range from 0 (no stable subarrays) to `n` (the entire array is stable).
        low = 0
        high = n 
        ans = n # Initialize with the worst-case (maximum) stability factor

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                # If `mid` is achievable, try for a smaller stability factor.
                ans = mid
                high = mid - 1
            else:
                # If `mid` is not achievable, we need a larger stability factor.
                low = mid + 1
        
        return ans

