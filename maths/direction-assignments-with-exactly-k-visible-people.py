"""
Direction Assignments with Exactly K Visible People
Difficulty: Medium

Description:
This problem asks us to count the number of ways to assign 'L' or 'R' directions to n people such that a specific person at `pos` sees exactly `k` other people. People to the left of `pos` (indices `i < pos`) are visible if they choose 'L', and people to the right of `pos` (indices `i > pos`) are visible if they choose 'R'. The person at `pos` can choose 'L' or 'R' independently, and their choice does not affect the count of people *they* see.

Example:
Input: n = 3, pos = 1, k = 0
Output: 2
Explanation: There is 1 person to the left (index 0) and 1 person to the right (index 2) of pos = 1. To see 0 people, person 0 must choose 'R' (invisible to pos) and person 2 must choose 'L' (invisible to pos). There is 1 way for the left side (C(1,0)=1) and 1 way for the right side (C(1,0)=1). The person at pos=1 has 2 choices ('L' or 'R'), so total ways = 1 * 1 * 2 = 2.

Approach:
The problem can be decomposed into two independent subproblems: counting visible people from the left and counting visible people from the right. Let `num_left` be the number of people to the left of `pos` (i.e., `pos`), and `num_right` be the number of people to the right of `pos` (i.e., `n - 1 - pos`). If we need `k_left` visible people from the left and `k_right` visible people from the right, such that `k_left + k_right = k`, the number of ways is `C(num_left, k_left) * C(num_right, k_right)`. `C(N, K)` represents "N choose K" combinations. We iterate through all possible values of `k_left` (from `max(0, k - num_right)` to `min(k, num_left)`), calculate the corresponding `k_right`, and sum up the products of combinations. Since `n` can be up to 10^5, we precompute factorials and inverse factorials modulo 10^9 + 7 to efficiently calculate combinations. Finally, we multiply the total sum by 2, as the choice of the person at `pos` does not affect the count of visible people and can be 'L' or 'R'.

Time Complexity: O(MAX_N_PRECOMPUTE + min(k, pos, n-1-pos)). The precomputation takes O(MAX_N_PRECOMPUTE) time. The loop runs at most O(min(N, K)) times, which is O(N) in the worst case. Since MAX_N_PRECOMPUTE is 10^5, the overall time complexity is dominated by O(MAX_N_PRECOMPUTE).
Space Complexity: O(MAX_N_PRECOMPUTE) for storing factorials and inverse factorials.
"""
from typing import List, Optional

MOD = 10**9 + 7
MAX_N_PRECOMPUTE = 10**5 # Max value for n is 10^5, used for factorial precomputation

# Precompute factorials and inverse factorials for combinations.
# These are global to be computed once when the module is loaded
# and shared across all instances/calls, which is typical for competitive programming setup.
fact = [1] * (MAX_N_PRECOMPUTE + 1)
inv_fact = [1] * (MAX_N_PRECOMPUTE + 1)

def _precompute_factorials_and_inverses():
    """
    Precomputes factorials and their modular inverses up to MAX_N_PRECOMPUTE.
    This allows O(1) computation of nCr after precomputation.
    """
    fact[0] = 1
    inv_fact[0] = 1
    for i in range(1, MAX_N_PRECOMPUTE + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Compute inverse factorial for MAX_N_PRECOMPUTE using Fermat's Little Theorem
    # a^(MOD-2) % MOD is a^(-1) % MOD for prime MOD
    inv_fact[MAX_N_PRECOMPUTE] = pow(fact[MAX_N_PRECOMPUTE], MOD - 2, MOD)
    
    # Compute other inverse factorials iteratively: inv(i!) = inv((i+1)!) * (i+1)
    for i in range(MAX_N_PRECOMPUTE - 1, 0, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD

# Call the precomputation function once when the script is loaded
_precompute_factorials_and_inverses()


class Solution:
    def nCr_mod_p(self, n, r):
        """
        Calculates nCr (n choose r) modulo MOD using precomputed factorials and inverse factorials.
        Returns 0 if r is out of bounds (r < 0 or r > n).
        """
        if r < 0 or r > n:
            return 0
        # C(n, r) = n! / (r! * (n-r)!) = n! * (r!)^-1 * ((n-r)!)^-1
        numerator = fact[n]
        denominator_inv = (inv_fact[r] * inv_fact[n - r]) % MOD
        return (numerator * denominator_inv) % MOD

    def countVisiblePeople(self, n: int, pos: int, k: int) -> int:
        num_left = pos # Number of people at indices 0 to pos-1
        num_right = n - 1 - pos # Number of people at indices pos+1 to n-1

        total_assignments = 0

        # We need to distribute k visible people between the left and right sides.
        # Let k_left be the number of visible people from the left side,
        # and k_right be the number of visible people from the right side.
        # Conditions:
        # 1. k_left + k_right = k
        # 2. 0 <= k_left <= num_left
        # 3. 0 <= k_right <= num_right
        # From (1) and (3): 0 <= k - k_left <= num_right
        #                     k - num_right <= k_left <= k
        # Combining with (2), the valid range for k_left is:
        # max(0, k - num_right) <= k_left <= min(k, num_left)

        start_k_left = max(0, k - num_right)
        end_k_left = min(k, num_left)

        for k_left in range(start_k_left, end_k_left + 1):
            k_right = k - k_left
            
            # Ways to choose k_left visible people from num_left people.
            # The chosen k_left people choose 'L', the remaining (num_left - k_left) choose 'R'.
            ways_left = self.nCr_mod_p(num_left, k_left)
            
            # Ways to choose k_right visible people from num_right people.
            # The chosen k_right people choose 'R', the remaining (num_right - k_right) choose 'L'.
            ways_right = self.nCr_mod_p(num_right, k_right)
            
            # The total ways for this specific (k_left, k_right) pair is their product.
            # Add this to the running total, ensuring modulo arithmetic.
            total_assignments = (total_assignments + (ways_left * ways_right) % MOD) % MOD
        
        # The person at 'pos' can choose either 'L' or 'R'. This choice does not affect
        # the count of people *they* see. Therefore, we multiply the total ways by 2.
        return (total_assignments * 2) % MOD

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.countVisiblePeople(n=3, pos=1, k=0) == 2, f"Test 1 Failed: {s.countVisiblePeople(n=3, pos=1, k=0)}"

    # Example 2
    assert s.countVisiblePeople(n=3, pos=2, k=1) == 4, f"Test 2 Failed: {s.countVisiblePeople(n=3, pos=2, k=1)}"

    # Example 3
    assert s.countVisiblePeople(n=1, pos=0, k=0) == 2, f"Test 3 Failed: {s.countVisiblePeople(n=1, pos=0, k=0)}"

    # Custom Test 1: n=5, pos=2, k=1
    # num_left=2 (0,1), num_right=2 (3,4)
    # k_left+k_right=1
    #   k_left=0, k_right=1: C(2,0)*C(2,1) = 1*2 = 2
    #   k_left=1, k_right=0: C(2,1)*C(2,0) = 2*1 = 2
    # Total for visible people = 2+2=4. Multiply by 2 for pos's choice = 8.
    assert s.countVisiblePeople(n=5, pos=2, k=1) == 8, f"Test 4 Failed: {s.countVisiblePeople(n=5, pos=2, k=1)}"

    # Custom Test 2: Max values for n, pos, k for simple case
    # n=10^5, pos=0, k=0
    # num_left=0, num_right=99999
    # k_left=0, k_right=0: C(0,0)*C(99999,0) = 1*1 = 1
    # Total = 1. Multiply by 2 = 2.
    assert s.countVisiblePeople(n=10**5, pos=0, k=0) == 2, f"Test 5 Failed: {s.countVisiblePeople(n=10**5, pos=0, k=0)}"

    # Custom Test 3: Large N, K in middle
    # n=10, pos=5, k=3
    # num_left=5, num_right=4
    # k_left+k_right=3
    # k_left range: max(0, 3-4)=-1 -> 0, min(3, 5)=3
    # Range: 0 to 3
    # k_left=0, k_right=3: C(5,0)*C(4,3) = 1*4 = 4
    # k_left=1, k_right=2: C(5,1)*C(4,2) = 5*6 = 30
    # k_left=2, k_right=1: C(5,2)*C(4,1) = 10*4 = 40
    # k_left=3, k_right=0: C(5,3)*C(4,0) = 10*1 = 10
    # Total = 4+30+40+10 = 84. Multiply by 2 = 168.
    assert s.countVisiblePeople(n=10, pos=5, k=3) == 168, f"Test 6 Failed: {s.countVisiblePeople(n=10, pos=5, k=3)}"


    print("All tests passed!")

