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
            
    def __getitem__(self, key):
        
        row = key[0]
        self._key_check(row)
        
        col = key[1]
        self._key_check(col)
        
        return self.board[row][col]
        
    def __setitem__(self, key, value):
        
        row = key[0]
        self._key_check(row)
        
        col = key[1]
        self._key_check(col)
        
        if value not in [-1, 0, 1]:
            raise ValueError('Board cell must be one of -1, 0 or 1.')
            
        self.board[row][col] = value
        
    def set_row_segments(self, row_segments):
        self.row_segments = row_segments
        
    def set_col_segments(self, col_segments):
        self.col_segments = col_segments
        
    def set_state(self, state):
        """Set the entire state of the board to a particular value."""

        if len(state) != self.size:
            raise ValueError(f'Board must have {self.size} rows.')
            
        for row in state:
            if len(row) != self.size:
                raise ValueError(f'Board must have {self.size} columns.')
                
        for row in range(self.size):
            for col in range(self.size):
                if state[row][col] not in [-1, 0, 1]:
                    raise ValueError('Board cell must be one of -1, 0, or 1.')
                    
        self.board = state        
        
    def solved(self):
        """Return whether the picross board is solved."""
        
        if self.row_segments is None or self.col_segments is None:
            raise RuntimeError("Segments must be defined for columns and rows.")
        
        for row in range(self.size):
            if not self._solved('row', row):
                return False
        
        for col in range(self.size):
            if not self._solved('col', col):
                return False
        
        return True
    
    def generate_valid_puzzle(self, seed=None):
        """Generate a picross puzzle whose solution is valid."""
        
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()
            
        self.board = self._generate_blank_board()
        for row in range(self.size):
            for col in range(self.size):
                if random.random() >= 0.5:
                    self.board[row][col] = 1
                else:
                    self.board[row][col] = 0
                    
        self.col_segments = self._generate_segments('col')
        self.row_segments = self._generate_segments('row')
        
        return self.board
    
    def _key_check(self, key):
        
        if key < 0 or key >= self.size:
            raise IndexError('Board rows and cols must be between 0 and {self.size - 1}')
            
    def _solved(self, axis, index):
        
        if axis == 'row':
            array = self.board[index]
            segments = self.row_segments[index]
        elif axis == 'col':
            array = [self.board[row][index] for row in range(self.size)]
            segments = self.col_segments[index]
        else:
            raise ValueError('axis must be either "row" or "col"')
            
        cur_segment = 0
        i = 0
        
        while i < self.size:
            length, prev_i = self._traverse_segment(array, i)
            if cur_segment >= len(segments):
                if length != 0:
                    return False
            elif length == 0:
                pass
            elif length != 0:
                if length != segments[cur_segment]:
                    return False
                if segments[cur_segment] != 0:
                    cur_segment += 1
            i = prev_i + 1

        return True
    
    def _generate_segments(self, axis):
        
        segments = []
        
        if axis == 'row':
            for row in range(self.size):
                array = self.board[row]
                segments.append(self._generate_definition(array))
        elif axis == 'col':
            for col in range(self.size):
                array = [self.board[row][col] for row in range(self.size)]
                segments.append(self._generate_definition(array))    
        else:
            raise ValueError('axis must be either "row" or "col"')
            
        return segments
    
    def _generate_definition(self, array):
            
        this_arrays_definition = []
        
        index = 0
        while index < len(array):
            if array[index] != 0:
                length, index = self._traverse_segment(array, index)
                this_arrays_definition.append(length)
            index+=1
        if len(this_arrays_definition) == 0:
            this_arrays_definition.append(0)
            
        return this_arrays_definition
    
    def _traverse_segment(self, array, starting_index):
        
        index = starting_index
        length = 0
        
        if array[index] == 0:
            return (length, index)
        
        while array[index] != 0:
            length += 1
            index += 1
            if index >= self.size:
                break
            
        return (length, index - 1)
            
    def _generate_blank_board(self):
        
        board = []
        for i in range(self.size):
            row = [0]*self.size
            board.append(row)
            
        return board