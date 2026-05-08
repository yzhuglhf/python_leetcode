import sys
from typing import List, Optional

# Increase recursion limit for potentially deep segment trees.
# A segment tree with N leaves has depth log N. Max N is 10^5, log2(10^5) is approximately 17.
# The recursion depth for a single update or query is O(log N).
# While typical Python recursion limits (e.g., 1000) are often sufficient, a higher limit
# is set for safety in competitive programming contexts, especially for "Hard" problems.
sys.setrecursionlimit(2 * 10**5) 

class Node:
    """
    Represents a node in the segment tree.
    Each node stores the count of elements and the sum of their values within its range.
    """
    def __init__(self, count=0, sum_val=0, left=None, right=None):
        self.count = count       # Number of elements in this node's range
        self.sum_val = sum_val   # Sum of values of elements in this node's range
        self.left = left         # Left child node
        self.right = right       # Right child node

class PersistentSegmentTree:
    """
    A Persistent Segment Tree implementation to query sum and count over ranges
    of an array's values for specific array index ranges.
    """
    def __init__(self, max_coord_value):
        """
        Initializes the Persistent Segment Tree.
        max_coord_value: The maximum possible value that can be stored in the tree.
                         The segment tree will cover the value range [0, max_coord_value].
        """
        self.max_coord_value = max_coord_value
        # roots[i] stores the root of the segment tree version after processing
        # elements from index 0 up to (i-1) of the input array.
        # roots[0] is an empty segment tree.
        self.roots = [self._build_empty_node(0, self.max_coord_value)] 

    def _build_empty_node(self, low, high):
        """Helper to create an empty node, used for initializing paths in updates."""
        return Node()

    def _update(self, prev_node: Node, low: int, high: int, index: int, val_to_add: int) -> Node:
        """
        Creates a new version of the segment tree by adding a value at a specific index.
        This function is recursive and creates new nodes only on the path from the root
        to the updated leaf, sharing other parts with the previous tree version.

        Args:
            prev_node: The root of the previous version of the segment tree.
            low, high: The range of values covered by the current segment tree node.
            index: The specific value (mapped_P[k]) to add/update.
            val_to_add: The actual value (mapped_P[k]) to add to the sum.

        Returns:
            The root of the new version of the segment tree.
        """
        # Create a new node, copying data from the previous node
        new_node = Node(prev_node.count, prev_node.sum_val, prev_node.left, prev_node.right)

        if low == high: # This is a leaf node, update its aggregates
            new_node.count += 1
            new_node.sum_val += val_to_add
            return new_node

        mid = (low + high) // 2
        if index <= mid:
            # The update path is in the left child. Create a new left child node.
            # If the previous left child was None, create an empty node to update.
            new_node.left = self._update(prev_node.left if prev_node.left else self._build_empty_node(low, mid), 
                                         low, mid, index, val_to_add)
        else:
            # The update path is in the right child. Create a new right child node.
            # If the previous right child was None, create an empty node to update.
            new_node.right = self._update(prev_node.right if prev_node.right else self._build_empty_node(mid + 1, high), 
                                          mid + 1, high, index, val_to_add)
        
        # Recalculate the current node's total count and sum based on its (potentially new) children
        new_node.count = (new_node.left.count if new_node.left else 0) + \
                         (new_node.right.count if new_node.right else 0)
        new_node.sum_val = (new_node.left.sum_val if new_node.left else 0) + \
                           (new_node.right.sum_val if new_node.right else 0)
        return new_node

    def add_element(self, k_idx: int, val: int):
        """
        Adds an element (val) corresponding to the k_idx-th position in the original array.
        This effectively creates a new version of the segment tree roots[k_idx + 1].

        Args:
            k_idx: The index in the original array (0-based).
            val: The mapped P[k_idx] value to be added to the tree.
        """
        new_root = self._update(self.roots[-1], 0, self.max_coord_value, val, val)
        self.roots.append(new_root)

    def _query_data(self, node: Optional[Node], low: int, high: int, query_low_val: int, query_high_val: int) -> tuple[int, int]:
        """
        Recursively queries a single segment tree version for aggregate data (count, sum_val)
        for values falling within a specified range [query_low_val, query_high_val].

        Args:
            node: The current node in the segment tree being processed.
            low, high: The value range covered by the current node.
            query_low_val, query_high_val: The target value range for the query.

        Returns:
            A tuple (count, sum_val) representing the aggregates for the queried range.
        """
        if not node or query_low_val > high or query_high_val < low:
            return 0, 0 # No overlap, or node is empty/non-existent
        
        if query_low_val <= low and high <= query_high_val:
            return node.count, node.sum_val # Current node's range is fully within the query range
        
        mid = (low + high) // 2
        # Recursively query left and right children
        left_count, left_sum = self._query_data(node.left, low, mid, query_low_val, query_high_val)
        right_count, right_sum = self._query_data(node.right, mid + 1, high, query_low_val, query_high_val)
        
        return left_count + right_count, left_sum + right_sum

    def query_range(self, k_start_idx: int, k_end_idx: int, val_low_mapped: int, val_high_mapped: int) -> tuple[int, int]:
        """
        Queries for aggregates (count, sum_val) of mapped_P values for elements
        in the original array from k_start_idx to k_end_idx (inclusive),
        where their mapped_P values are within [val_low_mapped, val_high_mapped].

        Args:
            k_start_idx: The starting index (inclusive) in the original array.
            k_end_idx: The ending index (inclusive) in the original array.
            val_low_mapped, val_high_mapped: The value range for mapped_P[k] to query.

        Returns:
            A tuple (count, sum_val) representing the aggregates.
        """
        if val_low_mapped > val_high_mapped: # Empty value range for P
            return 0, 0

        # The difference between two versions of the persistent segment tree
        # provides information about the elements added between those versions.
        # roots[k_end_idx + 1] contains data for mapped_P[0...k_end_idx].
        # roots[k_start_idx] contains data for mapped_P[0...k_start_idx-1].
        # Their difference gives data for mapped_P[k_start_idx...k_end_idx].
        current_root = self.roots[k_end_idx + 1] 
        prev_root = self.roots[k_start_idx]

        count_curr, sum_curr = self._query_data(current_root, 0, self.max_coord_value, val_low_mapped, val_high_mapped)
        count_prev, sum_prev = self._query_data(prev_root, 0, self.max_coord_value, val_low_mapped, val_high_mapped)

        return count_curr - count_prev, sum_curr - sum_prev


class Solution:
    def countStableSubarrays(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        N = len(nums)

        # Step 1: Precompute P[k] for all k
        # P[k] is defined as the largest index j < k such that nums[j] > nums[j+1].
        # If no such j exists, P[k] = -1.
        P = [-1] * N
        last_bad_idx = -1  # Stores the index of the last 'break point' (nums[j] > nums[j+1])
        for k in range(N):
            P[k] = last_bad_idx
            # Check if current index k is a break point for the sequence ending at k+1
            if k < N - 1 and nums[k] > nums[k+1]:
                last_bad_idx = k
        
        # Map P[k] values to be non-negative for use as indices in the segment tree.
        # P[k] ranges from -1 to N-2. Mapping P[k]+1 transforms this to [0, N-1].
        mapped_P = [p + 1 for p in P]
        
        # The maximum possible value for mapped_P[k] is N-1.
        # The segment tree will be built over the value range [0, N-1].
        max_mapped_P_value = N - 1 
        
        # Step 2: Build the Persistent Segment Tree
        pst = PersistentSegmentTree(max_mapped_P_value)
        for k_idx in range(N):
            pst.add_element(k_idx, mapped_P[k_idx])
        
        # Step 3: Process each query
        ans = [0] * len(queries)
        for i, (li, ri) in enumerate(queries):
            # The total number of stable subarrays in nums[li...ri] is given by:
            # Sum_{k=li}^{ri} (k - max(li-1, P[k]))
            
            # Calculate Sum_{k=li}^{ri} k (first term)
            # This is an arithmetic series sum from li to ri.
            # Using prefix sum formula: Sum(0 to ri) - Sum(0 to li-1)
            sum_k_li_ri = (ri * (ri + 1) // 2) - ((li - 1) * li // 2)

            # The threshold for P[k] is li-1.
            # When working with mapped_P (P[k]+1), this threshold becomes (li-1)+1 = li.
            threshold_for_P_mapped = li 

            # Calculate Sum_{k=li}^{ri} max(li-1, P[k]) (second term)
            # This second term is split into two parts:
            # 1. (li-1) * (count of k in [li, ri] where P[k] < li-1)
            #    P[k] < li-1 corresponds to mapped_P[k] < li.
            #    So, we query for mapped_P values in range [0, li-1].
            count_P_less, sum_P_less_mapped = pst.query_range(li, ri, 0, threshold_for_P_mapped - 1)
            
            # 2. (sum of P[k] for k in [li, ri] where P[k] >= li-1)
            #    P[k] >= li-1 corresponds to mapped_P[k] >= li.
            #    So, we query for mapped_P values in range [li, max_mapped_P_value].
            count_P_ge, sum_P_ge_mapped = pst.query_range(li, ri, threshold_for_P_mapped, max_mapped_P_value)

            # Convert mapped_P sums back to actual P sums:
            # sum_P_less_mapped is Sum(P[k]+1). To get Sum(P[k]), subtract 1 for each count.
            sum_P_actual_less = sum_P_less_mapped - count_P_less

            # Similarly for the P[k] >= li-1 part.
            sum_P_actual_ge = sum_P_ge_mapped - count_P_ge

            # Combine the two parts to get the full second term:
            # Sum_{k=li}^{ri} max(li-1, P[k]) = (li - 1) * count_P_less + sum_P_actual_ge
            term_to_subtract = (li - 1) * count_P_less + sum_P_actual_ge
            
            # Final answer for the current query
            ans[i] = sum_k_li_ri - term_to_subtract
            
        return ans

