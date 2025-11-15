"""
    Program to efficiently represent and solve a Sudoku puzzle
    
    Authors: Dimitrios Chavouzis, Will Baldwin
"""

from random import randrange
import time
from collections import Counter
import sys

# Increase recursion limit for deep backtracking puzzles
sys.setrecursionlimit(2000)

"""
Cell object that represents each square in a Sudoku puzzle
"""

class Cell:

    def __init__(self, id):
        self.id = id
        self.cur_val = 0 # 0 for unassigned
        self.values = list(range(1, 10)) # Domain (possible values)
        self.neighbors = []
        self.assigned_neigh = 0 # Counter for degree heuristic

    def add_value(self, number):
        self.values.append(number)

    def get_values(self):
        return self.values

    def set_current(self, number):
        self.cur_val = number
        
"""
=============================================================================
"""

"""
Board object that represents a Sudoku puzzle. It includes cells and various functions.
"""

class Board:

    def __init__(self):
        # Initializing the 9x9 board with unique IDs for cell tracking (Box, Row, Col)
        rows = []
        
        row_1 = [Cell("A11"), Cell("A12") , Cell("A13") , Cell("B14"), Cell("B15"), Cell("B16"), Cell("C17"), Cell("C18"), Cell("C19")]
        rows.append(row_1)
        
        row_2 = [Cell("A21"), Cell("A22") , Cell("A23") , Cell("B24"), Cell("B25"), Cell("B26"), Cell("C27"), Cell("C28"), Cell("C29")]
        rows.append(row_2)

        row_3 = [Cell("A31"), Cell("A32") , Cell("A33") , Cell("B34"), Cell("B35"), Cell("B36"), Cell("C37"), Cell("C38"), Cell("C39")]
        rows.append(row_3)
        
        row_4 = [Cell("D41"), Cell("D42") , Cell("D43") , Cell("E44"), Cell("E45"), Cell("E46"), Cell("F47"), Cell("F48"), Cell("F49")]
        rows.append(row_4)

        row_5 = [Cell("D51"), Cell("D52") , Cell("D53") , Cell("E54"), Cell("E55"), Cell("E56"), Cell("F57"), Cell("F58"), Cell("F59")]
        rows.append(row_5)
        
        row_6 = [Cell("D61"), Cell("D62") , Cell("D63") , Cell("E64"), Cell("E65"), Cell("E66"), Cell("F67"), Cell("F68"), Cell("F69")]
        rows.append(row_6)

        row_7 = [Cell("G71"), Cell("G72") , Cell("G73") , Cell("H74"), Cell("H75"), Cell("H76"), Cell("I77"), Cell("I78"), Cell("I79")]
        rows.append(row_7)
        
        row_8 = [Cell("G81"), Cell("G82") , Cell("G83") , Cell("H84"), Cell("H85"), Cell("H86"), Cell("I87"), Cell("I88"), Cell("I89")]
        rows.append(row_8)

        row_9 = [Cell("G91"), Cell("G92") , Cell("G93") , Cell("H94"), Cell("H95"), Cell("H96"), Cell("I97"), Cell("I98"), Cell("I99")]
        rows.append(row_9)
       
        self.board = [[y for y in row] for row in rows]

    def __len__(self):
        return 9

    def __getitem__(self, tup):
        y, x = tup
        y = int(y)
        x = int(x)
        return self.board[y][x]
    
    """
    Fills the board with the initial given clues
    """
    def fill_initial_board(self, str_board):
        count = 0
        for c in str_board:
            row = count // 9
            col = count % 9
            if(c != "."):
                # Initial assignment (a clue)
                self[row,col].set_current(int(c)) 
            count = count + 1
        return self

    """
    Assigns neighbors to each cell in our Board object (Row, Column, and 3x3 Box constraints)
    """
    def find_neighbors(self , box , row , col):
        neighbors = []
        assigned = 0
        
        for i in range(len(self)):
            for j in range(len(self)):
                cell = self.board[i][j]
                
                # Exclude the cell itself
                if cell.id[1] == row and cell.id[2] == col:
                    continue 

                # Check if it's in the same box, row, or column
                if (cell.id[0] == box or cell.id[1] == row or cell.id[2] == col):
                    if (cell.cur_val != 0):
                        assigned += 1
                    neighbors.append(cell)
        
        r = int(row) - 1
        c = int(col) - 1
  
        self[r,c].neighbors = neighbors
        self[r,c].assigned_neigh = assigned # Used by the Degree Heuristic

        return neighbors

    """
    Forward Check: Updates a cell's domain based on its currently assigned neighbors.
    This is used for initial domain setup and simple forward checking in backtracking.
    """
    def initial_values(self, neighbors, cell):
        all_poss = set(range(1, 10))
        
        # Remove values used by assigned neighbors
        for neighbor in neighbors:
            val = neighbor.cur_val
            if val != 0 and val in all_poss:
                all_poss.remove(val)
            
        # The cell's domain is updated
        cell.values = list(all_poss)
        return cell.values
    
    """
    Check if board is solved
    """
    def board_is_solved(self):
        for i in range(len(self)):
            for j in range(len(self)):
                if (self[i,j].cur_val == 0 ):
                    return False
        return True
    
    """
    Backtracking to solve a given sudoku puzzle. Implements MRV, Degree, and LCV.
    The pcell argument is kept for compatibility with the original signature but is unused.
    """
    def backtrack_with_min_val(self, pcell=None):
        # Base Case: All cells are assigned
        if (self.board_is_solved()):
            return True

        # Variable Ordering: Find the cell with the fewest possible values (MRV + Degree)
        min_cell = self.find_less_poss()

        # Update the domain of the selected cell based on fixed constraints (Forward Check)
        self.initial_values(min_cell.neighbors, min_cell) 
        
        # If the domain is empty, backtrack immediately
        if not min_cell.values:
            return False

        # Value Ordering: Least Constraining Value (LCV) heuristic
        ordered_values = min_cell.values
        if len(min_cell.values) > 1:
            # LCV returns an ordered list of values to try
            ordered_values = least_constr_val(min_cell)

        # Loop through ordered values
        for i in ordered_values:
            # Check for conflict with ALREADY assigned neighbors (is_allowed check is now redundant 
            # if initial_values worked, but kept for robustness/legacy)
            if is_allowed(min_cell, i): 
                
                # 1. Assignment
                min_cell.set_current(int(i))
                
                # 2. Recursive Call
                sol = self.backtrack_with_min_val(min_cell)

                if (sol):
                    return sol
                
        # 3. Backtrack: Un-assign the value
        min_cell.set_current(0)
        return False
    
    """
    Degree heuristic - breaks ties in MRV by picking cell with the FEWEST *assigned* neighbors.
    (Note: The standard degree heuristic prioritizes the most *unassigned* neighbors to maximize future pruning.)
    """
    def degree(self, min_cell, other_cell):
        # Tie-breaker: choose the one with more assigned neighbors to 'force' constraint earlier.
        # This is a non-standard but functional tie-breaker.
        if (other_cell.assigned_neigh > min_cell.assigned_neigh):
            return other_cell
        return min_cell
    
    """
    MRV heuristic - finds the cell with the least available remaining values.
    Includes the call for the Degree heuristic if a tie is detected.
    """
    def find_less_poss(self): 
        min_len = 10
        min_cell = None
        
        for i in range(len(self)):
            for j in range(len(self)):
                cell = self[i,j]
                
                # Only consider unassigned cells
                if cell.cur_val == 0:
                    
                    # Ensure the domain is up to date based on assigned neighbors before checking length
                    self.initial_values(cell.neighbors, cell)
                    current_len = len(cell.values)
                    
                    if min_cell is None or current_len < min_len:
                        min_len = current_len
                        min_cell = cell
                    
                    # Degree Heuristic Tie-breaker
                    elif current_len == min_len:
                        min_cell = self.degree(min_cell, cell)
                        min_len = len(min_cell.values) # Re-fetch min_len in case degree changed the cell
                        
        return min_cell
    
    
"""
GENERAL METHODS
=================================================================================
"""

def solve_back(board):
    # Start backtracking from an arbitrary cell (the function finds the true starting MRV cell)
    return board.backtrack_with_min_val(board[0,0])

def is_allowed(cell , value):
    """
    Checks if assigning 'value' to 'cell' violates any constraints 
    with ALREADY ASSIGNED neighbors.
    """
    for i in cell.neighbors:
        if (i.cur_val == value):
            return False
    return True

"""
Least Constraining Value Heuristic - Sorts the values available according to their 
                                     the constraints they pose to other UNASSIGNED cells.
"""
def least_constr_val(cell):
    # This heuristic chooses a value that rules out the fewest options
    # for UNASSIGNED neighbors, minimizing future constraints.
    value_scores = []
    
    # 1. Score each possible value in the cell's domain
    for value in cell.values:
        constraints_imposed = 0
        
        # Check unassigned neighbors
        for neighbor in cell.neighbors:
            # We only count constraints imposed on UNASSIGNED neighbors
            if neighbor.cur_val == 0:
                # Count how many future choices (unassigned neighbors) this value constrains
                if value in neighbor.values:
                    constraints_imposed += 1
        
        # Store the value and its score (lower score is better)
        value_scores.append((value, constraints_imposed))
        
    # 2. Sort the values: least constraining values (lowest score) come first
    # This uses a tuple for sorting: (score, value)
    value_scores.sort(key=lambda x: x[1])
    
    # 3. Return only the values in the correct order
    return [val for val, score in value_scores]


def main():

    easy = []
    medium = []
    hard = []
    very_hard = []
    evil = []
    arto_inkala = []
    
    # Example Evil puzzles (from the original input)
    evil.append('.2.....7....5...4....1..........35...9..7..........1.81.5...6..4...2.......8.....')
    evil.append('1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1')
    evil.append('.......7..6..1...4..34..2..8....3.5...29..7...4..8...9.2..6...7...1..9..7....8.6.')
    evil.append('1..5..4....9.3.....7...8..5..1....3.8..6..5...9...7..8..4.2..1.2..8..6.......1..2')
    evil.append('.8......1..7..4.2.6..3..7....2..9...1...6...8.3.4.......17..6...9...8..5.......4.')
    evil.append('1..4..8...4..3...9..9..6.5..5.3..........16......7...2..4.1.9..7..8....4.2...4.8.')
    evil.append('..5..97...6.....2.1..8....6.1.7....4..7.6..3.6....32.......6.4..9..5.1..8..1....2')
    evil.append('6.....2...9...1..5..8.3..4......2..15..6..9....7.9.....7...3..2...4..5....6.7..8.')
    
    # Arto Inkala's Evil puzzles
    evil.append('8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..')
    evil.append('1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..')

    
    
    # ======================================================================
    # NOTE: The following section requires a local CSV file and is commented 
    # out to ensure the program runs without file path errors.
    # ======================================================================
    # import csv
    # try:
    #     f = open('/Users/dimitrios/Desktop/370_Final/all_sample1000.csv')
    #     csv_f = csv.reader(f)

    #     for row in csv_f:
    #         if row[6] == "Easy": easy.append(row[2])
    #         if row[6] == "Medium": medium.append(row[2])
    #         if row[6] == "Hard": hard.append(row[2])
    #         if row[6] == "Very Hard": very_hard.append(row[2])
    #         if row[6] == "Evil": evil.append(row[2])
    #     print("Loaded puzzles from CSV.")
    # except FileNotFoundError:
    #     print("Could not load puzzles from local CSV file. Using hardcoded 'Evil' list.")

    
    print(f"Solving {len(evil)} 'Evil' puzzles with Backtracking and Heuristics...")
    
    total_time = 0
    solved_count = 0
    
    for puzzle in evil: 
        
        start_board = Board()
        
        # 1. Initialize Board and Constraint Graph
        for i in range(len(start_board)):
            for j in range(len(start_board)):
                cell = start_board[i,j]
                neigh = start_board.find_neighbors(cell.id[0] , cell.id[1], cell.id[2])
                filled_board = start_board.fill_initial_board(puzzle)
                # 2. Set initial domains based on fixed clues
                filled_board.initial_values(neigh, cell)
       
        # Solve
        start_back = time.time()
        solved = solve_back(filled_board)
        end_back = time.time()
        
        elapsed_time = (end_back - start_back)
        total_time += elapsed_time
        
        if solved:
            solved_count += 1
            print(f"-> Solved in: {elapsed_time:.4f} seconds")
        else:
            print(f"-> Failed to solve (Time: {elapsed_time:.4f} seconds)")
        
        
        # PRINTS THE SOLUTION OF THE BOARD
        print("\nSolution:")
        for i in range(len(filled_board)):
            if (i % 3 == 0):
                print("+-------------------------+")
            count_col = 0
            for j in range(len(filled_board)):
                if (j % 3 == 0):
                    print(" | ", end = "", flush = True),
                print(filled_board[i,j].cur_val, end = " ", flush = True),
                count_col = count_col + 1
            print(" |")
        print("+-------------------------+")
        
    print("\n==============================================")
    print(f"Total Puzzles Solved: {solved_count} / {len(evil)}")
    if len(evil) > 0:
        print(f"Backtracking Average Time is: {total_time / len(evil):.4f} seconds")
    
main()