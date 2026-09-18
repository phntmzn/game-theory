"""
30-PLAYER PRISONER'S DILEMMA

Uses:
    exec() -> dynamically creates strategy functions
    eval() -> dynamically evaluates payoff expressions

Python 3.x

30 explicitly defined players
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
    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",

    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",

    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",

    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",

    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",

    "always_cooperate",
    "always_defect",
    "tit_for_tat",
    "grim_trigger",
    "random",
]


# ============================================================
# PRISONER'S DILEMMA PAYOFFS
# ============================================================

TEMPTATION = 5
REWARD = 3
PUNISHMENT = 1
SUCKER = 0


PAYOFF_RULES = {
    "CC": "REWARD",
    "CD": "SUCKER",
    "DC": "TEMPTATION",
    "DD": "PUNISHMENT",
}


# ============================================================
# STRATEGIES
# ============================================================

STRATEGY_CODE = {

    "always_cooperate": """
def strategy(history):
    return "C"
""",

    "always_defect": """
def strategy(history):
    return "D"
""",

    "tit_for_tat": """
def strategy(history):
    if not history:
        return "C"

    return history[-1]
""",

    "grim_trigger": """
def strategy(history):
    if "D" in history:
        return "D"

    return "C"
""",

    "random": """
def strategy(history):
    return "C" if random.random() < 0.5 else "D"
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

        self.score = 0

        self.cooperations = 0

        self.defections = 0

        self.games = 0

        # History against each opponent.
        self.history = {}

    def choose_action(self, opponent):

        history = self.history.get(
            opponent.id,
            [],
        )

        return self.strategy(history)


# ============================================================
# CREATE 30 PLAYERS FROM LISTS
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
# EVAL PAYOFF ENGINE
# ============================================================

def payoff(my_action, opponent_action):

    key = my_action + opponent_action

    expression = PAYOFF_RULES[key]

    return eval(
        expression,
        {
            "__builtins__": {},

            "REWARD": REWARD,

            "TEMPTATION": TEMPTATION,

            "PUNISHMENT": PUNISHMENT,

            "SUCKER": SUCKER,
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

    shuffled = players.copy()

    random.shuffle(shuffled)

    # 30 players -> 15 matches.
    for i in range(0, NUM_PLAYERS, 2):

        player_a = shuffled[i]

        player_b = shuffled[i + 1]

        # ----------------------------------------------------
        # CHOOSE ACTIONS
        # ----------------------------------------------------

        action_a = player_a.choose_action(
            player_b
        )

        action_b = player_b.choose_action(
            player_a
        )

        # ----------------------------------------------------
        # CALCULATE PAYOFFS
        # ----------------------------------------------------

        payoff_a = payoff(
            action_a,
            action_b,
        )

        payoff_b = payoff(
            action_b,
            action_a,
        )

        player_a.score += payoff_a

        player_b.score += payoff_b

        player_a.games += 1

        player_b.games += 1

        # ----------------------------------------------------
        # UPDATE HISTORY
        # ----------------------------------------------------

        player_a.history.setdefault(
            player_b.id,
            [],
        ).append(action_b)

        player_b.history.setdefault(
            player_a.id,
            [],
        ).append(action_a)

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        if action_a == "C":
            player_a.cooperations += 1
        else:
            player_a.defections += 1

        if action_b == "C":
            player_b.cooperations += 1
        else:
            player_b.defections += 1

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        print(
            f"{player_a.name:10} "
            f"({player_a.strategy_name:16}) "
            f"{action_a} "
            f"vs "
            f"{player_b.name:10} "
            f"({player_b.strategy_name:16}) "
            f"{action_b} "
            f"| payoff="
            f"({payoff_a}, {payoff_b})"
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

    total_actions = (
        player.cooperations
        + player.defections
    )

    cooperation_rate = (
        player.cooperations
        / max(1, total_actions)
    )

    print(
        f"{position:02d}. "
        f"{player.name:10} | "
        f"score={player.score:5d} | "
        f"strategy={player.strategy_name:16} | "
        f"C={player.cooperations:3d} | "
        f"D={player.defections:3d} | "
        f"C-rate={cooperation_rate * 100:6.2f}%"
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

    total_c = sum(
        player.cooperations
        for player in members
    )

    total_d = sum(
        player.defections
        for player in members
    )

    print(
        f"{strategy_name:16} | "
        f"players={len(members):2d} | "
        f"avg score={average_score:8.2f} | "
        f"C={total_c:4d} | "
        f"D={total_d:4d}"
    )


# ============================================================
# PAYOFF MATRIX
# ============================================================

print()
print("=" * 75)
print("PAYOFF MATRIX")
print("=" * 75)

print()
print("             Opponent")
print("             C       D")
print("Player C     3       0")
print("Player D     5       1")