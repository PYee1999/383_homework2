Name(s): Wilson Neira, Preston Yee

Tournament Bot Name: "Boogie_Woogie_Bot_Boi_383"

A short description of your thinking and the design behind your evaluation() function, along with some thoughts on its effectiveness:

Our evaluation() function is designed such that it looks at the entire current state 
(or board), using the get_rows(), get_cols() and get_diags() functions.
As we traverse through the board horizontally, vertically and diagonally, we are using 
variables to keep track of the possible streaks/points that each player could possibily 
get, and cumultatively add them up.
At the end of the traversal, we return the difference between Player 1's total streak 
points and Player 2's total streak points. If the difference is positive, then Player 1 
is currently winning; if negative, then Player 2 is currently winning; otherwise, it is 
a tie.

Short descriptions of the cases that your boards in test_boards.py are meant to test:

Our test_boards.py has a variety of small 2x2, 2x3 and 3x3 boards, with some either
being completely empty or having at least one block, to see how the minimax and pruning 
algorithms work. We also have a couple 4x5 boards (also being either completely empty or 
having at least one block) to test our heuristic algorithm.

Notes or warnings about what you got working, what is partially working, and what is broken:

All functions/classes currently appear to be working; nothing is deemed partially working
or broken.