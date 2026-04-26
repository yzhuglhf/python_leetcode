"""Daily LeetCode solution generator — runs inside GitHub Actions."""
import os
import re
from datetime import date
from pathlib import Path

import anthropic

MEDIUM = [
    ("1", "Two Sum", "two_sum"),
    ("3", "Longest Substring Without Repeating Characters", "longest_substring_without_repeating_characters"),
    ("5", "Longest Palindromic Substring", "longest_palindromic_substring"),
    ("11", "Container With Most Water", "container_with_most_water"),
    ("15", "3Sum", "three_sum"),
    ("17", "Letter Combinations of a Phone Number", "letter_combinations_of_a_phone_number"),
    ("22", "Generate Parentheses", "generate_parentheses"),
    ("33", "Search in Rotated Sorted Array", "search_in_rotated_sorted_array"),
    ("39", "Combination Sum", "combination_sum"),
    ("46", "Permutations", "permutations"),
    ("48", "Rotate Image", "rotate_image"),
    ("49", "Group Anagrams", "group_anagrams"),
    ("53", "Maximum Subarray", "maximum_subarray"),
    ("54", "Spiral Matrix", "spiral_matrix"),
    ("55", "Jump Game", "jump_game"),
    ("56", "Merge Intervals", "merge_intervals"),
    ("62", "Unique Paths", "unique_paths"),
    ("73", "Set Matrix Zeroes", "set_matrix_zeroes"),
    ("79", "Word Search", "word_search"),
    ("91", "Decode Ways", "decode_ways"),
    ("98", "Validate Binary Search Tree", "validate_binary_search_tree"),
    ("102", "Binary Tree Level Order Traversal", "binary_tree_level_order_traversal"),
    ("128", "Longest Consecutive Sequence", "longest_consecutive_sequence"),
    ("131", "Palindrome Partitioning", "palindrome_partitioning"),
    ("139", "Word Break", "word_break"),
    ("152", "Maximum Product Subarray", "maximum_product_subarray"),
    ("153", "Find Minimum in Rotated Sorted Array", "find_minimum_in_rotated_sorted_array"),
    ("200", "Number of Islands", "number_of_islands"),
    ("207", "Course Schedule", "course_schedule"),
    ("215", "Kth Largest Element in an Array", "kth_largest_element_in_an_array"),
    ("238", "Product of Array Except Self", "product_of_array_except_self"),
    ("300", "Longest Increasing Subsequence", "longest_increasing_subsequence"),
    ("322", "Coin Change", "coin_change"),
    ("347", "Top K Frequent Elements", "top_k_frequent_elements"),
    ("416", "Partition Equal Subset Sum", "partition_equal_subset_sum"),
    ("435", "Non-overlapping Intervals", "non_overlapping_intervals"),
    ("438", "Find All Anagrams in a String", "find_all_anagrams_in_a_string"),
    ("621", "Task Scheduler", "task_scheduler"),
]

HARD = [
    ("4", "Median of Two Sorted Arrays", "median_of_two_sorted_arrays"),
    ("10", "Regular Expression Matching", "regular_expression_matching"),
    ("23", "Merge k Sorted Lists", "merge_k_sorted_lists"),
    ("25", "Reverse Nodes in k-Group", "reverse_nodes_in_k_group"),
    ("32", "Longest Valid Parentheses", "longest_valid_parentheses"),
    ("41", "First Missing Positive", "first_missing_positive"),
    ("42", "Trapping Rain Water", "trapping_rain_water"),
    ("45", "Jump Game II", "jump_game_ii"),
    ("51", "N-Queens", "n_queens"),
    ("72", "Edit Distance", "edit_distance"),
    ("76", "Minimum Window Substring", "minimum_window_substring"),
    ("84", "Largest Rectangle in Histogram", "largest_rectangle_in_histogram"),
    ("85", "Maximal Rectangle", "maximal_rectangle"),
    ("124", "Binary Tree Maximum Path Sum", "binary_tree_maximum_path_sum"),
    ("127", "Word Ladder", "word_ladder"),
    ("146", "LRU Cache", "lru_cache"),
    ("212", "Word Search II", "word_search_ii"),
    ("239", "Sliding Window Maximum", "sliding_window_maximum"),
    ("295", "Find Median from Data Stream", "find_median_from_data_stream"),
    ("297", "Serialize and Deserialize Binary Tree", "serialize_and_deserialize_binary_tree"),
    ("312", "Burst Balloons", "burst_balloons"),
    ("315", "Count of Smaller Numbers After Self", "count_of_smaller_numbers_after_self"),
    ("329", "Longest Increasing Path in a Matrix", "longest_increasing_path_in_a_matrix"),
    ("480", "Sliding Window Median", "sliding_window_median"),
]


def get_existing() -> set[str]:
    existing = set()
    for folder in ["medium", "hard"]:
        p = Path(folder)
        if p.exists():
            for f in p.glob("*.py"):
                existing.add(f.stem)
    return existing


def pick_problem(existing: set[str]) -> tuple[str, str, str, str]:
    today = date.today()
    if today.day % 2 == 1:
        pool, difficulty, folder = MEDIUM, "Medium", "medium"
    else:
        pool, difficulty, folder = HARD, "Hard", "hard"

    for number, title, snake in pool:
        if snake not in existing:
            return number, title, snake, difficulty, folder

    # Fall back to the other difficulty if all solved
    other_pool = HARD if difficulty == "Medium" else MEDIUM
    other_folder = "hard" if folder == "medium" else "medium"
    other_diff = "Hard" if difficulty == "Medium" else "Medium"
    for number, title, snake in other_pool:
        if snake not in existing:
            return number, title, snake, other_diff, other_folder

    raise RuntimeError("All problems already solved!")


def generate(number: str, title: str, difficulty: str) -> str:
    client = anthropic.Anthropic()
    prompt = f"""Write a complete Python LeetCode solution for:
Problem #{number}: {title} (Difficulty: {difficulty})

Output ONLY a valid .py file with this exact structure (no markdown fences):

\"\"\"
{title} (LeetCode #{number})
Difficulty: {difficulty}

Description:
<concise problem description>

Example:
<one clear example>

Approach:
<one-paragraph explanation of the algorithm>

Time Complexity: O(...)
Space Complexity: O(...)
\"\"\"
from typing import List, Optional


class Solution:
    def solve(self, ...) -> ...:
        ...


if __name__ == "__main__":
    s = Solution()
    assert s.solve(...) == ...
    assert s.solve(...) == ...
    assert s.solve(...) == ...
    print("All tests passed!")
"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text
    # Strip markdown fences if model adds them anyway
    match = re.search(r"```python\n(.*?)```", content, re.DOTALL)
    return match.group(1) if match else content


def update_readme(title: str, number: str, difficulty: str, folder: str, snake: str) -> None:
    readme = Path("README.md")
    today = date.today().isoformat()
    row = f"| [{title}]({folder}/{snake}.py) | #{number} | {difficulty} | {today} |"
    if not readme.exists():
        readme.write_text(
            "# LeetCode Solutions\n\n"
            "| Problem | Number | Difficulty | Date |\n"
            "|---------|--------|------------|------|\n"
            f"{row}\n"
        )
    else:
        readme.write_text(readme.read_text().rstrip() + "\n" + row + "\n")


def extract_approach(content: str) -> str:
    match = re.search(r"Approach:\n(.*?)(?:\n\nTime|Time Complexity)", content, re.DOTALL)
    if match:
        first_line = match.group(1).strip().split("\n")[0]
        return first_line[:60].rstrip(".,")
    return "optimal solution"


def main() -> None:
    existing = get_existing()
    number, title, snake, difficulty, folder = pick_problem(existing)
    print(f"Generating: {difficulty} #{number} {title}")

    content = generate(number, title, difficulty)

    Path(folder).mkdir(exist_ok=True)
    filepath = Path(folder) / f"{snake}.py"
    filepath.write_text(content)
    print(f"Written: {filepath}")

    update_readme(title, number, difficulty, folder, snake)

    approach = extract_approach(content)
    commit_msg = f"Add {difficulty}: {title} - {approach}"
    Path("/tmp/commit_msg.txt").write_text(commit_msg)
    print(f"Commit message: {commit_msg}")


if __name__ == "__main__":
    main()
