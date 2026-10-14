"""
Find Category Recommendation Pairs
Difficulty: Hard

Description:
This problem requires identifying pairs of product categories that are frequently purchased together by the same customers. The goal is to find all category pairs (category1, category2, where category1 < category2 lexicographically) for which at least 3 unique customers have purchased products from both categories. The final result should be ordered by the count of shared customers in descending order, then by category1 ascending, and finally by category2 ascending.

Example:
Input:
ProductPurchases table:
+---------+------------+----------+
| user_id | product_id | quantity |
+---------+------------+----------+
| 1       | 101        | 2        |
| 1       | 102        | 1        |
| 1       | 201        | 3        |
| 1       | 301        | 1        |
| 2       | 101        | 1        |
| 2       | 102        | 2        |
| 2       | 103        | 1        |
| 2       | 201        | 5        |
| 3       | 101        | 2        |
| 3       | 103        | 1        |
| 3       | 301        | 4        |
| 3       | 401        | 2        |
| 4       | 101        | 1        |
| 4       | 201        | 3        |
| 4       | 301        | 1        |
| 4       | 401        | 2        |
| 5       | 102        | 2        |
| 5       | 103        | 1        |
| 5       | 201        | 2        |
| 5       | 202        | 3        |
+---------+------------+----------+

ProductInfo table:
+------------+-------------+-------+
| product_id | category    | price |
+------------+-------------+-------+
| 101        | Electronics | 100   |
| 102        | Books       | 20    |
| 103        | Books       | 35    |
| 201        | Clothing    | 45    |
| 202        | Clothing    | 60    |
| 301        | Sports      | 75    |
| 401        | Kitchen     | 50    |
+------------+-------------+-------+

Output:
+-------------+-------------+----------------+
| category1   | category2   | customer_count |
+-------------+-------------+----------------+
| Books       | Clothing    | 3              |
| Books       | Electronics | 3              |
| Clothing    | Electronics | 3              |
| Electronics | Sports      | 3              |
+-------------+-------------+----------------+

Approach:
The solution involves several steps to aggregate and process the purchase data. First, a mapping from product IDs to their respective categories is built using the ProductInfo table for efficient lookups. Next, for each user, a set of all unique categories they have purchased from is compiled by iterating through the ProductPurchases and using the product-to-category mapping. To efficiently count shared customers between category pairs, an inverted mapping is then created: a dictionary where each key is a category and its value is a set of all unique users who have purchased products from that category. Finally, all unique category pairs (ensuring category1 < category2) are generated. For each pair, the intersection of the user sets for both categories is computed to determine the number of shared customers. Pairs with at least 3 shared customers are collected and then sorted according to the specified criteria: customer_count descending, then category1 ascending, and finally by category2 ascending.

Time Complexity: O(N + C^2 * U)
Let N be the number of rows in ProductPurchases, P be the number of rows in ProductInfo, C be the number of unique categories, and U be the number of unique users.
1. Building `product_id_to_category`: O(P).
2. Building `user_to_categories`: O(N) on average (iterating through N purchases, with O(1) average time for dictionary lookups and set insertions).
3. Building `category_to_users`: O(N_unique_user_categories), where N_unique_user_categories is the total count of unique (user, category) pairs, which is at most O(N).
4. Getting sorted `all_categories`: O(C log C).
5. Iterating through category pairs and computing intersections: There are O(C^2) possible pairs. For each pair, set intersection takes O(min(size_of_set1, size_of_set2)), which is at most O(U) in the worst case (if all U users bought from both categories). Thus, this step is O(C^2 * U).
6. Sorting the reportable pairs: O(R log R), where R is the number of reportable pairs (at most O(C^2)). This simplifies to O(C^2 log C).
The dominant factor in the overall time complexity is O(N + C^2 * U).

Space Complexity: O(N + C^2)
1. Storing `product_id_to_category`: O(P).
2. Storing `user_to_categories`: O(U + N_unique_user_categories), which simplifies to O(N) as N_unique_user_categories <= N.
3. Storing `category_to_users`: O(C + N_unique_user_categories), which simplifies to O(N).
4. Storing `all_categories`: O(C).
5. Storing `reportable_pairs_data`: O(R), which is O(C^2) in the worst case (if all pairs are reportable).
The dominant factor in the overall space complexity is O(N + C^2).
"""
import collections
from typing import List, Dict, Set, Tuple

class Solution:
    def findCategoryRecommendationPairs(self, productPurchases: List[Dict], productInfo: List[Dict]) -> List[Dict]:
        
        # Step 1: Create a mapping from product_id to category for efficient lookups.
        # This takes O(P) time where P is the number of products in ProductInfo.
        product_id_to_category: Dict[int, str] = {p['product_id']: p['category'] for p in productInfo}

        # Step 2: For each user, determine the set of unique categories they have purchased from.
        # This takes O(N) time where N is the number of purchases in ProductPurchases.
        # Each lookup in product_id_to_category and insertion into a set is O(1) on average.
        user_to_categories: Dict[int, Set[str]] = collections.defaultdict(set)
        for purchase in productPurchases:
            user_id = purchase['user_id']
            product_id = purchase['product_id']
            category = product_id_to_category.get(product_id)
            if category: # Ensure product_id exists in ProductInfo
                user_to_categories[user_id].add(category)
        
        # Step 3: Create an inverted mapping from each category to the set of unique users
        # who have purchased products from that category.
        # This takes O(N_unique_user_categories) time, which is at most O(N), as each (user, category) pair
        # derived from purchases is processed.
        category_to_users: Dict[str, Set[int]] = collections.defaultdict(set)
        for user_id, categories_purchased in user_to_categories.items():
            for category in categories_purchased:
                category_to_users[category].add(user_id)

        # Get all unique categories present in the data, sorted lexicographically.
        # Sorting ensures consistent pair generation (category1 < category2) and can help with deterministic output.
        # This takes O(C log C) time, where C is the number of unique categories.
        all_categories = sorted(list(category_to_users.keys()))

        # Step 4: Iterate through all unique category pairs (cat1 < cat2) and count shared customers.
        # This is the most computationally intensive part. There are O(C^2) possible pairs.
        # For each pair, calculating set intersection takes O(min(len(set1), len(set2))) time,
        # which is at most O(U) where U is the number of unique users.
        # Thus, this step is O(C^2 * U) in the worst case.
        reportable_pairs_data: List[Dict] = []
        
        for i in range(len(all_categories)):
            for j in range(i + 1, len(all_categories)):
                cat1 = all_categories[i]
                cat2 = all_categories[j]

                users_in_cat1 = category_to_users[cat1]
                users_in_cat2 = category_to_users[cat2]

                # Calculate the number of unique customers who purchased from both categories
                shared_customers_count = len(users_in_cat1.intersection(users_in_cat2))

                # Step 5: Filter for reportable pairs (at least 3 different customers)
                if shared_customers_count >= 3:
                    reportable_pairs_data.append({
                        'category1': cat1,
                        'category2': cat2,
                        'customer_count': shared_customers_count
                    })

        # Step 6: Sort the result according to the specified criteria.
        # Order by customer_count in descending order, then by category1 in ascending order,
        # and finally by category2 in ascending order.
        # This takes O(R log R) time, where R is the number of reportable pairs (at most O(C^2)).
        reportable_pairs_data.sort(key=lambda x: (-x['customer_count'], x['category1'], x['category2']))

        return reportable_pairs_data

if __name__ == "__main__":
    s = Solution()

    # Example from problem description
    product_purchases_ex1 = [
        {'user_id': 1, 'product_id': 101, 'quantity': 2},
        {'user_id': 1, 'product_id': 102, 'quantity': 1},
        {'user_id': 1, 'product_id': 201, 'quantity': 3},
        {'user_id': 1, 'product_id': 301, 'quantity': 1},
        {'user_id': 2, 'product_id': 101, 'quantity': 1},
        {'user_id': 2, 'product_id': 102, 'quantity': 2},
        {'user_id': 2, 'product_id': 103, 'quantity': 1},
        {'user_id': 2, 'product_id': 201, 'quantity': 5},
        {'user_id': 3, 'product_id': 101, 'quantity': 2},
        {'user_id': 3, 'product_id': 103, 'quantity': 1},
        {'user_id': 3, 'product_id': 301, 'quantity': 4},
        {'user_id': 3, 'product_id': 401, 'quantity': 2},
        {'user_id': 4, 'product_id': 101, 'quantity': 1},
        {'user_id': 4, 'product_id': 201, 'quantity': 3},
        {'user_id': 4, 'product_id': 301, 'quantity': 1},
        {'user_id': 4, 'product_id': 401, 'quantity': 2},
        {'user_id': 5, 'product_id': 102, 'quantity': 2},
        {'user_id': 5, 'product_id': 103, 'quantity': 1},
        {'user_id': 5, 'product_id': 201, 'quantity': 2},
        {'user_id': 5, 'product_id': 202, 'quantity': 3}
    ]

    product_info_ex1 = [
        {'product_id': 101, 'category': 'Electronics', 'price': 100},
        {'product_id': 102, 'category': 'Books', 'price': 20},
        {'product_id': 103, 'category': 'Books', 'price': 35},
        {'product_id': 201, 'category': 'Clothing', 'price': 45},
        {'product_id': 202, 'category': 'Clothing', 'price': 60},
        {'product_id': 301, 'category': 'Sports', 'price': 75},
        {'product_id': 401, 'category': 'Kitchen', 'price': 50}
    ]

    expected_output_ex1 = [
        {'category1': 'Books', 'category2': 'Clothing', 'customer_count': 3},
        {'category1': 'Books', 'category2': 'Electronics', 'customer_count': 3},
        {'category1': 'Clothing', 'category2': 'Electronics', 'customer_count': 3},
        {'category1': 'Electronics', 'category2': 'Sports', 'customer_count': 3}
    ]

    result_ex1 = s.findCategoryRecommendationPairs(product_purchases_ex1, product_info_ex1)
    assert result_ex1 == expected_output_ex1, f"Test Case 1 Failed:\nExpected: {expected_output_ex1}\nGot: {result_ex1}"

    # Test Case 2: No reportable pairs (customer_count < 3)
    product_purchases_ex2 = [
        {'user_id': 1, 'product_id': 101, 'quantity': 1},
        {'user_id': 1, 'product_id': 201, 'quantity': 1},
        {'user_id': 2, 'product_id': 101, 'quantity': 1},
        {'user_id': 2, 'product_id': 201, 'quantity': 1},
        {'user_id': 3, 'product_id': 101, 'quantity': 1},
    ]
    product_info_ex2 = [
        {'product_id': 101, 'category': 'Electronics', 'price': 100},
        {'product_id': 201, 'category': 'Clothing', 'price': 45},
    ]
    expected_output_ex2 = []
    result_ex2 = s.findCategoryRecommendationPairs(product_purchases_ex2, product_info_ex2)
    assert result_ex2 == expected_output_ex2, f"Test Case 2 Failed:\nExpected: {expected_output_ex2}\nGot: {result_ex2}"

    # Test Case 3: More than 3 customers, different categories, various counts
    product_purchases_ex3 = [
        {'user_id': 1, 'product_id': 101, 'quantity': 1}, # E
        {'user_id': 1, 'product_id': 201, 'quantity': 1}, # C
        {'user_id': 1, 'product_id': 301, 'quantity': 1}, # B
        {'user_id': 2, 'product_id': 101, 'quantity': 1}, # E
        {'user_id': 2, 'product_id': 201, 'quantity': 1}, # C
        {'user_id': 2, 'product_id': 301, 'quantity': 1}, # B
        {'user_id': 3, 'product_id': 101, 'quantity': 1}, # E
        {'user_id': 3, 'product_id': 201, 'quantity': 1}, # C
        {'user_id': 4, 'product_id': 101, 'quantity': 1}, # E
        {'user_id': 4, 'product_id': 201, 'quantity': 1}, # C
        {'user_id': 4, 'product_id': 301, 'quantity': 1}, # B
        {'user_id': 5, 'product_id': 101, 'quantity': 1}, # E
        {'user_id': 5, 'product_id': 301, 'quantity': 1}, # B
    ]
    product_info_ex3 = [
        {'product_id': 101, 'category': 'Electronics', 'price': 100},
        {'product_id': 201, 'category': 'Clothing', 'price': 45},
        {'product_id': 301, 'category': 'Books', 'price': 20},
    ]
    expected_output_ex3 = [
        {'category1': 'Clothing', 'category2': 'Electronics', 'customer_count': 4},
        {'category1': 'Books', 'category2': 'Electronics', 'customer_count': 4},
        {'category1': 'Books', 'category2': 'Clothing', 'customer_count': 3},
    ]
    result_ex3 = s.findCategoryRecommendationPairs(product_purchases_ex3, product_info_ex3)
    assert result_ex3 == expected_output_ex3, f"Test Case 3 Failed:\nExpected: {expected_output_ex3}\nGot: {result_ex3}"


    # Test Case 4: Categories not in any purchase
    product_purchases_ex4 = [
        {'user_id': 1, 'product_id': 101, 'quantity': 1},
        {'user_id': 1, 'product_id': 201, 'quantity': 1},
        {'user_id': 2, 'product_id': 101, 'quantity': 1},
        {'user_id': 2, 'product_id': 201, 'quantity': 1},
        {'user_id': 3, 'product_id': 101, 'quantity': 1},
        {'user_id': 3, 'product_id': 201, 'quantity': 1},
    ]
    product_info_ex4 = [
        {'product_id': 101, 'category': 'A', 'price': 10},
        {'product_id': 201, 'category': 'B', 'price': 20},
        {'product_id': 301, 'category': 'C', 'price': 30}, # Not purchased
    ]
    expected_output_ex4 = [
        {'category1': 'A', 'category2': 'B', 'customer_count': 3},
    ]
    result_ex4 = s.findCategoryRecommendationPairs(product_purchases_ex4, product_info_ex4)
    assert result_ex4 == expected_output_ex4, f"Test Case 4 Failed:\nExpected: {expected_output_ex4}\nGot: {result_ex4}"


    print("All tests passed!")

