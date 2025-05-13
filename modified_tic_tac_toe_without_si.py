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


def is_opponent_piece(tab, i, j, player):
    opp = "O" if player == "X" else "X"
    return tab[i][j] == opp


def has_opponent_pieces(tab, player):
    opp = "O" if player == "X" else "X"
    return any(opp in row for row in tab)


def change_piece(tab, i, j, player):
    orig = tab[i][j]
    if orig in (" ", player):
        return False
    tab[i][j] = player
    # jeżeli po podmianie ktokolwiek wygrywa – cofamy
    opp = "O" if player == "X" else "X"
    for y in range(3):
        for x in range(3):
            if check_win(tab, y, x, opp) or check_win(tab, y, x, player):
                tab[i][j] = orig
                return False
    return True


def print_board(tab):
    print("X → 0   1   2")
    print("  +---+---+---+")
    for idx, row in enumerate(tab):
        print(f"{idx} | " + " | ".join(row) + " |")
        print("  +---+---+---+")


def main():
    tab = [[" "] * 3 for _ in range(3)]
    cur = "X"
    moves = 0
    switched = {"X": False, "O": False}

    while moves < 9:
        print_board(tab)
        print(f"Runda {moves + 1}, gracz {cur}")

        can_switch = has_opponent_pieces(tab, cur) and not switched[cur]
        # instrukcja dla gracza
        if can_switch:
            print("Masz pionki przeciwnika – możesz:")
            print(" • postawić nowy: podaj 'X Y' (np. 0 2)")
            print(" • podmienić: podaj 'X Y C' (C = change), np. 1 1 C")
        else:
            print("Podaj współrzędne X Y (np. 0 0), by postawić swój pionek.")

        # odczyt i walidacja
        while True:
            parts = input("Twój ruch: ").split()
            # POSTAWIENIE
            if len(parts) == 2:
                try:
                    j, i = map(int, parts)
                    if 0 <= i <= 2 and 0 <= j <= 2 and tab[i][j] == " ":
                        tab[i][j] = cur
                        break
                except:
                    pass
                print("Nieprawidłowe pole lub pole zajęte.")

            # PODMIANA
            elif len(parts) == 3 and parts[2].upper() == "C":
                try:
                    j, i = map(int, parts[:2])
                    if can_switch and is_opponent_piece(tab, i, j, cur):
                        if change_piece(tab, i, j, cur):
                            switched[cur] = True
                            break
                        else:
                            print("Taki ruch jest niedozwolony (byłby wygrywający).")
                            continue
                except:
                    pass
                print("Nieprawidłowe podmiana pionka.")

            else:
                print("Niepoprawny format. Spróbuj jeszcze raz.")

        moves += 1

        # sprawdź, czy wygrałeś
        if check_win(tab, i, j, cur):
            print_board(tab)
            print(f"Gracz {cur} wygrał! 🎉")
            return

        cur = "O" if cur == "X" else "X"

    print_board(tab)
    print("Remis – plansza pełna.")


if __name__ == "__main__":
    main()
