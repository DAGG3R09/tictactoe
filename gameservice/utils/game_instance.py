

def check_winning_state(new_state, row, col):
    symbol = new_state[row][col]

    print(">>>>", new_state, symbol)

    flag = True
    for i in range(0, 3):
        if new_state[i][col] != symbol:
            flag = False
            break

    if flag:
        return True

    flag = True
    for i in range(0, 3):
        if new_state[row][i] != symbol:
            flag = False

    if flag:
        return True

    # // check diagonals
    r1 = 0
    c1 = 0
    while r1 < 3:
        if new_state[r1][c1] != symbol:
            break
        r1 += 1
        c1 += 1

    if r1 == 3:
        return True

    r1 = 0
    c1 = 2
    while r1 < 3:
        if new_state[r1][c1] != symbol:
            break
        r1 += 1
        c1 -= 1

    if r1 == 3:
        return True

    return False


if __name__ == "__main__":
    # c = [["X",None, None],[None, "X", None],[None, None, "X"]]
    c = [["O",None, None],["O", "X", None],["O", None, None]]
    print(check_winning_state(c, 0, 2))
