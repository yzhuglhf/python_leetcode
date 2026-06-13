"""
Integers With Multiple Sum of Two Cubes
Difficulty: Medium

Description:
This problem asks us to find all "good" integers less than or equal to a given integer n. An integer x is considered good if it can be expressed as the sum of two positive cubes (a^3 + b^3, with a <= b) in at least two distinct ways. We need to return these good integers in a sorted ascending order.

Example:
Input: n = 4104
Output: [1729,4104]

Approach:
The core idea is to iterate through all possible positive integer pairs (a, b) such that a <= b and their sum of cubes, a^3 + b^3, does not exceed n. For each sum calculated, we store how many distinct pairs (a, b) result in that sum. A hash map (Python dictionary) is used to efficiently count these occurrences, mapping `sum -> count`.

We determine an upper bound for `a` and `b`. Since `a^3 + b^3 <= n` and `a, b` are positive integers with `a <= b`, it implies `2*a^3 <= n` (so `a <= (n/2)^(1/3)`) and `b^3 <= n` (so `b <= n^(1/3)`). For `n = 10^9`, `n^(1/3)` is 1000. A safe upper bound for both `a` and `b` can be `int(n**(1/3)) + 2` to account for potential floating-point inaccuracies and ensure all relevant pairs are covered.
We precompute cubes up to this upper bound to speed up calculations. Then, we use nested loops: the outer loop for `a` from 1 up to the upper bound, and the inner loop for `b` from `a` up to the upper bound. Inside the loops, we calculate `current_sum = a^3 + b^3`. If `current_sum` exceeds `n`, we break the inner loop (since increasing `b` further would only yield larger sums). Similarly, if `a^3` alone exceeds `n`, we can break the outer loop. For each `current_sum` less than or equal to `n`, we increment its count in the hash map. Finally, we iterate through the hash map, collect all sums with a count of 2 or more, sort them, and return the result.

Time Complexity: O(n^(2/3))
The maximum value for `a` is roughly `(n/2)^(1/3)` and for `b` is `n^(1/3)`. The nested loops effectively iterate through pairs `(a, b)` such that `a^3 + b^3 <= n`. The number of such pairs is proportional to `n^(2/3)`. Each operation (cube calculation, dictionary lookup/update) is constant time on average. For `n = 10^9`, `n^(2/3) = 10^6`, so approximately `10^6` operations are performed.

Space Complexity: O(n^(2/3))
The `sums_count` dictionary stores entries for each unique sum `a^3 + b^3` that is less than or equal to `n`. The number of such distinct sums is also proportional to `n^(2/3)`. For `n = 10^9`, this means storing up to `10^6` key-value pairs, which is feasible within memory limits. The `cubes` list also takes `O(n^(1/3))` space, which is smaller.
"""
from typing import List
import collections

class Solution:
    def findGoodIntegers(self, n: int) -> List[int]:
        sums_count = collections.defaultdict(int)
        
        # Determine an upper bound for `a` and `b`.
        # Since a^3 + b^3 <= n and a, b are positive, a <= b.
        # This implies a^3 <= n/2 and b^3 <= n.
        # The maximum value for b (and thus a) is approximately n^(1/3).
        # For n = 10^9, n^(1/3) = 1000.
        # We add a small buffer (+2) to `int(n**(1/3))` to handle potential floating-point inaccuracies
        # and ensure all relevant cubic sums are considered.
        upper_bound = int(n**(1/3)) + 2 
        
        # Precompute cubes to optimize calculations in the loops.
        # cubes[i] will store i^3.
        cubes = [i**3 for i in range(upper_bound + 1)]
        
        # Iterate through all possible pairs (a, b) where 1 <= a <= b
        for a in range(1, upper_bound + 1):
            # Optimization: If a^3 alone is already greater than n,
            # then any a^3 + b^3 (since b >= 1) will also be greater than n.
            if cubes[a] > n:
                break
            
            for b in range(a, upper_bound + 1):
                current_sum = cubes[a] + cubes[b]
                
                # Optimization: If the current sum exceeds n,
                # any further increase in b for this 'a' will also result in sums > n.
                # So, we can break the inner loop.
                if current_sum > n:
                    break
                
                # Increment the count for this sum
                sums_count[current_sum] += 1
        
        good_integers = []
        # Collect all sums that were found at least twice
        for s, count in sums_count.items():
            if count >= 2:
                good_integers.append(s)
        
        # Sort the collected good integers in ascending order
        good_integers.sort()
        
        return good_integers

if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.findGoodIntegers(4104) == [1729, 4104], "Example 1 Failed"
    # Example 2
    assert s.findGoodIntegers(578) == [], "Example 2 Failed"
    # Additional test cases
    assert s.findGoodIntegers(1) == [], "n=1 Failed"
    assert s.findGoodIntegers(1728) == [], "n=1728 Failed"
    assert s.findGoodIntegers(1729) == [1729], "n=1729 Failed"
    assert s.findGoodIntegers(13831) == [1729, 4104], "n=13831 Failed"
    assert s.findGoodIntegers(13832) == [1729, 4104, 13832], "n=13832 Failed"
    print("All tests passed!")