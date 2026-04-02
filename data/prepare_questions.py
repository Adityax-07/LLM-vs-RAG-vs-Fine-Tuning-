import csv
import os

questions = [
    "What is binary search?",
    "What is the time complexity of binary search?",
    "When can you use binary search?",
    "Explain bubble sort.",
    "What is the difference between stack and queue?",
    "What is LIFO?",
    "What is FIFO?",
    "Explain merge sort.",
    "What is quicksort?",
    "What is the worst case time complexity of quicksort?",
    "What is a linked list?",
    "What is the difference between array and linked list?",
    "What is a doubly linked list?",
    "What is a binary tree?",
    "What is a Binary Search Tree?",
    "What is inorder traversal?",
    "What is the difference between BFS and DFS?",
    "What is dynamic programming?",
    "What is memoization?",
    "What is the difference between memoization and tabulation?",
    "Explain the coin change problem.",
    "What is React?",
    "What are React hooks?",
    "What is useState in React?",
    "What is useEffect in React?",
    "What is a REST API?",
    "What HTTP methods does REST use?",
    "What does HTTP status code 404 mean?",
    "What does HTTP status code 200 mean?",
    "What is CSS Flexbox?",
    "What does justify-content do in Flexbox?",
    "What is a JavaScript Promise?",
    "What are the three states of a Promise?",
    "What is async/await in JavaScript?",
    "What is Promise.all()?",
    "What is insertion sort?",
    "What is heap sort?",
    "What is a graph in data structures?",
    "What is Dijkstra algorithm?",
    "What is topological sort?",
    "What is the difference between stack and heap memory?",
    "What is a circular linked list?",
    "What is an AVL tree?",
    "What is the difference between preorder and postorder traversal?",
    "What is the knapsack problem?",
    "What is the longest common subsequence?",
    "What is flex-grow in CSS?",
    "What is useContext in React?",
    "What is useRef in React?",
    "What is the difference between PUT and PATCH in REST?",
]

os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.csv")
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "question"])
    for i, q in enumerate(questions, 1):
        writer.writerow([i, q])

print(f"Created {len(questions)} questions in data/questions.csv")
