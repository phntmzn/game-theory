# META GAME THEORY ENGINE
#
# A configurable recursive multi-player game engine.
#
# The game is described by DATA rather than hard-coded
# directly into the simulation.
#
# Example:
#   Mary, Bob, Alice, Sue + 16 players
#   Actions: C, T, E
#
# C = cooperate
# T = threaten
# E = escalate
#
# This is an abstract game-theory simulation.


from dataclasses import dataclass
from functools import lru_cache
from itertools import product


# ============================================================
# GAME SPECIFICATION
# ============================================================

@dataclass(frozen=True)
class GameSpec:
    name: str
    players: tuple[str, ...]
    actions: tuple[str, ...]
    depth: int
    rounds: int


# ============================================================
# PLAYER GENERATOR
# ============================================================

def make_players():
    fixed = (
        "Mary",
        "Bob",
        "Alice",
        "Sue",
    )

    extra = tuple(
        f"Player{i:02d}"
        for i in range(5, 21)
    )

    return fixed + extra


# ============================================================
# GAME PAYOFF
# ============================================================

def payoff(action, opponents):
    """
    Generic payoff function.

    The payoff depends only on the distribution
    of opponent actions.
    """

    cooperation = opponents.count("C")
    threats = opponents.count("T")
    escalation = opponents.count("E")

    rules = {
        "C": (
            3 * cooperation
            - 2 * threats
            - 5 * escalation
        ),

        "T": (
            2 * cooperation
            + threats
            - 4 * escalation
        ),

        "E": (
            4 * cooperation
            + 2 * threats
            - 8 * escalation
        ),
    }

    return rules[action]


# ============================================================
# STATE
# ============================================================

def initial_state(game):
    return tuple(
        game.actions[0]
        for _ in game.players
    )


def replace_action(state, index, action):
    state = list(state)
    state[index] = action
    return tuple(state)


# ============================================================
# RECURSIVE META SOLVER
# ============================================================

def make_solver(game):
    """
    Build a recursive solver for the supplied GameSpec.

    This is the meta-programming portion:
    the solver is generated from the game description.
    """

    @lru_cache(maxsize=None)
    def evaluate(state, player, depth):

        opponents = tuple(
            state[i]
            for i in range(len(state))
            if i != player
        )

        current = payoff(
            state[player],
            opponents,
        )

        if depth <= 0:
            return current

        future_values = []

        for action in game.actions:

            next_state = replace_action(
                state,
                player,
                action,
            )

            value = evaluate(
                next_state,
                player,
                depth - 1,
            )

            future_values.append(value)

        return current + max(future_values)

    return evaluate


# ============================================================
# BEST ACTION
# ============================================================

def best_action(game, solver, state, player):

    candidates = []

    for action in game.actions:

        candidate = replace_action(
            state,
            player,
            action,
        )

        value = solver(
            candidate,
            player,
            game.depth,
        )

        candidates.append(
            (value, action)
        )

    return max(candidates)


# ============================================================
# META SIMULATION
# ============================================================

def run_game(game):

    solver = make_solver(game)

    state = initial_state(game)

    print("=" * 70)
    print(game.name)
    print("=" * 70)

    print()
    print("Players:", len(game.players))
    print("Actions:", game.actions)
    print("Depth:", game.depth)
    print("Rounds:", game.rounds)

    for round_number in range(1, game.rounds + 1):

        next_state = list(state)

        print()
        print(f"ROUND {round_number}")
        print("-" * 70)

        for player_index, player in enumerate(game.players):

            value, action = best_action(
                game,
                solver,
                state,
                player_index,
            )

            next_state[player_index] = action

            print(
                f"{player:<12}"
                f"{action:<4}"
                f"value={value:8.2f}"
            )

        state = tuple(next_state)

        print()
        print(
            "Distribution:",
            {
                action: state.count(action)
                for action in game.actions
            }
        )

    return state


# ============================================================
# META-GAME GENERATOR
# ============================================================

def create_game(
    name,
    players,
    actions,
    depth=2,
    rounds=10,
):

    return GameSpec(
        name=name,
        players=tuple(players),
        actions=tuple(actions),
        depth=depth,
        rounds=rounds,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    game = create_game(
        name="Recursive Mutual Assured Destruction",
        players=make_players(),
        actions=("C", "T", "E"),
        depth=2,
        rounds=5,
    )

    final_state = run_game(game)

    print()
    print("=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    for player, action in zip(
        game.players,
        final_state,
    ):
        print(
            f"{player:<12} {action}"
        )