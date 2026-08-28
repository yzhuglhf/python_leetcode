import collections
from typing import List
# This line is crucial for the performance. On LeetCode, `sortedcontainers`
# is usually available for Python. If not, a custom balanced BST or
# a segment tree built over frequency and value would be needed,
# significantly increasing implementation complexity.
from sortedcontainers import SortedList


class SegmentTree:
    """
    Segment Tree to store (max_freq, min_val_at_max_freq) for frequency ranges.
    Each node in the segment tree represents a range of frequencies `[start, end]`.
    It stores a tuple `(max_freq, min_compressed_val)`:
    - `max_freq`: The highest frequency value encountered within its frequency range.
    - `min_compressed_val`: The smallest compressed value that achieves `max_freq`.
      If multiple values tie for `max_freq`, the smallest value is chosen.
    
    Query: find (max_freq, min_val) in a specified frequency range `[query_start_freq, query_end_freq]`.
    Update: `update(freq_idx, min_val_at_freq)` sets the information for a specific `freq_idx`.
    """
    def __init__(self, N_max_freq):
        # N_max_freq is the maximum possible frequency any element can have (i.e., n)
        self.N_max_freq = N_max_freq
        # Initialize tree nodes with (0, float('inf')) meaning no elements in this freq range.
        # A frequency of 0 means it does not contribute to max_freq; float('inf') for min_val ensures it loses ties.
        self.tree = [(0, float('inf'))] * (4 * N_max_freq + 4) # (max_freq, min_compressed_val)
    
    def _combine(self, left_res, right_res):
        """Combines results from two child nodes to get the result for their parent."""
        if left_res[0] > right_res[0]:
            return left_res
        elif right_res[0] > left_res[0]:
            return right_res
        else: # Frequencies are equal, break tie by choosing the smaller value
            return (left_res[0], min(left_res[1], right_res[1]))

    def update(self, freq_idx, min_val_at_freq):
        """
        Update the information for a specific frequency index.
        freq_idx: 1-based index (frequency value itself). Must be > 0.
        min_val_at_freq: The smallest compressed value that currently has `freq_idx` frequency.
                         If no value has this `freq_idx`, it should be `float('inf')`.
        """
        # A frequency of 0 is not tracked by the segment tree (its range starts from 1)
        if freq_idx == 0:
            return

        # The leaf node for `freq_idx` will store (freq_idx, min_val_at_freq).
        # If `min_val_at_freq` is `inf`, it means no element currently has this frequency.
        # In this case, we store (0, inf) to effectively "unset" this frequency, as 0 is lower than any valid frequency.
        val_tuple_for_leaf = (freq_idx, min_val_at_freq) if min_val_at_freq != float('inf') else (0, float('inf'))
        self._update_recursive(1, 1, self.N_max_freq, freq_idx, val_tuple_for_leaf)

    def _update_recursive(self, node, start, end, idx, val_tuple):
        """Recursive helper for point update."""
        if start == end: # Base case: leaf node
            self.tree[node] = val_tuple
            return

        mid = (start + end) // 2
        if start <= idx <= mid: # Go left
            self._update_recursive(2 * node, start, mid, idx, val_tuple)
        else: # Go right
            self._update_recursive(2 * node + 1, mid + 1, end, idx, val_tuple)
        
        # After updating children, re-combine their results for the parent node
        self.tree[node] = self._combine(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, query_start_freq, query_end_freq):
        """
        Query for the (max_freq, min_val) within the frequency range 
        `[query_start_freq, query_end_freq]`.
        """
        # Handle invalid or out-of-bounds query ranges
        if query_start_freq > query_end_freq or query_start_freq > self.N_max_freq: 
            return (0, float('inf'))
        # Ensure query_end_freq does not exceed the maximum trackable frequency
        query_end_freq = min(query_end_freq, self.N_max_freq)

        return self._query_recursive(1, 1, self.N_max_freq, query_start_freq, query_end_freq)

    def _query_recursive(self, node, start, end, query_start, query_end):
        """Recursive helper for range query."""
        # Case 1: Current node's range has no overlap with the query range
        if query_end < start or end < query_start: 
            return (0, float('inf'))
        # Case 2: Current node's range is fully contained within the query range
        if query_start <= start and end <= query_end: 
            return self.tree[node]

        # Case 3: Partial overlap, recurse on children
        mid = (start + end) // 2
        p1 = self._query_recursive(2 * node, start, mid, query_start, query_end)
        p2 = self._query_recursive(2 * node + 1, mid + 1, end, query_start, query_end)
        return self._combine(p1, p2)


class Solution:
    def subarrayMajority(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)

        # 1. Coordinate Compression
        # Map original values to a contiguous range [0, D-1] for efficient array indexing.
        unique_vals = sorted(list(set(nums)))
        val_to_compressed = {val: i for i, val in enumerate(unique_vals)}
        compressed_to_val = {i: val for i, val in enumerate(unique_vals)}
        compressed_nums = [val_to_compressed[x] for x in nums]
        
        num_distinct_vals = len(unique_vals)
        max_possible_freq = n # The maximum frequency any single element can have is `n`

        # 2. Mo's Algorithm Setup
        # Determine block size for sorting queries. A common heuristic is sqrt(N).
        block_size = int(n**0.5)
        if block_size == 0: # Handle cases like n=0, though constraints say n >= 1
            block_size = 1

        # Store queries with their original index to correctly place results in the answer array.
        queries_with_idx = []
        for i, (l, r, threshold) in enumerate(queries):
            queries_with_idx.append((l, r, threshold, i))
        
        # Sort queries using Mo's sorting scheme:
        # 1. By block index of the left pointer (l // block_size).
        # 2. For queries within the same block, alternate sorting direction for the right pointer `r`.
        #    This is `r` ascending for even blocks and `r` descending for odd blocks.
        queries_with_idx.sort(key=lambda q_tuple: (q_tuple[0] // block_size, 
                                                 q_tuple[1] if (q_tuple[0] // block_size) % 2 == 0 else -q_tuple[1]))

        # 3. Data Structures for Mo's Algorithm operations
        # `val_to_freq`: Array mapping a compressed value to its current frequency in the sliding window.
        val_to_freq = [0] * num_distinct_vals 
        
        # `freq_to_vals`: List of SortedList objects. `freq_to_vals[f]` stores all compressed values
        # that currently have a frequency `f` in the window, kept sorted to easily find the minimum.
        freq_to_vals = [SortedList() for _ in range(max_possible_freq + 1)] 
        
        # `segment_tree`: Used to efficiently query for the highest frequency (and its smallest value)
        # within a given range of frequencies (e.g., from `threshold` to `max_possible_freq`).
        segment_tree = SegmentTree(max_possible_freq)

        # Initialize the sliding window pointers. `curr_r` is -1 to represent an empty initial window.
        curr_l, curr_r = 0, -1 
        ans = [-1] * len(queries)

        def add(idx):
            """Adds the element at `compressed_nums[idx]` to the current window."""
            val = compressed_nums[idx]
            old_freq = val_to_freq[val]
            
            # If the element had a previous frequency, remove it from that `freq_to_vals` list
            # and update the segment tree for the old frequency.
            if old_freq > 0:
                freq_to_vals[old_freq].discard(val)
                min_val_for_old_freq = freq_to_vals[old_freq][0] if freq_to_vals[old_freq] else float('inf')
                segment_tree.update(old_freq, min_val_for_old_freq)

            # Increment frequency and add to the new `freq_to_vals` list.
            val_to_freq[val] += 1
            new_freq = val_to_freq[val]
            freq_to_vals[new_freq].add(val)
            # Update the segment tree for the new frequency.
            segment_tree.update(new_freq, freq_to_vals[new_freq][0])

        def remove(idx):
            """Removes the element at `compressed_nums[idx]` from the current window."""
            val = compressed_nums[idx]
            old_freq = val_to_freq[val]
            
            # Remove from its current `freq_to_vals` list and update the segment tree.
            freq_to_vals[old_freq].discard(val)
            min_val_for_old_freq = freq_to_vals[old_freq][0] if freq_to_vals[old_freq] else float('inf')
            segment_tree.update(old_freq, min_val_for_old_freq)

            # Decrement frequency.
            val_to_freq[val] -= 1
            new_freq = val_to_freq[val]
            
            # If the element still has a positive frequency, add it to the corresponding `freq_to_vals` list
            # and update the segment tree for the new frequency.
            if new_freq > 0:
                freq_to_vals[new_freq].add(val)
                segment_tree.update(new_freq, freq_to_vals[new_freq][0])
            # If `new_freq` is 0, the element is completely removed from the window's counts.
            # Its previous frequency `old_freq` was already updated in the segment tree to reflect the removal.

        # 4. Process Queries using Mo's algorithm
        for l, r, threshold, original_idx in queries_with_idx:
            # Move `curr_l` and `curr_r` pointers to match the query range `[l, r]`.
            while curr_l > l:
                curr_l -= 1
                add(curr_l)
            while curr_r < r:
                curr_r += 1
                add(curr_r)
            while curr_l < l:
                remove(curr_l)
                curr_l += 1
            while curr_r > r:
                remove(curr_r)
                curr_r -= 1
            
            # After the window is adjusted, query the segment tree.
            # We look for frequencies from `threshold` up to `max_possible_freq`.
            max_f_in_range, best_compressed_val = segment_tree.query(threshold, max_possible_freq)

            # If a valid element (meeting the threshold) is found, record its original value.
            if max_f_in_range >= threshold:
                ans[original_idx] = compressed_to_val[best_compressed_val]
            else:
                ans[original_idx] = -1 # No such element exists
        
        return ans


if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, 1, 2, 2, 1, 1]
    queries1 = [[0, 5, 4], [0, 3, 3], [2, 3, 2]]
    expected1 = [1, -1, 2]
    assert s.subarrayMajority(nums1, queries1) == expected1, f"Example 1 failed: {s.subarrayMajority(nums1, queries1)}"

    # Example 2
    nums2 = [3, 2, 3, 2, 3, 2, 3]
    queries2 = [[0, 6, 4], [1, 5, 2], [2, 4, 1], [3, 3, 1]]
    expected2 = [3, 2, 3, 2]
    assert s.subarrayMajority(nums2, queries2) == expected2, f"Example 2 failed: {s.subarrayMajority(nums2, queries2)}"

    # Additional Test Case 1: Single element subarray
    nums3 = [10, 20, 30]
    queries3 = [[0, 0, 1], [1, 1, 1], [2, 2, 1]]
    expected3 = [10, 20, 30]
    assert s.subarrayMajority(nums3, queries3) == expected3, f"Additional Test 1 failed: {s.subarrayMajority(nums3, queries3)}"

    # Additional Test Case 2: No element meets threshold
    nums4 = [1, 2, 3, 4, 5]
    queries4 = [[0, 4, 2]]
    expected4 = [-1]
    assert s.subarrayMajority(nums4, queries4) == expected4, f"Additional Test 2 failed: {s.subarrayMajority(nums4, queries4)}"

    # Additional Test Case 3: Tie in frequency, choose smallest value
    nums5 = [10, 20, 10, 30, 20]
    queries5 = [[0, 4, 2]] # Subarray [10, 20, 10, 30, 20], threshold 2
                           # Frequencies: 10 -> 2, 20 -> 2, 30 -> 1
                           # Both 10 and 20 meet threshold 2 with frequency 2. Choose 10 (smaller value).
    expected5 = [10]
    assert s.subarrayMajority(nums5, queries5) == expected5, f"Additional Test 3 failed: {s.subarrayMajority(nums5, queries5)}"

    # Additional Test Case 4: Larger array, varied thresholds
    nums6 = [5,5,1,2,5,1,1,2,5,5]
    queries6 = [[0,9,3],[0,9,4],[0,9,5],[0,4,3]]
    # Query 1: [0,9,3] -> [5,5,1,2,5,1,1,2,5,5], len=10. Freq: 5->5, 1->3, 2->2. Ans: 5 (freq 5)
    # Query 2: [0,9,4] -> Same array. Freq: 5->5, 1->3, 2->2. Ans: 5 (freq 5)
    # Query 3: [0,9,5] -> Same array. Freq: 5->5, 1->3, 2->2. Ans: 5 (freq 5)
    # Query 4: [0,4,3] -> [5,5,1,2,5], len=5. Freq: 5->3, 1->1, 2->1. Ans: 5 (freq 3)
    expected6 = [5,5,5,5]
    assert s.subarrayMajority(nums6, queries6) == expected6, f"Additional Test 4 failed: {s.subarrayMajority(nums6, queries6)}"

    print("All tests passed!")

