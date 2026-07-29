"""
Minimum Cost to Make Two Binary Strings Equal
Difficulty: Medium

Description:
This problem asks for the minimum cost to make two binary strings, s and t, equal using three types of operations: flipping a bit (cost `flipCost`), swapping bits within a string (e.g., s[i] with s[j], cost `swapCost`), or swapping a bit between strings at the same index (s[i] with t[i], cost `crossCost`). The key is to analyze how each operation affects the counts of mismatches. Mismatches can be of two types: s[i]=='0', t[i]=='1' (let's call this '01' type) or s[i]=='1', t[i]=='0' (let's call this '10' type). The goal is to reduce both `num_01` and `num_10` to zero with minimum total cost.

Example:
Input: s = "01000", t = "10111", flipCost = 10, swapCost = 2, crossCost = 2
Output: 16
Explanation:
Initially, we identify mismatches:
- s[0]='0', t[0]='1' (01 type)
- s[1]='1', t[1]='0' (10 type)
- s[2]='0', t[2]='1' (01 type)
- s[3]='0', t[3]='1' (01 type)
- s[4]='0', t[4]='1' (01 type)
So, we have `num_01 = 4` and `num_10 = 1`.

Consider two main strategies:
1.  **Flip all mismatches**: (4+1) * flipCost = 5 * 10 = 50.
2.  **Utilize swaps**:
    a.  Pair up one '01' and one '10' mismatch using an intra-string swap. This costs `swapCost = 2` and fixes two mismatches. `min(num_01, num_10) = min(4,1) = 1` such operation. Cost so far: 1 * 2 = 2.
        Remaining mismatches: `num_01 = 3`, `num_10 = 0`. So, 3 mismatches of '01' type are left.
    b.  Handle the 3 remaining '01' mismatches.
        i.  Flip all 3: 3 * flipCost = 3 * 10 = 30.
        ii. Use cross-swaps to enable more intra-string swaps: For two '01' mismatches, we can cross-swap one to make it '10' (cost `crossCost = 2`), then use an intra-string swap to fix the resulting '01' and '10' pair (cost `swapCost = 2`). Total cost for two same-type mismatches = `crossCost + swapCost = 2 + 2 = 4`.
            For 3 remaining '01's: We can fix one pair for `4` (`crossCost + swapCost`), leaving 1 '01' mismatch. This last '01' must be flipped for `flipCost = 10`. Total cost: `4 + 10 = 14`.
        Choosing the minimum between (i) and (ii) for the remaining 3 mismatches: `min(30, 14) = 14`.
    Total cost for strategy 2: `2 (from step 2a) + 14 (from step 2b) = 16`.
The minimum overall cost is `min(50, 16) = 16`.

Approach:
The solution involves counting the initial types of mismatches and then considering the most cost-effective ways to resolve them.
First, iterate through strings `s` and `t` to count `num_01` (positions `i` where `s[i]=='0'` and `t[i]=='1'`) and `num_10` (positions `i` where `s[i]=='1'` and `t[i]=='0'`).

We then calculate the minimum cost by evaluating two primary strategies:

1.  **Strategy A: Resolve all mismatches using only `flipCost` operations.**
    The total number of mismatches is `num_01 + num_10`.
    Cost = `(num_01 + num_10) * flipCost`.

2.  **Strategy B: Resolve mismatches by combining `swapCost`, `crossCost`, and `flipCost` operations.**
    a.  **Pairing opposite mismatches**: Perform `min(num_01, num_10)` intra-string swap operations. Each operation uses `swapCost` to fix one '01' mismatch and one '10' mismatch. This reduces both `num_01` and `num_10` by `min(num_01, num_10)`.
        Current cost: `min(num_01, num_10) * swapCost`.
        Remaining mismatches `k_remaining = abs(num_01 - num_10)`. These `k_remaining` mismatches are all of the same type.

    b.  **Resolving remaining same-type mismatches**: For these `k_remaining` mismatches, consider two sub-options:
        i.  **Flip all remaining**: Cost = `k_remaining * flipCost`.
        ii. **Convert and swap**: For every two same-type mismatches (e.g., two '01's), one can be converted to the opposite type ('10') using `crossCost`. Then, the resulting '01' and '10' can be fixed with an intra-string swap using `swapCost`. This combination costs `crossCost + swapCost` to fix two same-type mismatches. Any odd remaining mismatch (if `k_remaining` is odd) must be fixed by a `flipCost`.
            Cost = `(k_remaining // 2) * (crossCost + swapCost) + (k_remaining % 2) * flipCost`.
        Choose the minimum cost between these two sub-options for `k_remaining` mismatches.

    The total cost for Strategy B is the sum of costs from step (a) and the chosen minimum from step (b).

The final answer is the minimum of the costs calculated by Strategy A and Strategy B.

Time Complexity: O(N) because we iterate through the strings once to count mismatches.
Space Complexity: O(1) as we only store a few counters.
"""
from typing import List, Optional

class Solution:
    def minimumCost(self, s: str, t: str, flipCost: int, swapCost: int, crossCost: int) -> int:
        n = len(s)
        
        num_01 = 0  # Count of positions where s[i] = '0' and t[i] = '1'
        num_10 = 0  # Count of positions where s[i] = '1' and t[i] = '0'
        
        for i in range(n):
            if s[i] != t[i]:
                if s[i] == '0': # implies t[i] == '1'
                    num_01 += 1
                else: # s[i] == '1', implies t[i] == '0'
                    num_10 += 1
        
        # If strings are already equal, cost is 0
        if num_01 == 0 and num_10 == 0:
            return 0
        
        # Strategy A: Fix all mismatches using only flip operations
        # This serves as an upper bound and a fallback if other operations are too expensive.
        cost_strategy_A = (num_01 + num_10) * flipCost
        
        # Strategy B: Utilize swap and cross-swap operations where beneficial
        
        # Step B.a: Use intra-string swaps to fix pairs of (0,1) and (1,0) mismatches.
        # Each 'swapCost' operation can fix one (0,1) and one (1,0) mismatch.
        # We can perform min(num_01, num_10) such operations.
        k_pairs_fixed_by_swap = min(num_01, num_10)
        cost_part_B_a = k_pairs_fixed_by_swap * swapCost
        
        # After these swaps, the remaining mismatches are all of the same type.
        k_remaining = abs(num_01 - num_10)
        
        # Step B.b: Fix the k_remaining mismatches (all of the same type)
        
        # Option B.b.i: Fix all k_remaining mismatches using individual flip operations.
        cost_B_b_i = k_remaining * flipCost
        
        # Option B.b.ii: Use cross-swaps to enable more intra-string swaps for same-type mismatches.
        # For two mismatches of the same type (e.g., two '01's), we can:
        # 1. Apply a 'crossCost' operation on one '01' to convert it to a '10'.
        # 2. Then, the resulting '01' and '10' can be fixed by one 'swapCost' operation.
        # Total cost for two same-type mismatches = (crossCost + swapCost).
        # If k_remaining is odd, one mismatch will be left, which must be fixed by a 'flipCost'.
        cost_B_b_ii = (k_remaining // 2) * (crossCost + swapCost) + (k_remaining % 2) * flipCost
        
        # Choose the cheaper way to fix the k_remaining mismatches (min of Option B.b.i and B.b.ii)
        cost_part_B_b = min(cost_B_b_i, cost_B_b_ii)
        
        # Total cost for Strategy B is the sum of cost from B.a and B.b
        cost_strategy_B = cost_part_B_a + cost_part_B_b
        
        # The minimum overall cost is the minimum of Strategy A and Strategy B
        return min(cost_strategy_A, cost_strategy_B)

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s = "01000"
    t = "10111"
    flipCost = 10
    swapCost = 2
    crossCost = 2
    expected_output = 16
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 1 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    # Example 2
    s = "001"
    t = "110"
    flipCost = 2
    swapCost = 100
    crossCost = 100
    expected_output = 6
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 2 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    # Example 3
    s = "1010"
    t = "1010"
    flipCost = 5
    swapCost = 5
    crossCost = 5
    expected_output = 0
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 3 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    # Custom Test Case 1: All 01 mismatches, cross+swap is cheap
    s = "00"
    t = "11"
    flipCost = 10
    swapCost = 1
    crossCost = 1
    expected_output = 2 # 01,01 -> cross one to 10 (cost 1), then swap (cost 1). Total 2.
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 4 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    # Custom Test Case 2: All 01 mismatches, cross+swap is expensive, flips are better
    s = "00"
    t = "11"
    flipCost = 1
    swapCost = 100
    crossCost = 100
    expected_output = 2 # 01,01 -> flip both (cost 1+1=2).
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 5 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    # Custom Test Case 3: Mixed mismatches, simple swap is good
    s = "01"
    t = "10"
    flipCost = 10
    swapCost = 1
    crossCost = 10
    expected_output = 1 # 01,10 -> swap (cost 1).
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 6 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"
    
    # Custom Test Case 4: No mismatches
    s = "000"
    t = "000"
    flipCost = 10
    swapCost = 1
    crossCost = 1
    expected_output = 0
    assert s_obj.minimumCost(s, t, flipCost, swapCost, crossCost) == expected_output, f"Test Case 7 Failed: Expected {expected_output}, Got {s_obj.minimumCost(s, t, flipCost, swapCost, crossCost)}"

    print("All tests passed!")
