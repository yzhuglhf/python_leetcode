"""Daily LeetCode solution generator — fetches real problems from LeetCode API."""
import json
import random
import re
from datetime import date
from pathlib import Path

import google.generativeai as genai
import urllib.request

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

TOPIC_TO_FOLDER = {
    "array": "array",
    "hash-table": "array",
    "string": "string",
    "dynamic-programming": "dp",
    "math": "maths",
    "sorting": "array",
    "greedy": "greedy",
    "depth-first-search": "dfs",
    "binary-search": "binary_search",
    "database": None,
    "breadth-first-search": "bfs",
    "tree": "tree",
    "matrix": "matrix",
    "bit-manipulation": "bit",
    "two-pointers": "two_pointers",
    "prefix-sum": "prefix_sum",
    "heap-priority-queue": "pq",
    "binary-tree": "tree",
    "simulation": "array",
    "graph": "graph",
    "counting": "array",
    "sliding-window": "sliding_windows",
    "design": "design",
    "backtracking": "backtrack",
    "enumeration": "array",
    "union-find": "union_find",
    "linked-list": "linked_list",
    "ordered-set": "design",
    "monotonic-stack": "stack",
    "number-theory": "maths",
    "trie": "trie",
    "divide-and-conquer": "dp",
    "bitmask": "bit",
    "recursion": "backtrack",
    "stack": "stack",
    "queue": "stack",
    "memoization": "dp",
    "segment-tree": "segment_tree",
    "geometry": "maths",
    "topological-sort": "graph",
    "binary-search-tree": "tree",
    "hash-function": "design",
    "shortest-path": "graph",
}


def graphql(query: str, variables: dict) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        LEETCODE_GRAPHQL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fetch_problem_list() -> list[dict]:
    """Return all non-premium Medium/Hard problems via the stable REST endpoint."""
    req = urllib.request.Request(
        "https://leetcode.com/api/problems/all/",
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://leetcode.com"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())

    DIFF = {1: "Easy", 2: "Medium", 3: "Hard"}
    problems = []
    for item in data["stat_status_pairs"]:
        diff = DIFF.get(item["difficulty"]["level"])
        if diff in ("Medium", "Hard") and not item["paid_only"]:
            problems.append({
                "questionFrontendId": str(item["stat"]["frontend_question_id"]),
                "title": item["stat"]["question__title"],
                "titleSlug": item["stat"]["question__title_slug"],
                "difficulty": diff,
            })
    return problems


def fetch_problem_detail(slug: str) -> dict:
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
        content
        topicTags { name slug }
        codeSnippets { langSlug code }
      }
    }
    """
    data = graphql(query, {"titleSlug": slug})
    return data["data"]["question"]


def get_existing_numbers() -> set[str]:
    existing = set()
    for py_file in Path(".").rglob("*.py"):
        if ".github" in py_file.parts:
            continue
        m = re.match(r"^(\d+)[.\s_-]", py_file.name)
        if m:
            existing.add(m.group(1))
        existing.add(py_file.stem)
    return existing


def pick_topic_folder(topic_tags: list[dict]) -> str:
    for tag in topic_tags:
        folder = TOPIC_TO_FOLDER.get(tag["slug"])
        if folder:
            return folder
    return "array"


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_python_snippet(snippets: list[dict]) -> str:
    for s in snippets:
        if s["langSlug"] == "python3":
            return s["code"]
    return "class Solution:\n    pass"


def generate(detail: dict) -> str:
    import os
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash")

    description = strip_html(detail["content"] or "")
    snippet = get_python_snippet(detail.get("codeSnippets") or [])

    prompt = f"""Solve this LeetCode problem in Python.

Problem #{detail['questionId']}: {detail['title']} ({detail['difficulty']})

{description}

Starting code:
{snippet}

Output ONLY a valid .py file — no markdown fences — with this exact structure:

\"\"\"
{detail['title']} (LeetCode #{detail['questionId']})
Difficulty: {detail['difficulty']}

Description:
<concise 2-3 sentence summary>

Example:
<one clear input/output example>

Approach:
<one paragraph explaining the algorithm>

Time Complexity: O(...)
Space Complexity: O(...)
\"\"\"
from typing import List, Optional

<solution code using the provided class/method signature>

if __name__ == "__main__":
    s = Solution()
    assert ...
    assert ...
    assert ...
    print("All tests passed!")
"""
    response = model.generate_content(prompt)
    content = response.text
    m = re.search(r"```python\n(.*?)```", content, re.DOTALL)
    return m.group(1) if m else content


def extract_approach(content: str) -> str:
    m = re.search(r"Approach:\n(.*?)(?:\n\nTime|Time Complexity)", content, re.DOTALL)
    if m:
        return m.group(1).strip().split("\n")[0][:60].rstrip(".,")
    return "optimal solution"


def update_readme(title: str, number: str, difficulty: str, folder: str, filename: str) -> None:
    readme = Path("README.md")
    today = date.today().isoformat()
    row = f"| [{title}]({folder}/{filename}) | #{number} | {difficulty} | {today} |"
    if not readme.exists():
        readme.write_text(
            "# LeetCode Solutions\n\n"
            "| Problem | Number | Difficulty | Date |\n"
            "|---------|--------|------------|------|\n"
            f"{row}\n"
        )
    else:
        readme.write_text(readme.read_text().rstrip() + "\n" + row + "\n")


def main() -> None:
    existing = get_existing_numbers()

    print("Fetching problem list from LeetCode...")
    problems = fetch_problem_list()

    today = date.today()
    preferred = "Medium" if today.day % 2 == 1 else "Hard"

    # Filter unsolved, prefer today's difficulty
    pool = [p for p in problems if p["questionFrontendId"] not in existing
            and p["difficulty"] == preferred]
    if not pool:
        pool = [p for p in problems if p["questionFrontendId"] not in existing]

    if not pool:
        print("All problems solved!")
        return

    chosen = random.choice(pool[:50])  # pick randomly from first 50 unsolved
    print(f"Chosen: #{chosen['questionFrontendId']} {chosen['title']} ({chosen['difficulty']})")

    detail = fetch_problem_detail(chosen["titleSlug"])
    folder = pick_topic_folder(detail["topicTags"])
    content = generate(detail)

    Path(folder).mkdir(exist_ok=True)
    filename = f"{detail['questionId']}. {detail['title']}.py"
    filepath = Path(folder) / filename
    filepath.write_text(content)
    print(f"Written: {filepath}")

    update_readme(detail["title"], detail["questionId"], detail["difficulty"], folder, filename)

    approach = extract_approach(content)
    commit_msg = f"Add {detail['difficulty']}: {detail['title']} - {approach}"
    Path("/tmp/commit_msg.txt").write_text(commit_msg)
    print(f"Commit: {commit_msg}")


if __name__ == "__main__":
    main()
