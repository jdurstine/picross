import random

class PicrossBoard:
    
    def __init__(self, size, **kwargs):
        
        self.size = size
        self.board = self._generate_blank_board()
        self.row_segments = None
        self.col_segments = None
        
        if 'row_segment' in kwargs.keys():
            self.row_segments = kwargs['row_segments']
            
        if 'col_segments' in kwargs.keys():
            self.col_segments = kwargs['col_segments']
            
    def set_row_segments(self, row_segments):
        self.row_segments = row_segments
        
    def set_col_segments(self, col_segments):
        self.col_segments = col_segments
        
    def set_state(self, state):
        self.board = state
    
    def solved(self):
        """Return whether the picross board is solved."""
        
        if self.row_segments is None or self.col_segments is None:
            raise RuntimeError("Segments must be defined for columns and rows.")
        
        for row in range(self.size):
            if not self._row_solved(row):
                return False
        
        for col in range(self.size):
            if not self._col_solved(col):
                return False
        
        return True
    
    def generate_valid_puzzle(self, seed=None):
        """Generate a picross puzzle whose solution is valid."""
        
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()
            
        board = self._generate_blank_board()
        for row in range(self.size):
            for col in range(self.size):
                if random.random() >= 0.5:
                    board[row][col] = 1
                else:
                    board[row][col] = 0
                    
        self.col_segments = self._generate_column_segments()
        self.row_segments = self._generate_row_segments()
        
        return board
        
    def _generate_column_segments(self):
        
        col_segments = []
        
        row = 0
        for col in range(self.size):
            this_col = []
            while row < self.size:
                if self.board[row][col] != 0:
                    length, col = self._traverse_col_segment(col, row)
                    this_col.append(length)
                row+=1
            if len(col_segments) == 0:
                this_col.append(0)
            col_segments.append(this_col)
            
        return col_segments
        
        
    def _generate_row_segments(self):
        
        row_segments = []
        
        col = 0
        for row in range(self.size):
            this_row = []
            while col < self.size:
                if self.board[row][col] != 0:
                    length, col = self._traverse_row_segment(row, col)
                    this_row.append(length)
                col+=1
            if len(this_row)==0:
                this_row.append(0)
            row_segments.append(0)
            
        return row_segments
    
    def _generate_blank_board(self):
        
        board = []
        for i in range(self.size):
            row = [0]*self.size
            board.append(row)
            
        return board
        
    def _row_solved(self, row):
        """Check to see if a given row is solved based on the rows segments."""
        
        cur_segment = 0
        index = 0
        
        while index < self.size:
            length, last_index = self._traverse_row_segment(row, index)
            if cur_segment >= len(self.row_segments[row]):
                if length != 0:
                    return False
            else:
                if length != self.row_segments[row][cur_segment]:
                    return False
                if self.row_segments[row][cur_segment] != 0:
                    cur_segment += 1
            index = last_index + 1

        return True
                
    def _traverse_row_segment(self, row, starting_index):
        """Return the size of a segment and the last index checked."""
        
        index = starting_index
        length = 0
        
        if self.board[row][index] == 0:
            return (length, index)
        
        while self.board[row][index] != 0:
            length += 1
            index += 1
            if index >= self.size:
                break
            
        return (length, index - 1)
    
    def _col_solved(self, col):        
        """Check to see if a given row is solved based on the rows segments."""
        
        cur_segment = 0
        index = 0
        
        while index < self.size:
            length, last_index = self._traverse_row_segment(col, index)
            if cur_segment >= len(self.col_segments[col]):
                if length !=0:
                    return False
            else:
                if length != self.col_segments[col][cur_segment]:
                    return False
                if self.col_segments[col][cur_segment] != 0:
                    cur_segment += 1
            index = last_index + 1

        return True
        
    def _traverse_col_segment(self, col, starting_index):
        """Return the size of a segment and the last index checked."""
        
        index = starting_index
        length = 0
        
        if self.board[index][col] == 0:
            return (length, index)
        
        while self.board[index][col] != 0:
            length += 1
            index += 1
            if index >= self.size:
                break
            
        return (length, index - 1)
        
if __name__ == "__main__":
    #add tests
    
    board = PicrossBoard(2)
    row_segments = [[1], [0]]
    col_segments = [[1], [0]]

    board.set_row_segments(row_segments)
    board.set_col_segments(col_segments)
    
    print('Starting test 1...')
    solution = [[1, 0],
                [0, 0]]
    board.set_state(solution)
    assert board.solved() == True
    print('Test 1 passed.')
    
    print('Starting test 2...')
    solution = [[1, 0],
                [0, 1]]
    board.set_state(solution)
    assert board.solved() == False
    print('Tes 2 passed.')
    
    print('Starting test 3...')
    solution = [[1, 1],
                [0, 0]]
    new_board = board.generate_valid_puzzle(0)
    assert new_board == solution
    print('Test 3 passed.')
    
    
        
        
