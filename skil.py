from penguin_game import *

def sort_distance(game, current):
    distances = [current.get_turns_till_arrival(ice) for ice in game.get_all_icebergs()]
    distances_ices = {distances[i]:game.get_all_icebergs()[i] for i in range(len(game.get_all_icebergs()))}
    ices_numbers = {game.get_all_icebergs()[i]:i for i in range(len(game.get_all_icebergs()))}
    distances = sorted(distances)
    
    distances = [distances_ices[distance] for distance in distances]
    final = [[ices_numbers[distance], distance] for distance in distances]
    
    return final[1:]

def do_turn(game):
    penguins = [ice.penguin_amount for ice in game.get_all_icebergs()]
    for p, penguin in enumerate(penguins):
        if game.get_all_icebergs()[p] not in game.get_my_icebergs():
            penguins[p] = -penguin
    
    needs_saving = [0 for _ in range(len(game.get_all_icebergs()))]
    free = [0 for _ in range(len(game.get_all_icebergs()))]
    
    for i, ice in enumerate(game.get_all_icebergs()):
        for group in game.get_all_penguin_groups():
            if group.destination == ice:
                if group in game.get_my_penguin_groups():
                    penguins[i] += group.penguin_amount
                else:
                    penguins[i] -= group.penguin_amount
    
    for i, ice in enumerate(game.get_all_icebergs()):
        if ice in game.get_my_icebergs():
            if penguins[i] <= 0:
                needs_saving[i] = -penguins[i] + 1
            else:
                free[i] = penguins[i] - 1
    
    for i, ice in enumerate(game.get_all_icebergs()):
        if ice in game.get_my_icebergs():
            sorted_distance = sort_distance(game, ice)
            
            if needs_saving[i] > 0:
                for f, [_, friend] in enumerate(sorted_distance):
                    if needs_saving[i] > 0:
                        if friend in game.get_my_icebergs():
                            if needs_saving[f] == 0:
                                if free[i] > needs_saving[i]:
                                    friend.send_penguins(ice, needs_saving[i])
                                    free[f] -= needs_saving[i]
                                else:
                                    friend.send_penguins(ice, free[f])
                                    free[f] = 0
            else:
                cost = ice.upgrade_cost
                
                if -penguins[sorted_distance[0][0]] + -penguins[sorted_distance[1][0]] + 2 > cost and ice.level < ice.upgrade_level_limit:
                    if free[i] > cost:
                        ice.upgrade()
                else:
                    for s, [_, stranger] in enumerate(sorted_distance):
                        needed = -penguins[s] + 1
                        needed += stranger.penguins_per_turn * ice.get_turns_till_arrival(stranger)
                        if free[i] > needed:
                            ice.send_penguins(stranger, -penguins[s] + 1)
