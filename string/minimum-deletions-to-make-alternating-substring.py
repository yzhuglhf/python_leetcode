"""
Minimum Deletions to Make Alternating Substring
Difficulty: Hard

Description:
This problem requires maintaining a string of 'A's and 'B's and processing two types of queries: flipping a character at a specific index, and computing the minimum deletions to make a substring alternating. The minimum deletions for a substring to be alternating is equivalent to the count of adjacent identical characters within that substring.

Example:
Input: s = "ABA", queries = [[2,1,2],[1,1],[2,0,2]]
Output: [0,2]
Explanation: Initially s="ABA".
Query [2,1,2]: Substring "BA". No adjacent identical chars. 0 deletions.
Query [1,1]: Flip s[1] ('B' to 'A'). s becomes "AAA".
Query [2,0,2]: Substring "AAA". s[0]==s[1] and s[1]==s[2]. 2 deletions (e.g., delete s[1] and s[2] to get "A").

Approach:
The key insight is that the minimum deletions to make a substring `s[l..r]` alternating is simply the count of indices `i` such that `l <= i < r` and `s[i] == s[i+1]`. This is because each adjacent identical pair `s[i] == s[i+1]` requires at least one deletion to break. If we consider forming the longest possible alternating subsequence, we can do this greedily: keep the first character, then for each subsequent position, keep the character if it differs from the last character kept. The length of such a subsequence is `1 + count(s[i] != s[i+1])` for `i` from `l` to `r-1`. The number of deletions is `(length of substring) - (length of longest alternating subsequence)`, which is `(r-l+1) - (1 + count(s[i] != s[i+1]))`. This simplifies to `(r-l) - count(s[i] != s[i+1])`, which is precisely `count(s[i] == s[i+1])` for `i` from `l` to `r-1`.

To efficiently handle both point updates (flips) and range sum queries (counting adjacent identical characters), a Segment Tree is used. We convert the input string `s` into a mutable list `s_list`. A `diff_values` array of length `n-1` is created, where `diff_values[i]` is 1 if `s_list[i] == s_list[i+1]` and 0 otherwise. This `diff_values` array is then used to build a Segment Tree.
A flip operation `[1, j]` changes `s_list[j]`. This affects the adjacency status of `s_list[j-1]` with `s_list[j]` (if `j > 0`) and `s_list[j]` with `s_list[j+1]` (if `j < n-1`). For each affected pair, we re-evaluate if `s_list[k] == s_list[k+1]` and update the corresponding `diff_values[k]` in the Segment Tree (a point update).
A query `[2, l, r]` asks for the minimum deletions in `s[l..r]`. This translates directly to a range sum query on `diff_values` from index `l` to `r-1` in the Segment Tree.
A special case is `n=1`: any substring will have length 1, which is always alternating and requires 0 deletions. This case is handled separately to avoid segment tree operations on an empty `diff_values` array.

Time Complexity: O(N + Q logN)
N is the length of the string `s`, Q is the number of queries.
- Initial construction of `s_list`, `diff_values`, and Segment Tree: O(N).
- Each query of type 1 (flip): O(logN) for at most two point updates in the Segment Tree.
- Each query of type 2 (compute deletions): O(logN) for a range sum query in the Segment Tree.
Total time complexity is O(N + Q logN).

Space Complexity: O(N)
- `s_list`: O(N)
- `diff_values`: O(N)
- Segment Tree: O(N) (specifically, O(4N) in worst case for a binary tree implemented with an array)
Total space complexity is O(N).
"""
from typing import List, Optional

class SegmentTree:
    def __init__(self, arr_len):
        self.n = arr_len
        if self.n == 0: # Handle case where diff_values is empty (original string length 1)
            self.tree = []
            return
        
        # Segment tree size is typically 4*N for N leaves to be safe
        self.tree = [0] * (4 * self.n)
        
    def _build(self, node, start, end, diff_values):
        if start == end:
            self.tree[node] = diff_values[start]
            return
        
        mid = (start + end) // 2
        self._build(2 * node, start, mid, diff_values)
        self._build(2 * node + 1, mid + 1, end, diff_values)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def build(self, diff_values):
        if self.n == 0:
            return # Nothing to build for an empty diff_values array
        self._build(1, 0, self.n - 1, diff_values)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        
        mid = (start + end) // 2
        if start <= idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx, val):
        if self.n == 0:
            return # Cannot update if there are no diffs
        if not (0 <= idx < self.n):
            return # Index out of bounds for diff_values
        self._update(1, 0, self.n - 1, idx, val)

    def _query(self, node, start, end, l, r):
        # Current node's range is completely outside query range
        if r < start or end < l: 
            return 0
        # Current node's range is completely inside query range
        if l <= start and end <= r: 
            return self.tree[node]
        
        mid = (start + end) // 2
        p1 = self._query(2 * node, start, mid, l, r)
        p2 = self._query(2 * node + 1, mid + 1, end, l, r)
        return p1 + p2

    def query(self, l, r):
        if self.n == 0:
            return 0 # If original string length 1, no diffs, always 0 deletions
        # If the query range for diff_values is empty (e.g., for s[k..k], where r-1 < l)
        if r < l: 
            return 0
        
        # Ensure query range [l, r] is within valid diff_values indices [0, self.n-1]
        # This clamping handles cases where l or r are out of bounds for diff_values,
        # though for this specific problem, l and r are always derived such that they
        # correspond to valid string indices.
        l = max(0, l)
        r = min(self.n - 1, r)
        if r < l: # After clamping, if range becomes empty
            return 0
            
        return self._query(1, 0, self.n - 1, l, r)

class Solution:
    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        s_list = list(s) # Convert string to mutable list of characters
        
        # Handle n=1 edge case: a single-character string is always alternating.
        if n == 1:
            ans = []
            for query in queries:
                q_type = query[0]
                if q_type == 2:
                    ans.append(0) # 0 deletions for a length-1 substring
                # Type 1 query [1,0] for n=1: flip s[0]. This changes the string but does not affect any 'adjacent identical' count, as there are no adjacent characters.
            return ans

        # Initialize diff_values array: diff_values[i] = 1 if s_list[i] == s_list[i+1], else 0
        # This array has length n-1, for indices 0 to n-2.
        diff_values = [0] * (n - 1)
        for i in range(n - 1):
            if s_list[i] == s_list[i+1]:
                diff_values[i] = 1
        
        # Build segment tree on diff_values
        seg_tree = SegmentTree(n - 1)
        seg_tree.build(diff_values)
        
        ans = []
        
        for query in queries:
            q_type = query[0]
            
            if q_type == 1: # Flip s[j]
                j = query[1]
                
                # Flip the character in s_list
                s_list[j] = 'A' if s_list[j] == 'B' else 'B'
                
                # A flip at index j can affect diff_values[j-1] and diff_values[j]
                
                # Check and update diff_values[j-1] if j > 0
                if j > 0:
                    # Calculate the new value for diff_values[j-1]
                    new_diff_val = 1 if s_list[j-1] == s_list[j] else 0
                    seg_tree.update(j-1, new_diff_val)
                
                # Check and update diff_values[j] if j < n-1
                if j < n - 1:
                    # Calculate the new value for diff_values[j]
                    new_diff_val = 1 if s_list[j] == s_list[j+1] else 0
                    seg_tree.update(j, new_diff_val)
                        
            else: # Query type 2: compute deletions for s[l..r]
                l, r = query[1], query[2]
                
                # We need the sum of diff_values from index l to r-1.
                # The SegmentTree.query method handles cases like r-1 < l (e.g., l=r for a length-1 substring) by returning 0, which is correct.
                res = seg_tree.query(l, r - 1)
                ans.append(res)
                
        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    input_s1 = "ABA"
    queries1 = [[2,1,2],[1,1],[2,0,2]]
    expected1 = [0,2]
    assert s.minDeletions(input_s1, queries1) == expected1, f"Test Case 1 Failed: {s.minDeletions(input_s1, queries1)}"

    # Example 2
    input_s2 = "ABB"
    queries2 = [[2,0,2],[1,2],[2,0,2]]
    expected2 = [1,0]
    assert s.minDeletions(input_s2, queries2) == expected2, f"Test Case 2 Failed: {s.minDeletions(input_s2, queries2)}"

    # Example 3
    input_s3 = "BABA"
    queries3 = [[2,0,3],[1,1],[2,1,3]]
    expected3 = [0,1]
    assert s.minDeletions(input_s3, queries3) == expected3, f"Test Case 3 Failed: {s.minDeletions(input_s3, queries3)}"

    # Custom Test: n=1 edge case
    input_s4 = "A"
    queries4 = [[2,0,0],[1,0],[2,0,0]]
    expected4 = [0,0]
    assert s.minDeletions(input_s4, queries4) == expected4, f"Test Case 4 Failed: {s.minDeletions(input_s4, queries4)}"

    # Custom Test: Longer string, multiple flips
    input_s5 = "AAABBB"
    queries5 = [[2,0,5],[1,2],[2,0,5],[1,3],[2,0,5]]
    expected5 = [4,3,2] # "AAABBB" -> 4 deletions (AA,AA,BB,BB)
                        # Flip s[2] from B to A: "AAABAB" -> 3 deletions (AA,AA,AB)
                        # Flip s[3] from B to A: "AAABAA" -> 2 deletions (AA,AA,AA)
    assert s.minDeletions(input_s5, queries5) == expected5, f"Test Case 5 Failed: {s.minDeletions(input_s5, queries5)}"

    # Custom Test: Substring query with no deletions
    input_s6 = "ABABAB"
    queries6 = [[2,0,5],[2,1,4]]
    expected6 = [0,0]
    assert s.minDeletions(input_s6, queries6) == expected6, f"Test Case 6 Failed: {s.minDeletions(input_s6, queries6)}"

    print("All tests passed!")