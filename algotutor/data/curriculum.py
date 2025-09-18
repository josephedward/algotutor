# Sample algorithms and data structures curriculum
algorithms_curriculum = {
    "fundamentals": [
        "Big O Notation",
        "Time and Space Complexity Analysis",
        "Basic Data Structures Overview"
    ],
    "arrays_and_strings": [
        "Array Manipulation",
        "String Processing",
        "Two Pointers Technique",
        "Sliding Window Pattern"
    ],
    "hash_tables": [
        "Hash Map Usage Patterns",
        "Frequency Counting",
        "Fast Lookups and Mappings"
    ],
    "linked_lists": [
        "Singly Linked Lists",
        "Doubly Linked Lists", 
        "Cycle Detection",
        "List Reversal Patterns"
    ],
    "stacks_and_queues": [
        "LIFO and FIFO Principles",
        "Expression Evaluation",
        "Monotonic Stack",
        "BFS with Queues"
    ],
    "trees": [
        "Binary Trees",
        "Binary Search Trees",
        "Tree Traversals (Inorder, Preorder, Postorder)",
        "Level Order Traversal",
        "Tree Construction Problems"
    ],
    "graphs": [
        "Graph Representations",
        "Depth-First Search (DFS)",
        "Breadth-First Search (BFS)",
        "Topological Sort",
        "Union-Find"
    ],
    "dynamic_programming": [
        "Memoization vs Tabulation",
        "1D Dynamic Programming",
        "2D Dynamic Programming",
        "Common DP Patterns"
    ],
    "sorting_and_searching": [
        "Binary Search",
        "Quick Sort",
        "Merge Sort",
        "Custom Comparators"
    ],
    "advanced_patterns": [
        "Backtracking",
        "Greedy Algorithms",
        "Divide and Conquer",
        "Sliding Window Maximum"
    ]
}

# Sample problem patterns and their characteristics
algorithm_patterns = {
    "two_pointer": {
        "description": "Use two pointers moving towards each other or in same direction",
        "when_to_use": "Sorted arrays, palindromes, finding pairs",
        "complexity": "Usually O(n) time, O(1) space",
        "examples": ["Two Sum II", "Valid Palindrome", "Container With Most Water"]
    },
    "sliding_window": {
        "description": "Maintain a window of elements and slide it across the data",
        "when_to_use": "Contiguous subarrays, substring problems",
        "complexity": "Usually O(n) time, O(k) space where k is window size",
        "examples": ["Longest Substring Without Repeating Characters", "Minimum Window Substring"]
    },
    "binary_search": {
        "description": "Divide search space in half repeatedly",
        "when_to_use": "Sorted data, finding peak/valley, search in rotated arrays",
        "complexity": "O(log n) time, O(1) space",
        "examples": ["Search in Rotated Sorted Array", "Find Peak Element"]
    },
    "dynamic_programming": {
        "description": "Break problems into subproblems and store solutions",
        "when_to_use": "Optimization problems, counting problems, decision problems",
        "complexity": "Varies, often O(n²) time and space",
        "examples": ["Longest Common Subsequence", "Coin Change", "House Robber"]
    },
    "backtracking": {
        "description": "Try all possibilities and backtrack on invalid paths",
        "when_to_use": "Finding all solutions, constraint satisfaction",
        "complexity": "Exponential in worst case",
        "examples": ["N-Queens", "Sudoku Solver", "Word Search"]
    }
}

