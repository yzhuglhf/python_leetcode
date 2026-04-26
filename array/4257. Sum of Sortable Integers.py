"""
Sum of Sortable Integers (LeetCode #4257)
Difficulty: Hard

Description:
This problem asks us to find the sum of all "sortable" integers k. An integer k is sortable if it divides the array length n, and the array can be sorted in non-decreasing order by partitioning it into consecutive subarrays of length k and then cyclically rotating each subarray independently any number of times.

Example:
Input: nums = [3,1,2]
Output: 3
Explanation: For n=3, possible divisors are 1 and 3. For k=1, partitioning into [3],[1],[2] cannot be sorted as the values are out of order. For k=3, the single subarray [3,1,2] can be rotated once to [1,2,3], which is sorted. So only k=3 is sortable. The sum of sortable integers is 3.

Approach:
The solution involves iterating through all possible positive divisors 'k' of the array's length 'n'. For each candidate 'k', we verify if it is "sortable" by checking two conditions for every block of 'k' elements. First, we generate a globally sorted version of `nums`, called `sorted_nums`. For each block `i` (from `nums[i*k : (i+1)*k]`) and its corresponding target block from `sorted_nums` (from `sorted_nums[i*k : (i+1)*k]`), we ensure:
1. The elements within the current block are a permutation of the elements within the target block. This is efficiently checked using `collections.Counter` to compare element frequencies.
2. The current block can be cyclically rotated to exactly match the target block. This is checked by converting both blocks into a string representation using a delimiter (e.g., `"#".join(map(str, block))`). Then, we verify if the target block's string is a substring of the current block's string concatenated with itself and a delimiter (i.e., `target_str in (current_str + "#" + current_str)`). Python's string `in` operator is typically implemented with optimized algorithms (like Boyer-Moore or Rabin-Karp) for efficient substring search.
If both conditions hold true for all `n/k` blocks, then `k` is a sortable integer and is added to the total sum.

Time Complexity: O(N log N + d(N) * N * L)
- O(N log N) for initially sorting `nums` to `sorted_nums`.
- O(sqrt(N)) for finding all divisors of N, where `d(N)` is the number of divisors.
- For each of the `d(N)` divisors `k`:
    - We iterate through `N/k` blocks.
    - For each block of size `k`:
        - Comparing `collections.Counter` objects takes O(k) time.
        - Converting a block of `k` integers into a delimited string takes O(k * L) time, where `L` is the maximum number of digits for an integer (constant, approx. 6 for numbers up to 10^5).
        - Checking for substring existence using `in` takes O(k * L) time (assuming optimized string search, which generally implies linear time complexity in the length of strings involved).
    - Thus, for a given `k`, the total time for checking all `N/k` blocks is `(N/k) * (O(k) + O(k*L)) = O(N*L)`.
- The overall time complexity is O(N log N + d(N) * N * L). Given N=10^5, L=6, and maximum d(N) approx 128 (for N=83160), this equates to roughly `10^5 * log(10^5) + 128 * 10^5 * 6` operations, which is about `1.7 * 10^6 + 7.68 * 10^7 = 7.85 * 10^7`, feasible within typical time limits.

Space Complexity: O(N * L)
- O(N) for storing `sorted_nums`.
- O(d(N)) for storing the set of divisors.
- O(k * L) temporary space for `collections.Counter` and string representations of blocks during iteration. In the worst case (when `k=N`), this amounts to `O(N*L)`.
- Overall, as L is a small constant, the space complexity is effectively O(N).
"""
from typing import List, Optional
import collections
import math

class Solution:
    def sortableIntegers(self, nums: List[int]) -> int:
        n = len(nums)
        sorted_nums = sorted(nums)

        # 1. Find all divisors of n
        divisors = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divisors.add(i)
                divisors.add(n // i)
        
        total_sum = 0

        # 2. For each divisor k, check if it's sortable
        for k in divisors:
            is_k_sortable = True
            
            for block_idx in range(n // k):
                start_idx = block_idx * k
                end_idx = start_idx + k
                
                current_block = nums[start_idx:end_idx]
                target_block = sorted_nums[start_idx:end_idx]
                
                # Condition 1: Check if current_block is a permutation of target_block
                # If the counts of elements do not match, they cannot be rotated into each other.
                if collections.Counter(current_block) != collections.Counter(target_block):
                    is_k_sortable = False
                    break
                
                # Condition 2: Check if current_block can be rotated to target_block
                # Convert blocks to strings using a unique delimiter (e.g., '#') to avoid
                # ambiguity with multi-digit numbers (e.g., [1,2] vs [12]).
                s_current_block = "#".join(map(str, current_block))
                s_target_block = "#".join(map(str, target_block))
                
                # If target_block is a cyclic shift of current_block, then s_target_block
                # must be a substring of s_current_block concatenated with itself (with a delimiter
                # in between to handle rotations that cross the array boundary).
                # Example: current_block = [3,1,2] -> s_current_block = "3#1#2"
                # target_block = [1,2,3] -> s_target_block = "1#2#3"
                # The extended string "3#1#2#3#1#2" contains "1#2#3".
                if s_target_block not in (s_current_block + "#" + s_current_block):
                    is_k_sortable = False
                    break
            
            if is_k_sortable:
                total_sum += k
                
        return total_sum

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [3,1,2]
    expected1 = 3
    assert s.sortableIntegers(nums1) == expected1, f"Test 1 Failed: Input: {nums1}, Expected: {expected1}, Got: {s.sortableIntegers(nums1)}"
    
    # Example 2
    nums2 = [7,6,5]
    expected2 = 0
    assert s.sortableIntegers(nums2) == expected2, f"Test 2 Failed: Input: {nums2}, Expected: {expected2}, Got: {s.sortableIntegers(nums2)}"
    
    # Example 3
    nums3 = [5,8]
    expected3 = 3
    assert s.sortableIntegers(nums3) == expected3, f"Test 3 Failed: Input: {nums3}, Expected: {expected3}, Got: {s.sortableIntegers(nums3)}"

    # Additional Test Cases
    # Case 1: Already sorted array
    nums4 = [1,2,3,4] # n=4. Divisors: 1, 2, 4. All should be sortable.
    expected4 = 1 + 2 + 4 # = 7
    assert s.sortableIntegers(nums4) == expected4, f"Test 4 Failed: Input: {nums4}, Expected: {expected4}, Got: {s.sortableIntegers(nums4)}"

    # Case 2: Array that can be sorted by k=n, but not smaller k
    nums5 = [4,1,2,3] # n=4. sorted_nums = [1,2,3,4]
    # k=1: [4],[1],[2],[3] -> not sortable ([4] != [1])
    # k=2: [4,1],[2,3] -> Block [4,1] vs target [1,2]. Counters match, but "1#2" not in "4#1#4#1". Not sortable.
    # k=4: [4,1,2,3] -> Block [4,1,2,3] vs target [1,2,3,4]. Counters match. "1#2#3#4" in "4#1#2#3#4#1#2#3". Sortable.
    expected5 = 4
    assert s.sortableIntegers(nums5) == expected5, f"Test 5 Failed: Input: {nums5}, Expected: {expected5}, Got: {s.sortableIntegers(nums5)}"

    # Case 3: More complex permutation
    nums6 = [2,3,1,5,6,4] # n=6. sorted_nums = [1,2,3,4,5,6]. Divisors: 1, 2, 3, 6
    # k=1: Not sortable.
    # k=2: [2,3],[1,5],[6,4] vs [1,2],[3,4],[5,6]. Block 0 [2,3] vs [1,2]. Counter mismatch. Not sortable.
    # k=3: [2,3,1],[5,6,4] vs [1,2,3],[4,5,6]
    #   Block 0: [2,3,1] vs [1,2,3]. Counters match. "1#2#3" in "2#3#1#2#3#1". Yes.
    #   Block 1: [5,6,4] vs [4,5,6]. Counters match. "4#5#6" in "5#6#4#5#6#4". Yes.
    #   k=3 is sortable.
    # k=6: [2,3,1,5,6,4] vs [1,2,3,4,5,6]. Counters match. "1#2#3#4#5#6" in "2#3#1#5#6#4#2#3#1#5#6#4". Yes.
    #   k=6 is sortable.
    expected6 = 3 + 6 # = 9
    assert s.sortableIntegers(nums6) == expected6, f"Test 6 Failed: Input: {nums6}, Expected: {expected6}, Got: {s.sortableIntegers(nums6)}"
    
    # Case 4: All same numbers
    nums7 = [5,5,5,5] # n=4. sorted_nums = [5,5,5,5]. Divisors: 1, 2, 4. All should be sortable.
    expected7 = 1 + 2 + 4 # = 7
    assert s.sortableIntegers(nums7) == expected7, f"Test 7 Failed: Input: {nums7}, Expected: {expected7}, Got: {s.sortableIntegers(nums7)}"

    # Case 5: Numbers with different digit counts (check string conversion robustness)
    nums9 = [100, 1, 10, 2] # n=4. sorted_nums = [1, 2, 10, 100]
    # Divisors: 1, 2, 4
    # k=1: Not sortable.
    # k=2: [100,1],[10,2] vs [1,2],[10,100]. Block [100,1] vs [1,2]. Counter mismatch. Not sortable.
    # k=4: [100,1,10,2] vs [1,2,10,100]. Counters match. "1#2#10#100" in "100#1#10#2#100#1#10#2". Yes (shift 1).
    expected9 = 4
    assert s.sortableIntegers(nums9) == expected9, f"Test 9 Failed: Input: {nums9}, Expected: {expected9}, Got: {s.sortableIntegers(nums9)}"

    print("All tests passed!")

