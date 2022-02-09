from penguin_game import *

max_distance = None
conquer = {}

# {ice: {turn(current=0,1,2,...): [needed_to_conquer, owner],...}}
# positive number = will be an enemy iceberg in that turn, with n penguins.
# negative number = will be a friendly iceberg in that turn, with -n penguins.

possibilities = {}
# {levels added: {ice: action,...},...}

def update_conquer(game, l):
    friendly_needed = lambda ice, turn: -ice.penguin_amount \
                                        - ice.penguins_per_turn * turn \
                                        - sum([group.penguin_amount for group in game.get_my_penguin_groups() if
                                               group.destination.equals(ice) and group.turns_till_arrival <= turn]) \
                                        + sum([group.penguin_amount for group in game.get_enemy_penguin_groups() if
                                               group.destination.equals(ice) and group.turns_till_arrival <= turn])
    enemy_needed = lambda ice, turn: ice.penguin_amount \
                                     + ice.penguins_per_turn * turn \
                                     - sum([group.penguin_amount for group in game.get_my_penguin_groups() if
                                            group.destination.equals(ice) and group.turns_till_arrival <= turn]) \
                                     + sum([group.penguin_amount for group in game.get_enemy_penguin_groups() if
                                            group.destination.equals(ice) and group.turns_till_arrival <= turn])
    neutral_needed = lambda ice, turn: abs(ice.penguin_amount
                                           - sum([group.penguin_amount for group in game.get_enemy_penguin_groups() if
                                                  group.destination.equals(ice) and group.turns_till_arrival <= turn])) \
                                       - sum([group.penguin_amount for group in game.get_my_penguin_groups() if
                                              group.destination.equals(ice) and group.turns_till_arrival <= turn])

    need_to_conquer = {game.get_myself(): friendly_needed, game.get_enemy(): enemy_needed,
                       game.get_neutral(): neutral_needed}
    owners = {ice: ice.owner for ice in game.get_all_icebergs()}
    global conquer

    conquer = {ice: {turn: [need_to_conquer[owners[ice]](ice, turn), owners[ice]] for turn in range(max_distance) if
                     game.turn + turn <= game.max_turns} for ice in game.get_all_icebergs()}
    # if the turn_data changed from - to + => changed from friendly to enemy
    # if the turn_data changed from + to - => changed from enemy to friendly
    # if the iceberg was neutral and now either its amount of penguin changed or (the number of penguin groups sent to it decreased and it has the same penguin_amount), then the iceberg is no longer neutral (+=enemy, -=friendly)
    for ice, ice_data in conquer.items():
        owner_changed = False
        for turn, turn_data in ice_data.items()[1:]:
            prev = ice_data[turn - 1][0]
            curr = ice_data[turn][0]
            if owners[ice].equals(game.get_neutral()) and (prev != curr or (
                    sum([1 for group in game.get_all_penguin_groups() if
                         group.destination.equals(ice) and group.turns_till_arrival <= turn - 1]) < sum(
                    [1 for group in game.get_all_penguin_groups() if group.destination.equals(
                            ice) and group.turns_till_arrival <= turn]) and prev == curr)):  # Changed from neutral to other
                if curr < 0:  # Changed from neutral to friendly
                    owners[ice] = game.get_myself()
                    owner_changed = True
                elif curr > 0:  # Changed from neutral to enemy
                    owners[ice] = game.get_enemy()
                    owner_changed = True
            elif prev > 0 and curr < 0:  # Changed from positive to negative, from enemy to friendly.
                owners[ice] = game.get_myself()
                owner_changed = True
            elif prev < 0 and curr > 0:  # Changed from negative to positive, from friendly to enemy.
                owners[ice] = game.get_enemy()
                owner_changed = True

            if owner_changed:
                ice_data.update({t: [need_to_conquer[owners[ice]](ice, t), owners[ice]] for t in range(turn + 1, max_distance) if
                                 game.turn + t <= game.max_turns})




def play(game):
    """
        Go through the "conquer" dictionary from the highest level to the lowest level.
        For every turn t: if the iceberg (with n penguins in turn t) is not a friendly one, then send n+1 penguins to it from an iceberg that is less than or equal to t turns away from it. Then update the conquer dictionary.
        Upgrade all of the icebergs that haven't acted this turn if possible.
    """
    are_ok = {ice: True for ice in game.get_all_icebergs()}
    
    for ice, ice_data in dict(sorted(conquer.items(), key=lambda x: x[0].level, reverse=True)).items():
        for t, turn_data in ice_data.items():
            n = turn_data[0]
            if n > 0: 
                are_ok[ice] = False
    
    for ice, ice_data in dict(sorted(conquer.items(), key=lambda x: x[0].level, reverse=True)).items():
        for t, turn_data in ice_data.items():
            n = turn_data[0]
            if n > 0:  # Need to conquer this iceberg.
                for attacking_ice in sorted([i for i in game.get_my_icebergs()],
                                            key=lambda iceberg: t - iceberg.get_turns_till_arrival(ice)):
                    if attacking_ice.can_upgrade() and (attacking_ice.level + 1 >= ice.level):
                        break
                    if attacking_ice.penguin_amount > n + 6 and not attacking_ice.equals(ice) and not are_ok[ice]:
                        if ice.owner.equals(game.get_neutral()):
                            if attacking_ice.get_turns_till_arrival(ice) > t:
                                attacking_ice.send_penguins(ice, n + 1)
                                are_ok[ice] = True
                        else:
                            attacking_ice.send_penguins(ice, n + 1)
                            are_ok[ice] = True
                        # if attacking_ice.can_send_penguins(ice, n+1):
                        #if n != 1:

                        #else:
                           # if conquer.get(ice).get(attacking_ice.get_turns_till_arrival(ice) - 1)[0] == 1 + ice.penguins_per_turn:
                              #  attacking_ice.send_penguins(ice, 2)
                        # update_conquer(game, [attacking_ice, ice])
                    if are_ok[ice]:
                        break

    for ice in game.get_my_icebergs():
        if ice.can_upgrade() and not ice.already_acted and are_ok[ice]:
            ice.upgrade()


def do_turn(game):

    if game.turn == 1:
        global max_distance
        max_distance = max([ice1.get_turns_till_arrival(ice2) for ice1 in game.get_all_icebergs() for ice2 in game.get_all_icebergs()])
    update_conquer(game, [])
    play(game)



"""
TODO:
    dont upgrade an iceberg if its about to be conquered
    dont send penguins from an iceberg if its about to be conquered and its level is higher than the iceberg the penguins were sent to
    doesnt calculate the timing right - for neutral icebergs need turn_of_arrival==, not <=
    dont send penguins if they will still be on their way when the game ends
"""
