"""
Find Emotionally Consistent Users
Difficulty: Medium

Description:
This problem requires identifying users who demonstrate a strong consistency in their emotional reactions to content. We need to analyze each user's reactions, filter out those who haven't reacted to a sufficient number of distinct content items, and then determine if their most frequent reaction type constitutes a significant majority (at least 60%) of their total reactions.

Example:
Input:
reactions table:
+---------+------------+----------+
| user_id | content_id | reaction |
+---------+------------+----------+
| 1       | 101        | like     |
| 1       | 102        | like     |
| 1       | 103        | like     |
| 1       | 104        | wow      |
| 1       | 105        | like     |
| 2       | 201        | like     |
| 2       | 202        | wow      |
| 2       | 203        | sad      |
| 2       | 204        | like     |
| 2       | 205        | wow      |
| 3       | 301        | love     |
| 3       | 302        | love     |
| 3       | 303        | love     |
| 3       | 304        | love     |
| 3       | 305        | love     |
+---------+------------+----------+

Output:
+---------+-------------------+----------------+
| user_id | dominant_reaction | reaction_ratio |
+---------+-------------------+----------------+
| 3       | love              | 1.00           |
| 1       | like              | 0.80           |
+---------+-------------------+----------------+

Approach:
The solution involves several steps using the pandas library for data manipulation. First, we group the input `reactions` DataFrame by `user_id` to calculate two key metrics: the total number of reactions each user gave (`total_reactions`) and the number of distinct content items they reacted to (`distinct_content_items`). We then filter these users, keeping only those who have reacted to at least 5 different content items. For these eligible users, we again group their reactions to determine their most frequent reaction type (`dominant_reaction`) and its count (`dominant_reaction_count`) using a custom aggregation function. The `reaction_ratio` is then computed by dividing `dominant_reaction_count` by `total_reactions` and rounded to two decimal places. Finally, we filter users whose `reaction_ratio` is less than 0.60, and sort the remaining users by `reaction_ratio` in descending order, followed by `user_id` in ascending order, before returning the required columns.

Time Complexity: O(N log N)
- Groupby operations (counting total reactions, distinct content IDs, and dominant reactions) typically take O(N) time, where N is the number of rows in the `reactions` table. The `apply` method on grouped objects can be less efficient than optimized C-extensions, but for this specific logic (`value_counts` and `idxmax`), it performs well.
- Merging DataFrames takes O(N) in the worst case.
- Sorting the final result takes O(K log K) where K is the number of consistent users. In the worst case, K can be N.
Considering all steps, the overall time complexity is dominated by the groupby operations and the final sort, making it approximately O(N log N) in the general case.

Space Complexity: O(N)
- Intermediate DataFrames like `user_reaction_stats`, `eligible_reactions_data`, `dominant_reactions_df`, and `final_df` can store up to N rows, each potentially with several columns. This leads to O(N) space complexity to hold these temporary results.
"""
import pandas as pd
from typing import List, Optional

class Solution:
    def findEmotionallyConsistentUsers(self, reactions: pd.DataFrame) -> pd.DataFrame:
        # Step 1: Calculate total reactions and distinct content items per user
        user_reaction_stats = reactions.groupby('user_id').agg(
            total_reactions=('reaction', 'count'),
            distinct_content_items=('content_id', 'nunique')
        ).reset_index()

        # Step 2: Filter users who have reacted to at least 5 different content items
        eligible_users = user_reaction_stats[user_reaction_stats['distinct_content_items'] >= 5]

        # If no users meet the distinct content item requirement, return an empty DataFrame
        if eligible_users.empty:
            return pd.DataFrame(columns=['user_id', 'dominant_reaction', 'reaction_ratio'])

        # Filter the original reactions to only include data for eligible users
        eligible_reactions_data = reactions[reactions['user_id'].isin(eligible_users['user_id'])]

        # Step 3: Find dominant reaction and its count for each eligible user
        def get_dominant_reaction_info(group):
            # value_counts() returns a Series of unique reactions and their counts,
            # sorted in descending order by frequency.
            reaction_counts = group['reaction'].value_counts()
            
            # If a group is somehow empty (should not happen with prior filtering if input is valid),
            # return default values.
            if reaction_counts.empty:
                return pd.Series([None, 0])
            
            # The most frequent reaction is the index of the first item
            dominant_reaction = reaction_counts.index[0]
            # Its count is the value of the first item
            dominant_reaction_count = reaction_counts.iloc[0]
            
            return pd.Series([dominant_reaction, dominant_reaction_count])

        # Apply the function to each user's reactions to get dominant reaction details
        dominant_reactions_df = eligible_reactions_data.groupby('user_id').apply(get_dominant_reaction_info)
        dominant_reactions_df.columns = ['dominant_reaction', 'dominant_reaction_count']
        dominant_reactions_df = dominant_reactions_df.reset_index()

        # Step 4: Merge with eligible_users to combine total reactions and dominant reaction info
        final_df = pd.merge(eligible_users, dominant_reactions_df, on='user_id')

        # Step 5: Calculate reaction_ratio
        final_df['reaction_ratio'] = final_df['dominant_reaction_count'] / final_df['total_reactions']

        # Step 6: Apply consistency requirement (at least 60%)
        final_df = final_df[final_df['reaction_ratio'] >= 0.60]

        # If after filtering by ratio, no users remain, return an empty DataFrame
        if final_df.empty:
            return pd.DataFrame(columns=['user_id', 'dominant_reaction', 'reaction_ratio'])

        # Step 7: Round reaction_ratio to 2 decimal places
        final_df['reaction_ratio'] = final_df['reaction_ratio'].round(2)

        # Step 8: Select and order columns as per the output requirements
        result_df = final_df[['user_id', 'dominant_reaction', 'reaction_ratio']]
        result_df = result_df.sort_values(by=['reaction_ratio', 'user_id'], ascending=[False, True])

        return result_df

if __name__ == "__main__":
    s = Solution()

    # Test Case 1: Provided in the problem description
    reactions_data_1 = [
        {'user_id': 1, 'content_id': 101, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 102, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 103, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 104, 'reaction': 'wow'},
        {'user_id': 1, 'content_id': 105, 'reaction': 'like'},
        {'user_id': 2, 'content_id': 201, 'reaction': 'like'},
        {'user_id': 2, 'content_id': 202, 'reaction': 'wow'},
        {'user_id': 2, 'content_id': 203, 'reaction': 'sad'},
        {'user_id': 2, 'content_id': 204, 'reaction': 'like'},
        {'user_id': 2, 'content_id': 205, 'reaction': 'wow'},
        {'user_id': 3, 'content_id': 301, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 302, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 303, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 304, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 305, 'reaction': 'love'},
    ]
    reactions_df_1 = pd.DataFrame(reactions_data_1)
    
    expected_output_1_data = [
        {'user_id': 3, 'dominant_reaction': 'love', 'reaction_ratio': 1.00},
        {'user_id': 1, 'dominant_reaction': 'like', 'reaction_ratio': 0.80},
    ]
    expected_output_df_1 = pd.DataFrame(expected_output_1_data)
    
    result_df_1 = s.findEmotionallyConsistentUsers(reactions_df_1)
    pd.testing.assert_frame_equal(result_df_1, expected_output_df_1, check_dtype=True)

    # Test Case 2: No users meet distinct content item requirement (< 5 distinct content_ids)
    reactions_data_2 = [
        {'user_id': 1, 'content_id': 101, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 102, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 103, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 104, 'reaction': 'wow'}, # Only 4 distinct content for user 1
        {'user_id': 2, 'content_id': 201, 'reaction': 'like'},
        {'user_id': 2, 'content_id': 202, 'reaction': 'wow'}, # Only 2 distinct content for user 2
    ]
    reactions_df_2 = pd.DataFrame(reactions_data_2)
    expected_output_df_2 = pd.DataFrame(columns=['user_id', 'dominant_reaction', 'reaction_ratio']) # Empty DataFrame
    result_df_2 = s.findEmotionallyConsistentUsers(reactions_df_2)
    pd.testing.assert_frame_equal(result_df_2, expected_output_df_2, check_dtype=True)

    # Test Case 3: Users meet distinct content item requirement, but not ratio requirement (< 60%)
    reactions_data_3 = [
        {'user_id': 1, 'content_id': 101, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 102, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 103, 'reaction': 'wow'},
        {'user_id': 1, 'content_id': 104, 'reaction': 'sad'},
        {'user_id': 1, 'content_id': 105, 'reaction': 'happy'}, # 5 reactions, all different types. Max count 1. Ratio 1/5 = 0.2
    ]
    reactions_df_3 = pd.DataFrame(reactions_data_3)
    expected_output_df_3 = pd.DataFrame(columns=['user_id', 'dominant_reaction', 'reaction_ratio']) # Empty DataFrame
    result_df_3 = s.findEmotionallyConsistentUsers(reactions_df_3)
    pd.testing.assert_frame_equal(result_df_3, expected_output_df_3, check_dtype=True)
    
    # Test Case 4: User with exactly 5 distinct reactions, 3 of one type, ratio 0.60 (borderline case)
    reactions_data_4 = [
        {'user_id': 1, 'content_id': 101, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 102, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 103, 'reaction': 'like'}, # 3 likes
        {'user_id': 1, 'content_id': 104, 'reaction': 'wow'},
        {'user_id': 1, 'content_id': 105, 'reaction': 'sad'}, # Total 5 reactions, 5 distinct content. Dominant is 'like' with 3. Ratio = 3/5 = 0.60
    ]
    reactions_df_4 = pd.DataFrame(reactions_data_4)
    expected_output_4_data = [
        {'user_id': 1, 'dominant_reaction': 'like', 'reaction_ratio': 0.60},
    ]
    expected_output_df_4 = pd.DataFrame(expected_output_4_data)
    result_df_4 = s.findEmotionallyConsistentUsers(reactions_df_4)
    pd.testing.assert_frame_equal(result_df_4, expected_output_df_4, check_dtype=True)

    # Test Case 5: Empty input table
    reactions_df_5 = pd.DataFrame(columns=['user_id', 'content_id', 'reaction'])
    expected_output_df_5 = pd.DataFrame(columns=['user_id', 'dominant_reaction', 'reaction_ratio'])
    result_df_5 = s.findEmotionallyConsistentUsers(reactions_df_5)
    pd.testing.assert_frame_equal(result_df_5, expected_output_df_5, check_dtype=True)

    # Test Case 6: More users, some consistent, some not, different content counts
    reactions_data_6 = [
        {'user_id': 1, 'content_id': 101, 'reaction': 'like'}, # User 1: 5 distinct, 4 likes (0.8) -> Consistent
        {'user_id': 1, 'content_id': 102, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 103, 'reaction': 'like'},
        {'user_id': 1, 'content_id': 104, 'reaction': 'wow'},
        {'user_id': 1, 'content_id': 105, 'reaction': 'like'},
        {'user_id': 2, 'content_id': 201, 'reaction': 'like'}, # User 2: 4 distinct -> Not eligible
        {'user_id': 2, 'content_id': 202, 'reaction': 'wow'},
        {'user_id': 2, 'content_id': 203, 'reaction': 'sad'},
        {'user_id': 2, 'content_id': 204, 'reaction': 'like'},
        {'user_id': 3, 'content_id': 301, 'reaction': 'love'}, # User 3: 6 distinct, 4 loves, 2 likes. Total 6 reactions. 4/6 = 0.666... -> 0.67 -> Consistent
        {'user_id': 3, 'content_id': 302, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 303, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 304, 'reaction': 'like'},
        {'user_id': 3, 'content_id': 305, 'reaction': 'love'},
        {'user_id': 3, 'content_id': 306, 'reaction': 'like'},
        {'user_id': 4, 'content_id': 401, 'reaction': 'happy'},# User 4: 5 distinct, 3 happy, 2 sad. Total 5 reactions. 3/5 = 0.60 -> Consistent
        {'user_id': 4, 'content_id': 402, 'reaction': 'happy'},
        {'user_id': 4, 'content_id': 403, 'reaction': 'sad'},
        {'user_id': 4, 'content_id': 404, 'reaction': 'happy'},
        {'user_id': 4, 'content_id': 405, 'reaction': 'sad'},
        {'user_id': 5, 'content_id': 501, 'reaction': 'like'}, # User 5: 5 distinct, 2 like, 2 wow, 1 sad. Total 5 reactions. 2/5 = 0.40 -> Not consistent
        {'user_id': 5, 'content_id': 502, 'reaction': 'wow'},
        {'user_id': 5, 'content_id': 503, 'reaction': 'sad'},
        {'user_id': 5, 'content_id': 504, 'reaction': 'like'},
        {'user_id': 5, 'content_id': 505, 'reaction': 'wow'},
    ]
    reactions_df_6 = pd.DataFrame(reactions_data_6)
    expected_output_6_data = [
        {'user_id': 1, 'dominant_reaction': 'like', 'reaction_ratio': 0.80},
        {'user_id': 3, 'dominant_reaction': 'love', 'reaction_ratio': 0.67},
        {'user_id': 4, 'dominant_reaction': 'happy', 'reaction_ratio': 0.60},
    ]
    expected_output_df_6 = pd.DataFrame(expected_output_6_data)
    result_df_6 = s.findEmotionallyConsistentUsers(reactions_df_6)
    pd.testing.assert_frame_equal(result_df_6, expected_output_df_6, check_dtype=True)

    print("All tests passed!")

