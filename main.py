from n_queens import n_queens, print_n_queens


def play_n_queens():
    # n 은 가로 세로 길이
    n = 1
    solver = n_queens(n)
    print_n_queens(solver[0], solver[1], n)


if __name__ == "__main__":
    print("Example number : 1. nQueens, ")
    selected = input("select solver example : ")
    if selected is "1":
        play_n_queens()
