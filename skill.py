from penguin_game import *

def get_turns(game):
    ices = game.get_all_icebergs()
    groups = [[] for _ in range(len(ices))]
    turns = [[[ice.penguin_amount, ice.owner]] for ice in ices]
    
    for g, group in enumerate(game.get_all_penguin_groups()):
        for i, ice in enumerate(ices):
            if group.destination == ice:
                groups[i].append(group)
    for i, ice in enumerate(ices):
        for t in range(30):
            turn = game.turn + t
            
            if not turns[i][-1][1].equals(game.get_neutral()):
                turns[i].append([turns[i][-1][0] + ice.penguins_per_turn, turns[i][-1][1]])
            else:
                turns[i].append(turns[i][-1])
            
            for group in groups[i]:
                if group.turns_till_arrival + game.turn == turn:
                    if group.owner.equals(turns[i][-1]):
                        turns[i][-1][0] += group.penguin_amount
                    else:
                        turns[i][-1][0] -= group.penguin_amount
                        if turns[i][-1][0] <= 0:
                            turns[i][-1][0] *= -1
                            turns[i][-1][1] = group.owner
    
    return turns

def get_freedom(game, ices, turns):
    lowest = [[ice.penguin_amount, game.turn] for ice in ices]
    last_transfer = [game.turn for _ in ices]
    needs_saving = [[0, 0] for _ in ices]
    
    for i in range(len(turns)):
        for t, turn in enumerate(turns[i]):
            if turn[1].equals(ices[i].owner):
                if turn[0] < lowest[i][0]:
                    lowest[i] = [turn[0], t + game.turn]
            else:
                if -turn[0] < lowest[i][0]:
                    lowest[i] = [-turn[0], t + game.turn]
            
            if t > 0 and not turns[i][t][1].equals(turns[i][t-1][1]):
                last_transfer[i] = t + game.turn
    
    for i, ice in enumerate(ices):
        if ice.owner.equals(game.get_myself()):
            if not turns[i][last_transfer[i] - game.turn][1].equals(game.get_myself()):
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
        if lowest[i][1] < 0 and ices[i].owner.equals(game.get_myself()):
            lowest[i][0] = 0
    
    # saving
    for i, ice in enumerate(ices):
        if needs_saving[i][0] != 0 and sum([lowest[f][0] for f in range(len(ices)) if ices[f].owner.equals(game.get_myself())]):
            sorted_distance = sort_distance(game, ice)
            
            for f, friend in sorted_distance:
                if friend.owner.equals(game.get_myself()):
                    if needs_saving[f][0] == 0:
                        if ice.get_turns_till_arrival(friend) > needs_saving[i][1]:
                            needs_saving[i][0] = turns[i][ice.get_turns_till_arrival(friend)][0]
                        
                        friend.send_penguins(ice, lowest[f][0] - 1)
                        needs_saving[i][0] -= lowest[f][0] - 1
                        
                        if needs_saving[i][0] < 0:
                            needs_saving[i] = [0, 0]
    
    ices, turns, lowest, last_transfer, needs_saving = get_all(game)
    
    # upgrading and attacking
    for i, ice in enumerate(ices):
        if ice.owner.equals(game.get_myself()):
            cost = ice.upgrade_cost
            needed = [turns[e][ice.get_turns_till_arrival(ices[e])][0] + 1 for e in range(len(ices))]
            
            for e in range(len(ices)):
                if ices[e].owner.equals(game.get_myself()) or turns[e][last_transfer[e] - game.turn][1].equals(game.get_myself()):
                    needed[e] = -1
            sorted_needed = sorted(needed)
            
            first_real = len(ices)
            for n, need in enumerate(sorted_needed):
                if need != -1:
                    first_real = n
                    break
            
            if first_real + 1 < len(ices):
                print cost
                print "<"
                print sorted_needed[first_real]
                print sorted_needed[first_real+1]
                print needed
                print first_real
                print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
            if ice.level < ice.upgrade_level_limit and first_real + 1 < len(ices) and cost < sorted_needed[first_real] + sorted_needed[first_real+1]:
                if ice.can_upgrade():
                    ice.upgrade()
            else:
                score = [0 for s in ices]
                score_needed = score
                score_distances = score
                
                needed = [turns[e][ice.get_turns_till_arrival(ices[e])][0] + 1 for e in range(len(ices))]
                print [ice.get_turns_till_arrival(ices[e]) for e in range(len(ices))]
                print needed
                for e in range(len(ices)):
                    if ices[e].owner.equals(game.get_myself()) or turns[e][last_transfer[e] - game.turn][1].equals(game.get_myself()):
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
                    stranger = needed_numbers[s][0]
                    if not ices[stranger].owner.equals(game.get_myself()):
                        score[stranger] += score_needed[s]
                    
                    stranger = distances_numbers[s][0]
                    if not ices[stranger].owner.equals(game.get_myself()):
                        score[stranger] += score_distances[s]
                
                ices_scores = [[j, score[j]] for j in range(len(ices))]
                sorted_ices = sorted(ices_scores, key = lambda j: j[1])
                
                for s, _ in enumerate(sorted_ices):
                    stranger = ices[s]
                    
                    if not stranger.owner.equals(game.get_myself()) and needed[s] != -1:
                        if lowest[i][0] > needed[s]:
                            print ices
                            print s
                            print stranger
                            print lowest[i][0]
                            print needed[s]
                            print "---------------------------"
                            ice.send_penguins(stranger, needed[s])
                            lowest[i][0] -= needed[s]
"""
todo:
- if ice is heighst out of all, constantly attack with penguiin_per_turn
- fix wrong attacks: when ice attacks with less that it can have
- fix multiple ices saving a friend
"""
