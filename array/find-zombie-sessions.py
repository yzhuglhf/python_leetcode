"""
Find Zombie Sessions
Difficulty: Hard

Description:
This solution identifies "zombie sessions" from a table of app events. A session qualifies as a zombie session if its duration exceeds 30 minutes, it contains at least 5 scroll events, its click-to-scroll ratio is less than 0.20, and no purchases were made during the session. The result lists these sessions, including their user ID, duration in minutes, and scroll count, sorted by scroll count in descending order, then by session ID in ascending order.

Example:
Input:
app_events table:
+----------+---------+---------------------+------------+------------+-------------+
| event_id | user_id | event_timestamp     | event_type | session_id | event_value |
+----------+---------+---------------------+------------+------------+-------------+
| 1        | 201     | 2024-03-01 10:00:00 | app_open   | S001       | NULL        |
| 2        | 201     | 2024-03-01 10:05:00 | scroll     | S001       | 500         |
| ... (other events) ...
| 8        | 201     | 2024-03-01 10:35:00 | app_close  | S001       | NULL        |
+----------+---------+---------------------+------------+------------+-------------+
Output:
+------------+---------+--------------------------+--------------+
| session_id | user_id | session_duration_minutes | scroll_count |
+------------+---------+--------------------------+--------------+
| S001       | 201     | 35                       | 6            |
+------------+---------+--------------------------+--------------+

Approach:
The solution leverages the Pandas library to efficiently process the tabular `app_events` data. It begins by converting the `event_timestamp` column to datetime objects. Next, it groups the DataFrame by `session_id` and performs several aggregations: extracting the `user_id`, finding the `min` and `max` `event_timestamp` for duration calculation, counting 'scroll' and 'click' events, and determining if any 'purchase' event occurred within the session. Derived metrics, `session_duration_minutes` and `click_to_scroll_ratio`, are then calculated. The sessions are subsequently filtered based on the four specified zombie session criteria. Finally, the required columns are selected, `session_duration_minutes` is cast to an integer, and the results are sorted first by `scroll_count` in descending order, then by `session_id` in ascending order, before being returned as a list of lists.

Time Complexity: O(N)
The dominant operations are `pd.to_datetime` (O(N)), `groupby().agg()` (O(N)), and sorting (O(K log K) where K is number of unique sessions, K <= N). Therefore, the overall time complexity is O(N + K log K), which simplifies to O(N) since K is at most N.

Space Complexity: O(N)
The solution requires storing the input DataFrame (O(N)), and intermediate grouped data (O(K), where K is the number of unique sessions). Thus, the space complexity is O(N).
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional

class Solution:
    def findZombieSessions(self, app_events: pd.DataFrame) -> List[List[str]]:
        # Ensure event_timestamp is in datetime format
        app_events['event_timestamp'] = pd.to_datetime(app_events['event_timestamp'])

        # Group by session_id and aggregate required metrics
        session_stats = app_events.groupby('session_id').agg(
            user_id=('user_id', 'first'),  # user_id is constant per session, pick the first one
            min_timestamp=('event_timestamp', 'min'),
            max_timestamp=('event_timestamp', 'max'),
            scroll_count=('event_type', lambda x: (x == 'scroll').sum()),
            click_count=('event_type', lambda x: (x == 'click').sum()),
            has_purchase=('event_type', lambda x: (x == 'purchase').any())
        ).reset_index()

        # Calculate session duration in minutes
        session_stats['session_duration_minutes'] = (session_stats['max_timestamp'] - session_stats['min_timestamp']).dt.total_seconds() / 60

        # Calculate click-to-scroll ratio
        # If scroll_count is 0, the ratio is effectively infinite, which will not satisfy '< 0.20'.
        # This also correctly handles sessions that fail the 'scroll_count >= 5' condition.
        session_stats['click_to_scroll_ratio'] = session_stats.apply(
            lambda row: row['click_count'] / row['scroll_count'] if row['scroll_count'] > 0 else float('inf'),
            axis=1
        )

        # Filter for zombie sessions based on ALL criteria
        zombie_sessions_df = session_stats[
            (session_stats['session_duration_minutes'] > 30) &
            (session_stats['scroll_count'] >= 5) &
            (session_stats['click_to_scroll_ratio'] < 0.20) &
            (~session_stats['has_purchase'])
        ]

        # Select and format the required columns
        result_df = zombie_sessions_df[['session_id', 'user_id', 'session_duration_minutes', 'scroll_count']]

        # Convert session_duration_minutes to integer as per example
        result_df['session_duration_minutes'] = result_df['session_duration_minutes'].astype(int)

        # Sort the result as required: scroll_count descending, then session_id ascending
        result_df = result_df.sort_values(by=['scroll_count', 'session_id'], ascending=[False, True])

        # Convert to list of lists for the final output
        return result_df.values.tolist()


if __name__ == "__main__":
    s = Solution()

    # Test Case 1: Provided in the problem description
    app_events_data_1 = [
        {'event_id': 1, 'user_id': 201, 'event_timestamp': '2024-03-01 10:00:00', 'event_type': 'app_open', 'session_id': 'S001', 'event_value': None},
        {'event_id': 2, 'user_id': 201, 'event_timestamp': '2024-03-01 10:05:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 500},
        {'event_id': 3, 'user_id': 201, 'event_timestamp': '2024-03-01 10:10:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 750},
        {'event_id': 4, 'user_id': 201, 'event_timestamp': '2024-03-01 10:15:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 600},
        {'event_id': 5, 'user_id': 201, 'event_timestamp': '2024-03-01 10:20:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 800},
        {'event_id': 6, 'user_id': 201, 'event_timestamp': '2024-03-01 10:25:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 550},
        {'event_id': 7, 'user_id': 201, 'event_timestamp': '2024-03-01 10:30:00', 'event_type': 'scroll', 'session_id': 'S001', 'event_value': 900},
        {'event_id': 8, 'user_id': 201, 'event_timestamp': '2024-03-01 10:35:00', 'event_type': 'app_close', 'session_id': 'S001', 'event_value': None},
        {'event_id': 9, 'user_id': 202, 'event_timestamp': '2024-03-01 11:00:00', 'event_type': 'app_open', 'session_id': 'S002', 'event_value': None},
        {'event_id': 10, 'user_id': 202, 'event_timestamp': '2024-03-01 11:02:00', 'event_type': 'click', 'session_id': 'S002', 'event_value': None},
        {'event_id': 11, 'user_id': 202, 'event_timestamp': '2024-03-01 11:05:00', 'event_type': 'scroll', 'session_id': 'S002', 'event_value': 400},
        {'event_id': 12, 'user_id': 202, 'event_timestamp': '2024-03-01 11:08:00', 'event_type': 'click', 'session_id': 'S002', 'event_value': None},
        {'event_id': 13, 'user_id': 202, 'event_timestamp': '2024-03-01 11:10:00', 'event_type': 'scroll', 'session_id': 'S002', 'event_value': 350},
        {'event_id': 14, 'user_id': 202, 'event_timestamp': '2024-03-01 11:15:00', 'event_type': 'purchase', 'session_id': 'S002', 'event_value': 50},
        {'event_id': 15, 'user_id': 202, 'event_timestamp': '2024-03-01 11:20:00', 'event_type': 'app_close', 'session_id': 'S002', 'event_value': None},
        {'event_id': 16, 'user_id': 203, 'event_timestamp': '2024-03-01 12:00:00', 'event_type': 'app_open', 'session_id': 'S003', 'event_value': None},
        {'event_id': 17, 'user_id': 203, 'event_timestamp': '2024-03-01 12:10:00', 'event_type': 'scroll', 'session_id': 'S003', 'event_value': 1000},
        {'event_id': 18, 'user_id': 203, 'event_timestamp': '2024-03-01 12:20:00', 'event_type': 'scroll', 'session_id': 'S003', 'event_value': 1200},
        {'event_id': 19, 'user_id': 203, 'event_timestamp': '2024-03-01 12:25:00', 'event_type': 'click', 'session_id': 'S003', 'event_value': None},
        {'event_id': 20, 'user_id': 203, 'event_timestamp': '2024-03-01 12:30:00', 'event_type': 'scroll', 'session_id': 'S003', 'event_value': 800},
        {'event_id': 21, 'user_id': 203, 'event_timestamp': '2024-03-01 12:40:00', 'event_type': 'scroll', 'session_id': 'S003', 'event_value': 900},
        {'event_id': 22, 'user_id': 203, 'event_timestamp': '2024-03-01 12:50:00', 'event_type': 'scroll', 'session_id': 'S003', 'event_value': 1100},
        {'event_id': 23, 'user_id': 203, 'event_timestamp': '2024-03-01 13:00:00', 'event_type': 'app_close', 'session_id': 'S003', 'event_value': None},
        {'event_id': 24, 'user_id': 204, 'event_timestamp': '2024-03-01 14:00:00', 'event_type': 'app_open', 'session_id': 'S004', 'event_value': None},
        {'event_id': 25, 'user_id': 204, 'event_timestamp': '2024-03-01 14:05:00', 'event_type': 'scroll', 'session_id': 'S004', 'event_value': 600},
        {'event_id': 26, 'user_id': 204, 'event_timestamp': '2024-03-01 14:08:00', 'event_type': 'scroll', 'session_id': 'S004', 'event_value': 700},
        {'event_id': 27, 'user_id': 204, 'event_timestamp': '2024-03-01 14:10:00', 'event_type': 'click', 'session_id': 'S004', 'event_value': None},
        {'event_id': 28, 'user_id': 204, 'event_timestamp': '2024-03-01 14:12:00', 'event_type': 'app_close', 'session_id': 'S004', 'event_value': None}
    ]
    app_events_df_1 = pd.DataFrame(app_events_data_1)
    expected_1 = [['S001', 201, 35, 6]]
    result_1 = s.findZombieSessions(app_events_df_1.copy())
    assert result_1 == expected_1, f"Test Case 1 Failed: Expected {expected_1}, Got {result_1}"
    print(f"Test Case 1 Passed: {result_1}")

    # Test Case 2: No zombie sessions (due to purchase and short duration)
    app_events_data_2 = [
        {'event_id': 1, 'user_id': 101, 'event_timestamp': '2024-03-01 10:00:00', 'event_type': 'app_open', 'session_id': 'S005', 'event_value': None},
        {'event_id': 2, 'user_id': 101, 'event_timestamp': '2024-03-01 10:10:00', 'event_type': 'scroll', 'session_id': 'S005', 'event_value': 100},
        {'event_id': 3, 'user_id': 101, 'event_timestamp': '2024-03-01 10:20:00', 'event_type': 'scroll', 'session_id': 'S005', 'event_value': 100},
        {'event_id': 4, 'user_id': 101, 'event_timestamp': '2024-03-01 10:30:00', 'event_type': 'purchase', 'session_id': 'S005', 'event_value': 20}, # Has purchase
        {'event_id': 5, 'user_id': 101, 'event_timestamp': '2024-03-01 11:00:00', 'event_type': 'app_close', 'session_id': 'S005', 'event_value': None},
    ]
    app_events_df_2 = pd.DataFrame(app_events_data_2)
    expected_2 = []
    result_2 = s.findZombieSessions(app_events_df_2.copy())
    assert result_2 == expected_2, f"Test Case 2 Failed: Expected {expected_2}, Got {result_2}"
    print(f"Test Case 2 Passed: {result_2}")

    # Test Case 3: Multiple zombie sessions, check sorting (scroll_count DESC, session_id ASC)
    app_events_data_3 = [
        # S101: 40 min duration, 7 scrolls, 0 clicks -> ratio 0.0. Zombie
        {'event_id': 1, 'user_id': 100, 'event_timestamp': '2024-03-01 10:00:00', 'event_type': 'app_open', 'session_id': 'S101', 'event_value': None},
        {'event_id': 2, 'user_id': 100, 'event_timestamp': '2024-03-01 10:05:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 3, 'user_id': 100, 'event_timestamp': '2024-03-01 10:10:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 4, 'user_id': 100, 'event_timestamp': '2024-03-01 10:15:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 5, 'user_id': 100, 'event_timestamp': '2024-03-01 10:20:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 6, 'user_id': 100, 'event_timestamp': '2024-03-01 10:25:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 7, 'user_id': 100, 'event_timestamp': '2024-03-01 10:30:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1},
        {'event_id': 8, 'user_id': 100, 'event_timestamp': '2024-03-01 10:35:00', 'event_type': 'scroll', 'session_id': 'S101', 'event_value': 1}, # 7 scrolls
        {'event_id': 9, 'user_id': 100, 'event_timestamp': '2024-03-01 10:40:00', 'event_type': 'app_close', 'session_id': 'S101', 'event_value': None}, # 40 min duration
        # S102: 50 min duration, 6 scrolls, 1 click -> ratio 1/6 ~ 0.166. Zombie
        {'event_id': 10, 'user_id': 102, 'event_timestamp': '2024-03-01 11:00:00', 'event_type': 'app_open', 'session_id': 'S102', 'event_value': None},
        {'event_id': 11, 'user_id': 102, 'event_timestamp': '2024-03-01 11:05:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1},
        {'event_id': 12, 'user_id': 102, 'event_timestamp': '2024-03-01 11:10:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1},
        {'event_id': 13, 'user_id': 102, 'event_timestamp': '2024-03-01 11:15:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1},
        {'event_id': 14, 'user_id': 102, 'event_timestamp': '2024-03-01 11:20:00', 'event_type': 'click', 'session_id': 'S102', 'event_value': None}, # 1 click
        {'event_id': 15, 'user_id': 102, 'event_timestamp': '2024-03-01 11:25:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1},
        {'event_id': 16, 'user_id': 102, 'event_timestamp': '2024-03-01 11:30:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1},
        {'event_id': 17, 'user_id': 102, 'event_timestamp': '2024-03-01 11:35:00', 'event_type': 'scroll', 'session_id': 'S102', 'event_value': 1}, # 6 scrolls
        {'event_id': 18, 'user_id': 102, 'event_timestamp': '2024-03-01 11:50:00', 'event_type': 'app_close', 'session_id': 'S102', 'event_value': None}, # 50 min duration
        # S103: 35 min duration, 5 scrolls, 0 clicks -> ratio 0.0. Zombie
        {'event_id': 19, 'user_id': 103, 'event_timestamp': '2024-03-01 12:00:00', 'event_type': 'app_open', 'session_id': 'S103', 'event_value': None},
        {'event_id': 20, 'user_id': 103, 'event_timestamp': '2024-03-01 12:05:00', 'event_type': 'scroll', 'session_id': 'S103', 'event_value': 1},
        {'event_id': 21, 'user_id': 103, 'event_timestamp': '2024-03-01 12:10:00', 'event_type': 'scroll', 'session_id': 'S103', 'event_value': 1},
        {'event_id': 22, 'user_id': 103, 'event_timestamp': '2024-03-01 12:15:00', 'event_type': 'scroll', 'session_id': 'S103', 'event_value': 1},
        {'event_id': 23, 'user_id': 103, 'event_timestamp': '2024-03-01 12:20:00', 'event_type': 'scroll', 'session_id': 'S103', 'event_value': 1},
        {'event_id': 24, 'user_id': 103, 'event_timestamp': '2024-03-01 12:25:00', 'event_type': 'scroll', 'session_id': 'S103', 'event_value': 1}, # 5 scrolls
        {'event_id': 25, 'user_id': 103, 'event_timestamp': '2024-03-01 12:35:00', 'event_type': 'app_close', 'session_id': 'S103', 'event_value': None}, # 35 min duration
        # S104: 31 min duration, 5 scrolls, 1 click -> ratio 1/5 = 0.20 (NOT < 0.20). Not zombie
        {'event_id': 26, 'user_id': 104, 'event_timestamp': '2024-03-01 13:00:00', 'event_type': 'app_open', 'session_id': 'S104', 'event_value': None},
        {'event_id': 27, 'user_id': 104, 'event_timestamp': '2024-03-01 13:05:00', 'event_type': 'scroll', 'session_id': 'S104', 'event_value': 1},
        {'event_id': 28, 'user_id': 104, 'event_timestamp': '2024-03-01 13:10:00', 'event_type': 'scroll', 'session_id': 'S104', 'event_value': 1},
        {'event_id': 29, 'user_id': 104, 'event_timestamp': '2024-03-01 13:15:00', 'event_type': 'scroll', 'session_id': 'S104', 'event_value': 1},
        {'event_id': 30, 'user_id': 104, 'event_timestamp': '2024-03-01 13:20:00', 'event_type': 'scroll', 'session_id': 'S104', 'event_value': 1},
        {'event_id': 31, 'user_id': 104, 'event_timestamp': '2024-03-01 13:25:00', 'event_type': 'scroll', 'session_id': 'S104', 'event_value': 1}, # 5 scrolls
        {'event_id': 32, 'user_id': 104, 'event_timestamp': '2024-03-01 13:28:00', 'event_type': 'click', 'session_id': 'S104', 'event_value': None}, # 1 click
        {'event_id': 33, 'user_id': 104, 'event_timestamp': '2024-03-01 13:31:00', 'event_type': 'app_close', 'session_id': 'S104', 'event_value': None}, # 31 min duration
    ]
    app_events_df_3 = pd.DataFrame(app_events_data_3)
    # Expected: S101 (7 scrolls) then S102 (6 scrolls) then S103 (5 scrolls)
    expected_3 = [
        ['S101', 100, 40, 7],
        ['S102', 102, 50, 6],
        ['S103', 103, 35, 5]
    ]
    result_3 = s.findZombieSessions(app_events_df_3.copy())
    assert result_3 == expected_3, f"Test Case 3 Failed: Expected {expected_3}, Got {result_3}"
    print(f"Test Case 3 Passed: {result_3}")

    print("All tests passed!")
```