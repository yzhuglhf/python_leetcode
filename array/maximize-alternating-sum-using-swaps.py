"""
Maximize Alternating Sum Using Swaps
Difficulty: Hard

Description:
This problem asks us to maximize the alternating sum of an array `nums` (defined as `nums[0] - nums[1] + nums[2] - ...`), given a set of allowed swaps between elements at specified indices. The crucial aspect is that these swaps can be performed any number of times and in any order, implying that all indices reachable from each other through a sequence of swaps form a connected component where values can be freely rearranged.

Example:
Input: nums = [1,2,3], swaps = [[0,2],[1,2]]
Output: 4
Explanation: Indices 0, 1, and 2 are all connected into a single component. The original values are [1, 2, 3]. In this component, there are two even indices (0, 2) and one odd index (1). To maximize the sum, we assign the two largest values (3 and 2) to the even indices, and the smallest value (1) to the odd index. Possible final arrays include [3, 1, 2] or [2, 1, 3]. The alternating sum for [2, 1, 3] is 2 - 1 + 3 = 4.

Approach:
The problem can be decomposed into two main parts: identifying the groups of indices that can exchange values, and then optimally assigning values within each group.
1.  **Identify Connected Components**: The ability to perform swaps any number of times means that if indices `p` and `q` can be swapped, they are in the same "connected component." If `q` and `r` can also be swapped, then `p`, `q`, and `r` are all in the same component. A Disjoint Set Union (DSU) data structure is ideal for finding these connected components. We initialize a DSU structure for `n` indices. For each `[pi, qi]` in `swaps`, we perform a `union(pi, qi)` operation to merge the components containing `pi` and `qi`.
2.  **Aggregate Component Information**: After processing all swaps, we iterate through the original `nums` array. For each index `i`, we use the DSU's `find(i)` operation to determine which connected component it belongs to. For each component, we collect:
    *   All original `nums[j]` values that belong to any index `j` within that component.
    *   The total count of even indices (e.g., 0, 2, 4, ...) within the component.
    *   The total count of odd indices (e.g., 1, 3, 5, ...) within the component.
    A dictionary mapping component roots (representatives from DSU) to these statistics is suitable for this.
3.  **Calculate Maximum Alternating Sum**: The alternating sum `nums[0] - nums[1] + nums[2] - ...` can be rewritten as `(sum of values at even indices) - (sum of values at odd indices)`. To maximize this sum for a given connected component, we must assign the `even_count` largest values from its collected values to its even indices (these values contribute positively to the sum), and the `odd_count` smallest values to its odd indices (these values contribute negatively to the sum).
    For each component:
    a.  Sort the collected `nums` values in ascending order.
    b.  Add the `even_count` largest values (which will be at the end of the sorted list) to the `total_alternating_sum`.
    c.  Subtract the `odd_count` smallest values (which will be at the beginning of the sorted list) from the `total_alternating_sum`.
    This strategy ensures optimal assignment within each component because all values within a component are interchangeable, and we always want to pair positive coefficients (even indices) with large values and negative coefficients (odd indices) with small values.

Time Complexity: O(N log N + M * α(N)), where N is `nums.length` and M is `swaps.length`. The DSU operations (`find` and `union`) with path compression and union by rank take nearly constant time, O(α(N)) (inverse Ackermann function). Initializing DSU and aggregating component info takes O(N * α(N)). The dominant factor is sorting values within components, which takes O(N log N) in the worst case (e.g., all elements are in a single component).
Space Complexity: O(N), for the DSU parent/rank arrays and for storing the aggregated component information (values and counts for each component).
"""
from typing import List
import collections

# Helper class for Disjoint Set Union (DSU) operations
class DSU:
    def __init__(self, n):
        # parent[i] stores the parent of element i. If parent[i] == i, i is a root.
        self.parent = list(range(n))
        # rank[i] stores the rank (height) of the tree rooted at i, used for union by rank optimization.
        self.rank = [0] * n

    # Finds the root of the set containing element i with path compression.
    def find(self, i):
        if self.parent[i] == i:
            return i
        # Path compression: make every node on the path point directly to the root.
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    # Unites the sets containing elements i and j using union by rank.
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank: attach the smaller rank tree under the root of the larger rank tree.
            # This helps keep the trees shallow.
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_j] < self.rank[root_i]:
                self.parent[root_j] = root_i
            else:
                # If ranks are equal, attach one to the other and increment the rank of the new root.
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True # Successfully united two distinct sets
        return False # i and j were already in the same set

class Solution:
    def maxAlternatingSum(self, nums: List[int], swaps: List[List[int]]) -> int:
        n = len(nums)
        dsu = DSU(n)

        # 1. Find connected components using DSU
        # Each swap [p, q] means indices p and q are connected.
        # Since swaps can be performed any number of times, all indices reachable from each other
        # through a sequence of swaps form a connected component.
        for p, q in swaps:
            dsu.union(p, q)

        # 2. Aggregate information for each component
        # We need to store:
        # - All original values nums[i] that belong to this component.
        # - The count of even-indexed positions (0, 2, 4...) within this component.
        # - The count of odd-indexed positions (1, 3, 5...) within this component.
        # The key for the dictionary is the root (representative) of the component.
        # defaultdict allows us to easily add to lists and increment counts for new roots.
        components = collections.defaultdict(lambda: {'values': [], 'even_count': 0, 'odd_count': 0})

        for i in range(n):
            root = dsu.find(i) # Find the representative of the component for index i
            components[root]['values'].append(nums[i]) # Add the value at index i to its component's values list
            if i % 2 == 0:
                components[root]['even_count'] += 1 # Increment count if index i is even
            else:
                components[root]['odd_count'] += 1 # Increment count if index i is odd
        
        # 3. Calculate maximum alternating sum
        total_alternating_sum = 0

        # Iterate through each identified connected component
        for root in components:
            component_info = components[root]
            # Sort the values within the component to easily pick smallest/largest
            component_values = sorted(component_info['values'])
            even_count = component_info['even_count']
            odd_count = component_info['odd_count']
            
            # To maximize (sum of values at even indices - sum of values at odd indices):
            # We must assign the largest available values to the `even_count` even positions (added positively).
            # We must assign the smallest available values to the `odd_count` odd positions (subtracted negatively).
            
            # The `component_values` list is sorted in ascending order.
            # The smallest `odd_count` values are at the beginning (indices 0 to odd_count - 1).
            # The largest `even_count` values are at the end (indices k - even_count to k - 1), where k is len(component_values).
            
            k = len(component_values)
            
            # Subtract the smallest `odd_count` values from the total sum
            for i in range(odd_count):
                total_alternating_sum -= component_values[i]
            
            # Add the largest `even_count` values to the total sum
            # The slice starts at index k - even_count and goes up to k-1.
            for i in range(k - even_count, k):
                total_alternating_sum += component_values[i]
                
        return total_alternating_sum

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1, 2, 3]
    swaps1 = [[0, 2], [1, 2]]
    expected1 = 4
    assert s.maxAlternatingSum(nums1, swaps1) == expected1, f"Test 1 failed. Input: {nums1}, {swaps1}, Expected: {expected1}, Got: {s.maxAlternatingSum(nums1, swaps1)}"

    # Example 2
    nums2 = [1, 2, 3]
    swaps2 = [[1, 2]]
    expected2 = 2
    assert s.maxAlternatingSum(nums2, swaps2) == expected2, f"Test 2 failed. Input: {nums2}, {swaps2}, Expected: {expected2}, Got: {s.maxAlternatingSum(nums2, swaps2)}"

    # Example 3
    nums3 = [1, 1000000000, 1, 1000000000, 1, 1000000000]
    swaps3 = []
    # Original sum: 1 - 10^9 + 1 - 10^9 + 1 - 10^9 = 3 - 3*10^9 = -2999999997
    expected3 = -2999999997
    assert s.maxAlternatingSum(nums3, swaps3) == expected3, f"Test 3 failed. Input: {nums3}, {swaps3}, Expected: {expected3}, Got: {s.maxAlternatingSum(nums3, swaps3)}"

    # Custom test: all elements in one component
    nums4 = [10, 5, 20, 15] # Values
    # Indices: 0(E), 1(O), 2(E), 3(O)
    swaps4 = [[0,1],[1,2],[2,3]] # All indices 0,1,2,3 are connected
    # Sorted values: [5, 10, 15, 20]
    # Even count: 2 (indices 0, 2), Odd count: 2 (indices 1, 3)
    # Add largest 2 values: 15, 20 -> +15 +20
    # Subtract smallest 2 values: 5, 10 -> -5 -10
    # Expected sum: (15 + 20) - (5 + 10) = 35 - 15 = 20
    expected4 = 20
    assert s.maxAlternatingSum(nums4, swaps4) == expected4, f"Test 4 failed. Input: {nums4}, {swaps4}, Expected: {expected4}, Got: {s.maxAlternatingSum(nums4, swaps4)}"

    # Custom test: multiple separate components
    nums5 = [1, 10, 2, 20, 3, 30] # Values
    # Indices: 0(E), 1(O), 2(E), 3(O), 4(E), 5(O)
    swaps5 = [[0,2], [1,3]] # Components: {0,2}, {1,3}, {4}, {5} (indices 4 and 5 are not involved in swaps)
    
    # Component {0,2}: values=[1,2], even_count=2, odd_count=0. Add (1+2)=3.
    # Component {1,3}: values=[10,20], even_count=0, odd_count=2. Subtract (10+20)=-30.
    # Component {4}: values=[3], even_count=1, odd_count=0. Add 3.
    # Component {5}: values=[30], even_count=0, odd_count=1. Subtract 30.
    # Total sum: 3 - 30 + 3 - 30 = -54
    expected5 = -54
    assert s.maxAlternatingSum(nums5, swaps5) == expected5, f"Test 5 failed. Input: {nums5}, {swaps5}, Expected: {expected5}, Got: {s.maxAlternatingSum(nums5, swaps5)}"
    
    # Custom test: no swaps (each element is its own component)
    nums6 = [5, 10, 15, 20]
    swaps6 = []
    # Expected: 5 - 10 + 15 - 20 = -10
    expected6 = -10
    assert s.maxAlternatingSum(nums6, swaps6) == expected6, f"Test 6 failed. Input: {nums6}, {swaps6}, Expected: {expected6}, Got: {s.maxAlternatingSum(nums6, swaps6)}"


    print("All tests passed!")

```