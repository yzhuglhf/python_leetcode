"""
Find Users with Persistent Behavior Patterns
Difficulty: Hard

Description:
This problem requires identifying users who exhibit a stable behavior pattern, defined as performing the same single action for at least five consecutive days. If a user has multiple such sequences, only the longest one is considered. The final output needs to include the user ID, action, streak length, and the start and end dates of the longest qualifying streak, ordered by streak length (descending) then user ID (ascending).

Example:
Input:
activity table:
+---------+-------------+--------+
| user_id | action_date | action |
+---------+-------------+--------+
| 1       | 2024-01-01  | login  |
| 1       | 2024-01-02  | login  |
| 1       | 2024-01-03  | login  |
| 1       | 2024-01-04  | login  |
| 1       | 2024-01-05  | login  |
| 1       | 2024-01-06  | logout |
| 2       | 2024-01-01  | click  |
| 2       | 2024-01-02  | click  |
| 2       | 2024-01-03  | click  |
| 2       | 2024-01-04  | click  |
| 3       | 2024-01-01  | view   |
| 3       | 2024-01-02  | view   |
| 3       | 2024-01-03  | view   |
| 3       | 2024-01-04  | view   |
| 3       | 2024-01-05  | view   |
| 3       | 2024-01-06  | view   |
| 3       | 2024-01-07  | view   |
+---------+-------------+--------+

Output:
+---------+--------+---------------+------------+------------+
| user_id | action | streak_length | start_date | end_date   |
+---------+--------+---------------+------------+------------+
| 3       | view   | 7             | 2024-01-01 | 2024-01-07 |
| 1       | login  | 5             | 2024-01-01 | 2024-01-05 |
+---------+--------+---------------+------------+------------+

Approach:
The solution involves several steps using pandas for data manipulation. First, the 'action_date' column is converted to datetime objects. Then, to enforce the "exactly one action per day" rule, we count actions per user per day and filter the original activity to retain only those days where a user performed a single action. Next, to identify consecutive day streaks with the same action, the filtered data is sorted by user, action, and date. A 'group_id' is computed by subtracting a sequential rank from the 'action_date' within each (user, action) partition; this 'group_id' remains constant for consecutive dates. The data is then grouped by user, action, and 'group_id' to calculate the 'streak_length', 'start_date', and 'end_date' for each potential streak. Streaks shorter than 5 days are filtered out. Finally, for each user, the longest qualifying streak is selected (with action as a tie-breaker if multiple streaks have the same maximum length), and the results are sorted as specified before formatting dates to string.

Time Complexity: O(N log N)
The dominant operations are sorting (`sort_values`) and operations within `groupby` that often involve sorting or hash table construction, where N is the number of rows in the input `activity` table.
Space Complexity: O(N)
Several intermediate DataFrames are created to store filtered data, ranks, group IDs, and streak aggregates. In the worst case, these can be proportional to the size of the input table.
"""
import pandas as pd
from typing import List, Optional

class Solution:
    def find_persistent_behavior_patterns(self, activity: pd.DataFrame) -> pd.DataFrame:
        # Step 1: Ensure 'action_date' is in datetime format and filter for single action per day.
        # Convert 'action_date' to datetime objects for date arithmetic.
        activity['action_date'] = pd.to_datetime(activity['action_date'])

        # Count actions per user per day to identify days with exactly one action.
        daily_action_counts = activity.groupby(['user_id', 'action_date']).size().reset_index(name='action_count')

        # Filter for days where a user performed exactly one action.
        single_action_days = daily_action_counts[daily_action_counts['action_count'] == 1]

        # Merge back with the original activity data to keep only rows corresponding to single-action days.
        # This implicitly removes days where a user had multiple actions.
        filtered_activity = pd.merge(activity, single_action_days[['user_id', 'action_date']],
                                     on=['user_id', 'action_date'], how='inner')

        # Step 2 & 3: Identify potential streaks and calculate their properties (length, start, end dates).
        # Sort the filtered data by user, action, and date to prepare for streak identification.
        filtered_activity = filtered_activity.sort_values(by=['user_id', 'action', 'action_date'])

        # Calculate a 'group_id' for each continuous sequence of dates with the same action for a user.
        # This is achieved by subtracting a sequential rank (number of days passed since the start of a potential sequence)
        # from the 'action_date'. If the dates are consecutive, this difference remains constant.
        filtered_activity['rank'] = filtered_activity.groupby(['user_id', 'action'])['action_date'].rank(method='dense')
        filtered_activity['group_id'] = filtered_activity['action_date'] - pd.to_timedelta(filtered_activity['rank'].astype(int) - 1, unit='D')

        # Group by user, action, and the calculated 'group_id' to aggregate streak information.
        # For each group, we calculate the streak length (count of days), minimum date (start_date),
        # and maximum date (end_date).
        streaks = filtered_activity.groupby(['user_id', 'action', 'group_id']).agg(
            streak_length=('action_date', 'count'),
            start_date=('action_date', 'min'),
            end_date=('action_date', 'max')
        ).reset_index()

        # The 'group_id' was a temporary column for grouping; it's no longer needed in the final output.
        streaks = streaks.drop(columns=['group_id'])

        # Step 4: Filter for minimum streak length and select the maximum streak per user.
        # Keep only streaks that are at least 5 days long, as per the problem definition.
        long_streaks = streaks[streaks['streak_length'] >= 5]

        # If no users qualify after filtering, return an empty DataFrame with the expected columns.
        if long_streaks.empty:
            return pd.DataFrame(columns=['user_id', 'action', 'streak_length', 'start_date', 'end_date'])

        # For users with multiple qualifying streaks, select only the one with the maximum length.
        # In case of ties in maximum streak length for a user, we sort by 'action' ascending to ensure a deterministic choice
        # before dropping duplicates, keeping the 'first' (which will be the one with the highest streak_length and then alphabetically first action).
        long_streaks = long_streaks.sort_values(by=['user_id', 'streak_length', 'action'], ascending=[True, False, True])
        max_streaks_per_user = long_streaks.drop_duplicates(subset=['user_id'], keep='first')

        # Step 5: Order the final result as specified.
        # The result table should be ordered by 'streak_length' in descending order,
        # then by 'user_id' in ascending order.
        final_result = max_streaks_per_user.sort_values(by=['streak_length', 'user_id'], ascending=[False, True])

        # Format 'start_date' and 'end_date' columns to 'YYYY-MM-DD' string format.
        final_result['start_date'] = final_result['start_date'].dt.strftime('%Y-%m-%d')
        final_result['end_date'] = final_result['end_date'].dt.strftime('%Y-%m-%d')

        return final_result

if __name__ == "__main__":
    s = Solution()

    # Test Case 1: Basic case from problem description
    activity_data_1 = {
        'user_id': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3],
        'action_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06',
                        '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04',
                        '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07'],
        'action': ['login', 'login', 'login', 'login', 'login', 'logout',
                   'click', 'click', 'click', 'click',
                   'view', 'view', 'view', 'view', 'view', 'view', 'view']
    }
    activity_df_1 = pd.DataFrame(activity_data_1)
    
    expected_output_1_data = {
        'user_id': [3, 1],
        'action': ['view', 'login'],
        'streak_length': [7, 5],
        'start_date': ['2024-01-01', '2024-01-01'],
        'end_date': ['2024-01-07', '2024-01-05']
    }
    expected_output_1 = pd.DataFrame(expected_output_1_data)
    
    result_1 = s.find_persistent_behavior_patterns(activity_df_1.copy())
    pd.testing.assert_frame_equal(result_1, expected_output_1, check_dtype=False)
    print("Test Case 1 Passed: Example from problem description.")

    # Test Case 2: No qualifying streaks (all < 5 days)
    activity_data_2 = {
        'user_id': [1, 1, 1, 1, 2, 2, 2, 3, 3],
        'action_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04',
                        '2024-01-01', '2024-01-02', '2024-01-03',
                        '2024-01-05', '2024-01-06'],
        'action': ['login', 'login', 'login', 'login',
                   'click', 'click', 'click',
                   'view', 'view']
    }
    activity_df_2 = pd.DataFrame(activity_data_2)
    
    expected_output_2 = pd.DataFrame(columns=['user_id', 'action', 'streak_length', 'start_date', 'end_date'])
    result_2 = s.find_persistent_behavior_patterns(activity_df_2.copy())
    pd.testing.assert_frame_equal(result_2, expected_output_2, check_dtype=False)
    print("Test Case 2 Passed: No qualifying streaks.")

    # Test Case 3: User with multiple actions on a single day, breaking a potential streak
    activity_data_3 = {
        'user_id': [1, 1, 1, 1, 1, 1, 1],
        'action_date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06'],
        'action': ['login', 'click', 'login', 'login', 'login', 'login', 'login']
    }
    activity_df_3 = pd.DataFrame(activity_data_3)
    # The 'login' streak starts from 2024-01-02, so it's 5 days long.
    expected_output_3_data = {
        'user_id': [1],
        'action': ['login'],
        'streak_length': [5],
        'start_date': ['2024-01-02'],
        'end_date': ['2024-01-06']
    }
    expected_output_3 = pd.DataFrame(expected_output_3_data)
    
    result_3 = s.find_persistent_behavior_patterns(activity_df_3.copy())
    pd.testing.assert_frame_equal(result_3, expected_output_3, check_dtype=False)
    print("Test Case 3 Passed: Multiple actions on one day handling.")

    # Test Case 4: Multiple qualifying streaks for a user, pick longest
    activity_data_4 = {
        'user_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'action_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', # login 5 days
                        '2024-01-10', '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14', '2024-01-15', '2024-01-16'], # click 7 days
        'action': ['login', 'login', 'login', 'login', 'login',
                   'click', 'click', 'click', 'click', 'click', 'click', 'click']
    }
    activity_df_4 = pd.DataFrame(activity_data_4)
    
    expected_output_4_data = {
        'user_id': [1],
        'action': ['click'],
        'streak_length': [7],
        'start_date': ['2024-01-10'],
        'end_date': ['2024-01-16']
    }
    expected_output_4 = pd.DataFrame(expected_output_4_data)
    
    result_4 = s.find_persistent_behavior_patterns(activity_df_4.copy())
    pd.testing.assert_frame_equal(result_4, expected_output_4, check_dtype=False)
    print("Test Case 4 Passed: Multiple qualifying streaks, pick longest.")

    # Test Case 5: Tie in max streak length for a user, check tie-breaker (action ascending)
    activity_data_5 = {
        'user_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'action_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', # A 5 days
                        '2024-01-10', '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14'], # B 5 days
        'action': ['A', 'A', 'A', 'A', 'A',
                   'B', 'B', 'B', 'B', 'B']
    }
    activity_df_5 = pd.DataFrame(activity_data_5)
    
    expected_output_5_data = {
        'user_id': [1],
        'action': ['A'], # 'A' comes before 'B' alphabetically
        'streak_length': [5],
        'start_date': ['2024-01-01'],
        'end_date': ['2024-01-05']
    }
    expected_output_5 = pd.DataFrame(expected_output_5_data)
    
    result_5 = s.find_persistent_behavior_patterns(activity_df_5.copy())
    pd.testing.assert_frame_equal(result_5, expected_output_5, check_dtype=False)
    print("Test Case 5 Passed: Tie in max streak length, action tie-breaker.")

    # Test Case 6: Empty activity table
    activity_data_6 = {
        'user_id': [],
        'action_date': [],
        'action': []
    }
    activity_df_6 = pd.DataFrame(activity_data_6)
    
    expected_output_6 = pd.DataFrame(columns=['user_id', 'action', 'streak_length', 'start_date', 'end_date'])
    result_6 = s.find_persistent_behavior_patterns(activity_df_6.copy())
    pd.testing.assert_frame_equal(result_6, expected_output_6, check_dtype=False)
    print("Test Case 6 Passed: Empty activity table.")

    # Test Case 7: Gaps in dates within a potential streak
    activity_data_7 = {
        'user_id': [1, 1, 1, 1, 1, 1],
        'action_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-05', '2024-01-06', '2024-01-07'],
        'action': ['login', 'login', 'login', 'login', 'login', 'login']
    }
    activity_df_7 = pd.DataFrame(activity_data_7)
    # Streaks: (2024-01-01 to 2024-01-03, length 3), (2024-01-05 to 2024-01-07, length 3)
    # Neither qualifies (both less than 5 days)
    expected_output_7 = pd.DataFrame(columns=['user_id', 'action', 'streak_length', 'start_date', 'end_date'])
    result_7 = s.find_persistent_behavior_patterns(activity_df_7.copy())
    pd.testing.assert_frame_equal(result_7, expected_output_7, check_dtype=False)
    print("Test Case 7 Passed: Gaps in dates.")

    print("All tests passed!")

