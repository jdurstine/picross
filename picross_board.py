import random

class PicrossBoard:
    
    def __init__(self, size, **kwargs):
        
        self.size = size
        self.board = self._generate_blank_board()
        self.row_definitions = None
        self.col_definitions = None
        
        if 'row_definitions' in kwargs.keys():
            self.row_definitions = kwargs['row_definitions']
            
        if 'col_definitions' in kwargs.keys():
            self.col_definitions = kwargs['col_definitions']
            
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
        
    def set_row_definitions(self, row_definitions):
        self.row_definitions = row_definitions
        
    def set_col_definitions(self, col_definitions):
        self.col_definitions = col_definitions
        
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
        
        if self.row_definitions is None or self.col_definitions is None:
            raise RuntimeError("Definitions must be defined for columns and rows.")
        
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
                    
        self.col_definitions = self._generate_definitions('col')
        self.row_definitions = self._generate_definitions('row')
        
        return self.board
    
    def _key_check(self, key):
        
        if key < 0 or key >= self.size:
            raise IndexError('Board rows and cols must be between 0 and {self.size - 1}')
            
    def _solved(self, axis, index):
        
        if axis == 'row':
            array = self.board[index]
            segments = self.row_definitions[index]
        elif axis == 'col':
            array = [self.board[row][index] for row in range(self.size)]
            segments = self.col_definitions[index]
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
    
    def _generate_definitions(self, axis):
        
        definitions = []
        
        if axis == 'row':
            for row in range(self.size):
                array = self.board[row]
                definitions.append(self._generate_definition(array))
        elif axis == 'col':
            for col in range(self.size):
                array = [self.board[row][col] for row in range(self.size)]
                definitions.append(self._generate_definition(array))    
        else:
            raise ValueError('axis must be either "row" or "col"')
            
        return definitions
    
    def _generate_definition(self, array):
            
        definitions_segments = []
        
        index = 0
        while index < len(array):
            if array[index] != 0:
                length, index = self._traverse_segment(array, index)
                definitions_segments.append(length)
            index+=1
        if len(definitions_segments) == 0:
            definitions_segments.append(0)
            
        return definitions_segments
    
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