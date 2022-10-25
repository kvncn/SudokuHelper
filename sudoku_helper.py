""" File: sudoku_helper.py
    Author: Kevin Cascais Nisterenko
    Purpose: This program will take in a file with a sudoku board and
             then 'help' the user play a game of sudoku. It prints the
             board and it can either set a value to an empty position,
             go back to the previous board, give possible solutions or
             point out conflicts, all depending on user input.
"""
import os

class ListNode:
    """ Models a single node in a singly-linked list.  Has no methods, other
        than the constructor. Used directly from the provided class in the
        spec.
    """

    def __init__(self, val):
        """ Constructs the object; caller must pass a value, which will be
            stored in the 'val' field.
        """
        self.val = val
        self.next = None

    def __str__(self):
        vals = []
        objs = set()
        curr = self
        while curr is not None:
            curr_str = str(curr.val)
            if curr in objs:
                vals.append("{} -> ... (to infinity and beyond)"
                            .format(curr_str))
                break
            else:
                vals.append(curr_str)
                objs.add(curr)
            curr = curr.next

        return " -> ".join(vals)

def get_strs_array(filename):
    """
    This function uses nested for loops to iterate over the input text file and
    append every row as strings to a strs array to be used in the arr_of_strs_
    to_2d_array function. Moreover, it concatenates the periods as zeros so
    that it will work for the rest of the program.

    Parameters:
        filename -- string that contains the name of the sudoku grid file.

    Returns:
        strs -- array of strings, where each character will be appended to
                an array of the grid array.

    Pre-condition:
        The filename string must exits, be valid, and passed to the function.

    Post-condition:
        The function will return the strs array to the program.
    """
    try:
        in_file = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: The file could not be opened.")
        return []
    else:
        strs = []

        #  This outer loop will iterate over every line of the file
        #  and initialize the row string. Then an inner loop is used
        #  to iterate over the strings in the line array. Lastly, another
        #  loop is used to iterate over every character in the string,
        #  and concatenate the character to the row string, whcih will
        #  then be appended to the strs array.
        for line in in_file:
            line = line.strip().split()
            if len(line) == 0:
                continue
            row = ""
            for region in line:
                for char in region:
                    if char == ".":
                        char = "0"
                    row += char
            strs.append(row)

        in_file.close()

        return strs

def arr_of_strs_to_2d_array(strs):
    """
    This function uses nested for loops to iterate over the strs array and
    create an array of arrays of characters (2d array), that will contain
    each character organized in columns and rows. This grid array will then
    be returned by the function.

    Parameters:
        strs -- array of strings, where each character will be appended to
                an array of the grid array.

    Returns:
        grid -- array where each element is an array of characters organized
                by columns.

    Pre-condition:
        The strs array must exist and be passed into the function.

    Post-condition:
        The function will return the grid array to the program.
    """
    grid = []

    #  The outer loop will iterate over each column and the inner loop
    #  will iterate over each row and a column array will be initialized.
    #  The element of each row for a respective column will be appended to
    #  the array.
    for col in range(9):
        column = []
        for row in range(9):
            column.append(int(strs[row][col]))
        grid.append(column)

    return grid

def get_commands(grid):
    """
    This function uses a while True loop to continuously get the user input
    for a command. In the loop there is an if-elifs-else block to check and
    call the appropriate functions based on user input.

    Parameters:
        grid -- array where each element is an array of characters organized
                by columns.

    Returns:
        None

    Pre-condition:
        The obstacles set must exist and it must be valid.

    Post-condition:
        The function will call any of the other functions based on the user
        input, as well as printing the input prompt.
    """
    head = ListNode(grid)
    print_grid(head.val)
    print()
    print("Your command:")
    #  This loop will run until it reaches the end of a file and it
    #  will continuously ask user input for a command. Using an if-
    #  elifs-else block the command will be checked and the appropriate
    #  function called.
    while True:
        try:
            user_command = input()
        except EOFError:
            print()
            break
        if user_command == "":
            continue
        if len(user_command.split()) == 4:
            user_lst = user_command.split()
            if user_lst[0] == "set" and user_lst[1].isnumeric() and \
               user_lst[2].isnumeric() and user_lst[3].isnumeric():
                print()
                head = set_value(user_lst, head)
        elif user_command == "back":
            print()
            head = go_back(head)
        elif user_command == "search":
            print()
            search_possible(head)
        elif user_command == "conflicts":
            print()
            find_conflicts(head)
        else:
            print()
            print("ERROR: Invalid command")
        print()
        print_grid(head.val)
        print()
        print("Your command:")

def go_back(head):
    """
    This function uses a simple if-else statement to check if it is possible
    to go back. If not, it will simply print a message saying this. If it is
    possible, it will go back in the linked list stack.

    Parameters:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.

    Returns:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.
                It may have one node less or no changes depend on the
                conditions met.

    Pre-condition:
        The linked list stack must exist and head must be passed into the
        function.

    Post-condition:
        The function will print to the output if the operation is not possible,
        otherwise, nothing is printed. Regardless, head (changed or unchanged)
        is returned.
    """
    if head is not None and head.next is None:
        print("ERROR: You are already at the init state, you cannot go back.")
    else:
        head = head.next

    return head

def set_value(user_lst, head):
    """
    This function simply transforms the user specified location into
    integers, then calls the dup_grid function with the column, row and
    value to be changed. After this new grid is created, it is stored inside
    a new node and the new node is added to the linked list stack. There are
    invalid input checks to ensure the sudoku grid is filled correctly.

    Parameters:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.

    Returns:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.

    Pre-condition:
        The linked list stack must exist and head must be passed into the
        function. The user command must be that to set a new value and it
        must have been valid.

    Post-condition:
        The function will return head, now pointing to a new node, to the
        program.
    """
    col = int(user_lst[1]) - 1
    row = int(user_lst[2]) - 1
    val = int(user_lst[3])

    if col < 0 or col > 8 or row < 0 or row > 8:
        print("ERROR: The given column or row does not exist.")
    elif head.val[col][row] != 0:
        print("ERROR: The 'set' command cannot run, because ", end='')
        print("the space already holds a value.")
    elif val <= 0 or val > 9:
        print("ERROR: The value must be between 1 and 9.")
    else:
        print("Square {},{} set to {}.".format(user_lst[1], user_lst[2], val))

        new_grid = dup_grid(head.val, row, col, val)
        new_node = ListNode(new_grid)
        new_node.next = head
        head = new_node

    return head

def dup_grid(grid, in_row, in_col, val):
    """
    This function works similarly to the arr_of_strs_to_2d_array function.
    It will loop through every element in the grid array and every inner
    element of the grid array and append those to a new array that will
    then be appended to the duplicate. This way, a copy that prevents
    aliasing is created. Moreover, there is an if statement that is used
    to check and substitute or insert a value set by the user in this new
    grid at the specified position.

    Parameters:
        grid -- array where each element is an array of integers organized
                by columns.
        in_row -- integer that represents the row number to have its value
               changed in the new grid.
        in_col -- integer that represents the column number to have its value
               changed in the new grid.
        val -- integer that will be 'inserted' into a the position on the
               grid.

    Returns:
        duplicate -- array where each element is an array of integers organized
                     by columns.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return a duplicate of the passed grid array to
        the program.
    """
    duplicate = []

    #  The outer loop will iterate over each column and the inner loop
    #  will iterate over each row and a column array will be initialized.
    #  The element of each row for a respective column will be appended to
    #  the array.
    for col in range(9):
        column = []
        for row in range(9):
            if row == in_row and col == in_col:
                column.append(val)
            else:
                column.append(grid[col][row])
        duplicate.append(column)

    return duplicate

def find_conflicts(head):
    """
    This function iterates through every returned array from the get_conflict
    functions (column, row and sub-region) and prints an error message for each
    position where there is a conflict using for loops.

    Parameters:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.

    Returns:
        None

    Pre-condition:
        The linked list stack must exist and head must be passed into the
        function.

    Post-condition:
        The function will print to the output if the operation is not possible,
        otherwise, nothing is printed. Regardless, head (changed or unchanged)
        is returned.
    """
    grid = head.val

    columns = sorted(get_conflict_cols(grid))
    rows = sorted(get_conflict_rows(grid))
    squares_dict = get_squares_dict(grid)
    squares = sorted(get_conflict_squares(squares_dict))

    #  If there are no conflicts, the appropriate message will be printed.
    if len(columns) == 0 and len(rows) == 0 and len(squares) == 0:
        print("Hooray!  No conflicts found.")
    else:
        #  It will check every conflict array and then print the conflict
        #  message accordingly for every position in columns, rows and
        #  squares.
        if len(columns) > 0:
            for pos in columns:
                print("ERROR: Column {} has a conflict.".format(pos))
        if len(rows) > 0:
            for pos in rows:
                print("ERROR: Row {} has a conflict.".format(pos))
        if len(squares) > 0:
            for pos in squares:
                print("ERROR: Sub-region {},{} has a conflict."
                      .format(pos[0], pos[1]))

def get_conflict_cols(grid):
    """
    This function uses a for loop to iterate through every element
    of every column of the grid array and check if there are any
    duplicates, if there are, the column number will be appended to
    a columns array and then this array will be returned.

    Parameters:
        grid -- array where each element is an array of any possible elements
                organized by columns.

    Returns:
        columns -- array of the columns where there are conflicts.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return an array of the number of the conflicting
        columns.
    """
    columns = []

    #  The outer loop initializes an empty array and the dup variable to False.
    #  The inner loop will then append numbers that were not seen before to the
    #  array and if the number was seen and it is different than 0, dup will be
    #  changed to True because there is a duplicate there. Then if duplicate
    #  was changed to True, the column number will be appended to the columns
    #  list.
    for col in range(len(grid)):
        seen = []
        dup = False
        for num in grid[col]:
            if num not in seen:
                seen.append(num)
            elif num in seen and num != 0:
                dup = True
        if dup:
            columns.append(col + 1)

    return columns

def get_conflict_rows(grid):
    """
    This function works similarly to the get_conflict_cols function. It uses
    nested for loops to iterate through every row and the numbers in them and
    perform a check of duplicates. The function then returns an array with
    the row numbers where there were conflicts.

    Parameters:
        grid -- array where each element is an array of any possible elements
                organized by columns.

    Returns:
        rows -- array of integers that represent conflicting rows.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return an array of the numbers of the conflicting
        rows.
    """
    rows = []

    #  The outer loop initializes an empty array and the dup variable to False.
    #  The inner loop will then append numbers that were not seen before to the
    #  array and if the number was seen and it is different than 0, dup will be
    #  changed to True because there is a duplicate there. Then if duplicate
    #  was changed to True, the column number will be appended to the rows
    #  list.
    for col in range(len(grid)):
        seen = []
        dup = False
        for row in range(len(grid[col])):
            num = grid[row][col]
            if num not in seen:
                seen.append(num)
            elif num in seen and num != 0:
                dup = True
        if dup:
            rows.append(col + 1)

    return rows

def get_squares_dict(grid):
    """
    This function iterates through the grid and gets a 2d array of the squares.
    Then this array is organized into a dictionary with tuples of xy
    coordinates as its keys. This dictionary is then returned.

    Parameters:
        grid -- array where each element is an array of any possible elements
                organized by columns.

    Returns:
        squares_dict -- dictionary where the keys are tuples of two integers
                        representing x/y coordinates of a square in the board.
                        The values are arrays of integers that represent a
                        square/sub-region of the board.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return a dictionary of all the squares.
    """
    squares_array = []

    #  Creates a 2d array in which every inner array are the integers of a
    #  sub region on the board.
    for col in range(0, 9, 3):
        square = []
        for row in range(0, 9):
            square.append(grid[col][row])
            square.append(grid[col+1][row])
            square.append(grid[col+2][row])
        #  Separates the square arrays.
        squares_array.append(square[:9])
        squares_array.append(square[9:18])
        squares_array.append(square[18:])

    #  Each key is the square coordinate and the values are the square arrays.
    squares_dict = {(1,1): squares_array[0], (1,2): squares_array[1],
                    (1,3): squares_array[2], (2,1): squares_array[3],
                    (2,2): squares_array[4], (2,3): squares_array[5],
                    (3,1): squares_array[6], (3,2): squares_array[7],
                    (3,3): squares_array[8]}

    return squares_dict

def get_conflict_squares(squares_dict):
    """
    This function works similarly to the other get_conflict function. However,
    the outer loop now iterates through keys in a dictionary and the inner loop
    works essentailly the same in finding arrays with duplicate numbers.

    Parameters:
        squares_dict -- dictionary where the keys are tuples of two integers
                        representing x/y coordinates of a square in the board.
                        The values are arrays of integers that represent a
                        square/sub-region of the board.

    Returns:
        squares -- array of tuples of two integers each representing the
                   position of squares that have conflicting/duplicate
                   numbers in them.

    Pre-condition:
        The get_squares_dict function must have been called before and its
        return must be passed as a paramter to this function.

    Post-condition:
        The function will return an array of tuples of integers representing
        conflicting square positions.
    """
    squares = []

    #  The outer loop initializes an empty array and the dup variable to False.
    #  The inner loop will then append numbers that were not seen before to the
    #  array and if the number was seen and it is different than 0, dup will be
    #  changed to True because there is a duplicate there. Then if duplicate
    #  was changed to True, the column number will be appended to the squares
    #  list.
    for coordinates in squares_dict:
        seen = []
        dup = False
        for num in squares_dict[coordinates]:
            if num not in seen:
                seen.append(num)
            elif num in seen and num != 0:
                dup = True
        if dup:
            squares.append(coordinates)

    return squares

def search_possible(head):
    """
    This function uses nested for loops to iterate through every number in the
    grid and check for every zero if there is a single possible solution by
    calling the get_col, get_row and get_square functions and checking if
    there is a number from 1 to 9 there has not been used yet and another for
    loop is used for this. Then the function prints the correct message to
    the output.

    Parameters:
        head -- ListNode object that represents the first node of the linked
                list stack. It also gives access to the rest of the linked
                list.

    Returns:
        None

    Pre-condition:
        The linked list stack must exist and head must be passed into the
        function.

    Post-condition:
        The function will print to the output all spaces and their solutions
        (if there is only one solution) and the spaces that have no solutions.
        It can also print a no solutions found if the above conditions have not
        been met.
    """
    grid = head.val

    possible = False

    #  These for loops iterate through every number in the grid and then
    #  if the number is zero (meaning the user can change it), it will
    #  get the sets of all numbers in that zero respective colum, row and
    #  square and then unite these sets together.
    for row in range(9):
        for col in range(9):
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if grid[col][row] == 0:
                col_nums = get_col(grid, col)
                row_nums = get_row(grid, row)
                start_col, start_row = get_square_coords(col, row)
                square_nums = get_square(grid, start_col, start_row)

                invalid_nums = col_nums | row_nums | square_nums

                #  For every number in the set, it will remove that number
                #  from the nums array (which is then re-initialized after
                #  every run of the inner/middle for loop).
                for num in invalid_nums:
                    if num in nums:
                        nums.remove(num)

                #  Checks if the length of the nums array is 1 for every run
                #  of the inner loop and prints the appropriate message.
                if len(nums) == 1:
                    possible = True
                    print("Solution!  The only value possible at", end='')
                    print(" square {},{} is {}.".format(col+1, row+1, nums[0]))
                elif len(nums) == 0:
                    print("The square {},{}".format(col+1, row+1), end='')
                    print(" does not have any possible values!")

    if not possible:
        print("Sorry, no solutions were found.")

def get_square_coords(col, row):
    """
    This function transforms the row and col numbers of the current integer
    in the search_possible function loop and 'transforms' them into numbers
    that can be used in the get_square function to get the square set. To do
    this, if-elif-else blocks are used for both parameters.

    Parameters:
        col -- integer that represents the current column index of a number
               on the grid.
        row -- integer that represents the current row index of a number on
               the grid.

    Returns:
        start_col -- integer that represents the sub-region x index of a
                     number on the grid.
        start_row -- integer that represents the sub-region y index of a
                     number on the grid.

    Pre-condition:
        The col and row integers must be passed to the function.

    Post-condition:
        The function will return the start_col and start_row integers to the
        program.
    """
    if 0 <= row <= 2:
        start_row = 0
    elif 3 <= row <= 5:
        start_row = 1
    else:
        start_row = 2

    if 0 <= col <= 2:
        start_col = 0
    elif 3 <= col <= 5:
        start_col = 1
    else:
        start_col = 2

    return start_col, start_row

def get_col(grid, x):
    """
    This function uses a for loop to iterate through every integer
    of a column of the grid array and add that integer to a
    column set that will then be returned. One thing to note is
    that no zeros will be added to the array.

    Parameters:
        grid -- array where each element is an array of integers
                organized by columns.
        x -- integer that represents the column number/index.

    Returns:
        column -- set of integers of the column specified by x.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return a set of the specified column.
    """
    column = set()

    #  Adds every integer of the specified column in grid to the column
    #  set, except if the integer is zero.
    for num in grid[x]:
        if num != 0:
            column.add(num)

    return column

def get_row(grid, y):
    """
    This function uses a for loop to iterate through every row
    in grid and append the element at the y index to the row set
    which will then be returned. One thing to note is that no
    zeros will be added to the array.

    Parameters:
        grid -- array where each element is an array of integers
                organized by columns.
        y -- integer that represents the row number/index.

    Returns:
        row -- set of integers the row specified by y.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return a set of integers of the specified row.
    """
    row = set()

    #  Iterates through every column and adds to the row set the
    #  number at that row index, except if the number is zero.
    for i in range(9):
        if grid[i][y] != 0:
            row.add(grid[i][y])

    return row

def get_square(grid, sx, sy):
    """
    This function first transforms the given integers so that
    they will work for the sub-regions of the board and not
    only individual rows and columns. Then nested for loops are used
    to iterate through every column and row and stopping 3 columns
    and rows from the starting point. The elements found are then
    apended to the squares array.

    Parameters:
        grid -- array where each element is an array of integers
                organized by columns.
        sx -- integer that represents the column number/index of the square in
              regards to the grid as a whole.
        sy -- integer that represents the row number/index of the square in
              regards to the grid as a whole.

    Returns:
        square -- set of integers that represents a sub-region of the board.

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will return an array of the specified square sub-region.
    """
    square = set()

    #  Transforms the sx to work for each sub-region and not only each column.
    if sx == 1:
        sx = 3
    elif sx == 2:
        sx = 6

    #  Transforms the sy to work for each sub-region and not only each row.
    if sy == 1:
        sy = 3
    elif sy == 2:
        sy = 6

    #  Iterates through a sub-region starting with the given column index.
    for i in range(sx, sx + 3):
        #  Iterates through elements in the rows starting with the given row
        #  index.
        for j in range(sy, sy + 3):
            if grid[i][j] != 0:
                square.add(grid[i][j])

    return square

def print_grid(grid):
    """
    This function uses nested for loops to print the grid array divided into
    9 3x3 sub-regions. The outer loop will print vertical spaces between
    sub-regions, the middle loop will print out the numbers and horizontal
    spaces between sub-regions and the inner loop will transform integers
    to strings to print out.

    Parameters:
        grid -- array where each element is an array of integers organized
                by columns.

    Returns:
        None

    Pre-condition:
        The grid array must exist and be passed into the function.

    Post-condition:
        The function will print the sudoku grid to the output.
    """
    #  Iterates over every column and prints out the vertical spacing.
    for i in range(9):
        #  Iterates trough every 3 columns and prints out the 9 numbers
        #  (with a period for 0), of each row
        for j in range(0, 9, 3):
            num1 = grid[j][i]
            num2 = grid[j+1][i]
            num3 = grid[j+2][i]
            numbers = [num1, num2, num3]
            #  Substitutes 0 for periods and transforms integers to
            #  strings.
            for k in range(len(numbers)):
                if numbers[k] == 0:
                    numbers[k] = "."
                else:
                    numbers[k] = str(numbers[k])
            print(numbers[0] + numbers[1] + numbers[2], end='')
            # Prints the spacing between horizontal sub-regions.
            if j != 6:
                print(" ", end='')
        print()
        #  Separates each vertical sub-region with blank line.
        if i % 3 == 2 and i != 8:
            print()

def main():
    # chdir to the same directory as where this script is ... so
    # that open() will open the file we expect.
    this_script = os.path.realpath(__file__)
    dir_of_script = os.path.dirname(this_script)
    os.chdir(dir_of_script)

    print("Please give the name of the file that contains the board:")
    filename = input()

    file_array = get_strs_array(filename)

    if file_array != []:
        grid = arr_of_strs_to_2d_array(file_array)
        get_commands(grid)

if __name__ == "__main__":
    main()