"""
Minimum Operations to Make Binary Palindrome
Difficulty: Medium

Description:
Given an array of integers `nums`, for each `nums[i]`, find the minimum number of operations (increase or decrease by 1) required to transform it into a binary palindrome. A binary palindrome is a number whose binary representation (without leading zeros) reads the same forwards and backwards.

Example:
Input: nums = [1,2,4]
Output: [0,1,1]

Approach:
The problem constraints indicate that `nums[i]` can be up to 5000. This implies that relevant binary palindromes will have a relatively small number of bits. Specifically, numbers up to 5000 require at most 13 bits (since 2^12=4096 and 2^13=8192). To cover potential "nearest" palindromes that might be larger, we precompute all binary palindromes up to 14 bits (which means numbers up to 2^14 - 1 = 16383). This results in a small, constant number of palindromes (around 250).
The precomputation involves iterating through possible bit lengths (`k` from 1 to 14) and for each `k`, constructing palindromes by taking a first half (of `ceil(k/2)` bits, starting with '1') and appending its reversed prefix (excluding the middle bit for odd `k`).
Once the sorted list of palindromes is precomputed, for each `nums[i]`, we efficiently find its nearest palindrome using binary search (`bisect_left`). This function returns the index where `nums[i]` would be inserted to maintain sorted order. The nearest palindrome will then be one of the two palindromes adjacent to this insertion point: the one at `idx` (if `idx` is within bounds) or the one at `idx-1` (if `idx > 0`). We calculate the absolute difference between `nums[i]` and these candidate palindromes and take the minimum as the answer for `nums[i]`.

Time Complexity: O(N log M + C_p) where N is `len(nums)`, M is the number of precomputed palindromes, and C_p is the time for precomputing the palindromes. Since M is a small constant (254) and C_p involves operations proportional to `K_max * 2^(K_max/2) * K_max` where `K_max` is the maximum number of bits (14), C_p is also a small constant. Thus, the overall time complexity is effectively O(N).
Space Complexity: O(M) for storing the precomputed palindromes. Since M is a small constant (254), the space complexity is effectively O(1).
"""
from typing import List
import bisect

class Solution:
    # Use a class variable to store precomputed palindromes.
    # This ensures precomputation happens only once across all test cases
    # when the Solution class is used multiple times (e.g., in LeetCode's test runner).
    _palindromes: List[int] = None

    def _precompute_palindromes(self) -> None:
        """
        Precomputes all binary palindromes up to a certain bit length
        and stores them in a sorted list.
        """
        if Solution._palindromes is not None:
            return # Palindromes already computed

        all_palindromes = set()
        all_palindromes.add(1) # '1' (binary '1') is the smallest palindrome

        # Max nums[i] is 5000.
        # Numbers up to 5000 require at most 13 bits (2^12=4096, 2^13=8192).
        # To find the "nearest" palindrome, we might need to check numbers
        # slightly above the max nums[i]. For instance, a number close to 8192
        # might have 8191 (13 bits) or 8193 (14 bits) as its nearest palindrome.
        # Generating palindromes up to 14 bits (max value 2^14 - 1 = 16383)
        # provides a sufficient range.
        max_k_bits = 14 

        for k in range(2, max_k_bits + 1):
            first_half_len = (k + 1) // 2 # Equivalent to ceil(k/2)
            
            # Iterate through all possible first halves that start with '1'.
            # For a length 'L' binary string, numbers range from 2^(L-1) to 2^L - 1.
            for i in range(2**(first_half_len - 1), 2**first_half_len):
                bin_i = bin(i)[2:] # Get binary string representation, e.g., '101' for 5

                if k % 2 == 1: # Odd length palindrome, e.g., k=3, bin_i='10', palindrome is '101'
                    # The middle bit is part of `bin_i`. We only reverse `bin_i` excluding its last char.
                    suffix_to_reverse = bin_i[:-1] 
                else: # Even length palindrome, e.g., k=4, bin_i='10', palindrome is '1001'
                    # The entire `bin_i` forms the first half to be reversed.
                    suffix_to_reverse = bin_i 

                palindrome_val = int(bin_i + suffix_to_reverse[::-1], 2)
                all_palindromes.add(palindrome_val)
        
        Solution._palindromes = sorted(list(all_palindromes))

    def minOperations(self, nums: List[int]) -> List[int]:
        self._precompute_palindromes() # Ensure palindromes are precomputed
        
        ans = []
        for num in nums:
            # Use bisect_left to find the insertion point for `num` in the sorted palindromes list.
            # `idx` will be the index of the first palindrome >= `num`.
            idx = bisect.bisect_left(Solution._palindromes, num)
            
            min_ops = float('inf') # Initialize with a very large number

            # Candidate 1: Palindrome at or after the insertion point (`_palindromes[idx]`).
            # This is the smallest palindrome that is >= `num`.
            if idx < len(Solution._palindromes):
                min_ops = min(min_ops, abs(num - Solution._palindromes[idx]))
            
            # Candidate 2: Palindrome before the insertion point (`_palindromes[idx - 1]`).
            # This is the largest palindrome that is < `num`.
            if idx > 0:
                min_ops = min(min_ops, abs(num - Solution._palindromes[idx - 1]))
                
            ans.append(min_ops)
            
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [1, 2, 4]
    expected1 = [0, 1, 1]
    result1 = s.minOperations(nums1)
    print(f"Input: {nums1}, Output: {result1}, Expected: {expected1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"

    # Example 2
    nums2 = [6, 7, 12]
    expected2 = [1, 0, 3]
    result2 = s.minOperations(nums2)
    print(f"Input: {nums2}, Output: {result2}, Expected: {expected2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"

    # Custom test cases
    nums3 = [5] # Binary '101' is already a palindrome
    expected3 = [0]
    result3 = s.minOperations(nums3)
    print(f"Input: {nums3}, Output: {result3}, Expected: {expected3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"

    nums4 = [5000] # Binary '1001110001000'. Nearest palindrome is 4889 ('1001011101001'). Diff = 111.
    expected4 = [111]
    result4 = s.minOperations(nums4)
    print(f"Input: {nums4}, Output: {result4}, Expected: {expected4}")
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"

    nums5 = [8] # Binary '1000'. Nearest are 7 ('111') and 9 ('1001'). Both diff 1.
    expected5 = [1]
    result5 = s.minOperations(nums5)
    print(f"Input: {nums5}, Output: {result5}, Expected: {expected5}")
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    
    nums6 = [4096] # Binary '1000000000000'. Nearest are 4095 ('111...1') and 4097 ('100...01'). Both diff 1.
    expected6 = [1]
    result6 = s.minOperations(nums6)
    print(f"Input: {nums6}, Output: {result6}, Expected: {expected6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"

    print("All tests passed!")

```