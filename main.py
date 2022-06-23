def greeting():
    print("  Hello everyone!")
    print("-------------------")
    print("Welcome to the game")
    print("   Tic-Tac-Toe   ")
    print("-------------------")
    print("Do you know the rules of the game?")
    print("Enter YES, if you do")
    print("Or NO, if you would like to see them")
    print("-------------------")
    answer = input('Your answer:').upper()
    if answer == 'NO':
        print("----------------------------------------")
        print("The rules:")
        rules = """
        The game is played on a grid that's 3 squares by 3 squares.
        You are X, your friend (or the computer in this case) is O. 
        Players take turns putting their marks in empty squares.
        The first player to get 3 of her marks in a row (up, down, across, or diagonally) is the winner.
        When all 9 squares are full, the game is over.
        """
        print(rules)

    print("----------------------------------------")
    print("Stroke input principle: x  y ")
    print("  Where x is a line number")
    print("  And y is a column number.")
    print("So let's start the game! Good luck!")


greeting()

field = [[" "] * 3 for i in range(3)]


def show_field():
    print()
    print("    | 0 | 1 | 2 | ")
    print("-----------------")
    for i, row in enumerate(field):
        row_string = f"  {i} | {' | '.join(row)} | "
        print(row_string)
        print("-----------------")


def ask_coordinates():
    while True:
        coordinates = input("Your stroke: ").split()

        if len(coordinates) != 2:
            print("You didn't enter two coordinates. Try again.")
            continue

        x, y = coordinates

        if not (x.isdigit()) or not (y.isdigit()):
            print("You entered something wrong. Use digits instead.")
            continue

        x, y = int(x), int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print("The coordinates out of range. Try again.")
            continue

        if field[x][y] != " ":
            print("This cell is already taken. Try another one.")
            continue

        return x, y


def check_winning_positions():
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        chars = []
        for c in cord:
            chars.append(field[c[0]][c[1]])
        if chars == ["X", "X", "X"]:
            print("X has won the game! Congratulations!")
            print("---------------------------------")
            return True
        if chars == ["0", "0", "0"]:
            print("0 has won the game! Congratulations!")
            print("---------------------------------")
            return True
    return False


def gaming_process():
    count = 0
    while True:
        count += 1
        show_field()
        if count % 2 == 1:
            print("Now your turn, X!")
        else:
            print("Now your turn, 0!")

        x, y = ask_coordinates()

        if count % 2 == 1:
            field[x][y] = "X"
        else:
            field[x][y] = "0"

        if check_winning_positions():
            break

        if count == 9:
            print("You have a draw.")


def next_try():
    your_answer = input("Do you want to play again? \nEnter YES or NO. \nAnswer: ").upper()
    while True:
        if your_answer == 'YES':
            global field
            field = [[" "] * 3 for i in range(3)]
            gaming_process()
            next_try()
        else:
            print("It was an amazing game. Goodbye!")
        return False


gaming_process()
next_try()
