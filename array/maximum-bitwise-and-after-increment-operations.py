"""
Maximum Bitwise AND After Increment Operations
Difficulty: Hard

Description:
This problem asks to find the largest possible bitwise AND value for a subset of `m` numbers, chosen from `nums` and incremented using at most `k` total operations. The core idea is to realize that if a certain bitwise AND value `X` is achievable, any smaller value `Y` (where `Y <= X`) is also achievable, making the problem amenable to binary search on the answer.

Example:
Input: nums = [3,1,2], k = 8, m = 2
Output: 6
Explanation: To achieve a bitwise AND of 6 for a subset of size 2, we can choose nums[0]=3 and nums[2]=2. Increment 3 to 6 (cost 3) and 2 to 6 (cost 4). Total cost is 7, which is <= k=8. For any value greater than 6, the cost would exceed k.

Approach:
The problem can be solved using binary search on the target bitwise AND value. We define a `check(target_and_value)` function that determines if it's possible to achieve `target_and_value` as the bitwise AND of an `m`-sized subset, using no more than `k` operations. For a number `num` to contribute to a bitwise AND of `target_and_value`, it must be transformed into `new_num` such that `new_num >= num` and `(new_num & target_and_value) == target_and_value`. The `get_cost` helper function calculates the minimum operations needed for this transformation. This function handles three cases: if `num` already satisfies the condition, cost is 0; if `num < target_and_value`, the minimum `new_num` is `target_and_value`, costing `target_and_value - num`; otherwise (`num > target_and_value` but `(num & target_and_value) != target_and_value`), the minimum `new_num` is `(num | target_and_value)`, costing `(num | target_and_value) - num`. Inside `check`, we compute this cost for all numbers in `nums`, sort these costs, and sum the `m` smallest costs. If this sum is less than or equal to `k`, `check` returns `True`. The binary search then finds the largest `target_and_value` for which `check` returns `True`. The search range for the bitwise AND value is from 0 to `max(nums) + k`.

Time Complexity: O(N log N * log(MAX_VAL)), where N is the length of `nums` and `MAX_VAL` is the maximum possible value for a number (approximately `2 * 10^9`). The `check` function takes O(N log N) due to sorting, and the binary search performs O(log(MAX_VAL)) iterations.
Space Complexity: O(N) for storing the costs list within the `check` function.
"""
from typing import List, Optional

class Solution:
    def maximumAND(self, nums: List[int], k: int, m: int) -> int:

        # Helper function to calculate the minimum cost to transform 'num'
        # so that it satisfies (new_num & target) == target.
        # This 'new_num' must also be >= 'num'.
        def get_cost(num: int, target: int) -> int:
            # Case 1: If 'num' already satisfies the bitwise AND condition.
            # This implies all bits set in 'target' are also set in 'num'.
            # Also, if target > 0, this means num >= target.
            # No operations needed.
            if (num & target) == target:
                return 0
            
            # Case 2: 'num' is less than 'target', and does not satisfy the condition.
            # The minimum value 'num' must become to satisfy (val & target) == target
            # and val >= num, is 'target' itself.
            # Example: num=3 (011_2), target=6 (110_2). (3&6)=2!=6. num < target.
            # We need to change 3 to 6. Cost = 6 - 3 = 3 operations.
            if num < target:
                return target - num
            
            # Case 3: 'num' is greater than 'target', but does not satisfy the condition.
            # This means 'num' is larger than 'target' but is missing some bits
            # that 'target' has. We need to increment 'num' until all bits of
            # 'target' are set.
            # The smallest such number is achieved by taking 'num' and OR-ing it
            # with 'target'. This sets all required bits in 'num'.
            # Example: num=6 (110_2), target=5 (101_2). (6&5)=4!=5. num > target.
            # Cost = (6 | 5) - 6 = 7 - 6 = 1. (6 becomes 7)
            # Example: num=8 (1000_2), target=4 (0100_2). (8&4)=0!=4. num > target.
            # Cost = (8 | 4) - 8 = 12 - 8 = 4. (8 becomes 12)
            return (num | target) - num

        # Check function: returns True if it's possible to achieve 'target_and_value'
        # as bitwise AND for a subset of size 'm' using at most 'k' operations.
        def check(target_and_value: int) -> bool:
            # If target_and_value is 0, and nums[i] >= 1 (as per constraints),
            # then (num & 0) == 0 is always true for any num.
            # So, the cost for any number to achieve a bitwise AND of 0 is 0.
            # We can always pick m numbers with 0 total cost, which is <= k.
            if target_and_value == 0:
                return True

            costs = []
            for num in nums:
                costs.append(get_cost(num, target_and_value))
            
            # Sort the costs to pick the 'm' cheapest options.
            costs.sort()

            total_cost = 0
            for i in range(m):
                total_cost += costs[i]
            
            return total_cost <= k

        ans = 0
        # The maximum possible value for any element in nums is 10^9.
        # The maximum operations k is 10^9.
        # So, the maximum value an element can be incremented to is roughly 10^9 + 10^9 = 2 * 10^9.
        # The bitwise AND cannot exceed this potential maximum element value.
        # The lower bound for the answer is 0.
        # The upper bound can be set to max(nums) + k for a tighter range.
        low = 0
        high = max(nums) + k

        while low <= high:
            mid = low + (high - low) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    nums1 = [3,1,2]
    k1 = 8
    m1 = 2
    assert s.maximumAND(nums1, k1, m1) == 6, f"Test 1 Failed: Expected 6, Got {s.maximumAND(nums1, k1, m1)}"
    
    # Example 2
    nums2 = [1,2,8,4]
    k2 = 7
    m2 = 3
    assert s.maximumAND(nums2, k2, m2) == 4, f"Test 2 Failed: Expected 4, Got {s.maximumAND(nums2, k2, m2)}"
    
    # Example 3
    nums3 = [1,1]
    k3 = 3
    m3 = 2
    assert s.maximumAND(nums3, k3, m3) == 2, f"Test 3 Failed: Expected 2, Got {s.maximumAND(nums3, k3, m3)}"

    # Custom test case: m=1 (check if it acts like max(nums)+k for that num)
    nums4 = [10]
    k4 = 5
    m4 = 1
    assert s.maximumAND(nums4, k4, m4) == 15, f"Test 4 Failed: Expected 15, Got {s.maximumAND(nums4, k4, m4)}"

    # Custom test case: k=0 (no operations), find max AND of any subset
    nums5 = [7, 14, 21] # Binary: [0111, 1110, 10101]
    k5 = 0
    m5 = 2
    # Possible pairs and their AND:
    # (7,14) -> 0111 & 1110 = 0110 (6)
    # (7,21) -> 0111 & 10101 = 00101 (5)
    # (14,21) -> 1110 & 10101 = 1100 (12)
    # Max is 12
    assert s.maximumAND(nums5, k5, m5) == 12, f"Test 5 Failed: Expected 12, Got {s.maximumAND(nums5, k5, m5)}"

    # Custom test case: large numbers, large k, m=2. Maximize value.
    nums6 = [10**9, 10**9 + 1] # 10^9 is 0b111...00000000, 10^9+1 is 0b111...00000001
    k6 = 10**9
    m6 = 2
    # The maximum common bitmask within sum `max_val_in_nums + k` could be `2^30`.
    # 2^30 = 1073741824
    # get_cost(10^9, 2^30) = 2^30 - 10^9 = 73741824
    # get_cost(10^9+1, 2^30) = 2^30 - (10^9+1) = 73741823
    # Total cost = 73741824 + 73741823 = 147483647.
    # This cost (1.47 * 10^8) is <= k (10^9). So `check(2^30)` is True.
    # Any target higher than 2^30 will exceed k.
    assert s.maximumAND(nums6, k6, m6) == (1 << 30), f"Test 6 Failed: Expected {1<<30}, Got {s.maximumAND(nums6, k6, m6)}"

    # Custom test case: N large, m large, all nums small
    nums7 = [1] * 50000
    k7 = 10**9
    m7 = 50000
    # Average operations per number = k / m = 10^9 / 50000 = 20000.
    # So each 1 can be incremented to 1 + 20000 = 20001.
    # Target 20001: Cost for each num = 20001 - 1 = 20000. Total cost = 50000 * 20000 = 10^9. This is <= k.
    # Target 20002: Cost for each num = 20002 - 1 = 20001. Total cost = 50000 * 20001 = 10^9 + 50000. This is > k.
    # So the answer is 20001.
    assert s.maximumAND(nums7, k7, m7) == 20001, f"Test 7 Failed: Expected 20001, Got {s.maximumAND(nums7, k7, m7)}"
    
    print("All tests passed!")

