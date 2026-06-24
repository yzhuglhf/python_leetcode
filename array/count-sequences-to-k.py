"""
Count Sequences to K
Difficulty: Hard

Description:
This problem asks us to find the number of distinct sequences of operations (multiply, divide, or leave unchanged) on an initial value of 1, using elements from a given array `nums`, such that the final value exactly equals a target `k`. The constraints (`nums.length` up to 19, `nums[i]` up to 6) suggest a dynamic programming approach where the state efficiently tracks the current rational value.

Example:
Input: nums = [2,3,2], k = 6
Output: 2
Explanation:
1. (Multiply by 2) -> (Multiply by 3) -> (Leave unchanged) results in 1 * 2 * 3 * 1 = 6.
2. (Leave unchanged) -> (Multiply by 3) -> (Multiply by 2) results in 1 * 1 * 3 * 2 = 6.

Approach:
The key insight is to represent the current rational value `val` not as a floating-point number, but by its prime factorization. Since all `nums[i]` are integers between 1 and 6, their only prime factors are 2, 3, and 5. Consequently, any `val` formed will be of the form `2^e2 * 3^e3 * 5^e5`, where `e2, e3, e5` are integers (positive for factors in the numerator, negative for factors in the denominator). The initial value `val = 1` corresponds to `(e2=0, e3=0, e5=0)`. The target `k` is also factorized into `(target_e2, target_e3, target_e5)`. If `k` contains any prime factor other than 2, 3, or 5, or if its required exponents fall outside the possible range, the answer is immediately 0.

We employ a recursive depth-first search (DFS) with memoization (dynamic programming) to count sequences. The state of our DP is `(index, current_e2, current_e3, current_e5)`, representing the number of ways to reach the target exponents from `index` onwards, given the current exponents `(current_e2, current_e3, current_e5)`.
For each `nums[idx]` at the current `index`:
1. Pre-factorize `nums[idx]` into its prime exponents `(n_e2, n_e3, n_e5)`.
2. Consider "Multiply": Recursively call DP with `(index + 1, current_e2 + n_e2, current_e3 + n_e3, current_e5 + n_e5)`.
3. Consider "Divide": Recursively call DP with `(index + 1, current_e2 - n_e2, current_e3 - n_e3, current_e5 - n_e5)`.
4. Consider "Leave unchanged": Recursively call DP with `(index + 1, current_e2, current_e3, current_e5)`.
The total count for the current state is the sum of results from these three actions.

The base case for the recursion is when `index == len(nums)`. At this point, if the `current_e2, current_e3, current_e5` match the `target_e2, target_e3, target_e5`, we return 1 (one valid sequence found); otherwise, 0. Exponent ranges are pre-calculated based on `nums.length` (N=19) and `max(nums[i])` (6): `e2` ranges from -38 to 38, `e3` from -19 to 19, and `e5` from -19 to 19. Intermediate exponent values that fall outside these ranges are pruned, as they cannot lead to a valid target.

Time Complexity: O(N * MAX_EXP2 * MAX_EXP3 * MAX_EXP5)
Given `N <= 19`, `MAX_EXP2 = 38` (for prime 2), `MAX_EXP3 = 19` (for prime 3), `MAX_EXP5 = 19` (for prime 5), the number of states is approximately `(N+1) * (2*MAX_EXP2+1) * (2*MAX_EXP3+1) * (2*MAX_EXP5+1) = 20 * 77 * 39 * 39 ≈ 2.34 million`. Each state computation involves a few arithmetic operations and hash map lookups/insertions, taking nearly constant time. This results in a total operation count in the low millions, which is efficient enough for the given time limits.
Space Complexity: O(N * MAX_EXP2 * MAX_EXP3 * MAX_EXP5) for storing the memoization table.
"""
from typing import List, Optional
import collections

class Solution:
    def countSequences(self, nums: List[int], k: int) -> int:
        
        # Max absolute exponent bounds for primes 2, 3, and 5.
        # These are derived from nums.length <= 19 and nums[i] <= 6.
        # For prime 2: max_2_exp(4) = 2. Max change is 2. So, 19 * 2 = 38. Range [-38, 38].
        # For prime 3: max_3_exp(3) = 1 or max_3_exp(6) = 1. Max change is 1. So, 19 * 1 = 19. Range [-19, 19].
        # For prime 5: max_5_exp(5) = 1. Max change is 1. So, 19 * 1 = 19. Range [-19, 19].
        
        MAX_EXP2_ABS = 38
        MAX_EXP3_ABS = 19
        MAX_EXP5_ABS = 19
        
        # Pre-factorize nums[i] values (1 to 6) for quick lookup during DP transitions.
        # Each entry stores a tuple (exp2, exp3, exp5).
        factorizations = {}
        for num_val in range(1, 7):
            exp2, exp3, exp5 = 0, 0, 0
            temp_n = num_val
            
            # Count exponent for 2
            while temp_n > 0 and temp_n % 2 == 0:
                exp2 += 1
                temp_n //= 2
            # Count exponent for 3
            while temp_n > 0 and temp_n % 3 == 0:
                exp3 += 1
                temp_n //= 3
            # Count exponent for 5
            while temp_n > 0 and temp_n % 5 == 0:
                exp5 += 1
                temp_n //= 5
            
            factorizations[num_val] = (exp2, exp3, exp5)

        # Factorize target k. If k contains prime factors other than 2, 3, 5,
        # it's impossible to form, so return 0.
        target_exp2, target_exp3, target_exp5 = 0, 0, 0
        temp_k = k
        
        while temp_k > 0 and temp_k % 2 == 0:
            target_exp2 += 1
            temp_k //= 2
        while temp_k > 0 and temp_k % 3 == 0:
            target_exp3 += 1
            temp_k //= 3
        while temp_k > 0 and temp_k % 5 == 0:
            target_exp5 += 1
            temp_k //= 5
            
        if temp_k != 1:
            # `k` has prime factors not in {2, 3, 5}. Cannot be formed by `nums[i]`.
            return 0
            
        # If target exponents are outside the maximum possible range achievable by `nums`, return 0.
        if not (-MAX_EXP2_ABS <= target_exp2 <= MAX_EXP2_ABS and
                -MAX_EXP3_ABS <= target_exp3 <= MAX_EXP3_ABS and
                -MAX_EXP5_ABS <= target_exp5 <= MAX_EXP5_ABS):
            return 0
            
        # Memoization dictionary to store results of dp states.
        # Key: (index, current_exp2, current_exp3, current_exp5)
        # Value: count of sequences
        memo = {}

        def dp(idx, current_exp2, current_exp3, current_exp5):
            # Base case: All elements processed
            if idx == len(nums):
                # Check if the final exponents match the target exponents
                if (current_exp2 == target_exp2 and
                    current_exp3 == target_exp3 and
                    current_exp5 == target_exp5):
                    return 1  # Found one valid sequence
                return 0  # No match

            # Memoization check: return cached result if available
            state = (idx, current_exp2, current_exp3, current_exp5)
            if state in memo:
                return memo[state]

            count = 0
            num_val = nums[idx]
            n_exp2, n_exp3, n_exp5 = factorizations[num_val]

            # Try all three actions: Multiply, Divide, Leave unchanged
            
            # Action 1: Multiply val by nums[idx]
            new_exp2_mult = current_exp2 + n_exp2
            new_exp3_mult = current_exp3 + n_exp3
            new_exp5_mult = current_exp5 + n_exp5
            
            # Optimization: Prune if exponents go out of reasonable bounds.
            # Paths exceeding these bounds cannot reach the target K (which is within bounds).
            if (-MAX_EXP2_ABS <= new_exp2_mult <= MAX_EXP2_ABS and
                -MAX_EXP3_ABS <= new_exp3_mult <= MAX_EXP3_ABS and
                -MAX_EXP5_ABS <= new_exp5_mult <= MAX_EXP5_ABS):
                count += dp(idx + 1, new_exp2_mult, new_exp3_mult, new_exp5_mult)

            # Action 2: Divide val by nums[idx]
            new_exp2_div = current_exp2 - n_exp2
            new_exp3_div = current_exp3 - n_exp3
            new_exp5_div = current_exp5 - n_exp5
            
            if (-MAX_EXP2_ABS <= new_exp2_div <= MAX_EXP2_ABS and
                -MAX_EXP3_ABS <= new_exp3_div <= MAX_EXP3_ABS and
                -MAX_EXP5_ABS <= new_exp5_div <= MAX_EXP5_ABS):
                count += dp(idx + 1, new_exp2_div, new_exp3_div, new_exp5_div)

            # Action 3: Leave val unchanged
            # The current_exp values are always within bounds when this function is called,
            # so no explicit bounds check is needed here.
            count += dp(idx + 1, current_exp2, current_exp3, current_exp5)
            
            # Store the computed result in memoization table
            memo[state] = count
            return count

        # Initial call: val starts at 1, which corresponds to (exp2=0, exp3=0, exp5=0)
        return dp(0, 0, 0, 0)

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.countSequences(nums = [2,3,2], k = 6) == 2, f"Test Case 1 Failed: Expected 2, Got {s.countSequences(nums = [2,3,2], k = 6)}"

    # Example 2
    assert s.countSequences(nums = [4,6,3], k = 2) == 2, f"Test Case 2 Failed: Expected 2, Got {s.countSequences(nums = [4,6,3], k = 2)}"

    # Example 3
    assert s.countSequences(nums = [1,5], k = 1) == 3, f"Test Case 3 Failed: Expected 3, Got {s.countSequences(nums = [1,5], k = 1)}"

    # Custom Test Cases
    # Single element, target matches
    assert s.countSequences(nums = [2], k = 2) == 1, f"Custom Test Case 4 Failed: Expected 1, Got {s.countSequences(nums = [2], k = 2)}"
    # Single element, target is 1 (leave unchanged)
    assert s.countSequences(nums = [2], k = 1) == 1, f"Custom Test Case 5 Failed: Expected 1, Got {s.countSequences(nums = [2], k = 1)}"
    # Single element, target is 1 (nums[i] is 1)
    assert s.countSequences(nums = [1], k = 1) == 3, f"Custom Test Case 6 Failed: Expected 3, Got {s.countSequences(nums = [1], k = 1)}"
    # Target K has other prime factors (e.g., 7)
    assert s.countSequences(nums = [2], k = 7) == 0, f"Custom Test Case 7 Failed: Expected 0, Got {s.countSequences(nums = [2], k = 7)}"
    # Target K's exponent for prime 2 is too large to be formed (2^39 is > MAX_EXP2_ABS)
    assert s.countSequences(nums = [4], k = 2**39) == 0, f"Custom Test Case 8 Failed: Expected 0, Got {s.countSequences(nums = [4], k = 2**39)}"
    # Max N and small numbers, all multiply
    assert s.countSequences(nums = [2] * 19, k = 2**19) == 1, f"Custom Test Case 9 Failed: Expected 1, Got {s.countSequences(nums = [2] * 19, k = 2**19)}"
    # Max N, all 1s, k=1. Each 1 has 3 choices, all leading to same state.
    assert s.countSequences(nums = [1] * 19, k = 1) == 3**19, f"Custom Test Case 10 Failed: Expected {3**19}, Got {s.countSequences(nums = [1] * 19, k = 1)}"
    
    print("All tests passed!")

