"""
Maximum Value of an Alternating Sequence
Difficulty: Medium

Description:
This problem asks for the maximum possible element in an alternating sequence of length `n`, starting with `s`, where adjacent elements differ by at most `m`. An alternating sequence means the trend (increasing/decreasing) reverses at each step.

Example:
Input: n = 4, s = 3, m = 5
Output: 12
Explanation: One valid sequence is [3, 8, 7, 12]. The maximum element in the sequence is 12.

Approach:
The problem can be modeled using dynamic programming where we track the maximum possible value an element `seq[k]` can take, considering whether the sequence ended with an "up" move (`seq[k-1] < seq[k]`) or a "down" move (`seq[k-1] > seq[k]`). Let `s_max_up[k]` be the maximum value of `seq[k]` ending with an up-move, and `s_max_down[k]` for a down-move.

The recurrence relations for `k > 0` are:
`s_max_up[k] = s_max_down[k-1] + m`
`s_max_down[k] = s_max_up[k-1] - 1`

Base case `k=0`: `s_max_up[0] = s`, `s_max_down[0] = s`. The overall maximum element found starts at `s`.

By tracing these values for `k = 0, 1, 2, ...`:
- `k=0`: `s_max_up=s`, `s_max_down=s`. Current `overall_max=s`.
- `k=1`: `s_max_up=s+m`, `s_max_down=s-1`. Current `overall_max=max(s, s+m, s-1)=s+m`.
- `k=2`: `s_max_up=s+m-1`, `s_max_down=s+m-1`. Current `overall_max=max(s+m, s+m-1)=s+m`.
- `k=3`: `s_max_up=s+2m-1`, `s_max_down=s+m-2`. Current `overall_max=max(s+m, s+2m-1, s+m-2)=s+2m-1`.

We observe that the overall maximum element is always achieved at an odd index `k` by `s_max_up[k]`.
Specifically, for an odd index `k = 2j+1`, `s_max_up[k]` follows the pattern `s + m + j * (m-1)`.
The goal is to find the maximum possible element that can appear in *any* valid sequence of length up to `n`. This means we need to find the largest value `s_max_up[k]` for `k` such that `k < n` and `k` is odd.

Let `idx_max_odd` be the largest odd index reachable (i.e., `idx_max_odd <= n-1`).
1. If `n = 1`, the sequence is just `[s]`, so the maximum element is `s`.
2. If `n > 1`:
   - If `n` is even, then `n-1` is odd. So, `idx_max_odd = n-1`.
   - If `n` is odd, then `n-1` is even. So, the largest odd index is `n-2`. (Since `n > 1` here, `n` is at least 3, so `n-2` is at least 1).

Once `idx_max_odd` is determined, we calculate `j = (idx_max_odd - 1) // 2`.
The maximum possible value is then `s + m + j * (m-1)`.

This approach uses constant space and performs a few arithmetic operations, making it an `O(1)` time complexity solution.

Time Complexity: O(1)
Space Complexity: O(1)
"""
from typing import List, Optional

class Solution:
    def maximumValue(self, n: int, s: int, m: int) -> int:
        # Base case: if sequence length is 1, the only element is s.
        if n == 1:
            return s
        
        # Determine the largest odd index (k) such that k < n.
        # This is where the maximum value (s_max_up[k]) would occur.
        idx_max_odd: int
        if (n - 1) % 2 == 1:  # (n-1) is odd, meaning n is even
            idx_max_odd = n - 1
        else:  # (n-1) is even, meaning n is odd. The largest odd index is n-2.
            # Since n > 1 and n is odd, n is at least 3. Thus n-2 >= 1.
            idx_max_odd = n - 2
            
        # The general formula for s_max_up[k] where k = 2j+1 is s + m + j * (m-1).
        # We need to find j for our idx_max_odd.
        # j = (k - 1) // 2
        j = (idx_max_odd - 1) // 2
        
        # Calculate the maximum value using the derived formula.
        return s + m + j * (m - 1)

if __name__ == "__main__":
    s_obj = Solution()

    # Example 1
    assert s_obj.maximumValue(n = 4, s = 3, m = 5) == 12, "Example 1 Failed"

    # Example 2
    assert s_obj.maximumValue(n = 2, s = 4, m = 3) == 7, "Example 2 Failed"

    # Custom Test Cases
    # n=1 case
    assert s_obj.maximumValue(n = 1, s = 10, m = 100) == 10, "Test Case 1 Failed: n=1"
    
    # n=3 case (n is odd)
    assert s_obj.maximumValue(n = 3, s = 3, m = 5) == 8, "Test Case 2 Failed: n=3, s=3, m=5"
    # Sequence: [3, 8, 7]. Max is 8.

    # m=1 case (m-1 = 0)
    assert s_obj.maximumValue(n = 5, s = 10, m = 1) == 11, "Test Case 3 Failed: m=1"
    # Sequence e.g., [10, 11, 10, 11, 10]. Max is 11.

    # Large values
    assert s_obj.maximumValue(n = 10**9, s = 1, m = 10**5) == 1 + 10**5 + ( (10**9 - 2) // 2 ) * (10**5 - 1), "Test Case 4 Failed: Large n, s, m"
    assert s_obj.maximumValue(n=10**9, s=1, m=10**5) == 50000000000000, "Test Case 4 Failed: Calculated value"
    
    # Check with n=10^9 and m=1
    assert s_obj.maximumValue(n = 10**9, s = 1, m = 1) == 1 + 1 + ( (10**9 - 2) // 2 ) * (1-1), "Test Case 5 Failed: Large n, m=1"
    assert s_obj.maximumValue(n = 10**9, s = 1, m = 1) == 2, "Test Case 5 Failed: Calculated value for m=1"

    print("All tests passed!")

```