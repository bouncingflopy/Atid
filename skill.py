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
    
def do_turn(game):
    turns_by_ice, turns_by_turn = get_turns(game)
