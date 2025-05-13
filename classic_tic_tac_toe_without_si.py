def check_win(tab, i, j, player):
    if all(tab[i][x] == player for x in range(3)):
        return True
    if all(tab[x][j] == player for x in range(3)):
        return True
    if tab[1][1] == player:
        if tab[0][0] == player and tab[2][2] == player:
            return True
        if tab[0][2] == player and tab[2][0] == player:
            return True
    return False


def print_board(tab):
    print("X → 0   1   2")
    print("  +---+---+---+")
    for idx, row in enumerate(tab):
        print(f"{idx} | " + " | ".join(row) + " |")
        print("  +---+---+---+")
    print("↓")
    print("Y")



def main():
    tab = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    moves = 0

    while moves < 9:
        print_board(tab)
        print(f"Runda {moves + 1}, Gracz {current_player}:")

        while True:
            try:
                j, i = map(int, input("Podaj współrzędne X (kolumna), Y (wiersz), np. '1 0': ").split())
                if tab[i][j] == " ":
                    break
                else:
                    print("To pole jest już zajęte!")
            except (ValueError, IndexError):
                print("Nieprawidłowe dane. Podaj liczby od 0 do 2.")

        tab[i][j] = current_player
        moves += 1

        if check_win(tab, i, j, current_player):
            print_board(tab)
            print(f"Gracz {current_player} wygrał! Gratulacje!")
            return

        if moves == 9:
            print_board(tab)
            print("Remis! Plansza jest pełna.")
            return

        current_player = "O" if current_player == "X" else "X"


main()
