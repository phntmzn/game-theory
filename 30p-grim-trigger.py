"""
30-PLAYER GRIM TRIGGER GAME
Using eval() and exec()

Python 3.x

Each player repeatedly interacts with another player.

Grim Trigger:
    - Cooperate initially.
    - Continue cooperating while the opponent has never defected.
    - If the opponent defects once, defect forever against them.

exec() dynamically creates strategy functions.
eval() evaluates payoff expressions.

Do not use eval()/exec() with untrusted input.
"""

import random


# ============================================================
# CONFIGURATION
# ============================================================

NUM_PLAYERS = 30
ROUNDS = 50

# Prisoner's Dilemma payoff matrix
TEMPTATION = 5
REWARD = 3
PUNISHMENT = 1
SUCKER = 0


# ============================================================
# PAYOFF EXPRESSIONS
# ============================================================

PAYOFF_EXPRESSIONS = {
    "CC": "REWARD",
    "CD": "SUCKER",
    "DC": "TEMPTATION",
    "DD": "PUNISHMENT",
}


# ============================================================
# DYNAMIC GRIM TRIGGER STRATEGY
# ============================================================

GRIM_TRIGGER_CODE = """
def strategy(opponent_id, history):
    if history.get(opponent_id, False):
        return "D"

    return "C"
"""


# ============================================================
# CREATE STRATEGY WITH exec()
# ============================================================

def create_grim_trigger():

    namespace = {}

    exec(
        GRIM_TRIGGER_CODE,
        namespace,
    )

    return namespace["strategy"]


grim_trigger = create_grim_trigger()


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, player_id):

        self.id = player_id

        self.score = 0

        # True means this opponent has defected previously.
        self.grudges = {}

        self.cooperations = 0
        self.defections = 0

        self.games = 0

    def choose_action(self, opponent):

        return grim_trigger(
            opponent.id,
            self.grudges,
        )


# ============================================================
# EVAL PAYOFF ENGINE
# ============================================================

def calculate_payoff(my_action, opponent_action):

    key = my_action + opponent_action

    expression = PAYOFF_EXPRESSIONS[key]

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
# CREATE 30 PLAYERS
# ============================================================

players = [
    Player(i + 1)
    for i in range(NUM_PLAYERS)
]


# ============================================================
# SIMULATION
# ============================================================

for round_number in range(1, ROUNDS + 1):

    print()
    print("=" * 75)
    print(f"ROUND {round_number}")
    print("=" * 75)

    # Randomly pair players.
    shuffled = players.copy()

    random.shuffle(shuffled)

    for i in range(0, NUM_PLAYERS, 2):

        player_a = shuffled[i]
        player_b = shuffled[i + 1]

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        action_a = player_a.choose_action(
            player_b
        )

        action_b = player_b.choose_action(
            player_a
        )

        # ----------------------------------------------------
        # PAYOFFS
        # ----------------------------------------------------

        payoff_a = calculate_payoff(
            action_a,
            action_b,
        )

        payoff_b = calculate_payoff(
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

        if action_b == "D":
            player_a.grudges[player_b.id] = True

        if action_a == "D":
            player_b.grudges[player_a.id] = True

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
        # DISPLAY
        # ----------------------------------------------------

        print(
            f"P{player_a.id:02d} "
            f"{action_a} "
            f"vs "
            f"P{player_b.id:02d} "
            f"{action_b} | "
            f"payoffs="
            f"({payoff_a}, {payoff_b})"
        )


# ============================================================
# FINAL RESULTS
# ============================================================

print()
print("=" * 75)
print("FINAL RESULTS")
print("=" * 75)


ranking = sorted(
    players,
    key=lambda p: p.score,
    reverse=True,
)


for position, player in enumerate(
    ranking,
    start=1,
):

    cooperation_rate = (
        player.cooperations
        / max(1, player.games)
    )

    defection_rate = (
        player.defections
        / max(1, player.games)
    )

    grudges = len(player.grudges)

    print(
        f"{position:02d}. "
        f"P{player.id:02d} | "
        f"score={player.score:5d} | "
        f"games={player.games:3d} | "
        f"C={cooperation_rate * 100:6.2f}% | "
        f"D={defection_rate * 100:6.2f}% | "
        f"grudges={grudges:2d}"
    )


# ============================================================
# GLOBAL STATISTICS
# ============================================================

total_cooperations = sum(
    p.cooperations
    for p in players
)

total_defections = sum(
    p.defections
    for p in players
)

total_games = sum(
    p.games
    for p in players
)


print()
print("=" * 75)
print("GLOBAL STATISTICS")
print("=" * 75)

print(
    f"Total games:          {total_games}"
)

print(
    f"Cooperative actions:  {total_cooperations}"
)

print(
    f"Defective actions:    {total_defections}"
)

print(
    f"Cooperation rate:     "
    f"{total_cooperations / max(1, total_cooperations + total_defections) * 100:.2f}%"
)

print(
    f"Defection rate:       "
    f"{total_defections / max(1, total_cooperations + total_defections) * 100:.2f}%"
)