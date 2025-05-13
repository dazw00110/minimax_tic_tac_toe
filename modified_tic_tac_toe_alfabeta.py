import copy
import time

def check_win(tab, i, j, player):
    if all(tab[i][x] == player for x in range(3)): return True
    if all(tab[x][j] == player for x in range(3)): return True
    if tab[1][1] == player:
        if tab[0][0] == player and tab[2][2] == player: return True
        if tab[0][2] == player and tab[2][0] == player: return True
    return False

def get_moves(tab, player, swaps):
    moves = []
    opp = 'O' if player=='X' else 'X'
    for i in range(3):
        for j in range(3):
            if tab[i][j] == ' ':
                moves.append((i, j, 'place'))
            if swaps[player] > 0 and tab[i][j] == opp:
                tmp = copy.deepcopy(tab)
                tmp[i][j] = player
                if not check_win(tmp, i, j, player):
                    moves.append((i, j, 'swap'))
    return moves

def apply_move(tab, move, player, swaps):
    i, j, typ = move
    new_tab = copy.deepcopy(tab)
    new_swaps = swaps.copy()
    new_tab[i][j] = player
    if typ == 'swap':
        new_swaps[player] -= 1
    return new_tab, new_swaps

def game_over_score(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ' and check_win(board, i, j, board[i][j]):
                return 1000 if board[i][j] == 'X' else -1000
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 0
    return None

def evaluate(board):
    return check_blocking(board) + check_center(board) + check_two_in_row(board)

def minimax(tab, player, swaps):
    score = evaluate(tab)
    if score != 0 or all(tab[i][j] != ' ' for i in range(3) for j in range(3)):
        return score, None
    best_val = -99 if player=='X' else 99
    best_move = None
    for move in get_moves(tab, player, swaps):
        child_tab, child_swaps = apply_move(tab, move, player, swaps)
        val, _ = minimax(child_tab, 'O' if player=='X' else 'X', child_swaps)
        if (player=='X' and val > best_val) or (player=='O' and val < best_val):
            best_val, best_move = val, move
    return best_val, best_move

def game_over_score(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ' and check_win(board, i, j, board[i][j]):
                return 1000 if board[i][j] == 'X' else -1000
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 0
    return None

# Heurystyka: blocking + center + two-in-row
def evaluate(board):
    return check_blocking(board) + check_center(board) + check_two_in_row(board)


def print_board(tab):
    print("X → 0   1   2")
    print("  +---+---+---+")
    for idx,row in enumerate(tab):
        print(f"{idx} | " + " | ".join(row) + " |")
        print("  +---+---+---+")
    print("↓\nY\n")


def main():
    tab = [[" "]*3 for _ in range(3)]
    swaps = {'X': 1, 'O': 1}
    current = 'O'   # Ty zaczynasz jako O
    moves = 0
    last_i = last_j = 0

    while moves < 9:
        print_board(tab)
        print(f"Runda {moves+1}, gracz {current}")

        if current == 'X':
            # AI
            print("Komputer myśli…")
            start_time = time.time()
            _, move = minimax(tab, 'X', swaps)
            end_time = time.time()
            tab, swaps = apply_move(tab, move, 'X', swaps)
            last_i, last_j = move[0], move[1]
            print(f"Komputer posunął się na {move[1]} {move[0]}")
            print(f"Czas myślenia: {end_time - start_time:.2f} sekund")
        else:
            # Ty (O)
            has_opp = any(cell == 'X' for row in tab for cell in row)
            print("\nWspółrzędne podawaj jako dwie liczby od 0 do 2, oddzielone spacją.")
            print("Masz pionki przeciwnika – możesz:")
            print(" • postawić nowy: podaj 'X Y' (np. '0 2')")
            if has_opp and swaps['O'] > 0:
                print(" • podmienić:    podaj 'X Y C' (C = change), np. '1 1 C'")

            while True:
                try:
                    cmd = input("Twój ruch: ").strip().split()
                    if len(cmd) == 2:
                        try:
                            j, i = map(int, cmd)
                            if 0 <= i < 3 and 0 <= j < 3:
                                if tab[i][j] == ' ':
                                    tab[i][j] = 'O'
                                    last_i, last_j = i, j
                                    break
                                else:
                                    print("To pole jest już zajęte!")
                            else:
                                print("Współrzędne muszą być z zakresu 0-2!")
                        except ValueError:
                            print("Współrzędne muszą być liczbami całkowitymi!")
                    elif len(cmd) == 3 and has_opp and swaps['O'] > 0 and cmd[2].upper() == 'C':
                        try:
                            j, i = map(int, cmd[:2])
                            if 0 <= i < 3 and 0 <= j < 3:
                                if tab[i][j] == 'X':
                                    tmp = copy.deepcopy(tab)
                                    tmp[i][j] = 'O'
                                    if not check_win(tmp, i, j, 'O'):
                                        tab[i][j] = 'O'
                                        swaps['O'] -= 1
                                        last_i, last_j = i, j
                                        break
                                    else:
                                        print("Ten ruch spowodowałby natychmiastową wygraną!")
                                else:
                                    print("Możesz podmienić tylko pionek przeciwnika (X)!")
                            else:
                                print("Współrzędne muszą być z zakresu 0-2!")
                        except ValueError:
                            print("Współrzędne muszą być liczbami całkowitymi!")
                    else:
                        print("Niepoprawny format ruchu!")
                except Exception as e:
                    print("Wystąpił błąd. Spróbuj ponownie.")

        moves += 1
        if check_win(tab, last_i, last_j, current):
            print_board(tab)
            print(f"Gracz {current} wygrał!")
            return
        if moves == 9:
            print_board(tab)
            print("Remis!")
            return

        current = 'X' if current == 'O' else 'O'


if __name__ == '__main__':
    main()