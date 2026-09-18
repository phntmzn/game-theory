"""
30-PLAYER ULTIMATUM GAME
Using eval() and exec()

Python 3.x

30 players repeatedly play the Ultimatum Game.

Each player has:
    - a strategy
    - a score
    - a proposer behavior
    - a responder behavior

exec() dynamically creates strategy functions.
eval() evaluates game expressions.

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
# STRATEGY EXPRESSIONS
# ============================================================

PROPOSER_EXPRESSIONS = {

    # Offers 45-50% of the pot.
    "fair": """
random.uniform(0.45, 0.50)
""",

    # Offers 10-25%.
    "greedy": """
random.uniform(0.10, 0.25)
""",

    # Offers 25-40%.
    "moderate": """
random.uniform(0.25, 0.40)
""",

    # Completely variable offer.
    "random": """
random.uniform(0.01, 0.99)
""",

    # Adapts to the responder's threshold.
    "strategic": """
min(max(responder_threshold + random.uniform(0.01, 0.05), 0.01), 0.99)
""",
}


RESPONDER_EXPRESSIONS = {

    # Accept almost anything.
    "generous": """
offer >= 0.10
""",

    # Standard threshold.
    "neutral": """
offer >= 0.30
""",

    # Demands at least 40%.
    "strict": """
offer >= 0.40
""",

    # Demands an equal split.
    "egalitarian": """
offer >= 0.50
""",

    # Random acceptance.
    "random": """
random.random() > 0.30
""",
}


# ============================================================
# DYNAMIC FUNCTION GENERATION
# ============================================================

def create_proposer(expression):
    source = f"""
def strategy(random, responder_threshold):
    return {expression}
"""

    namespace = {}

    exec(source, namespace)

    return namespace["strategy"]


def create_responder(expression):
    source = f"""
def strategy(offer, random):
    return {expression}
"""

    namespace = {}

    exec(source, namespace)

    return namespace["strategy"]


proposer_functions = {
    name: create_proposer(expression)
    for name, expression in PROPOSER_EXPRESSIONS.items()
}


responder_functions = {
    name: create_responder(expression)
    for name, expression in RESPONDER_EXPRESSIONS.items()
}


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, player_id):
        self.id = player_id

        self.proposer_strategy = random.choice(
            list(proposer_functions)
        )

        self.responder_strategy = random.choice(
            list(responder_functions)
        )

        self.score = 0.0

        self.accepted = 0
        self.rejected = 0

        self.proposals = 0
        self.total_offered = 0.0

    def __str__(self):
        return (
            f"Player {self.id:02d} | "
            f"score={self.score:8.2f} | "
            f"proposer={self.proposer_strategy:10} | "
            f"responder={self.responder_strategy:11}"
        )


# ============================================================
# CREATE 30 PLAYERS
# ============================================================

players = [
    Player(i + 1)
    for i in range(NUM_PLAYERS)
]


# ============================================================
# PAYOFF EXPRESSIONS
# ============================================================

PROPOSER_ACCEPTED = """
POT - offer
"""

RESPONDER_ACCEPTED = """
offer
"""

PROPOSER_REJECTED = """
0
"""

RESPONDER_REJECTED = """
0
"""


# ============================================================
# EVAL-BASED PAYOFF ENGINE
# ============================================================

def evaluate(expression, offer):

    environment = {
        "POT": POT,
        "offer": offer,
    }

    return eval(
        expression,
        {"__builtins__": {}},
        environment,
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def responder_threshold(strategy):

    thresholds = {
        "generous": 0.10,
        "neutral": 0.30,
        "strict": 0.40,
        "egalitarian": 0.50,
        "random": 0.30,
    }

    return thresholds.get(
        strategy,
        0.30,
    )


def choose_responder(proposer):

    candidates = [
        p
        for p in players
        if p.id != proposer.id
    ]

    return random.choice(candidates)


# ============================================================
# GAME
# ============================================================

for round_number in range(1, ROUNDS + 1):

    random.shuffle(players)

    round_accepted = 0
    round_rejected = 0

    print()
    print("=" * 70)
    print(f"ROUND {round_number}")
    print("=" * 70)

    # Every player gets to propose once.
    for proposer in players:

        responder = choose_responder(proposer)

        proposer_function = proposer_functions[
            proposer.proposer_strategy
        ]

        responder_function = responder_functions[
            responder.responder_strategy
        ]

        threshold = responder_threshold(
            responder.responder_strategy
        )

        # ----------------------------------------------------
        # PROPOSAL
        # ----------------------------------------------------

        fraction = proposer_function(
            random,
            threshold,
        )

        fraction = max(
            0.0,
            min(1.0, fraction),
        )

        offer = POT * fraction

        proposer.proposals += 1
        proposer.total_offered += offer

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        accepted = responder_function(
            fraction,
            random,
        )

        # ----------------------------------------------------
        # PAYOFF
        # ----------------------------------------------------

        if accepted:

            proposer_payoff = evaluate(
                PROPOSER_ACCEPTED,
                offer,
            )

            responder_payoff = evaluate(
                RESPONDER_ACCEPTED,
                offer,
            )

            proposer.score += proposer_payoff
            responder.score += responder_payoff

            proposer.accepted += 1
            responder.accepted += 1

            round_accepted += 1

            result = "ACCEPT"

        else:

            proposer_payoff = evaluate(
                PROPOSER_REJECTED,
                offer,
            )

            responder_payoff = evaluate(
                RESPONDER_REJECTED,
                offer,
            )

            proposer.score += proposer_payoff
            responder.score += responder_payoff

            proposer.rejected += 1
            responder.rejected += 1

            round_rejected += 1

            result = "REJECT"

        # ----------------------------------------------------
        # ROUND EVENT
        # ----------------------------------------------------

        print(
            f"P{proposer.id:02d} "
            f"-> P{responder.id:02d} | "
            f"offer=${offer:6.2f} | "
            f"{result:6} | "
            f"proposer={proposer.proposer_strategy:10} | "
            f"responder={responder.responder_strategy:11}"
        )

    print()
    print(
        f"Accepted: {round_accepted:3d} | "
        f"Rejected: {round_rejected:3d}"
    )


# ============================================================
# FINAL RANKING
# ============================================================

print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)

ranking = sorted(
    players,
    key=lambda player: player.score,
    reverse=True,
)


for position, player in enumerate(ranking, 1):

    acceptance_rate = (
        player.accepted /
        max(1, player.accepted + player.rejected)
    )

    average_offer = (
        player.total_offered /
        max(1, player.proposals)
    )

    print(
        f"{position:02d}. "
        f"P{player.id:02d} | "
        f"score=${player.score:9.2f} | "
        f"accept={acceptance_rate * 100:6.2f}% | "
        f"avg offer=${average_offer:6.2f} | "
        f"prop={player.proposer_strategy:10} | "
        f"resp={player.responder_strategy}"
    )


# ============================================================
# STRATEGY STATISTICS
# ============================================================

print()
print("=" * 70)
print("STRATEGY STATISTICS")
print("=" * 70)


for strategy in proposer_functions:

    matching = [
        p for p in players
        if p.proposer_strategy == strategy
    ]

    if not matching:
        continue

    average_score = (
        sum(p.score for p in matching)
        / len(matching)
    )

    print(
        f"Proposer {strategy:10} | "
        f"players={len(matching):2d} | "
        f"average score=${average_score:9.2f}"
    )


for strategy in responder_functions:

    matching = [
        p for p in players
        if p.responder_strategy == strategy
    ]

    if not matching:
        continue

    average_score = (
        sum(p.score for p in matching)
        / len(matching)
    )

    print(
        f"Responder {strategy:11} | "
        f"players={len(matching):2d} | "
        f"average score=${average_score:9.2f}"
    )