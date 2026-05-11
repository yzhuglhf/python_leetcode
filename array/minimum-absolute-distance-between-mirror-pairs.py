"""
Minimum Absolute Distance Between Mirror Pairs
Difficulty: Medium

Description:
This problem asks us to find the minimum absolute difference between indices `i` and `j` for any "mirror pair". A mirror pair `(i, j)` with `i < j` exists if `reverse(nums[i]) == nums[j]`, where `reverse(x)` reverses the digits of `x` and omits leading zeros. If no such pair exists, return -1.

Example:
Input: `nums = [12,21,45,33,54]`
Output: `1`
Explanation: Pairs are `(0, 1)` (since `reverse(12)=21`) with distance `abs(0-1)=1`, and `(2, 4)` (since `reverse(45)=54`) with distance `abs(2-4)=2`. The minimum distance is `1`.

Approach:
We iterate through the `nums` array with index `j` from left to right. For each `nums[j]`, we first check if its value `nums[j]` has been observed as a reversed value of a previous number `nums[i]` (where `i < j`). We maintain a hash map, `last_seen_reverse_idx`, which stores the latest index `i` for each `value` that equals `reverse(nums[i])`. If `nums[j]` is found as a key in this map, it means `reverse(nums[i]) == nums[j]` for some `i < j`, and `i` is the value associated with `nums[j]` in the map. We then update our minimum distance with `j - i` (since `i < j`, `abs(i - j)` simplifies to `j - i`). Crucially, by storing only the *latest* `i` for each reversed value, we guarantee that `j - i` will be minimized for any `i` that satisfies the condition for the current `j`. After checking, we calculate `reversed_nums_j = reverse(nums[j])` and update `last_seen_reverse_idx[reversed_nums_j]` with the current index `j`. Finally, if no mirror pair was found, `min_abs_dist` remains infinity and we return -1; otherwise, we return the calculated minimum distance.

Time Complexity: O(N * D) where N is `len(nums)` and D is the maximum number of digits in an integer in `nums`. D is at most 10 for `10^9`, so effectively O(N). Each number reversal takes O(D) time, and hash map operations (insertion/lookup) take O(1) on average.
Space Complexity: O(N) in the worst case, as the `last_seen_reverse_idx` hash map can store up to N distinct reversed values and their corresponding indices.
"""
import math
from typing import List

class Solution:
    def _reverse(self, x: int) -> int:
        """
        Reverses the digits of an integer x.
        Leading zeros are omitted after reversing.
        Example: reverse(120) = 21.
        """
        s = str(x)
        reversed_s = s[::-1]
        return int(reversed_s)

    def minMirrorPairDistance(self, nums: List[int]) -> int:
        min_abs_dist = math.inf
        
        # last_seen_reverse_idx maps a reversed value V to the largest index i
        # such that reverse(nums[i]) == V.
        # This approach ensures we always get the 'i' closest to 'j' for a given 'current_num',
        # minimizing j - i directly.
        last_seen_reverse_idx = {} # type: dict[int, int]
        
        for j in range(len(nums)):
            current_num = nums[j]
            
            # Step 1: Check if current_num is the reverse of a previously seen number
            # i.e., find i < j such that reverse(nums[i]) == nums[j]
            if current_num in last_seen_reverse_idx:
                i = last_seen_reverse_idx[current_num]
                min_abs_dist = min(min_abs_dist, j - i)
            
            # Step 2: Add reverse(nums[j]) and its index j to the map
            # This updates the last seen index for reverse(nums[j]) to the current j,
            # effectively storing the largest i found so far for this reversed value.
            reversed_current_num = self._reverse(current_num)
            last_seen_reverse_idx[reversed_current_num] = j
            
        return int(min_abs_dist) if min_abs_dist != math.inf else -1

if __name__ == "__main__":
    s = Solution()

    # Example 1 from problem description
    assert s.minMirrorPairDistance(nums = [12,21,45,33,54]) == 1, "Example 1 Failed"
    # Example 2 from problem description
    assert s.minMirrorPairDistance(nums = [120,21]) == 1, "Example 2 Failed"
    # Example 3 from problem description
    assert s.minMirrorPairDistance(nums = [21,120]) == -1, "Example 3 Failed"
    
    # Custom test cases
    # All same numbers (e.g., all 1s, reverse(1) is 1)
    assert s.minMirrorPairDistance(nums = [1, 1, 1]) == 1, "Custom Test 1 Failed"
    # Basic mirror pair
    assert s.minMirrorPairDistance(nums = [123, 321]) == 1, "Custom Test 2 Failed"
    # No mirror pairs
    assert s.minMirrorPairDistance(nums = [1, 2, 3, 4, 5]) == -1, "Custom Test 3 Failed"
    # Number that reverses to a single digit
    assert s.minMirrorPairDistance(nums = [100, 1]) == 1, "Custom Test 4 Failed" # reverse(100) = 1
    assert s.minMirrorPairDistance(nums = [1000, 1]) == 1, "Custom Test 5 Failed" # reverse(1000) = 1
    # No mirror pairs with leading zeros
    assert s.minMirrorPairDistance(nums = [1, 2, 10, 20, 100]) == -1, "Custom Test 6 Failed" # reverse(10)=1, reverse(20)=2, reverse(100)=1
    # Multiple mirror pairs, check minimum
    assert s.minMirrorPairDistance(nums = [12345, 54321, 6789, 9876]) == 1, "Custom Test 7 Failed" # (0,1) dist 1, (2,3) dist 1. min is 1
    assert s.minMirrorPairDistance(nums = [1, 2, 3, 21, 12, 45, 54]) == 1, "Custom Test 8 Failed" # (3,4) dist 1. (5,6) dist 1. min is 1
    # Same number appears multiple times, creating a pair with itself
    assert s.minMirrorPairDistance(nums = [33, 44, 33]) == 2, "Custom Test 9 Failed" # reverse(33)=33. Pair (0,2) dist 2.

    print("All tests passed!")