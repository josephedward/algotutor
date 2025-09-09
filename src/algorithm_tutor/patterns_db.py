"""
Core pattern database containing the essential algorithmic patterns.
Based on patterns that cover 80%+ of interview questions.
"""

from typing import List

from .pattern import Difficulty, Pattern, PatternCategory, Problem


def get_core_patterns() -> List[Pattern]:
    """Get the 15-20 core algorithmic patterns for interview preparation."""
    patterns = []

    # 1. Two Pointers
    patterns.append(
        Pattern(
            name="Two Pointers",
            category=PatternCategory.TWO_POINTERS,
            description="Use two pointers moving towards each other or in same direction",
            key_concepts=[
                "Opposite direction pointers",
                "Same direction pointers",
                "Fast/slow pointers",
            ],
            time_complexity_notes="Usually O(n) instead of O(n²) brute force",
            space_complexity_notes="O(1) space complexity",
            when_to_use="Array/string problems with pairs, palindromes, or sorted data",
            problems=[
                Problem(
                    name="Two Sum II",
                    description="Find two numbers that add up to target in sorted array",
                    difficulty=Difficulty.EASY,
                    key_insights=[
                        "Sorted array allows two pointers",
                        "Move pointers based on sum comparison",
                    ],
                ),
                Problem(
                    name="3Sum",
                    description="Find all unique triplets that sum to zero",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Fix one number, use two pointers for remaining",
                        "Skip duplicates",
                    ],
                ),
            ],
        )
    )

    # 2. Sliding Window
    patterns.append(
        Pattern(
            name="Sliding Window",
            category=PatternCategory.SLIDING_WINDOW,
            description="Maintain a window over array/string and slide it to find optimal solutions",
            key_concepts=[
                "Fixed size window",
                "Dynamic size window",
                "Window expansion/contraction",
            ],
            time_complexity_notes="O(n) instead of O(n²) or O(n³)",
            space_complexity_notes="O(1) or O(k) where k is window size",
            when_to_use="Substring/subarray problems with constraints",
            problems=[
                Problem(
                    name="Maximum Subarray Sum of Size K",
                    description="Find maximum sum of any subarray of size k",
                    difficulty=Difficulty.EASY,
                    key_insights=["Slide window and update sum incrementally"],
                ),
                Problem(
                    name="Longest Substring Without Repeating Characters",
                    description="Find length of longest substring without repeating characters",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Expand window until duplicate, then contract from left"
                    ],
                ),
            ],
        )
    )

    # 3. Fast & Slow Pointers (Floyd's Cycle Detection)
    patterns.append(
        Pattern(
            name="Fast & Slow Pointers",
            category=PatternCategory.LINKED_LISTS,
            description="Use two pointers at different speeds to detect patterns",
            key_concepts=["Cycle detection", "Finding middle", "Palindrome check"],
            time_complexity_notes="O(n) with single pass",
            space_complexity_notes="O(1) space",
            when_to_use="Linked list cycles, finding middle, cycle length",
            problems=[
                Problem(
                    name="Linked List Cycle",
                    description="Detect if linked list has a cycle",
                    difficulty=Difficulty.EASY,
                    key_insights=[
                        "Fast pointer moves 2 steps, slow moves 1",
                        "They meet if cycle exists",
                    ],
                ),
                Problem(
                    name="Find Middle of Linked List",
                    description="Find middle node of linked list",
                    difficulty=Difficulty.EASY,
                    key_insights=["When fast reaches end, slow is at middle"],
                ),
            ],
        )
    )

    # 4. Merge Intervals
    patterns.append(
        Pattern(
            name="Merge Intervals",
            category=PatternCategory.INTERVALS,
            description="Deal with overlapping intervals efficiently",
            key_concepts=[
                "Sort by start time",
                "Merge overlapping",
                "Insert intervals",
            ],
            time_complexity_notes="O(n log n) due to sorting",
            space_complexity_notes="O(1) or O(n) for result",
            when_to_use="Scheduling, time intervals, range problems",
            problems=[
                Problem(
                    name="Merge Intervals",
                    description="Merge overlapping intervals",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=["Sort intervals", "Merge when overlap detected"],
                ),
                Problem(
                    name="Insert Interval",
                    description="Insert interval and merge if necessary",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Find position to insert",
                        "Merge left and right overlaps",
                    ],
                ),
            ],
        )
    )

    # 5. Cyclic Sort
    patterns.append(
        Pattern(
            name="Cyclic Sort",
            category=PatternCategory.ARRAYS,
            description="Sort arrays containing numbers in given range by placing each number at its correct index",
            key_concepts=[
                "Place number at index number-1",
                "Handle missing numbers",
                "Find duplicates",
            ],
            time_complexity_notes="O(n) for numbers in range [1, n]",
            space_complexity_notes="O(1) space",
            when_to_use="Arrays with numbers in specific range, finding missing/duplicate numbers",
            problems=[
                Problem(
                    name="Find Missing Number",
                    description="Find missing number in array containing n distinct numbers from 0 to n",
                    difficulty=Difficulty.EASY,
                    key_insights=[
                        "Place each number at correct position",
                        "Missing number's position will be empty",
                    ],
                ),
                Problem(
                    name="Find All Duplicates",
                    description="Find all duplicates in array where elements are in range [1, n]",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=["Use array positions to mark seen numbers"],
                ),
            ],
        )
    )

    # 6. In-place Reversal of LinkedList
    patterns.append(
        Pattern(
            name="In-place LinkedList Reversal",
            category=PatternCategory.LINKED_LISTS,
            description="Reverse parts of linked list without extra memory",
            key_concepts=[
                "Reverse entire list",
                "Reverse sublist",
                "Reverse in groups",
            ],
            time_complexity_notes="O(n)",
            space_complexity_notes="O(1) space",
            when_to_use="LinkedList modification problems",
            problems=[
                Problem(
                    name="Reverse LinkedList",
                    description="Reverse entire linked list",
                    difficulty=Difficulty.EASY,
                    key_insights=["Use three pointers: prev, current, next"],
                ),
                Problem(
                    name="Reverse Sublist",
                    description="Reverse linked list from position m to n",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Find start position",
                        "Reverse portion",
                        "Connect ends",
                    ],
                ),
            ],
        )
    )

    # 7. Tree BFS
    patterns.append(
        Pattern(
            name="Tree Breadth First Search",
            category=PatternCategory.TREES,
            description="Traverse tree level by level using queue",
            key_concepts=[
                "Level order traversal",
                "Level-wise processing",
                "Queue-based traversal",
            ],
            time_complexity_notes="O(n) where n is number of nodes",
            space_complexity_notes="O(w) where w is maximum width",
            when_to_use="Level order traversal, finding level-wise properties",
            problems=[
                Problem(
                    name="Binary Tree Level Order Traversal",
                    description="Return level order traversal as list of lists",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=["Use queue", "Process level by level"],
                ),
                Problem(
                    name="Binary Tree Zigzag Traversal",
                    description="Return zigzag level order traversal",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Alternate direction for each level",
                        "Use deque or reverse alternate levels",
                    ],
                ),
            ],
        )
    )

    # 8. Tree DFS
    patterns.append(
        Pattern(
            name="Tree Depth First Search",
            category=PatternCategory.TREES,
            description="Traverse tree using recursion or stack",
            key_concepts=[
                "Preorder, inorder, postorder",
                "Path finding",
                "Tree properties",
            ],
            time_complexity_notes="O(n) where n is number of nodes",
            space_complexity_notes="O(h) where h is height (recursion stack)",
            when_to_use="Path problems, tree validation, tree properties",
            problems=[
                Problem(
                    name="Path Sum",
                    description="Check if tree has path with given sum",
                    difficulty=Difficulty.EASY,
                    key_insights=[
                        "Subtract current value from sum",
                        "Check if leaf node",
                    ],
                ),
                Problem(
                    name="All Paths to Target Sum",
                    description="Find all paths that sum to target",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Backtrack to explore all paths",
                        "Use list to store current path",
                    ],
                ),
            ],
        )
    )

    # 9. Binary Search
    patterns.append(
        Pattern(
            name="Modified Binary Search",
            category=PatternCategory.BINARY_SEARCH,
            description="Apply binary search on sorted arrays with modifications",
            key_concepts=[
                "Search in rotated array",
                "Find peak element",
                "Search range",
            ],
            time_complexity_notes="O(log n)",
            space_complexity_notes="O(1)",
            when_to_use="Sorted arrays with modifications, finding elements/ranges",
            problems=[
                Problem(
                    name="Search in Rotated Array",
                    description="Search target in rotated sorted array",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "One half is always sorted",
                        "Determine which half to search",
                    ],
                ),
                Problem(
                    name="Find Peak Element",
                    description="Find peak element in array",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Move towards higher neighbor",
                        "Always guaranteed to find peak",
                    ],
                ),
            ],
        )
    )

    # 10. Top K Elements
    patterns.append(
        Pattern(
            name="Top K Elements",
            category=PatternCategory.HEAP,
            description="Find top K elements using heap data structure",
            key_concepts=[
                "Min heap for top K",
                "Max heap for bottom K",
                "Heap size management",
            ],
            time_complexity_notes="O(n log k) for top K",
            space_complexity_notes="O(k) for heap storage",
            when_to_use="Finding largest/smallest K elements, K closest elements",
            problems=[
                Problem(
                    name="Kth Largest Element",
                    description="Find kth largest element in array",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=["Use min heap of size K", "Maintain heap invariant"],
                ),
                Problem(
                    name="Top K Frequent Elements",
                    description="Find k most frequent elements",
                    difficulty=Difficulty.MEDIUM,
                    key_insights=[
                        "Count frequency",
                        "Use heap to get top K by frequency",
                    ],
                ),
            ],
        )
    )

    return patterns


def get_pattern_by_name(name: str) -> Pattern:
    """Get specific pattern by name."""
    patterns = get_core_patterns()
    for pattern in patterns:
        if pattern.name.lower() == name.lower():
            return pattern
    raise ValueError(f"Pattern '{name}' not found")


def get_patterns_by_category(category: PatternCategory) -> List[Pattern]:
    """Get all patterns in a specific category."""
    patterns = get_core_patterns()
    return [p for p in patterns if p.category == category]
