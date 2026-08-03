"""
Design Ride Sharing System
Difficulty: Medium

Description:
This system manages ride requests from riders and driver availability, matching them in the order they arrive. It supports adding riders and drivers, matching the earliest available pair, and allowing riders to cancel their requests if they haven't yet been matched.

Example:
Input:
["RideSharingSystem", "addRider", "addDriver", "addRider", "matchDriverWithRider", "addDriver", "cancelRider", "matchDriverWithRider", "matchDriverWithRider"]
[[], [3], [2], [1], [], [5], [3], [], []]

Output:
[null, null, null, null, [2, 3], null, null, [5, 1], [-1, -1]]

Approach:
The system is implemented using three core data structures to manage the state of riders and drivers efficiently. Two `collections.deque` objects, `waiting_riders` and `available_drivers`, maintain the strict First-In-First-Out (FIFO) order required for matching. A `set`, `active_riders`, is used to keep track of all riders who have requested a ride and have not yet been matched or cancelled. When `addRider` is called, the rider is appended to `waiting_riders` and added to `active_riders`. `addDriver` simply appends the driver to `available_drivers`. The `matchDriverWithRider` method iteratively dequeues riders from `waiting_riders` until an ID present in `active_riders` is found (skipping cancelled riders). If both an active rider and an available driver exist, they are matched, removed from their respective queues, and the rider is removed from `active_riders`. `cancelRider` efficiently removes a rider from `active_riders` if they are currently waiting, ensuring they will be skipped during future matching attempts.

Time Complexity:
- `__init__`: O(1)
- `addRider`: O(1) (amortized for `set.add`)
- `addDriver`: O(1)
- `matchDriverWithRider`: Amortized O(1). While a single call might iterate through 'k' cancelled riders in the worst case (O(k)), each rider is only dequeued once from `waiting_riders` over its lifetime, making the total cost amortized O(1) per match operation when considering the total work for all riders.
- `cancelRider`: O(1) (amortized for `set.remove`)

Space Complexity:
O(N + M), where N is the maximum number of concurrent waiting riders and M is the maximum number of concurrent available drivers. This is because both deques and the set store IDs. Given the constraints (max 1000 total calls and unique IDs), this is O(1000) at most.
"""
import collections
from typing import List, Optional

class RideSharingSystem:

    def __init__(self):
        """
        Initializes the system.
        Two deques are used to maintain the arrival order for riders and drivers.
        A set `active_riders` tracks riders who are currently waiting and have not been
        cancelled or matched. This allows efficient O(1) cancellation and O(1) check
        for active riders during matching, effectively skipping cancelled riders
        in the `waiting_riders` deque without iterating through it.
        """
        self.waiting_riders = collections.deque()  # Stores riderIds in arrival order
        self.available_drivers = collections.deque() # Stores driverIds in arrival order
        self.active_riders = set()  # Stores riderIds that are currently active and waiting

    def addRider(self, riderId: int) -> None:
        """
        Adds a new rider with the given riderId to the system.
        The rider is added to the waiting queue and marked as active.
        Time Complexity: O(1)
        """
        self.waiting_riders.append(riderId)
        self.active_riders.add(riderId)

    def addDriver(self, driverId: int) -> None:
        """
        Adds a new driver with the given driverId to the system.
        The driver is added to the available drivers queue.
        Time Complexity: O(1)
        """
        self.available_drivers.append(driverId)

    def matchDriverWithRider(self) -> List[int]:
        """
        Matches the earliest available driver with the earliest waiting active rider.
        Cancelled riders are skipped from the front of the rider queue until an
        active one is found. If a match is made, both are removed from their
        respective queues and the active_riders set.
        Time Complexity: Amortized O(1). In the worst case of many cancelled riders
                         at the front of the queue, it could be O(k) for k skips,
                         but each rider is processed from the deque only once.
        """
        matched_rider_id = -1

        # Find the earliest active rider
        while self.waiting_riders:
            potential_rider_id = self.waiting_riders[0] # Peek at the earliest rider
            if potential_rider_id in self.active_riders:
                # Found an active rider, pop them from the deque and mark as matched
                matched_rider_id = self.waiting_riders.popleft()
                self.active_riders.remove(matched_rider_id)
                break
            else:
                # This rider was cancelled, remove from deque and continue searching
                self.waiting_riders.popleft()

        # Check if an active rider and an available driver both exist
        if matched_rider_id == -1 or not self.available_drivers:
            return [-1, -1]
        
        # Both an active rider and an available driver are found
        driver_id = self.available_drivers.popleft()
        return [driver_id, matched_rider_id]

    def cancelRider(self, riderId: int) -> None:
        """
        Cancels the ride request of the rider with the given riderId if the rider
        exists and has not yet been matched. This is done by removing the rider
        from the `active_riders` set. When `matchDriverWithRider` attempts to
        process this rider later, it will be skipped.
        Time Complexity: O(1) (average for set operations)
        """
        if riderId in self.active_riders:
            self.active_riders.remove(riderId)

if __name__ == "__main__":
    # Example 1 test
    rideSharingSystem = RideSharingSystem()
    assert rideSharingSystem.addRider(3) is None
    assert rideSharingSystem.addDriver(2) is None
    assert rideSharingSystem.addRider(1) is None
    assert rideSharingSystem.matchDriverWithRider() == [2, 3]
    assert rideSharingSystem.addDriver(5) is None
    assert rideSharingSystem.cancelRider(3) is None # rider 3 already matched, cancel has no effect
    assert rideSharingSystem.matchDriverWithRider() == [5, 1]
    assert rideSharingSystem.matchDriverWithRider() == [-1, -1]
    print("Example 1 tests passed!")

    # Example 2 test
    rideSharingSystem2 = RideSharingSystem()
    assert rideSharingSystem2.addRider(8) is None
    assert rideSharingSystem2.addDriver(8) is None
    assert rideSharingSystem2.addDriver(6) is None
    assert rideSharingSystem2.matchDriverWithRider() == [8, 8]
    assert rideSharingSystem2.addRider(2) is None
    assert rideSharingSystem2.cancelRider(2) is None # rider 2 cancels
    assert rideSharingSystem2.matchDriverWithRider() == [-1, -1]
    print("Example 2 tests passed!")

    # Additional test cases
    rideSharingSystem3 = RideSharingSystem()
    rideSharingSystem3.addRider(10)
    rideSharingSystem3.cancelRider(10) # Rider cancels before any driver available
    rideSharingSystem3.addDriver(20)
    assert rideSharingSystem3.matchDriverWithRider() == [-1, -1] # No active rider

    rideSharingSystem3.addRider(11)
    rideSharingSystem3.addDriver(21)
    assert rideSharingSystem3.matchDriverWithRider() == [21, 11]

    rideSharingSystem3.addRider(12)
    rideSharingSystem3.addRider(13)
    rideSharingSystem3.cancelRider(12) # Rider 12 cancels
    rideSharingSystem3.addDriver(22)
    assert rideSharingSystem3.matchDriverWithRider() == [22, 13] # Driver 22 matches with Rider 13, skipping 12

    print("All additional tests passed!")
    print("All tests passed!")