'''
[FIND RECTANGLES]:
This function finds the smallest closed perimeter of a rectangle in a matrix.

For example:

0 0 0 0 0 0 0 0 
1 1 1 1 1 0 0 0
1 0 1 0 1 0 0 0
1 0 1 0 1 0 0 0
1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0

The function will return the:

TOP-LEFT ELEMENT:    (1,0)
RECTANGLE WIDTH:     3  
RECTANGLE HEIGHT:    4
RECTANGLE PERIMETER: (1,0), (1,1), (1,2), (4,0), (4,1), (4,2), (2,0), (3,0), (2,2), (3,2)   

If the rectangle hasn't been found, the top-left element which gets returned is "(-1,-1)"
'''


def find_smallest_rectangle(matrix, minimum_size):
    '''
    "minimum_size" : 2-elements tuple which represents the minimum size
                     of the peripheral rectangles to detect.
    '''
    # [The count of rows and columns
    # of the matrix gets retrieved]
    rows_cnt = len(matrix)
    cols_cnt = len(matrix[0]) if rows_cnt > 0 else 0

    #  /-------------------------------------------------------------\
    # | We iterate on all of the possible (height, width)             |
    # | couples, where "height" values span from "minimum_size[0]" to |
    # | "rows_cnt", while "width" values span from "2" to "cols_cnt"  |
    #  \-------------------------------------------------------------/
    for height in range(minimum_size[0], rows_cnt + 1):
        for width in range(minimum_size[1], cols_cnt + 1):
            #  /------------------------------------------------------------------\
            # | The dimensions of the submatrix which is getting tested            |
            # | - in the current iteration - in order to find the smallest         |
            # | perimetral rectangle - are "(rows_cnt - height, cols_cnt - width)" |
            # |                                                                    |
            # | (That means, smaller submatrices are tested first)                 |
            #  \------------------------------------------------------------------/
            for i in range(rows_cnt - height + 1):
                for j in range(cols_cnt - width + 1):
                    #  /--------------------------------------\
                    # | WHAT IS THE LOGIC BEHIND THE FUNCTION? |
                    #  \--------------------------------------/________________________
                    # | A single iteration of this double cycle corresponds to the     \
                    # | testing of a single perimetral rectangle of (i,j) size.         |
                    # |                                                                 |
                    # | The rows are tested first, starting with the top row:           |
                    # | if any element in the top row is found to be different          |
                    # | than "0", then the iteration gets skipped ("continue")          |
                    # | altogether, and a new perimetral rectangle of (i,j+1) size      |
                    # | gets tested.                                                    |
                    # |                                                                 |
                    # | If - instead - the row contains only "1"s, that means that      |
                    # | we've found a possible top row for a perimetral rectangle,      |
                    # | and the function proceeds with the current iteration by testing |
                    # | the bottom row (applying the same logic to it), then the left   |
                    # | column, then the right column.                                  |
                    # |                                                                 |
                    # | The first set of (i,j) indexes which passes all of the four     |
                    # | tests will be the one relative to the iteration in which        |
                    # | the smallest rectangle in the matrix has been found.            |
                    # |                                                                 |
                    # | If we get to the point of every test passing, the coordinates   |
                    # | of the elements of the perimetral rectangle get appended to a   |
                    # | "perimeter" list, which will be returned to the caller together |
                    # | with the "top-left coordinates", the width and the length of    |
                    # | the rectangle which has been detected.                          |
                    #  \---------------------------------------------------------------/

                    #  /---------------------------\
                    # | TESTING THE PERIMETRAL ROWS |
                    #  \---------------------------/
                    # [TESTING THE TOP ROW]
                    if any(matrix[i][j + x] != 1 for x in range(width)):
                        continue

                    # [TESTING THE BOTTOM ROW]
                    if any(matrix[i + height - 1][j + x] != 1 for x in range(width)):
                        continue

                    #  /--------------------------------\
                    # | TESTING THE PERIMETRAL COLUMNS   |
                    # |  (THE FOUR CORNERS ARE EXCLUDED, |
                    # |   GIVEN THEY'VE ALREADY BEEN     |
                    # |   TESTED BY TESTING THE TOP      |
                    # |   AND BOTTOM ROWS)               |
                    #  \--------------------------------/
                    # [TESTING THE LEFT COLUMN]
                    if any(matrix[i + y][j] != 1 for y in range(1, height - 1)):
                        continue

                    # [TESTING THE RIGHT COLUMN]
                    if any(matrix[i + y][j + width - 1] != 1 for y in range(1, height - 1)):
                        continue

                    # Build perimeter coordinates
                    perimeter = []
                    perimeter.extend((i, j + x) for x in range(width))                      # Top
                    perimeter.extend((i + y, j + width - 1) for y in range(1, height - 1))  # Right
                    perimeter.extend((i + height - 1, j + x) for x in range(width))         # Bottom
                    perimeter.extend((i + y, j) for y in range(1, height - 1))              # Left

                    #  /-----------------------------------------------------------------\
                    # | The "return values" get returned to the caller as soon as a       |
                    # | closed perimeter is found (thus ensuring that the found rectangle |
                    # | is - effectively - the smallest one).                             |
                    #  \-----------------------------------------------------------------/
                    return (i, j), width, height, perimeter

    # If no perimetral rectangles has been found, then the returned
    # value for the "top-left" set of coordinates is (-1, -1)
    return (-1, -1), 0, 0, []


#  /----\
# | TEST |
#  \----/
if __name__ == "__main__":
    matrix = [[0,0,0,0,0,0,0,0],
              [1,1,1,1,1,0,0,0],
              [1,0,1,0,1,0,0,0],
              [1,0,1,0,1,0,0,0],
              [1,1,1,1,1,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0]]
    
    smallest_rectangle = find_smallest_rectangle(matrix)
    print(f"[TOP-LEFT COORDINATES]: {smallest_rectangle[0]}\n[WIDTH]: {smallest_rectangle[1]}\n[HEIGTH]: {smallest_rectangle[2]}\n[PERIMETER]: {smallest_rectangle[3]}")