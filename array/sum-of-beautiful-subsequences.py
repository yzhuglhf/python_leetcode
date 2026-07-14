import math
from typing import List, Optional

# Define FenwickTree outside the Solution class as a global helper.
# This approach is suitable for competitive programming platforms where helper classes
# or functions can be defined globally without issues. It avoids re-defining
# the class on each call to totalBeauty, which could happen if it's inside the method
# and the method is called multiple times by the test framework.
class FenwickTree:
    def __init__(self, size: int):
        # The tree array is 1-indexed, so size + 1 is needed.
        self.tree = [0] * (size + 1)
        self.size = size
        self.MOD = 10**9 + 7

    def update(self, index: int, val: int) -> None:
        """
        Adds 'val' to the element at 'index' in the Fenwick Tree.
        index is 1-based.
        """
        while index <= self.size:
            self.tree[index] = (self.tree[index] + val) % self.MOD
            index += index & (-index) # Move to the next relevant parent node

    def query(self, index: int) -> int:
        """
        Queries the sum of elements from index 1 to 'index' (inclusive).
        index is 1-based.
        """
        res = 0
        while index > 0:
            res = (res + self.tree[index]) % self.MOD
            index -= index & (-index) # Move to the next relevant parent node
        return res

class Solution:
    def totalBeauty(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # Handle edge case where nums is empty, though constraints say n >= 1.
        if not nums:
            return 0
        
        # Determine the maximum value in nums. This helps set array sizes
        # and iteration bounds for GCDs.
        max_val = max(nums)
        
        # C[g] will store the count of strictly increasing subsequences whose
        # GCD is a multiple of g.
        # Array size is max_val + 1 to accommodate 1-based indexing for GCDs up to max_val.
        C = [0] * (max_val + 1)
        
        # --- Step 1: Calculate C[g] for all g from 1 to max_val ---
        # C[g] is computed by iterating through each possible GCD multiple 'g'.
        # For each 'g', we count strictly increasing subsequences where all elements
        # are multiples of 'g'.
        # The time complexity for this step is approximately O(N * avg_divisors * log(max_val)).
        for g in range(1, max_val + 1):
            # For each 'g', we use a fresh FenwickTree. Its size is max_val // g
            # because we will be working with values `num // g`.
            bit = FenwickTree(max_val // g)
            
            for num in nums:
                if num % g == 0:
                    # 'val_prime' is the number 'num' scaled down by 'g'.
                    # This transformation allows the Fenwick Tree to handle
                    # different GCD multiples effectively by mapping them
                    # to a smaller range.
                    val_prime = num // g
                    
                    # 'count' represents the number of new strictly increasing subsequences
                    # that can be formed ending with the current 'num', where all elements
                    # are multiples of 'g'.
                    # It includes:
                    # 1. The subsequence consisting only of `[num]` itself.
                    # 2. All subsequences (whose elements are multiples of 'g')
                    #    that end with a value strictly less than `num`, which can be extended by `num`.
                    #    `bit.query(val_prime - 1)` gives the sum of counts for values less than `val_prime`.
                    count = (1 + bit.query(val_prime - 1)) % MOD
                    
                    # Update the Fenwick Tree: we add 'count' at index 'val_prime'.
                    # This update reflects the total count of valid subsequences ending at 'val_prime'
                    # (when scaled by 'g').
                    bit.update(val_prime, count)
                    
                    # Accumulate 'count' into C[g].
                    C[g] = (C[g] + count) % MOD
        
        # E[g] will store the count of strictly increasing subsequences whose
        # GCD is *exactly* g.
        # Array size is max_val + 1.
        E = [0] * (max_val + 1)
        total_beauty = 0
        
        # --- Step 2: Calculate E[g] and total beauty using inclusion-exclusion ---
        # This step iterates 'g' downwards from max_val to 1.
        # This order ensures that when E[g] is computed, all E[g*k] (for k >= 2)
        # have already been determined.
        # The time complexity for this step is approximately O(max_val * log(max_val)).
        for g in range(max_val, 0, -1):
            # Initialize E[g] with C[g], which includes subsequences whose GCD is a multiple of g.
            E[g] = C[g]
            
            # Subtract counts of subsequences whose GCD is a *strict* multiple of g (e.g., 2g, 3g, etc.).
            # These were erroneously included in C[g] when we only checked if elements are multiples of g.
            for k in range(2, (max_val // g) + 1):
                # We subtract E[g*k] (which are already correctly computed exact counts for higher GCDs).
                # Adding MOD before taking modulo handles potential negative results from subtraction.
                E[g] = (E[g] - E[g * k] + MOD) % MOD
            
            # The beauty value for 'g' is `g * E[g]`. Add this to the total.
            total_beauty = (total_beauty + g * E[g]) % MOD
            
        return total_beauty

