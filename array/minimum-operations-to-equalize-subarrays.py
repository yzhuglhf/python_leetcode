"""
Minimum Operations to Equalize Subarrays
Difficulty: Hard

Description:
This problem asks us to find the minimum operations to make all elements in a given subarray `nums[li..ri]` equal. An operation consists of increasing or decreasing an element by `k`. If it's impossible, we return -1.

The key insight is that for elements `x` and `y` to be made equal using `±k` operations, they must have the same remainder when divided by `k` (i.e., `x % k == y % k`). If this condition is not met for any pair in the subarray, it's impossible. If it is met, we can transform each `nums[i]` to `q_i = nums[i] // k` (since `nums[i] - (nums[i] % k)` is a multiple of `k`). The problem then reduces to finding a target value `M` for the `q_i`'s such that `sum(|q_i - M|)` is minimized. This sum is minimized when `M` is the median of the `q_i` values in the subarray.

Example:
Input: nums = [1,4,7], k = 3, queries = [[0,1],[0,2]]
Output: [1,2]
For [0,1]: nums[0..1] = [1,4]. Both 1%3=1, 4%3=1. q_values are [1//3, 4//3] = [0,1]. Median is 0. Operations: |0-0| + |1-0| = 1.
For [0,2]: nums[0..2] = [1,4,7]. All 1%3=1. q_values are [1//3, 4//3, 7//3] = [0,1,2]. Median is 1. Operations: |0-1| + |1-1| + |2-1| = 1+0+1 = 2.

Approach:
1.  **Remainder Check Optimization**: Precompute an array `next_mismatch` where `next_mismatch[i]` stores the smallest index `j > i` such that `nums[j] % k != nums[i] % k`. If no such `j` exists, it's `n`. For a query `[li, ri]`, if `next_mismatch[li] <= ri`, it means there's a remainder mismatch in the range, so return -1. This step takes O(N) for precomputation and O(1) per query.
2.  **Median and Sum of Absolute Differences**: If the remainder check passes, we need to find the median `M` of the `q_i = nums[i] // k` values within `nums[li..ri]`, and then calculate `sum(|q_i - M|)`. This is a range median query and range sum query problem. A Persistent Segment Tree (PST) is well-suited for this.
    *   **Coordinate Compression**: Collect all `q_i` values, sort them, and assign ranks to unique values. The PST will operate on these ranks.
    *   **PST Construction**: Build `N+1` versions of a segment tree. `roots[0]` represents an empty set of `q_values`. `roots[i+1]` is created by taking `roots[i]` and adding `q_i` (its rank and value). Each node in the segment tree stores the `count` and `total_sum` of the `q_values` in its range. Construction takes `O(N log N)` time and space.
    *   **PST Query**: For a query `[li, ri]`:
        *   Determine the effective root nodes for the range: `root_ri = roots[ri+1]` and `root_li_minus_1 = roots[li]`.
        *   Find the median rank: Use `query_kth_smallest` on the PST to find the `(length - 1) // 2`-th smallest element's rank in the range `[li, ri]`. This is done by traversing the difference between `root_ri` and `root_li_minus_1`. Map this rank back to the actual median `q_value` (`M`).
        *   Calculate the sum of absolute differences: Use `query_stats` on the PST to find the sum and count of `q_values` strictly less than `M`, equal to `M`, and strictly greater than `M`. Let these be `(sum_less, count_less)`, `(sum_equal, count_equal)`, `(sum_greater, count_greater)`.
        *   The total operations will be `(M * count_less - sum_less) + (sum_greater - M * count_greater)`.
        Each query takes `O(log N)` time.

Time Complexity: O((N + Q) log N) due to PST construction and queries.
Space Complexity: O(N log N) for the Persistent Segment Tree.
"""
from typing import List, Optional

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.count = 0
        self.total_sum = 0

class PersistentSegmentTree:
    def __init__(self, max_val_rank):
        self.max_val_rank = max_val_rank
        # roots[0] is an effectively empty tree node
        self.roots = [self._create_empty_node()] 
        
    def _create_empty_node(self):
        # Returns a new Node with count=0, total_sum=0. Used as a placeholder for non-existent children.
        return Node()
        
    def _update(self, prev_node, low, high, idx, value):
        # Creates a new node that inherits values from prev_node and updates for idx
        new_node = Node()
        new_node.count = prev_node.count + 1
        new_node.total_sum = prev_node.total_sum + value

        if low == high: # Leaf node
            return new_node
        
        mid = (low + high) // 2
        if idx <= mid:
            # Recurse left, copy right child
            new_node.left = self._update(prev_node.left or self._create_empty_node(), low, mid, idx, value)
            new_node.right = prev_node.right
        else:
            # Copy left child, recurse right
            new_node.left = prev_node.left
            new_node.right = self._update(prev_node.right or self._create_empty_node(), mid + 1, high, idx, value)
        return new_node

    def add_version(self, prev_root_idx, q_rank, q_value):
        """Adds a new version of the segment tree based on the previous version,
        incorporating q_rank and q_value."""
        prev_root = self.roots[prev_root_idx]
        new_root = self._update(prev_root, 0, self.max_val_rank, q_rank, q_value)
        self.roots.append(new_root)

    def query_kth_smallest(self, root_ri, root_li_minus_1, k, low, high):
        """
        Finds the rank of the k-th smallest element (0-indexed k) in the range.
        root_ri: root node for elements up to ri
        root_li_minus_1: root node for elements up to li-1
        k: the 0-indexed rank of the element to find (e.g., k=0 for 1st smallest, median for (len-1)//2)
        low, high: current range of ranks this segment tree node represents
        """
        node_ri = root_ri
        node_li_minus_1 = root_li_minus_1

        while low < high:
            mid = (low + high) // 2
            
            # Count of elements in the left child's range [low, mid] for the subarray [li..ri]
            left_count_in_range = (node_ri.left.count if node_ri.left else 0) - \
                                  (node_li_minus_1.left.count if node_li_minus_1.left else 0)
            
            if k < left_count_in_range: # The k-th element is in the left subtree
                node_ri = node_ri.left or self._create_empty_node()
                node_li_minus_1 = node_li_minus_1.left or self._create_empty_node()
                high = mid
            else: # The k-th element is in the right subtree
                k -= left_count_in_range # Adjust k to be relative to the right subtree
                node_ri = node_ri.right or self._create_empty_node()
                node_li_minus_1 = node_li_minus_1.right or self._create_empty_node()
                low = mid + 1
        return low # Returns the rank of the k-th smallest element

    def _query_range_sum_count(self, node_ri, node_li_minus_1, current_low, current_high, target_low, target_high):
        """
        Helper to query sum and count for a specific value rank range [target_low, target_high]
        within the effective subarray defined by root_ri and root_li_minus_1.
        """
        # No overlap between current node's range and target range
        if current_low > target_high or current_high < target_low:
            return 0, 0 
        # Current node's range is fully contained within target range
        if target_low <= current_low and current_high <= target_high:
            return (node_ri.total_sum - node_li_minus_1.total_sum), \
                   (node_ri.count - node_li_minus_1.count)
        
        mid = (current_low + current_high) // 2
        
        sum_left, count_left = self._query_range_sum_count(node_ri.left or self._create_empty_node(),
                                                          node_li_minus_1.left or self._create_empty_node(),
                                                          current_low, mid, target_low, target_high)
        sum_right, count_right = self._query_range_sum_count(node_ri.right or self._create_empty_node(),
                                                            node_li_minus_1.right or self._create_empty_node(),
                                                            mid + 1, current_high, target_low, target_high)
        return sum_left + sum_right, count_left + count_right

    def query_stats(self, root_ri, root_li_minus_1, rank_M, max_rank):
        """
        Queries sum and count for elements less than, equal to, or greater than a given rank_M.
        """
        # Elements strictly less than rank_M
        sum_less_M, count_less_M = self._query_range_sum_count(root_ri, root_li_minus_1, 0, max_rank, 0, rank_M - 1)
        # Elements equal to rank_M
        sum_equal_M, count_equal_M = self._query_range_sum_count(root_ri, root_li_minus_1, 0, max_rank, rank_M, rank_M)
        # Elements strictly greater than rank_M
        sum_greater_M, count_greater_M = self._query_range_sum_count(root_ri, root_li_minus_1, 0, max_rank, rank_M + 1, max_rank)
        
        return sum_less_M, count_less_M, sum_equal_M, count_equal_M, sum_greater_M, count_greater_M


class Solution:
    def minOperations(self, nums: List[int], k: int, queries: List[List[int]]) -> List[int]:
        n = len(nums)
        ans = []

        # Step 1: Precompute next_mismatch for remainder check
        # next_mismatch[i] stores the smallest index j > i such that nums[j]%k != nums[i]%k.
        # If no such j exists, it's n.
        next_mismatch = [n] * n
        for i in range(n - 2, -1, -1):
            if (nums[i] % k) != (nums[i+1] % k):
                next_mismatch[i] = i + 1
            else:
                next_mismatch[i] = next_mismatch[i+1]

        # Step 2: Prepare data for Persistent Segment Tree (PST)
        q_values = [(num // k) for num in nums]
        
        # Coordinate compression for q_values
        q_values_sorted_unique = sorted(list(set(q_values)))
        if not q_values_sorted_unique: # Handle empty nums case, though constraints say n >= 1
            max_rank_coord = -1
            val_to_rank = {}
        else:
            max_rank_coord = len(q_values_sorted_unique) - 1
            val_to_rank = {val: i for i, val in enumerate(q_values_sorted_unique)}
        
        pst = PersistentSegmentTree(max_rank_coord)

        # Build PST versions
        for i in range(n):
            q_val = q_values[i]
            q_rank = val_to_rank[q_val]
            pst.add_version(i, q_rank, q_val) # Add version i+1 based on version i

        # Step 3: Process queries
        for li, ri in queries:
            # Remainder check
            if next_mismatch[li] <= ri:
                ans.append(-1)
                continue
            
            # If li == ri, no operations needed
            if li == ri:
                ans.append(0)
                continue

            length = ri - li + 1
            # For even length, median is typically (len/2 - 1)-th or (len/2)-th.
            # For odd length, median is (len-1)/2-th.
            # The problem of sum(|x_i - M|) is minimized by any median.
            # Using 0-indexed (length-1)//2 will always give the lower median for even length, and the unique median for odd length.
            kth_smallest_idx = (length - 1) // 2 

            # Get roots for the range [li, ri]
            root_ri = pst.roots[ri + 1]
            root_li_minus_1 = pst.roots[li]

            # Find the rank of the median value M
            median_rank = pst.query_kth_smallest(root_ri, root_li_minus_1, kth_smallest_idx, 0, max_rank_coord)
            median_q_value = q_values_sorted_unique[median_rank]

            # Query stats (sum and count) for values relative to the median
            sum_less_M, count_less_M, sum_equal_M, count_equal_M, sum_greater_M, count_greater_M = \
                pst.query_stats(root_ri, root_li_minus_1, median_rank, max_rank_coord)
            
            # Calculate total operations
            # All elements < M need (M - val) operations. Sum = M*count_less - sum_less
            # All elements > M need (val - M) operations. Sum = sum_greater - M*count_greater
            total_operations = (median_q_value * count_less_M - sum_less_M) + \
                               (sum_greater_M - median_q_value * count_greater_M)
            
            ans.append(total_operations)

        return ans


if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, 4, 7]
    k1 = 3
    queries1 = [[0, 1], [0, 2]]
    output1 = [1, 2]
    assert s.minOperations(nums1, k1, queries1) == output1, f"Test 1 failed. Expected: {output1}, Got: {s.minOperations(nums1, k1, queries1)}"

    # Example 2
    nums2 = [1, 2, 4]
    k2 = 2
    queries2 = [[0, 2], [0, 0], [1, 2]]
    output2 = [-1, 0, 1]
    assert s.minOperations(nums2, k2, queries2) == output2, f"Test 2 failed. Expected: {output2}, Got: {s.minOperations(nums2, k2, queries2)}"

    # Custom test case: all elements already equal
    nums3 = [5, 5, 5]
    k3 = 10
    queries3 = [[0, 2], [0, 0]]
    output3 = [0, 0]
    assert s.minOperations(nums3, k3, queries3) == output3, f"Test 3 failed. Expected: {output3}, Got: {s.minOperations(nums3, k3, queries3)}"

    # Custom test case: impossible remainder
    nums4 = [10, 11, 12]
    k4 = 2
    queries4 = [[0, 2]]
    output4 = [-1]
    assert s.minOperations(nums4, k4, queries4) == output4, f"Test 4 failed. Expected: {output4}, Got: {s.minOperations(nums4, k4, queries4)}"
    
    # Custom test case: large numbers, single element
    nums5 = [10**9, 10**9 + 5, 10**9 + 10]
    k5 = 5
    queries5 = [[0,0],[0,1],[1,2]]
    output5 = [0,1,1]
    assert s.minOperations(nums5, k5, queries5) == output5, f"Test 5 failed. Expected: {output5}, Got: {s.minOperations(nums5, k5, queries5)}"

    # Custom test case: large numbers, different k
    nums6 = [100, 103, 106, 110]
    k6 = 3
    queries6 = [[0, 2], [0, 3]]
    # [100, 103, 106] -> q_values [33, 34, 35]. Median 34. |33-34| + |34-34| + |35-34| = 1+0+1 = 2.
    # [100, 103, 106, 110] -> 110%3 = 2, others %3 = 1. Mismatch.
    output6 = [2, -1]
    assert s.minOperations(nums6, k6, queries6) == output6, f"Test 6 failed. Expected: {output6}, Got: {s.minOperations(nums6, k6, queries6)}"

    print("All tests passed!")