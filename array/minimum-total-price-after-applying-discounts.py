"""
Minimum Total Price After Applying Discounts
Difficulty: Medium

Description:
This problem asks us to find the minimum possible sum of final prices after optimally applying a given set of discounts to a given set of items. Each discount can be applied to at most one item, and each item can receive at most one discount. Items may also receive no discount. The final price after a `d` percent discount on price `p` is `p * (100 - d) / 100`.

Example:
Input: prices = [10,30,21], discounts = [50,60]
Output: 32.50000
Explanation: To minimize the total, we apply the largest discounts to the highest priced items. Sorted prices descending: [30, 21, 10]. Sorted discounts descending: [60, 50].
Apply 60% discount to 30: 30 * (100-60)/100 = 12.0
Apply 50% discount to 21: 21 * (100-50)/100 = 10.5
The item with price 10 receives no discount, contributing 10.0.
Total = 12.0 + 10.5 + 10.0 = 32.5.

Approach:
To minimize the total final price, we must maximize the total amount saved by applying discounts. The absolute amount saved for an item with price `p` using a discount `d` is `p * d / 100`. To maximize this sum of savings, a greedy strategy is optimal: pair the highest available price with the highest available discount. This is because a larger discount percentage applied to a larger initial price results in a greater absolute saving compared to applying it to a smaller price.
The algorithm proceeds as follows:
1. Sort the `prices` array in descending order.
2. Sort the `discounts` array in descending order.
3. Iterate through the sorted arrays, applying the `i`-th largest discount to the `i`-th highest priced item. This is done for `min(len(prices), len(discounts))` items. Calculate the discounted price for each such pair and add it to a running total.
4. Any remaining items in the `prices` array (those that did not receive a discount because there were fewer discounts than items) receive no discount. Their original prices are added to the running total.
This strategy ensures that the most impactful discounts (largest percentages) are applied to the items where they will yield the greatest absolute savings (highest prices), thereby minimizing the final total sum.

Time Complexity: O(N log N + M log M), where N is the length of `prices` and M is the length of `discounts`. This is dominated by the sorting steps.
Space Complexity: O(1) auxiliary space, as sorting is performed in-place in Python (for lists) and only a few variables are used to store the total sum and loop indices.
"""
import math
from typing import List, Optional

class Solution:
    def minPrice(self, prices: List[int], discounts: List[int]) -> float:
        # Sort prices in descending order.
        # This ensures that when we iterate, we are always considering the highest
        # priced items first, which should receive the highest discounts.
        prices.sort(reverse=True)
        
        # Sort discounts in descending order.
        # This ensures that when we iterate, we are always applying the largest
        # available discount percentage.
        discounts.sort(reverse=True)

        total_final_price = 0.0

        num_items = len(prices)
        num_discounts = len(discounts)

        # Determine how many items will receive a discount.
        # This is limited by the number of items or the number of available discounts,
        # whichever is smaller.
        items_to_discount = min(num_items, num_discounts)

        # Apply discounts: pair the highest price with the highest discount,
        # the second highest price with the second highest discount, and so on.
        for i in range(items_to_discount):
            p = prices[i]
            d = discounts[i]
            
            # Calculate the final price after applying the discount.
            # Using 100.0 ensures floating-point division even if p and (100-d) are integers.
            final_p = p * (100 - d) / 100.0
            total_final_price += final_p

        # Add the prices of any remaining items that did not receive a discount.
        # These will be the lowest priced items in the sorted 'prices' list
        # that couldn't be paired with an available discount.
        for i in range(items_to_discount, num_items):
            total_final_price += prices[i]

        return total_final_price

if __name__ == "__main__":
    s = Solution()

    # Example 1
    prices1 = [10, 30, 21]
    discounts1 = [50, 60]
    expected1 = 32.50000
    result1 = s.minPrice(prices1, discounts1)
    assert math.isclose(result1, expected1, rel_tol=1e-5), f"Test 1 failed: Expected {expected1}, got {result1}"
    print(f"Test 1 passed. Result: {result1}")

    # Example 2
    prices2 = [100, 70]
    discounts2 = [10, 40, 50]
    expected2 = 92.00000
    result2 = s.minPrice(prices2, discounts2)
    assert math.isclose(result2, expected2, rel_tol=1e-5), f"Test 2 failed: Expected {expected2}, got {result2}"
    print(f"Test 2 passed. Result: {result2}")

    # Example 3
    prices3 = [7, 3, 9]
    discounts3 = [100, 100]
    expected3 = 3.00000
    result3 = s.minPrice(prices3, discounts3)
    assert math.isclose(result3, expected3, rel_tol=1e-5), f"Test 3 failed: Expected {expected3}, got {result3}"
    print(f"Test 3 passed. Result: {result3}")

    # Additional Test Case: More prices than discounts
    prices4 = [50, 20, 80, 10]
    discounts4 = [20, 10]
    expected4 = 139.0 # (80 * 0.8) + (50 * 0.9) + 20 + 10 = 64 + 45 + 20 + 10 = 139
    result4 = s.minPrice(prices4, discounts4)
    assert math.isclose(result4, expected4, rel_tol=1e-5), f"Test 4 failed: Expected {expected4}, got {result4}"
    print(f"Test 4 passed. Result: {result4}")

    # Additional Test Case: More discounts than prices
    prices5 = [60, 40]
    discounts5 = [50, 30, 10]
    expected5 = 58.0 # (60 * 0.5) + (40 * 0.7) = 30 + 28 = 58
    result5 = s.minPrice(prices5, discounts5)
    assert math.isclose(result5, expected5, rel_tol=1e-5), f"Test 5 failed: Expected {expected5}, got {result5}"
    print(f"Test 5 passed. Result: {result5}")
    
    # Additional Test Case: Empty discounts list
    prices6 = [10, 20, 30]
    discounts6 = []
    expected6 = 60.0 # No discounts applied, sum of original prices
    result6 = s.minPrice(prices6, discounts6)
    assert math.isclose(result6, expected6, rel_tol=1e-5), f"Test 6 failed: Expected {expected6}, got {result6}"
    print(f"Test 6 passed. Result: {result6}")

    print("All tests passed!")