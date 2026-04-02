import os

docs = {
    "binary_search.txt": """Binary Search is an efficient algorithm for finding an item in a sorted list.
It works by repeatedly dividing the search interval in half.
Time Complexity: O(log n). Space Complexity: O(1).
Steps:
1) Find the middle element.
2) If target equals middle, return index.
3) If target < middle, search left half.
4) Else search right half.
Requires the array to be sorted before searching.
Best case: O(1) when middle element is the target.
""",

    "stack_queue.txt": """Stack is a linear data structure following LIFO (Last In First Out) principle.
Operations: push() adds element, pop() removes top element, peek() views top.
All stack operations run in O(1) time.
Use stack for: undo operations, expression evaluation, function call stack, DFS traversal.

Queue follows FIFO (First In First Out) principle.
Operations: enqueue() adds to rear, dequeue() removes from front.
All queue operations run in O(1) time.
Use queue for: BFS traversal, scheduling, print spooler, task queues.

Key difference: Stack removes most recently added item; Queue removes oldest item.
""",

    "sorting_algorithms.txt": """Bubble Sort: repeatedly swaps adjacent elements if out of order.
Time: O(n^2) average and worst. Space: O(1). Stable sort.

Merge Sort: divide array in half, sort each half recursively, merge results.
Time: O(n log n) all cases. Space: O(n). Stable sort. Best for linked lists.

Quick Sort: picks a pivot element, partitions array around it, recursively sorts partitions.
Time: O(n log n) average, O(n^2) worst case. Space: O(log n). Not stable.

Insertion Sort: builds sorted array one element at a time by inserting each into correct position.
Time: O(n^2) worst, O(n) best. Space: O(1). Good for small or nearly sorted arrays.

Heap Sort: builds a max-heap, repeatedly extracts maximum element.
Time: O(n log n). Space: O(1). Not stable.
""",

    "linked_list.txt": """Linked List is a linear data structure where elements are stored in nodes.
Each node contains: data field + pointer to next node.

Types:
- Singly Linked List: each node points to next node only.
- Doubly Linked List: each node has pointers to both next and previous nodes.
- Circular Linked List: last node points back to first node.

Advantages over arrays: dynamic size, O(1) insertion/deletion at head.
Disadvantages: no random access (must traverse), extra memory for pointers.

Operations: Insert at head O(1), Search O(n), Delete O(n), Access by index O(n).
""",

    "trees.txt": """Binary Tree: each node has at most 2 children called left and right child.
Root is the topmost node. Leaf nodes have no children.

Binary Search Tree (BST): left child < parent node < right child.
Search, Insert, Delete all take O(log n) average, O(n) worst case.

Tree Traversals:
- Inorder (Left, Root, Right): gives sorted order for BST.
- Preorder (Root, Left, Right): used to copy tree.
- Postorder (Left, Right, Root): used to delete tree.
- Level Order: BFS traversal level by level.

Height of tree: number of edges on longest path from root to leaf.
Balanced BST examples: AVL Tree, Red-Black Tree — guarantee O(log n) operations.
""",

    "dynamic_programming.txt": """Dynamic Programming (DP) solves problems by breaking into overlapping subproblems.
Stores results of subproblems to avoid recomputation (memoization).

Key properties required:
1. Optimal substructure: optimal solution built from optimal subproblem solutions.
2. Overlapping subproblems: same subproblems solved multiple times.

Approaches:
- Top-down (Memoization): recursion + cache results in a table.
- Bottom-up (Tabulation): fill table iteratively from smallest subproblems.

Classic DP problems:
- Fibonacci: O(2^n) naive → O(n) with DP.
- 0/1 Knapsack: maximize value within weight limit.
- Longest Common Subsequence (LCS).
- Coin Change: minimum coins to make a sum.
- Longest Increasing Subsequence.
""",

    "react_hooks.txt": """React Hooks are functions that let you use state and lifecycle features in functional components.
Introduced in React 16.8 to replace class components.

useState: manages local component state.
Syntax: const [state, setState] = useState(initialValue)
Example: const [count, setCount] = useState(0)

useEffect: handles side effects like API calls, subscriptions, DOM updates.
Runs after every render by default.
Syntax: useEffect(() => { /* effect */ }, [dependencies])
Empty dependency array [] means run only once on mount.

useContext: consume React context without wrapping in Consumer component.
Syntax: const value = useContext(MyContext)

useRef: holds mutable value that does not trigger re-render. Also used to access DOM elements.

Rules of Hooks:
1. Only call hooks at the top level (not inside loops or conditions).
2. Only call hooks from React function components or custom hooks.
""",

    "rest_api.txt": """REST API (Representational State Transfer) is an architectural style for web services.
REST uses standard HTTP methods to perform operations on resources.

HTTP Methods:
- GET: retrieve/read resource. No request body.
- POST: create new resource. Data sent in request body.
- PUT: update existing resource completely.
- PATCH: partially update a resource.
- DELETE: remove a resource.

HTTP Status Codes:
- 200 OK: request succeeded.
- 201 Created: new resource created successfully.
- 400 Bad Request: invalid request from client.
- 401 Unauthorized: authentication required.
- 403 Forbidden: authenticated but not authorized.
- 404 Not Found: resource does not exist.
- 500 Internal Server Error: server-side error.

REST principles: Stateless, Client-Server, Cacheable, Uniform Interface.
JSON is the most common data format for REST API responses.
""",

    "css_flexbox.txt": """CSS Flexbox (Flexible Box Layout) is a layout model for arranging items in a container.
Activated by setting display: flex on a container element.

Container properties:
- flex-direction: row (default, horizontal) or column (vertical).
- justify-content: aligns items on main axis. Values: flex-start, flex-end, center, space-between, space-around.
- align-items: aligns items on cross axis. Values: stretch (default), flex-start, flex-end, center.
- flex-wrap: nowrap (default) or wrap to allow items to move to next line.
- gap: space between flex items.

Item properties:
- flex-grow: how much item grows relative to siblings. 0 means no grow.
- flex-shrink: how much item shrinks when space is limited.
- flex-basis: initial size of item before flex calculations.
- align-self: overrides align-items for a single item.

Shorthand: flex: grow shrink basis (e.g., flex: 1 1 auto)
""",

    "javascript_promises.txt": """JavaScript Promises handle asynchronous operations in a cleaner way than callbacks.

Promise States:
- Pending: initial state, operation not complete.
- Fulfilled: operation completed successfully.
- Rejected: operation failed.

Creating a Promise:
const myPromise = new Promise((resolve, reject) => {
  if (success) resolve(result);
  else reject(error);
});

Consuming a Promise:
myPromise
  .then(result => console.log(result))
  .catch(error => console.error(error))
  .finally(() => console.log('always runs'));

async/await syntax (ES2017) is syntactic sugar over promises:
async function fetchData() {
  try {
    const data = await fetch(url);
    const json = await data.json();
    return json;
  } catch (error) {
    console.error(error);
  }
}

Promise utility methods:
- Promise.all([p1, p2]): runs in parallel, resolves when all resolve.
- Promise.race([p1, p2]): resolves/rejects with first settled promise.
- Promise.allSettled(): waits for all, returns all results regardless of success/failure.
""",

    "graph_algorithms.txt": """Graph is a data structure with nodes (vertices) connected by edges.
Types: Directed/Undirected, Weighted/Unweighted, Cyclic/Acyclic.

Representations:
- Adjacency Matrix: 2D array. O(1) edge lookup, O(V^2) space.
- Adjacency List: array of lists. O(V+E) space. Better for sparse graphs.

BFS (Breadth-First Search):
Explores level by level using a queue. Time: O(V+E).
Used for: shortest path in unweighted graph, level-order traversal.

DFS (Depth-First Search):
Explores as far as possible using stack/recursion. Time: O(V+E).
Used for: cycle detection, topological sort, connected components.

Dijkstra's Algorithm: shortest path in weighted graph with non-negative edges.
Time: O((V+E) log V) with priority queue.

Topological Sort: linear ordering of vertices where each directed edge u→v means u comes before v.
Only valid for Directed Acyclic Graphs (DAGs).
"""
}

os.makedirs("docs", exist_ok=True)
for filename, content in docs.items():
    with open(f"docs/{filename}", "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Created {len(docs)} documents in docs/")
