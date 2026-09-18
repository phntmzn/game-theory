# recursive_mad_20.py
#
# Abstract 20-player recursive Mutual Assured Destruction
# game-theory simulation.
#
# This is a toy mathematical model:
#
# C = De-escalate
# T = Threaten
# E = Escalate
#
# Players:
#   Mary, Bob, Alice, Sue
#   Player05 ... Player20
#
# No real-world weapons or operational parameters are modeled.

from functools import lru_cache


PLAYERS = (
    "Mary",
    "Bob",
    "Alice",
    "Sue",
    "Player05",
    "Player06",
    "Player07",
    "Player08",
    "Player09",
    "Player10",
    "Player11",
    "Player12",
    "Player13",
    "Player14",
    "Player15",
    "Player16",
    "Player17",
    "Player18",
    "Player19",
    "Player20",
)

ACTIONS = ("C", "T", "E")


# ---------------------------------------------------------
# Payoff model
# ---------------------------------------------------------

def payoff(action, opponents):
    """
    Calculate one player's payoff.

    C:
        Rewards a peaceful environment.

    T:
        Gains a small advantage from pressure.

    E:
        Gains a short-term advantage but becomes costly
        as more players escalate.
    """

    cooperation = opponents.count("C")
    threats = opponents.count("T")
    escalation = opponents.count("E")

    if action == "C":
        return (
            3 * cooperation
            - 2 * threats
            - 5 * escalation
        )

    if action == "T":
        return (
            2 * cooperation
            + threats
            - 4 * escalation
        )

    if action == "E":
        return (
            4 * cooperation
            + 2 * threats
            - 8 * escalation
        )

    raise ValueError(action)


# ---------------------------------------------------------
# Recursive evaluation
# ---------------------------------------------------------

@lru_cache(maxsize=None)
def recursive_value(
    actions,
    player,
    depth,
):
    """
    Recursively evaluate the future state.

    actions:
        Tuple containing one action for every player.

    player:
        Index of the player being evaluated.

    depth:
        Number of future decision layers.
    """

    if depth == 0:
        opponents = [
            actions[i]
            for i in range(len(actions))
            if i != player
        ]

        return payoff(
            actions[player],
            opponents,
        )

    best = float("-inf")

    for action in ACTIONS:

        next_actions = list(actions)
        next_actions[player] = action
        next_actions = tuple(next_actions)

        value = recursive_value(
            next_actions,
            player,
            depth - 1,
        )

        best = max(best, value)

    return best


# ---------------------------------------------------------
# Best response
# ---------------------------------------------------------

def best_response(actions, player, depth):
    """
    Find the action with the highest recursive value.
    """

    best_action = None
    best_value = float("-inf")

    for action in ACTIONS:

        candidate = list(actions)
        candidate[player] = action
        candidate = tuple(candidate)

        value = recursive_value(
            candidate,
            player,
            depth,
        )

        if value > best_value:
            best_value = value
            best_action = action

    return best_action, best_value


# ---------------------------------------------------------
# Initial state
# ---------------------------------------------------------

def initial_state():
    return tuple(
        "C"
        for _ in PLAYERS
    )


# ---------------------------------------------------------
# Simulation
# ---------------------------------------------------------

def simulate(rounds=10, depth=3):

    actions = initial_state()

    print("=" * 60)
    print("20-PLAYER RECURSIVE MAD GAME")
    print("=" * 60)

    for round_number in range(1, rounds + 1):

        new_actions = list(actions)

        print()
        print(f"ROUND {round_number}")
        print("-" * 60)

        for player_index, player in enumerate(PLAYERS):

            action, value = best_response(
                actions,
                player_index,
                depth,
            )

            new_actions[player_index] = action

            print(
                f"{player:<12} "
                f"{action} "
                f"value={value:8.2f}"
            )

        actions = tuple(new_actions)

        print()
        print(
            "C:",
            actions.count("C"),
            "T:",
            actions.count("T"),
            "E:",
            actions.count("E"),
        )

        # Abstract catastrophic terminal condition.
        if actions.count("E") == len(PLAYERS):

            print()
            print("ALL PLAYERS ESCALATED.")
            print("Game terminated.")

            break

    print()
    print("=" * 60)
    print("FINAL STATE")
    print("=" * 60)

    for player, action in zip(PLAYERS, actions):
        print(f"{player:<12} {action}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    simulate(
        rounds=10,
        depth=3,
    )