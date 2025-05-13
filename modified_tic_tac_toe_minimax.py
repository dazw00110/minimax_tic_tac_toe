import copy

def check_win(tab, i, j, player):
    if all(tab[i][x] == player for x in range(3)): return True
    if all(tab[x][j] == player for x in range(3)): return True
    if tab[1][1] == player:
        if tab[0][0] == player and tab[2][2] == player: return True
        if tab[0][2] == player and tab[2][0] == player: return True
    return False

def get_moves(tab, player, swaps):
    moves = []
    opp = 'O' if player == 'X' else 'X'
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
        print(f"Runda {moves + 1}, gracz {current}")

        if current == 'X':
            # AI
            pass
        else:
            # Ty (O)
            pass
        
        moves += 1
        current = 'X' if current == 'O' else 'O'
        
if __name__ == '__main__':
    main()
