"""
Minimum Total Cost to Process All Elements
Difficulty: Medium

Description:
This problem asks us to calculate the minimum total cost to process a sequence of elements `nums`, starting with `k` units of resources. If available resources are insufficient for `nums[i]`, we must perform operations to increase resources by `k`. Each operation incurs a sequential cost (1st operation costs 1, 2nd costs 2, etc.). The goal is to find the total cost modulo `10^9 + 7`.

Example:
Input: nums = [1,2,3,4], k = 4
Output: 3
Explanation: Initially 4 resources. Process 1 (left 3). Process 2 (left 1). For 3: need 3, have 1. Perform 1st operation (+4), cost 1. Resources become 1+4=5. Process 3 (left 2). For 4: need 4, have 2. Perform 2nd operation (+4), cost 2. Resources become 2+4=6. Process 4 (left 2). Total cost = 1+2 = 3.

Approach:
The problem can be solved by simulating the process greedily from left to right. We maintain `current_resources` (available resources), `operations_count` (the total number of operations performed across all elements), and `total_cost`. For each element `nums[i]`, we first check if `current_resources` are less than `nums[i]`. If so, we calculate the minimum number of additional operations (`X`) required to meet the demand. This `X` is found using ceiling division: `X = ceil((nums[i] - current_resources) / k)`. After determining `X`, `current_resources` are increased by `X * k`. The cost for these `X` new operations is the sum of an arithmetic series: `(operations_count + 1)`, `(operations_count + 2)`, ..., up to `(operations_count + X)`. This sum is `X * ( (operations_count + 1) + (operations_count + X) ) // 2`. This calculated cost is added to `total_cost`, and `operations_count` is updated by adding `X`. All additions to `total_cost` are performed modulo `10^9 + 7`, utilizing the modular inverse of 2 for the division step. Finally, regardless of whether operations were performed, `current_resources` are decreased by `nums[i]`. After iterating through all elements, `total_cost` will hold the minimum total cost.

Time Complexity: O(N), where N is the length of the `nums` array, as we iterate through the array once.
Space Complexity: O(1), as we only use a few constant extra variables.
"""
from typing import List

class Solution:
    def minimumCost(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        
        current_resources = k
        operations_count = 0  # Total number of operations performed across all elements
        total_cost = 0
        
        # Precompute modular inverse of 2 (since MOD is prime)
        inv2 = pow(2, MOD - 2, MOD)
        
        for num_i in nums:
            if current_resources < num_i:
                # Calculate how many operations (X) are needed
                # We need current_resources + X * k >= num_i
                # So, X * k >= num_i - current_resources
                # X >= (num_i - current_resources) / k
                
                needed_diff = num_i - current_resources
                
                # Use ceiling division: (A + B - 1) // B for ceil(A/B)
                # This correctly calculates the minimum integer X
                X = (needed_diff + k - 1) // k
                
                # Update current_resources by adding X*k
                current_resources += X * k
                
                # Calculate the cost for these X operations.
                # The costs are (operations_count + 1), ..., (operations_count + X)
                # This is an arithmetic series sum: X * (first_term + last_term) / 2
                
                first_new_op_cost = operations_count + 1
                last_new_op_cost = operations_count + X
                
                # Apply modular arithmetic for the cost calculation:
                # (X * (first_new_op_cost + last_new_op_cost) / 2) % MOD
                
                term_X_mod = X % MOD
                term_sum_mod = (first_new_op_cost % MOD + last_new_op_cost % MOD) % MOD
                
                cost_for_this_step = (term_X_mod * term_sum_mod % MOD * inv2) % MOD
                
                total_cost = (total_cost + cost_for_this_step) % MOD
                
                # Update the total count of operations performed
                operations_count += X
                
            # After ensuring sufficient resources, process the current element
            current_resources -= num_i
            
        return total_cost

if __name__ == "__main__":
    s = Solution()

    # Example 1
    nums1 = [1,2,3,4]
    k1 = 4
    expected1 = 3
    assert s.minimumCost(nums1, k1) == expected1, f"Test 1 Failed: {s.minimumCost(nums1, k1)}"

    # Example 2
    nums2 = [1,1,7,14]
    k2 = 4
    expected2 = 15
    assert s.minimumCost(nums2, k2) == expected2, f"Test 2 Failed: {s.minimumCost(nums2, k2)}"

    # Example 3
    nums3 = [1,2,3,4]
    k3 = 10
    expected3 = 0
    assert s.minimumCost(nums3, k3) == expected3, f"Test 3 Failed: {s.minimumCost(nums3, k3)}"

    # Custom Test 1: Single element needing operations
    nums4 = [10]
    k4 = 3
    # Initial: 3. Need 10. diff = 7. X = ceil(7/3) = 3 ops.
    # ops_count = 0. Costs: 1, 2, 3. Sum = 6.
    # Resources: 3 + 3*3 = 12. After proc 10: 12 - 10 = 2.
    expected4 = 6
    assert s.minimumCost(nums4, k4) == expected4, f"Test 4 Failed: {s.minimumCost(nums4, k4)}"

    # Custom Test 2: Multiple elements, some needing operations, some not
    nums5 = [5, 2, 8, 3]
    k5 = 5
    # Initial: 5 res, 0 ops, 0 cost
    # 1. num=5: res=5 >= 5. No ops. res = 5-5 = 0.
    # 2. num=2: res=0 < 2. diff=2. X=ceil(2/5)=1 op. res=0+1*5=5. op_count=0. Cost: 1. Total cost=1. op_count=1. res = 5-2=3.
    # 3. num=8: res=3 < 8. diff=5. X=ceil(5/5)=1 op. res=3+1*5=8. op_count=1. Cost: 1+1=2. Total cost=1+2=3. op_count=2. res = 8-8=0.
    # 4. num=3: res=0 < 3. diff=3. X=ceil(3/5)=1 op. res=0+1*5=5. op_count=2. Cost: 2+1=3. Total cost=3+3=6. op_count=3. res = 5-3=2.
    expected5 = 6
    assert s.minimumCost(nums5, k5) == expected5, f"Test 5 Failed: {s.minimumCost(nums5, k5)}"

    # Custom Test 3: Large values to test modulo and integer limits
    nums6 = [10**9, 10**9]
    k6 = 1
    # First num=10^9, k=1
    # res=1 < 10^9. diff = 10^9 - 1. X = (10^9 - 1) ops.
    # ops_count = 0. Cost is sum(1 to 10^9-1) = (10^9-1)*10^9/2.
    # (10^9-1) % MOD = (MOD-8). 10^9 % MOD = (MOD-7).
    # Cost = ((MOD-8) * (MOD-7) * inv2) % MOD = (56 * inv2) % MOD = 28.
    # total_cost = 28. ops_count = 10^9 - 1.
    # res = 1 + (10^9-1)*1 - 10^9 = 0.
    # Second num=10^9, k=1
    # res=0 < 10^9. diff = 10^9. X = 10^9 ops.
    # ops_count_prev = 10^9 - 1.
    # Costs are (10^9-1+1) to (10^9-1 + 10^9) => 10^9 to (2*10^9 - 1).
    # Sum = X * (first + last) / 2 = 10^9 * (10^9 + 2*10^9-1) / 2 = 10^9 * (3*10^9-1) / 2
    # X_mod = (MOD-7). First_mod = (MOD-7). Last_mod = (3*(MOD-7)-1) % MOD = (-21-1)%MOD = (-22)%MOD = (MOD-22).
    # Cost = ((MOD-7) * ((MOD-7) + (MOD-22)) % MOD * inv2) % MOD
    #      = ((MOD-7) * (-7 - 22) % MOD * inv2) % MOD
    #      = ((MOD-7) * (-29) % MOD * inv2) % MOD
    #      = (203 * inv2) % MOD = 101.5, becomes (203 * 500000004) % MOD = 102.
    # For (203 * inv2) % MOD: (203 * (MOD+1)/2) % MOD. 203 * 500000004 = 101500000812.
    # 101500000812 % (10^9+7) = 102.
    # Total cost = (28 + 102) % MOD = 130 % MOD = 130.
    expected6 = 130
    assert s.minimumCost(nums6, k6) == expected6, f"Test 6 Failed: {s.minimumCost(nums6, k6)}"

    print("All tests passed!")

