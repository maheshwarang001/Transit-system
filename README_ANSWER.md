# Mass Transit Billing System

## Overview

This system calculates the total billing for users in a mass transit network based on journey data, applying daily and monthly caps to ensure charges do not exceed specified limits. It also manages penalties for incomplete journeys.

## Assumptions & Constraints

- **Journey Data Volume**: Up to \(10^6\) journeys.
- **Unique Users**: Up to \(10^8\) users.
- **Stations & Zones**: Up to \(10^6\) stations.
- **Journey Completion**: All journeys are completed before midnight (00:00).
- **Active Journeys**: Only one active journey per user at any time.
- **Penalties**: Missing entry or exit results in a £5 penalty.
- **Data Accuracy**: Zone and station mappings are accurate and complete.
- **Input Sorting**: Input files are sorted by timestamp but not by user ID.

## Thinking & Implementation

1. **Data Handling**:
    - **Thought Process**: Given that journey data is sorted by timestamp, it reduces the complexity of processing journeys as they are handled in chronological order. This allows for a single pass through the data with state tracking.
    - **Implementation**: Implemented a linear scan of the journey data while maintaining maps for active journeys, user caps, and penalties.

2. **Journey Management**:
    - **Thought Process**: Each journey must be paired with an exit. By tracking the most recent entry for each user, we can efficiently determine if a journey is valid or needs a penalty.
    - **Implementation**: Utilized a map to track active journeys and detect missing entries or exits. Applied a £5 penalty for invalid journeys, and ensured each journey is validated before processing.

3. **Cap Management**:
    - **Thought Process**: To enforce daily and monthly caps, Needed to track expenses separately for each user and adjust charges as they approach the cap limits.
    - **Implementation**: Maintained separate maps for daily and monthly expenses. Applied caps dynamically during the processing of each journey, ensuring no user exceeds the set limits.

4. **Finalization**:
    - **Thought Process**: After processing all journeys, any remaining active journeys should be addressed. The results must be sorted to meet the output requirements.
    - **Implementation**: Processed any unclosed journeys, applied penalties, and sorted the final billing results by user ID before writing to the output file.

## Time Complexity

- **Best Case**:
    - Linear scan through all transactions: \(O(N)\)
    - Identifying pending journeys: \(O(K)\), where \(K\) is the number of users
    - Sorting users: \(O(N \log N)\) , based on Alpha Numerical string

- **Worst Case**:
    - Linear scan through all transactions: \(O(N)\)
    - Identifying pending journeys: \(O(N)\) (if all journeys are active)
    - Sorting users: \(O(N \log N)\)

## Space Complexity

- **Transaction Storage**: \(O(N)\)
- **User Caps Storage**: \(O(2K)\), where \(K\) is the number of users

## To Run
### copy
```bash
python3 main.py  "zone_map.csv" "journey_data.csv" "output.csv"
