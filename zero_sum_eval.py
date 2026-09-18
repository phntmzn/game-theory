# zero_sum_eval.py
#
# Zero-sum game using eval().
#
# Mary wants to maximize her payoff.
# Bob receives -Mary's payoff.
#
# Actions:
#   A, B, C

PLAYERS = ("Mary", "Bob")
ACTIONS = ("A", "B", "C")


# Payoff expressions for Mary.
#
# Each expression is evaluated dynamically.

PAYOFF_RULES = {
    ("A", "A"): "0",
    ("A", "B"): "3",
    ("A", "C"): "-2",

    ("B", "A"): "-3",
    ("B", "B"): "0",
    ("B", "C"): "4",

    ("C", "A"): "2",
    ("C", "B"): "-4",
    ("C", "C"): "0",
}


def evaluate_payoff(mary_action, bob_action):
    expression = PAYOFF_RULES[
        (mary_action, bob_action)
    ]

    # Evaluate only the internally generated
    # payoff expression.
    return eval(
        expression,
        {"__builtins__": {}},
    )


def play(mary_action, bob_action):
    mary_score = evaluate_payoff(
        mary_action,
        bob_action,
    )

    bob_score = -mary_score

    return mary_score, bob_score


def show_matrix():
    print("ZERO-SUM PAYOFF MATRIX")
    print()

    print("          Bob")
    print("       A    B    C")

    for mary_action in ACTIONS:

        values = []

        for bob_action in ACTIONS:

            mary, bob = play(
                mary_action,
                bob_action,
            )

            values.append(
                f"{mary:>3}"
            )

        print(
            f"Mary {mary_action}:"
            f"{''.join(values)}"
        )


def find_best_response(bob_action):
    results = []

    for mary_action in ACTIONS:

        mary_score, _ = play(
            mary_action,
            bob_action,
        )

        results.append(
            (mary_score, mary_action)
        )

    return max(results)


def find_worst_case(mary_action):
    results = []

    for bob_action in ACTIONS:

        mary_score, _ = play(
            mary_action,
            bob_action,
        )

        results.append(
            (mary_score, bob_action)
        )

    return min(results)


if __name__ == "__main__":

    show_matrix()

    print()
    print("MARY'S BEST RESPONSES")
    print()

    for bob_action in ACTIONS:

        score, action = find_best_response(
            bob_action
        )

        print(
            f"If Bob chooses {bob_action}: "
            f"Mary chooses {action} "
            f"(payoff {score})"
        )

    print()
    print("MARY'S WORST CASE FOR EACH ACTION")
    print()

    for mary_action in ACTIONS:

        score, bob_action = find_worst_case(
            mary_action
        )

        print(
            f"Mary chooses {mary_action}: "
            f"worst payoff = {score} "
            f"(Bob chooses {bob_action})"
        )