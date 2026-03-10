import time


class Vector:
    """
    Implement the methods below to create a 3D vector class.

    Magic methods cheatsheet: https://rszalski.github.io/magicmethods
    """

    """
    Implement a constructor that takes three coordinates (x, y, z) and stores
    them as attributes with the same names in the Vector.
    Default value for all coordinates should be 0.
    Example:
        v = Vector(1.2, 3.5, 4.1)
        v.x # 1.2
        v = Vector(z=1) # == Vector(0, 0, 1)
    """
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    """
    Implement vector addition and subtraction using `+` and `-` operators.
    Both operators should return a new vector and not modify its operands.
    If the second operand isn't a vector, raise ValueError.
    Example:
        Vector(1, 2, 3) + Vector(4, 5, 6) # Vector(5, 7, 8)
        Vector(1, 2, 3) - Vector(4, 5, 6) # Vector(-3, -3, -3)
    Hint:
        You can use isinstance(object, class) to check whether `object` is an instance of `class`.
    """
    def __add__(self, vec):
        if isinstance(vec, Vector):
            return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)
        else:
            raise ValueError
        
    def __sub__(self, vec):
        if isinstance(vec, Vector):
            return Vector(self.x - vec.x, self.y - vec.y, self.z - vec.z)
        else:
            raise ValueError
    """
    Implement the `==` comparison operator for Vector that returns True if both vectors have the same attributes.
    If the second operand isn't a vector, return False.
    Example:
        Vector(1, 1, 1) == Vector(1, 1, 1)  # True
        Vector(1, 1, 1) == Vector(2, 1, 1)  # False
        Vector(1, 2, 3) == 5                # False
    """
    def __eq__(self, vec):
        if not isinstance(vec, Vector):
            return False
        elif vec.x == self.x and vec.y == self.y and vec.z == self.z:
            return True
        else:
            return False
    
        
    """
    Implement string representation of Vector in the form `(x, y, z)`.
    Example:
        str(Vector(1, 2, 3))    # (1, 2, 3)
        print(Vector(0, 0, 0))  # (0, 0, 0)
    """
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    """
    Implement indexing for the vector, both for reading and writing.
    If the index is out of range (> 2), raise IndexError.
    Example:
        v = Vector(1, 2, 3)
        v[0] # 1
        v[2] # 3
        v[1] = 5 # v.y == 5

        v[10] # raises IndexError
    """
    def __getitem__(self, index):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case _:
                raise IndexError
    
    def __setitem__(self, index, value):
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case 2:
                self.z = value
            case _:
                raise IndexError
    
    """
    Implement the iterator protocol for the vector.
    Hint:
        Use `yield`.
    Example:
        v = Vector(1, 2, 3)
        for x in v:
            print(x) # prints 1, 2, 3
    """
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    
class Observable:
    """
    Implement the `observer` design pattern.
    Observable should have a `subscribe` method for adding new subscribers.
    It should also have a `notify` method that calls all of the stored subscribers and passes them its parameters.
    Example:
        obs = Observable()

        def fn1(x):
            print("fn1: {}".format(x))

        def fn2(x):
            print("fn2: {}".format(x))

        unsub1 = obs.subscribe(fn1)     # fn1 will be called everytime obs is notified
        unsub2 = obs.subscribe(fn2)     # fn2 will be called everytime obs is notified
        obs.notify(5)                   # should call fn1(5) and fn2(5)
        unsub1()                        # fn1 is no longer subscribed
        obs.notify(6)                   # should call fn2(6)
    """

    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        """
        Add subscriber to collection of subscribers.
        Return a function that will remove this subscriber from the collection when called.
        """
        self.subscribers.append(subscriber)

        def unsubscribe():
            self.subscribers.remove(subscriber)
        return unsubscribe

    def notify(self, *args, **kwargs):
        """
        Pass all parameters given to this function to all stored subscribers by calling them.
        """
        for sub in self.subscribers:
            sub(*args, **kwargs)


class UpperCaseDecorator:
    """
    Implement the `decorator` design pattern.
    UpperCaseDecorator should decorate a file which will be passed to its constructor.
    It should make all lower case characters written to the file uppercase and remove all
    upper case characters.
    It is enough to support the `write` and `writelines` methods of file.
    Example:
        with open("file.txt", "w") as f:
            decorated = UpperCaseDecorator(f)
            decorated.write("Hello World\n")
            decorated.writelines(["Nice to MEET\n", "YOU"])

        file.txt content after the above code is executed:
        ELLO ORLD
        ICE TO

    """
    def __init__(self, file):
        self.file = file

    def write(self, message):
        final_text = ""
        for char in message:
            if char.islower():
                final_text = final_text + char.upper()
            elif not char.isupper():
                final_text = final_text + char
        self.file.write(final_text)


    def writelines(self, str_list):
        for line in str_list:
            final_text = ""
            for char in line:
                if char.islower():
                    final_text = final_text + char.upper()
                elif not char.isupper():
                    final_text = final_text + char
            self.file.write(final_text)

class GameOfLife:
    """
    Implement "Game of life" (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

    The game board will be represented with nested tuples, where '.'
    marks a dead cell and 'x' marks a live cell. Cells that are out of bounds of the board are
    assumed to be dead. The board grid will always be a square.

    Try some patterns from wikipedia + the provided tests to test the functionality.

    The GameOfLife objects should be immutable, i.e. the move method will return a new instance
    of GameOfLife.

    Example:
        game = GameOfLife((
            ('.', '.', '.'),
            ('.', 'x', '.'),
            ('.', 'x', '.'),
            ('.', 'x', '.'),
            ('.', '.', '.')
        ))
        game.alive()    # 3
        game.dead()     # 12
        x = game.move() # 'game' doesn't change
        # x.board:
        (
            ('.', '.', '.'),
            ('.', '.', '.'),
            ('x', 'x', 'x'),
            ('.', '.', '.'),
            ('.', '.', '.')
        )

        str(x)
        ...\n
        ...\n
        xxx\n
        ...\n
        ...\n
    """

    def __init__(self, board):
        """
        Create a constructor that receives the game board and stores it in an attribute called
        'board'.
        """
        self.board = board

    def move(self):
        """
        Simulate one iteration of the game and return a new instance of GameOfLife containing
        the new board state.
        """
        new_bord = [list(row) for row in self.board]
        rows = len(self.board)
        cols = len(self.board[0])


        for cell_row in range(rows):
            for cell_col in range(cols):
                alive_neigh_count = 0
                for r in range(-1, 2):
                    for c in range(-1, 2):
                        if not (r == 0 and c ==0) and 0 <= cell_row + r < rows and cell_col + c <cols and cell_col + c >= 0:
                            alive_neigh_count += self.board[cell_row + r][cell_col + c] == "x"

                if alive_neigh_count < 2 or alive_neigh_count > 3:
                    new_bord[cell_row][cell_col] = "."

                elif alive_neigh_count == 3 and self.board[cell_row][cell_col] == ".":
                    new_bord[cell_row][cell_col] = "x"
                else:
                    new_bord[cell_row][cell_col] = self.board[cell_row][cell_col]

        final_board = tuple(tuple(row) for row in new_bord)

        return GameOfLife(final_board)

    def alive(self):
        """
        Return the number of cells that are alive.
        """
        count = 0
        rows = len(self.board)
        cols = len(self.board[0])
        for r in range(rows):
            for c in range(cols):
                if self.board[r][c] == "x":
                    count += 1
        return count


    def dead(self):
        """
        Return the number of cells that are dead.
        """
        rows = len(self.board)
        cols = len(self.board[0])
        all_cells = cols * rows
        return all_cells - self.alive()

    def __repr__(self):
        """
        Return a string that represents the state of the board in a single string (with newlines
        for each board row).
        """
        final_str = ""
        rows = len(self.board)
        cols = len(self.board[0])
        for r in range(rows):
            for c in range(cols):
                final_str += str(self.board[r][c])
            final_str += "\n"

        return final_str

def play_game(game, n):
    """
    You can use this function to render the game for n iterations
    """
    for i in range(n):
        print(game)
        game = game.move()
        time.sleep(0.25)  # sleep to see the output


# this code will only be executed if you run `python tasks.py`
# it will not be executed when tasks.py is imported
if __name__ == "__main__":
    play_game(GameOfLife((
        ('.', '.', '.'),
        ('.', 'x', '.'),
        ('.', 'x', '.'),
        ('.', 'x', '.'),
        ('.', '.', '.'),
    )), 10)
