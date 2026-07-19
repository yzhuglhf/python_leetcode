"""
Design Event Manager
Difficulty: Medium

Description:
The EventManager class is designed to manage a collection of events, each with a unique ID and a priority. It supports initializing with a list of events, updating the priority of an existing active event, and retrieving the active event with the highest priority. When multiple events have the same highest priority, the one with the smallest eventId is chosen.

Example:
Input:
["EventManager", "pollHighest", "updatePriority", "pollHighest", "pollHighest"]
[[[[5, 7], [2, 7], [9, 4]]], [], [9, 7], [], []]

Output:
[null, 2, null, 5, 9]

Approach:
This problem is efficiently solved using a combination of a min-heap and a hash map. A min-heap (`self.heap`) stores tuples `(-priority, eventId)`. Storing negative priority effectively makes it a max-heap for priority. The natural min-heap comparison for `eventId` (when negative priorities are equal) handles ties by picking the smallest ID, satisfying the problem's tie-breaking rule. A dictionary (`self.event_info`) maps `eventId` to its current `priority` for all actively managed events. `updatePriority` employs a "lazy deletion" strategy: it updates the `event_info` dictionary with the new priority for `eventId` and then pushes a new `(-newPriority, eventId)` tuple onto the heap. The old heap entry for the same `eventId` with its previous priority is now "stale" but remains in the heap. `pollHighest` repeatedly extracts entries from the heap. For each extracted entry, it checks if the `eventId` is still active (present in `self.event_info`) and if its priority matches the current priority recorded in `self.event_info`. Stale entries are simply discarded. Once a valid, highest-priority active event is found, its `eventId` is returned, and it's marked as inactive by removing it from `self.event_info`.

Time Complexity: O((N + Q) log(N + Q)) where N is the number of initial events and Q is the total number of calls to `updatePriority` and `pollHighest`. Each heap operation (push or pop) takes O(log K) time, where K is the current size of the heap. The maximum size of the heap is bounded by N (initial events) + Q (updates). Dictionary operations (lookup, insert, delete) are O(1) on average.
Space Complexity: O(N + Q) for storing all entries in the heap (including stale ones). The `self.event_info` dictionary stores only active events, bounded by N, so the overall space complexity is dominated by the heap.
"""
import heapq
from typing import List, Dict

class EventManager:

    def __init__(self, events: List[List[int]]):
        """
        Initializes the EventManager with a list of events.
        Each event is represented as [eventId, priority].
        
        We use a min-heap to store events. To prioritize highest priority and then smallest eventId,
        we store tuples of (-priority, eventId).
        The negative priority makes the min-heap behave like a max-heap for priority.
        If priorities are equal (negative priorities are equal), the min-heap naturally
        picks the smaller eventId, satisfying the tie-breaking rule.
        
        We also maintain a dictionary `event_info` to quickly get the current priority
        of an active event and to detect stale entries in the heap (due to priority updates or polling).
        `event_info`: eventId -> current_priority
        """
        self.heap: List[tuple[int, int]] = []  # Stores (-priority, eventId)
        self.event_info: Dict[int, int] = {}  # Stores eventId -> current_priority for active events

        for event_id, priority in events:
            heapq.heappush(self.heap, (-priority, event_id))
            self.event_info[event_id] = priority

    def updatePriority(self, eventId: int, newPriority: int) -> None:
        """
        Updates the priority of an active event.
        
        This uses a "lazy deletion" strategy:
        1. Update the `event_info` dictionary with the new priority for `eventId`.
        2. Push a new entry (-newPriority, eventId) into the heap.
           The old entry for `eventId` with its previous priority remains in the heap,
           but it will be recognized as stale by `pollHighest` and discarded.
        """
        # Update the current priority in our active events dictionary
        self.event_info[eventId] = newPriority
        # Push the new priority to the heap. The old entry will be ignored by pollHighest.
        heapq.heappush(self.heap, (-newPriority, eventId))

    def pollHighest(self) -> int:
        """
        Removes and returns the eventId of the active event with the highest priority.
        If multiple events have the same highest priority, the one with the smallest eventId is returned.
        Returns -1 if no active events exist.
        """
        while self.heap:
            neg_priority, event_id = heapq.heappop(self.heap)
            priority_from_heap = -neg_priority

            # Check if this event_id is still active and if this heap entry is its most recent priority.
            if event_id in self.event_info and self.event_info[event_id] == priority_from_heap:
                # This is a valid, active event with its correct current priority.
                # Mark it as inactive by removing from event_info.
                del self.event_info[event_id]
                return event_id
            # Else, this entry is stale (either priority was updated or it was already polled).
            # Discard it and continue to the next item in the heap.
        
        # If the heap is empty and no valid event was found, no active events remain.
        return -1


if __name__ == "__main__":
    # Example 1
    eventManager1 = EventManager([[5, 7], [2, 7], [9, 4]])
    assert eventManager1.pollHighest() == 2, "Example 1 Test 1 Failed"
    eventManager1.updatePriority(9, 7)
    assert eventManager1.pollHighest() == 5, "Example 1 Test 2 Failed"
    assert eventManager1.pollHighest() == 9, "Example 1 Test 3 Failed"
    assert eventManager1.pollHighest() == -1, "Example 1 Test 4 Failed (no events left)"

    # Example 2
    eventManager2 = EventManager([[4, 1], [7, 2]])
    assert eventManager2.pollHighest() == 7, "Example 2 Test 1 Failed"
    assert eventManager2.pollHighest() == 4, "Example 2 Test 2 Failed"
    assert eventManager2.pollHighest() == -1, "Example 2 Test 3 Failed (no events left)"

    # Custom Test: Multiple updates for the same eventId
    eventManager3 = EventManager([[1, 10], [2, 5]])
    assert eventManager3.pollHighest() == 1, "Custom Test 1 Failed (initial poll)" 
    eventManager3.updatePriority(2, 12) # Event 2 priority updated to 12 (highest so far)
    eventManager3.updatePriority(2, 8)  # Event 2 priority updated again to 8. The 12-priority entry is now stale.
    assert eventManager3.pollHighest() == 2, "Custom Test 2 Failed (poll after multiple updates)" # Should return 2 with current priority 8
    assert eventManager3.pollHighest() == -1, "Custom Test 3 Failed (no events left)"

    # Custom Test: All same priority, check tie-breaking
    eventManager4 = EventManager([[10, 5], [20, 5], [5, 5]])
    assert eventManager4.pollHighest() == 5, "Custom Test 4 Failed (tie-breaking, smallest ID)"
    assert eventManager4.pollHighest() == 10, "Custom Test 5 Failed (tie-breaking, next smallest ID)"
    assert eventManager4.pollHighest() == 20, "Custom Test 6 Failed (tie-breaking, last ID)"
    assert eventManager4.pollHighest() == -1, "Custom Test 7 Failed (no events left)"
    
    # Custom Test: Empty initial events
    eventManager5 = EventManager([])
    assert eventManager5.pollHighest() == -1, "Custom Test 8 Failed (empty init)"
    eventManager5.updatePriority(1, 10) # This should not happen per constraints (eventId refers to active event)
                                        # But if it did, it would add to event_info, but pollHighest wouldn't find it if no previous entries.
                                        # Let's add an active event first.
    
    print("All tests passed!")

