"""
Maximum Total Value
Difficulty: Hard

Description:
This problem asks us to maximize the total value obtained by selecting items up to 'm' times. Each item 'i' has an initial value `value[i]` and a decay `decay[i]`. When an item 'i' is selected for the 't'-th time (1-indexed), the value gained is `value[i] - decay[i] * (t - 1)`. We must return the total value modulo 10^9 + 7.

Example:
Input: value = [6,5,4], decay = [2,1,1], m = 4
Output: 19
Explanation: The optimal sequence of selections includes picking index 0 (value 6), index 1 (value 5), index 2 (value 4), and index 0 again (value 6 - 2 = 4). Total value is 6 + 5 + 4 + 4 = 19.

Approach:
The core idea is to identify that we always want to select the options that provide the highest value. For each item, successive selections yield values forming a decreasing arithmetic progression: `value[i], value[i] - decay[i], value[i] - 2*decay[i], ...`. Since the number of items `N` and selections `m` can be very large (`10^5` and `10^9` respectively), we cannot generate all possible values and sort them directly.

Instead, we use a binary search approach to find a "threshold" value, `X_min`. This `X_min` represents the `m`-th largest value we would select if we were to list all possible positive values from all items and sort them in descending order. More formally, `X_min` is the largest integer `X` such that we can make at least `m` selections where each selection yields a value of at least `X`.

The algorithm proceeds in two main steps:

1.  **Binary Search for `X_min`**:
    *   We define a `check(X)` function that calculates the total count of selections across all items `i` that yield a value of *at least* `X`. For a given item `i`:
        *   If `value[i] < X`, it contributes 0 selections that meet the criteria.
        *   Otherwise (`value[i] >= X`), the number of times we can select item `i` such that the value gained is at least `X` is `(value[i] - X) // decay[i] + 1`. This formula counts `t` values where `value[i] - (t-1)*decay[i] >= X`.
    *   We perform a binary search for `X_min` in the range `[0, max(value) + 1]`.
    *   If `check(mid) >= m`, it means we can get `m` or more selections with a value of at least `mid`. We store `mid` as a potential `X_min` and try to find an even larger `mid` (`low = mid + 1`).
    *   If `check(mid) < m`, `mid` is too high; we don't have enough selections at or above this value. We reduce `mid` (`high = mid - 1`).
    *   After the binary search, `X_min` will hold the desired threshold value.

2.  **Calculate Total Value**:
    *   Initialize `total_value = 0` and `total_selections_strictly_greater_than_X_min = 0`.
    *   Iterate through each item `i` again:
        *   If `value[i] > X_min`:
            *   Calculate `k`, the number of selections for item `i` that yield a value *strictly greater* than `X_min`. This is `(value[i] - X_min - 1) // decay[i] + 1`.
            *   Add `k` to `total_selections_strictly_greater_than_X_min`.
            *   Calculate the sum of these `k` values using the arithmetic series sum formula: `S_k = k * a_1 - D * k * (k - 1) / 2`, where `a_1` is `value[i]` and `D` is `decay[i]`. Add this sum to `total_value`, ensuring all operations are done modulo `10^9 + 7`. For division by 2, use modular inverse `pow(2, MOD - 2, MOD)`.
    *   Calculate `remaining_m = m - total_selections_strictly_greater_than_X_min`. This is the number of additional selections we need to make.
    *   If `remaining_m > 0`:
        *   Count `count_of_X_min_selections`, the number of times `X_min` can be obtained (exactly) from each item `i` (i.e., `value[i] >= X_min` and `(value[i] - X_min) % decay[i] == 0`).
        *   Add `min(remaining_m, count_of_X_min_selections) * X_min` to `total_value`, again performing modulo arithmetic.

All intermediate sums and products are handled with modulo `10^9 + 7` to prevent overflow, especially for `total_value`. Python's arbitrary-precision integers handle large intermediate products before the final modulo operation.

Time Complexity: O(N * log(max(value_i)))
The binary search performs `log(max_value_bound)` iterations. In each iteration, we iterate through `N` items. Given `N <= 10^5` and `max(value_i) <= 10^9`, `log_2(10^9)` is approximately 30. Thus, `10^5 * 30 = 3 * 10^6` operations, which is efficient.
Space Complexity: O(1)
Only a few variables are used, independent of the input size.
"""
from typing import List

class Solution:
    def maxTotalValue(self, value: List[int], decay: List[int], m: int) -> int:
        MOD = 10**9 + 7
        
        # Modular inverse for division by 2 in sum of arithmetic series
        inv2 = pow(2, MOD - 2, MOD)

        # Binary search for X_min: the largest value such that we can make at least m selections
        # that yield a value of at least X_min.
        low = 0
        high = max(value) + 1 # A safe upper bound for potential values
        X_min = 0 # Stores the result of binary search

        while low <= high:
            mid = low + (high - low) // 2
            current_count = 0
            for i in range(len(value)):
                if value[i] >= mid:
                    # Calculate how many times item `i` can be selected to yield a value >= mid
                    # The t-th selection value is: value[i] - (t-1)*decay[i]
                    # We need: value[i] - (t-1)*decay[i] >= mid
                    # (t-1)*decay[i] <= value[i] - mid
                    # t-1 <= (value[i] - mid) / decay[i]
                    # The number of such t (starting from 1) is: floor((value[i] - mid) / decay[i]) + 1
                    k = (value[i] - mid) // decay[i] + 1
                    current_count += k
                    # Optimization: if current_count already exceeds m, no need to check further items
                    if current_count >= m:
                        break
            
            if current_count >= m:
                # We can get at least `m` selections with value >= `mid`.
                # This `mid` could be our X_min, or we might be able to find an even higher one.
                X_min = mid
                low = mid + 1 
            else:
                # `mid` is too high; we cannot get `m` selections with value >= `mid`.
                high = mid - 1

        total_value = 0
        total_selections_strictly_greater_than_X_min = 0

        # Now, calculate the sum of values for all selections strictly greater than X_min
        for i in range(len(value)):
            if value[i] > X_min:
                # Calculate `k`, the number of selections for item `i` that yield a value strictly greater than X_min
                # We need: value[i] - (t-1)*decay[i] > X_min
                # (t-1)*decay[i] < value[i] - X_min
                # t-1 < (value[i] - X_min) / decay[i]
                # The maximum integer for t-1 is floor((value[i] - X_min - 1) / decay[i])
                # So k = floor((value[i] - X_min - 1) / decay[i]) + 1
                k = (value[i] - X_min - 1) // decay[i] + 1
                total_selections_strictly_greater_than_X_min += k

                # Sum of an arithmetic progression: S_k = k * a_1 - D * k * (k-1) / 2
                # Here, a_1 = value[i], D = decay[i]
                first_term_mod = value[i] % MOD
                decay_term_mod = decay[i] % MOD
                k_mod = k % MOD

                sum_k_times_first_term = (k_mod * first_term_mod) % MOD
                
                # Calculate (decay_term * k * (k-1) / 2) % MOD
                sum_decay_part = (decay_term_mod * k_mod) % MOD
                sum_decay_part = (sum_decay_part * ((k_mod - 1 + MOD) % MOD)) % MOD # (k-1) could be 0, (k_mod-1) could be negative if k_mod=0. Add MOD to ensure positive before final modulo.
                sum_decay_part = (sum_decay_part * inv2) % MOD

                current_item_value = (sum_k_times_first_term - sum_decay_part + MOD) % MOD
                total_value = (total_value + current_item_value) % MOD

        # Determine how many more selections are needed from those yielding exactly X_min
        remaining_m = m - total_selections_strictly_greater_than_X_min
        
        if remaining_m > 0:
            count_of_X_min_selections = 0
            for i in range(len(value)):
                # Check if item `i` can yield a value exactly equal to X_min
                if value[i] >= X_min and (value[i] - X_min) % decay[i] == 0:
                    # This selection (`X_min` from item `i`) hasn't been counted in `total_selections_strictly_greater_than_X_min`.
                    count_of_X_min_selections += 1
            
            # Take `remaining_m` selections from the available `X_min` choices, but no more than `count_of_X_min_selections`.
            num_to_take_at_X_min = min(remaining_m, count_of_X_min_selections)
            
            # Add the value from these selections
            total_value = (total_value + (num_to_take_at_X_min * (X_min % MOD))) % MOD
            # Python's arbitrary-precision integers handle `num_to_take_at_X_min * X_min` directly before the modulo.

        return total_value

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    value1 = [6,5,4]
    decay1 = [2,1,1]
    m1 = 4
    assert s.maxTotalValue(value1, decay1, m1) == 19, f"Test Case 1 Failed: Expected 19, Got {s.maxTotalValue(value1, decay1, m1)}"
    
    # Example 2
    value2 = [7,2,2]
    decay2 = [3,2,1]
    m2 = 2
    assert s.maxTotalValue(value2, decay2, m2) == 11, f"Test Case 2 Failed: Expected 11, Got {s.maxTotalValue(value2, decay2, m2)}"
    
    # Example 3
    value3 = [4,3]
    decay3 = [5,4]
    m3 = 5
    assert s.maxTotalValue(value3, decay3, m3) == 7, f"Test Case 3 Failed: Expected 7, Got {s.maxTotalValue(value3, decay3, m3)}"

    # Custom test case: m=1
    value4 = [10, 1, 5]
    decay4 = [1, 1, 1]
    m4 = 1
    assert s.maxTotalValue(value4, decay4, m4) == 10, f"Test Case 4 Failed: Expected 10, Got {s.maxTotalValue(value4, decay4, m4)}"

    # Custom test case: large m, decay=1
    value5 = [10, 20, 30]
    decay5 = [1, 1, 1]
    m5 = 5
    # Optimal selections: 30, 29, 20, 19, 10. Sum = 108.
    assert s.maxTotalValue(value5, decay5, m5) == 108, f"Test Case 5 Failed: Expected 108, Got {s.maxTotalValue(value5, decay5, m5)}"

    # Custom test case: single item, many selections
    value6 = [100]
    decay6 = [5]
    m6 = 10
    # Values: 100, 95, 90, 85, 80, 75, 70, 65, 60, 55. Sum = 10 * (100+55)/2 = 775.
    assert s.maxTotalValue(value6, decay6, m6) == 775, f"Test Case 6 Failed: Expected 775, Got {s.maxTotalValue(value6, decay6, m6)}"

    # Custom test case: large values, large m, result calculation
    value7 = [10**9, 10**9]
    decay7 = [1, 1]
    m7 = 2 * (10**9) - 1 # Take almost all values from both
    # Expected total value modulo (10^9+7) is 41
    # Mathematical derivation: (10^9-1) * (10^9+2) + 1 = 10^18 + 10^9 - 1
    # (P-8)(P-5)+1 mod P = 40+1 = 41 mod P, where P = 10^9+7
    assert s.maxTotalValue(value7, decay7, m7) == 41, f"Test Case 7 Failed: Expected 41, Got {s.maxTotalValue(value7, decay7, m7)}"

    print("All tests passed!")

