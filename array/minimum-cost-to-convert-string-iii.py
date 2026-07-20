"""
Minimum Cost to Convert String III
Difficulty: Hard

Description:
This problem asks for the minimum cost to transform a source string into a target string using a given set of transformation rules. Each rule specifies a pattern and a replacement string of the same length, along with a base cost. Patterns can contain wildcards ('*'). Applying a rule incurs its base cost plus one for each wildcard character matched. A crucial constraint is that once characters in a segment are used by a rule, they cannot be used again, effectively meaning rule applications must operate on disjoint segments of the string.

Example:
Input: source = "hello", target = "world", rules = [["he","wo"],["llo","rld"]], costs = [3,4]
Output: 7
Explanation: First, "he" is replaced by "wo" at cost 3, making the string "wollo". Then, "llo" is replaced by "rld" at cost 4, resulting in "world". Total cost is 3 + 4 = 7.

Approach:
This problem can be solved using dynamic programming. We define `dp[i]` as the minimum cost to transform the prefix `source[0...i-1]` into `target[0...i-1]`. The base case is `dp[0] = 0` for an empty prefix. For each `i` from 1 to `N` (length of the strings), `dp[i]` is initialized based on whether `source[i-1]` matches `target[i-1]` (if so, `dp[i] = dp[i-1]`, otherwise `dp[i] = infinity`). Then, we iterate through all available rules. For each rule of length `L`, if it can be applied to the segment `source[i-L...i-1]` to produce `target[i-L...i-1]` (considering wildcards and base cost), we update `dp[i] = min(dp[i], dp[i-L] + current_rule_cost)`. The cost of a rule application is its base cost plus the count of '*' characters in its pattern. If `dp[N]` remains infinity after all computations, it implies the transformation is impossible, and we return -1.

Time Complexity: O(N * M * P_max)
Where N is the length of source/target, M is the number of rules, and P_max is the maximum pattern length.
Space Complexity: O(N)
Where N is the length of source/target, primarily due to the DP array.
"""
from typing import List
import math

class Solution:
    def minCost(self, source: str, target: str, rules: List[List[str]], costs: List[int]) -> int:
        n = len(source)
        
        # dp[i] will store the minimum cost to transform source[0...i-1] to target[0...i-1]
        dp = [math.inf] * (n + 1)
        dp[0] = 0 # Cost to transform empty prefix is 0
        
        for i in range(1, n + 1):
            # Option 1: The current character source[i-1] already matches target[i-1].
            # In this case, no rule is applied for this specific position, and the cost is inherited from dp[i-1].
            if source[i-1] == target[i-1]:
                dp[i] = dp[i-1]
            # If they don't match, and no rule is applied ending at i-1 covering this character,
            # then dp[i] remains math.inf (its initial value for this iteration if not updated by a rule).
            
            # Option 2: Apply a rule that ends at index i-1.
            # This rule would transform source[i-L ... i-1] to target[i-L ... i-1],
            # where L is the length of the pattern/replacement.
            for k in range(len(rules)):
                pattern, replacement = rules[k]
                base_cost = costs[k]
                L = len(pattern)
                
                # Check if the rule can be applied (i.e., there's a valid preceding state dp[i-L])
                # and the length L doesn't exceed the current prefix length.
                if i - L >= 0 and dp[i-L] != math.inf:
                    
                    # Ensure the replacement string exactly matches the target segment
                    if replacement != target[i-L:i]:
                        continue # This rule cannot produce the required target segment
                    
                    current_rule_cost = base_cost
                    wildcard_count = 0
                    possible_match_source = True # Flag to check pattern against source segment
                    
                    # Check if the pattern matches the source segment and count wildcards
                    for j in range(L):
                        s_char = source[i-L+j]
                        p_char = pattern[j]
                        
                        if p_char == '*':
                            wildcard_count += 1
                        elif s_char != p_char:
                            possible_match_source = False
                            break # Mismatch with a non-wildcard character in the pattern
                    
                    if possible_match_source:
                        current_rule_cost += wildcard_count
                        dp[i] = min(dp[i], dp[i-L] + current_rule_cost)
        
        # If dp[n] is still infinity, it means it's impossible to transform the string
        return dp[n] if dp[n] != math.inf else -1

if __name__ == "__main__":
    s = Solution()

    # Example 1
    source1 = "hello"
    target1 = "world"
    rules1 = [["he","wo"],["llo","rld"]]
    costs1 = [3,4]
    assert s.minCost(source1, target1, rules1, costs1) == 7, "Example 1 Failed"

    # Example 2
    source2 = "cat"
    target2 = "dog"
    rules2 = [["c*t","dog"]]
    costs2 = [2]
    assert s.minCost(source2, target2, rules2, costs2) == 3, "Example 2 Failed"

    # Example 3
    source3 = "test"
    target3 = "next"
    rules3 = [["*e*t","next"]]
    costs3 = [4]
    assert s.minCost(source3, target3, rules3, costs3) == 6, "Example 3 Failed"

    # Example 4 (Impossible transformation)
    source4 = "ab"
    target4 = "bc"
    rules4 = [["a*","bd"]]
    costs4 = [9]
    assert s.minCost(source4, target4, rules4, costs4) == -1, "Example 4 Failed"

    # Custom test: all characters match, cost should be 0
    source5 = "abc"
    target5 = "abc"
    rules5 = [["a","x"]] # Rule won't be used if it results in non-target or higher cost
    costs5 = [10]
    assert s.minCost(source5, target5, rules5, costs5) == 0, "Custom Test 5 Failed (all match)"

    # Custom test: multiple rules for same segment, choose minimum
    source6 = "abcdef"
    target6 = "axcdef"
    rules6_actual = [["ab","ax"], ["a*","ax"]] 
    costs6_actual = [5, 2] # "a*" matches "ab", 1 wildcard. Cost: 2 + 1 = 3. "ab" matches "ab". Cost: 5.
    assert s.minCost(source6, target6, rules6_actual, costs6_actual) == 3, "Custom Test 6 Failed (multiple rules, choose min)" 

    # Custom test: longer string, only parts match
    source7 = "banana"
    target7 = "b_nana" # '_' is a literal char in target
    rules7 = [["ba","b_"]]
    costs7 = [1]
    assert s.minCost(source7, target7, rules7, costs7) == 1, "Custom Test 7 Failed"
    
    # Custom test: What if only a small part needs transformation, rest is impossible
    source8 = "apple"
    target8 = "apply"
    rules8 = [["e","y"]]
    costs8 = [1]
    assert s.minCost(source8, target8, rules8, costs8) == 1, "Custom Test 8 Failed"
    
    # Custom test: Rule application for middle segment
    source9 = "abc"
    target9 = "axc"
    rules9 = [["b","x"]]
    costs9 = [1]
    assert s.minCost(source9, target9, rules9, costs9) == 1, "Custom Test 9 Failed"

    # Custom test: Chained rules
    source10 = "apple"
    target10 = "grape"
    rules10 = [["ap","gr"], ["ple","ape"]]
    costs10 = [1, 2]
    assert s.minCost(source10, target10, rules10, costs10) == 3, "Custom Test 10 Failed"

    print("All tests passed!")