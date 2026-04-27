"""
Angles of a Triangle
Difficulty: Medium

Description:
Given three positive integer side lengths, this problem asks to determine if they can form a triangle with a positive area. If such a triangle can be formed, its three internal angles (in degrees) must be calculated, sorted in non-decreasing order, and returned as a list of floating-point numbers. Otherwise, an empty list should be returned.

Example:
Input: sides = [3,4,5]
Output: [36.86990,53.13010,90.00000]

Approach:
The algorithm begins by sorting the input `sides` array to ensure `s1 <= s2 <= s3`. It then applies the triangle inequality theorem: if the sum of the two shorter sides is not strictly greater than the longest side (`s1 + s2 <= s3`), a triangle with positive area cannot exist, and an empty list is returned. Otherwise, the Law of Cosines is used to calculate each internal angle. For an angle opposite side `a`, the formula is `cos(Angle) = (b^2 + c^2 - a^2) / (2bc)`. The calculated cosine value is clamped to the range `[-1.0, 1.0]` to prevent potential `ValueError` due to floating-point inaccuracies when passed to `math.acos`. `math.acos` converts the cosine to radians, and `math.degrees` converts radians to degrees. After all three angles are computed, they are collected into a list, sorted in non-decreasing order, and returned.

Time Complexity: O(1)
The input array `sides` has a fixed length of 3. Sorting an array of 3 elements takes constant time. All subsequent calculations involve a fixed number of arithmetic operations and standard library function calls, each taking constant time. Therefore, the overall time complexity is O(1).
Space Complexity: O(1)
A fixed number of variables are used to store the sorted side lengths and the calculated angles. The auxiliary space required does not grow with the input values, making the space complexity O(1).
"""
import math
from typing import List, Optional

class Solution:
    def internalAngles(self, sides: list[int]) -> list[float]:
        # Sort sides to easily apply triangle inequality and for consistent mapping for angle calculation
        # Let a, b, c be the side lengths after sorting
        a, b, c = sorted(sides)

        # 1. Check Triangle Inequality Theorem
        # For a triangle with positive area, the sum of any two sides must be strictly greater than the third side.
        # After sorting a <= b <= c, we only need to check if a + b > c.
        # If a + b <= c, it's either a degenerate triangle (a+b=c, zero area) or impossible (a+b<c).
        if a + b <= c:
            return []

        # Convert sides to float for calculations to maintain precision and avoid integer division issues
        fa, fb, fc = float(a), float(b), float(c)

        # 2. Calculate angles using the Law of Cosines
        # Law of Cosines: side_opposite_angle^2 = side1^2 + side2^2 - 2 * side1 * side2 * cos(Angle)
        # Rearranging for cos(Angle): cos(Angle) = (side1^2 + side2^2 - side_opposite_angle^2) / (2 * side1 * side2)

        # Angle opposite side 'a'
        cos_A = (fb*fb + fc*fc - fa*fa) / (2 * fb * fc)
        # Clamp cos_A to [-1.0, 1.0] to handle potential floating-point inaccuracies
        cos_A = max(-1.0, min(1.0, cos_A))
        angle_A_rad = math.acos(cos_A)

        # Angle opposite side 'b'
        cos_B = (fa*fa + fc*fc - fb*fb) / (2 * fa * fc)
        # Clamp cos_B to [-1.0, 1.0]
        cos_B = max(-1.0, min(1.0, cos_B))
        angle_B_rad = math.acos(cos_B)

        # Angle opposite side 'c'
        cos_C = (fa*fa + fb*fb - fc*fc) / (2 * fa * fb)
        # Clamp cos_C to [-1.0, 1.0]
        cos_C = max(-1.0, min(1.0, cos_C))
        angle_C_rad = math.acos(cos_C)

        # 3. Convert angles from radians to degrees
        angle_A_deg = math.degrees(angle_A_rad)
        angle_B_deg = math.degrees(angle_B_rad)
        angle_C_deg = math.degrees(angle_C_rad)
        
        # 4. Collect, sort, and return the angles
        angles = [angle_A_deg, angle_B_deg, angle_C_deg]
        angles.sort()
        
        return angles

if __name__ == "__main__":
    s = Solution()

    # Helper for float comparison with tolerance
    def assert_floats_almost_equal(actual, expected, tolerance=1e-5, msg=""):
        assert len(actual) == len(expected), f"Length mismatch: {msg} Got {len(actual)}, Expected {len(expected)}"
        for i in range(len(actual)):
            assert abs(actual[i] - expected[i]) < tolerance, \
                   f"{msg} Angle {i} mismatch: Got {actual[i]:.7f}, Expected {expected[i]:.7f}"
        
    # Example 1: Right-angled triangle (3-4-5)
    result1 = s.internalAngles([3, 4, 5])
    expected1 = [36.86989764584401, 53.13010235415599, 90.0]
    assert_floats_almost_equal(result1, expected1, msg="Test 1 ([3,4,5])")
    print(f"Test 1 passed: Input: [3,4,5], Output: {result1}")

    # Example 2: Invalid triangle (2-4-2)
    result2 = s.internalAngles([2, 4, 2])
    expected2 = []
    assert result2 == expected2, f"Test 2 ([2,4,2]) failed: Got {result2}, Expected {expected2}"
    print(f"Test 2 passed: Input: [2,4,2], Output: {result2}")

    # Example 3: Equilateral triangle (5-5-5)
    result3 = s.internalAngles([5, 5, 5])
    expected3 = [60.0, 60.0, 60.0]
    assert_floats_almost_equal(result3, expected3, msg="Test 3 ([5,5,5])")
    print(f"Test 3 passed: Input: [5,5,5], Output: {result3}")

    # Example 4: Obtuse triangle (3-4-6)
    # Calculated values for (3,4,6)
    # cos(A) = (4^2+6^2-3^2)/(2*4*6) = 43/48
    # cos(B) = (3^2+6^2-4^2)/(2*3*6) = 29/36
    # cos(C) = (3^2+4^2-6^2)/(2*3*4) = -11/24
    expected4 = sorted([math.degrees(math.acos(43/48)), 
                        math.degrees(math.acos(29/36)), 
                        math.degrees(math.acos(-11/24))])
    result4 = s.internalAngles([3, 4, 6])
    assert_floats_almost_equal(result4, expected4, msg="Test 4 ([3,4,6])")
    print(f"Test 4 passed: Input: [3,4,6], Output: {result4}")

    # Example 5: Degenerate triangle (sum equals longest side, 1-2-3)
    result5 = s.internalAngles([1, 2, 3])
    expected5 = []
    assert result5 == expected5, f"Test 5 ([1,2,3]) failed: Got {result5}, Expected {expected5}"
    print(f"Test 5 passed: Input: [1,2,3], Output: {result5}")

    # Example 6: Impossible triangle (sum less than longest side, 1-10-2)
    result6 = s.internalAngles([1, 10, 2])
    expected6 = []
    assert result6 == expected6, f"Test 6 ([1,10,2]) failed: Got {result6}, Expected {expected6}"
    print(f"Test 6 passed: Input: [1,10,2], Output: {result6}")

    # Example 7: Large sides
    result7 = s.internalAngles([1000, 999, 100])
    # For a=100, b=999, c=1000
    expected7 = sorted([
        math.degrees(math.acos((999**2 + 1000**2 - 100**2) / (2 * 999 * 1000))),
        math.degrees(math.acos((100**2 + 1000**2 - 999**2) / (2 * 100 * 1000))),
        math.degrees(math.acos((100**2 + 999**2 - 1000**2) / (2 * 100 * 999)))
    ])
    result7 = s.internalAngles([1000, 999, 100])
    assert_floats_almost_equal(result7, expected7, msg="Test 7 ([1000,999,100])")
    print(f"Test 7 passed: Input: [1000,999,100], Output: {result7}")

    print("\nAll tests passed!")