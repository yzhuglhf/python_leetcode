"""
Concatenate Non-Zero Digits and Multiply by Sum II
Difficulty: Medium

Description:
This problem asks us to process range queries on a string of digits. For each query [li, ri], we must extract the substring s[li..ri], form a new integer 'x' by concatenating its non-zero digits, calculate 'sum' as the sum of digits in 'x', and return (x * sum) modulo (10^9 + 7).

Example:
Input: s = "10203004", queries = [[0,7],[1,3],[4,6]]
Output: [12340, 4, 9]
Explanation:
- For s[0..7] = "10203004", x = 1234, sum = 10, answer = 1234 * 10 = 12340.
- For s[1..3] = "020", x = 2, sum = 2, answer = 2 * 2 = 4.
- For s[4..6] = "300", x = 3, sum = 3, answer = 3 * 3 = 9.

Approach:
A naive approach of iterating through each substring for every query would be too slow (O(M*Q)). Instead, we use a Segment Tree to efficiently handle range queries. Each node in the segment tree represents a range [start, end] of the original string 's' and stores three pieces of information: `val_x` (the integer formed by concatenating non-zero digits in its range, modulo 10^9 + 7), `val_sum` (the sum of these non-zero digits, modulo 10^9 + 7), and `count_non_zero` (the total number of non-zero digits in its range).

The segment tree is built bottom-up. Leaf nodes correspond to individual digits in 's': if s[i] is '0', the node stores (0, 0, 0); otherwise, it stores (digit, digit, 1). Parent nodes merge information from their two children. When merging a `left_node` and `right_node`, the new `val_x` is calculated as `(left_node.val_x * 10^(right_node.count_non_zero) + right_node.val_x) % MOD`. The `val_sum` is `(left_node.val_sum + right_node.val_sum) % MOD`, and `count_non_zero` is the sum of child counts. To make the merge operation O(1), powers of 10 (10^k % MOD) up to string length 'm' are precomputed. Queries for a range [li, ri] traverse the tree, combining results from all relevant nodes. A `Node(0, 0, 0)` acts as the identity element for merging (representing an empty sequence of non-zero digits). Finally, for each query, `(x * sum) % MOD` is computed.

Time Complexity: O(m + Q log m)
Space Complexity: O(m)
"""
from typing import List, Optional # Optional is not strictly needed but included in template

MOD = 10**9 + 7

class Node:
    """
    Represents data stored in a segment tree node for a given range.
    val_x: The integer formed by concatenating non-zero digits, modulo MOD.
    val_sum: The sum of non-zero digits, modulo MOD.
    count_non_zero: The count of non-zero digits in the range.
    """
    def __init__(self, val_x: int = 0, val_sum: int = 0, count_non_zero: int = 0):
        self.val_x = val_x
        self.val_sum = val_sum
        self.count_non_zero = count_non_zero

class SegmentTree:
    """
    A segment tree to efficiently query concatenated non-zero digits and their sum.
    """
    def __init__(self, s: str, m: int):
        self.s = s
        self.m = m
        self.tree = [Node()] * (4 * m) # Initialize with identity nodes
        
        # Precompute powers of 10 modulo MOD
        self.powers_of_10 = [1] * (m + 1)
        for i in range(1, m + 1):
            self.powers_of_10[i] = (self.powers_of_10[i-1] * 10) % MOD
        
        # Build the segment tree
        self._build(1, 0, m - 1)

    def _merge_nodes(self, left_node: Node, right_node: Node) -> Node:
        """
        Merges information from two child nodes to form a parent node.
        If we have x_left for the left part and x_right for the right part,
        with N_right non-zero digits in the right part,
        the combined x is (x_left * 10^N_right + x_right) % MOD.
        The combined sum is (sum_left + sum_right) % MOD.
        The combined count is (count_left + count_right).
        Node(0, 0, 0) acts as an identity element for this merge operation.
        """
        res_x = (left_node.val_x * self.powers_of_10[right_node.count_non_zero] + right_node.val_x) % MOD
        res_sum = (left_node.val_sum + right_node.val_sum) % MOD
        res_count = left_node.count_non_zero + right_node.count_non_zero
        return Node(res_x, res_sum, res_count)

    def _build(self, idx: int, start: int, end: int):
        """
        Recursively builds the segment tree.
        idx: Current node's index in self.tree.
        start, end: Range covered by current node.
        """
        if start == end: # Leaf node
            digit = int(self.s[start])
            if digit == 0:
                self.tree[idx] = Node(0, 0, 0)
            else:
                self.tree[idx] = Node(digit, digit, 1)
            return

        mid = (start + end) // 2
        self._build(2 * idx, start, mid) # Build left child
        self._build(2 * idx + 1, mid + 1, end) # Build right child
        self.tree[idx] = self._merge_nodes(self.tree[2 * idx], self.tree[2 * idx + 1])

    def query(self, l: int, r: int) -> Node:
        """
        Queries the segment tree for a given range [l, r].
        Returns a Node containing the aggregated information for that range.
        """
        return self._query_recursive(1, 0, self.m - 1, l, r)

    def _query_recursive(self, idx: int, start: int, end: int, l: int, r: int) -> Node:
        """
        Recursive helper for query.
        idx: Current node's index.
        start, end: Range covered by current node.
        l, r: Query range.
        """
        # If the current node's range is completely outside the query range
        if r < start or end < l:
            return Node(0, 0, 0) # Return identity element

        # If the current node's range is completely inside the query range
        if l <= start and end <= r:
            return self.tree[idx]

        # If the current node's range partially overlaps the query range
        mid = (start + end) // 2
        left_res = self._query_recursive(2 * idx, start, mid, l, r)
        right_res = self._query_recursive(2 * idx + 1, mid + 1, end, l, r)
        
        return self._merge_nodes(left_res, right_res)

class Solution:
    def sumAndMultiply(self, s: str, queries: List[List[int]]) -> List[int]:
        m = len(s)
        segment_tree = SegmentTree(s, m)
        
        results = []
        for li, ri in queries:
            # Query the segment tree for the range [li, ri]
            node = segment_tree.query(li, ri)
            
            x = node.val_x
            s_sum = node.val_sum
            
            # Calculate the final answer for the query: (x * s_sum) % MOD
            ans = (x * s_sum) % MOD
            results.append(ans)
            
        return results

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    s1 = "10203004"
    queries1 = [[0,7],[1,3],[4,6]]
    expected1 = [12340, 4, 9]
    assert s_obj.sumAndMultiply(s1, queries1) == expected1, f"Test 1 Failed: {s_obj.sumAndMultiply(s1, queries1)}"

    # Example 2
    s2 = "1000"
    queries2 = [[0,3],[1,1]]
    expected2 = [1, 0]
    assert s_obj.sumAndMultiply(s2, queries2) == expected2, f"Test 2 Failed: {s_obj.sumAndMultiply(s2, queries2)}"

    # Example 3
    s3 = "9876543210"
    queries3 = [[0,9]]
    expected3 = [444444137]
    assert s_obj.sumAndMultiply(s3, queries3) == expected3, f"Test 3 Failed: {s_obj.sumAndMultiply(s3, queries3)}"

    # Additional Test Cases
    # All zeros
    s4 = "00000"
    queries4 = [[0,4], [1,1], [2,3]]
    expected4 = [0, 0, 0]
    assert s_obj.sumAndMultiply(s4, queries4) == expected4, f"Test 4 Failed: {s_obj.sumAndMultiply(s4, queries4)}"

    # Single digit non-zero
    s5 = "5"
    queries5 = [[0,0]]
    expected5 = [25]
    assert s_obj.sumAndMultiply(s5, queries5) == expected5, f"Test 5 Failed: {s_obj.sumAndMultiply(s5, queries5)}"

    # Mix of zeros and non-zeros
    s6 = "100502"
    queries6 = [[0,5], [1,4], [0,0], [3,5]]
    # s[0..5]="100502" -> x=152, sum=1+5+2=8 -> 152*8 = 1216
    # s[1..4]="0050" -> x=5, sum=5 -> 5*5 = 25
    # s[0..0]="1" -> x=1, sum=1 -> 1*1 = 1
    # s[3..5]="502" -> x=52, sum=5+2=7 -> 52*7 = 364
    expected6 = [1216, 25, 1, 364]
    assert s_obj.sumAndMultiply(s6, queries6) == expected6, f"Test 6 Failed: {s_obj.sumAndMultiply(s6, queries6)}"

    print("All tests passed!")
