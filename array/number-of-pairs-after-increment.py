"""
Number of Pairs After Increment
Difficulty: Hard

Description:
This problem involves maintaining an array `nums2` that undergoes range updates and efficiently counting pairs `(j, k)` such that `nums1[j] + nums2[k] == tot`. The small size of `nums1` (max 5 elements) is a critical hint, suggesting that we can iterate through `nums1` elements and for each, query `nums2` for a specific target value. `nums2` is large and subject to range increments, which necessitates a data structure capable of handling range updates and efficient value counts.

Example:
Input: nums1 = [1,2], nums2 = [3,4], queries = [[2,5],[1,0,0,2],[2,5]]
Output: [2,1]

Approach:
The problem is solved using a Square Root Decomposition approach. The `nums2` array is divided into blocks of size approximately `sqrt(N)`, where `N` is the length of `nums2`. Each block maintains a sorted list of its current elements and a lazy tag representing pending increments for all elements within that block.

For a type 1 query `[1, x, y, val]` (range update):
1. The `nums2` array itself stores the true current values of its elements.
2. If the update range `[x, y]` falls entirely within a single block, elements in `nums2` from `x` to `y` are directly updated, and the corresponding block's sorted list is rebuilt.
3. If the update range spans multiple blocks, elements in the partial blocks at the ends of the range are directly updated in `nums2`, and their blocks are rebuilt. For all full blocks entirely contained within `[x, y]`, their lazy tags are incremented by `val`. This approach balances the cost between direct updates/rebuilds and lazy propagation.

For a type 2 query `[2, tot]` (count pairs):
1. Iterate through each element `n1_val` in `nums1`. For each `n1_val`, the target value we are looking for in `nums2` is `target_val = tot - n1_val`.
2. For each block:
   a. Calculate the effective target value to search for in the block's sorted list by subtracting the block's lazy tag: `search_val = target_val - lazy_updates[i]`.
   b. Use binary search (specifically `bisect_left` and `bisect_right` from the `bisect` module) on the block's sorted list to count occurrences of `search_val`.
   c. Add this count to the total pairs.
This method efficiently handles range updates and value queries by balancing the cost between direct updates/rebuilds and lazy propagation.

Time Complexity: O(N log(sqrt(N)) + Q * (sqrt(N) log(sqrt(N)) + M1 * sqrt(N) log(sqrt(N))))
Let N be `len(nums2)`, M1 be `len(nums1)`, and Q be `len(queries)`.
- Initialization: O(N log(sqrt(N))) to sort all blocks initially.
- Type 1 Query (update): O(sqrt(N) log(sqrt(N))) in the worst case (rebuilding two partial blocks, and updating lazy tags for `sqrt(N)` full blocks).
- Type 2 Query (count): For each of M1 elements in `nums1`, we iterate through `sqrt(N)` blocks, performing a binary search (log(sqrt(N))) on each. Total: O(M1 * sqrt(N) log(sqrt(N))).
The dominant term is roughly O(Q * M1 * sqrt(N) log(sqrt(N))). Given the constraints (N=5*10^4, M1=5, Q=5*10^4), this results in approximately 4.5 * 10^8 operations, which is tight but generally passes in Python due to optimized built-in functions.

Space Complexity: O(N) for storing `nums2`, `blocks` (total N elements across all sorted lists), and `lazy_updates` (sqrt(N) elements).
"""
from typing import List
import bisect

class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        N = len(nums2)
        
        # Determine block size. A common choice is sqrt(N).
        # Ensures BLOCK_SIZE is at least 1, even if N is very small.
        BLOCK_SIZE = max(1, int(N**0.5))
        
        # Calculate the number of blocks needed
        num_blocks = (N + BLOCK_SIZE - 1) // BLOCK_SIZE

        # `blocks[i]` stores the sorted elements of the i-th block.
        # These elements are the actual values in `nums2` within that block's range,
        # and do NOT include the `lazy_updates[i]` value.
        blocks = [[] for _ in range(num_blocks)]
        
        # `lazy_updates[i]` stores the accumulated increment for all elements conceptually in `blocks[i]`.
        # When querying, the `lazy_updates[i]` value must be accounted for.
        lazy_updates = [0] * num_blocks

        # Initialize blocks by populating them with initial nums2 values and sorting.
        for i in range(num_blocks):
            start_idx = i * BLOCK_SIZE
            end_idx = min(start_idx + BLOCK_SIZE, N)
            blocks[i] = sorted(nums2[start_idx:end_idx])

        # Helper function to rebuild a block's sorted list after direct updates to `nums2` elements.
        def rebuild_block(block_idx):
            start_idx = block_idx * BLOCK_SIZE
            end_idx = min(start_idx + BLOCK_SIZE, N)
            blocks[block_idx] = sorted(nums2[start_idx:end_idx])

        ans = []
        for query in queries:
            query_type = query[0]

            if query_type == 1: # Update query: [1, x, y, val]
                _, x, y, val = query
                
                block_x = x // BLOCK_SIZE
                block_y = y // BLOCK_SIZE

                # Apply updates to partial blocks
                if block_x == block_y:
                    # All updates are within a single block
                    for i in range(x, y + 1):
                        nums2[i] += val
                    rebuild_block(block_x)
                else:
                    # Update elements in the first partial block (from x to the end of block_x)
                    for i in range(x, (block_x + 1) * BLOCK_SIZE):
                        nums2[i] += val
                    rebuild_block(block_x)

                    # Update elements in the last partial block (from the start of block_y to y)
                    for i in range(block_y * BLOCK_SIZE, y + 1):
                        nums2[i] += val
                    rebuild_block(block_y)

                    # Apply lazy updates to full blocks in between (from block_x + 1 to block_y - 1)
                    for i in range(block_x + 1, block_y):
                        lazy_updates[i] += val

            else: # Query type == 2: [2, tot]
                _, tot = query
                current_pairs = 0
                
                # For each element in nums1, determine the target value in nums2
                for n1_val in nums1:
                    target_val = tot - n1_val
                    
                    # Iterate through all blocks to find occurrences of the target value
                    for i in range(num_blocks):
                        # The actual value we're looking for in nums2 elements within block i is `target_val`.
                        # However, the values stored in `blocks[i]` are the original values plus some previous direct updates,
                        # but WITHOUT the current `lazy_updates[i]`.
                        # So, if `stored_value + lazy_updates[i] == target_val`, then `stored_value == target_val - lazy_updates[i]`.
                        search_val = target_val - lazy_updates[i]
                        
                        # Count occurrences of `search_val` in the sorted `blocks[i]` list using binary search.
                        count = bisect.bisect_right(blocks[i], search_val) - bisect.bisect_left(blocks[i], search_val)
                        current_pairs += count
                ans.append(current_pairs)
        
        return ans

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1_1 = [1,2]
    nums2_1 = [3,4]
    queries_1 = [[2,5],[1,0,0,2],[2,5]]
    expected_1 = [2,1]
    assert s.numberOfPairs(nums1_1, nums2_1, queries_1) == expected_1, f"Test 1 Failed: {s.numberOfPairs(nums1_1, nums2_1, queries_1)}"

    # Example 2
    nums1_2 = [1,1]
    nums2_2 = [2,2,3]
    queries_2 = [[2,4],[1,0,1,1],[2,4]]
    expected_2 = [2,6]
    assert s.numberOfPairs(nums1_2, nums2_2, queries_2) == expected_2, f"Test 2 Failed: {s.numberOfPairs(nums1_2, nums2_2, queries_2)}"

    # Example 3
    nums1_3 = [2,5,8,4]
    nums2_3 = [1,3,8]
    queries_3 = [[2,9],[1,1,2,1],[2,10]]
    expected_3 = [1,0]
    assert s.numberOfPairs(nums1_3, nums2_3, queries_3) == expected_3, f"Test 3 Failed: {s.numberOfPairs(nums1_3, nums2_3, queries_3)}"

    # Custom Test Case 1: All updates on full blocks
    nums1_4 = [5]
    nums2_4 = [1,1,1,1,1,1,1,1,1,1] # N=10, BLOCK_SIZE=3, 4 blocks
    queries_4 = [[2,6], [1,0,9,1], [2,7]]
    # Initial: nums2 = [1,1,1,1,1,1,1,1,1,1].
    # Q0: [2,6]. n1=5, target=1. 10 pairs. Output: [10]
    # Q1: [1,0,9,1]. nums2 becomes [2,2,2,2,2,2,2,2,2,2].
    # Q2: [2,7]. n1=5, target=2. 10 pairs. Output: [10, 10]
    expected_4 = [10, 10]
    assert s.numberOfPairs(nums1_4, nums2_4, queries_4) == expected_4, f"Test 4 Failed: {s.numberOfPairs(nums1_4, nums2_4, queries_4)}"

    # Custom Test Case 2: Mixed partial and full block updates
    nums1_5 = [10]
    nums2_5 = [1,2,3,4,5,6,7,8,9,10,11,12] # N=12, BLOCK_SIZE=3, 4 blocks
    queries_5 = [[2,11], [1,1,10,2], [2,13]]
    # Initial: nums2=[1,2,3,4,5,6,7,8,9,10,11,12]
    # Q0: [2,11]. n1=10, target=1. 1 pair (nums2[0]=1). Output: [1]
    # Q1: [1,1,10,2]. Add 2 to nums2[1...10].
    # nums2 becomes: [1, 4,5,6,7,8,9,10,11,12,13,12]
    # Q2: [2,13]. n1=10, target=3. 1 pair (nums2[2]=3). Output: [1, 1]
    expected_5 = [1, 1]
    assert s.numberOfPairs(nums1_5, nums2_5, queries_5) == expected_5, f"Test 5 Failed: {s.numberOfPairs(nums1_5, nums2_5, queries_5)}"

    print("All tests passed!")

