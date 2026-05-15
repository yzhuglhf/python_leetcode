"""
Minimum Cost to Acquire Required Items
Difficulty: Medium

Description:
This problem asks for the minimum cost to fulfill two item requirements, need1 and need2, using three types of items. Type 1 items provide 1 unit towards need1 at cost cost1, Type 2 items provide 1 unit towards need2 at cost cost2, and Type Both items provide 1 unit towards both need1 and need2 at cost costBoth. The challenge lies in efficiently finding the optimal number of each item type, especially since needs can be very large (up to 10^9), precluding a simple iterative or DP approach.

Example:
Input: cost1 = 3, cost2 = 2, costBoth = 1, need1 = 3, need2 = 2
Output: 3
Explanation: By purchasing 3 items of type 'Both', the total cost is 3 * 1 = 3. This satisfies need1 (3 >= 3) and need2 (3 >= 2). This is the minimum possible cost.

Approach:
Let 'z' be the number of Type Both items purchased. If we purchase 'z' Type Both items, we contribute 'z' units to both need1 and need2. The cost for these items is `z * costBoth`. After acquiring 'z' Type Both items, the remaining requirement for Type 1 is `max(0, need1 - z)` and for Type 2 is `max(0, need2 - z)`. These remaining requirements must be fulfilled by purchasing Type 1 and Type 2 items respectively. The cost for these additional items would be `max(0, need1 - z) * cost1 + max(0, need2 - z) * cost2`.
Thus, the total cost for a given 'z' is `f(z) = z * costBoth + max(0, need1 - z) * cost1 + max(0, need2 - z) * cost2`.
The function `f(z)` is a convex function, meaning its slope is non-decreasing. This property allows us to use ternary search to find the minimum value of `f(z)`. The optimal number of Type Both items, 'z', will be in the range from `0` up to `max(need1, need2)`. If `z` exceeds `max(need1, need2)`, both remaining needs become zero, and the cost `z * costBoth` will only increase (since costBoth >= 1), so we don't need to search beyond this upper bound.
The ternary search iteratively narrows down the interval `[low_z, high_z]` where the minimum might lie. We pick two points `m1` and `m2` within this interval and compare `f(m1)` and `f(m2)`. Based on which cost is lower, we discard one-third of the interval. This process continues until the interval becomes very small (e.g., contains 1, 2, or 3 elements). Finally, we linearly scan this small remaining interval to find the exact minimum cost. An explicit check for `need1 = 0` and `need2 = 0` handles the trivial case.

Time Complexity: O(log(max(need1, need2))) due to ternary search. For needs up to 10^9, log_3(10^9) is a very small number (approximately 19 iterations), making this efficient. The final linear scan is over a constant small number of elements.
Space Complexity: O(1) as only a few variables are used.
"""
from typing import List, Optional

class Solution:
    def minimumCost(self, cost1: int, cost2: int, costBoth: int, need1: int, need2: int) -> int:
        
        # Helper function to calculate total cost for a given number of 'both' items (z)
        def calculate_total_cost(z: int) -> int:
            # Calculate remaining needs after buying z 'both' items
            # max(0, ...) ensures needs don't go negative
            remaining_need1 = max(0, need1 - z)
            remaining_need2 = max(0, need2 - z)
            
            # Calculate total cost. Python's integers handle arbitrary size.
            return z * costBoth + remaining_need1 * cost1 + remaining_need2 * cost2

        # Handle trivial case where no items are needed
        if need1 == 0 and need2 == 0:
            return 0

        # Define the search range for 'z' (number of type 'both' items)
        # The maximum 'z' we might consider is max(need1, need2).
        # Buying more than this would lead to higher cost without further benefit.
        low_z, high_z = 0, max(need1, need2)

        # Initialize minimum cost to a very large value
        ans = float('inf')

        # Perform ternary search to find the minimum cost
        # The loop continues as long as there are at least 3 distinct values in [low_z, high_z]
        while low_z + 2 <= high_z:
            m1 = low_z + (high_z - low_z) // 3
            m2 = high_z - (high_z - low_z) // 3
            
            cost_m1 = calculate_total_cost(m1)
            cost_m2 = calculate_total_cost(m2)
            
            if cost_m1 < cost_m2:
                # The minimum is in the left two-thirds [low_z, m2].
                # We include m2 as it could potentially be the minimum.
                high_z = m2 
            else:
                # The minimum is in the right two-thirds [m1, high_z].
                # We include m1 as it could potentially be the minimum.
                low_z = m1 

        # After the loop, the interval [low_z, high_z] will contain at most 3 elements.
        # Linearly iterate through this small range to find the exact minimum.
        for z_val in range(low_z, high_z + 1):
            ans = min(ans, calculate_total_cost(z_val))
        
        return ans

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.minimumCost(cost1=3, cost2=2, costBoth=1, need1=3, need2=2) == 3, "Example 1 Failed"
    
    # Example 2
    assert s.minimumCost(cost1=5, cost2=4, costBoth=15, need1=2, need2=3) == 22, "Example 2 Failed"
    
    # Example 3
    assert s.minimumCost(cost1=5, cost2=4, costBoth=15, need1=0, need2=0) == 0, "Example 3 Failed"

    # Custom test cases
    # Case: costBoth is very cheap, need only one type
    assert s.minimumCost(cost1=100, cost2=100, costBoth=1, need1=10, need2=0) == 10, "Custom Test 1 Failed"
    # Explanation: Buy 10 Type Both items (cost 10*1=10). Contributes 10 to need1 (>=10) and 10 to need2 (>=0).

    # Case: costBoth is expensive, cheaper to buy separately
    assert s.minimumCost(cost1=1, cost2=1, costBoth=10, need1=5, need2=5) == 10, "Custom Test 2 Failed"
    # Explanation: Buy 5 Type 1 (cost 5*1) and 5 Type 2 (cost 5*1). Total 10. (5 Type Both would cost 5*10=50).

    # Case: mixed scenario
    assert s.minimumCost(cost1=10, cost2=1, costBoth=2, need1=5, need2=1) == 10, "Custom Test 3 Failed"
    # Explanation:
    # z=0: 5*10 + 1*1 = 51
    # z=1: 1*2 + (5-1)*10 + max(0,1-1)*1 = 2 + 4*10 + 0 = 42
    # z=5: 5*2 + max(0,5-5)*10 + max(0,1-5)*1 = 10 + 0 + 0 = 10. Min is 10.

    # Case: very large needs, costBoth is cheapest
    assert s.minimumCost(cost1=10**6, cost2=10**6, costBoth=1, need1=10**9, need2=10**9) == 10**9, "Custom Test 4 Failed"
    # Explanation: Buy 10^9 Type Both items. Total cost = 10^9 * 1 = 10^9.

    # Case: very large needs, costBoth is expensive
    assert s.minimumCost(cost1=1, cost2=1, costBoth=10**6, need1=10**9, need2=10**9) == 2 * 10**9, "Custom Test 5 Failed"
    # Explanation: Buy 10^9 Type 1 and 10^9 Type 2. Total cost = 10^9 * 1 + 10^9 * 1 = 2 * 10^9.

    # Case: Another mixed scenario
    assert s.minimumCost(cost1=10, cost2=100, costBoth=5, need1=10, need2=1) == 50, "Custom Test 6 Failed"
    # Explanation:
    # z=0: Cost = 10*10 + 1*100 = 200
    # z=1: Cost = 1*5 + (10-1)*10 + max(0,1-1)*100 = 5 + 90 + 0 = 95
    # ...
    # z=10: Cost = 10*5 + max(0,10-10)*10 + max(0,1-10)*100 = 50 + 0 + 0 = 50. Min is 50.

    print("All tests passed!")

