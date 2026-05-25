"""
Construct Uniform Parity Array II
Difficulty: Medium

Description:
This problem asks if an array `nums2` can be constructed from a given array `nums1` such that all elements in `nums2` have the same parity (all even or all odd). For each `nums2[i]`, we can either assign `nums1[i]` directly or assign the difference `nums1[i] - nums1[j]` for some `j != i`, provided the difference is at least 1.

Example:
Input: nums1 = [1,4,7]
Output: true
Explanation: We can construct `nums2 = [1, 3, 7]` where all elements are odd. `nums2[0] = nums1[0] = 1`, `nums2[1] = nums1[1] - nums1[0] = 4 - 1 = 3`, `nums2[2] = nums1[2] = 7`.

Approach:
The problem can be solved by checking if it's possible to make all elements in `nums2` even, or if it's possible to make all elements odd. For each `nums1[i]`, if we want to change its parity, we must use the subtraction operation `nums1[i] - nums1[j]`. For `nums1[i] - nums1[j]` to have a different parity than `nums1[i]`, `nums1[j]` must have an opposite parity to `nums1[i]`. For instance, to change an even `nums1[i]` to odd, `nums1[j]` must be odd. The constraint `nums1[i] - nums1[j] >= 1` is crucial, implying `nums1[i] > nums1[j]`.
We first iterate through `nums1` to determine if it contains any even numbers (`has_even`), any odd numbers (`has_odd`), the minimum odd value (`min_odd_val`), and the minimum even value (`min_even_val`).
1. **Can `nums2` be all even?** This is possible if and only if `nums1` contains no odd numbers (`has_odd` is false). In this scenario, all elements in `nums1` are already even, so we can set `nums2[i] = nums1[i]`. If `nums1` contains any odd numbers, the smallest odd number cannot be converted to even (as there's no smaller odd number to subtract), thus making an all-even `nums2` impossible.
2. **Can `nums2` be all odd?** This requires `nums1` to contain at least one odd number (`has_odd` is true), as we need an odd number `nums1[j]` to subtract from any even `nums1[i]` to make it odd (even - odd = odd). If `has_even` is false, all numbers are already odd, and we can set `nums2[i] = nums1[i]`. If `has_even` is true, meaning there are even numbers in `nums1` that need to be converted to odd, then every even `nums1[i]` must be strictly greater than `min_odd_val` (the smallest odd number in `nums1`) to allow the subtraction `nums1[i] - min_odd_val`. Thus, this path is possible if `has_odd` is true, and either `has_even` is false, or `min_even_val > min_odd_val`.
The function returns true if either of these possibilities holds.

Time Complexity: O(N)
Space Complexity: O(1)
"""
from typing import List, Optional

class Solution:
    def uniformArray(self, nums1: List[int]) -> bool:
        has_even = False
        has_odd = False
        min_odd_val = float('inf')  # Stores the minimum odd value in nums1
        min_even_val = float('inf') # Stores the minimum even value in nums1
        
        # First pass to gather essential information about nums1
        for x in nums1:
            if x % 2 == 0:
                has_even = True
                min_even_val = min(min_even_val, x)
            else:
                has_odd = True
                min_odd_val = min(min_odd_val, x)
        
        # Possibility 1: Can nums2 be constructed such that all its elements are even?
        # This is possible if and only if nums1 contains no odd numbers.
        # If all numbers in nums1 are already even, we can simply set nums2[i] = nums1[i] for all i.
        # If there's an odd number in nums1, say 'x', to make it even, we must use x - y where y is odd.
        # However, if 'x' is the smallest odd number (min_odd_val), there is no smaller odd 'y' to subtract.
        # Thus, min_odd_val cannot be converted to an even number.
        possible_all_even = not has_odd

        # Possibility 2: Can nums2 be constructed such that all its elements are odd?
        possible_all_odd = False
        # To make any even number odd (even - odd = odd), we need at least one odd number in nums1 to subtract.
        if has_odd:
            # If nums1 contains no even numbers, all elements are already odd.
            # We can simply set nums2[i] = nums1[i] for all i.
            if not has_even:
                possible_all_odd = True
            else:
                # If there are even numbers in nums1, they must be convertible to odd.
                # An even number 'x' can be made odd by x - y, where 'y' is odd and x > y.
                # To ensure all even numbers can be converted, the smallest even number (min_even_val)
                # must be strictly greater than the smallest odd number (min_odd_val).
                # If min_even_val > min_odd_val, then every even number 'x' (since x >= min_even_val)
                # can be made odd by subtracting min_odd_val (as x >= min_even_val > min_odd_val).
                if min_even_val > min_odd_val:
                    possible_all_odd = True
        
        # Return true if either an all-even or an all-odd array can be constructed.
        return possible_all_even or possible_all_odd

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.uniformArray([1,4,7]) == True, "Example 1 failed"
    
    # Example 2
    assert s.uniformArray([2,3]) == False, "Example 2 failed"
    
    # Example 3
    assert s.uniformArray([4,6]) == True, "Example 3 failed"

    # Additional test cases
    # All odd numbers
    assert s.uniformArray([1,3,5]) == True, "Test Case 4 failed: All odd"
    
    # All even numbers
    assert s.uniformArray([2,4,6]) == True, "Test Case 5 failed: All even"

    # Single odd number
    assert s.uniformArray([1]) == True, "Test Case 6 failed: Single odd"

    # Single even number
    assert s.uniformArray([2]) == True, "Test Case 7 failed: Single even"

    # Mixed, can make all odd
    assert s.uniformArray([10, 1, 12]) == True, "Test Case 8 failed: Mixed, can make odd" 
    # Explanation: all odd possible: 1, 10-1=9, 12-1=11.
    
    # Mixed, cannot make all odd because min_even <= min_odd
    # Cannot make all even because 5 is odd. Cannot make all odd because 2 < 5, so 2 cannot be made odd.
    assert s.uniformArray([2, 5, 4]) == False, "Test Case 9 failed: Mixed, min_even < min_odd" 
    
    # Mixed, multiple odds. Can make all odd. Cannot make all even because 1 and 3 are odd.
    assert s.uniformArray([1, 3, 6]) == True, "Test Case 10 failed: Multiple odds, smallest odd can stay odd" 
    # Explanation: all odd possible: 1, 3, 6-1=5.

    # Mixed, min_even_val > min_odd_val condition.
    # All odd possible: 10-3=7, 20-3=17, 3.
    assert s.uniformArray([10, 20, 3]) == True, "Test Case 11 failed: min_even_val > min_odd_val" 
    
    # Mixed, min_even_val NOT > min_odd_val.
    # All odd impossible: 2 is even, min_odd_val is 3. 2 is not > 3, so 2 cannot be made odd.
    # All even impossible: 3 is odd, cannot be made even.
    assert s.uniformArray([2, 20, 3]) == False, "Test Case 12 failed: min_even_val NOT > min_odd_val"

    print("All tests passed!")
"""