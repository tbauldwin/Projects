#author: Taylor Bauldwin
#Date: 8/13/2020
#Discription: BlackBox programs intializes a board and takes locations for atoms and will run the popular puzzle game known
# as black box. uses shoot ray method to search for atoms. Program also contains a function to get the score and to know how
#many atoms are remaining.




class BlackBoxGame:
    """Class black box game intializes the board and includes functions for all of the rules of the games"""


    # An init method that takes as its parameter a list of (row, column) tuples for the locations of the atoms in the black box,
    # and initializes any data members. You may assume that the given coordinates are valid and don't contain any duplicates.
    # You may also assume that the list contains at least one tuple.
    def __init__(self, list_rows_cols):
        '''This method initializes the game'''
        self.__board = [[0 for i in range(10)] for j in range(10)]
        self.__tup_lists = list_rows_cols
        self.__score = 25  # Initial score
        self.__atoms = len(list_rows_cols)  # Total number of atoms
        self.__list_of_visits = []
        self.__prev_vals = []
        for i in self.__tup_lists:
            self.__board[i[0]][i[1]] = -1

    # A method named shoot_ray that takes as its parameters the row and column (in that order) of the border square where the ray originates.
    # If the chosen row and column designate a corner square or a non-border square, it should return False. Otherwise, shoot_ray should
    # return a tuple of the row and column (in that order) of the exit border square. If there is no exit border square (because there was a hit),
    # then shoot_ray should return None. The guessing player's score should be adjusted accordingly. (Note: if the return value of a function can
    # have different types, it's a very good idea to specify that in the docstring.)
    def shoot_ray(self, row, col):
        '''This method returns different types.
        First of all we will check if the shooting place is a corner if yes then return False
        then we check if the the shooting place  is inside the board if yes then return False
        Now we check the path of movement-(up/down/right/left)
        check if entry is already visited using entry_exit_check method, if False
            Decrease one point of entry
        else:
            return None
        Now if all above conditions are satisfied then one by one we check for all the possible conditions of exit
        First check if the shooted ray passes without hitting any atome-update exit variable and score
        Second check if the shooted ray hits the atom-if yes decrease no of atoms update score and set exit as None

        Third check on the basis of direction of ray(if down) row+1,col+1 or row+1,col-1  contains an atom, if yes then set exit same as entry and update score
        Fourth use looping to walk through the path(using path set above) and check(if path is down) if every(excluding i==0) i+1,j+1 or i+1,j-1 is an atom if yes then
        check where the atom is present(j+1/j-1/both) then set the exit accordingly and update the score
        Check if the exit is not same as entry if yes then deduct exit score
        save entry point as tuple in list_of_visits
        if exit is not None save exit point as tuple in list_of_visits'''

        path = None
        if row == 0:
            path = "down"
        elif row == 9:
            path = "up"
        elif col == 0:
            path = "right"
        elif col == 9:
            path = "left"



        if self.is_corner_square(row, col) or self.is_nonborder_square(row, col) :
            return False

        start = (row, col)
        if start not in self.__prev_vals:
            self.__score = self.__score - 1
            self.__prev_vals.append(start)

        val = self.shoot_ray_helper(row, col, path)
        if val != None:
            if val not in self.__prev_vals:
                self.__score = self.__score - 1
                self.__prev_vals.append(val)

        return val



    def shoot_ray_helper(self, row, col, path):
        """helper function for shoot ray, function iterates through the proper col or row in search for an atom
        function will call on itself if a deflection happens or return no if ray makes it all the way through its
        intended path"""

        if path == "down":
                for i in range(row, 9):
                    if self.__board[i + 1][col - 1] == -1 and self.check(i + 1, col - 1):
                        return self.shoot_ray_helper(i, col, "right")
                    elif self.__board[i + 1][col + 1] == -1 and self.check(i + 1, col + 1):
                        return self.shoot_ray_helper(i, col, "left")
                    elif self.__board[i][col] == -1 and self.check(i, col):
                        return None
                return (9, col)

        if path == "up":
                for i in range(row, 0, -1):
                    if self.__board[i - 1][col - 1] == -1 and self.check(i - 1, col - 1):
                        return self.shoot_ray_helper(i, col, "right")
                    elif self.__board[i - 1][col + 1] == -1 and self.check(i - 1, col + 1):
                        return self.shoot_ray_helper(i, col, "left")
                    elif self.__board[i][col] == -1 and self.check(i, col):
                        return None
                return (0, col)

        if path == "right":
                for i in range(col, 9):
                    if self.__board[row - 1][i + 1] == -1 and self.check(row - 1, i + 1):
                        return self.shoot_ray_helper(row, i, "down")
                    elif self.__board[row + 1][i + 1] == -1 and self.check(row + 1, i + 1):
                        return self.shoot_ray_helper(row, i, "up")
                    elif self.__board[row][i] == -1 and self.check(row, i):
                        return None
                return (row, 9)

        if path == "left":
                for i in range(col, 0, -1):
                    if self.__board[row - 1][i - 1] == -1 and self.check(row - 1, i - 1):
                        return self.shoot_ray_helper(row, i, "down")
                    elif self.__board[row + 1][i - 1] == -1 and self.check(row + 1, i - 1):
                        return self.shoot_ray_helper(row, i, "up")
                    elif self.__board[row][i] == -1 and self.check(row, i):
                        return None
                return (row, 0)



    # A method named guess_atom that takes as parameters a row and column (in that order). If there is an atom at that location,
    # guess_atom should return True, otherwise it should return False. The guessing player's score should be adjusted accordingly.
    def guess_atom(self, row, col):
        '''convert row, column into a tuple and check if this tuple is present in the data member of list of tuples
        if yes then decrease number of atoms return true
        else decrease score by 5 and return false'''

        if self.__board[row][col] == -1:
            if (row, col) not in self.__list_of_visits:
                self.__atoms = self.__atoms - 1
                self.__list_of_visits.append((row, col))
            return True

        if (row, col) in self.__list_of_visits:
            return False

        if self.__board[row][col] == 0:
            self.__list_of_visits.append((row, col))  # so if they guess the same
            self.__score = self.__score - 5
            return False

        return False



    def get_score(self):
        '''This method that takes no parameters and returns the current score.'''
        return self.__score

    def atoms_left(self):
        '''This method takes no parameters and returns the number of atoms that haven't been guessed yet.'''
        return self.__atoms

    # Helper methods
    def print_board(self):
        '''This method prints the board'''
        for i in self.__board:
            print(i)

    # Method returns True if specified row and col is a corner square
    def is_corner_square(self ,row, col):
        if row == 0 and (col == 9 or col == 0):
            return True
        if row == 9 and (col == 9 or col == 0):
            return True

        return False


    def is_nonborder_square(self ,row, col):
        """Method returns True if specified row and col is a nonborder square"""
        if row == 0 or row == 9 or col == 0 or col == 9:
            return False
        return True

    def check(self ,row ,col):
        """Helper function used to check whether the index are valid or not for the board"""
        if row >= 0 and row <= 9 and col >= 0 and col <= 9:
            return True
        else:
            return False

    # # Controls
    # def move_up():
    #     self.__current_position[1] += 1

    # def move_down():
    #     self.__current_position[1] -= 1


    # def move_right():
    #     self.__current_position[0] += 1

    # def move_left():
    #     self.__current_position[0] -= 1


    # def is_atom_adjacent(row, col):
    #     if self.__board[row + 1][col + 1] == -1 or self.__board[row - 1][col - 1] == -1 or self.__board
    #     return None


# Here's a very simple example of how the class could be used:

#game = BlackBoxGame([(3 ,2), (1, 7), (4, 6), (8, 8)])
#move_result = game.shoot_ray(3, 9)
#game.shoot_ray(0, 2)
#guess_result = game.guess_atom(5, 5)
#score = game.get_score()
#atoms = game.atoms_left()
