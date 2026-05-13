"""
Merge Adjacent Equal Elements
Difficulty: Medium

Description:
You are given an integer array. The task is to repeatedly merge the leftmost adjacent pair of equal elements by summing them. This operation modifies the array, and the process must be repeated on the updated array until no more adjacent equal elements can be found. The final array after all possible merges should be returned.

Example:
Input: nums = [3,1,1,2]
Output: [3,4]
Explanation:
1. The leftmost adjacent equal pair is (1, 1). They are merged into 1 + 1 = 2, resulting in the array [3, 2, 2].
2. In the updated array, the leftmost adjacent equal pair is (2, 2). They are merged into 2 + 2 = 4, resulting in [3, 4].
No more adjacent equal elements remain. Thus, the final array is [3, 4].

Approach:
The problem specifies choosing the "leftmost" adjacent pair for merging. A direct simulation involving list slicing or deletions would be inefficient due to the O(N) cost of such operations on Python lists, leading to an overall O(N^2) time complexity. A more efficient O(N) approach utilizes a stack-like data structure (implemented using a standard Python list).

We iterate through the input array `nums` from left to right. We maintain a `res` list, which acts as our stack. For each `num` in `nums`:
1. We check if `res` is not empty AND its last element (`res[-1]`) is equal to the current `num`.
2. If they are equal, it signifies an adjacent pair that can be merged. We perform the merge by popping `res[-1]` and adding it to `num`, effectively replacing the two elements with their sum. The crucial part is that this newly formed sum (now stored in `num`) must then immediately be re-evaluated against the *new* last element of `res`. This iterative checking and merging is handled by a `while` loop.
3. This `while` loop continues as long as `num` can merge with `res[-1]`. This mechanism inherently handles the "leftmost" rule, as a merged sum `X` will attempt to merge with its new left neighbor, and if it merges, the new sum `Y` will then attempt to merge with *its* left neighbor, and so on. This propagates merges correctly to the left.
4. Once `num` can no longer be merged with `res[-1]` (either `res` is empty, or `res[-1]` is different from `num`), we append the current `num` (which might be an original element or a sum of multiple merged elements) to `res`.
After iterating through all elements in `nums`, the `res` list will contain the final merged array.

Time Complexity: O(N), where N is the length of the input array `nums`. Each element from `nums` is pushed onto the `res` list at most once. Each element is popped from `res` at most once (when it's part of a merge operation). The total number of `append` and `pop` operations across the entire algorithm is proportional to `N`.
Space Complexity: O(N), where N is the length of the input array `nums`. In the worst case (e.g., `[1,2,3,4]` where no merges occur), the `res` list will store all N elements.
"""
from typing import List, Optional

class Solution:
    def mergeAdjacent(self, nums: List[int]) -> List[int]:
        res = [] # This list will act as a stack

        for num in nums:
            # While the stack is not empty and the current number can merge with the top of the stack
            while res and res[-1] == num:
                # Merge: pop the stack's top and add it to the current number
                num += res.pop()
            # After all possible merges to the left are done for the current num,
            # push the (possibly merged) num onto the stack
            res.append(num)
        
        return res

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.mergeAdjacent([3,1,1,2]) == [3,4], "Example 1 failed"

    # Example 2
    assert s.mergeAdjacent([2,2,4]) == [8], "Example 2 failed"

    # Example 3
    assert s.mergeAdjacent([3,7,5]) == [3,7,5], "Example 3 failed"

    # Additional test cases
    assert s.mergeAdjacent([1,1,1,1]) == [4], "Test case 4 failed: All ones"
    assert s.mergeAdjacent([1,2,2,4]) == [1,8], "Test case 5 failed: Chained merge"
    assert s.mergeAdjacent([1,1,2,2,4,4]) == [4,2,8], "Test case 6 failed: Complex merges"
    assert s.mergeAdjacent([1,1,1]) == [3], "Test case 7 failed: Three ones"
    assert s.mergeAdjacent([1]) == [1], "Test case 8 failed: Single element"
    assert s.mergeAdjacent([]) == [], "Test case 9 failed: Empty input"
    assert s.mergeAdjacent([5,5,5,5,5]) == [25], "Test case 10 failed: Many equal"
    assert s.mergeAdjacent([10,20,30,40]) == [10,20,30,40], "Test case 11 failed: No merges"
    
    print("All tests passed!")