"""
Longest Alternating Subarray After Removing At Most One Element
Difficulty: Hard

Description:
This problem asks for the maximum length of an alternating subarray after removing at most one element from the input array `nums`. An alternating subarray has elements that strictly alternate between greater and smaller (e.g., `a < b > c < d` or `a > b < c > d`). A single element subarray is considered alternating.

Example:
Input: `nums = [3,2,1,2,3,2,1]`
Output: `4`
Explanation: If we remove `nums[3]` (value `2`), the array becomes `[3,2,1,3,2,1]`. The subarray `[2,1,3,2]` (indices 1,2,3,4 from the modified array) is alternating: `2 > 1 < 3 > 2`, and has length 4. (The original example explanation was misleading; the array `[3,2,1,3,2,1]` itself is not alternating, but `[2,1,3,2]` is its alternating subarray.)

Approach:
The problem can be solved using dynamic programming with a prefix and suffix pass. We need to handle two main scenarios: no element removed, and exactly one element removed.

1.  **No element removed**: We find the longest alternating subarray in the original `nums` array. This can be done with a single pass. We maintain two DP states:
    *   `pref_up[i]`: Length of the longest alternating subarray ending at index `i`, where `nums[i-1] < nums[i]`.
    *   `pref_down[i]`: Length of the longest alternating subarray ending at index `i`, where `nums[i-1] > nums[i]`.
    For `i=0`, both `pref_up[0]` and `pref_down[0]` are 1 (a single element).
    For `i > 0`:
    *   If `nums[i] > nums[i-1]`, then `pref_up[i] = pref_down[i-1] + 1` (to form `... > X < Y`). `pref_down[i]` resets to 1.
    *   If `nums[i] < nums[i-1]`, then `pref_down[i] = pref_up[i-1] + 1` (to form `... < X > Y`). `pref_up[i]` resets to 1.
    *   If `nums[i] == nums[i-1]`, both `pref_up[i]` and `pref_down[i]` reset to 1 (sequence breaks).
    The maximum value among all `pref_up[i]` and `pref_down[i]` gives the longest alternating subarray without removal.

2.  **Exactly one element removed**: If we remove `nums[j]` (where `0 < j < n-1`), we are essentially trying to connect the alternating subarray ending at `nums[j-1]` with an alternating subarray starting at `nums[j+1]`. To facilitate this, we also compute suffix DP arrays:
    *   `suff_up[i]`: Length of the longest alternating subarray starting at index `i`, where `nums[i] < nums[i+1]`.
    *   `suff_down[i]`: Length of the longest alternating subarray starting at index `i`, where `nums[i] > nums[i+1]`.
    These are computed in a similar way but iterating from `n-2` down to `0`.

    After computing `pref_up/down` and `suff_up/down` arrays, we iterate through all possible removal indices `j` from `1` to `n-2`.
    For each `j`, we consider connecting `nums[j-1]` and `nums[j+1]`:
    *   If `nums[j-1] < nums[j+1]`: We need the left part to end with `> nums[j-1]` and the right part to start with `nums[j+1] >`. This forms `... > nums[j-1] < nums[j+1] > ...`. The length is `pref_down[j-1] + suff_down[j+1]`.
    *   If `nums[j-1] > nums[j+1]`: We need the left part to end with `< nums[j-1]` and the right part to start with `nums[j+1] <`. This forms `... < nums[j-1] > nums[j+1] < ...`. The length is `pref_up[j-1] + suff_up[j+1]`.
    *   If `nums[j-1] == nums[j+1]`, no alternating connection can be made by skipping `nums[j]`, so we don't update `max_len`.

The overall maximum length is tracked and returned.

Time Complexity: O(N) because we perform a constant number of passes over the array.
Space Complexity: O(N) for storing the four DP arrays (`pref_up`, `pref_down`, `suff_up`, `suff_down`).

"""
from typing import List, Optional

class Solution:
    def longestAlternating(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return n

        # pref_up[i]: length of longest alternating subarray ending at i,
        #             where the last comparison was nums[i-1] < nums[i]
        # pref_down[i]: length of longest alternating subarray ending at i,
        #               where the last comparison was nums[i-1] > nums[i]
        pref_up = [1] * n
        pref_down = [1] * n

        max_len = 1

        for i in range(1, n):
            # By default, a single element forms an alternating subarray of length 1.
            # So, if no valid extension is found, it resets to 1.
            pref_up[i] = 1
            pref_down[i] = 1

            if nums[i] > nums[i-1]:
                # If nums[i] is greater than nums[i-1], it forms an 'up' slope.
                # This 'up' slope must follow a 'down' slope (nums[prev] > nums[i-1]).
                pref_up[i] = pref_down[i-1] + 1
            elif nums[i] < nums[i-1]:
                # If nums[i] is smaller than nums[i-1], it forms a 'down' slope.
                # This 'down' slope must follow an 'up' slope (nums[prev] < nums[i-1]).
                pref_down[i] = pref_up[i-1] + 1
            # If nums[i] == nums[i-1], both pref_up[i] and pref_down[i] remain 1,
            # indicating no alternating extension, only a new sequence of length 1.
            
            max_len = max(max_len, pref_up[i], pref_down[i])

        # suff_up[i]: length of longest alternating subarray starting at i,
        #             where the first comparison will be nums[i] < nums[i+1]
        # suff_down[i]: length of longest alternating subarray starting at i,
        #               where the first comparison will be nums[i] > nums[i+1]
        suff_up = [1] * n
        suff_down = [1] * n

        for i in range(n - 2, -1, -1):
            # By default, a single element forms an alternating subarray of length 1.
            suff_up[i] = 1
            suff_down[i] = 1

            if nums[i] < nums[i+1]:
                # If nums[i] is smaller than nums[i+1], it forms an 'up' slope.
                # This 'up' slope must be followed by a 'down' slope (nums[i+1] > nums[next]).
                suff_up[i] = suff_down[i+1] + 1
            elif nums[i] > nums[i+1]:
                # If nums[i] is greater than nums[i+1], it forms a 'down' slope.
                # This 'down' slope must be followed by an 'up' slope (nums[i+1] < nums[next]).
                suff_down[i] = suff_up[i+1] + 1
            # If nums[i] == nums[i+1], both suff_up[i] and suff_down[i] remain 1.
            
        # Consider removing one element at index j (0 < j < N-1)
        # We try to connect nums[j-1] and nums[j+1]
        for j in range(1, n - 1):
            if nums[j-1] < nums[j+1]:
                # If nums[j-1] < nums[j+1], the connection is an 'up' slope.
                # To maintain alternation, the prefix part must end with a 'down' slope
                # (i.e., ... > nums[j-1]), and the suffix part must start with a 'down' slope
                # (i.e., nums[j+1] > ...). This forms: ... > nums[j-1] < nums[j+1] > ...
                current_len = pref_down[j-1] + suff_down[j+1]
                max_len = max(max_len, current_len)
            elif nums[j-1] > nums[j+1]:
                # If nums[j-1] > nums[j+1], the connection is a 'down' slope.
                # To maintain alternation, the prefix part must end with an 'up' slope
                # (i.e., ... < nums[j-1]), and the suffix part must start with an 'up' slope
                # (i.e., nums[j+1] < ...). This forms: ... < nums[j-1] > nums[j+1] < ...
                current_len = pref_up[j-1] + suff_up[j+1]
                max_len = max(max_len, current_len)
            # If nums[j-1] == nums[j+1], they cannot form an alternating connection.
            # The maximum length involving nums[j-1] or nums[j+1] would be
            # captured by the no-removal case already (length 1 for each element,
            # or any longer sequence not involving this specific connection).

        return max_len

if __name__ == "__main__":
    s = Solution()
    
    # Example 1
    assert s.longestAlternating(nums = [2,1,3,2]) == 4
    
    # Example 2
    assert s.longestAlternating(nums = [3,2,1,2,3,2,1]) == 4
    
    # Example 3
    assert s.longestAlternating(nums = [100000,100000]) == 1

    # Additional test cases
    assert s.longestAlternating(nums = [1,2]) == 2 # No removal, [1,2]
    assert s.longestAlternating(nums = [1,5,2]) == 3 # No removal, [1,5,2]
    assert s.longestAlternating(nums = [1,2,1]) == 3 # No removal, [1,2,1]
    assert s.longestAlternating(nums = [1,1,1,1]) == 1 # All same, max 1
    assert s.longestAlternating(nums = [1,2,3,4,5]) == 2 # Longest is [X,Y]
    assert s.longestAlternating(nums = [5,4,3,2,1]) == 2 # Longest is [X,Y]
    assert s.longestAlternating(nums = [1,3,2,4,3]) == 4 # No removal [1,3,2,4]
    assert s.longestAlternating(nums = [1,2,5,3,4]) == 4 # Remove 5 -> [1,2,3,4] (no), remove 2 -> [1,5,3,4] (len 3: 1<5>3). [1,2,3,4] is not alternating. Remove 2 -> [1,5,3,4] `1<5>3<4` len 4
    
    # Let's verify [1,2,5,3,4] output 4
    # N=5
    # Prefixes:
    # [1] -> up=1, down=1
    # [1,2] -> up=2, down=1 (1<2)
    # [1,2,5] -> up=pref_down[1]+1=1+1=2, down=1 (2<5)
    # [1,2,5,3] -> up=1, down=pref_up[2]+1=2+1=3 (5>3)
    # [1,2,5,3,4] -> up=pref_down[3]+1=3+1=4, down=1 (3<4)
    # max_len from prefixes is 4. (For [1,2,5,3,4] this gives [1,2,5,3,4] itself if it was alternating, but the last elements are 3<4 so 4 is pref_up[4] from pref_down[3]. pref_down[3] is from pref_up[2]=2 ([1,2,5]). So `[2,5,3,4]` is `2<5>3<4`, length 4. So `[1,2,5,3,4]` is `1<2<5>3<4`, not alt. but `[2,5,3,4]` is alt.)
    # Suffixes:
    # [4] -> up=1, down=1
    # [3,4] -> up=suff_down[4]+1=2, down=1 (3<4)
    # [5,3,4] -> up=1, down=suff_up[3]+1=3 (5>3<4)
    # [2,5,3,4] -> up=suff_down[2]+1=4, down=1 (2<5>3<4)
    # [1,2,5,3,4] -> up=1, down=suff_up[1]+1=2 (1<2)
    #
    # Combinations (j from 1 to N-2 (1 to 3)):
    # j=1 (remove 2): nums[0]=1, nums[2]=5. (1<5). Use pref_down[0]+suff_down[2] = 1+3=4. Sequence [1,5,3,4] (1<5>3<4). Valid. max_len = 4.
    # j=2 (remove 5): nums[1]=2, nums[3]=3. (2<3). Use pref_down[1]+suff_down[3] = 1+2=3. Sequence [1,2,3,4] (not alt). `pref_down[1]=1` is for `[2]`, `suff_down[3]=2` is for `[3,4]`. This becomes `[2,3,4]`. `2<3<4` not alt. Wait. `pref_down[1]` means `... > nums[1]`. `nums[0]>nums[1]` (not in this case, `1<2`). So `pref_down[1]` is `1`. This value is always 1 for this combination.
    # This calculation error is concerning. Let's re-verify the `pref_down` values for [1,2,5,3,4]:
    # nums:     [1, 2, 5, 3, 4]
    # pref_up:  [1, 2, 2, 1, 4] (correct)
    # pref_down:[1, 1, 1, 3, 1] (correct)
    # suff_up:  [1, 4, 1, 2, 1] (correct)
    # suff_down:[1, 1, 3, 1, 1] (correct)
    #
    # For j=1 (remove 2): nums[0]=1, nums[2]=5. (1<5).
    # current_len = pref_down[0] + suff_down[2] = 1 + 3 = 4. (Sequence `[1,5,3,4]` which is `1<5>3<4`, valid).
    # For j=2 (remove 5): nums[1]=2, nums[3]=3. (2<3).
    # current_len = pref_down[1] + suff_down[3] = 1 + 1 = 2. (Sequence `[2,3]`, valid, but smaller than 4).
    # For j=3 (remove 3): nums[2]=5, nums[4]=4. (5>4).
    # current_len = pref_up[2] + suff_up[4] = 2 + 1 = 3. (Sequence `[2,5,4]` which is `2<5>4`, valid, but smaller than 4).
    # Max is 4. Looks correct.

    print("All tests passed!")