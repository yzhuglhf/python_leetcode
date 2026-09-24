"""
Lexicographically Largest Power Array
Difficulty: Hard

Description:
Given an array of integers `nums`, the goal is to find a permutation `perm` of `nums` such that a derived `power` array is lexicographically largest. The `power` array has 15 elements, where `power[i]` is defined as the largest `j` such that the first `j` elements of `perm` all have the `(14 - i)`th bit set.

Example:
Input: nums = [3,1,7]
Output: [0,0,0,0,0,0,0,0,0,0,0,0,1,2,3]
Explanation: The permutation `perm = [7, 3, 1]` yields this result. For bit 2 (power[12]), only `perm[0]=7` has it set, so power[12]=1. For bit 1 (power[13]), `perm[0]=7` and `perm[1]=3` have it set, so power[13]=2. For bit 0 (power[14]), `perm[0]=7`, `perm[1]=3`, `perm[2]=1` all have it set, so power[14]=3. Other `power` values are 0 as relevant higher bits are not set in any number.

Approach:
The problem asks for the lexicographically largest `power` array, which implies maximizing `power[0]`, then `power[1]`, and so on. Each `power[i]` corresponds to checking the `(14 - i)`th bit. To achieve this, we need to construct a permutation `perm` of `nums`. A greedy strategy for lexicographical maximization often involves sorting. In this case, sorting `nums` in descending order proves to be effective. By placing larger numbers at the beginning of `perm`, we ensure that numbers with higher bit values or more set bits, which contribute to larger values for `power[i]` at earlier indices `i`, appear first. This arrangement helps in creating the longest possible prefix of elements that share a common set bit for each bit position, starting from the most significant bit (bit 14, for `power[0]`) down to the least significant bit (bit 0, for `power[14]`). After sorting `nums` to obtain `perm`, we iterate through each bit position from 14 down to 0 (corresponding to `power[0]` to `power[14]`) and count how many elements in the prefix of `perm` have that specific bit set, stopping at the first element that doesn't have the bit set.

Time Complexity: O(N log N)
The dominant factor is sorting `nums`, which takes O(N log N) time, where N is the length of `nums`. The subsequent loop to calculate the `power` array iterates 15 times (a constant), and within each iteration, it loops through `perm` at most N times. Thus, this part takes O(15 * N) = O(N) time.
Space Complexity: O(N)
Sorting `nums` might require O(N) auxiliary space if a new sorted list is created (e.g., Python's `sorted()` function). If sorting is done in-place, the space complexity would be O(log N) or O(1) depending on the sort implementation. The `power` array takes O(15) = O(1) space.
"""
from typing import List, Optional

class Solution:
    def largestPower(self, nums: List[int]) -> List[int]:
        # Step 1: Sort nums in descending order to form the permutation perm.
        # This greedy choice is crucial for maximizing lexicographical order of the power array.
        # Larger numbers tend to have higher bits set, or more bits set overall,
        # which helps in forming longer prefixes for the bits being checked.
        perm = sorted(nums, reverse=True)
        n = len(perm)
        
        # Step 2: Initialize the power array of length 15 with zeros.
        power = [0] * 15
        
        # Step 3: Iterate through each bit position from 14 down to 0.
        # This corresponds to power[0] for bit 14, power[1] for bit 13, ..., power[14] for bit 0.
        for i in range(15):
            # Calculate the bit position to check for the current power[i] entry.
            # power[0] corresponds to bit 14, power[1] to bit 13, ..., power[14] to bit 0.
            bit_to_check = 14 - i
            
            # Count the number of elements in the prefix of perm that have this bit set.
            current_prefix_count = 0
            for j in range(n):
                # Check if the 'bit_to_check'th bit is set in perm[j]
                if (perm[j] >> bit_to_check) & 1:
                    current_prefix_count += 1
                else:
                    # If the bit is not set, the prefix satisfying the condition ends here.
                    # All subsequent elements perm[k] (k > j) would also break this prefix condition
                    # if they were to be included, because they appear after perm[j] in the permutation.
                    break
            
            # Store the determined count in the power array.
            power[i] = current_prefix_count
            
        return power

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [7, 5]
    expected1 = [0,0,0,0,0,0,0,0,0,0,0,0,2,1,2]
    assert s.largestPower(nums1) == expected1, f"Test 1 failed: Input {nums1}, Expected {expected1}, Got {s.largestPower(nums1)}"
    print(f"Test 1 passed for input {nums1}")

    # Example 2
    nums2 = [3, 1, 7]
    expected2 = [0,0,0,0,0,0,0,0,0,0,0,0,1,2,3]
    assert s.largestPower(nums2) == expected2, f"Test 2 failed: Input {nums2}, Expected {expected2}, Got {s.largestPower(nums2)}"
    print(f"Test 2 passed for input {nums2}")

    # Custom test case: [6, 3, 1]
    # Sorted perm = [6, 3, 1]
    # 6: 110 (binary)
    # 3: 011 (binary)
    # 1: 001 (binary)
    #
    # Power array:
    # power[0]..power[11] (bits 14..3): 0 for all numbers -> 0
    # power[12] (bit 2): 6 has bit 2, 3 does not. -> count = 1
    # power[13] (bit 1): 6 has bit 1, 3 has bit 1, 1 does not. -> count = 2
    # power[14] (bit 0): 6 does not have bit 0. -> count = 0
    # Expected: [0,0,0,0,0,0,0,0,0,0,0,0,1,2,0]
    nums3 = [6, 3, 1]
    expected3 = [0,0,0,0,0,0,0,0,0,0,0,0,1,2,0]
    assert s.largestPower(nums3) == expected3, f"Test 3 failed: Input {nums3}, Expected {expected3}, Got {s.largestPower(nums3)}"
    print(f"Test 3 passed for input {nums3}")

    # Custom test case: nums with only one element
    nums4 = [10] # 10 = 0...01010_2
    # perm = [10]
    # Power array for relevant bits:
    # power[11] (bit 3): 10 has bit 3 -> count = 1
    # power[12] (bit 2): 10 does not have bit 2 -> count = 0
    # power[13] (bit 1): 10 has bit 1 -> count = 1
    # power[14] (bit 0): 10 does not have bit 0 -> count = 0
    expected4 = [0] * 11 + [1, 0, 1, 0]
    assert s.largestPower(nums4) == expected4, f"Test 4 failed: Input {nums4}, Expected {expected4}, Got {s.largestPower(nums4)}"
    print(f"Test 4 passed for input {nums4}")

    # Custom test case: all numbers have all bits set (2^15 - 1)
    nums5 = [32767, 32767, 32767] # 32767 = (2^15 - 1), all bits 0-14 are set
    # perm = [32767, 32767, 32767]
    # All numbers have all bits set, so for every bit, all 3 elements satisfy the condition.
    # All power values should be 3.
    expected5 = [3] * 15
    assert s.largestPower(nums5) == expected5, f"Test 5 failed: Input {nums5}, Expected {expected5}, Got {s.largestPower(nums5)}"
    print(f"Test 5 passed for input {nums5}")

    # Custom test case: all numbers are 0
    nums6 = [0, 0, 0]
    # perm = [0, 0, 0]
    # No number has any bit set.
    # All power values should be 0.
    expected6 = [0] * 15
    assert s.largestPower(nums6) == expected6, f"Test 6 failed: Input {nums6}, Expected {expected6}, Got {s.largestPower(nums6)}"
    print(f"Test 6 passed for input {nums6}")

    # Custom test case: N=1, nums=[0]
    nums7 = [0]
    expected7 = [0] * 15
    assert s.largestPower(nums7) == expected7, f"Test 7 failed: Input {nums7}, Expected {expected7}, Got {s.largestPower(nums7)}"
    print(f"Test 7 passed for input {nums7}")

    # Custom test case: N=1, nums=[1]
    nums8 = [1] # 1 = 0...001_2
    # Only power[14] (bit 0) should be 1, rest 0
    expected8 = [0] * 14 + [1]
    assert s.largestPower(nums8) == expected8, f"Test 8 failed: Input {nums8}, Expected {expected8}, Got {s.largestPower(nums8)}"
    print(f"Test 8 passed for input {nums8}")

    print("All tests passed!")
