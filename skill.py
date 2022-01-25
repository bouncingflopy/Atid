from penguin_game import *

def sort_moving(game, moving):
    moves = []
    
    for i in range(len(moving)):
        small_am = 300
        small = []
        
        for move in moving:
            if move not in moves:
                if move[1] < small_am:
                    small_am = move[1]
                    small = move
        
        moves.append(small)
    
    return moves

def get_owner(game):
    owner = [0 for _ in range(len(game.get_all_icebergs()))]
    for i, ice in enumerate(game.get_all_icebergs()):
        if ice in game.get_my_icebergs():
            owner[i] = 1
        elif ice in game.get_enemy_icebergs():
            owner[i] = -1
    
    return owner

def get_needed(game):
    owner = get_owner(game)
    ices = [[ice.penguin_amount, ice.level, owner[i]] for i, ice in enumerate(game.get_all_icebergs())]
    moving = [[] for _ in range(len(game.get_all_icebergs()))]
    needed = [0 for _ in range(len(game.get_all_icebergs()))]
    turns = [0 for _ in range(len(game.get_all_icebergs()))]
    free = [0 for _ in range(len(game.get_all_icebergs()))]
    
    for i, ice in enumerate(game.get_all_icebergs()):
        
        # moving
        for g in game.get_all_penguin_groups():
            if g.destination == ice:
                if g.source in game.get_my_icebergs():
                    moving[i].append([g.penguin_amount, g.turns_till_arrival])
                else:
                    moving[i].append([-g.penguin_amount, g.turns_till_arrival])
        
        # ices
        moving_sorted = sort_moving(game, moving[i])
        current_move = 0
        lowest = ices[i][0]
        for move in moving_sorted:
            if move != []:
                if ices[i][2] != 0:
                    ices[i][0] += ices[i][1] * (move[1] - current_move)
                
                if ices[i][0] < lowest:
                    lowest = ices[i][0]
                
                if move[0] > 0:
                    if ices[i][2] == 1:
                        ices[i][0] += move[0]
                    else:
                        ices[i][0] -= move[0]
                        if ices[i][0] < 0:
                            ices[i][0] = -ices[i][0]
                            ices[i][2] = 1
                else:
                    if ices[i][2] == -1:
                        ices[i][0] += -move[0]
                    else:
                        ices[i][0] -= -move[0]
                        if ices[i][0] < 0:
                            ices[i][0] = -ices[i][0]
                            ices[i][2] = -1
                            
                if ices[i][0] < lowest:
                    lowest = ices[i][0]
                current_move = move[1]
                turns[i] = move[1]
        if lowest > 0:
            free[i] = lowest
        
    # needed
    for i in range(len(needed)):
        if ices[i][2] != 1:
            needed[i] = ices[i][0] + 1
    
    return needed, turns, free

def sort_needed(game, needed, turns, current):
    ices = game.get_all_icebergs()
    needed_sorted = [0 for _ in range(len(needed))]
    
    for i, need in enumerate(needed):
        if turns[i] >= current.get_turns_till_arrival(ices[i]):
            needed_sorted[i] = need
        else:
            needed_sorted[i] = need
            needed_sorted[i] += ices[i].penguins_per_turn * (current.get_turns_till_arrival(ices[i]) - turns[i])
    
    return needed_sorted

def sort_distance(game, current):
    ices = game.get_all_icebergs()
    ices_numbers = {ices[i]:i for i in range(len(ices))}
    distances = [current.get_turns_till_arrival(ice) for ice in ices]
    distances_ices = {distances[i]:ices[i] for i in range(len(ices))}
    
    distances = sorted(distances)
    sorted_distances = [distances_ices[distance] for distance in distances]
    sorted_distances = [[ices_numbers[ice], ice] for ice in sorted_distances]
    
    return sorted_distances

def do_turn(game):
    needed, turns, free = get_needed(game)
    
    for i, ice in enumerate(game.get_all_icebergs()):
        if ice in game.get_my_icebergs():
            
            if needed[i] > 0:
                f = 0
                used = []
                
                while needed[i] > 0 and len(used) < len(game.get_all_icebergs()):
                    friend = game.get_all_icebergs()[f]
                    
                    if friend in game.get_my_icebergs():
                        if friend not in used:
                            if needed[f] <= 0:
                                if free[f] > needed[i]:
                                    friend.send_penguins(ice, needed[i])
                                    needed[i] = 0
                                else:
                                    friend.send_penguins(ice, free[f])
                    
                    used.append(friend)
                    f += 1
            else:
                if ice.level < ice.upgrade_level_limit:
                    cost = ice.upgrade_cost
                    needed_sorted = sort_needed(game, needed, turns, ice)
                    
                    if cost < needed_sorted[0] + needed_sorted[1]:
                        if free[i] > cost:
                            ice.upgrade()
                    else:
                        # attack
                        sorted_distances = sort_distance(game, ice)
                        
                        for s, stranger in sorted_distances:
                            if turns[s] > ice.get_turns_till_arrival(stranger):
                                need = needed[s]
                            else:
                                need = needed[s]
                                need += stranger.penguins_per_turn * (ice.get_turns_till_arrival(stranger) - turns[s])
                            
                            if free[i] > need + 1 and stranger not in game.get_my_icebergs():
                                ice.send_penguins(stranger, need + 1)
