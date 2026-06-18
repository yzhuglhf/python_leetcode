"""
Count Subarrays With Majority Element II
Difficulty: Hard

Description:
This problem requires counting all subarrays within a given array `nums` where a specific `target` element is the majority element. An element is a majority element if it appears strictly more than half the times in the subarray. This condition can be rephrased as the count of `target` elements being strictly greater than the count of all other elements within the subarray.

Example:
Input: nums = [1,2,2,3], target = 2
Output: 5

Approach:
The core idea is to transform the original problem into counting subarrays with a positive sum. We construct a temporary array where each occurrence of `target` is replaced by `1`, and every other element is replaced by `-1`. In this transformed array, a subarray's sum being strictly positive directly corresponds to `target` being the majority element in the original subarray. We then use prefix sums combined with a Fenwick Tree (BIT) to efficiently count such subarrays. We maintain a `current_prefix_sum` as we iterate. For each `current_prefix_sum`, we query the BIT to find how many previous prefix sums (including an initial `0` for an empty prefix sum) are strictly less than the `current_prefix_sum`. This count is added to our total answer, and then the `current_prefix_sum`'s frequency is updated in the BIT. To handle negative prefix sums, all prefix sum values are offset by `N` (the array length) before being used as BIT indices.

Time Complexity: O(N log N) where N is the length of `nums`. Each of the N elements involves one update and one query operation on the Fenwick Tree, both taking O(log N) time because the BIT's size is proportional to N.
Space Complexity: O(N) for storing the Fenwick Tree.
"""
from typing import List

# Helper Fenwick Tree (BIT) class
class FenwickTree:
    def __init__(self, size):
        # The tree array uses 1-based indexing internally, hence size+1
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, delta):
        # Convert 0-based index to 1-based for BIT operations
        index += 1 
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index):
        # Convert 0-based index to 1-based for BIT operations
        # Querying index 'k' means summing frequencies from original 0-based index 0 to 'k'
        index += 1
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & (-index)
        return s

class Solution:
    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        
        # We need to map prefix sums from [-N, N] to [0, 2N]
        # So, balance + N will be the 0-based index in the Fenwick Tree
        # The BIT size needs to cover indices from 0 to 2N
        # Max balance is N, min balance is -N.
        # Max 0-based index: N + N = 2N. Min 0-based index: -N + N = 0.
        # So, BIT size should be 2N + 1 to cover 0-based indices 0 to 2N.
        bit_size = 2 * n + 1
        bit = FenwickTree(bit_size)
        
        # Offset to map balance to BIT index. A balance 'b' maps to BIT index 'b + offset'.
        offset = n
        
        ans = 0
        current_balance = 0
        
        # Initialize BIT with an entry for prefix sum 0, representing an empty prefix.
        # This handles subarrays that start from index 0.
        # The balance 0 maps to BIT index `0 + offset`.
        bit.update(0 + offset, 1) 
        
        for num in nums:
            if num == target:
                current_balance += 1
            else:
                current_balance -= 1
            
            # We are looking for previous_balance such that current_balance - previous_balance > 0
            # i.e., previous_balance < current_balance
            # Query the BIT for the count of all prefix sums strictly less than current_balance.
            # The highest 0-based index to query for values less than current_balance is (current_balance - 1).
            # This value maps to BIT index `(current_balance - 1) + offset`.
            ans += bit.query(current_balance - 1 + offset)
            
            # Add the current_balance to the BIT by updating its frequency.
            # The current_balance maps to BIT index `current_balance + offset`.
            bit.update(current_balance + offset, 1)
            
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [1,2,2,3]
    target1 = 2
    expected1 = 5
    assert s.countMajoritySubarrays(nums1, target1) == expected1, f"Test 1 Failed: {s.countMajoritySubarrays(nums1, target1)}"
    
    # Example 2
    nums2 = [1,1,1,1]
    target2 = 1
    expected2 = 10
    assert s.countMajoritySubarrays(nums2, target2) == expected2, f"Test 2 Failed: {s.countMajoritySubarrays(nums2, target2)}"
    
    # Example 3
    nums3 = [1,2,3]
    target3 = 4
    expected3 = 0
    assert s.countMajoritySubarrays(nums3, target3) == expected3, f"Test 3 Failed: {s.countMajoritySubarrays(nums3, target3)}"

    # Additional test cases
    # Single element, target is majority
    nums4 = [5]
    target4 = 5
    expected4 = 1 # Subarray: [5]
    assert s.countMajoritySubarrays(nums4, target4) == expected4, f"Test 4 Failed: {s.countMajoritySubarrays(nums4, target4)}"

    # Single element, target is not majority (or not present)
    nums5 = [5]
    target5 = 6
    expected5 = 0
    assert s.countMajoritySubarrays(nums5, target5) == expected5, f"Test 5 Failed: {s.countMajoritySubarrays(nums5, target5)}"

    # Array where target appears, and multiple are majority
    nums6 = [1,2,3,4,2,5,2]
    target6 = 2
    expected6 = 4 # Subarrays: [2] (at index 1), [2] (at index 4), [2] (at index 6), [2,5,2] (at indices 4-6)
    assert s.countMajoritySubarrays(nums6, target6) == expected6, f"Test 6 Failed: {s.countMajoritySubarrays(nums6, target6)}"

    # Empty nums (not possible per constraints, but good for understanding)
    # nums7 = []
    # target7 = 1
    # expected7 = 0
    # assert s.countMajoritySubarrays(nums7, target7) == expected7, f"Test 7 Failed: {s.countMajoritySubarrays(nums7, target7)}"

    # All elements not target
    nums8 = [1,2,3,4]
    target8 = 5
    expected8 = 0
    assert s.countMajoritySubarrays(nums8, target8) == expected8, f"Test 8 Failed: {s.countMajoritySubarrays(nums8, target8)}"

    print("All tests passed!")