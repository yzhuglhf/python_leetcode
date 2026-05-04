"""
K-th Smallest Remaining Even Integer in Subarray Queries
Difficulty: Hard

Description:
For each query [li, ri, ki], consider the subarray nums[li..ri]. From the infinite sequence of positive even integers, remove all elements that appear in this subarray. The goal is to find the ki-th smallest integer remaining in the modified sequence.

Example:
Input: nums = [1,4,7], queries = [[0,2,1],[1,1,2],[0,0,3]]
Output: [2,6,6]

Approach:
The problem requires finding the k-th smallest element in a dynamically modified sequence. This often suggests a binary search on the answer. Let the target k-th remaining even integer be X. X must be an even number, say X = 2*M. The count of all positive even integers less than or equal to X is M. We need to find the smallest M such that after removing certain even numbers, M minus the count of removed even numbers less than or equal to X is at least ki.
The `check(M)` function for binary search would determine the total count of removed even integers that are less than or equal to `2*M` and are present in `nums[li..ri]`. Let this count be `C`. If `M - C >= ki`, then `2*M` is a potential answer, and we try for a smaller `M`. Otherwise, `M` is too small, and we need a larger `M`.
To efficiently calculate `C`, we need to count even numbers within a specific range `[actual_l, actual_r]` of `nums`, where `actual_l = li` and `actual_r = min(ri, bisect_right(nums, 2*M) - 1)`. This is a range sum query, which can be optimized using a Segment Tree. The Segment Tree is pre-built on `nums` to store a 1 at index `i` if `nums[i]` is even, and 0 otherwise. A query on the Segment Tree then returns the count of even numbers in `nums` within the specified index range.
The binary search on `M` takes `O(log(MAX_M))` iterations, where `MAX_M` is `ki + N` (N being `len(nums)`). Each iteration involves `bisect_right` (O(log N)) and a Segment Tree query (O(log N)). Thus, each query is processed in `O(log(MAX_M) * log N)`. Total time complexity is `O(N + Q * log(MAX_M) * log N)` due to Segment Tree build and query processing.

Time Complexity: O(N + Q * log(MAX_M) * log N), where N is `len(nums)`, Q is `len(queries)`, and MAX_M is approximately `max(ki) + N`.
Space Complexity: O(N) for the Segment Tree.
"""
from typing import List
from bisect import bisect_right

class SegmentTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        # Tree size: 4 * n is a common safe upper bound for segment tree arrays
        self.tree = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, start: int, end: int):
        """
        Recursively builds the segment tree.
        node: current node index in self.tree
        start, end: range of indices in arr covered by current node
        """
        if start == end:
            # Leaf node: store 1 if arr[start] is even, else 0
            self.tree[node] = 1 if arr[start] % 2 == 0 else 0
        else:
            mid = (start + end) // 2
            # Build left child
            self._build(arr, 2 * node + 1, start, mid)
            # Build right child
            self._build(arr, 2 * node + 2, mid + 1, end)
            # Internal node stores the sum of its children
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """
        Queries the segment tree for the sum of values (count of evens) in range [l, r].
        node: current node index in self.tree
        start, end: range of indices in arr covered by current node
        l, r: query range
        """
        # If the current segment is outside the query range, return 0
        if r < start or end < l:
            return 0
        
        # If the current segment is completely within the query range, return its stored value
        if l <= start and end <= r:
            return self.tree[node]
        
        # If the current segment partially overlaps, recurse on children and sum results
        mid = (start + end) // 2
        p1 = self.query(2 * node + 1, start, mid, l, r)
        p2 = self.query(2 * node + 2, mid + 1, end, l, r)
        return p1 + p2


class Solution:
    def kthRemainingInteger(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # Pre-build a segment tree to count even numbers in ranges of `nums`
        seg_tree = SegmentTree(nums)

        results = []
        for li, ri, ki in queries:
            # Binary search for 'M', where 2*M is the k-th smallest remaining even integer.
            # 'M' represents the index of the even number in the infinite sequence of evens.
            # The smallest possible M is 1 (for 2).
            # The largest possible M could be ki + N, where N is the maximum number of evens
            # that could be removed from nums. If all N numbers in nums are even and removed,
            # we would need to find the (ki + N)-th overall even number.
            low_M = 1
            high_M = ki + n # Upper bound for M (N = len(nums))
            
            ans_M = high_M # Initialize with a default answer, will be updated to smallest valid M

            while low_M <= high_M:
                mid_M = low_M + (high_M - low_M) // 2
                current_X = 2 * mid_M # The even number corresponding to mid_M

                # Find the effective range in `nums` that contains elements <= current_X
                # bisect_right returns the insertion point for current_X,
                # so -1 gives the index of the largest element <= current_X.
                idx_upper_bound_val = bisect_right(nums, current_X) - 1

                # The actual range in `nums` to consider for removals is intersection of:
                # 1. The query range [li, ri]
                # 2. The range of elements in `nums` that are <= current_X (i.e., [0, idx_upper_bound_val])
                actual_l = li
                actual_r = min(ri, idx_upper_bound_val)

                count_removed_evens = 0
                if actual_l <= actual_r: # Ensure the effective range is valid
                    # Use the segment tree to count even numbers in the derived range [actual_l, actual_r]
                    count_removed_evens = seg_tree.query(0, 0, n - 1, actual_l, actual_r)
                
                # Calculate the count of remaining even integers less than or equal to current_X.
                # Total even numbers up to current_X is mid_M.
                num_remaining_evens_le_X = mid_M - count_removed_evens

                if num_remaining_evens_le_X >= ki:
                    # current_X (which is 2 * mid_M) satisfies the condition (or is larger than needed).
                    # This means it's a potential answer. Try to find a smaller M.
                    ans_M = mid_M
                    high_M = mid_M - 1
                else:
                    # current_X is too small; not enough remaining even numbers.
                    # Need to look for a larger M.
                    low_M = mid_M + 1
            
            # The k-th smallest remaining even integer is 2 * ans_M.
            results.append(2 * ans_M)
        
        return results

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, 4, 7]
    queries1 = [[0, 2, 1], [1, 1, 2], [0, 0, 3]]
    expected1 = [2, 6, 6]
    assert s.kthRemainingInteger(nums1, queries1) == expected1, f"Test 1 Failed: Expected {expected1}, Got {s.kthRemainingInteger(nums1, queries1)}"

    # Example 2
    nums2 = [2, 5, 8]
    queries2 = [[0, 1, 2], [1, 2, 1], [0, 2, 4]]
    expected2 = [6, 2, 12]
    assert s.kthRemainingInteger(nums2, queries2) == expected2, f"Test 2 Failed: Expected {expected2}, Got {s.kthRemainingInteger(nums2, queries2)}"

    # Example 3
    nums3 = [3, 6]
    queries3 = [[0, 1, 1], [1, 1, 3]]
    expected3 = [2, 8]
    assert s.kthRemainingInteger(nums3, queries3) == expected3, f"Test 3 Failed: Expected {expected3}, Got {s.kthRemainingInteger(nums3, queries3)}"

    # Additional test cases:
    # No evens in nums
    nums4 = [1, 3, 5]
    queries4 = [[0, 2, 1], [0, 2, 5]]
    expected4 = [2, 10] 
    assert s.kthRemainingInteger(nums4, queries4) == expected4, f"Test 4 Failed: Expected {expected4}, Got {s.kthRemainingInteger(nums4, queries4)}"

    # All evens in nums
    nums5 = [2, 4, 6]
    queries5 = [[0, 2, 1], [0, 2, 2], [0, 2, 3]]
    # Subarray [2,4,6]. Removed [2,4,6]. Remaining evens: 8, 10, 12...
    expected5 = [8, 10, 12]
    assert s.kthRemainingInteger(nums5, queries5) == expected5, f"Test 5 Failed: Expected {expected5}, Got {s.kthRemainingInteger(nums5, queries5)}"

    # Larger numbers and ki
    nums6 = [100000000, 200000000, 300000000]
    queries6 = [[0, 2, 1], [0, 2, 1000]]
    expected6 = [2, 2000] 
    assert s.kthRemainingInteger(nums6, queries6) == expected6, f"Test 6 Failed: Expected {expected6}, Got {s.kthRemainingInteger(nums6, queries6)}"

    # Mixed evens and odds, various query ranges
    nums7 = [1, 2, 3, 4, 5, 6]
    queries7 = [[0, 0, 1], # nums[0]=1, no evens removed. 1st is 2.
                [2, 2, 2], # nums[2]=3, no evens removed. 2nd is 4.
                [0, 5, 1], # nums[0..5]=[1,2,3,4,5,6]. Removed [2,4,6]. Remaining 1st is 8.
                [0, 5, 2]] # nums[0..5]=[1,2,3,4,5,6]. Removed [2,4,6]. Remaining 2nd is 10.
    expected7 = [2, 4, 8, 10]
    assert s.kthRemainingInteger(nums7, queries7) == expected7, f"Test 7 Failed: Expected {expected7}, Got {s.kthRemainingInteger(nums7, queries7)}"

    print("All tests passed!")
