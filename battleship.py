from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "You are trying to make a shot out of the board!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "You have already did a shot in this cell."


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, length, o):
        self.bow = bow
        self.length = length
        self.o = o
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoot(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("The ship is destroyed!")
                    return False
                else:
                    print("The ship is wounded!")
                    return True

        self.field[d.x][d.y] = "."
        print("Shot missed!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Computer's turn: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn: ").split()

            if len(cords) != 2:
                print(" Write down 2 coordinates properly. ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" You didn't write the digits. Try again! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = False

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greeting(self):
        print("-------------------")
        print("  Hello everyone!  ")
        print(" Welcome to the game  ")
        print("    Battleship    ")
        print("-------------------")
        print("Do you know the rules of the game?")
        print("Enter YES, if you do")
        print("Or NO, if you would like to see them")
        print("-------------------")
        answer = input("Your answer: ").upper()
        if answer == "NO":
            print("""Battleships may be placed either horizontally or vertically, not diagonally. 
            Battleships may not overlap. Battleships may not cover numbers or letters.
            Battleships must be entirely on the grid.
            If you hit an enemy ship, you have one more bonus move.""")
        print("-------------------")
        print("Stroke input principle: x  y ")
        print("  Where x is a line number")
        print("  And y is a column number.")
        print("So let's start the game! Good luck!")

    def print_boards(self):
        print("-" * 20)
        print("Your board:")
        print(self.us.board)
        print("-" * 20)
        print("The computer's board:")
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-" * 20)
                print("Now is your turn.")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Now is computer's turn.")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("You are the winner! Congratulation!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("The computer has won!")
                break
            num += 1

    def start(self):
        self.greeting()
        self.loop()
        self.next_try()

    def next_try(self):
        your_answer = input("Do you want to play again? \nEnter YES or NO. \nAnswer: ").upper()
        while True:
            if your_answer == 'YES':
                self.__init__()
                self.random_board()
                self.random_place()
                self.print_boards()
                self.loop()
                self.next_try()
            else:
                print("It was an amazing game. Goodbye!")
            return False


g = Game()
g.start()
