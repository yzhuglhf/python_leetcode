"""Daily LeetCode solution generator — runs inside GitHub Actions."""
import re
from datetime import date
from pathlib import Path

import anthropic

# (number, title, snake_case, topic_folder, difficulty)
PROBLEMS = [
    # Array
    ("53",  "Maximum Subarray",                          "maximum_subarray",                          "array",          "Medium"),
    ("54",  "Spiral Matrix",                             "spiral_matrix",                             "array",          "Medium"),
    ("128", "Longest Consecutive Sequence",              "longest_consecutive_sequence",              "array",          "Medium"),
    ("169", "Majority Element",                          "majority_element",                          "array",          "Easy"),
    ("274", "H-Index",                                   "h_index",                                   "array",          "Medium"),
    ("380", "Insert Delete GetRandom O(1)",               "insert_delete_getrandom",                   "array",          "Medium"),
    ("238", "Product of Array Except Self",              "product_of_array_except_self",              "prefix_sum",     "Medium"),
    # Two Pointers
    ("15",  "3Sum",                                      "three_sum",                                 "two_pointers",   "Medium"),
    ("11",  "Container With Most Water",                 "container_with_most_water",                 "two_pointers",   "Medium"),
    # Sliding Window
    ("3",   "Longest Substring Without Repeating Characters", "longest_substring_without_repeating_characters", "sliding_windows", "Medium"),
    # Binary Search
    ("33",  "Search in Rotated Sorted Array",            "search_in_rotated_sorted_array",            "binary_search",  "Medium"),
    ("153", "Find Minimum in Rotated Sorted Array",      "find_minimum_in_rotated_sorted_array",      "binary_search",  "Medium"),
    ("4",   "Median of Two Sorted Arrays",               "median_of_two_sorted_arrays",               "binary_search",  "Hard"),
    # Backtracking
    ("17",  "Letter Combinations of a Phone Number",     "letter_combinations_of_a_phone_number",     "backtrack",      "Medium"),
    ("22",  "Generate Parentheses",                      "generate_parentheses",                      "backtrack",      "Medium"),
    ("39",  "Combination Sum",                           "combination_sum",                           "backtrack",      "Medium"),
    ("46",  "Permutations",                              "permutations",                              "backtrack",      "Medium"),
    ("79",  "Word Search",                               "word_search",                               "backtrack",      "Medium"),
    ("131", "Palindrome Partitioning",                   "palindrome_partitioning",                   "backtrack",      "Medium"),
    ("212", "Word Search II",                            "word_search_ii",                            "backtrack",      "Hard"),
    ("51",  "N-Queens",                                  "n_queens",                                  "backtrack",      "Hard"),
    # DP
    ("5",   "Longest Palindromic Substring",             "longest_palindromic_substring",             "dp",             "Medium"),
    ("55",  "Jump Game",                                 "jump_game",                                 "dp",             "Medium"),
    ("62",  "Unique Paths",                              "unique_paths",                              "dp",             "Medium"),
    ("91",  "Decode Ways",                               "decode_ways",                               "dp",             "Medium"),
    ("139", "Word Break",                                "word_break",                                "dp",             "Medium"),
    ("152", "Maximum Product Subarray",                  "maximum_product_subarray",                  "dp",             "Medium"),
    ("300", "Longest Increasing Subsequence",            "longest_increasing_subsequence",            "dp",             "Medium"),
    ("322", "Coin Change",                               "coin_change",                               "dp",             "Medium"),
    ("416", "Partition Equal Subset Sum",                "partition_equal_subset_sum",                "dp",             "Medium"),
    ("72",  "Edit Distance",                             "edit_distance",                             "dp",             "Medium"),
    ("10",  "Regular Expression Matching",               "regular_expression_matching",               "dp",             "Hard"),
    ("45",  "Jump Game II",                              "jump_game_ii",                              "dp",             "Medium"),
    # Graph / BFS / DFS
    ("200", "Number of Islands",                         "number_of_islands",                         "dfs",            "Medium"),
    ("207", "Course Schedule",                           "course_schedule",                           "graph",          "Medium"),
    ("127", "Word Ladder",                               "word_ladder",                               "bfs",            "Hard"),
    # Tree
    ("98",  "Validate Binary Search Tree",               "validate_binary_search_tree",               "tree",           "Medium"),
    ("102", "Binary Tree Level Order Traversal",         "binary_tree_level_order_traversal",         "tree",           "Medium"),
    ("124", "Binary Tree Maximum Path Sum",              "binary_tree_maximum_path_sum",              "tree",           "Hard"),
    ("297", "Serialize and Deserialize Binary Tree",     "serialize_and_deserialize_binary_tree",     "tree",           "Hard"),
    # Design
    ("146", "LRU Cache",                                 "lru_cache",                                 "design",         "Medium"),
    ("295", "Find Median from Data Stream",              "find_median_from_data_stream",              "design",         "Hard"),
    # Stack
    ("84",  "Largest Rectangle in Histogram",            "largest_rectangle_in_histogram",            "stack",          "Hard"),
    ("32",  "Longest Valid Parentheses",                 "longest_valid_parentheses",                 "stack",          "Hard"),
    # Priority Queue
    ("23",  "Merge k Sorted Lists",                      "merge_k_sorted_lists",                      "pq",             "Hard"),
    ("215", "Kth Largest Element in an Array",           "kth_largest_element_in_an_array",           "pq",             "Medium"),
    ("347", "Top K Frequent Elements",                   "top_k_frequent_elements",                   "pq",             "Medium"),
    ("239", "Sliding Window Maximum",                    "sliding_window_maximum",                    "pq",             "Hard"),
    # Two Pointers / Greedy
    ("56",  "Merge Intervals",                           "merge_intervals",                           "greedy",         "Medium"),
    ("435", "Non-overlapping Intervals",                 "non_overlapping_intervals",                 "greedy",         "Medium"),
    ("621", "Task Scheduler",                            "task_scheduler",                            "greedy",         "Medium"),
    # Misc Hard
    ("42",  "Trapping Rain Water",                       "trapping_rain_water",                       "two_pointers",   "Hard"),
    ("41",  "First Missing Positive",                    "first_missing_positive",                    "array",          "Hard"),
    ("76",  "Minimum Window Substring",                  "minimum_window_substring",                  "sliding_windows","Hard"),
]


def get_existing_numbers() -> set[str]:
    """Collect all LeetCode problem numbers already in the repo."""
    existing = set()
    for py_file in Path(".").rglob("*.py"):
        if ".github" in py_file.parts:
            continue
        # Match filenames like "123. Title.py" or "123_title.py"
        m = re.match(r"^(\d+)[.\s_-]", py_file.name)
        if m:
            existing.add(m.group(1))
        # Also match plain snake_case names (our own additions)
        existing.add(py_file.stem)
    return existing


def pick_problem(existing: set[str]) -> tuple:
    today = date.today()
    # Alternate Medium / Hard by day parity
    preferred = "Medium" if today.day % 2 == 1 else "Hard"
    fallback  = "Hard"   if preferred == "Medium" else "Medium"

    for difficulty in (preferred, fallback):
        for number, title, snake, topic, diff in PROBLEMS:
            if diff == difficulty and number not in existing and snake not in existing:
                return number, title, snake, topic, difficulty
    raise RuntimeError("All problems already solved!")


def generate(number: str, title: str, difficulty: str, topic: str) -> str:
    client = anthropic.Anthropic()
    prompt = f"""Write a complete Python LeetCode solution for:
Problem #{number}: {title} (Difficulty: {difficulty}, Topic: {topic})

Output ONLY a valid .py file — no markdown fences — with this exact structure:

\"\"\"
{title} (LeetCode #{number})
Difficulty: {difficulty}

Description:
<concise problem description>

Example:
<one clear input/output example>

Approach:
<one paragraph explaining the algorithm and why it works>

Time Complexity: O(...)
Space Complexity: O(...)
\"\"\"
from typing import List, Optional


class Solution:
    def methodName(self, ...) -> ...:
        ...


if __name__ == "__main__":
    s = Solution()
    assert s.methodName(...) == ...
    assert s.methodName(...) == ...
    assert s.methodName(...) == ...
    print("All tests passed!")
"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text
    # Strip markdown fences if the model adds them anyway
    m = re.search(r"```python\n(.*?)```", content, re.DOTALL)
    return m.group(1) if m else content


def extract_approach(content: str) -> str:
    m = re.search(r"Approach:\n(.*?)(?:\n\nTime|Time Complexity)", content, re.DOTALL)
    if m:
        first_line = m.group(1).strip().split("\n")[0]
        return first_line[:60].rstrip(".,")
    return "optimal solution"


def update_readme(title: str, number: str, difficulty: str, topic: str, filename: str) -> None:
    readme = Path("README.md")
    today = date.today().isoformat()
    row = f"| [{title}]({topic}/{filename}) | #{number} | {difficulty} | {today} |"
    if not readme.exists():
        readme.write_text(
            "# LeetCode Solutions\n\n"
            "| Problem | Number | Difficulty | Date |\n"
            "|---------|--------|------------|------|\n"
            f"{row}\n"
        )
    else:
        text = readme.read_text().rstrip()
        readme.write_text(text + "\n" + row + "\n")


def main() -> None:
    existing = get_existing_numbers()
    number, title, snake, topic, difficulty = pick_problem(existing)
    print(f"Generating: {difficulty} #{number} {title} → {topic}/")

    content = generate(number, title, difficulty, topic)

    Path(topic).mkdir(exist_ok=True)
    filename = f"{number}. {title}.py"
    filepath = Path(topic) / filename
    filepath.write_text(content)
    print(f"Written: {filepath}")

    update_readme(title, number, difficulty, topic, filename)

    approach = extract_approach(content)
    commit_msg = f"Add {difficulty}: {title} - {approach}"
    Path("/tmp/commit_msg.txt").write_text(commit_msg)
    print(f"Commit: {commit_msg}")


if __name__ == "__main__":
    main()
