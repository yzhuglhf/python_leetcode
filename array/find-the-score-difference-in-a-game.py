"""
Find the Score Difference in a Game
Difficulty: Medium

Description:
This problem simulates a game between two players over a series of rounds, where points are given by an array `nums`. Player roles (active/inactive) can swap based on two distinct rules applied sequentially for each game: first, if the current game's points are odd; and second, if the game is the 6th, 12th, 18th, etc. game. The active player for that game gains the points. The goal is to calculate the first player's total score minus the second player's total score.

Example:
Input: nums = [2,4,2,1,2,1]
Output: 4
Explanation: Initially player 1 is active.
Game 0 (points 2): P1 gains 2. (P1=2, P2=0, P1 active)
Game 1 (points 4): P1 gains 4. (P1=6, P2=0, P1 active)
Game 2 (points 2): P1 gains 2. (P1=8, P2=0, P1 active)
Game 3 (points 1): Points are odd, players swap. P2 becomes active and gains 1. (P1=8, P2=1, P2 active)
Game 4 (points 2): No swap. P2 remains active and gains 2. (P1=8, P2=3, P2 active)
Game 5 (points 1): Points are odd, players swap (P1 active). Then, it's the 6th game (index 5), players swap again (P2 active). P2 gains 1. (P1=8, P2=4, P2 active)
Final: P1 score = 8, P2 score = 4. Difference = 8 - 4 = 4.

Approach:
The problem can be solved by iterating through the `nums` array, keeping track of each player's accumulated score and which player is currently active. A boolean variable `player1_is_active` can be used to represent the active player, initialized to `True` (meaning Player 1 is active). For each game `i` (0-indexed) with `points = nums[i]`, we apply the two swap rules sequentially:
1. If `points` is odd, toggle `player1_is_active`.
2. If `(i + 1)` (the 1-indexed game number) is a multiple of 6, toggle `player1_is_active`.
After applying potential swaps, the player indicated by `player1_is_active` gains `points`. We maintain `score1` and `score2` accordingly. After processing all games, the function returns `score1 - score2`.

Time Complexity: O(N), where N is the length of the `nums` array. We iterate through the array exactly once, performing constant time operations in each iteration.
Space Complexity: O(1), as we only use a few constant-space variables to store scores and the active player's state.
"""
from typing import List, Optional

class Solution:
    def scoreDifference(self, nums: List[int]) -> int:
        score1 = 0
        score2 = 0
        player1_is_active = True # True if Player 1 is active, False if Player 2 is active

        for i, points in enumerate(nums):
            # Rule 1: If points are odd, active and inactive players swap roles.
            if points % 2 != 0:
                player1_is_active = not player1_is_active
            
            # Rule 2: In every 6th game (that is, game indices 5, 11, 17, ...), players swap roles.
            # (i + 1) represents the game number (1-indexed).
            # This condition is equivalent to i % 6 == 5 for 0-indexed i.
            if (i + 1) % 6 == 0: 
                player1_is_active = not player1_is_active
            
            # Rule 3: The active player plays the ith game and gains nums[i] points.
            if player1_is_active:
                score1 += points
            else:
                score2 += points
        
        return score1 - score2

if __name__ == "__main__":
    s = Solution()

    # Example 1:
    nums1 = [1,2,3]
    expected1 = 0
    assert s.scoreDifference(nums1) == expected1, f"Test 1 Failed: Input: {nums1}, Expected: {expected1}, Got: {s.scoreDifference(nums1)}"

    # Example 2:
    nums2 = [2,4,2,1,2,1]
    expected2 = 4
    assert s.scoreDifference(nums2) == expected2, f"Test 2 Failed: Input: {nums2}, Expected: {expected2}, Got: {s.scoreDifference(nums2)}"

    # Example 3:
    nums3 = [1]
    expected3 = -1
    assert s.scoreDifference(nums3) == expected3, f"Test 3 Failed: Input: {nums3}, Expected: {expected3}, Got: {s.scoreDifference(nums3)}"

    # Additional test cases:

    # All even points, no 6th game swaps, Player 1 always active
    nums4 = [2, 4, 6] 
    expected4 = 12 # P1: 2+4+6=12, P2: 0. Diff: 12
    assert s.scoreDifference(nums4) == expected4, f"Test 4 Failed: Input: {nums4}, Expected: {expected4}, Got: {s.scoreDifference(nums4)}"

    # All odd points, no 6th game swaps
    # Game 0 (1): odd -> swap, P2 active. P2 gets 1. (P1=0, P2=1)
    # Game 1 (3): odd -> swap, P1 active. P1 gets 3. (P1=3, P2=1)
    # Game 2 (5): odd -> swap, P2 active. P2 gets 5. (P1=3, P2=6)
    nums5 = [1, 3, 5] 
    expected5 = -3 # P1: 3, P2: 1+5=6. Diff: 3-6 = -3
    assert s.scoreDifference(nums5) == expected5, f"Test 5 Failed: Input: {nums5}, Expected: {expected5}, Got: {s.scoreDifference(nums5)}"

    # Test with exactly 6 games, various swaps
    # nums = [1, 2, 3, 4, 5, 6]
    # Initial: P1 active (score1=0, score2=0)
    # i=0, pts=1 (odd): Swap. P2 active. P2 gets 1. (P1=0, P2=1)
    # i=1, pts=2 (even): No swap. P2 active. P2 gets 2. (P1=0, P2=3)
    # i=2, pts=3 (odd): Swap. P1 active. P1 gets 3. (P1=3, P2=3)
    # i=3, pts=4 (even): No swap. P1 active. P1 gets 4. (P1=7, P2=3)
    # i=4, pts=5 (odd): Swap. P2 active. P2 gets 5. (P1=7, P2=8)
    # i=5, pts=6 (even):
    #   Rule 1 (pts even): No swap. (P2 active)
    #   Rule 2 (i=5 is 6th game): Swap. P1 active.
    #   P1 gets 6. (P1=13, P2=8)
    nums6 = [1, 2, 3, 4, 5, 6]
    expected6 = 5 # P1: 13, P2: 8. Diff: 13-8 = 5
    assert s.scoreDifference(nums6) == expected6, f"Test 6 Failed: Input: {nums6}, Expected: {expected6}, Got: {s.scoreDifference(nums6)}"

    # Test with multiple 6th game swaps
    # nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] (12 games)
    # Initial: P1 active (s1=0, s2=0)
    # G0(1): odd->swap. P2 gets 1. (P1=0, P2=1, P2 active)
    # G1(1): odd->swap. P1 gets 1. (P1=1, P2=1, P1 active)
    # G2(1): odd->swap. P2 gets 1. (P1=1, P2=2, P2 active)
    # G3(1): odd->swap. P1 gets 1. (P1=2, P2=2, P1 active)
    # G4(1): odd->swap. P2 gets 1. (P1=2, P2=3, P2 active)
    # G5(1): odd->swap(P1 active). 6th game->swap(P2 active). P2 gets 1. (P1=2, P2=4, P2 active)
    # G6(1): odd->swap. P1 gets 1. (P1=3, P2=4, P1 active)
    # G7(1): odd->swap. P2 gets 1. (P1=3, P2=5, P2 active)
    # G8(1): odd->swap. P1 gets 1. (P1=4, P2=5, P1 active)
    # G9(1): odd->swap. P2 gets 1. (P1=4, P2=6, P2 active)
    # G10(1): odd->swap. P1 gets 1. (P1=5, P2=6, P1 active)
    # G11(1): odd->swap(P2 active). 12th game->swap(P1 active). P1 gets 1. (P1=6, P2=6, P1 active)
    nums7 = [1] * 12
    expected7 = 0 # P1: 6, P2: 6. Diff: 0
    assert s.scoreDifference(nums7) == expected7, f"Test 7 Failed: Input: {nums7}, Expected: {expected7}, Got: {s.scoreDifference(nums7)}"


    print("All tests passed!")
