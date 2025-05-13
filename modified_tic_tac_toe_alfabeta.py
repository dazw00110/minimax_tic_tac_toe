import copy
import time

# Sprawdzenie wygranej (3 w rzędzie)
def check_win(tab, i, j, player):
    if all(tab[i][x] == player for x in range(3)): return True
    if all(tab[x][j] == player for x in range(3)): return True
    if tab[1][1] == player:
        if tab[0][0] == player and tab[2][2] == player: return True
        if tab[0][2] == player and tab[2][0] == player: return True
    return False

# Dostępne ruchy: postaw lub podmień (swap)
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

# Zastosowanie ruchu
def apply_move(tab, move, player, swaps):
    i, j, typ = move
    new_tab = copy.deepcopy(tab)
    new_swaps = swaps.copy()
    new_tab[i][j] = player
    if typ == 'swap':
        new_swaps[player] -= 1
    return new_tab, new_swaps

# Heurystyka: blocking + center + two-in-row
def evaluate(board):
    return check_blocking(board) + check_center(board) + check_two_in_row(board)

# Sprawdzenie, czy gra zakończona: wygrana lub remis
def game_over_score(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ' and check_win(board, i, j, board[i][j]):
                return 1000 if board[i][j] == 'X' else -1000
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 0
    return None

# Sprawdzenie blokowania
def check_blocking(board):
    s = 0
    # blokowanie O przez X
    for i in range(3):
        if board[i].count('O') == 2 and board[i].count(' ') == 1: s += 50
        col = [board[0][i], board[1][i], board[2][i]]
        if col.count('O') == 2 and col.count(' ') == 1: s += 50
    diag1 = [board[0][0], board[1][1], board[2][2]]
    diag2 = [board[0][2], board[1][1], board[2][0]]
    if diag1.count('O') == 2 and diag1.count(' ') == 1: s += 50
    if diag2.count('O') == 2 and diag2.count(' ') == 1: s += 50
    # blokowanie X przez O
    for i in range(3):
        if board[i].count('X') == 2 and board[i].count(' ') == 1: s -= 50
        col = [board[0][i], board[1][i], board[2][i]]
        if col.count('X') == 2 and col.count(' ') == 1: s -= 50
    if diag1.count('X') == 2 and diag1.count(' ') == 1: s -= 50
    if diag2.count('X') == 2 and diag2.count(' ') == 1: s -= 50
    return s

# Sprawdzenie środka planszy
def check_center(board):
    if board[1][1] == 'X': return 1
    if board[1][1] == 'O': return -1
    return 0

# Sprawdzenie dwóch w rzędzie
def check_two_in_row(board):
    s = 0
    for sym, val in [('X', 10), ('O', -10)]:
        for i in range(3):
            if board[i].count(sym) == 2 and board[i].count(' ') == 1: s += val
            col = [board[0][i], board[1][i], board[2][i]]
            if col.count(sym) == 2 and col.count(' ') == 1: s += val
        diag1 = [board[0][0], board[1][1], board[2][2]]
        diag2 = [board[0][2], board[1][1], board[2][0]]
        if diag1.count(sym) == 2 and diag1.count(' ') == 1: s += val
        if diag2.count(sym) == 2 and diag2.count(' ') == 1: s += val
    return s

# Minimax z przycinaniem alfa-beta
def minimax(tab, player, swaps, depth, alpha, beta):
    over = game_over_score(tab)
    if over is not None:
        return over, None
    if depth == 0:
        return evaluate(tab), None

    best_move = None
    if player == 'X':  # maksymalizujemy
        value = -float('inf')
        for move in get_moves(tab, player, swaps):
            child_tab, child_swaps = apply_move(tab, move, player, swaps)
            val, _ = minimax(child_tab, 'O', child_swaps, depth-1, alpha, beta)
            if val > value:
                value, best_move = val, move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # przycinamy
        return value, best_move
    else:  # minimalizujemy
        value = float('inf')
        for move in get_moves(tab, player, swaps):
            child_tab, child_swaps = apply_move(tab, move, player, swaps)
            val, _ = minimax(child_tab, 'X', child_swaps, depth-1, alpha, beta)
            if val < value:
                value, best_move = val, move
            beta = min(beta, value)  # DODANE: aktualizacja beta
            if beta <= alpha:
                break  # przycinamy
        return value, best_move

# Wyświetlanie planszy
def print_board(tab):
    print("X → 0   1   2")
    print("  +---+---+---+")
    for idx,row in enumerate(tab):
        print(f"{idx} | " + " | ".join(row) + " |")
        print("  +---+---+---+")

# Główna pętla gry
def main():
    tab = [[" "]*3 for _ in range(3)]
    swaps = {'X': 1, 'O': 1}
    current = 'O'
    moves = 0
    depth_limit = 6  # ograniczenie głębokości Minimax (max 9 w klasycznym TTT)

    while True:
        print_board(tab)
        print(f"Runda {moves+1}, gracz {current}")

        if current == 'X':
            print("Komputer myśli…")
            start = time.time()
            _, move = minimax(tab, 'X', swaps, depth_limit, -float('inf'), float('inf'))
            end = time.time()
            tab, swaps = apply_move(tab, move, 'X', swaps)
            print(f"Komputer ruch: {move[1]} {move[0]} (czas {end-start:.2f}s)")
        else:
            has_opp = any(cell == 'X' for row in tab for cell in row)
            print("Podaj 'X Y' by postawić pionek.")
            if swaps['O'] > 0 and has_opp:
                print("Aby podmienić pionek X na O, użyj 'X Y C'.")

            while True:
                cmd = input("Twój ruch: ").split()
                if len(cmd) == 2:
                    j, i = map(int, cmd)
                    if 0 <= i < 3 and 0 <= j < 3 and tab[i][j] == ' ':
                        tab[i][j] = 'O'
                        break
                elif len(cmd) == 3 and has_opp and swaps['O'] > 0 and cmd[2].upper() == 'C':
                    j, i = map(int, cmd[:2])
                    if 0 <= i < 3 and 0 <= j < 3 and tab[i][j] == 'X':
                        tmp = copy.deepcopy(tab)
                        tmp[i][j] = 'O'
                        if not check_win(tmp, i, j, 'O'):
                            tab[i][j] = 'O'
                            swaps['O'] -= 1
                            break
                print("Niepoprawny ruch, spróbuj jeszcze raz.")

        moves += 1
        over = game_over_score(tab)
        if over is not None:
            print_board(tab)
            if over == 0:
                print("Remis!")
            else:
                print(f"Gracz { 'X' if over>0 else 'O' } wygrał!")
            return

        current = 'X' if current == 'O' else 'O'

if __name__ == '__main__':
    main()
