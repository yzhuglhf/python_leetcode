import collections
from typing import List

class Solution:
    def maximumMEX(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # dp_mex_value[i] stores the chosen MEX for the segment nums[i:dp_next_idx[i]]
        # dp_next_idx[i] stores the index of the start of the next segment
        dp_mex_value = [-1] * (n + 1)
        dp_next_idx = [n] * (n + 1)
        
        # rank_values[i] stores a tuple representing the lexicographical value of dp[i].
        # It is (first_MEX_value, rank_of_subsequent_segment).
        # Python's tuple comparison works lexicographically.
        # rank_values[n] corresponds to an empty array. A non-existent MEX is -1, 
        # and an empty array is the base case, represented by an empty tuple.
        # So, (-1, ()) is the "smallest" possible rank tuple.
        rank_values = [(-1, ())] * (n + 1) 

        # Iterate `i` from `n-1` down to `0` (inclusive).
        # `i` is the starting index of the current segment `nums[i:]`.
        for i in range(n - 1, -1, -1):
            max_overall_mex_val = 0
            best_next_idx_for_i = n 
            # Initialize with the rank of an empty array, which is the smallest.
            best_rank_tuple_for_split = rank_values[n] 
            
            # `freq` map to count elements in the current segment `nums[i...j]`.
            freq = collections.defaultdict(int)
            # `current_mex_candidate` is the smallest non-negative integer not yet seen in `nums[i...j]`.
            current_mex_candidate = 0
            
            # Iterate `j` from `i` to `n-1`. `j` is the ending index of the current prefix `nums[i...j]`.
            for j in range(i, n):
                val = nums[j]
                freq[val] += 1
                
                # Update `current_mex_candidate`: increment as long as it's present in `freq`.
                while freq[current_mex_candidate] > 0:
                    current_mex_candidate += 1
                
                # `current_mex_candidate` is now MEX(nums[i...j]).
                current_mex_val = current_mex_candidate
                # The next segment starts at `j + 1`.
                next_segment_start_idx = j + 1

                # Form a tuple for the current choice: (MEX of current segment, rank of subsequent segment).
                # `rank_values[next_segment_start_idx]` is already computed from previous iterations (since `next_segment_start_idx > i`).
                current_candidate_rank_tuple = (current_mex_val, rank_values[next_segment_start_idx])

                # Compare the current choice's rank tuple with the best found so far for this `i`.
                # Python's tuple comparison is lexicographical, handling the problem's requirement directly.
                if current_candidate_rank_tuple > best_rank_tuple_for_split:
                    best_rank_tuple_for_split = current_candidate_rank_tuple
                    max_overall_mex_val = current_mex_val
                    best_next_idx_for_i = next_segment_start_idx
            
            # Store the best MEX value and the corresponding next split index for `dp[i]`.
            dp_mex_value[i] = max_overall_mex_val
            dp_next_idx[i] = best_next_idx_for_i
            
            # Update `rank_values[i]` with the chosen MEX and the rank of its subsequent segment.
            rank_values[i] = (dp_mex_value[i], rank_values[dp_next_idx[i]])
        
        # Construct the final `result` array by following the `dp_next_idx` pointers
        # starting from index 0.
        result = []
        current_idx = 0
        while current_idx < n:
            result.append(dp_mex_value[current_idx])
            current_idx = dp_next_idx[current_idx]
            
        return result

