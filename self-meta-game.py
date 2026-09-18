# SELF-MODIFYING GAME THEORY PROGRAM
#
# Demonstrates:
#   - eval()
#   - exec()
#   - runtime strategy generation
#   - recursive game evaluation
#   - self-modifying strategy rules
#
# The generated code is restricted to strategy expressions
# created internally by the program.


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


# ------------------------------------------------------------
# Strategy factory
# ------------------------------------------------------------

def build_strategy(name, expression):
    """
    Dynamically create a strategy function.

    expression is generated internally.
    """

    source = f"""
def strategy(history, player_index):
    return {expression}
"""

    namespace = {
        "ACTIONS": ACTIONS,
    }

    exec(
        source,
        namespace,
    )

    function = namespace["strategy"]
    function.__name__ = name

    return function


# ------------------------------------------------------------
# Initial strategies
# ------------------------------------------------------------

strategies = {}


strategies["Mary"] = build_strategy(
    "mary_strategy",
    '"C"',
)

strategies["Bob"] = build_strategy(
    "bob_strategy",
    '"C" if not history else history[-1][player_index]',
)

strategies["Alice"] = build_strategy(
    "alice_strategy",
    '"E"',
)

strategies["Sue"] = build_strategy(
    "sue_strategy",
    '"T" if history and history[-1].count("E") else "C"',
)


# Everyone else starts with cooperation.

for player in PLAYERS[4:]:
    strategies[player] = build_strategy(
        f"{player.lower()}_strategy",
        '"C"',
    )


# ------------------------------------------------------------
# Payoff
# ------------------------------------------------------------

def payoff(action, opponents):

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

    return 0


# ------------------------------------------------------------
# Runtime strategy modification
# ------------------------------------------------------------

def modify_strategy(player, expression):

    name = f"{player.lower()}_modified"

    strategies[player] = build_strategy(
        name,
        expression,
    )

    print(
        f"MODIFIED: {player} -> {name}"
    )


# ------------------------------------------------------------
# Evaluate strategy
# ------------------------------------------------------------

def evaluate_player(
    player_index,
    history,
):

    player = PLAYERS[player_index]

    strategy = strategies[player]

    action = strategy(
        history,
        player_index,
    )

    opponents = []

    if history:
        opponents = [
            history[-1][i]
            for i in range(len(PLAYERS))
            if i != player_index
        ]

    score = payoff(
        action,
        opponents,
    )

    return action, score


# ------------------------------------------------------------
# Meta-rule
# ------------------------------------------------------------

def meta_rule(history):

    if not history:
        return

    previous = history[-1]

    escalation_count = previous.count("E")

    threat_count = previous.count("T")

    # If escalation becomes widespread,
    # modify cooperative players into
    # defensive trigger strategies.

    if escalation_count >= 5:

        for player in PLAYERS:

            expression = (
                '"E" if '
                'history and history[-1].count("E") >= 5 '
                'else "C"'
            )

            modify_strategy(
                player,
                expression,
            )

    # If there is a large threat state,
    # modify the population to become
    # more forgiving.

    elif threat_count >= 8:

        for player in PLAYERS:

            expression = (
                '"C" if '
                'not history or history[-1].count("E") == 0 '
                'else "T"'
            )

            modify_strategy(
                player,
                expression,
            )


# ------------------------------------------------------------
# Game
# ------------------------------------------------------------

def run(rounds=10):

    history = []

    for round_number in range(1, rounds + 1):

        print()
        print("=" * 60)
        print(f"ROUND {round_number}")
        print("=" * 60)

        actions = []

        for index, player in enumerate(PLAYERS):

            action, score = evaluate_player(
                index,
                history,
            )

            actions.append(action)

            print(
                f"{player:<12}"
                f"{action:<3}"
                f"score={score:>5}"
            )

        history.append(actions)

        print()
        print(
            "C:",
            actions.count("C"),
            "T:",
            actions.count("T"),
            "E:",
            actions.count("E"),
        )

        # Let the meta-program alter itself.
        meta_rule(history)

    return history


# ------------------------------------------------------------
# Demonstrate eval()
# ------------------------------------------------------------

def inspect_state(history):

    if not history:
        return

    expression = (
        "history[-1].count('E')"
    )

    escalation_count = eval(
        expression,
        {"history": history},
    )

    print()
    print(
        "eval() calculated escalation:",
        escalation_count,
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":

    history = run(
        rounds=10,
    )

    inspect_state(history)