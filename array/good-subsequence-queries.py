import math
from collections import defaultdict

# Precomputation for primes, SPF, Mobius, and divisors up to MAX_VAL
MAX_VAL = 50000
spf = [0] * (MAX_VAL + 1) # Smallest Prime Factor
mu = [0] * (MAX_VAL + 1)  # Mobius function
primes = []               # List of primes
divisors_list = [[] for _ in range(MAX_VAL + 1)] # List of divisors for each number

def precompute_number_theory():
    mu[1] = 1
    for i in range(2, MAX_VAL + 1):
        if spf[i] == 0: # i is prime
            spf[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if p > spf[i] or i * p > MAX_VAL:
                break
            spf[i * p] = p
            if p == spf[i]: # p divides i, so i*p has repeated prime factor p
                mu[i * p] = 0
            else: # p does not divide i
                mu[i * p] = -mu[i]

    for i in range(1, MAX_VAL + 1):
        for j in range(i, MAX_VAL + 1, i):
            divisors_list[j].append(i)

precompute_number_theory()

class Solution:
    def countGoodSubseq(self, nums: list[int], p: int, queries: list[list[int]]) -> int:
        n = len(nums)
        
        # norm_count[y] stores the count of x/p where x % p == 0 and x/p == y
        norm_count = defaultdict(int) 
        
        # num_active_multiples[d] stores the count of distinct y's (from active_y_set) divisible by d
        # This is used for Mobius inversion sum
        num_active_multiples = defaultdict(int)
        
        # active_y_set stores the distinct y values (x/p) where norm_count[y] > 0
        active_y_set = set() 
        
        # has_coprime_pair is True if there exist y1, y2 in active_y_set (both >1) such that gcd(y1, y2) == 1
        has_coprime_pair = False
        
        # Function to check if adding a value makes has_coprime_pair True
        # Called when `has_coprime_pair` is currently False.
        # `val_to_add` is the new y value that is about to become active.
        # `num_active_multiples` reflects the state *before* `val_to_add` is added to `active_y_set`.
        def _check_coprime_on_add(val_to_add):
            nonlocal has_coprime_pair
            
            # If val_to_add is 1, it's covered by norm_count[1] > 0 condition.
            # This function is specifically for finding a pair (y1, y2) where gcd(y1, y2)=1 and y1, y2 are both >1.
            # So if val_to_add is 1, it can be skipped here for `has_coprime_pair`.
            if val_to_add == 1:
                return

            # Use Mobius inversion to count active elements coprime to `val_to_add`.
            # A value `A` is coprime to `B` iff sum_{d|A} mu[d] * (count of values in set divisible by d and also divisible by B) > 0.
            # Here we count values in `active_y_set` (excluding `val_to_add` itself) that are coprime to `val_to_add`.
            # `num_active_multiples[d]` currently holds counts for `active_y_set`.
            coprime_partners_count = 0
            for d in divisors_list[val_to_add]:
                if d <= MAX_VAL and mu[d] != 0: # Ensure d is within precomputed range
                    coprime_partners_count += mu[d] * num_active_multiples[d]
            
            if coprime_partners_count > 0:
                has_coprime_pair = True
        
        ans = 0

        # Initial population of active_y_set and num_active_multiples
        for val in nums:
            if val % p == 0:
                y = val // p
                norm_count[y] += 1
                if norm_count[y] == 1: # y becomes active for the first time
                    active_y_set.add(y)
                    # For a newly active `y`, update counts for its divisors
                    for d in divisors_list[y]:
                        if d <= MAX_VAL:
                            num_active_multiples[d] += 1

        # Determine initial has_coprime_pair status
        # This check is O(MAX_VAL * d(MAX_VAL)) in worst case, acceptable for initial setup.
        if n > 2 and norm_count[1] == 0: # Only need to check if 1 is not present
            for y1 in list(active_y_set): 
                if y1 == 1: continue # Handled by norm_count[1]
                coprime_partners_count = 0
                for d in divisors_list[y1]:
                    if d <= MAX_VAL and mu[d] != 0:
                        coprime_partners_count += mu[d] * num_active_multiples[d]
                # If y1 > 1, then gcd(y1, y1) = y1 != 1. So coprime_partners_count correctly counts partners other than y1 itself.
                if coprime_partners_count > 0:
                    has_coprime_pair = True
                    break

        # Check initial state for good subsequence
        if norm_count[1] > 0:
            ans += 1
        elif n > 2 and has_coprime_pair:
            ans += 1
            
        for indi, vali in queries:
            old_val = nums[indi]
            nums[indi] = vali
            
            # --- Remove old_val effects ---
            if old_val % p == 0:
                y_old = old_val // p
                norm_count[y_old] -= 1
                
                if norm_count[y_old] == 0: # y_old becomes inactive
                    active_y_set.remove(y_old)
                    for d in divisors_list[y_old]:
                        if d <= MAX_VAL:
                            num_active_multiples[d] -= 1
                    
                    # If has_coprime_pair was True, it might become False.
                    # This is the most expensive recomputation. Only do if it could actually become false
                    # and if we still need the flag (i.e. norm_count[1] is 0 and there are enough other elements).
                    if has_coprime_pair and norm_count[1] == 0 and len(active_y_set) >= 2:
                        has_coprime_pair = False # Reset and re-evaluate
                        for y1 in list(active_y_set):
                            if y1 == 1: continue
                            coprime_partners_count = 0
                            for d in divisors_list[y1]:
                                if d <= MAX_VAL and mu[d] != 0:
                                    coprime_partners_count += mu[d] * num_active_multiples[d]
                            if coprime_partners_count > 0:
                                has_coprime_pair = True
                                break
            
            # --- Add new_val effects ---
            if vali % p == 0:
                y_new = vali // p
                norm_count[y_new] += 1
                
                if norm_count[y_new] == 1: # y_new becomes active
                    # Before adding to num_active_multiples, check if y_new forms a coprime pair with existing ones
                    # Only check if has_coprime_pair is currently False and we have at least one existing partner candidate.
                    if not has_coprime_pair and len(active_y_set) >= 1: # len >= 1 means potentially a pair (y_new, existing_y)
                        _check_coprime_on_add(y_new) 
                    
                    active_y_set.add(y_new)
                    for d in divisors_list[y_new]:
                        if d <= MAX_VAL:
                            num_active_multiples[d] += 1
            
            # --- Determine current_is_good status ---
            current_is_good = False
            if norm_count[1] > 0: # Condition 1: p itself is in nums
                current_is_good = True
            elif n > 2 and len(active_y_set) >= 2: # Condition 2: n > 2 AND enough active y's AND a coprime pair exists
                if has_coprime_pair:
                    current_is_good = True
            
            if current_is_good:
                ans += 1
                
        return ans

