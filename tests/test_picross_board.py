from picross_board import PicrossBoard

class TestPicrossBoard:
    
    def test_solution_solved(self):
        
        board = PicrossBoard(2)
        
        row_segments = [[1], [0]]
        board.set_row_segments(row_segments)
        
        col_segments = [[1], [0]]
        board.set_col_segments(col_segments)
        
        solution = [[1, 0],
                    [0, 0]]
        board.set_state(solution)
        
        assert board.solved() == True
    
    def test_solution_not_solved(self):
        
        board = PicrossBoard(2)
        
        row_segments = [[1], [0]]
        board.set_row_segments(row_segments)
        
        col_segments = [[1], [0]]
        board.set_col_segments(col_segments)
        
        solution = [[1, 0],
                    [0, 1]]
        board.set_state(solution)
        
        assert board.solved() == False
    
    def test_generate_valid_puzzle(self):
        
        solution = [[1, 1],
                    [0, 0]]

        board = PicrossBoard(2)
        state = board.generate_valid_puzzle(0)
       
        assert board.row_segments == [[2], [0]]
        assert board.col_segments == [[1], [1]]
        assert state == solution