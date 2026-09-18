"""
WAR OF ATTRITION USING eval() AND exec()

Python 3.x

The players repeatedly decide how much they are willing to spend
to remain in a contest.

eval()  -> evaluates payoff/strategy expressions
exec()  -> dynamically creates strategy functions
"""

import random


# ------------------------------------------------------------
# Game configuration
# ------------------------------------------------------------

ROUNDS = 10
PLAYERS = 6

STRATEGIES = {
    "aggressive": "min(max(base + random.uniform(0, 5), 0), 100)",
    "cautious": "min(max(base * 0.55 + random.uniform(0, 3), 0), 100)",
    "random": "random.uniform(0, 100)",
    "adaptive": "min(max(opponent_bid * 0.9 + random.uniform(-2, 2), 0), 100)",
}


# ------------------------------------------------------------
# Dynamically create strategies with exec()
# ------------------------------------------------------------

def make_strategy(expression):
    source = f"""
def strategy(base, opponent_bid, random):
    return {expression}
"""

    namespace = {}
    exec(source, namespace)

    return namespace["strategy"]


strategy_functions = {
    name: make_strategy(expression)
    for name, expression in STRATEGIES.items()
}


# ------------------------------------------------------------
# Player
# ------------------------------------------------------------

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy_name = strategy
        self.strategy = strategy_functions[strategy]
        self.score = 1000.0
        self.total_cost = 0.0

    def bid(self, opponent_bid):
        value = self.strategy(
            self.score / 20,
            opponent_bid,
            random,
        )

        return max(0.0, float(value))


# ------------------------------------------------------------
# eval() payoff calculation
# ------------------------------------------------------------

PAYOFF_EXPRESSION = """
winner_bid * 2
- winner_bid
- loser_bid * 0.25
"""


def calculate_payoff(winner_bid, loser_bid):
    return eval(
        PAYOFF_EXPRESSION,
        {
            "winner_bid": winner_bid,
            "loser_bid": loser_bid,
        },
    )


# ------------------------------------------------------------
# Create players
# ------------------------------------------------------------

players = []

strategy_names = list(STRATEGIES)

for i in range(PLAYERS):
    strategy = strategy_names[i % len(strategy_names)]
    players.append(
        Player(
            f"Player_{i + 1}",
            strategy,
        )
    )


# ------------------------------------------------------------
# Run war of attrition
# ------------------------------------------------------------

for round_number in range(1, ROUNDS + 1):

    print(f"\n--- ROUND {round_number} ---")

    active = players.copy()

    while len(active) > 1:

        p1, p2 = random.sample(active, 2)

        bid1 = p1.bid(0)
        bid2 = p2.bid(bid1)

        print(
            f"{p1.name} ({p1.strategy_name}) "
            f"bids {bid1:.2f}"
        )

        print(
            f"{p2.name} ({p2.strategy_name}) "
            f"bids {bid2:.2f}"
        )

        # Everyone pays the cost of remaining in the contest.
        p1.score -= bid1
        p2.score -= bid2

        p1.total_cost += bid1
        p2.total_cost += bid2

        # Higher bid wins.
        if bid1 > bid2:
            winner = p1
            loser = p2
            winner_bid = bid1
            loser_bid = bid2

        elif bid2 > bid1:
            winner = p2
            loser = p1
            winner_bid = bid2
            loser_bid = bid1

        else:
            print("Tie.")
            continue

        payoff = calculate_payoff(
            winner_bid,
            loser_bid,
        )

        winner.score += payoff

        print(
            f"Winner: {winner.name} "
            f"+{payoff:.2f}"
        )

        # Loser leaves this particular contest.
        active.remove(loser)


# ------------------------------------------------------------
# Final results
# ------------------------------------------------------------

print("\n==============================")
print("FINAL RESULTS")
print("==============================")

ranking = sorted(
    players,
    key=lambda p: p.score,
    reverse=True,
)

for position, player in enumerate(ranking, 1):

    print(
        f"{position}. "
        f"{player.name:10} "
        f"strategy={player.strategy_name:10} "
        f"score={player.score:8.2f} "
        f"cost={player.total_cost:8.2f}"
    )