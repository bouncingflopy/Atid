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
        
        moves[i] = small
    
    return moves

def get_owner(game):
    owner = [0 for _ in range(len(game.get_all_icebergs))]
    for i, ice in enumerate(game.get_all_icebergs()):
        if ice in game.get_my_icebergs():
            owner[i] = 1
        else if ice in game.get_enemy_icebergs():
            owner[i] = -1
    
    return owner

def get_needed(game):
    owner = get_owner(game)
    ices = [[ice.penguin_amount, ice.level, owner[i]] for i, ice in enumerate(game.get_all_icebergs())]
    moving = [[] for _ in range(len(game.get_all_icebergs))]
    needed = [0 for _ in range(len(game.get_all_icebergs))]
    turns = [0 for _ in range(len(game.get_all_icebergs))]
    
    for i, ice in enumerate(game.get_all_icebergs()):
        
        # moving
        for g in game.get_all_penguin_groups():
            if g.destination == ice:
                if g.source in game.get_my_icebergs():
                    moving[i] = [g.penguin_amount, g.turns_till_arrival]
                else:
                    moving[i] = [-g.penguin_amount, g.turns_till_arrival]
        
        # ices
        moving_sorted = sort_moving(game, moving[i])
        for move in moving_sorted:
            if ices[i][2] != 0:
                ices[i][0] += ices[i][1] * move[1]
            
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
            
            turns[i] = move[1]
        
    # needed
    for i in range(len(needed):
        if ices[i][2] != 1:
            needed[i] = ices[i][0] + 1
    
    return needed, turns

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
    sorted_distances = {ices_numbers[ice]:ice for ice in sorted_distances}
    
    return sorted_distances

def do_turn(game):
    needed, turns = get_needed(game)
    
    for i, ice in enumerate(game.get_all_icebergs()):
        
        if ice in game.get_my_icebergs():
            f = 0
            used = []
            
            while needed[i] > 0 and len(used) <= len(game.get_all_icebergs()):
                f += 1
                friend = game.get_all_icebergs()[f]
                
                if friend in game.get_my_icebergs():
                    if friend not in used:
                        if needed[f] <= 0:
                            if friend.penguin_amount > needed[i]:
                                friend.send_penguins(ice, needed[i])
                                needed[i] = 0
                            else:
                                friend.send_penguins(ice, friend.penguin_amount)
                used.append(friend)
        else:
            if ice.level < ice.upgrade_level_limit:
                cost = ice.upgrade_cost
                needed_sorted = sort_needed(game, needed, turns, current)
                
                if cost < needed_sorted[0] + needed_sorted[1]:
                    if ice.can_upgrade:
                        ice.upgrade()
                else:
                    # attack
                    sorted_distances = sort_distance(game, current)
                    
                    for e, enemy in sorted_distances:
                        if turns[e] > ice.get_turns_till_arrival(enemy):
                            need = needed[e]
                        else:
                            need = needed[e]
                            need += enemy.penguins_per_turn * (ice.get_turns_till_arrival(enemy) - turns[e])
                        
                        free = ice.penguin_amount - needed[i]
                        if free > need + 1:
                            ice.send_penguins(enemy, need + 1)
