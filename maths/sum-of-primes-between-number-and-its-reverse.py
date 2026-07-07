"""
Sum of Primes Between Number and Its Reverse
Difficulty: Medium

Description:
This function calculates the sum of all prime numbers found within a range defined by an input integer `n` and its digit-reversed counterpart `r`. The range is inclusive, from `min(n, r)` to `max(n, r)`.

Example:
Input: n = 13
Output: 132
Explanation: The reverse of 13 is 31. The range is [13, 31]. Primes are 13, 17, 19, 23, 29, 31. Their sum is 132.

Approach:
The algorithm first determines the reversed integer `r` from the input `n` by converting `n` to a string, reversing it, and converting it back to an integer. Then, it establishes the lower and upper bounds of the range as `min(n, r)` and `max(n, r)` respectively. To efficiently find prime numbers within this range, a Sieve of Eratosthenes is precomputed once up to the maximum possible value of `n` (which is 1000 according to constraints) as a class attribute. This sieve stores a boolean array indicating whether each number up to 1000 is prime. Finally, the function iterates from the `lower` bound to the `upper` bound, checking each number against the precomputed sieve. If a number is marked as prime, it is added to a running total, which is returned at the end.

Time Complexity: O(MAX_N * log(log(MAX_N))) for sieve precomputation (executed once when the class is loaded), and O(max(n, r)) for each call to `sumOfPrimesInRange`. Since `max(n, r)` is at most `MAX_N`, the per-call complexity is O(MAX_N). The overall dominant factor considering multiple calls and precomputation is effectively efficient for the given constraints.
Space Complexity: O(MAX_N) for storing the prime sieve, where MAX_N is the maximum possible value for n (1000).
"""
from typing import List, Optional

class Solution:
    # Define the maximum constraint for n
    MAX_N_CONSTRAINT = 1000
    
    # Precompute primes up to MAX_N_CONSTRAINT using Sieve of Eratosthenes
    # _is_prime[i] will be True if i is prime, False otherwise
    _is_prime = [True] * (MAX_N_CONSTRAINT + 1)
    
    # 0 and 1 are not prime numbers
    _is_prime[0] = False
    if MAX_N_CONSTRAINT >= 1: # Ensure index 1 exists
        _is_prime[1] = False
    
    # Run the Sieve algorithm
    # Iterate from 2 up to sqrt(MAX_N_CONSTRAINT)
    for p in range(2, int(MAX_N_CONSTRAINT**0.5) + 1):
        if _is_prime[p]:
            # Mark all multiples of p (starting from p*p) as not prime
            for multiple in range(p*p, MAX_N_CONSTRAINT + 1, p):
                _is_prime[multiple] = False

    def sumOfPrimesInRange(self, n: int) -> int:
        # Step 1: Reverse the integer n
        # Convert n to a string, reverse the string, then convert back to an integer.
        # This handles cases like 10 -> "10" -> "01" -> 1 correctly.
        r_str = str(n)[::-1]
        r = int(r_str)

        # Step 2: Determine the lower and upper bounds of the range
        lower = min(n, r)
        upper = max(n, r)

        # Step 3 & 4: Iterate through the range and sum all prime numbers
        total_sum = 0
        # Iterate from the lower bound to the upper bound (inclusive)
        for i in range(lower, upper + 1):
            # Check if the current number 'i' is prime using the precomputed sieve
            if Solution._is_prime[i]:
                total_sum += i
        
        return total_sum

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.sumOfPrimesInRange(13) == 132, "Test Case 1 Failed: n=13"
    
    # Example 2
    assert s.sumOfPrimesInRange(10) == 17, "Test Case 2 Failed: n=10"
    
    # Example 3
    assert s.sumOfPrimesInRange(8) == 0, "Test Case 3 Failed: n=8"
    
    # Additional test cases
    # n = 1, r = 1. Range [1, 1]. No primes. Sum = 0.
    assert s.sumOfPrimesInRange(1) == 0, "Test Case 4 Failed: n=1"
    
    # n = 2, r = 2. Range [2, 2]. Prime: 2. Sum = 2.
    assert s.sumOfPrimesInRange(2) == 2, "Test Case 5 Failed: n=2"

    # n = 7, r = 7. Range [7, 7]. Prime: 7. Sum = 7.
    assert s.sumOfPrimesInRange(7) == 7, "Test Case 6 Failed: n=7"
    
    # n = 100 (reverse is 1), Range [1, 100]. Sum of primes up to 100.
    assert s.sumOfPrimesInRange(100) == 1060, "Test Case 7 Failed: n=100"

    # n = 999 (reverse is 999), Range [999, 999]. 999 is not prime (divisible by 3, 9, etc.). Sum = 0.
    assert s.sumOfPrimesInRange(999) == 0, "Test Case 8 Failed: n=999"

    # n = 997 (prime), r = 799 (not prime, 17 * 47). Range [799, 997].
    # Sum of primes between 799 and 997 inclusive.
    # Primes in [799, 997] are: 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997.
    # The sum is 25964.
    assert s.sumOfPrimesInRange(997) == 25964, "Test Case 9 Failed: n=997"
    
    print("All tests passed!")