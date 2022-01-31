from penguin_game import *

def get_turns(game):
    ices = game.get_all_icebergs()
    groups = [[] for _ in range(len(ices))]
    turns = [[[ice.penguin_amount, ice.owner.id]] for ice in ices]
    
    for g, group in enumerate(game.get_all_penguin_groups()):
        for i, ice in enumerate(ices):
            if group.destination == ice:
                groups[i].append(group)
    for i, ice in enumerate(ices):
        for t in range(30):
            turn = game.turn + t
            new_penguins = turns[i][-1][0]
            new_owner = turns[i][-1][1]
            
            if not turns[i][-1][1] == game.get_neutral().id:
                new_penguins = turns[i][-1][0] + ice.penguins_per_turn
            
            for group in groups[i]:
                if group.turns_till_arrival + game.turn == turn:
                    if group.owner.id == new_owner:
                        new_penguins += group.penguin_amount
                    else:
                        new_penguins -= group.penguin_amount
                        if new_penguins < 0:
                            new_penguins *= -1
                            new_owner = group.owner.id
                        elif new_penguins == 0:
                            new_owner = game.get_neutral().id
            
            turns[i].append([new_penguins, new_owner])
    
    return turns

def get_freedom(game, ices, turns):
    lowest = [[ice.penguin_amount, game.turn] for ice in ices]
    last_transfer = [game.turn for _ in ices]
    needs_saving = [[0, 0] for _ in ices]
    
    for i in range(len(turns)):
        for t, turn in enumerate(turns[i]):
            if turn[1] == ices[i].owner.id:
                if turn[0] < lowest[i][0]:
                    lowest[i] = [turn[0], t + game.turn]
            else:
                if -turn[0] < lowest[i][0]:
                    lowest[i] = [-turn[0], t + game.turn]
            
            if t > 0 and not turns[i][t][1] == turns[i][t-1][1]:
                last_transfer[i] = t + game.turn
    
    for i, ice in enumerate(ices):
        if ice.owner == game.get_myself().id:
            if not turns[i][last_transfer[i] - game.turn][1] == game.get_myself().id:
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

def get_all(game):
    ices = game.get_all_icebergs()
    turns = get_turns(game)
    lowest, last_transfer, needs_saving = get_freedom(game, ices, turns)
    
    return ices, turns, lowest, last_transfer, needs_saving

def do_turn(game):
    ices, turns, lowest, last_transfer, needs_saving = get_all(game)
    
    for i in range(len(ices)):
        if needs_saving[i] > 0:
            lowest[i][0] = 0
    
    # saving
    for i, ice in enumerate(ices):
        if needs_saving[i][0] != 0 and sum([lowest[f][0] for f in range(len(ices)) if ices[f].owner.equals(game.get_myself())]):
            sorted_distance = sort_distance(game, ice)
            
            for f, friend in sorted_distance:
                if friend.owner.equals(game.get_myself()):
                    if needs_saving[f][0] == 0:
                        if ice.get_turns_till_arrival(friend) > needs_saving[i][1]:
                            needs_saving[i][0] = turns[i][ice.get_turns_till_arrival(friend) + 1][0]
                        
                        friend.send_penguins(ice, lowest[f][0] - 1)
                        needs_saving[i][0] -= lowest[f][0] - 1
                        
                        if needs_saving[i][0] < 0:
                            needs_saving[i] = [0, 0]
    
    # upgrading and attacking
    for i, ice in enumerate(ices):
        if ice.owner.equals(game.get_myself()):
            ices, turns, lowest, last_transfer, needs_saving = get_all(game)
            
            cost = ice.upgrade_cost
            needed = [turns[e][ice.get_turns_till_arrival(ices[e]) + 1][0] + 1 for e in range(len(ices))]
            
            for e in range(len(ices)):
                if ices[e].owner.equals(game.get_myself()) or turns[e][last_transfer[e] - game.turn][1] == game.get_myself().id:
                    needed[e] = -1
            sorted_needed = sorted(needed)
            
            first_real = len(ices)
            for n, need in enumerate(sorted_needed):
                if need != -1:
                    first_real = n
                    break
            
            if ice.level < ice.upgrade_level_limit and first_real + 1 < len(ices) and cost < sorted_needed[first_real] + sorted_needed[first_real+1] and lowest[i][0] > cost:
                if ice.can_upgrade():
                    ice.upgrade()
            else:
                score = [0 for s in ices]
                score_needed = score
                score_distances = score
                
                needed = [turns[e][ice.get_turns_till_arrival(ices[e]) + 1][0] + 1 for e in range(len(ices))]
                for e in range(len(ices)):
                    if ices[e].owner.equals(game.get_myself()) or turns[e][last_transfer[e] - game.turn + 1][1] == game.get_myself().id:
                        needed[e] = -1
                needed_numbers = [[j, needed[j]] for j in range(len(needed))]
                sorted_needed = sorted(needed_numbers, key = lambda need: need[1])
                
                distances = [ice.get_turns_till_arrival(s) for s in ices]
                distances_numbers = [[j, distances[j]] for j in range(len(distances))]
                sorted_distances = sorted(distances_numbers, key = lambda distance: distance[1])
                
                for s in range(len(score)):
                    # needed
                    if sorted_needed[s][1] != -1:
                        if s > 0 and sorted_needed[s - 1][1] != -1 and sorted_needed[s][1] == sorted_needed[s - 1][1]:
                            score_needed[s] = score_needed[s - 1]
                        else:
                            score_needed[s] = s + 1
                    
                    # distances
                    if s > 0 and sorted_distances[s][1] == sorted_distances[s - 1][1]:
                        score_distances[s] = score_distances[s - 1]
                    else:
                        score_distances[s] = s + 1
                
                for s in range(len(score)):
                    needed_stranger = needed_numbers[s][0]
                    if not ices[needed_stranger].owner.equals(game.get_myself()):
                        score[needed_stranger] += score_needed[s]
                    
                    distance_stranger = distances_numbers[s][0]
                    if not ices[distance_stranger].owner.equals(game.get_myself()):
                        score[distance_stranger] += score_distances[s]
                    
                
                ices_scores = [[j, score[j]] for j in range(len(ices))]
                sorted_ices = sorted(ices_scores, key = lambda j: j[1])
                
                for s, _ in enumerate(sorted_ices):
                    stranger = ices[s]
                    
                    if not stranger.owner.equals(game.get_myself()) and needed[s] != -1:
                        if lowest[i][0] > needed[s]:
                            ice.send_penguins(stranger, needed[s])
                            lowest[i][0] -= needed[s]
                            needed[s] = -1
"""
todo:
- if ice is heighest out of all, constantly attack with penguiin_per_turn
- fix wrong attacks: when ice attacks with less that it can have
- fix multiple ices saving a friend
- wait for enemy to attack neutral if twice of enemy is less than neutral (time the attack to hit exactly after enemy's attack)
- saving system not detecting 1 remanding enemy take over
- check if upgrade is better by correct sorted scores
- if ice attacking and wont win, pioritize helping
- fix scoreing system
"""
