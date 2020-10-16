import pytest
from picross_board import PicrossBoard

parameters = 'size, seed, row_definitions, col_definitions, solution, solved'
testdata = [
        # size, seed, row_definitions, col_definitions, solution, solved
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
                             row_definitions, col_definitions,
                             solution, solved):
        
        if solved is None or solution is None:
            pytest.skip("Test can not run if solution of solved status is " +
                        "not provided")
        
        board = PicrossBoard(size)     
        
        board.set_row_definitions(row_definitions)
        board.set_col_definitions(col_definitions)
        
        board.set_state(solution)
        
        assert board.solved() == solved

    @pytest.mark.parametrize(parameters, testdata)    
    def test_generate_valid_puzzle(self, size, seed,
                                   row_definitions, col_definitions,
                                   solution, solved):
        
        if seed is None:
            pytest.skip("Test can not run when a seed is not provided.")
        
        board = PicrossBoard(size)
        state = board.generate_valid_puzzle(seed)
       
        assert board.row_definitions == row_definitions
        assert board.col_definitions == col_definitions
        assert state == solution