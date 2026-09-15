"""
Find the Smallest Balanced Index
Difficulty: Medium

Description:
This problem requires finding the smallest index in an integer array `nums` such that the sum of elements strictly to its left equals the product of elements strictly to its right. Special conditions apply for empty segments: an empty left side has a sum of 0, and an empty right side has a product of 1.

Example:
Input: nums = [2,8,2,2,5]
Output: 2
Explanation: For index 2, the left sum (nums[0] + nums[1] = 2 + 8 = 10) equals the right product (nums[3] * nums[4] = 2 * 5 = 10). This is the smallest such index.

Approach:
The solution employs a two-pass approach using auxiliary arrays to achieve O(N) time complexity. First, a prefix sum array `prefix_sums` is computed, where `prefix_sums[i]` stores the sum of elements from `nums[0]` to `nums[i-1]`. This allows constant-time retrieval of any left sum. Second, a suffix product array `suffix_products` is computed, where `suffix_products[i]` stores the product of elements from `nums[i]` to `nums[n-1]`. To prevent potential performance issues with extremely large products due to Python's arbitrary-precision integers, a `MAX_THRESHOLD_PRODUCT` (set slightly above the maximum possible sum) is used. If any intermediate product exceeds this threshold, it is capped, as it can no longer equal any possible sum. Finally, the algorithm iterates from `i = 0` to `n-1`. For each index `i`, it compares `prefix_sums[i]` (the sum of elements strictly to the left) with `suffix_products[i+1]` (the product of elements strictly to the right). The first index `i` that satisfies this equality is the smallest balanced index and is returned. If no such index is found after checking all possibilities, -1 is returned.

Time Complexity: O(N)
Space Complexity: O(N)
"""
from typing import List, Optional

class Solution:
    def smallestBalancedIndex(self, nums: List[int]) -> int:
        n = len(nums)

        # Maximum possible sum: n * max(nums[i]) = 10^5 * 10^9 = 10^14.
        # Products that exceed this value can never equal any possible sum.
        # We use a threshold slightly greater than this maximum sum to cap product values
        # and avoid potentially very large integer computations, ensuring efficiency.
        MAX_THRESHOLD_PRODUCT = 10**14 + 1 

        # 1. Compute prefix sums
        # prefix_sums[i] will store the sum of nums[0]...nums[i-1]
        # prefix_sums[0] = 0 (representing the sum of an empty prefix)
        prefix_sums = [0] * (n + 1)
        current_sum = 0
        for i in range(n):
            current_sum += nums[i]
            prefix_sums[i+1] = current_sum
        
        # 2. Compute suffix products
        # suffix_products[i] will store the product of nums[i]...nums[n-1]
        # suffix_products[n] = 1 (representing the product of an empty suffix)
        suffix_products = [0] * (n + 1)
        suffix_products[n] = 1 # Base case for an empty right side, product is 1
        
        for i in range(n - 1, -1, -1):
            num_val = nums[i]
            # This is the product of elements nums[i+1]...nums[n-1]
            current_prod_from_right = suffix_products[i+1] 
            
            # Check for potential overflow before multiplication or if it's already capped.
            # If current_prod_from_right is already at or above the threshold,
            # multiplying it by num_val (which is >= 1) will keep it above.
            if current_prod_from_right >= MAX_THRESHOLD_PRODUCT:
                suffix_products[i] = MAX_THRESHOLD_PRODUCT
            # If num_val multiplied by current_prod_from_right would exceed the threshold.
            # This check prevents actual computation of extremely large numbers.
            elif num_val > MAX_THRESHOLD_PRODUCT // current_prod_from_right:
                suffix_products[i] = MAX_THRESHOLD_PRODUCT
            else:
                suffix_products[i] = num_val * current_prod_from_right
        
        # 3. Iterate from left to right to find the smallest balanced index
        for i in range(n):
            # The sum of elements strictly to the left of index i is prefix_sums[i]
            left_sum = prefix_sums[i]
            
            # The product of elements strictly to the right of index i is suffix_products[i+1]
            right_product = suffix_products[i+1]
            
            if left_sum == right_product:
                return i # Found the smallest balanced index

        # If the loop completes, no balanced index was found
        return -1

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.smallestBalancedIndex(nums=[2,1,2]) == 1, "Example 1 failed"
    
    # Example 2
    assert s.smallestBalancedIndex(nums=[2,8,2,2,5]) == 2, "Example 2 failed"
    
    # Example 3
    assert s.smallestBalancedIndex(nums=[1]) == -1, "Example 3 failed"

    # Additional Test Case 1: All ones, first balanced index should be 1
    assert s.smallestBalancedIndex(nums=[1,1,1,1]) == 1, "Test Case 1 failed"

    # Additional Test Case 2: No balanced index
    assert s.smallestBalancedIndex(nums=[1,2,3,4,5,6]) == -1, "Test Case 2 failed"

    # Additional Test Case 3: Large numbers with a balanced index
    # Left sum = nums[0] = 10^9
    # Right product = nums[2]*nums[3]*nums[4] = 1*1*10^9 = 10^9
    assert s.smallestBalancedIndex(nums=[10**9, 1, 1, 1, 10**9]) == 1, "Test Case 3 failed"

    # Additional Test Case 4: Products quickly exceed sums, should use thresholding
    assert s.smallestBalancedIndex(nums=[1, 1000, 1000]) == -1, "Test Case 4 failed"
    # For i=0: left_sum=0, right_product=1000*1000 = 10^6
    # For i=1: left_sum=1, right_product=1000
    # For i=2: left_sum=1+1000=1001, right_product=1
    
    # Additional Test Case 5: Single element, not balanced
    assert s.smallestBalancedIndex(nums=[100]) == -1, "Test Case 5 failed"

    # Additional Test Case 6: Empty left side, product to the right is 1
    assert s.smallestBalancedIndex(nums=[0,1]) == -1 # (left sum 0, right product 1 -- wait, nums[i] >= 1, so this case is impossible as per constraints)
    # The constraints state 1 <= nums[i] <= 10^9. So 0 is not possible.
    # Correct test case for 1 <= nums[i]
    assert s.smallestBalancedIndex(nums=[1,1]) == 1 # i=0: left=0, right=1. i=1: left=1, right=1.
    
    # Additional Test Case 7: All elements are large, product exceeds threshold
    assert s.smallestBalancedIndex(nums=[10**9, 10**9, 10**9]) == -1, "Test Case 7 failed"


    print("All tests passed!")

```