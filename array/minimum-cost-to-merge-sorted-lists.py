"""
Minimum Cost to Merge Sorted Lists
Difficulty: Hard

Description:
This problem asks for the minimum total cost to merge N sorted lists into a single sorted list. The cost of merging two lists, A and B, is defined as len(A) + len(B) + abs(median(A) - median(B)). The problem constraints specify a small number of initial lists (N <= 12) but potentially large list lengths, with the total sum of lengths not exceeding 2000.

Example:
Input: lists = [[1,3,5],[2,4],[6,7,8]]
Output: 18
Explanation:
Merge a = [1, 3, 5] and b = [2, 4]:
	len(a) = 3 and len(b) = 2
	median(a) = 3 and median(b) = 2
	cost = 3 + 2 + abs(3 - 2) = 6
So lists becomes [[1, 2, 3, 4, 5], [6, 7, 8]].

Merge a = [1, 2, 3, 4, 5] and b = [6, 7, 8]:
	len(a) = 5 and len(b) = 3
	median(a) = 3 and median(b) = 7
	cost = 5 + 3 + abs(3 - 7) = 12
So lists becomes [[1, 2, 3, 4, 5, 6, 7, 8]], and total cost is 6 + 12 = 18.

Approach:
Given the small number of initial lists (N <= 12), a dynamic programming approach with bitmasking is suitable. We define `dp[mask]` to store a tuple `(min_cost, merged_list)`, where `min_cost` is the minimum cost to merge the lists represented by the set bits in `mask`, and `merged_list` is the actual sorted list resulting from this minimum cost merge.

The base cases are `dp[1 << i] = (0, lists[i])` for each initial list `lists[i]`, as merging a single list has no cost and results in itself.
For any `mask` representing a set of lists, we iterate through all possible ways to partition this `mask` into two non-empty disjoint submasks, `submask1` and `submask2`, such that `submask1 | submask2 = mask`. To ensure each distinct partition `(submask1, submask2)` is considered exactly once and avoid redundant calculations (e.g., `(submask1, submask2)` vs `(submask2, submask1)`), we can enforce that `submask1` must always contain the least significant bit (LSB) of `mask`.

For each valid partition (`submask1`, `submask2`):
1. Recursively retrieve or calculate `(cost1, list1) = dp[submask1]` and `(cost2, list2) = dp[submask2]` using memoization.
2. Calculate the merge cost for `list1` and `list2`: `current_merge_cost = len(list1) + len(list2) + abs(median(list1) - median(list2))`.
3. The total cost for this particular split is `cost1 + cost2 + current_merge_cost`.
4. If this total cost is less than the current minimum recorded for `dp[mask]`, update `dp[mask]` with this new minimum cost and the result of merging `list1` and `list2`.

The `median` of an array `arr` is defined as `arr[(len(arr) - 1) // 2]`. A helper function `merge_two_sorted_lists` efficiently combines two sorted lists in linear time. Memoization (`memo` dictionary) stores and retrieves previously computed `dp[mask]` values to avoid re-computation.

Time Complexity: O(3^N * L), where N is the number of initial lists (at most 12) and L is the maximum total length of elements in any merged list (sum of initial list lengths, at most 2000). There are 2^N possible bitmask states. For each mask, iterating through its valid partitions involves `2^(count_set_bits(mask)-1)` choices. Summing these over all masks results in O(3^N) state transitions. Each transition involves merging two lists, which takes O(L) time in the worst case.
Space Complexity: O(2^N * L), for storing `(cost, merged_list)` tuples in the `memo` dictionary. There are 2^N states, and each `merged_list` can contain up to L elements.
"""
from typing import List, Optional

class Solution:
    def merge_two_sorted_lists(self, list1: List[int], list2: List[int]) -> List[int]:
        """
        Merges two sorted lists into a single sorted list.
        """
        merged = []
        ptr1, ptr2 = 0, 0
        n1, n2 = len(list1), len(list2)

        while ptr1 < n1 and ptr2 < n2:
            if list1[ptr1] <= list2[ptr2]:
                merged.append(list1[ptr1])
                ptr1 += 1
            else:
                merged.append(list2[ptr2])
                ptr2 += 1
        
        # Add remaining elements from list1, if any
        merged.extend(list1[ptr1:])
        # Add remaining elements from list2, if any
        merged.extend(list2[ptr2:])
        
        return merged

    def get_median_value(self, arr: List[int]) -> int:
        """
        Calculates the median of a sorted list according to the problem definition.
        Median is the left middle element.
        For length 1, index (1-1)//2 = 0.
        For length 2, index (2-1)//2 = 0.
        For length 3, index (3-1)//2 = 1.
        """
        length = len(arr)
        return arr[(length - 1) // 2]

    def minMergeCost(self, lists: List[List[int]]) -> int:
        N = len(lists)
        self.lists = lists  # Store initial lists for easy access in the recursive function
        memo = {}           # Memoization table: mask -> (min_cost, merged_list)

        def solve(mask):
            """
            Recursive function to find the minimum cost to merge lists indicated by 'mask'.
            Returns a tuple: (minimum total cost, the resulting merged sorted list).
            """
            if mask in memo:
                return memo[mask]

            # Base case: if mask represents a single initial list
            # A mask has only one bit set if mask & (mask - 1) == 0
            if (mask & (mask - 1)) == 0:
                # Find the 0-indexed position of the set bit
                idx = (mask).bit_length() - 1
                return (0, self.lists[idx])  # Cost is 0 for an initial list, result is the list itself

            min_total_cost = float('inf')
            res_list = None

            # Iterate over all proper submasks of 'mask' for submask1
            # To ensure unique splits (submask1, submask2) and avoid (submask2, submask1),
            # we enforce that submask1 must contain the least significant bit (LSB) of 'mask'.
            lsb_mask = mask & -mask  # Extracts the LSB bit of mask (e.g., for binary 01100, lsb_mask is 00100)

            # Iterate submask1 from `mask-1` downwards using bit manipulation.
            # `(submask1_iter - 1) & mask` efficiently generates all proper submasks in decreasing order.
            submask1_iter = (mask - 1) & mask
            while submask1_iter > 0:
                # Check if submask1_iter contains the LSB of 'mask'.
                # This ensures that for each partition {A, B} of `mask`, only one of (A, B) or (B, A) is processed.
                if (submask1_iter & lsb_mask) != 0:
                    part1_mask = submask1_iter
                    part2_mask = mask ^ part1_mask # part2_mask is the complement, containing remaining bits

                    # Recursively get costs and lists for the two parts
                    cost1, list1 = solve(part1_mask)
                    cost2, list2 = solve(part2_mask)

                    # Calculate current merge cost for these two lists
                    len1 = len(list1)
                    len2 = len(list2)
                    median1 = self.get_median_value(list1)
                    median2 = self.get_median_value(list2)
                    
                    current_merge_cost = len1 + len2 + abs(median1 - median2)
                    total_cost_for_split = cost1 + cost2 + current_merge_cost

                    # Update minimum if this split yields a lower total cost
                    if total_cost_for_split < min_total_cost:
                        min_total_cost = total_cost_for_split
                        res_list = self.merge_two_sorted_lists(list1, list2)
                
                # Move to the next smaller proper submask
                submask1_iter = (submask1_iter - 1) & mask
            
            memo[mask] = (min_total_cost, res_list)
            return min_total_cost, res_list
        
        # The final mask represents all initial lists merged into one.
        final_mask = (1 << N) - 1
        result_cost, _ = solve(final_mask)
        return result_cost

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.minMergeCost(lists=[[1,3,5],[2,4],[6,7,8]]) == 18

    # Example 2
    assert s.minMergeCost(lists=[[1,1,5],[1,4,7,8]]) == 10

    # Example 3
    assert s.minMergeCost(lists=[[1],[3]]) == 4

    # Example 4
    assert s.minMergeCost(lists=[[1],[1]]) == 2

    # Custom test case: 4 lists
    # L0=[1], L1=[10], L2=[20], L3=[30]
    # Merge L0,L1: 1+1+abs(1-10) = 2+9=11. M01=[1,10], med=1
    # Merge L2,L3: 1+1+abs(20-30)=2+10=12. M23=[20,30], med=20
    # Merge M01,M23: 2+2+abs(1-20)=4+19=23. M0123=[1,10,20,30], med=10
    # Total = 11+12+23 = 46

    # Another path:
    # Merge L0,L2: 1+1+abs(1-20)=2+19=21. M02=[1,20], med=1
    # Merge L1,L3: 1+1+abs(10-30)=2+20=22. M13=[10,30], med=10
    # Merge M02,M13: 2+2+abs(1-10)=4+9=13. M0123=[1,10,20,30], med=10
    # Total = 21+22+13 = 56. (Higher)

    # Another path:
    # Merge L0,L3: 1+1+abs(1-30)=2+29=31. M03=[1,30], med=1
    # Merge L1,L2: 1+1+abs(10-20)=2+10=12. M12=[10,20], med=10
    # Merge M03,M12: 2+2+abs(1-10)=4+9=13. M0123=[1,10,20,30], med=10
    # Total = 31+12+13 = 56. (Higher)
    assert s.minMergeCost(lists=[[1],[10],[20],[30]]) == 46
    
    # Larger lists, 3 elements
    assert s.minMergeCost(lists=[[1,2],[10,11],[20,21]]) == 2 + 2 + abs(1-10) + 4 + 2 + abs(2-20) == 4+9 + 6+18 == 13+24 == 37

    # This calculation path for 3 lists [[1,2],[10,11],[20,21]]:
    # L0=[1,2] med=1, len=2
    # L1=[10,11] med=10, len=2
    # L2=[20,21] med=20, len=2

    # Path 1: (L0,L1) -> M01. Then (M01,L2) -> Final
    #   (L0,L1) merge cost: len(L0)+len(L1)+abs(med(L0)-med(L1)) = 2+2+abs(1-10) = 4+9=13
    #   M01=[1,2,10,11], len=4, med=2
    #   (M01,L2) merge cost: len(M01)+len(L2)+abs(med(M01)-med(L2)) = 4+2+abs(2-20) = 6+18=24
    #   Total = 13+24 = 37

    # Path 2: (L1,L2) -> M12. Then (L0,M12) -> Final
    #   (L1,L2) merge cost: len(L1)+len(L2)+abs(med(L1)-med(L2)) = 2+2+abs(10-20) = 4+10=14
    #   M12=[10,11,20,21], len=4, med=11
    #   (L0,M12) merge cost: len(L0)+len(M12)+abs(med(L0)-med(M12)) = 2+4+abs(1-11) = 6+10=16
    #   Total = 14+16 = 30
    assert s.minMergeCost(lists=[[1,2],[10,11],[20,21]]) == 30

    print("All tests passed!")

