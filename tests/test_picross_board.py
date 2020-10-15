import pytest
from picross_board import PicrossBoard

parameters = 'size, seed, row_segments, col_segments, solution, solved'
testdata = [
        # size, seed, row_segments, col_segments, solution, solved
        (2, None, [[1], [0]], [[1], [0]], [[1, 0], [0, 0]], True),
        (2, 0, [[2], [0]], [[1], [1]], [[1, 1], [0, 0]], True),
        (4,
         None,
         [[3], [3], [2], [2]],
         [[1, 1], [3], [2, 1], [1, 1]],
         [[1, 1, 1, 0],
          [0, 1, 1, 1],
          [1, 1, 0, 0],
          [0, 0, 1, 1]],
         True)
        ]

class TestPicrossBoard:

    @pytest.mark.parametrize(parameters, testdata) 
    def test_solution_solved(self, size, seed,
                             row_segments, col_segments,
                             solution, solved):
        
        if solved is None or solution is None:
            pytest.skip("Test can not run if solution of solved status is " +
                        "not provided")
        
        board = PicrossBoard(size)     
        
        board.set_row_segments(row_segments)
        board.set_col_segments(col_segments)
        
        board.set_state(solution)
        
        assert board.solved() == solved

    @pytest.mark.parametrize(parameters, testdata)    
    def test_generate_valid_puzzle(self, size, seed,
                                   row_segments, col_segments,
                                   solution, solved):
        
        if seed is None:
            pytest.skip("Test can not run when a seed is not provided.")
        
        board = PicrossBoard(size)
        state = board.generate_valid_puzzle(seed)
       
        assert board.row_segments == row_segments
        assert board.col_segments == col_segments
        assert state == solution