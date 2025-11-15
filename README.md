Sudoku Solver
A fast and efficient solver for classic 9x9 Sudoku puzzles.

🚀 Overview
This program takes a single-line string representation of a Sudoku puzzle and outputs the unique solution, if one exists.

💻 Usage
The solver is designed to accept an 81-character input string via the command line or a simple input method.

Input Format:
The puzzle must be an 81-character string.
Digits (1-9) represent the given clues.
Period (.) or Zero (0) represent empty cells.
The string reads the grid row-by-row, from top-left to bottom-right.

Example (AI Escargot): 1.....7.9..3..2...8..96...5....53...9...1..8...26....4..3....1..41.....7..7...3..

⚙️ Algorithm
The core logic uses a Backtracking Algorithm with Constraint Propagation (or specify your primary algorithm, e.g., Dancing Links) to recursively try numbers in empty cells while respecting Sudoku rules (unique number per row, column, and 3x3 box).

🛠️ Setup
Clone the Repository:

Bash
git clone [Your Repository URL]
Prerequisites:
[Language, e.g., Python 3.x]


👤 Author - Dimitrios Chavouzis, Will Baldwin
