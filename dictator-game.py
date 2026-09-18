"""
30-PLAYER DICTATOR GAME

Uses:
    exec() -> dynamically creates dictator strategies
    eval() -> dynamically evaluates payoff expressions

Python 3.x

30 players
50 rounds
Multiple strategies
Repeated interactions

Do not use eval()/exec() with untrusted input.
"""

import random


# ============================================================
# CONFIGURATION
# ============================================================

NUM_PLAYERS = 30
ROUNDS = 50
POT = 100.0


# ============================================================
# 30 PLAYER NAMES
# ============================================================

PLAYER_NAMES = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank",
    "Grace",
    "Henry",
    "Iris",
    "Jack",
    "Karen",
    "Leo",
    "Mia",
    "Nathan",
    "Olivia",
    "Paul",
    "Quinn",
    "Rachel",
    "Sam",
    "Tara",
    "Uma",
    "Victor",
    "Wendy",
    "Xavier",
    "Yara",
    "Zach",
    "Aaron",
    "Bella",
    "Caleb",
    "Daisy",
]


# ============================================================
# STRATEGY ASSIGNMENTS
# ============================================================

PLAYER_STRATEGIES = [
    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",

    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",

    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",

    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",

    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",

    "equal_split",
    "greedy",
    "generous",
    "moderate",
    "random",
]


# ============================================================
# DICTATOR STRATEGIES
# ============================================================

STRATEGY_CODE = {

    # Give 50%.
    "equal_split": """
def strategy(pot, random):
    return pot * 0.50
""",

    # Give 10%.
    "greedy": """
def strategy(pot, random):
    return pot * 0.10
""",

    # Give 75%.
    "generous": """
def strategy(pot, random):
    return pot * 0.75
""",

    # Give 35%.
    "moderate": """
def strategy(pot, random):
    return pot * 0.35
""",

    # Give a random amount.
    "random": """
def strategy(pot, random):
    return random.uniform(0, pot)
""",
}


# ============================================================
# CREATE STRATEGIES USING exec()
# ============================================================

def create_strategy(source):

    namespace = {
        "random": random,
    }

    exec(
        source,
        namespace,
    )

    return namespace["strategy"]


strategies = {
    name: create_strategy(source)
    for name, source in STRATEGY_CODE.items()
}


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(
        self,
        player_id,
        name,
        strategy_name,
    ):

        self.id = player_id

        self.name = name

        self.strategy_name = strategy_name

        self.strategy = strategies[
            strategy_name
        ]

        self.score = 0.0

        self.total_given = 0.0

        self.total_received = 0.0

        self.games_as_dictator = 0

        self.games_as_recipient = 0

        self.history = []

    def choose_amount(self):

        amount = self.strategy(
            POT,
            random,
        )

        return max(
            0.0,
            min(POT, float(amount)),
        )


# ============================================================
# CREATE 30 PLAYERS
# ============================================================

players = [
    Player(
        player_id=i + 1,
        name=PLAYER_NAMES[i],
        strategy_name=PLAYER_STRATEGIES[i],
    )
    for i in range(NUM_PLAYERS)
]


# ============================================================
# DISPLAY PLAYERS
# ============================================================

print()
print("=" * 75)
print("30 PLAYERS")
print("=" * 75)

for player in players:

    print(
        f"P{player.id:02d} | "
        f"{player.name:10} | "
        f"{player.strategy_name}"
    )


# ============================================================
# PAYOFF EXPRESSIONS
# ============================================================

DICTATOR_PAYOFF = """
POT - amount
"""

RECIPIENT_PAYOFF = """
amount
"""


# ============================================================
# EVAL PAYOFF ENGINE
# ============================================================

def evaluate(
    expression,
    amount,
):

    return eval(
        expression,
        {
            "__builtins__": {},

            "POT": POT,

            "amount": amount,
        },
    )


# ============================================================
# TOURNAMENT
# ============================================================

for round_number in range(1, ROUNDS + 1):

    print()
    print("=" * 75)
    print(f"ROUND {round_number}")
    print("=" * 75)

    # Randomly determine who is dictator.
    shuffled = players.copy()

    random.shuffle(shuffled)

    # Every player acts as dictator once.
    for dictator in shuffled:

        recipients = [
            player
            for player in players
            if player.id != dictator.id
        ]

        recipient = random.choice(
            recipients
        )

        # ----------------------------------------------------
        # DICTATOR DECISION
        # ----------------------------------------------------

        amount = dictator.choose_amount()

        # ----------------------------------------------------
        # PAYOFFS USING eval()
        # ----------------------------------------------------

        dictator_payoff = evaluate(
            DICTATOR_PAYOFF,
            amount,
        )

        recipient_payoff = evaluate(
            RECIPIENT_PAYOFF,
            amount,
        )

        # ----------------------------------------------------
        # UPDATE SCORES
        # ----------------------------------------------------

        dictator.score += dictator_payoff

        recipient.score += recipient_payoff

        dictator.total_given += amount

        recipient.total_received += amount

        dictator.games_as_dictator += 1

        recipient.games_as_recipient += 1

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        dictator.history.append(
            {
                "role": "dictator",
                "recipient": recipient.name,
                "amount_given": amount,
                "payoff": dictator_payoff,
            }
        )

        recipient.history.append(
            {
                "role": "recipient",
                "dictator": dictator.name,
                "amount_received": amount,
                "payoff": recipient_payoff,
            }
        )

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        print(
            f"{dictator.name:10} "
            f"-> "
            f"{recipient.name:10} | "
            f"given=${amount:6.2f} | "
            f"dictator=${dictator_payoff:6.2f} | "
            f"recipient=${recipient_payoff:6.2f} | "
            f"strategy={dictator.strategy_name}"
        )


# ============================================================
# FINAL RANKING
# ============================================================

print()
print("=" * 75)
print("FINAL RANKING")
print("=" * 75)

ranking = sorted(
    players,
    key=lambda player: player.score,
    reverse=True,
)


for position, player in enumerate(
    ranking,
    start=1,
):

    average_given = (
        player.total_given
        / max(1, player.games_as_dictator)
    )

    average_received = (
        player.total_received
        / max(1, player.games_as_recipient)
    )

    print(
        f"{position:02d}. "
        f"{player.name:10} | "
        f"score=${player.score:9.2f} | "
        f"strategy={player.strategy_name:12} | "
        f"given=${player.total_given:9.2f} | "
        f"received=${player.total_received:9.2f} | "
        f"avg given=${average_given:6.2f} | "
        f"avg received=${average_received:6.2f}"
    )


# ============================================================
# STRATEGY STATISTICS
# ============================================================

print()
print("=" * 75)
print("STRATEGY STATISTICS")
print("=" * 75)

for strategy_name in strategies:

    members = [
        player
        for player in players
        if player.strategy_name == strategy_name
    ]

    if not members:
        continue

    average_score = (
        sum(
            player.score
            for player in members
        )
        / len(members)
    )

    total_given = sum(
        player.total_given
        for player in members
    )

    average_given = (
        total_given
        / sum(
            player.games_as_dictator
            for player in members
        )
    )

    print(
        f"{strategy_name:12} | "
        f"players={len(members):2d} | "
        f"avg score=${average_score:9.2f} | "
        f"avg given=${average_given:6.2f}"
    )


# ============================================================
# GAME SUMMARY
# ============================================================

print()
print("=" * 75)
print("GAME SUMMARY")
print("=" * 75)

total_given = sum(
    player.total_given
    for player in players
)

total_rounds = (
    NUM_PLAYERS * ROUNDS
)

average_offer = (
    total_given
    / total_rounds
)

print(
    f"Players:              {NUM_PLAYERS}"
)

print(
    f"Rounds:               {ROUNDS}"
)

print(
    f"Dictator decisions:   {total_rounds}"
)

print(
    f"Pot per decision:     ${POT:.2f}"
)

print(
    f"Total distributed:    ${total_given:,.2f}"
)

print(
    f"Average amount given: ${average_offer:.2f}"
)


# ============================================================
# EXAMPLE PAYOFF RULES
# ============================================================

print()
print("=" * 75)
print("PAYOFF RULES")
print("=" * 75)

print(
    "Dictator payoff: POT - amount"
)

print(
    "Recipient payoff: amount"
)
