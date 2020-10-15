from picross_board import PicrossBoard

solution = [[1, 1, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1]]

board = PicrossBoard(4)

board.set_row_segments([[3], [3], [2], [2]])
board.set_col_segments([[1, 1], [3], [2, 1], [1, 1]])
board.set_state(solution)

board.solved()