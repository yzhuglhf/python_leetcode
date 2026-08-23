"""
Find Churn Risk Customers
Difficulty: Medium

Description:
This problem requires identifying customers at risk of churning based on specific criteria derived from their subscription event history. 
These criteria include having an active subscription, performing downgrades, significant revenue reduction compared to historical maximum, 
and a minimum subscription duration.

Example:
Input:
subscription_events table:
+----------+---------+------------+------------+-----------+----------------+
| event_id | user_id | event_date | event_type | plan_name | monthly_amount |
+----------+---------+------------+------------+-----------+----------------+
| 1        | 501     | 2024-01-01 | start      | premium   | 29.99          |
| 2        | 501     | 2024-02-15 | downgrade  | standard  | 19.99          |
| 3        | 501     | 2024-03-20 | downgrade  | basic     | 9.99           |
| 4        | 502     | 2024-01-05 | start      | standard  | 19.99          |
| 5        | 502     | 2024-02-10 | upgrade    | premium   | 29.99          |
| 6        | 502     | 2024-03-15 | downgrade  | basic     | 9.99           |
| 7        | 503     | 2024-01-10 | start      | basic     | 9.99           |
| 8        | 503     | 2024-02-20 | upgrade    | standard   | 19.99          |
| 9        | 503     | 2024-03-25 | upgrade    | premium   | 29.99          |
| 10       | 504     | 2024-01-15 | start      | premium   | 29.99          |
| 11       | 504     | 2024-03-01 | downgrade  | standard   | 19.99          |
| 12       | 504     | 2024-03-30 | cancel     | NULL      | 0.00           |
| 13       | 505     | 2024-02-01 | start      | basic     | 9.99           |
| 14       | 505     | 2024-02-28 | upgrade    | standard   | 19.99          |
| 15       | 506     | 2024-01-20 | start      | premium   | 29.99          |
| 16       | 506     | 2024-03-10 | downgrade  | basic     | 9.99           |
+----------+---------+------------+------------+-----------+----------------+

Output:
+----------+--------------+------------------------+-----------------------+--------------------+
| user_id  | current_plan | current_monthly_amount | max_historical_amount | days_as_subscriber |
+----------+--------------+------------------------+-----------------------+--------------------+
| 501      | basic        | 9.99                   | 29.99                 | 79                 |
| 502      | basic        | 9.99                   | 29.99                 | 70                 |
+----------+--------------+------------------------+-----------------------+--------------------+

Approach:
The solution processes each user's subscription events to evaluate four churn risk criteria. First, events are grouped by user and sorted chronologically. For each user, it determines if their last event is a cancellation (Criterion 1), if they have any downgrade events (Criterion 2), if their current monthly subscription amount is less than 50% of their highest historical monthly amount (Criterion 3, ignoring cancel events for historical max), and if their total subscription duration is at least 60 days (Criterion 4). Users meeting all criteria are included in the result, which is then sorted by subscription duration (descending) and user ID (ascending).

Time Complexity: O(N log E_max) where N is the total number of events and E_max is the maximum number of events for a single user. In the worst case, E_max = N, leading to O(N log N).
Space Complexity: O(N) to store the grouped events and intermediate results.
"""
import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional

class Solution:
    def findChurnRiskCustomers(self, subscription_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        user_data = defaultdict(list)
        
        # Pre-process events: convert date strings to datetime.date objects
        # and group events by user_id. A shallow copy of each event dict is made
        # to avoid modifying the original input list in place.
        for event in subscription_events:
            event_copy = event.copy() 
            event_copy['event_date_obj'] = datetime.date.fromisoformat(event_copy['event_date'])
            user_data[event_copy['user_id']].append(event_copy)
        
        churn_risk_customers = []

        for user_id, events in user_data.items():
            # Sort events by date to easily find the first and last event,
            # and to process history chronologically.
            events.sort(key=lambda x: x['event_date_obj'])

            first_event = events[0]
            last_event = events[-1]

            # Criterion 1: Currently have an active subscription (their last event is not cancel).
            if last_event['event_type'] == 'cancel':
                continue # User is cancelled, not a churn risk customer

            # Criterion 2: Have performed at least one downgrade in their subscription history.
            has_downgrade = False
            for event in events:
                if event['event_type'] == 'downgrade':
                    has_downgrade = True
                    break
            if not has_downgrade:
                continue # No downgrades, not a churn risk customer

            # Criterion 3: Their current plan revenue is less than 50% of their historical maximum plan revenue.
            current_monthly_amount = float(last_event['monthly_amount'])
            
            # Calculate historical maximum monthly amount, excluding 'cancel' events where monthly_amount is 0.
            max_historical_amount = 0.0
            found_positive_amount = False # Flag to ensure a valid positive max_historical_amount was found.
            for event in events:
                if event['event_type'] != 'cancel':
                    amount = float(event['monthly_amount'])
                    if amount > 0: # Only consider positive amounts for max_historical_amount
                        max_historical_amount = max(max_historical_amount, amount)
                        found_positive_amount = True
            
            # If no positive historical amount was ever found, the comparison is meaningless.
            # This could happen if a user only ever had free plans or cancelled with 0 amount.
            if not found_positive_amount or max_historical_amount == 0: 
                continue 
            
            # Check the 50% revenue reduction condition
            if not (current_monthly_amount / max_historical_amount < 0.5):
                continue # Revenue condition not met, not a churn risk customer

            # Criterion 4: Have been a subscriber for at least 60 days.
            days_as_subscriber = (last_event['event_date_obj'] - first_event['event_date_obj']).days
            if days_as_subscriber < 60:
                continue # Insufficient duration, not a churn risk customer
            
            # If all criteria are met, add the user to the result list.
            churn_risk_customers.append({
                "user_id": user_id,
                "current_plan": last_event['plan_name'],
                "current_monthly_amount": current_monthly_amount,
                "max_historical_amount": max_historical_amount,
                "days_as_subscriber": days_as_subscriber
            })
        
        # Sort the final results as specified:
        # ordered by days_as_subscriber in descending order, then by user_id in ascending order.
        churn_risk_customers.sort(key=lambda x: (-x['days_as_subscriber'], x['user_id']))
        
        return churn_risk_customers

if __name__ == "__main__":
    s = Solution()
    
    subscription_events_input = [
        {'event_id': 1, 'user_id': 501, 'event_date': '2024-01-01', 'event_type': 'start', 'plan_name': 'premium', 'monthly_amount': 29.99},
        {'event_id': 2, 'user_id': 501, 'event_date': '2024-02-15', 'event_type': 'downgrade', 'plan_name': 'standard', 'monthly_amount': 19.99},
        {'event_id': 3, 'user_id': 501, 'event_date': '2024-03-20', 'event_type': 'downgrade', 'plan_name': 'basic', 'monthly_amount': 9.99},
        {'event_id': 4, 'user_id': 502, 'event_date': '2024-01-05', 'event_type': 'start', 'plan_name': 'standard', 'monthly_amount': 19.99},
        {'event_id': 5, 'user_id': 502, 'event_date': '2024-02-10', 'event_type': 'upgrade', 'plan_name': 'premium', 'monthly_amount': 29.99},
        {'event_id': 6, 'user_id': 502, 'event_date': '2024-03-15', 'event_type': 'downgrade', 'plan_name': 'basic', 'monthly_amount': 9.99},
        {'event_id': 7, 'user_id': 503, 'event_date': '2024-01-10', 'event_type': 'start', 'plan_name': 'basic', 'monthly_amount': 9.99},
        {'event_id': 8, 'user_id': 503, 'event_date': '2024-02-20', 'event_type': 'upgrade', 'plan_name': 'standard', 'monthly_amount': 19.99},
        {'event_id': 9, 'user_id': 503, 'event_date': '2024-03-25', 'event_type': 'upgrade', 'plan_name': 'premium', 'monthly_amount': 29.99},
        {'event_id': 10, 'user_id': 504, 'event_date': '2024-01-15', 'event_type': 'start', 'plan_name': 'premium', 'monthly_amount': 29.99},
        {'event_id': 11, 'user_id': 504, 'event_date': '2024-03-01', 'event_type': 'downgrade', 'plan_name': 'standard', 'monthly_amount': 19.99},
        {'event_id': 12, 'user_id': 504, 'event_date': '2024-03-30', 'event_type': 'cancel', 'plan_name': None, 'monthly_amount': 0.00},
        {'event_id': 13, 'user_id': 505, 'event_date': '2024-02-01', 'event_type': 'start', 'plan_name': 'basic', 'monthly_amount': 9.99},
        {'event_id': 14, 'user_id': 505, 'event_date': '2024-02-28', 'event_type': 'upgrade', 'plan_name': 'standard', 'monthly_amount': 19.99},
        {'event_id': 15, 'user_id': 506, 'event_date': '2024-01-20', 'event_type': 'start', 'plan_name': 'premium', 'monthly_amount': 29.99},
        {'event_id': 16, 'user_id': 506, 'event_date': '2024-03-10', 'event_type': 'downgrade', 'plan_name': 'basic', 'monthly_amount': 9.99}
    ]

    expected_output = [
        {'user_id': 501, 'current_plan': 'basic', 'current_monthly_amount': 9.99, 'max_historical_amount': 29.99, 'days_as_subscriber': 79},
        {'user_id': 502, 'current_plan': 'basic', 'current_monthly_amount': 9.99, 'max_historical_amount': 29.99, 'days_as_subscriber': 70}
    ]

    result = s.findChurnRiskCustomers(subscription_events_input)
    assert result == expected_output, f"Test failed. Expected: {expected_output}, Got: {result}"
    print("All tests passed!")

