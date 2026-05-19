"""
Smallest All-Ones Multiple
Difficulty: Medium

Description:
This problem asks us to find the smallest positive integer n that consists only of the digit 1 (e.g., 1, 11, 111, ...) and is divisible by a given positive integer k. We need to return the number of digits in n. If no such n exists, we should return -1.

Example:
Input: k = 7
Output: 6
Explanation: n = 111111 because 111111 is divisible by 7, and it is the smallest such number. Its length is 6.

Approach:
We are looking for an all-ones number, which can be generated iteratively: `current_num = (previous_num * 10 + 1)`. To avoid large number overflow, we can work with remainders modulo k. Let `current_remainder` be the remainder of the current all-ones number when divided by k. The next all-ones number's remainder will be `(current_remainder * 10 + 1) % k`. We start with `remainder = 0` (conceptually representing an empty number before the first '1') and `length = 0`. In each step, we update the remainder and increment length. If `remainder` becomes 0, we have found our number, and `length` is the answer. A crucial optimization is to first check if `k` is divisible by 2 or 5. All-ones numbers always end in 1, so they are odd and not divisible by 5. Thus, if `k` has 2 or 5 as a prime factor, no such all-ones multiple exists, and we return -1 immediately. For all other `k`, such a number is guaranteed to exist. By the pigeonhole principle, if a solution exists, we will find it within at most `k` iterations, as there are `k` possible remainders (0 to k-1) before a cycle must occur.

Time Complexity: O(k)
Space Complexity: O(1)
"""
from typing import List, Optional

class Solution:
    def minAllOneMultiple(self, k: int) -> int:
        # All-ones numbers always end in 1.
        # This means they are odd, so they cannot be divisible by any even number (k % 2 == 0).
        # This also means they are not divisible by 5, as numbers divisible by 5 must end in 0 or 5 (k % 5 == 0).
        # Therefore, if k is divisible by 2 or 5, no such all-ones multiple exists.
        if k % 2 == 0 or k % 5 == 0:
            return -1
        
        # Initialize remainder to 0. The first iteration will calculate (0 * 10 + 1) % k = 1 % k,
        # correctly representing the number '1'.
        remainder = 0
        # Initialize length to 0. It will be incremented in each step.
        length = 0
        
        # We iterate at most k times.
        # This is because there are k possible remainders (0 to k-1).
        # If a solution exists, we will find it before a non-zero remainder repeats,
        # which must happen within k iterations according to the pigeonhole principle.
        for _ in range(k):
            remainder = (remainder * 10 + 1) % k
            length += 1
            
            if remainder == 0:
                # If the remainder is 0, we have found an all-ones number divisible by k.
                # 'length' stores the number of digits in this number.
                return length
        
        # This line should theoretically not be reached for k not divisible by 2 or 5,
        # as a solution is guaranteed to exist within k steps. However, some problem
        # implementations or environments might implicitly require a return value.
        # In competitive programming, this usually indicates an error in reasoning
        # if the mathematical guarantee holds.
        return -1 

if __name__ == "__main__":
    s = Solution()
    
    # Example 1: k = 3 -> Output: 3
    assert s.minAllOneMultiple(3) == 3, f"Test failed for k=3. Expected 3, got {s.minAllOneMultiple(3)}"
    
    # Example 2: k = 7 -> Output: 6
    assert s.minAllOneMultiple(7) == 6, f"Test failed for k=7. Expected 6, got {s.minAllOneMultiple(7)}"
    
    # Example 3: k = 2 -> Output: -1
    assert s.minAllOneMultiple(2) == -1, f"Test failed for k=2. Expected -1, got {s.minAllOneMultiple(2)}"
    
    # Additional test cases
    assert s.minAllOneMultiple(1) == -1, f"Test failed for k=1. Expected -1, got {s.minAllOneMultiple(1)}" # Constraint 2 <= k, but useful for testing
    assert s.minAllOneMultiple(10) == -1, f"Test failed for k=10. Expected -1, got {s.minAllOneMultiple(10)}" # Divisible by 2 and 5
    assert s.minAllOneMultiple(5) == -1, f"Test failed for k=5. Expected -1, got {s.minAllOneMultiple(5)}" # Divisible by 5
    assert s.minAllOneMultiple(13) == 6, f"Test failed for k=13. Expected 6, got {s.minAllOneMultiple(13)}" # 111111 is divisible by 13
    assert s.minAllOneMultiple(9) == 9, f"Test failed for k=9. Expected 9, got {s.minAllOneMultiple(9)}" # 111,111,111 is divisible by 9
    assert s.minAllOneMultiple(21) == 6, f"Test failed for k=21. Expected 6, got {s.minAllOneMultiple(21)}" # 111111 is divisible by 21 (111111 = 21 * 5291)
    
    print("All tests passed!")