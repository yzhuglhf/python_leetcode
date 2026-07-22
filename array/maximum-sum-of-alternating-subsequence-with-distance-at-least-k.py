"""
Maximum Sum of Alternating Subsequence With Distance at Least K
Difficulty: Hard

Description:
This problem asks for the maximum sum of a subsequence of `nums` where consecutive elements `nums[it]` and `nums[it+1]` satisfy `it+1 - it >= k` and are strictly alternating (e.g., `a < b > c < d` or `a > b < c > d`). A single-element subsequence is considered strictly alternating. The goal is to find the maximum possible score (sum of selected values).

Example:
Input: nums = [3,5,4,2,4], k = 1
Output: 14
Explanation: The subsequence [3, 5, 2, 4] formed by indices [0, 1, 3, 4] satisfies the conditions: `1-0=1>=k`, `3-1=2>=k`, `4-3=1>=k`. The values alternate `3 < 5 > 2 < 4`. The sum is 3+5+2+4=14.

Approach:
This problem can be solved using dynamic programming combined with two segment trees for efficient range maximum queries. We maintain two DP arrays, `dp_less[i]` and `dp_greater[i]`, representing the maximum sum of an alternating subsequence ending at `nums[i]` where `nums[i]` is a "valley" (strictly less than its predecessor) or a "peak" (strictly greater than its predecessor), respectively. For each index `i`, `dp_less[i]` can be `nums[i]` itself (as a subsequence of length 1), or `nums[i]` plus the maximum `dp_greater[j]` (where `nums[j] > nums[i]`) for any valid preceding index `j` such that `j <= i-k`. Similarly, `dp_greater[i]` can be `nums[i]` or `nums[i]` plus the maximum `dp_less[j]` (where `nums[j] < nums[i]`) for any `j <= i-k`.

To efficiently find the required maximum `dp_greater[j]` or `dp_less[j]` values over a value range and subject to the `j <= i-k` index constraint, we use two segment trees. `seg_tree_for_less_val` stores the maximum `dp_less` scores for each possible value `v` that can be a valley, and `seg_tree_for_greater_val` stores maximum `dp_greater` scores for values `v` that can be peaks. The `j <= i-k` sliding window condition is handled by a two-phase process for each `i`: first, if `i-k` is a valid index, we update the segment trees with `dp_less[i-k]` and `dp_greater[i-k]`. This makes `dp` values from `i-k` available for queries at `i`. Second, we calculate `dp_less[i]` and `dp_greater[i]` by querying these segment trees based on `nums[i]`'s value. The final answer is the maximum value found across all `dp_less[i]` and `dp_greater[i]`.

Time Complexity: O(N * log(MAX_VAL)), where N is the length of `nums` and MAX_VAL is the maximum possible value in `nums` (10^5). Each of N iterations involves a constant number of segment tree updates and queries, each taking O(log(MAX_VAL)) time.
Space Complexity: O(N + MAX_VAL), for storing the DP arrays and the two segment trees.
"""
from typing import List, Optional

class SegmentTree:
    def __init__(self, size):
        # size: The upper bound of values + 1 (e.g., for values 1 to 10^5, size = 100001)
        self.size = size
        # The tree array requires 2*size for a complete binary tree where leaves store values
        # Initialize with -float('inf') to correctly handle max queries when no valid elements are present
        self.tree = [-float('inf')] * (2 * size)

    def update(self, pos, val):
        # Go to the leaf node corresponding to 'pos' (the value itself)
        # We need to take the maximum if there are multiple updates for the same position,
        # ensuring the segment tree always stores the best score for a given value.
        pos += self.size
        self.tree[pos] = max(self.tree[pos], val)
        # Propagate changes up to the root, updating parent nodes
        while pos > 1:
            pos //= 2
            self.tree[pos] = max(self.tree[pos * 2], self.tree[pos * 2 + 1])

    def query(self, l, r):
        # Query the maximum value in the range [l, r] (inclusive)
        # If the range is invalid (l > r), return -float('inf')
        if l > r:
            return -float('inf')
        
        # Adjust indices to point to leaf nodes in the segment tree's internal representation
        l += self.size
        r += self.size
        res = -float('inf')
        
        # Traverse up the tree to cover the query range
        while l <= r:
            if l % 2 == 1:  # If l is a right child, its parent is not fully covered, so include l's value
                res = max(res, self.tree[l])
                l += 1 # Move to its right sibling for the next iteration (parent's right child)
            if r % 2 == 0:  # If r is a left child, its parent is not fully covered, so include r's value
                res = max(res, self.tree[r])
                r -= 1 # Move to its left sibling for the next iteration (parent's left child)
            l //= 2 # Move to parent
            r //= 2 # Move to parent
        return res

class Solution:
    def maxAlternatingSum(self, nums: List[int], k: int) -> int:
        N = len(nums)
        MAX_NUM_VAL = 100000 # Constraints: 1 <= nums[i] <= 10^5
        
        # dp_less[i]: max sum ending at nums[i], where nums[i] is a "valley" (strictly smaller than its predecessor)
        dp_less = [0] * N
        # dp_greater[i]: max sum ending at nums[i], where nums[i] is a "peak" (strictly greater than its predecessor)
        dp_greater = [0] * N

        # Segment trees to store max dp scores for specific values.
        # `size = MAX_NUM_VAL + 1` handles value range from 0 to MAX_NUM_VAL.
        # We query for `nums[i]` values typically in `[1, MAX_NUM_VAL]`.
        seg_tree_for_less_val = SegmentTree(MAX_NUM_VAL + 1)
        seg_tree_for_greater_val = SegmentTree(MAX_NUM_VAL + 1)

        ans = 0 # Since nums[i] >= 1, any valid subsequence sum will be positive. Initializing with 0 is safe.

        for i in range(N):
            current_num = nums[i]

            # Phase 1: Update segment trees with dp values from index `i-k`.
            # These values represent potential preceding elements that are now far enough
            # (distance >= k) from `current_num` to be included in a subsequence.
            if i - k >= 0:
                # We update the segment trees at `nums[i-k]` with `dp_less[i-k]` and `dp_greater[i-k]`.
                # The `update` method internally takes the maximum, so if multiple indices have
                # the same value `nums[i-k]`, the tree stores the best `dp` score for that value.
                seg_tree_for_less_val.update(nums[i-k], dp_less[i-k])
                seg_tree_for_greater_val.update(nums[i-k], dp_greater[i-k])

            # Phase 2: Calculate dp_less[i] and dp_greater[i] for the current index `i`.

            # Option 1: `current_num` forms a subsequence of length 1.
            # In this case, it can be considered both a "valley" and a "peak" as it has no predecessor.
            current_val_as_less_score = current_num
            current_val_as_greater_score = current_num

            # Option 2: `current_num` extends a previous alternating subsequence.

            # If `current_num` is a "valley" (i.e., `nums[j] > current_num` for some `j`):
            # We need to find the maximum `dp_greater[j]` from available previous elements `j <= i-k`
            # where `nums[j]` is strictly greater than `current_num`.
            # Query range for values: `(current_num, MAX_NUM_VAL]`
            prev_peak_max_score = seg_tree_for_greater_val.query(current_num + 1, MAX_NUM_VAL)
            if prev_peak_max_score != -float('inf'):
                current_val_as_less_score = max(current_val_as_less_score, current_num + prev_peak_max_score)
            
            dp_less[i] = current_val_as_less_score

            # If `current_num` is a "peak" (i.e., `nums[j] < current_num` for some `j`):
            # We need to find the maximum `dp_less[j]` from available previous elements `j <= i-k`
            # where `nums[j]` is strictly less than `current_num`.
            # Query range for values: `[1, current_num - 1]`
            prev_valley_max_score = seg_tree_for_less_val.query(1, current_num - 1)
            if prev_valley_max_score != -float('inf'):
                current_val_as_greater_score = max(current_val_as_greater_score, current_num + prev_valley_max_score)
            
            dp_greater[i] = current_val_as_greater_score
            
            # Update the overall maximum score found so far
            ans = max(ans, dp_less[i], dp_greater[i])
            
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [5,4,2]
    k1 = 2
    assert s.maxAlternatingSum(nums1, k1) == 7, f"Test 1 Failed: {s.maxAlternatingSum(nums1, k1)}"
    
    # Example 2
    nums2 = [3,5,4,2,4]
    k2 = 1
    assert s.maxAlternatingSum(nums2, k2) == 14, f"Test 2 Failed: {s.maxAlternatingSum(nums2, k2)}"
    
    # Example 3
    nums3 = [5]
    k3 = 1
    assert s.maxAlternatingSum(nums3, k3) == 5, f"Test 3 Failed: {s.maxAlternatingSum(nums3, k3)}"

    # Custom test case: longer sequence, varying k
    nums4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k4 = 2
    # Possible sequence: [1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8, 7, 9, 8, 10] - but distance is hard.
    # Try alternating: 1 < 3 > 2 < 4 > 3 < 5 > 4 < 6 > 5 < 7 > 6 < 8 > 7 < 9 > 8 < 10
    # Or start high: 10 > 8 < 9 > 7 < 8 ...
    # Simple increasing subsequence (distance k=2): [1, 3, 5, 7, 9] sum=25
    # Simple decreasing subsequence (distance k=2): [10, 8, 6, 4, 2] sum=30
    # Alternating: [1, 3] sum 4, [1, 4] sum 5 etc.
    # [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10] (indices 0,4,1,5,2,6,3,7,4,8,5,9) This is not right.
    # We want indices: 0 <= i1 < i2 < ... < im < n
    # Consider [1, 3, 2, 5, 4, 7, 6, 9, 8, 10]
    # Indices: [0,2,1,4,3,6,5,8,7,9]
    # Values: nums[0]=1, nums[2]=3 (1<3)
    # Then previous index for nums[1]=2 is 2 (2-1=1<k=2, not allowed)
    # The simple optimal is often picking highest and then next highest valid distance, or similar.
    # For [1,2,3,4,5,6,7,8,9,10] k=2:
    # Max sum: [10] = 10
    # [9, 10] fails distance. [8] = 8.
    # [10, 8] -> 18
    # [10, 8, 6] -> 24
    # [10, 8, 6, 4] -> 28
    # [10, 8, 6, 4, 2] -> 30 (indices [9,7,5,3,1]) 10>8<9>7<8... No, 10>8>6>4>2, this is not alternating
    # Must be strictly alternating!
    # A single element is strictly alternating. Max single: 10.
    # 1 < 3 (index 0,2) sum 4.
    # 1 < 4 (index 0,3) sum 5.
    # 1 < 5 (index 0,4) sum 6.
    # ...
    # 1 < 10 (index 0,9) sum 11.
    # 10 > 8 (index 9,7) sum 18.
    # Try [1, 5, 3, 7, 4, 9, 6]
    # Indices: [0,4,2,6,3,8,5]
    # Values: [1, 5, 3, 7, 4, 9, 6]
    # 1 < 5 (index diff 4 >= 2)
    # 5 > 3 (index diff 2 >= 2)
    # 3 < 7 (index diff 4 >= 2)
    # 7 > 4 (index diff 3 >= 2)
    # 4 < 9 (index diff 5 >= 2)
    # 9 > 6 (index diff 3 >= 2)
    # Sum: 1+5+3+7+4+9+6 = 35.
    assert s.maxAlternatingSum(nums4, k4) == 35, f"Test 4 Failed: {s.maxAlternatingSum(nums4, k4)}" # Calculated this manually

    nums5 = [10, 1, 2, 11, 3, 4, 12, 5, 6, 13]
    k5 = 2
    # [10] sum 10
    # [10, 1] no, 10 > 1. 1-0=1 < 2
    # [10, 2] no, 10 > 2. 2-0=2 >= 2. sum 12
    # [10, 2, 3] no. 2<3. 3-2=1 < 2
    # [10, 2, 11] (indices 0,2,3) 10>2<11. 3-2=1 < 2. No.
    # [10, 2, 4] (indices 0,2,5) 10>2<4. 5-2=3 >= 2. sum 16
    # [10, 2, 4, 12] (indices 0,2,5,6) 10>2<4<12 No.
    # [10, 2, 4, 6] (indices 0,2,5,8) 10>2<4<6 No.
    # [10, 2, 12] (indices 0,2,6) 10>2<12. 6-2=4 >= 2. sum 24
    # [10, 2, 12, 5] (indices 0,2,6,7) 10>2<12>5. 7-6=1 < 2. No.
    # [10, 2, 12, 6] (indices 0,2,6,8) 10>2<12>6. 8-6=2 >= 2. sum 30
    # [10, 2, 12, 6, 13] (indices 0,2,6,8,9) 10>2<12>6<13. 9-8=1 < 2. No.
    # Let's check a sequence from example: [3, 5, 2, 4] indices [0,1,3,4] for k=1.
    # Values: nums[0]=3, nums[1]=5 (3<5)
    # nums[3]=2 (5>2)
    # nums[4]=4 (2<4)
    # Score 3+5+2+4=14.
    # For nums5 and k=2:
    # Option 1: Start high.
    # [13] = 13
    # [13, 6] (idx 9,8) 13>6. 9-8=1 < 2. No.
    # [13, 5] (idx 9,7) 13>5. 9-7=2 >= 2. Sum 18.
    # [13, 5, 12] (idx 9,7,6) 13>5<12. 7-6=1 < 2. No.
    # [13, 5, 11] (idx 9,7,3) 13>5<11. 9-7=2, 7-3=4. Sum 29.
    # [13, 5, 11, 2] (idx 9,7,3,2) 13>5<11>2. 3-2=1 < 2. No.
    # [13, 5, 11, 1] (idx 9,7,3,1) 13>5<11>1. 3-1=2 >= 2. Sum 30.
    # This seems like a strong candidate: 13+5+11+1 = 30.
    # Let's try [10, 3, 11, 4, 12, 5, 13, 6]
    # Indices: [0,4,3,5,6,7,9,8]
    # Values: [10,3,11,4,12,5,13,6]
    # 10 > 3 (4-0 = 4 >= 2)
    # 3 < 11 (3-4 = -1 < 0. No.)
    # The current approach correctly handles this with `max` logic.
    assert s.maxAlternatingSum(nums5, k5) == 30, f"Test 5 Failed: {s.maxAlternatingSum(nums5, k5)}"

    print("All tests passed!")

```