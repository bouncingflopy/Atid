from penguin_game import *

def get_turns(game):
    ices = game.get_all_icebergs()
    groups = [[] for _ in range(len(ices))]
    turns_by_ice = [[[ice.penguin_amount, ice.owner]] for ice in range(len(ice))]
    
    for g, group in enumerate(game.get_all_penguin_groups()):
        for i, ice in enumerate(ices):
            if group.destination == ice:
                groups[i].append(group)
    for i, ice in enumerate(ices):
        for t in range(game.max_turns - game.turn):
            turn = game.turns + t
            
            if not group.owner.equals(game.get_neutral()):
                turns_by_ice[i].append([turns_by_ice[i][-1][0] + ice.penguins_per_turn, turns_by_ice[i][-1][1]])
            else:
                turns_by_ice[i].append(turns_by_ice[i][-1])
            
            for group in groups[i]:
                if group.turns_till_arrival + game.turn == turn:
                    if group.owner.equals(turns_by_ice[i][-1]):
                        turns_by_ice[i][-1][0] += group.penguin_amount
                    else:
                        turns_by_ice[i][-1][0] -= group.penguin_amount
                        if turns_by_ice[i][-1][0] <= 0:
                            turns_by_ice[i][-1][0] *= -1
                            turns_by_ice[i][-1][1] = group.owner
    
    turns_by_turn = [[[turns_by_ice[i][t + game.turn]] for i in range(len(ices))] for t in range(game.max_turns - game.turn)]
    
    return turns_by_ice, turns_by_turn

def get_freedom(game, ices, turns_by_ice, turns_by_turn):
    lowest = [[ice.penguin_amount, game.turn] for ice in ices]
    last_transfer = [0 for _ in ices]
    needs_saving = [[0, 0] for _ in ices]
    
    for i, turns for enumerate(turns_by_ice):
        for t, turn in enumerate(turns):
            if turn[1].equals(ices[i].owner):
                if turn[0] < lowest[i][0]:
                    lowest[i] = [turn[0], t + game.turn]
            else:
                if -turn[0] < lowest[i][0]:
                    lowest[i] = [-turn[0], t + game.turn]
            
            if t > 0 and not turns[t][1].equals(turns[t-1][1]):
                last_transfer[i] = t + game.turn
    
    for i, ice in enumerate(ices):
        if ice.owner.equals(game.get_myself()):
            if not turns_by_ice[i][last_transfer[i]][1].equals(game.get_myself()):
                needs_saving[i][0] = last_transfer[i]
    
    return lowest, last_transfer, needs_saving
    
def sort_distance(game, current):
    ices = game.get_all_icebergs()
    ices_numbers = {ices[i]:i for i in range(len(ices))}
    distances = [current.get_turns_till_arrival(ice) for ice in ices]
    distances_ices = {distances[i]:ices[i] for i in range(len(ices))}
    distances = sorted(distances)
    
    result = [distances_ices[distance] for distance in distances]
    result = [[ices_numbers[ice], ice] for ice in result]
    
    return result[1:]

def do_turn(game):
    ices = game.get_all_icebergs()
    turns_by_ice, turns_by_turn = get_turns(game)
    lowest, last_transfer, needs_saving - get_freedom(game, ices, turns_by_ice, turns_by_turn)
    
    # saving
    for i, ice in enumerate(ices):
        if needs_saving[i][0] != 0:
            sorted_distance = sort_distance(game, ice)
            
            for f, friend in sorted_distance:
                if friend.owner.equals(game.get_myself()):
                    if needs_saving[f][0] == 0:
                        if ice.get_turns_till_arrival(friend) > needs_saving[i][1]:
                            needs_saving[i][0] = turns_by_ice[i][ice.get_turns_till_arrival(friend) + game.turn][0]
                        
                        friend.send_penguins(ice, lowest[f] - 1)
                        needs_saving[i][0] -= lowest[f] - 1
                        
                        if needs_saving[i][0] < 0:
                            needs_saving[i] = [0, 0]
    
    turns_by_ice, turns_by_turn = get_turns(game)
    lowest, last_transfer, needs_saving - get_freedom(game, ices, turns_by_ice, turns_by_turn)
    
    # upgrading and attacking
    for i, ice in enumerate(ices):
        if ice.owner.equals(game.get_myself()):
            cost = ice.upgrade_cost
            needed = [turns_by_ices[i][ice.get_turns_till_arrival(ices[e]) + game.turns][0] + 1 for e in range(len(ices))
            if not ices[e].owner.equals(game.get_myself()) or not turns_by_ices[i][last_transfer[e]][1].equals(game.get_myself()) else -1]
            sorted_needed = sorted(needed)
            
            first_real = len(ices)
            for n, need in enumerate(needed):
                if need != -1:
                    first_real = n
                    break
            
            if ice.level < ice.upgrade_level_limit and first_real + 1 < len(ices) and cost < sorted_needed[first_real] + sorted_needed[first_real+1]:
                if ice.can_upgrade():
                    ice.upgrade()
            else:
                needed_numbers = {needed[j]:j for j in range(len(ices))}
                
                for need in sorted_needed:
                    if need > -1:
                        if ice.penguin_amount > need:
                            ice.send_penguins(ices[needed_numbers[need]], need)
                            turns_by_ice, turns_by_turn = get_turns(game)
                            lowest, last_transfer, needs_saving - get_freedom(game, ices, turns_by_ice, turns_by_turn)
